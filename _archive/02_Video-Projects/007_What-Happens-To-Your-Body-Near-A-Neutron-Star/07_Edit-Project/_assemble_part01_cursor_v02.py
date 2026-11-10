#!/usr/bin/env python3
"""Assemble Neutron Star Part 01 cursor v02: ~63.4s complete-sentence VO, remnant-rise end."""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
RAW = EP / "04_Generated-Clips/01_Raw/part-01"
VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.wav"
if not VO.exists():
    VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.mp3"
OUT_DIR = HERE / "parts"
WORK = HERE / "parts/_work_part01_cursor_v02"
XFADE = 0.40
# SRT cue 22 ends 00:01:03,419 — "a brief, furious goodbye."
MASTER_DUR = 63.420
PLATE_FILES = [
    "omni_p01_01_almost-ordinary-star_cursor_v01.mp4",
    "omni_p01_02_orbit-banks-into-frame_cursor_v01.mp4",
    "omni_p01_03_tide-tears-a-line_cursor_v01.mp4",
    "omni_p01_04_light-bends-into-a-ring_cursor_v01.mp4",
    "omni_p01_05_second-by-second-close_cursor_v01.mp4",
    "omni_p01_06_see-feel-you-ends_cursor_v01.mp4",
    "omni_p01_07_it-began-as-a-giant_cursor_v01.mp4",
    "omni_p01_09_compact-fierce-wrong_cursor_v01.mp4",
    "omni_p01_10_remnant-intensity-rise_cursor_v01.mp4",
]


def probe(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clips = []
    for name in PLATE_FILES:
        src = RAW / name
        if not src.exists() or src.stat().st_size < 200_000:
            raise SystemExit(f"missing plate {src}")
        clips.append(src)

    beds = []
    for i, src in enumerate(clips, 1):
        bed = WORK / f"bed_{i:02d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            str(bed),
        ])
        beds.append(bed)

    n = len(beds)
    durs = [probe(b) for b in beds]
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + durs[i - 1] - XFADE)
    out_dur = offsets[-1] + durs[-1]
    if out_dur + 0.05 < MASTER_DUR:
        raise SystemExit(f"Picture {out_dur:.2f}s shorter than VO cut {MASTER_DUR:.2f}s")

    ins: list[str] = []
    for b in beds:
        ins += ["-i", str(b)]
    filters = []
    vprev, aprev = "0:v", "0:a"
    for i in range(1, n):
        vout, aout = f"v{i}", f"a{i}"
        filters.append(
            f"[{vprev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offsets[i]:.3f}[{vout}]"
        )
        filters.append(f"[{aprev}][{i}:a]acrossfade=d={XFADE}[{aout}]")
        vprev, aprev = vout, aout
    picture = WORK / "picture.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *ins,
        "-filter_complex", ";".join(filters),
        "-map", f"[{vprev}]", "-map", f"[{aprev}]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2",
        "-t", f"{out_dur:.3f}",
        str(picture),
    ])

    rough = OUT_DIR / "neutron_star_part-01_cursor_rough_v02.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(VO),
        "-filter_complex",
        f"[0:v]trim=0:{MASTER_DUR:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{MASTER_DUR:.3f},asetpts=PTS-STARTPTS[vo];"
        f"[0:a]volume=0.20,atrim=0:{MASTER_DUR:.3f},asetpts=PTS-STARTPTS[amb];"
        f"[amb][vo]amix=inputs=2:duration=first:dropout_transition=0.3[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{MASTER_DUR:.3f}",
        str(rough),
    ])

    open15 = OUT_DIR / "neutron_star_part-01_cursor_open15_v02.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(rough), "-t", "15",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(open15),
    ])
    print(f"rough {rough} {probe(rough):.3f}s")
    print(f"open15 {open15} {probe(open15):.3f}s")


if __name__ == "__main__":
    main()
