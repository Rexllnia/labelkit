from core.dedup.phash import find_similar
from core.dedup.selector import choose_candidates
from services import staging_service
from config import IMAGES

def run(cfg):
    algo = cfg.get("algo", "phash")
    threshold = int(cfg.get("threshold", 8))
    keep = cfg.get("keep", "first")
    auto_stage = cfg.get("auto_stage", True)

    if algo != "phash":
        return {"error": "unknown algo"}

    groups = find_similar(IMAGES, threshold)
    remove = choose_candidates(groups, keep)

    if auto_stage:
        for img in remove:
            staging_service.mark(img)

    return {
        "algo": algo,
        "threshold": threshold,
        "groups": groups,
        "marked": remove
    }
