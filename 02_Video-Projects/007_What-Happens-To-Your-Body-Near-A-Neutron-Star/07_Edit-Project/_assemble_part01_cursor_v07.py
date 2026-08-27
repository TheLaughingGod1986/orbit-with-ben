#!/usr/bin/env python3
"""Assemble Neutron Star Part 01 v07: same v06 picture, continuous score under VO.

Omni native beds restart every ~8s plate — that read as music cutting.
v07 keeps picture, ducks a single 76s underscore under Ben Orbit Narrator,
and keeps Omni SFX as quiet texture only.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
PICTURE = HERE / "parts/_work_part01_cursor_v06/picture.mp4"
VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.wav"
if not VO.exists():
    VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.mp3"
MUSIC = EP / "05_Music/neutron_star_part01_score_bed_v01.mp3"
OUT_DIR = HERE / "parts"
QC = EP / "_qc_p01_cursor_v07"


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
    for p in (PICTURE, VO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    QC.mkdir(parents=True, exist_ok=True)
    vo_dur = probe(VO)
    pic_dur = probe(PICTURE)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"Picture {pic_dur:.2f}s shorter than VO {vo_dur:.2f}s")
    master_dur = vo_dur
    rough = OUT_DIR / "neutron_star_part-01_cursor_rough_v07.mp4"
    # VO lead. Continuous score ducked under speech. Omni SFX as quiet texture
    # so plate joins no longer read as a new song starting.
    graph = (
        f"[0:v]trim=0:{master_dur:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][vo_sc];"
        f"[2:a]atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS,"
        "loudnorm=I=-28:LRA=9:TP=-3,"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        f"[0:a]volume=0.08,atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo[omni];"
        "[music][vo_sc]sidechaincompress="
        "threshold=0.018:ratio=8:attack=20:release=500[ducked];"
        "[vo][ducked][omni]amix=inputs=3:weights='1 0.55 0.28':normalize=0,"
        "alimiter=limit=0.90:level=false[a]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(PICTURE), "-i", str(VO), "-i", str(MUSIC),
        "-filter_complex", graph,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{master_dur:.3f}",
        str(rough),
    ])
    open15 = OUT_DIR / "neutron_star_part-01_cursor_open15_v07.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(rough), "-t", "15",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(open15),
    ])
    print(f"rough {rough} {probe(rough):.3f}s")
    print(f"open15 {open15} {probe(open15):.3f}s")
    print(f"vo {vo_dur:.2f}s  picture {pic_dur:.2f}s  music {probe(MUSIC):.2f}s")


if __name__ == "__main__":
    main()
