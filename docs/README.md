# RSoft PLTools Documentation

This directory contains the documentation for RSoft PLTools, built using Jekyll for GitHub Pages and Sphinx for API documentation.

## Structure

```
docs/
├── _config.yml              # Jekyll configuration for GitHub Pages
├── index.md                 # Main documentation homepage
├── installation.md          # Installation guide
├── quick-start.md           # Quick start guide  
├── tutorials.md             # Detailed tutorials
├── api-reference.md         # API overview
├── examples.md              # Code examples
├── changelog.md             # Version history
├── build_docs.sh            # Local documentation build script
├── sphinx/                  # Sphinx documentation source
│   ├── conf.py             # Sphinx configuration
│   ├── index.rst           # Sphinx homepage
│   ├── requirements.txt    # Sphinx dependencies
│   ├── Makefile            # Sphinx build commands
│   └── *.rst               # Auto-generated API docs
└── _build/                  # Generated documentation output
    └── html/               # HTML documentation files
```

## Viewing Documentation

### Online
The documentation is automatically published to GitHub Pages at:
**https://sail-labs.github.io/rsoft_cad/**

### Local Development

1. **Install dependencies:**
   ```bash
   conda activate rsoft-tools
   conda install sphinx sphinx_rtd_theme myst-parser tqdm -c conda-forge
   ```

2. **Build documentation:**
   ```bash
   cd docs
   ./build_docs.sh
   ```

3. **View locally:**
   Open `docs/_build/html/index.html` in your browser

## Documentation Types

### GitHub Pages (Jekyll)
- **Purpose**: User-friendly documentation website
- **Technology**: Jekyll with Minima theme
- **Files**: `*.md` files in docs root
- **Features**:
  - Installation guides
  - Tutorials and examples  
  - Getting started guides
  - API overview

### Sphinx Documentation
- **Purpose**: Detailed API documentation from docstrings
- **Technology**: Sphinx with Read the Docs theme
- **Files**: `sphinx/` directory
- **Features**:
  - Auto-generated API docs
  - Cross-references
  - Search functionality
  - Code highlighting

## Building Process

### Automatic (GitHub Actions)
Documentation is automatically built and deployed when changes are pushed to the main branch using the workflow in `.github/workflows/docs.yml`.

### Manual
Use the provided build script:
```bash
./build_docs.sh
```

This script:
1. Activates the conda environment
2. Generates API documentation from source code
3. Builds HTML documentation with Sphinx
4. Optionally opens the documentation in your browser

## Contributing to Documentation

### Adding New Pages
1. Create new `.md` files in the docs root
2. Add front matter with Jekyll configuration
3. Update `_config.yml` navigation if needed

### Updating API Documentation
API documentation is automatically generated from docstrings. To improve it:
1. Update docstrings in the source code
2. Follow Google/NumPy docstring conventions
3. Rebuild documentation to see changes

### Fixing Documentation Issues
1. **Sphinx warnings**: Check docstring formatting
2. **Missing modules**: Ensure all dependencies are installed
3. **Build failures**: Check the GitHub Actions logs

## Configuration

### Jekyll (_config.yml)
- Site metadata and navigation
- Theme configuration
- Plugin settings

### Sphinx (sphinx/conf.py)
- Extensions and plugins
- API documentation settings
- Theme customization
- Cross-reference mappings

## Dependencies

### Runtime
- sphinx >= 4.0.0
- sphinx-rtd-theme >= 1.0.0  
- myst-parser >= 0.18.0
- sphinx-autodoc-typehints >= 1.12.0

### Development
All dependencies are managed through conda and specified in:
- `sphinx/requirements.txt` - Sphinx dependencies
- Main project dependencies for code import

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure the project is installed in development mode
pip install -e .
```

**Sphinx build warnings:**
- Check docstring formatting in source code
- Ensure all imports work correctly

**GitHub Pages not updating:**
- Check GitHub Actions workflow status
- Verify Pages is enabled in repository settings

**Local build failures:**
```bash
# Clean and rebuild
cd docs/sphinx
make clean
./build_docs.sh
```

### Getting Help
1. Check GitHub Actions logs for build errors
2. Review Sphinx documentation for advanced configuration
3. Open an issue for documentation-specific problems

## Maintenance

### Regular Tasks
- Update dependencies in requirements.txt
- Review and fix Sphinx warnings
- Update examples as API changes
- Keep installation instructions current

### Version Updates
- Update version numbers in conf.py
- Add changelog entries
- Update API reference for new features