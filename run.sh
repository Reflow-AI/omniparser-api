#!/bin/bash
set -e  # Exit on error

# Print commands being executed (for debugging)
set -x

# Update and install system dependencies
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git-lfs \
    wget \
    libgl1 \
    libglib2.0-0 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Add conda to path and initialize
export PATH="/opt/conda/bin:$PATH"
conda init bash
source ~/.bashrc

# Create and activate conda environment
conda create -n omni python=3.12 -y
eval "$(conda shell.bash hook)"
conda activate omni

git lfs install
git lfs pull

pip uninstall -y opencv-python opencv-python-headless
pip install --no-cache-dir opencv-python-headless==4.8.1.78
pip install -r requirements.txt
pip install huggingface_hub
pip install ultralytics

# Download model weights
python download.py
echo "Contents of weights directory:"
ls -lR weights

# Make entrypoint executable and run it
chmod +x entrypoint.sh
./entrypoint.sh