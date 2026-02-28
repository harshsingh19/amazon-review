#!/bin/bash

# Install script for amazon-review project dependencies

echo "Installing amazon-review dependencies..."

# Determine which pip command to use
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "Error: pip or pip3 is not installed. Please install Python and pip first."
    exit 1
fi

echo "Using: $PIP_CMD"

# Install requirements
$PIP_CMD install -r requirements.txt
python3 -m spacy download en_core_web_sm

if [ $? -eq 0 ]; then
    echo "✓ All dependencies installed successfully!"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
