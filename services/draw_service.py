import os, io, base64
from config import IMAGES, LABELS
from core.yolo.parser import load_yolo_labels
from core.image.draw import draw_yolo_boxes

def draw(image_name):
    """
    返回 base64 PNG
    """
    img_path = os.path.join(IMAGES, image_name)
    label_path = os.path.join(
        LABELS, image_name.rsplit(".",1)[0] + ".txt"
    )

    if not os.path.exists(img_path):
        return None

    boxes = []
    if os.path.exists(label_path):
        boxes = load_yolo_labels(label_path)

    img = draw_yolo_boxes(img_path, boxes)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "image": image_name,
        "boxes": len(boxes),
        "data": b64
    }
