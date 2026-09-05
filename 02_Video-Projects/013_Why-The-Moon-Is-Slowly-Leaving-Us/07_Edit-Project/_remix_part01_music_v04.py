#!/usr/bin/env python3
"""Remix Moon Leaving Part 01 rough with ducked underscore under VO.

Takes the locked Part 01 picture (v03) + Ben Orbit Narrator VO + ElevenLabs
score bed → soft sidechain-ducked mix (neutron-star house levels).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
VIDEO = PROJ / "07_Edit-Project/parts/moon_leaving_part-01_rough_v03.mp4"
VO = PROJ / "02_Voiceover/parts/moon_leaving_part-01_vo_v01.wav"
MUSIC = PROJ / "05_Music/moon-leaving-part01_score_bed_v01.mp3"
OUT = PROJ / "07_Edit-Project/parts/moon_leaving_part-01_rough_v04.mp4"
META = PROJ / "07_Edit-Project/parts/moon_leaving_part-01_rough_v04_mix_meta.json"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def main() -> None:
    for p in (VIDEO, VO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    master = min(probe(VIDEO), probe(VO))
    fade_st = max(0.0, master - 2.5)
    graph = (
        f"[0:v]trim=0:{master:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{master:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,"
        "loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[vo][vo_sc];"
        f"[2:a]aloop=loop=-1:size=2e+09,atrim=0:{master:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,"
        "loudnorm=I=-28:LRA=9:TP=-3,"
        f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_st:.3f}:d=2.5[music];"
        "[music][vo_sc]sidechaincompress="
        "threshold=0.018:ratio=8:attack=20:release=500[ducked];"
        "[vo][ducked]amix=inputs=2:weights='1 0.55':normalize=0,"
        "alimiter=limit=0.90:level=false[a]"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(VIDEO),
            "-i",
            str(VO),
            "-i",
            str(MUSIC),
            "-filter_complex",
            graph,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-b:a",
            "192k",
            "-t",
            f"{master:.3f}",
            str(OUT),
        ]
    )
    META.write_text(
        json.dumps(
            {
                "video": str(VIDEO),
                "vo": str(VO),
                "music": str(MUSIC),
                "out": str(OUT),
                "duration_s": probe(OUT),
                "music_target_lufs": -28,
                "vo_target_lufs": -16,
                "amix_weights": "1 0.55",
                "sidechain": "threshold=0.018:ratio=8:attack=20:release=500",
                "fade_in_s": 1.2,
                "fade_out_s": 2.5,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"OUT {OUT} ({probe(OUT):.3f}s)")

    if UAT.exists():
        for old in UAT.glob("moon_leaving_part-01_rough_v0*.mp4"):
            old.unlink()
        dest = UAT / "moon_leaving_part-01_rough_v04.mp4"
        shutil.copy2(OUT, dest)
        print(f"UAT {dest}")


if __name__ == "__main__":
    main()
