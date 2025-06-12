#!/bin/bash

# Build documentation script for RSoft PLTools
# This script activates the conda environment and builds the Sphinx documentation

set -e  # Exit on any error

echo "Building RSoft PLTools Documentation..."

# Activate conda environment
source /Users/chrisbetters/miniforge3/etc/profile.d/conda.sh
conda activate rsoft-tools

# Navigate to sphinx directory
cd "$(dirname "$0")/sphinx"

echo "Cleaning previous builds..."
rm -rf ../_build

echo "Generating API documentation..."
sphinx-apidoc -o . ../../src/rsoft_cad --force --module-first

echo "Building HTML documentation..."
sphinx-build -b html . ../_build/html

echo "Documentation built successfully!"
echo "Open docs/_build/html/index.html in your browser to view the documentation."

# Optional: Open in browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Opening documentation in browser..."
    open ../_build/html/index.html
fi