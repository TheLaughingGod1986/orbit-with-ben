#!/usr/bin/env python3
"""Rebuild SHORTS_UPLOAD_INDEX files to the live YouTube generation (25 Aug 2026).

The social mirrors (Meta / Threads / TikTok) and the funnel-comment watcher all
iterate these indexes. 001–003 still pointed at a deleted generation of video
ids (old titles, old ≥40s cuts), 005 had no index at all, and 006/007 lacked the
`schedule_iso` / `visibility` fields `is_live()` reads — so live Shorts never
mirrored, while one stale entry actually posted to Meta with a dead id.

Superseded arrays are kept in-file under `superseded_shorts_2026-08-25`.
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from build_scene_first_short_covers import JOBS, resolve  # noqa: E402

REPO = TOOLS.parents[2]
PROJ = REPO / "02_Video-Projects"
AUDIT = REPO / "00_Brand/Channel-Setup/audits/registry_rebuild_2026-08-25"
LONDON = ZoneInfo("Europe/London")

LIVE = {v["id"]: v for v in json.loads((AUDIT / "live_videos.json").read_text())}

LONGS = {
    "001_Will-We-Ever-Meet-Aliens": "Mo93x0fxB1Q",
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole": "3xrxdmaOwJI",
    "003_Exoplanets-Strangest-Alien-Worlds": "b8-X_FyJnHM",
    "004_JWST-Discoveries-That-Change-Everything": "ziKBPJ6FY0U",
    "005_The-Last-Star-In-The-Universe": "REXYxuLOBoI",
    "006_Could-Life-Exist-Under-The-Ice-Of-Europa": "NbW5G1BpPY0",
    "007_What-Happens-To-Your-Body-Near-A-Neutron-Star": "Yk1tLh23rko",
}


def project_of(path: str) -> str | None:
    p = Path(path)
    try:
        rel = p.relative_to(PROJ)
    except ValueError:
        return None
    return rel.parts[0]


def london_iso(utc_str: str) -> str:
    dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    return dt.astimezone(LONDON).isoformat(timespec="seconds")


def schedule_and_visibility(v: dict) -> tuple[str, str]:
    if v["privacy"] == "public":
        return london_iso(v["publishedAt"]), "public"
    if v.get("publishAt"):
        return london_iso(v["publishAt"]), "scheduled"
    return "", v["privacy"]


def live_entries_by_project() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for vid, pattern, _lines in JOBS:
        v = LIVE.get(vid)
        src = resolve(pattern)
        if not v or not src:
            continue
        project = project_of(src)
        if not project or project.startswith("_"):
            continue  # experiments have no index
        sched, vis = schedule_and_visibility(v)
        out.setdefault(project, []).append({
            "video_id": vid,
            "url": f"https://youtu.be/{vid}",
            "title": v["title"],
            "file": str(Path(src).relative_to(PROJ / project)),
            "description": v["description"],
            "tags": ",".join(v["tags"]),
            "made_for_kids": False,
            "related": LONGS[project],
            "schedule_iso": sched,
            "visibility": vis,
        })
    for entries in out.values():
        entries.sort(key=lambda e: e["schedule_iso"])
        for n, e in enumerate(entries, 1):
            e["id"] = f"{n:02d}"
    return out


def rebuild_full(project: str, entries: list[dict]) -> None:
    """001/002/003/005: replace the shorts array with the live generation."""
    idx_path = PROJ / project / "10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(idx_path.read_text()) if idx_path.exists() else {}
    old = data.get("shorts") or []
    if old:
        data["superseded_shorts_2026-08-25"] = old
    long_id = LONGS[project]
    data["shorts"] = entries
    data["long_id"] = long_id
    data["long_url"] = f"https://youtu.be/{long_id}"
    data.pop("long_placeholder", None)
    data["updated"] = "2026-08-25"
    data["note"] = ("Rebuilt to the live YouTube generation (25 Aug 2026). Old ids were a "
                    "deleted generation; social mirrors and the funnel watcher read this file.")
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{project}: wrote {len(entries)} live shorts (superseded {len(old)})")


def refresh_in_place(project: str) -> None:
    """004/006/007: keep entry shape, refresh live fields + normalise mirror fields."""
    idx_path = PROJ / project / "10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(idx_path.read_text())
    n = 0
    for e in data.get("shorts") or []:
        vid = (e.get("video_id") or e.get("youtube_id") or e.get("youtube_video_id") or "").strip()
        v = LIVE.get(vid)
        if not v:
            e["missing_on_youtube_2026-08-25"] = True
            continue
        sched, vis = schedule_and_visibility(v)
        e["video_id"] = vid
        e["url"] = f"https://youtu.be/{vid}"
        e["title"] = v["title"]
        e["schedule_iso"] = sched
        e["visibility"] = vis
        if not e.get("file"):
            src = next((resolve(pat) for i, pat, _ in JOBS if i == vid), None)
            if src:
                e["file"] = str(Path(src).relative_to(PROJ / project))
        n += 1
    data["updated"] = "2026-08-25"
    idx_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{project}: refreshed {n} entries in place")


def main() -> None:
    by_project = live_entries_by_project()
    for project in ("001_Will-We-Ever-Meet-Aliens",
                    "002_What-Happens-If-You-Fall-Into-A-Black-Hole",
                    "003_Exoplanets-Strangest-Alien-Worlds",
                    "005_The-Last-Star-In-The-Universe"):
        rebuild_full(project, by_project.get(project, []))
    for project in ("004_JWST-Discoveries-That-Change-Everything",
                    "006_Could-Life-Exist-Under-The-Ice-Of-Europa",
                    "007_What-Happens-To-Your-Body-Near-A-Neutron-Star"):
        refresh_in_place(project)
    skipped = {p: len(v) for p, v in by_project.items() if p not in LONGS}
    if skipped:
        print("skipped (no index home):", skipped)


if __name__ == "__main__":
    main()
