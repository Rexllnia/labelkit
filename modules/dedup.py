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


def choose_candidates(groups, keep="first"):
    """
    Decide which images should be removed.

    keep:
        - "first": keep first image
        - "last": keep last image

    Returns:
        ["b.jpg", "c.jpg", ...]
    """
    remove = []

    for g in groups:
        if len(g) <= 1:
            continue
        if keep == "first":
            remove.extend(g[1:])
        else:
            remove.extend(g[:-1])

    return remove


# -----------------------------
# Optional integration: staging
# -----------------------------

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


# -----------------------------
# CLI usage
# -----------------------------

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True)
    ap.add_argument("--threshold", type=int, default=8)
    ap.add_argument("--staging", default=None)
    args = ap.parse_args()

    groups = find_similar(args.images, args.threshold)
    to_remove = choose_candidates(groups)

    print("Similar groups:")
    for g in groups:
        print("  ", g)

    print("\nSuggested remove:")
    for f in to_remove:
        print("  ", f)

    if args.staging:
        mark_to_staging(to_remove, args.staging)
        print(f"\nMarked {len(to_remove)} files to staging")
