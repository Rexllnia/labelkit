def validate_yolo_line(line):
    try:
        cls, x, y, w, h = map(float, line.split())
        return (
            0 <= x <= 1 and
            0 <= y <= 1 and
            0 < w <= 1 and
            0 < h <= 1
        )
    except:
        return False
