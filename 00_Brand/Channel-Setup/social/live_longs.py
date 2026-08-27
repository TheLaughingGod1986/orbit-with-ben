#!/usr/bin/env python3
"""Discover live YouTube longs that still need a soft social link share.

Longs are shared as YouTube link cards / link posts (not Reels). Shorts stay
on the existing Meta/Threads Shorts watchers. TikTok stays paused.
"""
from __future__ import annotations

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parents[3]
SETUP = Path(__file__).resolve().parents[1]
LEDGER = SETUP / "social" / "LONGS_POSTED.json"
LONDON = ZoneInfo("Europe/London")
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"

# Public / soon-public Thursday films (source of truth for long social share).
KNOWN_LONGS = [
    {
        "video_id": "Mo93x0fxB1Q",
        "title": "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained",
        "url": "https://youtu.be/Mo93x0fxB1Q",
        "status": "public",
    },
    {
        "video_id": "3xrxdmaOwJI",
        "title": "What Happens If You Fall Into a Black Hole?",
        "url": "https://youtu.be/3xrxdmaOwJI",
        "status": "public",
    },
    {
        "video_id": "b8-X_FyJnHM",
        "title": "Alien Worlds: The Strangest Planets We've Ever Found",
        "url": "https://youtu.be/b8-X_FyJnHM",
        "status": "public",
    },
    {
        "video_id": "ziKBPJ6FY0U",
        "title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "url": "https://youtu.be/ziKBPJ6FY0U",
        "status": "public",
    },
    {
        "video_id": "REXYxuLOBoI",
        "title": "What Happens When the Last Star Dies?",
        "url": "https://youtu.be/REXYxuLOBoI",
        "status": "premiere",  # Thu 27 Aug 18:00 London
    },
    {
        "video_id": "NbW5G1BpPY0",
        "title": "Could Life Exist Under The Ice Of Europa?",
        "url": "https://youtu.be/NbW5G1BpPY0",
        "status": "scheduled",  # Thu 3 Sept
    },
]

DONE = {
    "ok",
    "posted",
    "posted_link_card",
    "posted_permalink_only",
    "seeded",
    "skipped",
    "partial",
}


def load_ledger() -> dict:
    if not LEDGER.exists():
        return {"version": 1, "posted": {}, "updated_at": None}
    return json.loads(LEDGER.read_text())


def save_ledger(data: dict) -> None:
    data["updated_at"] = datetime.now(LONDON).isoformat()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")


def mark_posted(video_id: str, platform: str, result: dict, *, title: str = "") -> None:
    data = load_ledger()
    posted = data.setdefault("posted", {})
    key = f"yt:{video_id}"
    entry = posted.get(key) or {
        "youtube_id": video_id,
        "title": title,
        "youtube_url": f"https://youtu.be/{video_id}",
        "marked_at": datetime.now(LONDON).isoformat(),
    }
    entry[platform] = {
        "status": result.get("status") or "posted_link_card",
        "when": datetime.now(LONDON).isoformat(),
        **{k: v for k, v in result.items() if k != "status"},
    }
    # umbrella status when any platform posted
    entry["status"] = "posted_link_card"
    entry["marked_at"] = datetime.now(LONDON).isoformat()
    if title:
        entry["title"] = title
    posted[key] = entry
    save_ledger(data)


def platform_done(entry: dict | None, platform: str) -> bool:
    if not entry:
        return False
    plat = entry.get(platform)
    if isinstance(plat, dict) and plat.get("status") in DONE:
        return True
    return False


def rss_public_ids() -> dict[str, dict]:
    """video_id -> {title, published} for latest channel items."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        root = ET.fromstring(resp.read())
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    out: dict[str, dict] = {}
    for entry in root.findall("atom:entry", ns):
        vid = entry.findtext("yt:videoId", default="", namespaces=ns)
        title = entry.findtext("atom:title", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        if vid:
            out[vid] = {"title": title, "published": published}
    return out


def watch_page_public(video_id: str) -> bool:
    """True only when the long is actually watchable (not a waiting premiere)."""
    try:
        req = urllib.request.Request(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", "ignore")
        low = html.lower()
        if "premiere" in low and (
            "waiting" in low
            or "scheduled for" in low
            or '"playabilitystatus":{"status":"live_stream_offline"' in low
            or "will premiere" in low
        ):
            return False
        if "UNPLAYABLE" in html:
            return False
        return '"playabilityStatus":{"status":"OK"' in html or '"viewCount"' in html
    except Exception:
        return False


def is_long_live(film: dict, rss: dict[str, dict]) -> bool:
    vid = film["video_id"]
    status = (film.get("status") or "").lower()
    if status == "public":
        return True
    if status in {"premiere", "scheduled"}:
        # Only share once actually watchable.
        return watch_page_public(vid)
    if vid in rss:
        return True
    return watch_page_public(vid)


def long_caption(film: dict) -> str:
    title = film.get("title") or "New film"
    url = film.get("url") or f"https://youtu.be/{film['video_id']}"
    return (
        f"{title}\n\n"
        f"Now on YouTube → {url}\n\n"
        f"#space #orbitwithben"
    )


def pending_live_longs(*, platform: str) -> list[dict]:
    """Return live longs not yet shared on this platform (at most a few)."""
    ledger = load_ledger().get("posted") or {}
    rss = rss_public_ids()
    pending: list[dict] = []
    for film in KNOWN_LONGS:
        vid = film["video_id"]
        entry = ledger.get(f"yt:{vid}")
        if platform_done(entry, platform):
            continue
        if not is_long_live(film, rss):
            continue
        item = dict(film)
        if vid in rss and rss[vid].get("title"):
            item["title"] = rss[vid]["title"]
        item["_caption"] = long_caption(item)
        item["_ledger_key"] = f"yt:{vid}"
        pending.append(item)
    # Prefer newest public films first (JWST before older catalogue).
    pending.sort(
        key=lambda f: 0
        if f["video_id"] == "ziKBPJ6FY0U"
        else 1
        if f["video_id"] in {"b8-X_FyJnHM", "3xrxdmaOwJI", "Mo93x0fxB1Q"}
        else 2
    )
    return pending
