#!/bin/bash

# Check if Python 3.11 is installed
if command -v python3.11 &>/dev/null; then
    echo "Python 3.11 is installed."

    # Create virtual environment
    python3.11 -m venv .venv
    
    # Activate virtual environment
    . .venv/bin/activate
    
    # Install requirements
    pip install -r requirements.txt
else
    echo "Python 3.11 is not installed."
fi
