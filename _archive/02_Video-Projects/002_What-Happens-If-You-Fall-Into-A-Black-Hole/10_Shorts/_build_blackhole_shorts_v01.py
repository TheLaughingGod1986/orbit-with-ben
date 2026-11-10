#!/usr/bin/env python3
"""Create six vertical Shorts from the Video 002 upload master."""

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
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

_TOOLS = Path(__file__).resolve().parents[3] / "04_Audio" / "tools"
sys.path.insert(0, str(_TOOLS))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

# Timestamps from blackhole_v03/v04 timeline scene starts
SHORTS = [
    {
        "id": "01",
        "slug": "event-horizon",
        "start": 762.208,  # scene 09 crossing
        "duration": 42.0,
        "headline": "CROSS THIS LINE\\nAND YOU NEVER\\nCOME BACK",
        "role": "Hook",
    },
    {
        "id": "02",
        "slug": "spaghettification",
        "start": 660.208,  # scene 08
        "duration": 40.0,
        "headline": "FALLING IN\\nWOULDN'T FEEL\\nLIKE FALLING",
        "role": "Fact",
    },
    {
        "id": "03",
        "slug": "time-dilation",
        "start": 553.083,  # scene 07
        "duration": 42.0,
        "headline": "TIME STOPS\\nAT THE EDGE\\n— FOR THEM",
        "role": "Scale",
    },
    {
        "id": "04",
        "slug": "look-back",
        "start": 792.083,  # scene 09B/C area — failed turnback energy
        "duration": 40.0,
        "headline": "WOULD YOU\\nLOOK BACK?",
        "role": "Orbit",
    },
    {
        "id": "05",
        "slug": "photon-sphere",
        "start": 382.417,  # scene 06 approach / lensing
        "duration": 42.0,
        "headline": "WHAT YOUR\\nEYES WOULD\\nSEE",
        "role": "Visual",
    },
    {
        "id": "06",
        "slug": "point-of-no-return",
        "start": 275.167,  # scene 05 event horizon explained
        "duration": 43.0,
        "headline": "THE POINT OF\\nNO RETURN\\nEXPLAINED",
        "role": "Deeper",
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
            "26",
            "-annotate",
            "+0+70",
            "WHAT HAPPENS IF YOU FALL INTO A BLACK HOLE?",
            str(persistent),
        ]
    )
    run(
        common
        + [
            "-gravity",
            "north",
            "-pointsize",
            "72",
            "-interline-spacing",
            "2",
            "-annotate",
            "+0+160",
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
            "40",
            "-annotate",
            "+0+205",
            "WATCH THE FULL STORY  →",
            str(cta),
        ]
    )
    return persistent, hook, cta


def render(item: dict, temp: Path) -> Path:
    persistent, hook, cta = make_overlay_images(temp, item)
    output = OUT / f"blackhole_short-{item['id']}_{item['slug']}_v01.mp4"
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
    report: dict = {"source": str(MASTER), "shorts": []}
    with tempfile.TemporaryDirectory(prefix="bh-shorts-") as temp_name:
        temp = Path(temp_name)
        for item in SHORTS:
            print(f"Rendering S{item['id']} {item['slug']}…", flush=True)
            output = render(item, temp)
            report["shorts"].append({**item, "output": str(output), "probe": probe(output)})
            print(f"  → {output.name}", flush=True)
    report_path = OUT / "blackhole_launch-shorts_v01_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()
