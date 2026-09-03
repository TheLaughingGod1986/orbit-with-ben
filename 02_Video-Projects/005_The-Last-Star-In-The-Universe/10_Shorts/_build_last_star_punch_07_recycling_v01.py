#!/tmp/ytvenv/bin/python3
"""Last Star punch 07 — Star Recycling Isn't Perfect (Wed 2 Sep 11:30 UK).

Unique idea vs live cluster:
  DN4L1DkerMM = star *birth* ending
  This Short   = leftover *mass locked* in white dwarfs / husks (why nurseries fail)

Picture recut (mute-test): galaxy dust + lone star in a dust ring.
Do not use 4:20–5:40 of the long (eyeball / fusion-window fail).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "005_The-Last-Star-In-The-Universe"
)
OUT = ROOT / "10_Shorts/06_Final-Exports"
LONG_ID = "REXYxuLOBoI"
LONG_TITLE = "What Happens When the Last Star Dies?"
LONG_URL = f"https://www.youtube.com/watch?v={LONG_ID}"
DURATION = 26.0
VO_START = 89.44  # "However, the recycling is not perfect."
PIC_START = 106.0  # galaxy dust, no Orbit in frame 1
PIC_MAIN = 22.0
LOOP = 4.0

MASTER_CANDIDATES = [
    Path("/tmp/hos_shorts_audit/long_REXYxuLOBoI.mp4"),
    ROOT / "09_Final-Export/last_star_UPLOAD.mp4",
]

CAPTION_LIB = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/TikTok/auto"
)
sys.path.insert(0, str(CAPTION_LIB))
from onscreen_captions import (  # noqa: E402
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)

_TOOLS = Path("/Users/benjaminoats/YouTube/orbit-with-ben/04_Audio/tools")
sys.path.insert(0, str(_TOOLS))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

BEATS = [
    {"start": 0.0, "end": 2.2, "lines": [("recycling isn't", "yellow"), ("perfect", "white")]},
    {"start": 2.2, "end": 5.0, "lines": [("leftover mass", "yellow"), ("gets trapped", "white")]},
    {"start": 5.0, "end": 8.2, "lines": [("white dwarfs", "yellow"), ("neutron husks", "white")]},
    {
        "start": 9.0,
        "end": 13.8,
        "lines": [("what happens when", "white"), ("the last star dies?", "yellow")],
    },
    {"start": 14.0, "end": 17.2, "lines": [("star-ready gas", "yellow"), ("runs low", "white")]},
    {"start": 17.2, "end": 21.6, "lines": [("no refill", "yellow")]},
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_master() -> Path:
    for p in MASTER_CANDIDATES:
        if p.exists() and p.stat().st_size > 1_000_000:
            return p
    raise SystemExit("Missing Last Star long. Expected /tmp/hos_shorts_audit/long_REXYxuLOBoI.mp4")


def assemble_picture(master: Path, temp: Path) -> Path:
    main = temp / "pic_main.mp4"
    loop = temp / "pic_loop.mp4"
    concat_list = temp / "concat.txt"
    joined = temp / "pic_26s.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(PIC_START),
            "-t",
            str(PIC_MAIN),
            "-i",
            str(master),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            str(main),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(PIC_START),
            "-t",
            str(LOOP),
            "-i",
            str(master),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            str(loop),
        ]
    )
    concat_list.write_text(f"file '{main}'\nfile '{loop}'\n")
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(joined),
        ]
    )
    return joined


def extract_vo(master: Path, temp: Path) -> Path:
    audio = temp / "vo.m4a"
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(VO_START),
            "-t",
            str(DURATION),
            "-i",
            str(master),
            "-vn",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(audio),
        ]
    )
    return audio


def render(temp: Path) -> Path:
    master = resolve_master()
    picture = assemble_picture(master, temp)
    audio = extract_vo(master, temp)

    beat_paths: list[Path] = []
    for i, beat in enumerate(BEATS):
        p = temp / f"beat-{i:02d}.png"
        size = 64 if beat["start"] >= 9.0 and beat["start"] < 14.0 else 92
        y = 560 if size == 64 else 780
        render_beat_png(p, beat["lines"], pointsize=size, y_center=y)
        beat_paths.append(p)
    cta = temp / "cta.png"
    render_cta_png(cta, y=1520)

    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "last-star_punch-07_recycling_v01.mp4"
    overlay = ffmpeg_overlay_filter(BEATS, cta_start=22.0, beat_input_start=2)
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay

    cmd = ["ffmpeg", "-y", "-i", str(picture), "-i", str(audio)]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    cmd += [
        "-filter_complex",
        filtergraph,
        "-map",
        "[v]",
        "-map",
        "1:a:0",
        *shorts_encode_args(),
        "-t",
        str(DURATION),
        str(output),
    ]
    run(cmd)
    return output


def probe(path: Path) -> dict:
    raw = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=width,height,codec_type",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(raw.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ls_punch07_") as td:
        out = render(Path(td))
    info = probe(out)
    dur = float(info["format"]["duration"])
    if not (22.0 <= dur <= 27.5):
        raise SystemExit(f"Duration {dur:.2f}s outside 22–27s gate: {out}")
    print(json.dumps({"out": str(out), "probe": info}, indent=2))


if __name__ == "__main__":
    main()
