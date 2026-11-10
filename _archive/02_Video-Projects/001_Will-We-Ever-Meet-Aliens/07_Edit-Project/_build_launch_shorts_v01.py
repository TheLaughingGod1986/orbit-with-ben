#!/usr/bin/env python3
"""Create four vertical launch Shorts from the approved v17 master."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
MASTER = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v17_FINAL_UPLOAD_READY_MASTER.mp4"
OUT = ROOT / "10_Shorts/06_Final-Exports"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

_TOOLS = Path(__file__).resolve().parents[3] / "04_Audio" / "tools"
sys.path.insert(0, str(_TOOLS))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

SHORTS = [
    {
        "id": "01",
        "slug": "distance",
        "start": 21.650,
        "duration": 40.000,
        "headline": "SPACE IS RUDE\\nABOUT DISTANCE",
        "accent": "&H003D8BFF",
        "role": "Discovery",
    },
    {
        "id": "02",
        "slug": "fermi-paradox",
        "start": 157.791,
        "duration": 43.500,
        "headline": "WHERE IS\\nEVERYBODY?",
        "accent": "&H003D8BFF",
        "role": "Highlight",
    },
    {
        "id": "03",
        "slug": "zoo-hypothesis",
        "start": 534.251,
        "duration": 43.000,
        "headline": "WHAT IF THEY'RE\\nWATCHING US?",
        "accent": "&H003D8BFF",
        "role": "Theory",
    },
    {
        "id": "04",
        "slug": "hidden-clues",
        "start": 1041.078,
        "duration": 48.000,
        "headline": "WHAT IF THE CLUE\\nIS ALREADY HERE?",
        "accent": "&H003D8BFF",
        "role": "Cliffhanger",
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def make_overlay_images(temp: Path, item: dict) -> tuple[Path, Path, Path]:
    persistent = temp / f"short-{item['id']}-persistent.png"
    hook = temp / f"short-{item['id']}-hook.png"
    cta = temp / f"short-{item['id']}-cta.png"
    common = [
        "magick",
        "-size",
        "1080x1920",
        "xc:none",
        "-font",
        FONT,
        "-fill",
        "white",
        "-stroke",
        "#10182c",
        "-strokewidth",
        "3",
    ]
    run(
        common
        + [
            "-gravity",
            "north",
            "-pointsize",
            "33",
            "-annotate",
            "+0+72",
            f"ORBIT  •  {item['role'].upper()}",
            "-gravity",
            "south",
            "-pointsize",
            "29",
            "-annotate",
            "+0+70",
            "WILL WE EVER MEET ALIENS?",
            str(persistent),
        ]
    )
    run(
        common
        + [
            "-gravity",
            "north",
            "-pointsize",
            "76",
            "-interline-spacing",
            "4",
            "-annotate",
            "+0+170",
            item["headline"],
            str(hook),
        ]
    )
    run(
        [
            "magick",
            "-size",
            "1080x1920",
            "xc:none",
            "-fill",
            "#07101FCC",
            "-stroke",
            "#FFFFFF33",
            "-strokewidth",
            "2",
            "-draw",
            "roundrectangle 70,1600 1010,1785 34,34",
            "-font",
            FONT,
            "-fill",
            "white",
            "-stroke",
            "#10182c",
            "-strokewidth",
            "3",
            "-gravity",
            "south",
            "-pointsize",
            "44",
            "-annotate",
            "+0+205",
            "WATCH THE FULL STORY  →",
            str(cta),
        ]
    )
    return persistent, hook, cta


def render(item: dict, temp: Path) -> Path:
    persistent, hook, cta = make_overlay_images(temp, item)
    output = OUT / f"aliens_short-{item['id']}_{item['slug']}_v01.mp4"
    start = str(item["start"])
    duration = str(item["duration"])
    filtergraph = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=20:1,eq=brightness=-0.28:saturation=0.88[bgv];"
        "[fg]scale=1020:-2,setsar=1[fgv];"
        "[bgv][fgv]overlay=(W-w)/2:(H-h)/2:format=auto,"
        "drawbox=x=28:y=(h-574)/2:w=1024:h=574:color=white@0.15:t=2[base];"
        "[base][1:v]overlay=0:0:format=auto[persistent];"
        "[persistent][2:v]overlay=0:0:enable='between(t,0,5.8)':format=auto[hook];"
        f"[hook][3:v]overlay=0:0:enable='gte(t,{max(item['duration'] - 5.5, 0):.3f})':"
        "format=auto,format=yuv420p[v]"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            start,
            "-t",
            duration,
            "-i",
            str(MASTER),
            "-loop",
            "1",
            "-framerate",
            "30",
            "-i",
            str(persistent),
            "-loop",
            "1",
            "-framerate",
            "30",
            "-i",
            str(hook),
            "-loop",
            "1",
            "-framerate",
            "30",
            "-i",
            str(cta),
            "-filter_complex",
            filtergraph,
            "-map",
            "[v]",
            "-map",
            "0:a:0",
            *shorts_encode_args(),
            "-t",
            duration,
            str(output),
        ]
    )
    return output


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
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
        raise SystemExit(f"Missing approved master: {MASTER}")
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"source": str(MASTER), "shorts": []}
    with tempfile.TemporaryDirectory(prefix="orbit-shorts-") as temp_name:
        temp = Path(temp_name)
        for item in SHORTS:
            output = render(item, temp)
            report["shorts"].append(
                {
                    **item,
                    "output": str(output),
                    "probe": probe(output),
                }
            )
    report_path = OUT / "aliens_launch-shorts_v01_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
