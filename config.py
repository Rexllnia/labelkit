# config.py
import os

DATA = "data"

IMAGES = os.path.join(DATA, "images")
LABELS = os.path.join(DATA, "labels")

TRASH_I = os.path.join(DATA, "trash/images")
TRASH_L = os.path.join(DATA, "trash/labels")

STAGING = os.path.join(DATA, "staging.json")
COMMITS = os.path.join(DATA, "commits.json")

for d in [IMAGES, LABELS, TRASH_I, TRASH_L]:
    os.makedirs(d, exist_ok=True)
