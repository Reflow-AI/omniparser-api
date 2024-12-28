import os
from huggingface_hub import snapshot_download

repo_id = "microsoft/OmniParser"

local_dir = "weights"

os.makedirs(local_dir, exist_ok=True)

snapshot_download(repo_id, local_dir=local_dir, ignore_patterns=["*.md"])

print(f"Weights downloaded to {local_dir}")