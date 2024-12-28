# OmniParser: Screen Parsing tool for Pure Vision Based GUI Agent

<p align="center">
  <img src="imgs/logo.png" alt="Logo">
</p>

[![arXiv](https://img.shields.io/badge/Paper-green)](https://arxiv.org/abs/2408.00203)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📢 [[Project Page](https://microsoft.github.io/OmniParser/)] [[Blog Post](https://www.microsoft.com/en-us/research/articles/omniparser-for-pure-vision-based-gui-agent/)] [[Models](https://huggingface.co/microsoft/OmniParser)] [huggingface space](https://huggingface.co/spaces/microsoft/OmniParser)

**OmniParser** is a comprehensive method for parsing user interface screenshots into structured and easy-to-understand elements, which significantly enhances the ability of GPT-4V to generate actions that can be accurately grounded in the corresponding regions of the interface. 

## News
- [2024/11/26] We release an updated version, OmniParser V1.5 which features 1) more fine grained/small icon detection, 2) prediction of whether each screen element is interactable or not. Examples in the demo.ipynb. 
- [2024/10] OmniParser was the #1 trending model on huggingface model hub (starting 10/29/2024). 
- [2024/10] Feel free to checkout our demo on [huggingface space](https://huggingface.co/spaces/microsoft/OmniParser)! (stay tuned for OmniParser + Claude Computer Use)
- [2024/10] Both Interactive Region Detection Model and Icon functional description model are released! [Hugginface models](https://huggingface.co/microsoft/OmniParser)
- [2024/09] OmniParser achieves the best performance on [Windows Agent Arena](https://microsoft.github.io/WindowsAgentArena/)! 

## Install 
Install environment:
```python
conda create -n "omni" python==3.12
conda activate omni
pip install -r requirements.txt
```

Then download the model ckpts files in: https://huggingface.co/microsoft/OmniParser, and put them under weights/, default folder structure is: weights/icon_detect, weights/icon_caption_florence, weights/icon_caption_blip2. 

For v1: 
convert the safetensor to .pt file. 
```python
python weights/convert_safetensor_to_pt.py

For v1.5: 
download 'model_v1_5.pt' from https://huggingface.co/microsoft/OmniParser/tree/main/icon_detect_v1_5, make a new dir: weights/icon_detect_v1_5, and put it inside the folder. No weight conversion is needed. 
```

## Examples:
We put together a few simple examples in the demo.ipynb. 

## Gradio Demo
To run gradio demo, simply run:
```python
# For v1
python gradio_demo.py --icon_detect_model weights/icon_detect/best.pt --icon_caption_model florence2
# For v1.5
python gradio_demo.py --icon_detect_model weights/icon_detect_v1_5/model_v1_5.pt --icon_caption_model florence2
```


## RunPod Deployment Guide

### Option 1: Using Docker

1. Build and push the Docker image:
```bash
docker build -t your-dockerhub-username/omniparser:latest .
docker push your-dockerhub-username/omniparser:latest
```

2. On RunPod:
   - Create a new template or use an existing one
   - Set the Docker image URL
   - Add environment variables in the RunPod UI:
     - `API_KEY`: Your API key for authentication
     - `PORT`: Port for the API server (default: 1337)
     - `ICON_DETECT_MODEL`: Path to detection model
     - `ICON_CAPTION_MODEL`: Caption model type (florence2 or blip2)

### Option 2: Direct Deployment

1. Clone the repository on RunPod:
```bash
git clone https://github.com/your-username/omniparser.git
cd omniparser
```

2. Create a `.env` file:
```bash
cat << EOF > .env
API_KEY=your_api_key_here
PORT=1337
ICON_DETECT_MODEL=weights/icon_detect_v1_5/model_v1_5.pt
ICON_CAPTION_MODEL=florence2
EOF
```

3. Run the installation script:
```bash
chmod +x run.sh
./run.sh
```

### Accessing the API

- The API will be available at: `https://[pod-id]-[port].proxy.runpod.net`
- API documentation: `https://[pod-id]-[port].proxy.runpod.net/docs`
- Include your API key in requests using the `X-API-Key` header

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Authentication key for API access | None |
| `PORT` | Port for the API server | 1337 |
| `ICON_DETECT_MODEL` | Path to detection model | weights/icon_detect_v1_5/model_v1_5.pt |
| `ICON_CAPTION_MODEL` | Caption model type (florence2 or blip2) | florence2 |

### Using RunPod CLI

To deploy using RunPod CLI:
```bash
runpodctl create pod \
  --env API_KEY=your_key \
  --env PORT=1337 \
  --env ICON_DETECT_MODEL=weights/icon_detect_v1_5/model_v1_5.pt \
  --env ICON_CAPTION_MODEL=florence2 \
  --gpu "NVIDIA RTX 4000" \
  --container your-dockerhub-username/omniparser:latest \
  --name omniparser
```

### Example API Usage

Using curl:
```bash
curl -X POST \
  https://[pod-id]-[port].proxy.runpod.net/process \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

Using Python:
```python
import requests
import base64

# Encode image
with open("screenshot.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Make request
response = requests.post(
    "https://[pod-id]-[port].proxy.runpod.net/process",
    headers={"X-API-Key": "your_api_key"},
    json={"image": encoded_string}
)

print(response.json())
```


## Model Weights License
For the model checkpoints on huggingface model hub, please note that icon_detect model is under AGPL license since it is a license inherited from the original yolo model. And icon_caption_blip2 & icon_caption_florence is under MIT license. Please refer to the LICENSE file in the folder of each model: https://huggingface.co/microsoft/OmniParser.

## 📚 Citation
Our technical report can be found [here](https://arxiv.org/abs/2408.00203).
If you find our work useful, please consider citing our work:
```
@misc{lu2024omniparserpurevisionbased,
      title={OmniParser for Pure Vision Based GUI Agent}, 
      author={Yadong Lu and Jianwei Yang and Yelong Shen and Ahmed Awadallah},
      year={2024},
      eprint={2408.00203},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2408.00203}, 
}
```