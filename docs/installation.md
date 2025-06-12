---
layout: default
title: Installation
nav_order: 2
---

# Installation Guide

## Prerequisites

Before installing RSoft CAD, ensure you have:

- **Python 3.6 or higher**
- **RSoft CAD software** (for running simulations)
- **Git** (for cloning the repository)

## Installation Methods

### Method 1: Development Installation (Recommended)

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/SAIL-Labs/rsoft_cad.git
cd rsoft_cad

# Install in development mode
pip install -e .
```

This method allows you to modify the code and see changes immediately without reinstalling.

### Method 2: Direct Installation

If you don't plan to modify the code:

```bash
pip install git+https://github.com/SAIL-Labs/rsoft_cad.git
```

## Dependencies

The package automatically installs the following Python dependencies:

- **numpy** (≥1.2) - Numerical computations
- **matplotlib** (≥2.0) - Plotting and visualization
- **pandas** - Data manipulation and analysis
- **scipy** - Scientific computing
- **seaborn** - Statistical data visualization

## Verification

To verify your installation, run:

```python
import rsoft_cad
print(rsoft_cad.__version__)
```

Or test with a simple example:

```python
from rsoft_cad.lantern import PhotonicLantern
from rsoft_cad.utils.config.modifier import load_config

# Load default configuration
config = load_config("config/default_config.json")
print("Installation successful!")
```

## RSoft CAD Configuration

For running simulations, you'll need RSoft CAD installed and properly configured:

1. **Install RSoft CAD** following the vendor's instructions
2. **Set environment variables** (if required by your RSoft installation)
3. **Verify RSoft commands** are accessible from your command line

Common RSoft simulation packages used:
- `bsimw32` - BeamPROP simulations
- `femsimw32` - FemSIM simulations

## Development Setup

For contributors or advanced users:

```bash
# Clone and enter directory
git clone https://github.com/SAIL-Labs/rsoft_cad.git
cd rsoft_cad

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .

# Install development tools (optional)
pip install pytest black flake8
```

## Troubleshooting

### Common Issues

**Import Error**: If you get import errors, ensure:
- Python version is 3.6+
- All dependencies are installed
- Virtual environment is activated (if using one)

**RSoft Simulation Errors**: If simulations fail:
- Verify RSoft CAD is properly installed
- Check RSoft license is valid
- Ensure simulation executables are in PATH

**Path Issues**: If config files aren't found:
- Run Python from the project root directory
- Use absolute paths for configuration files
- Check file permissions

### Getting Help

If you encounter issues:

1. Check the [GitHub issues](https://github.com/SAIL-Labs/rsoft_cad/issues)
2. Review the examples in the `examples/` directory
3. Contact: bongkokwei@gmail.com

## Next Steps

Once installed, proceed to:
- [Quick Start Guide](quick-start.html) - Basic usage
- [Tutorials](tutorials.html) - Step-by-step examples
- [Examples](examples.html) - Code samples