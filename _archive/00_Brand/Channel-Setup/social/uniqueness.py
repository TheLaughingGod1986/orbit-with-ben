"""One unique Short per social platform — no remake / file / title duplicates.

Ben (25 Aug 2026): one Instagram reel, one Facebook reel, one Threads post
per unique Short. In any window of ~30 posts, each item must be a different
video. Recuts and new YouTube IDs of the same title/file do not get a second
post.
"""
from __future__ import annotations

import re
from pathlib import Path

UNIQUE_WINDOW = 30
DONE_STATUSES = {
    "ok",
    "partial",
    "posted",
    "posted_link_card",
    "posted_permalink_only",
    "skipped",
    "seeded",
    "disabled",
    "scheduled",
    "scheduled_covered",
    "unconfirmed",
}


def normalize_title(title: str) -> str:
    text = (title or "").lower()
    text = re.sub(r"[|#].*$", "", text)
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def file_slug(path: str) -> str:
    name = Path(path or "").stem.lower()
    if not name:
        return ""
    name = re.sub(r"_(v\d+|diamond|cdp|punch|captions|titlecta|smooth|normal).*$", "", name)
    return name


def youtube_id(short: dict) -> str:
    return (
        short.get("video_id")
        or short.get("youtube_id")
        or short.get("youtube_video_id")
        or ""
    ).strip()


def fingerprints(short: dict) -> set[str]:
    keys: set[str] = set()
    vid = youtube_id(short)
    if vid:
        keys.add(f"yt:{vid}")
    slug = file_slug(short.get("file") or short.get("_abs_file") or short.get("path") or "")
    if slug:
        keys.add(f"file:{slug}")
    title = normalize_title(short.get("title") or "")
    if title:
        keys.add(f"title:{title}")
    return {k for k in keys if k.split(":", 1)[-1]}


def entry_fingerprints(key: str, entry: dict) -> set[str]:
    blob = dict(entry or {})
    blob.setdefault("video_id", blob.get("youtube_id") or "")
    if key.startswith("yt:") and "video_id" not in blob:
        blob["video_id"] = key[3:]
    keys = fingerprints(blob)
    if key:
        keys.add(key)
    return keys


def entry_is_done(entry: dict, *, platform: str | None = None) -> bool:
    if not entry:
        return False
    if entry.get("status") in DONE_STATUSES:
        return True
    if entry.get("result_status") in DONE_STATUSES:
        return True
    if platform:
        plat = entry.get(platform)
        return isinstance(plat, dict) and plat.get("status") in DONE_STATUSES
    for name in ("instagram", "facebook", "threads"):
        plat = entry.get(name)
        if isinstance(plat, dict) and plat.get("status") in DONE_STATUSES:
            return True
    return False


def already_mirrored(short: dict, posted: dict, *, platform: str | None = None) -> bool:
    """True if this Short (or a remake / same file / same title) is already on the ledger."""
    want = fingerprints(short)
    if not want:
        return False
    for key, entry in (posted or {}).items():
        if not entry_is_done(entry, platform=platform):
            # still count scheduled / posted umbrella even if platform slice missing
            if not entry_is_done(entry):
                continue
        have = entry_fingerprints(key, entry)
        if want & have:
            return True
    return False


def recent_content_keys(posted: dict, *, limit: int = UNIQUE_WINDOW) -> set[str]:
    items = []
    for key, entry in (posted or {}).items():
        if not entry_is_done(entry):
            continue
        when = entry.get("marked_at") or entry.get("when") or ""
        items.append((str(when), key, entry))
    items.sort(reverse=True)
    out: set[str] = set()
    for _, key, entry in items[:limit]:
        out |= {
            k
            for k in entry_fingerprints(key, entry)
            if k.startswith(("file:", "title:"))
        }
    return out


def is_repeat_in_window(short: dict, posted: dict, *, limit: int = UNIQUE_WINDOW) -> bool:
    want = {k for k in fingerprints(short) if k.startswith(("file:", "title:"))}
    if not want:
        return False
    return bool(want & recent_content_keys(posted, limit=limit))


def first_unique(shorts: list[dict], posted: dict, *, platform: str | None = None) -> list[dict]:
    """Keep the first live copy of each unique Short; drop remakes and batch dups."""
    seen: set[str] = set()
    unique: list[dict] = []
    for s in shorts:
        if already_mirrored(s, posted, platform=platform):
            continue
        if is_repeat_in_window(s, posted):
            continue
        fps = fingerprints(s)
        if fps & seen:
            continue
        seen |= fps
        unique.append(s)
    return unique
