# Import required libraries
import os
import numpy as np
import json
import logging
from typing import Union, List, Dict, Tuple, Any, Optional
from functools import partial

# Import custom modules
from rsoft_cad.lantern import ModeSelectiveLantern, PhotonicLantern
from rsoft_cad.rsoft_simulations import run_simulation
from rsoft_cad.utils import interpolate_taper_value
from rsoft_cad.geometry import calculate_taper_properties
from rsoft_cad import LaunchType, MonitorType, TaperType


# Simple registry - just a dictionary mapping lantern types to their classes
LANTERN_REGISTRY = {
    "mode_selective": {
        "class": ModeSelectiveLantern,
        "default_launch_mode": "LP01",
        "file_prefix": "mspl",
        "required_params": ["highest_mode"],
        "create_method_param": "highest_mode",  # The parameter name for create_lantern()
    },
    "photonic": {
        "class": PhotonicLantern,
        "default_launch_mode": "0",
        "file_prefix": "photonic_lantern",
        "required_params": ["layer_config"],
        "create_method_param": "layer_config",
    },
    # Adding new lantern types is just adding entries here!
    # "new_lantern_type": {
    #     "class": NewLanternClass,
    #     "default_launch_mode": "default_mode",
    #     "file_prefix": "new_lantern",
    #     "required_params": ["required_param1", "required_param2"],
    #     "create_method_param": "main_config_param"
    # }
}


def register_lantern_type(
    name: str,
    lantern_class,
    default_launch_mode: str,
    file_prefix: str,
    required_params: List[str],
    create_method_param: str,
):
    """
    Register a new lantern type. Call this to add new lantern types without modifying this file.

    Args:
        name: Name to use for the lantern type (e.g., "my_custom_lantern")
        lantern_class: The lantern class (e.g., MyCustomLantern)
        default_launch_mode: Default launch mode for this lantern type
        file_prefix: Prefix for output files
        required_params: List of required parameter names
        create_method_param: Main parameter name to pass to create_lantern()

    Example:
        register_lantern_type(
            name="fiber_bundle",
            lantern_class=FiberBundleLantern,
            default_launch_mode="bundle_01",
            file_prefix="fiber_bundle",
            required_params=["bundle_config"],
            create_method_param="bundle_config"
        )
    """
    LANTERN_REGISTRY[name] = {
        "class": lantern_class,
        "default_launch_mode": default_launch_mode,
        "file_prefix": file_prefix,
        "required_params": required_params,
        "create_method_param": create_method_param,
    }


