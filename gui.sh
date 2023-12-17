#!/bin/bash

# Check if the Python script file exists
if [ -f "gui.py" ]; then
    # Execute the Python script
    python gui.py
else
    echo "Python script not found."
fi
