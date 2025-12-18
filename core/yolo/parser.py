# core/yolo/parser.py

def load_yolo_labels(label_path):
    """
    return: list of (cls, x, y, w, h)  all normalized
    """
    boxes = []
    with open(label_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                cls, x, y, w, h = map(float, line.split())
                boxes.append((int(cls), x, y, w, h))
            except:
                continue
    return boxes
