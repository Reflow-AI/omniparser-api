# OmniParser API

FastAPI server wrapper for the [OmniParser](https://github.com/microsoft/OmniParser) Image-to-text model.

## How it works
OmniParser is a screen parsing tool that converts GUI screens into structured elements. It uses computer vision models to:
- Detect UI elements and icons
- Extract text using OCR
- Generate descriptions for visual elements

## Getting Started

### Local
1. Clone the repository
2. Build the Docker image:
```
docker build -t omni-parser .
```
3. Run the Docker container:
```
docker run -p 1337:1337 -e API_KEY=your_secret_key omni-parser
```
4. Access the API at `http://localhost:1337`

### API Usage

#### Process an Image
```
curl -X POST "http://localhost:1337/process_image" \
  -H "X-API-Key: your_api_key" \
  -F "image=@screenshot.png" \
  -F "box_threshold=0.05" \
  -F "iou_threshold=0.1"
```

#### Parameters
- `box_threshold` (float, default: 0.05): Detection confidence threshold
- `iou_threshold` (float, default: 0.1): Intersection over Union threshold
- `use_paddleocr` (bool, default: false): Use PaddleOCR instead of EasyOCR
- `imgsz` (int, default: 1920): Input image size
- `icon_process_batch_size` (int, default: 64): Batch size for icon processing

#### Response Format
```
{
  "image": "base64_encoded_processed_image",
  "parsed_content_list": [
    {
      "type": "text/icon",
      "content": "description",
      "coordinates": [x1, y1, x2, y2]
    }
  ],
  "label_coordinates": {
    "element_id": {
      "bbox": [x1, y1, x2, y2],
      "label": "description"
    }
  }
}
```


# Deploy on RunPod

##  Using Pre-built Template

1. Visit: https://runpod.io/console/deploy?template=fcslnl2rq4&ref=ccxrf2yd
2. Select Configuration:
   - GPU: RTX 3090 or better
   - Disk: 80GB
   - Environment Variables: API_KEY=your_secret_key
3. Click Deploy and wait for the pod to be ready (3-5 minutes)
4. Access API: https://<pod-id>-1337.proxy.runpod.net/docs

## Method 2: Custom Deployment

1. Build & Push Docker Image:
```bash
docker login
docker build -t yourusername/omni-parser:latest .
docker push yourusername/omni-parser:latest
```

2. Create Template:
   - RunPod Console → Templates → New Template
   - Settings:
     - Image: yourusername/omni-parser:latest
     - Disk: 20GB
     - Ports: 1337
     - Env: API_KEY=your_secret_key

3. Deploy:
   - Select GPU (RTX 3090+)
   - Deploy container
   - Wait for initialization

## Test API
```bash
curl -X POST "https://<pod-id>-1337.proxy.runpod.net/process_image" \
  -H "X-API-Key: your_api_key" \
  -F "image=@screenshot.png"
```

## Requirements
- GPU: 12GB+ VRAM
- Storage: 20GB minimum
- Network: Open port 1337

## RunPod Serverless Deployment

1. Build the serverless image:
```bash
docker build -t yourusername/omni-parser-runpod:latest -f Dockerfile.runpod .
```

2. Push to Docker Hub:
```bash
docker push yourusername/omni-parser-runpod:latest
```

3. Create RunPod endpoint:
```bash
runpod endpoint create \
    --name omniparser \
    --image yourusername/omni-parser-runpod:latest \
    --gpu-type NVIDIA_RTX_3090 \
    --min-workers 1
```

4. Test the endpoint:
```python
import runpod
import base64

# Load and encode image
with open("screenshot.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Call endpoint
runpod.api_key = "your_runpod_api_key"
response = runpod.run(
    endpoint_id="your_endpoint_id",
    input={
        "image": encoded_string,
        "box_threshold": 0.05,
        "iou_threshold": 0.1
    }
)

print(response)
```

## License & Attribution
This project is a wrapper around [Microsoft's OmniParser](https://github.com/microsoft/OmniParser). Please note the following licenses:
- Original OmniParser is under CC-BY-4.0 license
- Icon detection model (YOLO-based) is under AGPL license
- Icon caption models (BLIP2 & Florence) are under MIT license

If you use this project, please cite the original work:
```bibtex
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
