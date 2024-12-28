import runpod
import base64
from PIL import Image
import io
from api import process

def handler(event):
    """
    RunPod serverless handler
    """
    try:
        # Get input data
        if not event.get("input"):
            raise ValueError("No input provided")

        # Get image data
        image_data = event["input"].get("image")
        if not image_data:
            raise ValueError("No image provided")

        # Convert base64 to PIL Image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Get parameters
        params = {
            "box_threshold": event["input"].get("box_threshold", 0.05),
            "iou_threshold": event["input"].get("iou_threshold", 0.1),
            "use_paddleocr": event["input"].get("use_paddleocr", False),
            "imgsz": event["input"].get("imgsz", 1920),
            "icon_process_batch_size": event["input"].get("icon_process_batch_size", 64)
        }

        # Process image
        processed_image, parsed_content_list, label_coordinates = process(
            image,
            **params
        )

        # Convert processed image to base64
        buffered = io.BytesIO()
        processed_image.save(buffered, format="PNG")
        processed_image_b64 = base64.b64encode(buffered.getvalue()).decode()

        return {
            "image": processed_image_b64,
            "parsed_content_list": parsed_content_list,
            "label_coordinates": label_coordinates
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({
        "handler": handler
    })
