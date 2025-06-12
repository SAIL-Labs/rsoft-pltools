---
layout: default
title: Tutorials
nav_order: 4
---

# Tutorials

Comprehensive guides for common RSoft CAD workflows and advanced techniques.

## Tutorial 1: Designing Your First Photonic Lantern

### Overview
Learn to create a basic photonic lantern from scratch, including configuration, simulation, and analysis.

### Step 1: Understanding the Configuration
```python
from rsoft_cad.utils.config.modifier import load_config, modify_parameter

# Load and examine the default configuration
config = load_config("config/default_config.json")

# Key parameters to understand:
# - Num_Cores_Ring: Number of cores in the ring
# - Core_Diameter: Diameter of individual cores
# - Taper_Length: Length of the taper section
# - Taper_Factor: How much the structure tapers
```

### Step 2: Create the Lantern
```python
from rsoft_cad.lantern import PhotonicLantern

# Initialize the lantern
lantern = PhotonicLantern()

# Create with specific parameters
core_map = lantern.create_lantern(
    config=config,
    highest_mode="LP02",    # Maximum mode to support
    taper_factor=12,        # Taper ratio
    taper_length=45000,     # Taper length in microns
    savefile=True           # Save intermediate files
)

print(f"Created lantern with {len(core_map)} cores")
```

### Step 3: Add Launch Conditions
```python
# Add launch field at the input
lantern.add_launch_field(
    launch_type="LP01",     # Launch LP01 mode
    power=1.0,              # Normalized power
    position=(0, 0),        # Center position
    width=8.0               # Beam width
)

# Save the complete design
lantern.write("tutorial_lantern.ind")
```

### Step 4: Run Simulation
```python
from rsoft_cad.rsoft_simulations import run_simulation

# Execute BeamPROP simulation
result = run_simulation(
    design_filepath=lantern.design_filepath,
    design_filename=lantern.design_filename,
    sim_package="bsimw32",
    prefix_name="tutorial_sim",
    save_folder="tutorial_results"
)

if result.returncode == 0:
    print("Simulation completed successfully!")
else:
    print(f"Simulation failed: {result.stderr}")
```

## Tutorial 2: Mode Selective Lantern Design

### Overview
Design a mode selective lantern that efficiently couples specific LP modes.

### Step 1: Mode Analysis
```python
from rsoft_cad.utils.lp_modes import calculate_mode_cutoff
from rsoft_cad.constants import SINGLE_MODE_FIBERS

# Analyze mode properties for SMF-28 fiber
fiber_params = SINGLE_MODE_FIBERS["SMF-28"]
cutoff_freq = calculate_mode_cutoff(
    core_diameter=fiber_params["core_diameter"],
    numerical_aperture=fiber_params["numerical_aperture"],
    wavelength=1550  # nm
)

print(f"LP11 cutoff frequency: {cutoff_freq} THz")
```

### Step 2: Create Mode Selective Lantern
```python
from rsoft_cad.lantern import ModeSelectiveLantern

# Initialize mode selective lantern
mspl = ModeSelectiveLantern()

# Create with mode-specific parameters
core_map = mspl.create_lantern(
    highest_mode="LP11",        # Target mode
    launch_mode="LP01",         # Input mode
    taper_factor=8,             # Conservative taper
    taper_length=60000,         # Longer taper for mode selectivity
    mode_coupling_strength=0.1  # Weak coupling
)

# Add specific launch conditions for mode conversion
mspl.add_launch_field(
    launch_type="LP01",
    power=1.0,
    position=(0, 0)
)

mspl.write("mode_selective_lantern.ind")
```

### Step 3: Optimization Loop
```python
import numpy as np

# Optimize taper parameters
taper_factors = np.linspace(5, 15, 6)
coupling_efficiencies = []

for factor in taper_factors:
    # Create lantern with current parameters
    mspl = ModeSelectiveLantern()
    core_map = mspl.create_lantern(
        highest_mode="LP11",
        launch_mode="LP01",
        taper_factor=factor,
        taper_length=60000
    )
    
    # Run simulation
    result = run_simulation(
        mspl.design_filepath,
        mspl.design_filename,
        "bsimw32",
        f"opt_factor_{factor}"
    )
    
    # Extract coupling efficiency (simplified)
    if result.returncode == 0:
        efficiency = extract_coupling_efficiency(f"opt_factor_{factor}_monitor.dat")
        coupling_efficiencies.append(efficiency)
    else:
        coupling_efficiencies.append(0)

# Find optimal taper factor
optimal_factor = taper_factors[np.argmax(coupling_efficiencies)]
print(f"Optimal taper factor: {optimal_factor}")
```

