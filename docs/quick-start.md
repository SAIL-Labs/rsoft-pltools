---
layout: default
title: Quick Start
nav_order: 3
---

# Quick Start Guide

This guide will get you up and running with RSoft CAD in minutes.

## Basic Concepts

RSoft CAD is organized around three main concepts:

1. **Photonic Lanterns** - The optical devices you're designing
2. **Simulations** - Running optical analysis on your designs
3. **Analysis** - Processing and visualizing results

## Your First Photonic Lantern

### 1. Create a Simple Photonic Lantern

```python
from rsoft_cad.lantern import PhotonicLantern
from rsoft_cad.utils.config.modifier import load_config

# Load the default configuration
config = load_config("config/default_config.json")

# Create a photonic lantern
lantern = PhotonicLantern()
core_map = lantern.create_lantern(
    config=config,
    highest_mode="LP02",
    taper_factor=10,
    taper_length=50000
)

# Save the design
lantern.write("my_first_lantern.ind")
print(f"Lantern created with {len(core_map)} cores")
```

### 2. Run a Simulation

```python
from rsoft_cad.rsoft_simulations import run_simulation

# Run BeamPROP simulation
result = run_simulation(
    design_filepath="./",
    design_filename="my_first_lantern.ind",
    sim_package="bsimw32",
    prefix_name="test_run"
)

print(f"Simulation completed with code: {result.returncode}")
```

### 3. Analyze Results

```python
from rsoft_cad.utils.rsoft_file_plot import plot_monitor_data

# Plot simulation results
fig, ax = plot_monitor_data("test_run_monitor.dat")
fig.show()
```

## Mode Selective Lantern Example

Mode selective lanterns are specialized for specific optical modes:

```python
from rsoft_cad.lantern import ModeSelectiveLantern

# Create mode selective lantern
mspl = ModeSelectiveLantern()
core_map = mspl.create_lantern(
    highest_mode="LP11",
    launch_mode="LP01",
    taper_factor=5,
    taper_length=80000
)

# Add launch field for specific mode
mspl.add_launch_field(
    launch_type="LP01",
    power=1.0,
    position=(0, 0)
)

# Save the design
mspl.write("mode_selective_lantern.ind")
```

## Parameter Sweeps

Explore design space with parameter sweeps:

```python
from rsoft_cad.beamprop import beamprop_tapered_lantern
import numpy as np

# Define parameter range
taper_lengths = np.linspace(20000, 80000, 10)

# Run parameter sweep
results = []
for i, length in enumerate(taper_lengths):
    core_map = beamprop_tapered_lantern(
        expt_dir="sweep_output",
        opt_name=f"run_{i:03d}",
        taper_factor=15,
        taper_length=length,
        highest_mode="LP02",
        launch_mode="LP01"
    )
    results.append((length, core_map))

print(f"Completed {len(results)} simulations")
```

## Configuration Management

Use JSON configuration files for reproducible designs:

```python
from rsoft_cad.utils.config.modifier import load_config, modify_parameter, save_config

# Load base configuration
config = load_config("config/complete_pl_config.json")

# Modify parameters
config = modify_parameter(config, "pl_params.Num_Cores_Ring", 6)
config = modify_parameter(config, "pl_params.Taper_Length", 60000)
config = modify_parameter(config, "pl_params.Core_Diameter", 8.5)

# Save custom configuration
save_config(config, "my_custom_config.json")

# Use in lantern creation
lantern = PhotonicLantern()
lantern.create_lantern(config=config)
```

## Visualization

Visualize your designs and results:

```python
from rsoft_cad.utils.fiber_layout import visualise_layout
from rsoft_cad.utils.rsoft_file_plot import combined_field_plots

# Visualize fiber layout
fig = visualise_layout(core_map, show_indices=True)
fig.show()

# Plot field distributions
fig, axes = combined_field_plots(
    "simulation_results/",
    field_type="intensity",
    colormap="hot"
)
fig.show()
```

## Command Line Interface

RSoft CAD also provides command-line tools:

```bash
# Run FemSIM parameter scan
python -c "from rsoft_cad.femsim import femsimulation; femsimulation()" \
    --taper-factors 18.75 \
    --taper-length 40000 \
    --num-grids 200 \
    --num-points 200

# Plot effective index results
python -c "from rsoft_cad.femsim import nef_plot; nef_plot()" \
    --folder-path femsim_run_001 \
    --plot-type real \
    --fit-data
```

## Common Patterns

### 1. Design → Simulate → Analyze Workflow

```python
# Design
lantern = PhotonicLantern()
lantern.create_lantern(highest_mode="LP02", taper_length=50000)
lantern.write("design.ind")

# Simulate
result = run_simulation("./", "design.ind", "bsimw32", "analysis")

# Analyze
if result.returncode == 0:
    fig, ax = plot_monitor_data("analysis_monitor.dat")
    fig.savefig("results.png")
```

### 2. Batch Processing

```python
# Process multiple configurations
configs = [
    {"taper_length": 30000, "taper_factor": 10},
    {"taper_length": 50000, "taper_factor": 15},
    {"taper_length": 70000, "taper_factor": 20},
]

for i, params in enumerate(configs):
    lantern = PhotonicLantern()
    lantern.create_lantern(**params)
    lantern.write(f"design_{i}.ind")
    
    result = run_simulation("./", f"design_{i}.ind", "bsimw32", f"batch_{i}")
    print(f"Config {i}: {'Success' if result.returncode == 0 else 'Failed'}")
```

## Next Steps

Now that you've mastered the basics:

- Explore [Tutorials](tutorials.html) for detailed guides
- Check out [Examples](examples.html) for real-world use cases
- Review [API Reference](api-reference.html) for complete documentation
- See advanced optimization techniques in the full documentation

## Need Help?

- Review the `examples/` directory in the repository
- Check [GitHub Issues](https://github.com/SAIL-Labs/rsoft_cad/issues)
- Contact: bongkokwei@gmail.com