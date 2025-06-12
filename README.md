# RSoft PLTools - Photonic Lantern Simulation Toolkit

[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://sail-labs.github.io/rsoft_cad/)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

RSoft PLTools is a comprehensive Python package for designing, simulating, and analysing photonic lanterns - specialised optical components that enable efficient coupling between multimode and single-mode optical systems. This toolkit provides tools for designing various lantern configurations, running optical simulations, and analysing results.

📖 **[View Full Documentation](https://sail-labs.github.io/rsoft_cad/)**

## Features

### Key Capabilities
- Multi-core fibre and photonic lantern design
- Mode selective lantern (MSL) generation
- Flexible configuration management
- Simulation file generation for RSoft CAD
- Geometric layout visualisation
- Parametric design exploration
- Advanced mode analysis

### Supported Functionalities
- Hexagonal and circular fibre layouts
- Mode coupling analysis
- Customisable fibre parameters
- Automated lantern geometry calculations
- Simulation file generation for BeamPROP and FemSIM
- Effective refractive index calculation and analysis
- Taper length optimisation

## Installation

```bash
# Clone the repository
git clone https://github.com/SAIL-Labs/rsoft_cad.git
cd rsoft_cadr

# Install in development mode
pip install -e .
```

## Core Modules

### Core Functionality
- Multi-core fibre and photonic lantern design
- Mode selective lantern (MSL) generation
- Flexible configuration management
- Simulation file generation for RSoft CAD
- Geometric layout visualisation
- Parametric design exploration
- Advanced mode analysis

### Layout Options
- Hexagonal and circular fibre layouts
- Customisable fibre parameters
- Automated lantern geometry calculations
- Flexible core diameter and refractive index settings
- Multiple LP mode support (LP01, LP11, LP21, LP02, etc.)

### Simulation Capabilities
- Simulation file generation for BeamPROP and FemSIM
- Effective refractive index calculation and analysis
- Mode coupling analysis
- Automatic mode cutoff frequency management
- Field propagation modelling

### Optimisation
- Taper length optimisation algorithms
- Parameter sweep functionality
- Outlier detection and filtering for data processing
- Finding optimal configurations for mode coupling

### Analysis Tools
- Enhanced visualisation for field distributions
- Effective index analysis plots
- Parameter sweep results visualisation
- Data export capabilities for various formats
- Result processing utilities

### Interface Options
- Command-line interface for complex simulations
- Python API for script-based automation
- Configuration file management

## Example Usage

### Creating and Simulating a Mode Selective Lantern

```python
from rsoft_cadr.rsoft_mspl import ModeSelectiveLantern
from rsoft_cadr.rsoft_simulations import run_simulation
import os

# Create a mode selective lantern
mspl = ModeSelectiveLantern()
core_map = mspl.create_lantern(
    highest_mode="LP11",
    launch_mode="LP01",
    taper_factor=5,
    taper_length=80000,
    savefile=True  # Ensure the file is saved for simulation
)

# Run simulation
filepath = mspl.design_filepath
filename = mspl.design_filename

# Simulate the lantern design
simulation_result = run_simulation(
    filepath,
    filename,
    sim_package="bsimw32",
    prefix_name=f"LP01_taper_80000",
    save_folder="mode_selective_lantern_simulations",
    hide_sim=True
)

# Optional: Check simulation output
print(f"Simulation completed with return code: {simulation_result.returncode}")
print("Simulation stdout:", simulation_result.stdout)
print("Simulation stderr:", simulation_result.stderr)
```

### Performing Parameter Sweeps

```python
from rsoft_cadr.beamprop import beamprop_tapered_lantern
import numpy as np

# Define taper lengths to analyse
taper_lengths = np.linspace(20000, 80000, 20)

# Run simulations for different taper lengths
for i, taper_length in enumerate(taper_lengths):
    core_map = beamprop_tapered_lantern(
        expt_dir="output/taper_length_sweep",
        opt_name=f"run_{i:03d}",
        taper_factor=15,
        taper_length=taper_length,
        highest_mode="LP02",
        launch_mode="LP02",
        result_files_prefix=f"run_{i:03d}"
    )

# Analyse the results
from rsoft_cadr.beamprop import plot_combined_monitor_files
fig, ax, combined_df, final_values, summary, optimal_taper, optimal_value = plot_combined_monitor_files(
    "output/taper_length_sweep/rsoft_data_files"
)
```

### Using Configuration Files

```python
from rsoft_cadr.utils.config.modifier import load_config, modify_parameter, save_config

# Load the default configuration
config = load_config("config/complete_pl_config.json")

# Modify parameters
config = modify_parameter(config, "pl_params.Num_Cores_Ring", 6)
config = modify_parameter(config, "pl_params.Taper_Length", 60000)

# Save the modified configuration
save_config(config, "config/custom_config.json")

# Use the custom configuration
from photonic_lantern import create_photonic_lantern
create_photonic_lantern(config, "output/custom_lantern.ind")
```

### Analysing Effective Refractive Index

```python
from rsoft_cadr.femsim import femsim_tapered_lantern, nef_plot
from rsoft_cadr.femsim.visualisation import plot_combined_nef_files
import matplotlib.pyplot as plt

# Run FemSIM simulation for effective index analysis
femsim_tapered_lantern(
    expt_dir="output/neff_scan",
    taper_factor=13,
    taper_length=50000,
    num_points=100,
    highest_mode="LP02",
    launch_mode="LP01"
)

data_folder = "output/neff_scan/rsoft_data_files"
fig = plot_combined_nef_files(
    folder_path=data_folder,
    include_subfolders=False,
    plot_type="real",  # Options: "real", "imag", or "both"
    save_plot=False,
    max_indices=12,
    use_filename_as_x=True,
    remove_outliers=True,
    window_size=5000,
    z_threshold=3.0,
    colormap="managua",
    plot_indices=None,  # Optionally specify indices to plot
    fit_data=True,
    fit_function=None,  # Will use default polynomial fitting
)

plt.show()
```

Alternatively, we can simulate, plot and analyse effective indices using the command-line interface

```bash
# Run FemSIM simulation
python -c "from rsoft_cadr.femsim import femsimulation; femsimulation()" \
    --taper-factors 18.75 \
    --taper-length 40000 \
    --num-grids 200 \
    --num-points 200 \
    --mode-output OUTPUT_NONE
# Plot effective indices
python -c "from rsoft_cadr.femsim import nef_plot; nef_plot()" \
    --folder-path femsim_run_001 \
    --plot-type real \
    --fit-data
```

## Visualisation

The toolkit provides visualisation utilities:
- Hexagonal fibre layout plotting
- Mode positioning visualisation
- Capillary and core diameter representations
- Effective index analysis plots
- Field distribution visualisation

## Requirements

- Python 3.6+
- NumPy 1.2+
- Matplotlib 2.0+
- Pandas
- SciPy
- Seaborn
- RSoft CAD (for simulations)

## Documentation

Complete documentation is available at **[https://sail-labs.github.io/rsoft_cad/](https://sail-labs.github.io/rsoft_cad/)**

### Quick Links
- 📖 [Installation Guide](https://sail-labs.github.io/rsoft_cad/installation.html)
- 🚀 [Quick Start](https://sail-labs.github.io/rsoft_cad/quick-start.html)
- 📚 [Tutorials](https://sail-labs.github.io/rsoft_cad/tutorials.html)
- 🔧 [API Reference](https://sail-labs.github.io/rsoft_cad/api-reference.html)
- 💡 [Examples](https://sail-labs.github.io/rsoft_cad/examples.html)

### Building Documentation Locally

To build the documentation locally:

```bash
# Install documentation dependencies
conda activate rsoft-tools
conda install sphinx sphinx_rtd_theme myst-parser -c conda-forge

# Build documentation
cd docs
./build_docs.sh
```

The documentation will be available at `docs/_build/html/index.html`.

## Contact

Kok-Wei Bong - kok-wei.bong@sydney.edu.au