## Tutorial 3: Parameter Sweep Analysis

### Overview
Systematically explore design parameters to find optimal configurations.

### Step 1: Define Parameter Space
```python
from rsoft_cad.beamprop import beamprop_tapered_lantern
import numpy as np
import pandas as pd

# Define parameter ranges
taper_lengths = np.linspace(20000, 80000, 13)
taper_factors = np.linspace(10, 20, 6)

# Create parameter grid
param_grid = [(tl, tf) for tl in taper_lengths for tf in taper_factors]
print(f"Total simulations: {len(param_grid)}")
```

### Step 2: Execute Parameter Sweep
```python
results = []

for i, (taper_length, taper_factor) in enumerate(param_grid):
    print(f"Running simulation {i+1}/{len(param_grid)}")
    
    # Run simulation with current parameters
    core_map = beamprop_tapered_lantern(
        expt_dir="param_sweep",
        opt_name=f"run_{i:03d}",
        taper_factor=taper_factor,
        taper_length=taper_length,
        highest_mode="LP02",
        launch_mode="LP01",
        result_files_prefix=f"sweep_{i:03d}"
    )
    
    # Store parameters and results
    results.append({
        'run_id': i,
        'taper_length': taper_length,
        'taper_factor': taper_factor,
        'num_cores': len(core_map)
    })

# Convert to DataFrame for analysis
df_results = pd.DataFrame(results)
df_results.to_csv("parameter_sweep_results.csv", index=False)
```

### Step 3: Analyze and Visualize Results
```python
from rsoft_cad.beamprop.beamprop_plot_util import plot_combined_monitor_files
import matplotlib.pyplot as plt

# Load and analyze monitor data
fig, ax, combined_df, final_values, summary, optimal_taper, optimal_value = plot_combined_monitor_files(
    "param_sweep/rsoft_data_files",
    save_plot=True,
    plot_filename="parameter_sweep_analysis"
)

# Create parameter sensitivity plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Coupling efficiency vs taper length
for tf in taper_factors:
    mask = df_results['taper_factor'] == tf
    subset = df_results[mask]
    axes[0].plot(subset['taper_length'], subset['coupling_efficiency'], 
                label=f'TF={tf}', marker='o')

axes[0].set_xlabel('Taper Length (μm)')
axes[0].set_ylabel('Coupling Efficiency')
axes[0].legend()
axes[0].grid(True)

# Plot 2: Heatmap of parameter space
pivot_data = df_results.pivot('taper_factor', 'taper_length', 'coupling_efficiency')
im = axes[1].imshow(pivot_data, aspect='auto', cmap='viridis')
axes[1].set_xlabel('Taper Length')
axes[1].set_ylabel('Taper Factor')
plt.colorbar(im, ax=axes[1], label='Coupling Efficiency')

plt.tight_layout()
plt.savefig("parameter_sensitivity.png", dpi=300)
plt.show()

print(f"Optimal configuration: TL={optimal_taper}, Efficiency={optimal_value:.3f}")
```

## Tutorial 4: Effective Index Analysis

### Overview
Use FemSIM to analyze effective refractive indices and mode properties.

### Step 1: Set Up FemSIM Simulation
```python
from rsoft_cad.femsim import femsim_tapered_lantern

# Run FemSIM for effective index calculation
femsim_tapered_lantern(
    expt_dir="neff_analysis",
    taper_factor=15,
    taper_length=50000,
    num_points=150,          # Number of z-points
    num_grids=250,           # Grid resolution
    highest_mode="LP02",
    launch_mode="LP01"
)
```

### Step 2: Process and Visualize Results
```python
from rsoft_cad.femsim.visualisation import plot_combined_nef_files
from rsoft_cad.femsim.curve_fitting import fit_polynomial_to_data

# Load and plot effective index data
fig = plot_combined_nef_files(
    folder_path="neff_analysis/rsoft_data_files",
    plot_type="real",           # Plot real part of n_eff
    save_plot=True,
    max_indices=15,             # Plot first 15 modes
    remove_outliers=True,       # Clean data
    fit_data=True,              # Add polynomial fits
    colormap="plasma"
)

plt.title("Effective Index Evolution Along Taper")
plt.show()
```

