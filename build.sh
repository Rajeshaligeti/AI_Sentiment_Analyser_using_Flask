#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

echo "Build completed successfully!"
