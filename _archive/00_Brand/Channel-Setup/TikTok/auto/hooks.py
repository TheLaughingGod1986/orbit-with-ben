#!/usr/bin/env python3
"""Hook for YouTube publish-now scripts: mirror one short to TikTok after it goes public."""
from __future__ import annotations

import sys
from pathlib import Path

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from caption import confirm_needle, tiktok_caption  # noqa: E402
from discover import resolve_file  # noqa: E402
from ensure_chrome import ensure_chrome  # noqa: E402
from ledger import is_posted, mark_posted  # noqa: E402
from studio_upload import post_short  # noqa: E402
from upload_block import blocked_result, uploads_paused  # noqa: E402


def notify_short_live(project_root: str | Path, short: dict) -> dict:
    """
    Call after a short is set Public on YouTube.

    project_root: video project folder (contains 10_Shorts/)
    short: entry from SHORTS_UPLOAD_INDEX.json
    """
    if uploads_paused():
        return blocked_result()

    project_root = Path(project_root)
    item = dict(short)
    item["_project"] = project_root.name
    if is_posted(item):
        return {"status": "already_posted", "key": item.get("video_id")}

    path = resolve_file(project_root, item)
    if not path or not path.exists():
        return {"status": "missing_file", "file": item.get("file")}

    chrome = ensure_chrome()
    if not chrome.get("ok"):
        return {"status": "chrome_unavailable", "error": chrome.get("error")}

    caption = tiktok_caption(item)
    needle = confirm_needle(item, caption)
    result = post_short(
        video_path=path,
        caption=caption,
        confirm_needle=needle,
        audit_dir=AUTO.parent / "audit" / "auto",
    )
    if result.get("status") == "ok":
        mark_posted(item, result)
    return result
