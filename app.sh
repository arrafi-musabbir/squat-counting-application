#!/bin/bash

# Default Python script name (change this if needed)
default_python_script="app.py"
Terminal=true
# Use the provided Python script or the default if not provided
python_script="${1:-$default_python_script}"

# Check if the Python script file exists
if [ ! -f "$python_script" ]; then
    echo "Error: Python script '$python_script' not found."
    exit 1
fi

# Execute the Python script
exec python3 "$python_script"