def make_parameterised_lantern(
    lantern_type: str,
    # Common parameters for all lantern types
    launch_mode: Optional[Union[str, List[str]]] = None,
    opt_name: str = "run_000",
    taper_factor: float = 21,
    taper_length: float = 80000,
    sim_type: str = "beamprop",
    femnev: int = 1,
    save_neff: bool = True,
    step_x: Optional[float] = None,
    step_y: Optional[float] = None,
    domain_min: float = 0,
    data_dir: str = "output",
    expt_dir: str = "pl_property_scan",
    mode_output: str = "OUTPUT_REAL_IMAG",
    core_dia_dict: Optional[Dict[str, float]] = None,
    cladding_dia_dict: Optional[Dict[str, float]] = None,
    bg_index_dict: Optional[Dict[str, float]] = None,
    cladding_index_dict: Optional[Dict[str, float]] = None,
    core_index_dict: Optional[Dict[str, float]] = None,
    monitor_type: MonitorType = MonitorType.FIBER_POWER,
    launch_type: LaunchType = LaunchType.GAUSSIAN,
    taper_config: Union[TaperType, Dict[str, TaperType]] = TaperType.linear(),
    capillary_od: float = 900,
    final_capillary_id: float = 40,
    num_points: int = 100,
    num_grid: int = 200,
    num_pads: int = 50,
    sort_neff: int = 1,  # [0=none, 1=highest, 2=lowest]
    **lantern_specific_kwargs,  # All lantern-specific parameters go here
) -> Tuple[str, str, Dict[str, Tuple[float, float]]]:
    """
    Create a parameterised photonic lantern configuration with specified properties.

    This function creates any type of photonic lantern using a simple registry pattern.
    Adding new lantern types only requires updating the LANTERN_REGISTRY or calling
    register_lantern_type().

    Args:
        lantern_type (str): Type of lantern to create (e.g., "mode_selective", "photonic")
        launch_mode (str | List[str] | None): The mode(s) to launch from (None uses lantern default)
        opt_name (str): Name identifier for the run (default: "run_000")
        taper_factor (float): The factor by which the fibers are tapered (default: 21)
        taper_length (float): The length of the taper in microns (default: 80000)
        sim_type (str): Simulation type, either "beamprop" or "femsim" (default: "beamprop")
        femnev (int): Number of eigenmodes to find in FEM simulation (default: 1)
        save_neff (bool): Whether to save effective indices (default: True)
        step_x (float | None): Step size in x-direction. If None, calculated from num_grid (default: None)
        step_y (float | None): Step size in y-direction. If None, calculated from num_grid (default: None)
        domain_min (float): Minimum domain boundary in microns (default: 0)
        data_dir (str): Parent directory for outputs (default: "output")
        expt_dir (str): Sub-directory for experiment outputs (default: "pl_property_scan")
        num_grid (int): Number of grid points for simulation (default: 200)
        mode_output (str): Output format for simulation modes (default: "OUTPUT_REAL_IMAG")
        core_dia_dict (Dict[str, float] | None): Dictionary mapping modes to core diameters (default: None)
        cladding_dia_dict (Dict[str, float] | None): Dictionary mapping modes to cladding diameters (default: None)
        bg_index_dict (Dict[str, float] | None): Dictionary mapping modes to background indices (default: None)
        cladding_index_dict (Dict[str, float] | None): Dictionary mapping modes to cladding indices (default: None)
        core_index_dict (Dict[str, float] | None): Dictionary mapping modes to core indices (default: None)
        monitor_type (MonitorType): Type of monitor to add to each pathway. Defaults to FIBER_POWER.
        taper_config (TaperType | Dict[str, TaperType]): Taper profile to use if tapering is applied. Defaults to LINEAR.
        launch_type (LaunchType): Type of field distribution to launch. Defaults to GAUSSIAN.
        capillary_od (float): Outer diameter of the capillary in microns (default: 900)
        final_capillary_id (float): Final inner diameter of the capillary after tapering in microns (default: 40)
        num_points (int): Number of points along z-axis for model discretization (default: 100)
        num_pads (int): Number of padding grid points (default: 50)
        sort_neff (int): Eigenmode sorting option [0=none, 1=highest, 2=lowest] (default: 1)
        **lantern_specific_kwargs: Lantern-specific parameters:
            For mode_selective: highest_mode (str)
            For photonic: layer_config (List[Tuple[int, float]])
            For custom types: whatever parameters they need

    Returns:
        Tuple[str, str, Dict[str, Tuple[float, float]]]: A tuple containing:
            - filepath (str): Path to the directory containing the generated design file
            - file_name (str): Name of the generated design file
            - core_map (Dict[str, Tuple[float, float]]): Mapping of modes to their spatial coordinates

    Raises:
        ValueError: If an invalid simulation type or lantern type is provided
        ValueError: If required parameters for the selected lantern type are missing
    """

    # Set up logger
    logger = logging.getLogger(__name__)

    # Validate lantern type
    if lantern_type not in LANTERN_REGISTRY:
        available_types = list(LANTERN_REGISTRY.keys())
        raise ValueError(
            f"Unknown lantern type: {lantern_type}. Available types: {available_types}"
        )

    lantern_info = LANTERN_REGISTRY[lantern_type]

    # Check required parameters
    missing_params = []
    for param in lantern_info["required_params"]:
        if param not in lantern_specific_kwargs:
            missing_params.append(param)

    if missing_params:
        raise ValueError(
            f"Missing required parameters for {lantern_type}: {missing_params}"
        )

    logger.info(
        f"Creating parameterised {lantern_info['file_prefix']} lantern with name: {opt_name}"
    )

    # Validate simulation type
    if sim_type == "beamprop":
        sim_string = "ST_BEAMPROP"
    elif sim_type == "femsim":
        sim_string = "ST_FEMSIM"
    else:
        raise ValueError(
            f"Invalid simulation type: {sim_type}. Expected 'femsim' or 'beamprop'."
        )

    # Create lantern instance
    lantern = lantern_info["class"]()
    logger.debug(f"Created {lantern_info['class'].__name__} instance")

    # Use default launch mode if none provided
    if launch_mode is None:
        launch_mode = lantern_info["default_launch_mode"]
        logger.debug(f"Using default launch_mode: {launch_mode}")

    # Prepare parameters for create_lantern - common parameters first
    create_params = {
        "launch_mode": launch_mode,
        "opt_name": opt_name,
        "savefile": False,  # Hold off on saving design file
        "taper_factor": taper_factor,
        "taper_length": taper_length,
        "core_dia_dict": core_dia_dict,
        "cladding_dia_dict": cladding_dia_dict,
        "bg_index_dict": bg_index_dict,
        "cladding_index_dict": cladding_index_dict,
        "core_index_dict": core_index_dict,
        "monitor_type": monitor_type,
        "launch_type": launch_type,
        "taper_config": taper_config,
        "capillary_od": capillary_od,
        "final_capillary_id": final_capillary_id,
        "num_points": num_points,
    }

    # Add the main lantern-specific parameter
    main_param = lantern_info["create_method_param"]
    create_params[main_param] = lantern_specific_kwargs[main_param]

    # Add any other lantern-specific parameters that the create_lantern method accepts
    # This allows for future flexibility without breaking existing code
    remaining_kwargs = {
        k: v for k, v in lantern_specific_kwargs.items() if k != main_param
    }
    create_params.update(remaining_kwargs)

    # Create the lantern
    logger.debug(
        f"Creating {lantern_type} lantern with main param: {main_param}={lantern_specific_kwargs[main_param]}"
    )
    core_map = lantern.create_lantern(**create_params)

    logger.debug(f"Lantern created with {len(core_map)} cores")

    # Calculate simulation boundaries (same logic as before)
    if taper_factor > 1:  # backwards compatibility
        (dia_at_pos, _, taper_factor, _) = calculate_taper_properties(
            position=domain_min,
            start_dia=lantern.cap_dia,
            end_dia=None,
            taper_factor=taper_factor,
            taper_length=taper_length,
        )
    else:
        dia_at_pos = interpolate_taper_value(
            lantern.model,
            "capillary_inner_diameter",
            z_pos=domain_min,
        )

    core_pos_x = 0
    core_pos_y = 0

    # Calculate boundaries
    boundary_max = np.ceil(core_pos_x + (dia_at_pos / 2))
    boundary_min = np.floor(core_pos_x - (dia_at_pos / 2))
    boundary_max_y = np.ceil(core_pos_y + (dia_at_pos / 2))
    boundary_min_y = np.floor(core_pos_y - (dia_at_pos / 2))

    grid_size_x = step_x if step_x is not None else (2 * boundary_max) / num_grid
    grid_size_y = step_y if step_y is not None else (2 * boundary_max_y) / num_grid

    logger.debug(f"Grid sizes calculated: x={grid_size_x}, y={grid_size_y}")

    # Add padding
    boundary_min_y -= int(num_pads * 1.5) * grid_size_y
    boundary_max_y += num_pads * grid_size_y
    boundary_min -= num_pads * grid_size_x
    boundary_max += num_pads * grid_size_x

    # Simulation parameters
    sim_params = {
        "boundary_max": boundary_max,
        "boundary_min": boundary_min,
        "boundary_max_y": boundary_max_y,
        "boundary_min_y": boundary_min_y,
        "domain_min": domain_min,
        "grid_size": grid_size_x,
        "grid_size_y": grid_size_y,
        "grid_align_x": 1,
        "grid_align_y": 1,
        "sim_tool": sim_string,
        "fem_nev": femnev,
        "fem_neff_seeding": int(save_neff),
        "mode_output_format": mode_output,
        "slice_display_mode": "DISPLAY_CONTOURMAPXY",
        "field_output_format": "OUTPUT_REAL_IMAG",
        "mode_launch_type": 2,
        "cad_aspectratio_x": 50,
        "cad_aspectratio_y ": 50,
        "fem_outh": 0,
        "fem_outs": 0,
        "fem_plot_mesh": 0,
        "fem_save_meshfile": 0,
        "fem_leaky": 1,
        "fem_float": 0,
        "fem_sortev": sort_neff,
    }

    # Update global simulation parameters
    lantern.update_global_params(**sim_params)

    # Generate filename
    file_name = (
        f"{sim_type}_{lantern_info['file_prefix']}_{len(core_map)}_cores_{opt_name}.ind"
    )
    filepath = os.path.join(data_dir, expt_dir)
    design_filename = os.path.join(filepath, file_name)

    # Create directory if it doesn't exist
    os.makedirs(filepath, exist_ok=True)

    # Write design file
    logger.info(f"Writing design file to {design_filename}")
    lantern.write(design_filename)

    # Save the input parameters to a file
    params = {
        "lantern_type": lantern_type,
        "boundary_max": boundary_max,
        "boundary_min": boundary_min,
        "boundary_max_y": boundary_max_y,
        "boundary_min_y": boundary_min_y,
        "domain_min": domain_min,
        "grid_size": grid_size_x,
        "grid_size_y": grid_size_y,
        "launch_mode": launch_mode,
        "opt_name": opt_name,
        "taper_factor": taper_factor,
        "taper_length": taper_length,
        "sim_type": sim_type,
        "femnev": femnev,
        "save_neff": save_neff,
        "step_x": step_x,
        "step_y": step_y,
        "domain_min": domain_min,
        "data_dir": data_dir,
        "expt_dir": expt_dir,
        "num_grid": num_grid,
    }

    # Add all lantern-specific parameters to saved params
    params.update(lantern_specific_kwargs)

    # Generate params filename
    params_filename = os.path.join(data_dir, expt_dir, f"params_{opt_name}.json")

    # Write parameters to file
    logger.info(f"Saving parameters to {params_filename}")
    with open(params_filename, "w") as f:
        json.dump(params, f, indent=4)

    logger.info(f"Lantern creation complete: {file_name}")

    return filepath, file_name, core_map


