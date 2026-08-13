#!/usr/bin/env python3
"""Assemble Europa Part 01 rough from available Omni plates + VO."""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
VO = EP / "02_Voiceover/parts/europa_part-01_vo_v01.mp3"
CLIPS = EP / "04_Generated-Clips/01_Raw/part-01"
OUT_DIR = EP / "07_Edit-Project/parts"
WORK = OUT_DIR / "_work_part01"
MASTER = OUT_DIR / "europa_part-01_rough_v01.mp4"

# Use whatever unique Omni plates exist (journey order)
PLATES = [
    ("01", "jupiter-to-europa"),
    ("02", "cracked-ice-scars"),
    ("03", "into-the-crack"),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def make_bed(src: Path, bed: Path, need: float) -> None:
    src_dur = probe(src)
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p"
    )
    if src_dur + 0.05 >= need:
        run(
            [
                "ffmpeg", "-y", "-i", str(src), "-t", f"{need:.3f}",
                "-vf", vf,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
                str(bed),
            ]
        )
    else:
        freeze = need - src_dur
        run(
            [
                "ffmpeg", "-y", "-i", str(src),
                "-filter_complex",
                f"[0:v]{vf},tpad=stop_mode=clone:stop_duration={freeze:.3f}[v];"
                f"[0:a]apad=whole_dur={need:.3f}[a]",
                "-map", "[v]", "-map", "[a]", "-t", f"{need:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
                str(bed),
            ]
        )


def main() -> None:
    vo_dur = probe(VO)
    available = []
    for pid, slug in PLATES:
        src = CLIPS / f"omni_p01_{pid}_{slug}_v01.mp4"
        if src.exists() and src.stat().st_size > 500_000:
            available.append((pid, slug, src))
    if not available:
        raise SystemExit("no Omni plates")
    WORK.mkdir(parents=True, exist_ok=True)
    # Equal VO windows for available plates (journey order)
    slice_len = vo_dur / len(available)
    beds = []
    for i, (pid, slug, src) in enumerate(available):
        need = slice_len if i < len(available) - 1 else (vo_dur - slice_len * i)
        bed = WORK / f"bed_{pid}.mp4"
        make_bed(src, bed, need)
        beds.append(bed)
        print(f"bed {pid} need={need:.2f}s src={probe(src):.2f}s ({slug})", flush=True)
    concat = WORK / "picture.concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in beds))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(picture)])
    run(
        [
            "ffmpeg", "-y",
            "-i", str(picture), "-i", str(VO),
            "-filter_complex",
            "[0:a]volume=0.22[sfx];[1:a]volume=1.0[vo];"
            "[sfx][vo]amix=inputs=2:duration=longest:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]",
            "-t", f"{vo_dur:.3f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-movflags", "+faststart",
            str(MASTER),
        ]
    )
    print(f"MASTER → {MASTER} ({probe(MASTER):.2f}s)", flush=True)


if __name__ == "__main__":
    main()
