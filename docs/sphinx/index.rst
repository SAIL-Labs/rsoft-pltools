RSoft PLTools Documentation
===========================

Welcome to RSoft PLTools documentation! This package provides comprehensive tools for designing, simulating, and analyzing photonic lanterns.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quick-start
   tutorials
   examples
   api-reference
   changelog
   modules

RSoft PLTools - Photonic Lantern Simulation Toolkit
===================================================

A comprehensive Python package for designing, simulating, and analysing photonic lanterns - specialised optical components that enable efficient coupling between multimode and single-mode optical systems.

Key Features
------------

* Multi-core fibre and photonic lantern design
* Mode selective lantern (MSL) generation
* Flexible configuration management
* Simulation file generation for RSoft CAD
* Geometric layout visualisation
* Parametric design exploration
* Advanced mode analysis

Core Capabilities
-----------------

Design & Layout
~~~~~~~~~~~~~~~
* Hexagonal and circular fibre layouts
* Customisable fibre parameters
* Automated lantern geometry calculations
* Multiple LP mode support (LP01, LP11, LP21, LP02, etc.)

Simulation Support
~~~~~~~~~~~~~~~~~~
* BeamPROP and FemSIM simulation file generation
* Effective refractive index calculation and analysis
* Mode coupling analysis
* Field propagation modelling

Analysis & Optimisation
~~~~~~~~~~~~~~~~~~~~~~~
* Taper length optimisation algorithms
* Parameter sweep functionality
* Outlier detection and data processing
* Enhanced visualisation for field distributions

Quick Start
-----------

.. code-block:: python

   from rsoft_cad.lantern import PhotonicLantern
   from rsoft_cad.rsoft_simulations import run_simulation

   # Create a photonic lantern
   lantern = PhotonicLantern(**params)
   lantern.create_lantern(layer_config)
   lantern.add_launch_field(...)
   lantern.write(filepath)

   # Run simulation
   result = run_simulation(design_filepath, design_filename, sim_package, prefix_name)

Installation
------------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/SAIL-Labs/rsoft_cad.git
   cd rsoft_cad
   
   # Install in development mode
   pip install -e .

Architecture
------------

The toolkit follows a layered design:

* **Base Circuit Layer**: Core RSoft simulation file generation
* **Simulation Layer**: Simulation orchestration with subprocess management  
* **Domain Model Layer**: Photonic device modeling with inheritance-based design
* **Utilities Layer**: File I/O, plotting, configuration management
* **Application Layer**: High-level workflows

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`