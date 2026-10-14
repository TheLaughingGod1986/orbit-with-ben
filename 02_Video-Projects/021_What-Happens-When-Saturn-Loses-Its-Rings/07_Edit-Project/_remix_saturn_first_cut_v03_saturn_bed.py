#!/usr/bin/env python3
"""Swap NEW Saturn score bed into first cut v03 (picture unchanged).

Keeps amix normalize=0 + loudnorm I=-14 from the v03 polish.
Audio / media stay out of git — delivers to iCloud only.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "saturn_film" / "work_first_cut_v03"
OUT_LOCAL = HERE / "saturn_film" / "saturn_first_cut_v03.mp4"
BED = HERE.parent / "05_Music" / "saturn-rings_score_bed_v01.mp3"
VO = WORK / "vo_timeline.wav"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR = UAT / "saturn_first_cut_v03"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd[:12]), flush=True)
    subprocess.run(cmd, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def chunk_write(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as f, dest.open("wb") as out:
        while True:
            b = f.read(512 * 1024)
            if not b:
                break
            out.write(b)


def measure_lufs(path: Path) -> dict:
    p = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", "ebur128=framelog=verbose", "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    out: dict = {}
    for line in p.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            try:
                out["integrated_lufs"] = float(line.split("I:")[1].split("LUFS")[0].strip())
            except ValueError:
                pass
        if "LRA:" in line and "LU" in line:
            try:
                out["lra"] = float(line.split("LRA:")[1].split("LU")[0].strip())
            except ValueError:
                pass
    return out


def main() -> None:
    assert OUT_LOCAL.exists(), OUT_LOCAL
    assert BED.exists(), BED
    assert VO.exists(), VO

    # Probe picture duration
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(OUT_LOCAL)],
        text=True,
    ).strip())
    print(f"picture={dur:.3f}s bed={BED.name}", flush=True)

    music_raw = WORK / "music_raw_saturn_v01.m4a"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", "-1", "-i", str(BED),
        "-t", f"{dur:.3f}", "-c:a", "aac", "-b:a", "192k", str(music_raw),
    ])

    mixed = WORK / "mix_saturn_bed_v01.m4a"
    fade_start = max(0.0, dur - 10.0)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO), "-i", str(music_raw),
        "-filter_complex",
        f"[1:a]volume=0.12,afade=t=out:st={fade_start:.3f}:d=10[m];"
        f"[0:a][m]amix=inputs=2:duration=first:normalize=0,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", "192k", str(mixed),
    ])

    # Picture from existing cut, audio from new mix
    remixed = WORK / "saturn_first_cut_v03_saturn_bed.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(OUT_LOCAL), "-i", str(mixed),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(remixed),
    ])

    # Replace local cut + deliver iCloud
    shutil.copy2(remixed, OUT_LOCAL)
    digest = sha256(OUT_LOCAL)
    lufs = measure_lufs(OUT_LOCAL)
    print(f"LUFS {lufs} sha256={digest}", flush=True)

    UAT_DIR.mkdir(parents=True, exist_ok=True)
    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v03.mp4")
    arrival = {
        "cut": "v03",
        "music_swap": "saturn-rings_score_bed_v01.mp3",
        "music_sha256": sha256(BED),
        "music_path_local": str(BED),
        "music_path_icloud": str(
            UAT / "saturn_score_bed_v01" / "saturn-rings_score_bed_v01.mp3"
        ),
        "duration": dur,
        "sha256": digest,
        "loudness": lufs,
        "framing": "unchanged from v03 polish (cover/blur_bg, 4x zoompan)",
        "note": "Moon Leaving temp bed replaced. Audio/media iCloud only; no force-add.",
    }
    (WORK / "ARRIVAL_saturn_bed.json").write_text(json.dumps(arrival, indent=2) + "\n")
    (UAT_DIR / "ARRIVAL.json").write_text(json.dumps(arrival, indent=2) + "\n")
    art = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts")
    (art / "saturn_first_cut_v03_ARRIVAL_saturn_bed.json").write_text(
        json.dumps(arrival, indent=2) + "\n"
    )
    print("DONE", json.dumps(arrival, indent=2))


if __name__ == "__main__":
    main()
