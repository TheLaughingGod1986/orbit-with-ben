#!/usr/bin/env python3
"""Assemble Europa Part 01 rough v02 — 1× Omni only, no freeze-pad / no stretch."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
VO = EP / "02_Voiceover/parts/europa_part-01_vo_v01.mp3"
PLATES_JSON = EP / "07_Edit-Project/parts/part-01_omni_plates_v02.json"
CLIPS = EP / "04_Generated-Clips/01_Raw/part-01"
OUT_DIR = EP / "07_Edit-Project/parts"
WORK = OUT_DIR / "_work_part01_v02"
MASTER = OUT_DIR / "europa_part-01_rough_v02.mp4"


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
    """Trim to need at 1×. Never freeze / stretch / loop."""
    src_dur = probe(src)
    use = min(need, src_dur)
    if use + 0.05 < need:
        # Caller must not request more motion than exists.
        raise SystemExit(
            f"SHORT CLIP (no freeze allowed): {src.name} is {src_dur:.2f}s, need {need:.2f}s"
        )
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p"
    )
    run(
        [
            "ffmpeg", "-y", "-i", str(src), "-t", f"{use:.3f}",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            str(bed),
        ]
    )


def main() -> None:
    plan = json.loads(PLATES_JSON.read_text())
    vo_dur = probe(VO)
    available = []
    for plate in plan["plates"]:
        src = CLIPS / f"omni_p01_{plate['id']}_{plate['slug']}_v02.mp4"
        if src.exists() and src.stat().st_size > 500_000:
            available.append((plate, src, probe(src)))
        else:
            raise SystemExit(f"missing plate: {src.name}")
    WORK.mkdir(parents=True, exist_ok=True)
    # Use full 1× motion from every plate. Never freeze to stretch to VO.
    # If motion is slightly shorter than VO (<1s), trim master to picture length.
    motion_total = sum(d for _, _, d in available)
    if motion_total + 0.05 < vo_dur - 1.0:
        raise SystemExit(
            f"Not enough motion ({motion_total:.2f}s) for VO ({vo_dur:.2f}s) — generate more plates"
        )
    beds = []
    for plate, src, src_dur in available:
        bed = WORK / f"bed_{plate['id']}.mp4"
        make_bed(src, bed, src_dur)  # full clip, 1×
        beds.append(bed)
        print(f"bed {plate['id']} use={src_dur:.2f}s ({plate['slug']})", flush=True)
    concat = WORK / "picture.concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in beds))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(picture)])
    pic_dur = probe(picture)
    master_dur = min(pic_dur, vo_dur)
    if pic_dur + 0.05 < vo_dur:
        print(
            f"WARN: picture {pic_dur:.2f}s < VO {vo_dur:.2f}s — trimming "
            f"{vo_dur - pic_dur:.2f}s of VO (no freeze)",
            flush=True,
        )
    run(
        [
            "ffmpeg", "-y",
            "-i", str(picture), "-i", str(VO),
            "-filter_complex",
            "[0:a]volume=0.22[sfx];[1:a]volume=1.0[vo];"
            "[sfx][vo]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]",
            "-t", f"{master_dur:.3f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-movflags", "+faststart",
            str(MASTER),
        ]
    )
    print(f"MASTER → {MASTER} ({probe(MASTER):.2f}s)", flush=True)


if __name__ == "__main__":
    main()