### Step 3: Mode Coupling Analysis
```python
from rsoft_cad.femsim.data_processing import analyze_mode_coupling

# Analyze mode coupling from effective index data
coupling_data = analyze_mode_coupling(
    "neff_analysis/rsoft_data_files",
    mode_pairs=[("LP01", "LP11"), ("LP01", "LP21")],
    coupling_threshold=0.001
)

# Plot coupling evolution
fig, ax = plt.subplots(figsize=(10, 6))
for pair, data in coupling_data.items():
    ax.plot(data['z_position'], data['coupling_strength'], 
           label=f"{pair[0]} ↔ {pair[1]}", linewidth=2)

ax.set_xlabel('Z Position (μm)')
ax.set_ylabel('Coupling Strength')
ax.legend()
ax.grid(True, alpha=0.3)
plt.title("Mode Coupling Evolution")
plt.show()
```

## Tutorial 5: Custom Taper Design

### Overview
Create custom taper profiles for specialized applications.

### Step 1: Define Custom Taper Function
```python
from rsoft_cad.geometry.custom_taper import CustomTaper
import numpy as np

def exponential_taper(z, z_start, z_end, r_start, r_end, alpha=1.5):
    """Custom exponential taper profile"""
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
```

### Step 2: Apply to Lantern Design
```python
from rsoft_cad.lantern import PhotonicLantern

# Create lantern with custom taper
lantern = PhotonicLantern()
core_map = lantern.create_lantern(
    highest_mode="LP02",
    custom_taper=taper,        # Use custom taper
    taper_length=50000
)

# Visualize taper profile
z_positions = np.linspace(0, 70000, 1000)
radii = [taper.radius_at_position(z) for z in z_positions]

plt.figure(figsize=(10, 6))
plt.plot(z_positions, radii, linewidth=2)
plt.xlabel('Z Position (μm)')
plt.ylabel('Radius (μm)')
plt.title('Custom Exponential Taper Profile')
plt.grid(True, alpha=0.3)
plt.show()

lantern.write("custom_taper_lantern.ind")
```

## Tutorial 6: Advanced Visualization

### Overview
Create publication-quality plots and animations of your results.

### Step 1: Field Distribution Plots
```python
from rsoft_cad.utils.rsoft_file_plot import combined_field_plots

# Create comprehensive field plots
fig, axes = combined_field_plots(
    data_folder="simulation_results/",
    field_type="intensity",
    z_positions=[0, 25000, 50000],    # Specific z-positions
    colormap="hot",
    normalize=True,
    save_plots=True,
    plot_format="png",
    dpi=300
)

# Add custom annotations
for i, ax in enumerate(axes.flat):
    ax.set_title(f"Z = {[0, 25000, 50000][i]} μm")
    ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("field_evolution.png", dpi=300, bbox_inches='tight')
plt.show()
```

### Step 2: Animation of Field Propagation
```python
import matplotlib.animation as animation

def create_propagation_animation(data_folder, output_filename="propagation.mp4"):
    # Load field data at multiple z-positions
    field_data = load_field_evolution(data_folder)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def animate(frame):
        ax.clear()
        z_pos = field_data['z_positions'][frame]
        field = field_data['fields'][frame]
        
        im = ax.imshow(field, cmap='hot', extent=[-50, 50, -50, 50])
        ax.set_title(f'Field Intensity at Z = {z_pos:.0f} μm')
        ax.set_xlabel('X (μm)')
        ax.set_ylabel('Y (μm)')
        
        return [im]
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, animate, frames=len(field_data['z_positions']),
        interval=100, blit=False, repeat=True
    )
    
    # Save as video
    anim.save(output_filename, writer='ffmpeg', fps=10, dpi=150)
    plt.show()

# Create animation
create_propagation_animation("simulation_results/")
```

## Next Steps

These tutorials cover the core workflows in RSoft CAD. For more advanced topics:

- Explore the [Examples](examples.html) section for real-world applications
- Check the [API Reference](api-reference.html) for detailed function documentation
- Review the source code in the `examples/` directory for additional patterns

## Common Troubleshooting

### Simulation Failures
- Check RSoft installation and licensing
- Verify input file format
- Ensure sufficient computational resources

### Memory Issues
- Reduce grid resolution for large simulations
- Use parameter chunking for large sweeps
- Monitor system resources during execution

### Convergence Problems
- Adjust simulation parameters (step size, iterations)
- Check boundary conditions
- Verify mode definitions and launch conditions