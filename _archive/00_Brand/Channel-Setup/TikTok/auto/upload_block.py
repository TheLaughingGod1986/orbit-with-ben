"""Hard stop for TikTok uploads while the account is banned."""
from __future__ import annotations

import json
import os
from pathlib import Path

SETUP = Path(__file__).resolve().parents[1]
BLOCK = SETUP / "TIKTOK_UPLOAD_BLOCK.json"
MESSAGE = (
    "TikTok uploads are paused (account ban). No posts until Ben lifts "
    "TIKTOK_UPLOAD_BLOCK.json and says so."
)


def uploads_paused() -> bool:
    env = (os.environ.get("TIKTOK_UPLOADS_PAUSED") or "").strip().lower()
    if env in {"1", "true", "yes"}:
        return True
    if env in {"0", "false", "no"}:
        return False
    if not BLOCK.exists():
        return False
    try:
        data = json.loads(BLOCK.read_text())
    except Exception:
        return True
    return bool(data.get("paused"))


def blocked_result() -> dict:
    return {"status": "paused", "reason": "tiktok_ban", "message": MESSAGE}
