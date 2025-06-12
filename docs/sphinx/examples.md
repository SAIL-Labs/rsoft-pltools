---
layout: default
title: Examples
nav_order: 6
---

# Examples

This section provides practical examples demonstrating how to use RSoft PLTools for various photonic lantern design and simulation tasks.

## Basic Photonic Lantern Creation

### Simple Photonic Lantern

```python
from rsoft_cad.lantern import PhotonicLantern
from rsoft_cad.utils.config.modifier import load_config

# Load default configuration
config = load_config("config/default_config.json")

# Create a basic photonic lantern
lantern = PhotonicLantern()
core_map = lantern.create_lantern(
    config=config,
    highest_mode="LP02",
    taper_factor=10,
    taper_length=50000
)

# Save the design
lantern.write("basic_lantern.ind")
print(f"Created lantern with {len(core_map)} cores")
```

### Mode Selective Lantern

```python
from rsoft_cad.lantern import ModeSelectiveLantern

# Create mode selective lantern for LP11 mode
mspl = ModeSelectiveLantern()
core_map = mspl.create_lantern(
    highest_mode="LP11",
    launch_mode="LP01", 
    taper_factor=8,
    taper_length=60000
)

# Add launch field
mspl.add_launch_field(
    launch_type="LP01",
    power=1.0,
    position=(0, 0)
)

mspl.write("mode_selective_lantern.ind")
```

## Configuration Management

### Custom Configuration

```python
from rsoft_cad.utils.config.modifier import load_config, modify_parameter, save_config

# Load base configuration
config = load_config("config/complete_pl_config.json")

# Customize parameters
config = modify_parameter(config, "pl_params.Num_Cores_Ring", 6)
config = modify_parameter(config, "pl_params.Core_Diameter", 8.5)
config = modify_parameter(config, "pl_params.Taper_Length", 45000)

# Save custom configuration
save_config(config, "my_custom_config.json")

# Use in lantern creation
lantern = PhotonicLantern()
lantern.create_lantern(config=config)
lantern.write("custom_lantern.ind")
```

## Simulation and Analysis

### Running BeamPROP Simulation

```python
from rsoft_cad.rsoft_simulations import run_simulation

# Run simulation
result = run_simulation(
    design_filepath="./",
    design_filename="basic_lantern.ind",
    sim_package="bsimw32",
    prefix_name="example_sim",
    save_folder="simulation_results"
)

if result.returncode == 0:
    print("Simulation completed successfully!")
    print(f"Results saved in: simulation_results/")
else:
    print(f"Simulation failed: {result.stderr}")
```

### Parameter Sweep

```python
from rsoft_cad.beamprop import beamprop_tapered_lantern
import numpy as np

# Define parameter range
taper_lengths = np.linspace(30000, 70000, 5)
results = []

for i, length in enumerate(taper_lengths):
    print(f"Running simulation {i+1}/{len(taper_lengths)}")
    
    core_map = beamprop_tapered_lantern(
        expt_dir="parameter_sweep",
        opt_name=f"tl_{length:.0f}",
        taper_factor=12,
        taper_length=length,
        highest_mode="LP02",
        launch_mode="LP01"
    )
    
    results.append({
        'taper_length': length,
        'num_cores': len(core_map)
    })

print(f"Completed {len(results)} simulations")
```

### Analyzing Results

```python
from rsoft_cad.beamprop.beamprop_plot_util import plot_combined_monitor_files

# Plot and analyze results
fig, ax, combined_df, final_values, summary, optimal_taper, optimal_value = plot_combined_monitor_files(
    "parameter_sweep/rsoft_data_files",
    save_plot=True,
    plot_filename="sweep_analysis"
)

print(f"Optimal taper length: {optimal_taper}")
print(f"Best coupling efficiency: {optimal_value:.3f}")
```

## Effective Index Analysis with FemSIM

### FemSIM Simulation

```python
from rsoft_cad.femsim import femsim_tapered_lantern

# Run FemSIM for effective index analysis
femsim_tapered_lantern(
    expt_dir="neff_study",
    taper_factor=15,
    taper_length=50000,
    num_points=100,
    highest_mode="LP02",
    launch_mode="LP01"
)
```

### Visualizing Effective Index Data

```python
from rsoft_cad.femsim.visualisation import plot_combined_nef_files
import matplotlib.pyplot as plt

# Plot effective index evolution
fig = plot_combined_nef_files(
    folder_path="neff_study/rsoft_data_files",
    plot_type="real",
    save_plot=True,
    max_indices=12,
    remove_outliers=True,
    fit_data=True,
    colormap="viridis"
)

plt.title("Effective Index Evolution Along Taper")
plt.xlabel("Z Position (μm)")
plt.ylabel("Effective Index")
plt.show()
```

