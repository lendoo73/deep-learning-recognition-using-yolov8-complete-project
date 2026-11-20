import base64

from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
import numpy as np
from starlette.responses import JSONResponse
from ultralytics import YOLO
import supervision as sv

router = APIRouter(
    prefix="/brain_tumor",
    tags=["Brain Tumor"]
)

model = YOLO("models/best.pt")


@router.post("/predict")
async def predict_brain_tumor(image: UploadFile = File(...)):
    contents = await image.read()
    pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    np_img = np.array(pil_img)

    results = model(np_img, verbose=False)[0]

    # Process detections with NMS using supervision
    detections = sv.Detections.from_ultralytics(results).with_nms()

    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_image = np_img.copy()
    annotated_image = box_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

    # Prepare labels and confidences to return
    predicted_labels = [
        {"class": model.names[int(cls)], "confidence": float(conf)}
        for cls, conf in zip(detections.class_id, detections.confidence)
    ]

    # Convert annotated image (numpy array) to base64 string to return in JSON
    pil_annotated = Image.fromarray(annotated_image)
    buffered = io.BytesIO()
    pil_annotated.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return JSONResponse(
        content={
            "predictions": predicted_labels,
            "annotated_image_base64": img_str,
        }
    )
