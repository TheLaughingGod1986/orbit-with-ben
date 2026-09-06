#!/usr/bin/env python3
"""Mint 3 mystery Neutron punches (15–17 Sep) cut from the long.

Intent: open a curiosity gap so viewers tap Related → Yk1tLh23rko.
Picture + VO from the broadcast long. Yellow/white kinetic captions + end CTA.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/TikTok/auto"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from onscreen_captions import (  # noqa: E402
    auto_beats_from_phrases,
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

LONG = Path("/tmp/orbit_neutron_mystery/neutron_long_editor.mp4")
OUT = ROOT / "10_Shorts/06_Final-Exports"
REPORT = ROOT / "10_Shorts/MYSTERY_PUNCHES_15_17_SEP.json"
FILM_TITLE = "What Happens to Your Body Near a Neutron Star?"
LONG_ID = "Yk1tLh23rko"
LONG_URL = f"https://www.youtube.com/watch?v={LONG_ID}"

PUNCHES = [
    {
        "id": "06",
        "slug": "light-climbs-out-exhausted",
        "start": 228.0,
        "duration": 25.0,
        "title": "Why Does Light Leave Exhausted?",
        "phrases": [
            "light climbs out",
            "exhausted",
            "gravity steals\nits energy",
            "what else\nis it hiding?",
        ],
        "schedule_uk": "2026-09-15T11:30:00+01:00",
    },
    {
        "id": "07",
        "slug": "probe-closer-than-you",
        "start": 412.0,
        "duration": 25.0,
        "title": "Could a Probe Get Closer Than You?",
        "phrases": [
            "you wouldn't last",
            "could a probe?",
            "built for\nmilliseconds",
            "the answer\nis worse",
        ],
        "schedule_uk": "2026-09-16T11:30:00+01:00",
    },
    {
        "id": "08",
        "slug": "one-second-after-contact",
        "start": 468.0,
        "duration": 26.0,
        "title": "What Happens One Second After Contact?",
        "phrases": [
            "one second\nafter contact",
            "not a handshake",
            "you stop being\nuseful",
            "watch the\nfull film →",
        ],
        "schedule_uk": "2026-09-17T11:30:00+01:00",
    },
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def description_for(title: str) -> str:
    return (
        f"{title}\n\n"
        f"Watch the full film — {FILM_TITLE}\n"
        f"{LONG_URL}\n\n"
        "#NeutronStar #Astronomy #Shorts #Astrophysics #Gravity "
        "#SpaceDocumentary #Physics #OrbitWithBen"
    )


def render(item: dict, temp: Path) -> Path:
    beats = auto_beats_from_phrases(
        item["phrases"],
        duration=item["duration"],
        hook_end=9.0,
        punch_first_hook=True,
    )
    beats.append(
        {
            "start": 10.5,
            "end": 15.0,
            "lines": [
                ("full film", "white"),
                (FILM_TITLE.lower(), "yellow"),
            ],
        }
    )
    beat_paths: list[Path] = []
    for i, beat in enumerate(beats):
        p = temp / f"s{item['id']}-beat-{i:02d}.png"
        kwargs = {}
        if i == len(beats) - 1:
            kwargs = {"pointsize": 52, "y_center": 700}
        render_beat_png(p, beat["lines"], **kwargs)
        beat_paths.append(p)

    cta = temp / f"s{item['id']}-cta.png"
    render_cta_png(cta, text="watch the full film →")

    output = OUT / f"neutron_mystery-{item['id']}_{item['slug']}_v01.mp4"
    OUT.mkdir(parents=True, exist_ok=True)

    cta_start = max(item["duration"] - 4.0, 0.0)
    overlay = ffmpeg_overlay_filter(
        beats, cta_start=cta_start, beat_input_start=1
    )
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(item["start"]),
        "-t",
        str(item["duration"]),
        "-i",
        str(LONG),
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
    raw = subprocess.check_output(
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
        text=True,
    )
    return json.loads(raw)


def main() -> None:
    if not LONG.exists():
        raise SystemExit(f"Missing long cut: {LONG}")
    report: dict = {
        "related": LONG_ID,
        "long_url": LONG_URL,
        "source": str(LONG),
        "intent": "mystery captions → Related pill → Neutron long",
        "shorts": [],
    }
    with tempfile.TemporaryDirectory(prefix="neutron-mystery-") as tmp:
        temp = Path(tmp)
        for item in PUNCHES:
            print(f"Rendering {item['id']} {item['slug']}…", flush=True)
            out = render(item, temp)
            meta = probe(out)
            dur = float(meta["format"]["duration"])
            report["shorts"].append(
                {
                    **item,
                    "file": str(out),
                    "duration_s": round(dur, 2),
                    "bytes": int(meta["format"]["size"]),
                    "description": description_for(item["title"]),
                    "related": LONG_ID,
                }
            )
            print(f"  → {out.name} {dur:.2f}s", flush=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print("REPORT", REPORT)


if __name__ == "__main__":
    main()
