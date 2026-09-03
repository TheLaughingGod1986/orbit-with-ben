#!/usr/bin/env python3
"""Rewrite Shorts indexes to live YouTube IDs and seed social remake keys.

Run from repo root. Does not post. Does not load LaunchAgents.
Source of live IDs: CHANNEL_AUDIT_2026-08-25/public_views.json (RSS 25 Aug night).
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
LONDON = ZoneInfo("Europe/London")
NOW = datetime.now(LONDON).isoformat(timespec="seconds")
PROJECTS = ROOT / "02_Video-Projects"


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {path.relative_to(ROOT)}")


def mark_dead(short: dict, *, reason: str) -> None:
    short["visibility"] = "private"
    short["published_now"] = False
    short["superseded"] = True
    short["unavailable"] = True
    short["index_rewritten_at"] = NOW
    note = (short.get("note") or "").rstrip()
    extra = f"Superseded {NOW[:10]} — {reason}"
    short["note"] = f"{note} · {extra}" if note else extra


def live_row(
    *,
    sid: str,
    file: str,
    title: str,
    video_id: str,
    schedule_iso: str,
    related: str,
    description: str,
    old_video_id: str | None = None,
    extra: dict | None = None,
) -> dict:
    row = {
        "id": sid,
        "file": file,
        "title": title,
        "schedule_iso": schedule_iso,
        "description": description,
        "video_id": video_id,
        "youtube_video_id": video_id,
        "url": f"https://youtu.be/{video_id}",
        "related": related,
        "visibility": "public",
        "published_now": True,
        "caption_style": "finalverdict-yellow-white-v02",
        "index_rewritten_at": NOW,
        "file_in_this_clone": False,
    }
    if old_video_id:
        row["old_video_id"] = old_video_id
    if extra:
        row.update(extra)
    return row


def seed_entry(
    *,
    video_id: str,
    title: str,
    file: str = "",
    project: str = "",
    status: str = "seeded",
    note: str = "",
    extra: dict | None = None,
) -> dict:
    entry = {
        "marked_at": NOW,
        "when": NOW,
        "title": title,
        "file": file,
        "youtube_id": video_id,
        "youtube_url": f"https://youtu.be/{video_id}",
        "project": project,
        "result_status": status,
        "status": status,
        "method": "index_rewrite_2026-08-25",
        "note": note,
    }
    if extra:
        entry.update(extra)
    return entry


def rewrite_001() -> None:
    path = PROJECTS / "001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(path.read_text())
    for s in data["shorts"]:
        mark_dead(
            s,
            reason="YouTube ID unavailable on 25 Aug audit; do not auto-mirror",
        )
    zoo = next(s for s in data["shorts"] if s["id"] == "03")
    data["shorts"].append(
        live_row(
            sid="03-live",
            file=zoo["file"],
            title="What If They're Leaving Us Alone On Purpose",
            video_id="03v4f1hlvtQ",
            schedule_iso="2026-08-19T11:30:00+01:00",
            related="Mo93x0fxB1Q",
            description=zoo["description"],
            old_video_id="rFJoOdQAc9c",
            extra={
                "related_ok": True,
                "note": "Live remake of zoo-hypothesis Short (rFJoOdQAc9c). RSS 25 Aug.",
            },
        )
    )
    data["updated"] = NOW
    data["audit"] = "00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-08-25/FULL_AUDIT.md"
    data["index_note"] = (
        "25 Aug rewrite: corpse Fermi IDs marked private. Live shelf only "
        "03v4f1hlvtQ on RSS. Remakes do not get a second social post."
    )
    dump(path, data)


def rewrite_002() -> None:
    path = PROJECTS / "002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(path.read_text())
    by_id = {s["id"]: s for s in data["shorts"]}
    for s in data["shorts"]:
        mark_dead(
            s,
            reason="Scheduled corpse ID (deleted). TikTok hammered these 25 Aug until pause",
        )
    data["shorts"].extend(
        [
            live_row(
                sid="03-live",
                file=by_id["03"]["file"],
                title="Time Appears to Stop at a Black Hole",
                video_id="tUAdhOnMW2g",
                schedule_iso="2026-08-07T12:30:00+01:00",
                related="n7CbJrOCnU0",
                description=by_id["03"]["description"],
                old_video_id="HvAKGjx4lv0",
                extra={
                    "note": "Public orphan (not in Uploads-only walks). Keep in inventory.",
                },
            ),
            live_row(
                sid="05-live",
                file=by_id["05"]["file"],
                title="What You Would See Falling Into a Black Hole",
                video_id="B2STcIAF1lY",
                schedule_iso="2026-08-09T12:30:00+01:00",
                related="n7CbJrOCnU0",
                description=by_id["05"]["description"],
                old_video_id="icedH_gK8JE",
                extra={
                    "note": "Public punch remake of photon-sphere Short. Confirm still public on posting Mac.",
                },
            ),
        ]
    )
    data["updated"] = NOW
    data["index_note"] = (
        "25 Aug rewrite: six corpse scheduled IDs marked private. Live: "
        "tUAdhOnMW2g + B2STcIAF1lY."
    )
    dump(path, data)


def rewrite_003() -> None:
    path = PROJECTS / "003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/SHORTS_UPLOAD_INDEX.json"
    data = json.loads(path.read_text())
    live_map = {
        "02": {
            "video_id": "M-VN84HCNls",
            "title": "We Found Planets Made of Diamond",
            "schedule_iso": "2026-08-14T11:30:00+01:00",
        },
        "03": {
            "video_id": "MDvAKtmKauw",
            "title": "Three Suns in the Sky — Real Alien Worlds",
            "schedule_iso": "2026-08-15T23:31:00+01:00",
        },
        "04": {
            "video_id": "tEOHYQbcgOw",
            "title": "This Planet's Night Never Cools Down",
            "schedule_iso": "2026-08-16T11:30:00+01:00",
        },
        "05": {
            "video_id": "OlwENQcY-jg",
            "title": "Why This Alien World Looks Like a Giant Eye",
            "schedule_iso": "2026-08-17T11:30:00+01:00",
        },
        "06": {
            "video_id": "QRi6Dxq0hz0",
            "title": "We Could Smell Alien Life in a Spectrum",
            "schedule_iso": "2026-08-18T11:30:00+01:00",
        },
    }
    for s in data["shorts"]:
        live = live_map.get(s["id"])
        if not live:
            mark_dead(
                s,
                reason="No live remake ID on 25 Aug RSS (glass-rain). Do not auto-mirror corpse ho9VJxp7f3A",
            )
            continue
        s["old_index_video_id"] = s.get("video_id")
        if s.get("old_video_id"):
            s.setdefault("historical_video_ids", [s["old_video_id"]])
        s["old_video_id"] = s.get("video_id")
        s["title"] = live["title"]
        s["video_id"] = live["video_id"]
        s["youtube_video_id"] = live["video_id"]
        s["url"] = f"https://youtu.be/{live['video_id']}"
        s["schedule_iso"] = live["schedule_iso"]
        s["visibility"] = "public"
        s["published_now"] = True
        s["superseded"] = False
        s["unavailable"] = False
        s["index_rewritten_at"] = NOW
        s["file_in_this_clone"] = False
        s["note"] = (
            f"Live remake {live['video_id']} (RSS 25 Aug). "
            f"Previous index ID {s['old_video_id']}. One social post per Short."
        )
        s["related"] = "b8-X_FyJnHM"
    data["long_id"] = "b8-X_FyJnHM"
    data["long_url"] = "https://youtu.be/b8-X_FyJnHM"
    data["updated"] = NOW
    data["index_note"] = (
        "25 Aug rewrite: diamond/three-suns/hot-jupiter/eyeball/habitability → live remake IDs. "
        "Glass-rain left superseded (no RSS id)."
    )
    dump(path, data)


def write_jwst() -> None:
    folder = PROJECTS / "004_JWST-Discoveries-That-Change-Everything/10_Shorts"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "06_Final-Exports").mkdir(parents=True, exist_ok=True)
    long_id = "ziKBPJ6FY0U"
    shorts = [
        {
            "id": "01",
            "file": "10_Shorts/06_Final-Exports/jwst_short-01_galaxies-too-early.mp4",
            "title": "These Galaxies Appeared Too Early",
            "schedule_iso": "2026-08-20T20:00:00+01:00",
            "video_id": "l1d1ypHxLk0",
            "note": "JWST launch Short. Threads profile had this caption twice — do not post a third.",
        },
        {
            "id": "02",
            "file": "10_Shorts/06_Final-Exports/jwst_short-02_black-holes-too-fast.mp4",
            "title": "Black Holes Grew Too Big, Too Fast",
            "schedule_iso": "2026-08-21T11:30:00+01:00",
            "video_id": "ZnsJTCcrTlA",
        },
        {
            "id": "03",
            "file": "10_Shorts/06_Final-Exports/jwst_short-03_textbook.mp4",
            "title": "Why JWST Pictures Don't Match the Textbook",
            "schedule_iso": "2026-08-22T11:30:00+01:00",
            "video_id": "P-li_ZWk4lg",
        },
        {
            "id": "04",
            "file": "10_Shorts/06_Final-Exports/jwst_short-04_infrared-eyes.mp4",
            "title": "What JWST's Infrared Eyes Can See",
            "schedule_iso": "2026-08-23T11:30:00+01:00",
            "video_id": "P32uaiserG0",
        },
        {
            "id": "05",
            "file": "10_Shorts/06_Final-Exports/jwst_short-05_universe-older.mp4",
            "title": "Is the Universe Older Than We Thought?",
            "schedule_iso": "2026-08-24T11:30:00+01:00",
            "video_id": "4-ZEpKD1yak",
        },
        {
            "id": "06",
            "file": "10_Shorts/06_Final-Exports/jwst_short-06_too-big-too-soon.mp4",
            "title": "JWST Keeps Finding Galaxies Too Big, Too Soon",
            "schedule_iso": "2026-08-25T11:30:00+01:00",
            "video_id": "68uTDP2esso",
            "note": "Posted YouTube 25 Aug 11:30 UK. Threads succeeded on posting Mac; Meta unconfirmed. Files not in this clone.",
        },
    ]
    rows = []
    for s in shorts:
        desc = (
            f"{s['title']}.\n\nThis is one moment from the full documentary.\n"
            f"Watch the full film:\nhttps://youtu.be/{long_id}\n\n"
            "#JWST #JamesWebb #Space #Shorts #OrbitWithBen"
        )
        rows.append(
            live_row(
                sid=s["id"],
                file=s["file"],
                title=s["title"],
                video_id=s["video_id"],
                schedule_iso=s["schedule_iso"],
                related=long_id,
                description=desc,
                extra={"note": s.get("note") or "Live JWST cluster Short. RSS 25 Aug."},
            )
        )
    data = {
        "long_id": long_id,
        "long_url": f"https://youtu.be/{long_id}",
        "long_title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "shorts": rows,
        "related_to_long": long_id,
        "caption_style": "finalverdict-yellow-white-v02",
        "funnel": "soft CTA on-screen + description full-film link + related video",
        "updated": NOW,
        "file_in_this_clone": False,
        "index_note": (
            "Created 25 Aug from live RSS IDs so social discover can see JWST. "
            "mp4s are not in this Git clone — watcher will not upload until files exist. "
            "Zero /go/ on Shorts. Seed Threads for 01+06; leave Meta unsown until IG grid confirmed."
        ),
    }
    dump(folder / "SHORTS_UPLOAD_INDEX.json", data)


def seed_ledgers() -> None:
    remakes = [
        {
            "video_id": "03v4f1hlvtQ",
            "title": "What If They're Leaving Us Alone On Purpose",
            "file": "10_Shorts/06_Final-Exports/aliens_short-03_zoo-hypothesis_v02.mp4",
            "project": "001_Will-We-Ever-Meet-Aliens",
            "note": "Remake of rFJoOdQAc9c. Do not post a second copy.",
        },
        {
            "video_id": "tUAdhOnMW2g",
            "title": "Time Appears to Stop at a Black Hole",
            "file": "10_Shorts/06_Final-Exports/blackhole_short-03_time-dilation_v02.mp4",
            "project": "002_What-Happens-If-You-Fall-Into-A-Black-Hole",
            "note": "Live remake. Seeded so watchers do not treat as new.",
        },
        {
            "video_id": "B2STcIAF1lY",
            "title": "What You Would See Falling Into a Black Hole",
            "file": "10_Shorts/06_Final-Exports/blackhole_short-05_photon-sphere_v02.mp4",
            "project": "002_What-Happens-If-You-Fall-Into-A-Black-Hole",
            "note": "Live remake. Seeded so watchers do not treat as new.",
        },
        {
            "video_id": "M-VN84HCNls",
            "title": "We Found Planets Made of Diamond",
            "file": "10_Shorts/06_Final-Exports/exoplanets_short-02_diamond_v02.mp4",
            "project": "003_Exoplanets-Strangest-Alien-Worlds",
            "note": "Remake of aoR-dA_g7eI. One IG/FB/Threads post.",
        },
        {
            "video_id": "MDvAKtmKauw",
            "title": "Three Suns in the Sky — Real Alien Worlds",
            "file": "10_Shorts/06_Final-Exports/exoplanets_short-03_three-suns_v02.mp4",
            "project": "003_Exoplanets-Strangest-Alien-Worlds",
            "note": "Remake of 6QFGAFZk264. One IG/FB/Threads post.",
        },
        {
            "video_id": "tEOHYQbcgOw",
            "title": "This Planet's Night Never Cools Down",
            "file": "10_Shorts/06_Final-Exports/exoplanets_short-04_hot-jupiter_v02.mp4",
            "project": "003_Exoplanets-Strangest-Alien-Worlds",
            "note": "Remake of eOOFVrJ2Ojc (retitled).",
        },
        {
            "video_id": "OlwENQcY-jg",
            "title": "Why This Alien World Looks Like a Giant Eye",
            "file": "10_Shorts/06_Final-Exports/exoplanets_short-05_eyeball_v02.mp4",
            "project": "003_Exoplanets-Strangest-Alien-Worlds",
            "note": "Remake of Web2otrTcT0 (retitled).",
        },
        {
            "video_id": "QRi6Dxq0hz0",
            "title": "We Could Smell Alien Life in a Spectrum",
            "file": "10_Shorts/06_Final-Exports/exoplanets_short-06_habitability_v02.mp4",
            "project": "003_Exoplanets-Strangest-Alien-Worlds",
            "note": "Remake of 1qts3tIsg9c (retitled).",
        },
    ]
    jwst_threads = [
        {
            "video_id": "l1d1ypHxLk0",
            "title": "These Galaxies Appeared Too Early",
            "file": "10_Shorts/06_Final-Exports/jwst_short-01_galaxies-too-early.mp4",
            "project": "004_JWST-Discoveries-That-Change-Everything",
            "status": "posted",
            "note": "On Threads profile twice (25 Aug audit). Seeded to block a third auto-post.",
        },
        {
            "video_id": "68uTDP2esso",
            "title": "JWST Keeps Finding Galaxies Too Big, Too Soon",
            "file": "10_Shorts/06_Final-Exports/jwst_short-06_too-big-too-soon.mp4",
            "project": "004_JWST-Discoveries-That-Change-Everything",
            "status": "posted",
            "note": "Threads succeeded on posting Mac 25 Aug. Permalink not in this clone.",
        },
    ]

    meta_path = ROOT / "00_Brand/Channel-Setup/Meta/META_POSTED.json"
    meta = json.loads(meta_path.read_text())
    posted = meta.setdefault("posted", {})
    for r in remakes:
        key = f"yt:{r['video_id']}"
        if key in posted:
            continue
        posted[key] = seed_entry(
            **r,
            extra={
                "instagram": {"status": "seeded"},
                "facebook": {"status": "seeded"},
            },
        )
    meta["updated_at"] = NOW
    meta["index_rewrite_note"] = (
        "25 Aug: seeded live remake IDs so uniqueness blocks a second IG/FB post. "
        "JWST not seeded on Meta — confirm Instagram grid before loading the watcher."
    )
    dump(meta_path, meta)

    th_path = ROOT / "00_Brand/Channel-Setup/Threads/THREADS_POSTED.json"
    th = json.loads(th_path.read_text())
    posted = th.setdefault("posted", {})
    for r in remakes + jwst_threads:
        key = f"yt:{r['video_id']}"
        if key in posted:
            continue
        posted[key] = seed_entry(**{k: r[k] for k in ("video_id", "title", "file", "project", "note")}, status=r.get("status", "seeded"))
        posted[key]["threads"] = {"status": r.get("status", "seeded")}
    th["updated_at"] = NOW
    th["index_rewrite_note"] = (
        "25 Aug: seeded remakes + JWST 01/06. Distance Short still has two permalinks "
        "(DblNwwOjOcl, DblMYecDCGa). Galaxies caption was duplicated on profile — delete extras in app."
    )
    dump(th_path, th)

    tt_path = ROOT / "00_Brand/Channel-Setup/TikTok/TIKTOK_POSTED.json"
    tt = json.loads(tt_path.read_text())
    posted = tt.setdefault("posted", {})
    for r in remakes:
        key = f"yt:{r['video_id']}"
        if key in posted:
            continue
        posted[key] = seed_entry(**r)
    tt["updated_at"] = NOW
    tt["index_rewrite_note"] = (
        "25 Aug: seeded live remake IDs. Uploads remain paused. Do not Post-now."
    )
    dump(tt_path, tt)


def main() -> None:
    rewrite_001()
    rewrite_002()
    rewrite_003()
    write_jwst()
    seed_ledgers()
    print("done", NOW)


if __name__ == "__main__":
    main()
