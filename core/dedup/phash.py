"""
labelkit.modules.dedup

Detect similar images using perceptual hash (pHash).
This module NEVER deletes files.
"""

import os
import json
from PIL import Image
import imagehash
from itertools import combinations

# -----------------------------
# Core hash logic
# -----------------------------

def compute_phash(img_path):
    try:
        with Image.open(img_path) as img:
            return imagehash.phash(img)
    except Exception as e:
        print(f"[WARN] skip {img_path}: {e}")
        return None


def hamming(a, b):
    return abs(a - b)


# -----------------------------
# Public API
# -----------------------------

def find_similar(
    image_dir,
    threshold=8,
):
    """
    Scan image_dir and return groups of similar images.

    Returns:
        [
          ["a.jpg", "b.jpg", "c.jpg"],
          ["x.png", "y.png"]
        ]
    """
    hashes = {}

    for f in sorted(os.listdir(image_dir)):
        path = os.path.join(image_dir, f)
        if not os.path.isfile(path):
            continue
        h = compute_phash(path)
        if h is not None:
            hashes[f] = h

    visited = set()
    groups = []

    for a, b in combinations(hashes.items(), 2):
        f1, h1 = a
        f2, h2 = b

        if hamming(h1, h2) <= threshold:
            if f1 in visited or f2 in visited:
                continue
            group = [f1, f2]
            visited.add(f1)
            visited.add(f2)
            groups.append(group)

    return groups

def mark_to_staging(
    files,
    staging_path
):
    """
    Add files to staging.json pending list.
    """
    if os.path.exists(staging_path):
        with open(staging_path) as f:
            try:
                data = json.load(f)
            except:
                data = {"pending": []}
    else:
        data = {"pending": []}

    for f in files:
        if f not in data["pending"]:
            data["pending"].append(f)

    with open(staging_path, "w") as f:
        json.dump(data, f, indent=2)

