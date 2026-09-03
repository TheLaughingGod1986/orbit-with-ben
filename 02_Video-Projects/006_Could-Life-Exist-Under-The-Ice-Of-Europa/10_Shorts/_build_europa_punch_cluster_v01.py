#!/tmp/ytvenv/bin/python3
"""Europa punch cluster — 22–27s Shorts, Related NbW5G1BpPY0.

Blocked until a 16:9 master is on disk (Studio owner download or
europa_v02_HAND_OPEN_END_UPLOAD.mp4). Premiere NbW5G1BpPY0 is not yt-dlp-able.

  python3 _build_europa_punch_cluster_v01.py          # all, skip-existing
  python3 _build_europa_punch_cluster_v01.py 01       # Thursday morning promo only
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLUSTER = Path(__file__).resolve().parent / "EUROPA_SHORTS_CLUSTER_v01.json"
OUT = Path(__file__).resolve().parent / "06_Final-Exports"
LONG_ID = "NbW5G1BpPY0"
LONG_TITLE = "Could Life Exist Under The Ice Of Europa?"
DURATION = 26.0

MASTER_CANDIDATES = [
    ROOT / "09_Final-Export/europa_v02_STUDIO_OWNER.mp4",
    ROOT / "09_Final-Export/europa_v02_HAND_OPEN_END_UPLOAD.mp4",
    ROOT / "09_Final-Export/europa_broadcast_v02.mp4",
    ROOT / "09_Final-Export/europa_broadcast_v01.mp4",
    Path("/tmp/hos_shorts_audit/long_NbW5G1BpPY0.mp4"),
]

# VO windows filled after owner download + SRT. Starts are placeholders
# from part-rough durations (~60–80s each). Rebuild from SRT before upload.
WINDOWS = {
    "01": {"start": 8.0, "phrases": ["ocean under", "that ice", "not a frozen rock"]},
    "02": {"start": 48.0, "phrases": ["bigger than", "earth's oceans", "hidden under ice"]},
    "03": {"start": 28.0, "phrases": ["ice scars", "linea", "that's the tell"]},
    "04": {"start": 70.0, "phrases": ["under the ice", "the dive", "a whole ocean"]},
    "05": {"start": 240.0, "phrases": ["how we'd know", "it's alive", "chemistry not monsters"]},
    "06": {"start": 300.0, "phrases": ["plumes", "salt fingerprints", "ocean below"]},
    "07": {"start": 360.0, "phrases": ["clipper", "goes to look", "above the ice"]},
    "08": {"start": 420.0, "phrases": ["closer isn't", "certain", "we still look"]},
}

CAPTION_LIB = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/TikTok/auto"
)
sys.path.insert(0, str(CAPTION_LIB))
from onscreen_captions import (  # noqa: E402
    auto_beats_from_phrases,
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)

sys.path.insert(0, str(Path("/Users/benjaminoats/YouTube/orbit-with-ben/04_Audio/tools")))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def resolve_master() -> Path:
    for p in MASTER_CANDIDATES:
        if p.exists() and p.stat().st_size > 5_000_000:
            return p
    raise SystemExit(
        "Europa 16:9 master missing. Owner-download NbW5G1BpPY0 from Studio:\n"
        "  python3 00_Brand/Channel-Setup/audits/_studio_download_europa_v01.py\n"
        "Then drop the file at:\n"
        f"  {MASTER_CANDIDATES[0]}"
    )


def render_one(item: dict, master: Path, temp: Path) -> Path:
    wid = item["id"]
    win = WINDOWS[wid]
    slug = item["title"].lower().replace(" ", "-").replace("'", "")[:40]
    beats = auto_beats_from_phrases(
        win["phrases"],
        duration=DURATION,
        hook_end=8.0,
        punch_first_hook=win["phrases"][0],
    )
    # Film title ~9–14s
    beats.append(
        {
            "start": 9.0,
            "end": 13.8,
            "lines": [("could life exist", "white"), ("under the ice of europa?", "yellow")],
        }
    )
    beat_paths = []
    for i, beat in enumerate(beats):
        p = temp / f"{wid}-b{i:02d}.png"
        size = 64 if 8.8 <= float(beat["start"]) < 14.0 else 92
        y = 560 if size == 64 else 780
        render_beat_png(p, beat["lines"], pointsize=size, y_center=y)
        beat_paths.append(p)
    cta = temp / f"{wid}-cta.png"
    render_cta_png(cta, y=1520)

    # 22s unique + 4s loop of the open
    main = temp / f"{wid}-main.mp4"
    loop = temp / f"{wid}-loop.mp4"
    joined = temp / f"{wid}-pic.mp4"
    run(
        [
            "ffmpeg", "-y", "-ss", str(win["start"]), "-t", "22",
            "-i", str(master), "-an", "-c:v", "libx264", "-preset", "fast",
            "-crf", "16", "-pix_fmt", "yuv420p", str(main),
        ]
    )
    run(
        [
            "ffmpeg", "-y", "-ss", str(win["start"]), "-t", "4",
            "-i", str(master), "-an", "-c:v", "libx264", "-preset", "fast",
            "-crf", "16", "-pix_fmt", "yuv420p", str(loop),
        ]
    )
    lst = temp / f"{wid}-concat.txt"
    lst.write_text(f"file '{main}'\nfile '{loop}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])

    overlay = ffmpeg_overlay_filter(beats, cta_start=22.0, beat_input_start=1)
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay
    output = OUT / f"europa_punch-{wid}_{slug}_v01.mp4"
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", str(joined)]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    # VO from the same window as picture for first cut; recut after SRT QA
    cmd += [
        "-ss", str(win["start"]), "-t", str(DURATION), "-i", str(master),
        "-filter_complex", filtergraph,
        "-map", "[v]", "-map", f"{2 + len(beat_paths)}:a:0?",
        *shorts_encode_args(),
        "-t", str(DURATION),
        str(output),
    ]
    # Simpler: mux VO from master at same start via separate audio extract
    audio = temp / f"{wid}-vo.m4a"
    run(
        [
            "ffmpeg", "-y", "-ss", str(win["start"]), "-t", str(DURATION),
            "-i", str(master), "-vn", "-c:a", "aac", "-b:a", "256k",
            "-ar", "48000", "-ac", "2", str(audio),
        ]
    )
    cmd = ["ffmpeg", "-y", "-i", str(joined), "-i", str(audio)]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    overlay = ffmpeg_overlay_filter(beats, cta_start=22.0, beat_input_start=2)
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay
    cmd += [
        "-filter_complex", filtergraph,
        "-map", "[v]", "-map", "1:a:0",
        *shorts_encode_args(),
        "-t", str(DURATION),
        str(output),
    ]
    run(cmd)
    return output


def main() -> None:
    cluster = json.loads(CLUSTER.read_text())
    want = sys.argv[1:] if len(sys.argv) > 1 else [s["id"] for s in cluster["shorts"]]
    master = resolve_master()
    built = []
    with tempfile.TemporaryDirectory(prefix="europa_punch_") as td:
        temp = Path(td)
        for item in cluster["shorts"]:
            if item["id"] not in want:
                continue
            built.append(str(render_one(item, master, temp)))
    print(json.dumps({"master": str(master), "built": built}, indent=2))


if __name__ == "__main__":
    main()
