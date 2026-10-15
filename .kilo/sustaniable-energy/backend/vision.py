import io
from PIL import Image
from ultralytics import YOLO

EQUIPMENT = {
    "laptop": "Computer Workstation",
    "tv": "Display/Projector Screen",
    "keyboard": "Computer",
    "mouse": "Computer",
    "microwave": "Microwave",
    "refrigerator": "Refrigerator",
}
_model = None


def _get_model() -> YOLO:
    global _model
    if _model is None:
        _model = YOLO("yolov8n.pt")
    return _model


def detect(image_bytes: bytes) -> dict:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    result = _get_model()(img, conf=0.35, verbose=False)[0]
    image_height, image_width = result.orig_shape
    detections = [
        {
            "label": result.names[int(box.cls)],
            "display": result.names[int(box.cls)].replace("_", " ").title(),
            "confidence": round(float(box.conf), 2),
            "box": [
                round(float(box.xyxy[0][0]) / image_width * 100, 2),
                round(float(box.xyxy[0][1]) / image_height * 100, 2),
                round(float(box.xyxy[0][2] - box.xyxy[0][0]) / image_width * 100, 2),
                round(float(box.xyxy[0][3] - box.xyxy[0][1]) / image_height * 100, 2),
            ],
        }
        for box in result.boxes
    ]
    people = sum(1 for d in detections if d["label"] == "person")
    equipment = sorted({EQUIPMENT[d["label"]] for d in detections if d["label"] in EQUIPMENT})
    return {"detections": detections, "people": people, "equipment_visible": equipment}
