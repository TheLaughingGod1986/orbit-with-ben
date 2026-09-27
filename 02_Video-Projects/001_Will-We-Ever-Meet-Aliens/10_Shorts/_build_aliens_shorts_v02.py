#!/usr/bin/env python3
"""Aliens launch Shorts v02 — finalverdict-style yellow/white kinetic captions."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
OUT = ROOT / "10_Shorts/06_Final-Exports"
LONG_URL = "https://youtu.be/Mo93x0fxB1Q"


def resolve_master() -> Path:
    preferred = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v17_FINAL_UPLOAD_READY_MASTER.mp4"
    if preferred.exists():
        return preferred
    candidates = sorted(
        ROOT.glob("09_Final-Export/aliens_BOLD_EXPLAINER_v*_UPLOAD_READY_MASTER.mp4")
    )
    if not candidates:
        raise SystemExit(f"Missing aliens upload master under {ROOT / '09_Final-Export'}")
    return candidates[-1]

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
        "slug": "distance",
        "start": 21.650,
        "duration": 40.000,
        "role": "Discovery",
        "hook": "space is rude",
        "phrases": ["space is rude", "about distance", "even a hello\ntakes forever"],
    },
    {
        "id": "02",
        "slug": "fermi-paradox",
        "start": 157.791,
        "duration": 43.500,
        "role": "Highlight",
        "hook": "everybody?",
        "phrases": ["where is", "everybody?", "countless stars\nno clear hello"],
    },
    {
        "id": "03",
        "slug": "zoo-hypothesis",
        "start": 534.251,
        "duration": 43.000,
        "role": "Theory",
        "hook": "watching?",
        "phrases": ["what if", "they're watching?", "the zoo hypothesis"],
    },
    {
        "id": "04",
        "slug": "hidden-clues",
        "start": 1041.078,
        "duration": 48.000,
        "role": "Cliffhanger",
        "hook": "already here?",
        "phrases": ["what if the clue", "is already here?", "in an archive"],
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_beats(item: dict) -> list[dict]:
    sync = SYNC_DIR / f"aliens_short-{item['id']}_{item['slug']}_beats.json"
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


def render(item: dict, temp: Path, master: Path) -> Path:
    beats = resolve_beats(item)
    beat_paths: list[Path] = []
    for i, beat in enumerate(beats):
        p = temp / f"short-{item['id']}-beat-{i:02d}.png"
        render_beat_png(p, beat["lines"])
        beat_paths.append(p)
    cta = temp / f"short-{item['id']}-cta.png"
    render_cta_png(cta)

    output = OUT / f"aliens_short-{item['id']}_{item['slug']}_v02.mp4"
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
    master = resolve_master()
    print(f"Master: {master.name}", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    report: dict = {
        "style": "finalverdict-yellow-white-v02",
        "source": str(master),
        "long_url": LONG_URL,
        "shorts": [],
    }
    with tempfile.TemporaryDirectory(prefix="aliens-shorts-v02-") as temp_name:
        temp = Path(temp_name)
        for item in SHORTS:
            if only and item["slug"] not in only and item["id"] not in only:
                continue
            print(f"Rendering S{item['id']} {item['slug']} (v02)…", flush=True)
            output = render(item, temp, master)
            report["shorts"].append(
                {**item, "output": str(output), "probe": probe(output)}
            )
            print(f"  → {output.name}", flush=True)
    report_path = OUT / "aliens_launch-shorts_v02_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()
