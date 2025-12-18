from modules.commit import commit_delete, rollback_commit, list_commits
from services import staging_service
from config import IMAGES, LABELS, TRASH_I, TRASH_L, COMMITS

def commit():
    s = staging_service.get()
    if not s["pending"]:
        return None

    record = commit_delete(
        files=s["pending"],
        image_dir=IMAGES,
        label_dir=LABELS,
        trash_image_dir=TRASH_I,
        trash_label_dir=TRASH_L,
        commit_file=COMMITS
    )

    staging_service.clear()
    return record

def history():
    return list_commits(COMMITS)

def rollback(cid):
    return rollback_commit(
        commit_id=cid,
        image_dir=IMAGES,
        label_dir=LABELS,
        trash_image_dir=TRASH_I,
        trash_label_dir=TRASH_L,
        commit_file=COMMITS
    )
