---
layout: default
title: Changelog
nav_order: 7
---

# Changelog

All notable changes to RSoft PLTools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation site with GitHub Pages
- Sphinx-based API documentation generation
- GitHub Actions workflow for automatic documentation building
- Command-line interface for FemSIM simulations
- Advanced visualization tools for effective index analysis
- Custom taper profile support
- Parameter sweep utilities for optimization

### Changed
- Improved error handling and validation
- Enhanced configuration management system
- Better integration between BeamPROP and FemSIM workflows

### Fixed
- Documentation formatting and cross-references
- Import issues with optional dependencies

## [0.1.0] - 2024-12-13

### Added
- Initial release of RSoft PLTools
- Core photonic lantern design functionality
- Mode selective lantern support
- RSoft simulation file generation
- BeamPROP and FemSIM integration
- Configuration management system
- Fiber layout visualization
- Basic plotting and analysis tools

### Features
- **Lantern Design**
  - Photonic lantern creation with customizable parameters
  - Mode selective lantern (MSL) generation
  - Hexagonal and circular fiber layouts
  - Automated geometry calculations

- **Simulation Support**
  - RSoft CAD file generation
  - BeamPROP simulation orchestration
  - FemSIM effective index analysis
  - Subprocess management for simulations

- **Analysis Tools**
  - Monitor data plotting
  - Effective index visualization
  - Parameter sweep analysis
  - Outlier detection and data cleaning

- **Configuration System**
  - JSON-based hierarchical configuration
  - Dynamic parameter expressions
  - Runtime configuration modification
  - Template-based segment definitions

### Dependencies
- Python 3.6+
- NumPy 1.2+
- Matplotlib 2.0+
- Pandas
- SciPy
- Seaborn

### Known Issues
- Some docstring formatting issues in Sphinx generation
- Missing tqdm dependency for progress bars
- Limited error messages for simulation failures

---

## Development Notes

### Version 0.1.0 Architecture

The initial release implements a layered architecture:

1. **Base Circuit Layer** (`rsoft_circuit.py`)
   - Core RSoft simulation file generation
   - Builder pattern with component factories
   - Type-safe enums for simulation parameters

2. **Simulation Layer** (`rsoft_simulations.py`)
   - Simulation orchestration with subprocess management
   - Error handling and validation
   - Support for multiple RSoft packages

3. **Domain Model Layer** (`lantern/`, `geometry/`)
   - Photonic device modeling with inheritance
   - Composition with FiberConfigurator and SegmentManager
   - Strategy pattern for different lantern types

4. **Utilities Layer** (`utils/`)
   - File I/O operations
   - Plotting and visualization
   - Configuration management

5. **Application Layer** (`simulations/`, `examples/`)
   - High-level workflows
   - Example implementations
   - Parameter scanning utilities

### Future Roadmap

#### Version 0.2.0 (Planned)
- [ ] Enhanced mode coupling analysis
- [ ] Optimization algorithms for taper design
- [ ] Web-based configuration interface
- [ ] Performance improvements for large simulations
- [ ] Additional fiber types and materials

#### Version 0.3.0 (Planned)
- [ ] Machine learning integration for design optimization
- [ ] 3D visualization capabilities
- [ ] Export to commercial simulation packages
- [ ] Advanced post-processing tools

### Contributing

When contributing to RSoft PLTools:

1. **Documentation**: Update both code docstrings and user documentation
2. **Testing**: Add tests for new functionality
3. **Changelog**: Update this changelog with your changes
4. **Version**: Follow semantic versioning principles

### Migration Guide

#### From Pre-Release to v0.1.0

If you were using development versions before the official release:

1. **Configuration Files**: Update configuration format to new JSON schema
2. **Import Statements**: Update imports to use new module structure
3. **Function Names**: Some utility functions have been renamed for consistency
4. **Dependencies**: Install new required packages (pandas, scipy, seaborn)

#### Example Migration

**Old (Pre-release):**
```python
from rsoft_tools import create_lantern
from rsoft_tools.utils import plot_results

lantern = create_lantern(cores=6, taper=50000)
plot_results(lantern.output_file)
```

**New (v0.1.0):**
```python
from rsoft_cad.lantern import PhotonicLantern
from rsoft_cad.utils.rsoft_file_plot import plot_monitor_data

lantern = PhotonicLantern()
core_map = lantern.create_lantern(highest_mode="LP02", taper_length=50000)
plot_monitor_data("simulation_results/monitor.dat")
```

---

For detailed API changes and migration assistance, please refer to the [API Reference](api-reference.html) and [GitHub Issues](https://github.com/SAIL-Labs/rsoft_cad/issues).