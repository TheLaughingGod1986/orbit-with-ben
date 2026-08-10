#!/usr/bin/env python3
"""Black-hole punch-first Shorts v03 — 22–28s discovery cuts.

Retention rule (locked):
  strongest-fact open in 0–1.5s · curiosity-gap end · soft CTA last ~3s
  Related parent: 3xrxdmaOwJI

Does NOT upload. Publishing freeze may still be ON — exports only.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
MASTER = ROOT / "09_Final-Export/blackhole_v06_SMOOTH_NORMAL_UPLOAD_READY_MASTER.mp4"
OUT = ROOT / "10_Shorts/06_Final-Exports"
SYNC_DIR = ROOT / "10_Shorts/07_Caption-Sync"
LONG_URL = "https://youtu.be/3xrxdmaOwJI"
LONG_ID = "3xrxdmaOwJI"

CAPTION_LIB = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/auto"
)
sys.path.insert(0, str(CAPTION_LIB))
from onscreen_captions import (  # noqa: E402
    auto_beats_from_phrases,
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)

# Durations locked inside 22–28s. Starts chosen so the spoken hook lands early.
SHORTS = [
    {
        "id": "p01",
        "slug": "cross-this-line",
        "start": 762.208,
        "duration": 26.0,
        "role": "Hook",
        "hook": "cross this line",
        "phrases": ["cross this line", "and you never", "come back"],
        "title": "Cross This Line and You Never Come Back",
    },
    {
        "id": "p02",
        "slug": "wouldnt-feel-like-falling",
        "start": 660.208,
        "duration": 26.0,
        "role": "Fact",
        "hook": "wouldn't feel",
        "phrases": ["falling in", "wouldn't feel", "like falling"],
        "title": "Falling In Wouldn't Feel Like Falling",
    },
    {
        "id": "p03",
        "slug": "time-stops-for-them",
        "start": 553.083,
        "duration": 26.0,
        "role": "Scale",
        "hook": "time stops",
        "phrases": ["time stops", "at the edge", "for them"],
        "title": "Time Stops at the Edge — For Them",
    },
    {
        "id": "p04",
        "slug": "would-you-look-back",
        "start": 792.083,
        "duration": 24.0,
        "role": "Orbit",
        "hook": "look back?",
        "phrases": ["would you", "look back?"],
        "title": "Would You Look Back?",
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_beats(item: dict) -> list[dict]:
    sync = SYNC_DIR / f"blackhole_punch-{item['id']}_{item['slug']}_beats.json"
    if sync.exists():
        beats = (json.loads(sync.read_text()).get("beats")) or []
        if beats:
            return beats
    return auto_beats_from_phrases(
        item["phrases"],
        duration=item["duration"],
        hook_end=6.0,
        punch_first_hook=item.get("hook") or True,
    )


def render(item: dict, temp: Path, master: Path) -> Path:
    beats = resolve_beats(item)
    beat_paths: list[Path] = []
    for i, beat in enumerate(beats):
        p = temp / f"punch-{item['id']}-beat-{i:02d}.png"
        render_beat_png(p, beat["lines"])
        beat_paths.append(p)
    cta = temp / f"punch-{item['id']}-cta.png"
    render_cta_png(cta)

    output = OUT / f"blackhole_punch-{item['id']}_{item['slug']}_v03.mp4"
    cta_start = max(item["duration"] - 3.0, 0)
    overlay = ffmpeg_overlay_filter(beats, cta_start=cta_start, beat_input_start=1)
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(item["start"]),
        "-t",
        str(item["duration"]),
        "-i",
        str(master),
    ]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    cmd += [
        "-filter_complex",
        filtergraph,
        "-map",
        "[v]",
        "-map",
        "0:a:0",
        "-c:v",
        "h264_videotoolbox",
        "-b:v",
        "12M",
        "-maxrate",
        "16M",
        "-r",
        "30",
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-ar",
        "48000",
        "-t",
        str(item["duration"]),
        "-movflags",
        "+faststart",
        str(output),
    ]
    run(cmd)
    return output


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    master = MASTER
    if not master.exists():
        alt = ROOT / "09_Final-Export/blackhole_v05_NORMAL_SPEED_UPLOAD_READY_MASTER.mp4"
        if alt.exists():
            master = alt
        else:
            raise SystemExit(f"Missing BH master: {MASTER}")
    OUT.mkdir(parents=True, exist_ok=True)
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    report: dict = {
        "style": "punch-first-22-28s-v03",
        "source": str(master),
        "long_url": LONG_URL,
        "parent_long_id": LONG_ID,
        "rule": "22–28s · punch-first open · curiosity-gap end · no upload in this script",
        "shorts": [],
    }
    with tempfile.TemporaryDirectory(prefix="bh-punch-v03-") as temp_name:
        temp = Path(temp_name)
        for item in SHORTS:
            if only and item["slug"] not in only and item["id"] not in only:
                continue
            assert 22.0 <= item["duration"] <= 28.0, item
            print(f"Rendering punch {item['id']} {item['slug']}…", flush=True)
            output = render(item, temp, master)
            meta = {**item, "output": str(output), "probe": probe(output)}
            report["shorts"].append(meta)
            dur = float(meta["probe"]["format"]["duration"])
            print(f"  → {output.name} ({dur:.1f}s)", flush=True)
            if not (21.5 <= dur <= 28.5):
                raise SystemExit(f"Duration out of punch window: {dur}")
    report_path = OUT / "blackhole_punch-shorts_v03_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()