## Layout Visualization

### Fiber Layout Visualization

```python
from rsoft_cad.utils.fiber_layout import visualise_layout
import matplotlib.pyplot as plt

# Create and visualize lantern
lantern = PhotonicLantern()
core_map = lantern.create_lantern(
    highest_mode="LP02",
    taper_length=40000
)

# Visualize the layout
fig = visualise_layout(
    core_map, 
    show_indices=True,
    core_color='blue',
    capillary_color='lightgray'
)

plt.title("Photonic Lantern Cross-Section")
plt.axis('equal')
plt.show()
```

## Command Line Interface Examples

### FemSIM Parameter Scan

```bash
# Run FemSIM simulation with specific parameters
python -c "from rsoft_cad.femsim import femsimulation; femsimulation()" \
    --taper-factors 18.75 \
    --taper-length 40000 \
    --num-grids 200 \
    --num-points 150 \
    --mode-output OUTPUT_NONE
```

### Plotting Effective Index Results

```bash
# Plot and analyze effective index data
python -c "from rsoft_cad.femsim import nef_plot; nef_plot()" \
    --folder-path femsim_run_001 \
    --plot-type real \
    --fit-data \
    --remove-outliers
```

## Advanced Examples

### Custom Taper Profile

```python
from rsoft_cad.geometry.custom_taper import CustomTaper
import numpy as np

# Define custom exponential taper
def exponential_taper(z, z_start, z_end, r_start, r_end, alpha=1.5):
    if z < z_start or z > z_end:
        return r_start if z < z_start else r_end
    
    normalized_z = (z - z_start) / (z_end - z_start)
    return r_start * np.exp(-alpha * normalized_z) + r_end * (1 - np.exp(-alpha * normalized_z))

# Create custom taper
taper = CustomTaper(
    taper_function=exponential_taper,
    start_position=10000,
    end_position=60000,
    start_radius=25.0,
    end_radius=8.0
)

# Use in lantern design
lantern = PhotonicLantern()
core_map = lantern.create_lantern(
    highest_mode="LP02",
    custom_taper=taper
)
```

### Batch Processing Multiple Configurations

```python
import json
from pathlib import Path

# Define multiple configurations
configurations = [
    {"taper_length": 30000, "taper_factor": 10, "highest_mode": "LP01"},
    {"taper_length": 50000, "taper_factor": 15, "highest_mode": "LP11"},
    {"taper_length": 70000, "taper_factor": 20, "highest_mode": "LP02"},
]

results = []

for i, config in enumerate(configurations):
    print(f"Processing configuration {i+1}/{len(configurations)}")
    
    # Create lantern
    lantern = PhotonicLantern()
    core_map = lantern.create_lantern(**config)
    
    # Save design
    output_path = f"batch_design_{i}.ind"
    lantern.write(output_path)
    
    # Run simulation
    result = run_simulation(
        design_filepath="./",
        design_filename=output_path,
        sim_package="bsimw32",
        prefix_name=f"batch_{i}"
    )
    
    # Store results
    results.append({
        "config": config,
        "output_file": output_path,
        "simulation_success": result.returncode == 0,
        "num_cores": len(core_map)
    })

# Save batch results
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Batch processing completed!")
```

## Integration with External Tools

### Exporting to Other Formats

```python
import pandas as pd

# Export core positions for external analysis
def export_core_positions(core_map, filename):
    data = []
    for core_id, core_info in core_map.items():
        data.append({
            'core_id': core_id,
            'x_position': core_info['x'],
            'y_position': core_info['y'],
            'diameter': core_info.get('diameter', 'N/A'),
            'type': core_info.get('type', 'core')
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Core positions exported to {filename}")

# Use the function
lantern = PhotonicLantern()
core_map = lantern.create_lantern(highest_mode="LP02")
export_core_positions(core_map, "core_positions.csv")
```

## Tips for Success

1. **Start Simple**: Begin with basic configurations before attempting complex designs
2. **Parameter Validation**: Always validate your parameters before running simulations
3. **Incremental Development**: Build and test your designs incrementally
4. **Resource Management**: Monitor computational resources for large parameter sweeps
5. **Documentation**: Keep track of successful configurations for future reference

For more examples, check the `examples/` directory in the repository.