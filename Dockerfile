FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH

# Copy your project files
COPY . /workspace
WORKDIR /workspace

# Install basic dependencies and clean up
RUN apt-get update && apt-get install -y \
    git-lfs \
    wget \
    libgl1 \
    libglib2.0-0 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Initialize conda
RUN conda init bash && \
    echo "conda activate omni" >> ~/.bashrc

# Create conda environment and install dependencies
RUN conda create -n omni python=3.12 -y && \
    conda activate omni && \
    pip uninstall -y opencv-python opencv-python-headless && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install -r requirements.txt && \
    pip install huggingface_hub && \
    pip install ultralytics

# Download model weights
RUN conda activate omni && \
    python download.py

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"] 