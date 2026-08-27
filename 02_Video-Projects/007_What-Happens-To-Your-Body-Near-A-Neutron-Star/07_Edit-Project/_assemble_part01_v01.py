#!/usr/bin/env python3
"""Assemble Neutron Star Part 01: xfade + acrossfade, no freeze-pad."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
PLATES = json.loads((HERE / "parts/part-01_omni_plates_v01.json").read_text())
RAW = EP / "04_Generated-Clips/01_Raw/part-01"
VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.wav"
if not VO.exists():
    VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.mp3"
OUT_DIR = HERE / "parts"
WORK = HERE / "parts/_work_part01_v01"
QC = EP / "_qc_p01"
XFADE = 0.12


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
    QC.mkdir(parents=True, exist_ok=True)
    clips = []
    for plate in PLATES["plates"]:
        src = RAW / plate["file"]
        if src.exists() and src.stat().st_size > 200_000:
            clips.append(src)
    if len(clips) < 3:
        raise SystemExit(f"Need at least 3 real plates, found {len(clips)}")

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

    # xfade + acrossfade chain
    n = len(beds)
    durs = [probe(b) for b in beds]
    # offset[i] = start of clip i in output
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + durs[i - 1] - XFADE)
    out_dur = offsets[-1] + durs[-1]

    ins = []
    for b in beds:
        ins += ["-i", str(b)]
    filters = []
    vprev = "0:v"
    aprev = "0:a"
    for i in range(1, n):
        vout = f"v{i}"
        aout = f"a{i}"
        filters.append(
            f"[{vprev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offsets[i]:.3f}[{vout}]"
        )
        filters.append(
            f"[{aprev}][{i}:a]acrossfade=d={XFADE}[{aout}]"
        )
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

    vo_dur = probe(VO)
    pic_dur = probe(picture)
    # Picture-first is visual (no Orbit 0-3s). VO starts at 0 over plate 01.
    # Never freeze-pad: picture must cover VO. Trim to min if picture is longer.
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"Picture {pic_dur:.2f}s shorter than VO {vo_dur:.2f}s — generate more plates, do not freeze-pad"
        )
    master_dur = vo_dur
    rough = OUT_DIR / "neutron_star_part-01_rough_v01.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(VO),
        "-filter_complex",
        f"[0:v]trim=0:{master_dur:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS[vo];"
        f"[0:a]volume=0.22,atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS[amb];"
        f"[amb][vo]amix=inputs=2:duration=first:dropout_transition=0.3[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{master_dur:.3f}",
        str(rough),
    ])

    open15 = OUT_DIR / "neutron_star_part-01_open15_v01.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(rough), "-t", "15",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2",
        str(open15),
    ])

    # QC stills: 0.5, 2.5, 8, 15, last 2s
    last = max(0.1, master_dur - 2.0)
    for t, name in [(0.5, "t00_5"), (2.5, "t02_5"), (8.0, "t08"), (15.0, "t15"), (last, "t_last2s")]:
        if t > master_dur:
            continue
        dest = QC / f"qc_{name}.jpg"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(rough), "-frames:v", "1", "-q:v", "2", str(dest),
        ])

    print(f"rough {rough} {probe(rough):.2f}s")
    print(f"open15 {open15} {probe(open15):.2f}s")
    print(f"vo {VO} {vo_dur:.2f}s  picture {pic_dur:.2f}s  VO starts at 0 (picture-first = no Orbit 0-3s)")
    print(f"plates used {len(clips)}")


if __name__ == "__main__":
    main()
