#!/tmp/ytvenv/bin/python3
"""Europa punch 02 — Europa's Hidden Ocean Is Bigger Than Earth's (Fri 4 Sep 11:30 UK).

Picture: Europa ice + Jupiter (no Orbit in the open) from t≈28s — not t=48 (Orbit).
VO: 'hidden ocean, deep, dark, and big enough to matter' (~2:55), after punch-01's 149s window.
Related: NbW5G1BpPY0. Zero /go/.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "06_Final-Exports"
COVER_DIR = Path(__file__).resolve().parent / "08_Covers"
DURATION = 26.0
VO_START = 175.0  # after punch-01 149–175; hidden-ocean scale beat
PIC_START = 28.0  # ice + Jupiter, no Orbit (t=48 is Orbit — reject)
PIC_MAIN = 22.0
LOOP = 4.0
LONG_ID = "NbW5G1BpPY0"

MASTER_CANDIDATES = [
    ROOT / "09_Final-Export/europa_v02_STUDIO_OWNER.mp4",
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

sys.path.insert(0, str(Path("/Users/benjaminoats/YouTube/orbit-with-ben/04_Audio/tools")))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

BEATS = [
    {"start": 0.0, "end": 2.4, "lines": [("not a puddle", "yellow"), ("under frost", "white")]},
    {"start": 2.4, "end": 5.4, "lines": [("a hidden ocean", "yellow"), ("under that ice", "white")]},
    {"start": 5.4, "end": 8.6, "lines": [("big enough", "white"), ("to matter", "yellow")]},
    {
        "start": 9.0,
        "end": 13.8,
        "lines": [("could life exist", "white"), ("under the ice of europa?", "yellow")],
    },
    {"start": 14.0, "end": 17.6, "lines": [("deep, dark", "white"), ("and still liquid", "yellow")]},
    {"start": 17.6, "end": 21.6, "lines": [("if life needs water", "white"), ("it has a home", "yellow")]},
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_master() -> Path:
    for p in MASTER_CANDIDATES:
        if p.exists() and p.stat().st_size > 5_000_000:
            return p
    raise SystemExit("Missing Europa master europa_v02_STUDIO_OWNER.mp4")


def assemble_picture(master: Path, temp: Path) -> Path:
    main = temp / "pic_main.mp4"
    loop = temp / "pic_loop.mp4"
    concat_list = temp / "concat.txt"
    joined = temp / "pic_26s.mp4"
    for dest, dur in ((main, PIC_MAIN), (loop, LOOP)):
        run(
            [
                "ffmpeg", "-y", "-ss", str(PIC_START), "-t", str(dur),
                "-i", str(master), "-an", "-c:v", "libx264", "-preset", "fast",
                "-crf", "16", "-pix_fmt", "yuv420p", str(dest),
            ]
        )
    concat_list.write_text(f"file '{main}'\nfile '{loop}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(joined)])
    return joined


def extract_vo(master: Path, temp: Path) -> Path:
    audio = temp / "vo.m4a"
    run(
        [
            "ffmpeg", "-y", "-ss", str(VO_START), "-t", str(DURATION),
            "-i", str(master), "-vn", "-c:a", "aac", "-b:a", "256k",
            "-ar", "48000", "-ac", "2", str(audio),
        ]
    )
    return audio


def write_cover(master: Path) -> Path:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    out = COVER_DIR / "europa_punch-02_cover.jpg"
    run(
        [
            "ffmpeg", "-y", "-ss", str(PIC_START), "-i", str(master), "-frames:v", "1",
            "-vf", "crop=405:720:(1280-405)/2:0,scale=1080:1920",
            "-q:v", "3", str(out),
        ]
    )
    return out


def render(temp: Path) -> Path:
    master = resolve_master()
    picture = assemble_picture(master, temp)
    audio = extract_vo(master, temp)
    write_cover(master)

    beat_paths: list[Path] = []
    for i, beat in enumerate(BEATS):
        p = temp / f"beat-{i:02d}.png"
        size = 64 if 9.0 <= beat["start"] < 14.0 else 92
        y = 560 if size == 64 else 780
        render_beat_png(p, beat["lines"], pointsize=size, y_center=y)
        beat_paths.append(p)
    cta = temp / "cta.png"
    render_cta_png(cta, y=1520)

    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "europa_punch-02_bigger-than-earth_v01.mp4"
    overlay = ffmpeg_overlay_filter(BEATS, cta_start=22.0, beat_input_start=2)
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay
    cmd = ["ffmpeg", "-y", "-i", str(picture), "-i", str(audio)]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    cmd += [
        "-filter_complex", filtergraph,
        "-map", "[v]", "-map", "1:a:0",
        *shorts_encode_args(),
        "-t", str(DURATION),
        str(output),
    ]
    run(cmd)
    return output


def probe(path: Path) -> dict:
    raw = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size:stream=width,height,codec_type",
            "-of", "json", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return json.loads(raw.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="eu_punch02_") as td:
        out = render(Path(td))
    info = probe(out)
    dur = float(info["format"]["duration"])
    if not (22.0 <= dur <= 27.5):
        raise SystemExit(f"Duration {dur:.2f}s outside 22–27s gate: {out}")
    streams = {s.get("codec_type"): s for s in info.get("streams", [])}
    v = streams.get("video") or {}
    if (v.get("width"), v.get("height")) != (1080, 1920):
        raise SystemExit(f"Not 1080x1920: {v}")
    print(json.dumps({"out": str(out), "probe": info}, indent=2))


if __name__ == "__main__":
    main()
