---
layout: default
title: Home
nav_order: 1
description: "RSoft CAD - Photonic Lantern Simulation Toolkit"
permalink: /
---

# RSoft CAD - Photonic Lantern Simulation Toolkit

A comprehensive Python package for designing, simulating, and analysing photonic lanterns - specialised optical components that enable efficient coupling between multimode and single-mode optical systems.

## Overview

The Photonic Lantern Simulation Toolkit provides tools for designing various lantern configurations, running optical simulations, and analysing results. It features a layered architecture with clear separation between circuit generation, simulation orchestration, and domain modeling.

## Key Features

- **Multi-core fibre and photonic lantern design**
- **Mode selective lantern (MSL) generation**
- **Flexible configuration management**
- **Simulation file generation for RSoft CAD**
- **Geometric layout visualisation**
- **Parametric design exploration**
- **Advanced mode analysis**

## Core Capabilities

### Design & Layout
- Hexagonal and circular fibre layouts
- Customisable fibre parameters
- Automated lantern geometry calculations
- Multiple LP mode support (LP01, LP11, LP21, LP02, etc.)

### Simulation Support
- BeamPROP and FemSIM simulation file generation
- Effective refractive index calculation and analysis
- Mode coupling analysis
- Field propagation modelling

### Analysis & Optimisation
- Taper length optimisation algorithms
- Parameter sweep functionality
- Outlier detection and data processing
- Enhanced visualisation for field distributions

## Quick Start

```python
from rsoft_cad.lantern import PhotonicLantern
from rsoft_cad.rsoft_simulations import run_simulation

# Create a photonic lantern
lantern = PhotonicLantern(**params)
lantern.create_lantern(layer_config)
lantern.add_launch_field(...)
lantern.write(filepath)

# Run simulation
result = run_simulation(design_filepath, design_filename, sim_package, prefix_name)
```

## Navigation

- [Installation Guide](installation.html) - Get started with RSoft CAD
- [Quick Start](quick-start.html) - Basic usage examples
- [Tutorials](tutorials.html) - Step-by-step guides
- [API Reference](api-reference.html) - Complete API documentation
- [Examples](examples.html) - Code examples and use cases

## Architecture

The toolkit follows a layered design:

- **Base Circuit Layer**: Core RSoft simulation file generation
- **Simulation Layer**: Simulation orchestration with subprocess management
- **Domain Model Layer**: Photonic device modeling with inheritance-based design
- **Utilities Layer**: File I/O, plotting, configuration management
- **Application Layer**: High-level workflows

## Support

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/SAIL-Labs/rsoft_cad).

**Author**: Kok-Wei Bong - bongkokwei@gmail.com