"""
labelkit.modules.commit

Commit / rollback manager.
No Flask, no UI, pure logic.
"""

import os
import json
import time
import shutil


# -------------------------
# Utils
# -------------------------

def _load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            txt = f.read().strip()
            return json.loads(txt) if txt else default
    except Exception as e:
        print(f"[WARN] load {path} failed:", e)
        return default


def _save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


# -------------------------
# Public API
# -------------------------

def commit_delete(
    files,
    image_dir,
    label_dir,
    trash_image_dir,
    trash_label_dir,
    commit_file
):
    """
    Commit a delete operation.
    Move files to trash and record commit.
    """
    if not files:
        return None

    commits = _load_json(commit_file, [])
    cid = len(commits) + 1

    record = {
        "id": cid,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": files
    }

    for img in files:
        src = os.path.join(image_dir, img)
        if os.path.exists(src):
            shutil.move(src, os.path.join(trash_image_dir, img))

        lab = os.path.splitext(img)[0] + ".txt"
        lab_src = os.path.join(label_dir, lab)
        if os.path.exists(lab_src):
            shutil.move(lab_src, os.path.join(trash_label_dir, lab))

    commits.append(record)
    _save_json(commit_file, commits)

    return record


def list_commits(commit_file):
    """Return commit history."""
    return _load_json(commit_file, [])


def rollback_commit(
    commit_id,
    image_dir,
    label_dir,
    trash_image_dir,
    trash_label_dir,
    commit_file
):
    """
    Rollback a commit by id.
    """
    commits = _load_json(commit_file, [])
    rec = next((c for c in commits if c["id"] == commit_id), None)
    if not rec:
        return False

    for img in rec["files"]:
        src = os.path.join(trash_image_dir, img)
        if os.path.exists(src):
            shutil.move(src, os.path.join(image_dir, img))

        lab = os.path.splitext(img)[0] + ".txt"
        lab_src = os.path.join(trash_label_dir, lab)
        if os.path.exists(lab_src):
            shutil.move(lab_src, os.path.join(label_dir, lab))

    # remove commit record
    commits = [c for c in commits if c["id"] != commit_id]
    _save_json(commit_file, commits)

    return True
