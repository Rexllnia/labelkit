# core/image/draw.py
from PIL import Image, ImageDraw

def draw_yolo_boxes(img_path, boxes, color=(255,0,0), width=2):
    """
    boxes: [(cls, x, y, w, h)] normalized
    """
    img = Image.open(img_path).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    for cls, x, y, w, h in boxes:
        cx, cy = x * W, y * H
        bw, bh = w * W, h * H

        x1 = cx - bw / 2
        y1 = cy - bh / 2
        x2 = cx + bw / 2
        y2 = cy + bh / 2

        draw.rectangle([x1, y1, x2, y2], outline=color, width=width)

    return img
