#!/usr/bin/env python3
"""Listing package readiness for Passed / Scheduled cards and the upload/social handoff (Ben, 7 Nov 2026).

A package is complete when title, thumbnail, description and tags are set. The Videos Passed lane
shows what's missing, or "Ready to upload" / "Ready to post". Scheduled cards show a real
publishAt in London time only — never invent YouTube ids or schedule times.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTING_FIELDS = ("title", "thumbnail", "description", "tags")


def _text(value) -> str:
    return str(value or "").strip()


def _exists(root: Path, rel: str) -> bool:
    if not rel:
        return False
    p = Path(rel)
    cands = [p] if p.is_absolute() else [root / rel]
    return any(c.is_file() for c in cands)


def load_manifest(path: Path | None) -> dict | None:
    if not path or not path.is_file():
        return None
    try:
        doc = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return doc if isinstance(doc, dict) else None


def find_manifest(root: Path, *, number: str = "", vtype: str = "", package_dir: str = "") -> Path | None:
    """Best PACKAGE_MANIFEST.json for a film/Short when one exists on disk. No invention."""
    if package_dir:
        folder = Path(package_dir) if Path(package_dir).is_absolute() else root / package_dir
        for name in ("PACKAGE_MANIFEST.json", "package_manifest.json"):
            hit = folder / name
            if hit.is_file():
                return hit
    num = re.sub(r"\D", "", str(number or ""))[:3]
    projects = root / "02_Video-Projects"
    if not num or not projects.is_dir():
        return None
    folders = sorted(projects.glob(f"{num}_*"))
    if not folders:
        return None
    film = folders[0]
    if vtype == "short":
        shorts = sorted(film.glob("10_Shorts/*/11_Upload-Package/PACKAGE_MANIFEST.json"))
        if len(shorts) == 1:
            return shorts[0]
        long_m = film / "11_Upload-Package" / "PACKAGE_MANIFEST.json"
        return long_m if long_m.is_file() else None
    hit = film / "11_Upload-Package" / "PACKAGE_MANIFEST.json"
    return hit if hit.is_file() else None


def missing_fields(manifest: dict | None, root: Path | None = None) -> list[str]:
    """Which of title / thumbnail / description / tags are unset or point at a missing relative file."""
    root = root or ROOT
    if not isinstance(manifest, dict):
        return list(LISTING_FIELDS)
    missing: list[str] = []
    if not _text(manifest.get("title")):
        missing.append("title")
    thumb = _text(manifest.get("thumbnail") or ((manifest.get("thumbnailAbc") or [None])[0]))
    if not thumb:
        missing.append("thumbnail")
    elif root and not thumb.startswith(("/", "~")) and not _exists(root, thumb):
        missing.append("thumbnail")
    desc_inline = _text(manifest.get("description"))
    desc_file = _text(manifest.get("descriptionFile"))
    if not desc_inline and not desc_file:
        missing.append("description")
    elif desc_file and not desc_inline and root and not _exists(root, desc_file):
        missing.append("description")
    tags = manifest.get("tags")
    tags_file = _text(manifest.get("tagsFile"))
    if isinstance(tags, list):
        ok = any(_text(t) for t in tags)
    else:
        ok = bool(_text(tags) or tags_file)
    if not ok:
        missing.append("tags")
    elif tags_file and not _text(tags) and root and not _exists(root, tags_file):
        missing.append("tags")
    return missing


def destination_of(video: dict | None = None, manifest: dict | None = None, approved: dict | None = None) -> str:
    """youtube (default) or social (Buffer). Never invents a YouTube id."""
    for src in (video or {}, approved or {}, ((video or {}).get("approved") or {}), manifest or {}):
        if not isinstance(src, dict):
            continue
        dest = _text(src.get("destination") or src.get("deliverTo")).lower()
        if dest in ("social", "buffer"):
            return "social"
        if src.get("socialOnly") is True:
            return "social"
        blob = " ".join(_text(src.get(k)) for k in ("what", "title", "format", "kind"))
        if re.search(r"\bsocial[\s_-]?only\b", blob, re.I):
            return "social"
    return "youtube"


def schedule_status(youtube: dict | None) -> str:
    """Plain schedule line from a known publishAt only — never invents a slot."""
    yt = youtube or {}
    if yt.get("state") != "scheduled" and not (yt.get("publishAt") and yt.get("privacy") == "private"):
        return ""
    london = _text(yt.get("publishAtLondon"))
    if london:
        clean = re.sub(r"\s*(GMT|BST|UTC)\s*$", "", london).strip()
        if not re.search(r"\bLondon\b", clean, re.I):
            clean = f"{clean} London"
        return f"Scheduled for {clean}"
    if yt.get("publishAt"):
        return f"Scheduled for {yt['publishAt']}"
    return ""


def status_line(*, missing: list[str], youtube: dict | None = None, destination: str = "youtube") -> str:
    sched = schedule_status(youtube)
    if sched:
        return sched
    if missing:
        return "Needs " + ", ".join(missing)
    if destination == "social":
        return "Ready to post"
    return "Ready to upload"


def inspect(manifest: dict | None = None, *, root: Path | None = None, youtube: dict | None = None,
            destination: str = "youtube", path: Path | None = None) -> dict:
    root = root or ROOT
    doc = manifest if manifest is not None else load_manifest(path)
    missing = missing_fields(doc, root)
    dest = destination if destination != "youtube" else destination_of(manifest=doc)
    return {
        "complete": not missing,
        "missing": missing,
        "destination": dest,
        "status": status_line(missing=missing, youtube=youtube, destination=dest),
        "manifestPath": str(path) if path else "",
        "title": _text((doc or {}).get("title")),
    }


def for_video(video: dict, root: Path | None = None) -> dict:
    """Listing block to attach on a tracker video (Passed / Scheduled)."""
    root = root or ROOT
    yt = video.get("youtube") or {}
    approved = video.get("approved") if isinstance(video.get("approved"), dict) else {}
    dest = destination_of(video, approved=approved)
    pkg = ""
    for src in (video, approved):
        if isinstance(src, dict) and src.get("packageDir"):
            pkg = str(src.get("packageDir"))
            break
    path = find_manifest(root, number=str(video.get("number") or ""), vtype=str(video.get("type") or ""),
                         package_dir=pkg)
    if isinstance(video.get("listing"), dict) and video["listing"].get("missing") is not None and not path:
        base = dict(video["listing"])
        base.setdefault("destination", dest)
        base["status"] = status_line(missing=list(base.get("missing") or []), youtube=yt,
                                     destination=base.get("destination") or dest)
        base["complete"] = not list(base.get("missing") or [])
        return base
    return inspect(path=path, root=root, youtube=yt, destination=dest)
