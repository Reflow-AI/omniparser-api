#!/bin/bash
set -e

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate omni

# Start the API server
python api.py
