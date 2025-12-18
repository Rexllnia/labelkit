import json, os
from config import STAGING

def _load():
    if not os.path.exists(STAGING):
        return {"pending": []}
    with open(STAGING) as f:
        txt = f.read().strip()
        return json.loads(txt) if txt else {"pending": []}

def _save(data):
    with open(STAGING, "w") as f:
        json.dump(data, f, indent=2)

def get():
    return _load()

def mark(img):
    s = _load()
    if img not in s["pending"]:
        s["pending"].append(img)
    _save(s)

def unmark(img):
    s = _load()
    if img in s["pending"]:
        s["pending"].remove(img)
    _save(s)

def clear():
    _save({"pending": []})