# Convenience functions for backward compatibility and ease of use
def make_mode_selective_lantern(highest_mode: str = "LP02", **kwargs):
    """Convenience function for creating mode selective lanterns."""
    return make_parameterised_lantern(
        "mode_selective", highest_mode=highest_mode, **kwargs
    )


def make_photonic_lantern(layer_config: List[Tuple[int, float]], **kwargs):
    """Convenience function for creating photonic lanterns."""
    return make_parameterised_lantern("photonic", layer_config=layer_config, **kwargs)


if __name__ == "__main__":
    # Example 1: Mode Selective Lantern
    filepath, filename, core_map = make_parameterised_lantern(
        "mode_selective",
        highest_mode="LP02",
        launch_mode="LP01",
        taper_factor=1,
        sim_type="femsim",
        femnev=6,
        taper_length=50000,
        expt_dir="mode_selective_test",
        taper_config={
            "core": TaperType.exponential(),
            "cladding": TaperType.exponential(),
            "cap": TaperType.exponential(),
        },
        domain_min=25000,
        opt_name="mspl_test_run",
    )

    # Example 2: Photonic Lantern
    filepath, filename, core_map = make_parameterised_lantern(
        "photonic",
        layer_config=[
            (1, 1.0),  # Center layer: 1 circle at center
            (6, 1.0),  # First ring: 6 circles
            (12, 1.0),  # Second ring: 12 circles
        ],
        taper_factor=1,
        sim_type="femsim",
        femnev=6,
        taper_length=50000,
        expt_dir="photonic_test",
        domain_min=25000,
        opt_name="pl_test_run",
    )

    # Example 3: Using convenience functions
    filepath, filename, core_map = make_mode_selective_lantern(
        highest_mode="LP11", opt_name="convenience_test"
    )

    # Example 4: Adding a new lantern type (would be done in external code)
    # register_lantern_type(
    #     name="fiber_bundle",
    #     lantern_class=FiberBundleLantern,  # Your custom class
    #     default_launch_mode="bundle_01",
    #     file_prefix="fiber_bundle",
    #     required_params=["bundle_config"],
    #     create_method_param="bundle_config"
    # )
    #
    # # Then use it
    # make_parameterised_lantern("fiber_bundle", bundle_config=my_config, opt_name="bundle_test")
