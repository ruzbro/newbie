#!/bin/bash

# This script installs Jupyter and IPython using pip.
# These packages are essential for interactive data analysis and running notebooks.

echo "Starting the installation of Jupyter and IPython..."

# Install packages using pip
pip install jupyter ipython notebook jupyterlab pandas numpy matplotlib plotly

# Install and register the IPython kernel
python -m ipykernel install --user --name=python3

# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Jupyter and IPython have been successfully installed."
    echo "The IPython kernel has been registered."
    echo "Please restart your IDE to ensure all changes take effect."
else
    echo "An error occurred during the installation. Please check the output above."
fi 