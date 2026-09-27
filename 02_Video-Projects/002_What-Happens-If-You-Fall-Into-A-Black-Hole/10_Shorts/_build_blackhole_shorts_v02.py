#!/usr/bin/env python3
"""Black-hole Shorts v02 — finalverdict-style yellow/white kinetic captions."""

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
MASTER = ROOT / "09_Final-Export/blackhole_v04_UPLOAD_READY_MASTER.mp4"
OUT = ROOT / "10_Shorts/06_Final-Exports"
LONG_URL = "https://youtu.be/n7CbJrOCnU0"

CAPTION_LIB = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/tools"
)
sys.path.insert(0, str(CAPTION_LIB))
from onscreen_captions import (  # noqa: E402
    auto_beats_from_phrases,
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)

_TOOLS = Path(__file__).resolve().parents[3] / "04_Audio" / "tools"
sys.path.insert(0, str(_TOOLS))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

SYNC_DIR = ROOT / "10_Shorts/07_Caption-Sync"

SHORTS = [
    {
        "id": "01",
        "slug": "event-horizon",
        "start": 762.208,
        "duration": 42.0,
        "role": "Hook",
        "hook": "cross this line",
        "phrases": ["cross this line", "and you never", "come back"],
    },
    {
        "id": "02",
        "slug": "spaghettification",
        "start": 660.208,
        "duration": 40.0,
        "role": "Fact",
        "hook": "wouldn't feel",
        "phrases": ["falling in", "wouldn't feel", "like falling"],
    },
    {
        "id": "03",
        "slug": "time-dilation",
        "start": 553.083,
        "duration": 42.0,
        "role": "Scale",
        "hook": "time stops",
        "phrases": ["time stops", "at the edge", "for them"],
    },
    {
        "id": "04",
        "slug": "look-back",
        "start": 792.083,
        "duration": 40.0,
        "role": "Orbit",
        "hook": "look back?",
        "phrases": ["would you", "look back?"],
    },
    {
        "id": "05",
        "slug": "photon-sphere",
        "start": 382.417,
        "duration": 42.0,
        "role": "Visual",
        "hook": "eyes would",
        "phrases": ["what your", "eyes would", "see"],
    },
    {
        "id": "06",
        "slug": "point-of-no-return",
        "start": 275.167,
        "duration": 43.0,
        "role": "Deeper",
        "hook": "no return",
        "phrases": ["the point of", "no return", "explained"],
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_master() -> Path:
    if MASTER.exists():
        return MASTER
    raise SystemExit(f"Missing blackhole master: {MASTER}")


def resolve_beats(item: dict) -> list[dict]:
    sync = SYNC_DIR / f"blackhole_short-{item['id']}_{item['slug']}_beats.json"
    if sync.exists():
        data = json.loads(sync.read_text())
        beats = data.get("beats") or []
        if beats:
            return beats
    return auto_beats_from_phrases(
        item["phrases"],
        duration=item["duration"],
        hook_end=8.0,
        punch_first_hook=item.get("hook") or True,
    )


def render(item: dict, temp: Path) -> Path:
    beats = resolve_beats(item)
    beat_paths: list[Path] = []
    for i, beat in enumerate(beats):
        p = temp / f"short-{item['id']}-beat-{i:02d}.png"
        render_beat_png(p, beat["lines"])
        beat_paths.append(p)
    cta = temp / f"short-{item['id']}-cta.png"
    render_cta_png(cta)

    output = OUT / f"blackhole_short-{item['id']}_{item['slug']}_v02.mp4"
    cta_start = max(item["duration"] - 4.5, 0)
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
        str(MASTER),
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
        *shorts_encode_args(),
        "-t",
        str(item["duration"]),
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
            "format=duration,size:stream=index,codec_type,codec_name,width,height",
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
    if not MASTER.exists():
        raise SystemExit(f"Missing master: {MASTER}")
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    report: dict = {
        "style": "finalverdict-yellow-white-v02",
        "source": str(MASTER),
        "long_url": LONG_URL,
        "shorts": [],
    }
    with tempfile.TemporaryDirectory(prefix="bh-shorts-v02-") as temp_name:
        temp = Path(temp_name)
        for item in SHORTS:
            if only and item["slug"] not in only and item["id"] not in only:
                continue
            print(f"Rendering S{item['id']} {item['slug']} (v02)…", flush=True)
            output = render(item, temp)
            report["shorts"].append(
                {**item, "output": str(output), "probe": probe(output)}
            )
            print(f"  → {output.name}", flush=True)
    report_path = OUT / "blackhole_launch-shorts_v02_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()
