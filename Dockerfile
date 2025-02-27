FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN mkdir -p /app /workspace
WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    git-lfs \
    wget \
    libgl1 \
    libglib2.0-0 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

SHELL ["/bin/bash", "-c"]

RUN conda create -n omni python=3.12 -y && \
    eval "$(conda shell.bash hook)" && \
    conda activate omni && \
    pip uninstall -y opencv-python opencv-python-headless && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install -r requirements.txt && \
    pip install huggingface_hub && \
    pip install ultralytics

RUN eval "$(conda shell.bash hook)" && \
    conda activate omni && \
    python download.py

RUN echo 'eval "$(conda shell.bash hook)"' >> /root/.bashrc && \
    echo "conda activate omni" >> /root/.bashrc

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

VOLUME /workspace

EXPOSE 1337
EXPOSE 22

CMD ["/app/entrypoint.sh"] 