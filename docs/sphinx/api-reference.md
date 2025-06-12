---
layout: default
title: API Reference
nav_order: 5
---

# API Reference

Complete API documentation generated from docstrings. For the most up-to-date API documentation with full details, see the [Sphinx-generated documentation](https://sail-labs.github.io/rsoft_cad/sphinx/).

## Core Modules

### rsoft_cad.lantern

The main module for creating photonic lanterns.

#### PhotonicLantern
- `PhotonicLantern()` - Main class for creating standard photonic lanterns
- `create_lantern()` - Generate lantern geometry and configuration
- `add_launch_field()` - Add optical launch conditions
- `write()` - Save design to RSoft file format

#### ModeSelectiveLantern
- `ModeSelectiveLantern()` - Specialized class for mode-selective lanterns
- `create_lantern()` - Generate mode-selective lantern geometry
- Inherits from PhotonicLantern with mode-specific optimizations

### rsoft_cad.rsoft_circuit

Core RSoft simulation file generation.

#### RSoftCircuit
- `RSoftCircuit()` - Base class for RSoft simulation files
- Builder pattern with component factories
- Type-safe enums: `TaperType`, `LaunchType`, `MonitorType`

### rsoft_cad.rsoft_simulations

Simulation orchestration and execution.

#### Functions
- `run_simulation()` - Execute RSoft simulations with subprocess management
- Parameter validation and error handling
- Support for BeamPROP and FemSIM packages

### rsoft_cad.beamprop

BeamPROP simulation package integration.

#### Main Functions
- `beamprop_tapered_lantern()` - Run BeamPROP simulations for tapered lanterns
- `plot_combined_monitor_files()` - Analyze and visualize simulation results

### rsoft_cad.femsim

FemSIM simulation package for effective index analysis.

#### Main Functions
- `femsim_tapered_lantern()` - Run FemSIM simulations
- `femsimulation()` - Command-line interface for FemSIM
- `nef_plot()` - Plot effective index results

#### Analysis Modules
- `curve_fitting` - Polynomial fitting for effective index data
- `outlier_detection` - Data cleaning and outlier removal
- `visualisation` - Advanced plotting and analysis tools

### rsoft_cad.utils

Utility functions and helper modules.

#### Configuration Management
- `utils.config.modifier` - JSON configuration loading and modification
  - `load_config()` - Load configuration files
  - `modify_parameter()` - Update configuration parameters
  - `save_config()` - Save modified configurations

#### Fiber Layout
- `utils.fiber_layout.hexagonal` - Hexagonal fiber arrangements
- `utils.fiber_layout.circular` - Circular fiber layouts
- `utils.fiber_layout.visualise_layout` - Layout visualization tools

#### File I/O
- `utils.rsoft_file_io` - RSoft file reading and writing
  - `readers` - Read RSoft output files
  - `writers` - Write RSoft input files
  - `finders` - Locate and search files

#### Plotting
- `utils.rsoft_file_plot` - Visualization tools
  - `field_plots` - Field distribution plotting
  - `monitor_plots` - Monitor data visualization
  - `combined_field_plots` - Multi-panel field plots

## Advanced Modules

### rsoft_cad.geometry

Geometric modeling and taper design.

#### Classes
- `CustomTaper` - Custom taper profile definitions
- Taper calculation utilities

### rsoft_cad.optimisation

Optimization algorithms and cost functions.

#### Modules
- `genetic_algorithm` - Genetic algorithm optimization
- `cost_function` - Cost function definitions for optimization

### rsoft_cad.layout

Specialized layout generation.

#### Functions
- `mode_selective_layout` - Layout algorithms for mode-selective lanterns

## Constants and Utilities

### rsoft_cad.constants

Important physical and simulation constants.

- `SINGLE_MODE_FIBERS` - Database of standard fiber parameters
- Default wavelengths and refractive indices

### rsoft_cad.utils.lp_modes

LP mode calculations and utilities.

#### Functions
- `calculate_mode_cutoff()` - Mode cutoff frequency calculations
- LP mode definitions and properties

## Configuration System

The configuration system uses JSON files with hierarchical structure:

```python
{
  "pl_params": {
    "Num_Cores_Ring": 6,
    "Core_Diameter": 8.2,
    "Taper_Length": 50000,
    "Taper_Factor": 12
  },
  "simulation": {
    "wavelength": 1550,
    "grid_size": 0.1
  }
}
```

### Parameterized Expressions

Configuration supports dynamic expressions:
- `"360 / Num_Cores_Ring"` - Automatic angle calculation
- `"Core_Diameter * 1.5"` - Derived parameters

## Error Handling

### Common Exceptions

- `ConfigurationError` - Invalid configuration parameters
- `SimulationError` - Simulation execution failures
- `FileFormatError` - Invalid file formats

### Best Practices

1. **Parameter Validation**: Always validate parameters before simulation
2. **Error Checking**: Check return codes from simulations
3. **Resource Management**: Monitor memory usage for large simulations
4. **Logging**: Use built-in logging for debugging

## Type Hints

RSoft PLTools uses type hints throughout for better IDE support:

```python
from typing import Dict, List, Optional, Tuple
from rsoft_cad.lantern import PhotonicLantern

def create_custom_lantern(
    config: Dict[str, Any],
    output_path: str,
    taper_length: Optional[float] = None
) -> Tuple[PhotonicLantern, Dict[str, Any]]:
    # Implementation
    pass
```

## Extension Points

### Custom Lantern Types

Register new lantern types using the registry system:

```python
from rsoft_cad.simulations.parameterised_lanterns import register_lantern_type

@register_lantern_type("my_custom_lantern")
class MyCustomLantern(PhotonicLantern):
    def create_lantern(self, **kwargs):
        # Custom implementation
        pass
```

### Custom File Formats

Extend file I/O for new formats:

```python
from rsoft_cad.utils.rsoft_file_io.writers import register_writer

@register_writer(".myformat")
def write_my_format(data, filepath):
    # Custom writer implementation
    pass
```

## Performance Considerations

### Large Simulations
- Use chunked parameter sweeps for memory management
- Consider parallel processing for independent simulations
- Monitor disk space for output files

### Optimization
- Cache configuration objects for repeated use
- Pre-validate parameters before batch processing
- Use appropriate grid resolutions for simulation accuracy vs. speed

For detailed function signatures, parameters, and examples, please refer to the individual module documentation in the [Sphinx documentation](https://sail-labs.github.io/rsoft_cad/sphinx/).