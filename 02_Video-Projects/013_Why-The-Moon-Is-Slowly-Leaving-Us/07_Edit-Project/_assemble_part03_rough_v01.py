#!/usr/bin/env python3
"""Assemble Moon Leaving Part 03 rough v01 — picture-first, no freeze-pad.

Requires ~18 unique world plates covering VO (~136.7s).
Does not remint Part 01/02. Does not reuse Part 01/02 plates.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
OUT_DIR = HERE / "parts"
WORK = OUT_DIR / "_work_p03_v01"
OUT = OUT_DIR / "moon_leaving_part-03_rough_v01.mp4"
META = OUT_DIR / "moon_leaving_part-03_rough_v01_mix_meta.json"
PLATES_DIR = PROJ / "04_Generated-Clips/part03/flow_world_v01"
INVENTORY = PLATES_DIR / "_inventory_v01.json"
VO_CANDIDATES = [
    PROJ / "02_Voiceover/parts/moon_leaving_part-03_vo_v01.wav",
    PROJ / "02_Voiceover/parts/moon_leaving_part-03_vo_v01.mp3",
    PROJ / "02_Voiceover/parts/moon_leaving_part-03_vo_v01.m4a",
]
MUSIC_CANDIDATES = [
    PROJ / "05_Music/moon-leaving-part03_score_bed_v01.mp3",
    PROJ / "05_Music/moon-leaving-part03_score_bed_v01.wav",
]
NEED_PLATES = 18
VO_TARGET_S = 136.7


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


def first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.exists() and p.stat().st_size > 1000:
            return p
    return None


def load_plates() -> list[Path]:
    if INVENTORY.exists():
        data = json.loads(INVENTORY.read_text())
        files = [PLATES_DIR / row["file"] for row in data.get("plates", [])]
        files = [p for p in files if p.exists()]
        if files:
            return files
    return sorted(
        [p for p in PLATES_DIR.glob("*.mp4") if p.stat().st_size > 200_000],
        key=lambda p: p.name,
    )


def main() -> int:
    plates = load_plates()
    total = sum(probe(p) for p in plates)
    if len(plates) < NEED_PLATES or total < VO_TARGET_S - 2.0:
        print(
            f"ABORT need ~{NEED_PLATES} unique plates covering ~{VO_TARGET_S}s; "
            f"have {len(plates)} plates / {total:.1f}s. Freeze-pad forbidden.",
            flush=True,
        )
        return 2

    vo = first_existing(VO_CANDIDATES)
    if not vo:
        print("ABORT missing Part 03 VO wav/mp3 under 02_Voiceover/parts/", flush=True)
        return 2

    WORK.mkdir(parents=True, exist_ok=True)
    beds: list[Path] = []
    # Spend VO length across plates in order (trim last plate; never freeze-extend).
    remaining = probe(vo)
    for i, src in enumerate(plates, 1):
        if remaining <= 0.05:
            break
        src_dur = probe(src)
        use = min(src_dur, remaining)
        bed = WORK / f"bed_{i:02d}.mp4"
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,fps=24,format=yuv420p"
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(src),
                "-vf",
                vf,
                "-an",
                "-t",
                f"{use:.3f}",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                str(bed),
            ]
        )
        beds.append(bed)
        remaining -= use

    if remaining > 1.0:
        print(
            f"ABORT picture short by {remaining:.1f}s after spending plates; "
            "mint more unique world plates (no freeze-pad).",
            flush=True,
        )
        return 2

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{b}'\n" for b in beds))
    picture = WORK / "picture.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-an",
            str(picture),
        ]
    )

    pic_dur = probe(picture)
    use_vo = WORK / "vo_trim.wav"
    vo_dur = probe(vo)
    if vo_dur > pic_dur + 0.05:
        fade_at = max(0.0, pic_dur - 0.8)
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(vo),
                "-t",
                f"{pic_dur:.3f}",
                "-af",
                f"afade=t=out:st={fade_at:.3f}:d=0.8",
                "-c:a",
                "pcm_s16le",
                str(use_vo),
            ]
        )
    else:
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(vo),
                "-c:a",
                "pcm_s16le",
                str(use_vo),
            ]
        )

    music = first_existing(MUSIC_CANDIDATES)
    fc = "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[vo]"
    inputs = ["-i", str(picture), "-i", str(use_vo)]
    maps = ["-map", "0:v", "-map", "[a]"]
    if music:
        inputs += ["-i", str(music)]
        fc += (
            ";[2:a]volume=0.12,afade=t=in:st=0:d=1,"
            f"afade=t=out:st={max(0.0, pic_dur - 1.5):.3f}:d=1.5[m];"
            "[vo][m]amix=inputs=2:duration=first:dropout_transition=0[a]"
        )
    else:
        fc += ";[vo]anull[a]"

    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            *inputs,
            "-filter_complex",
            fc,
            *maps,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(OUT),
        ]
    )

    meta = {
        "out": str(OUT),
        "duration_s": probe(OUT),
        "plates_used": [p.name for p in plates[: len(beds)]],
        "vo": str(vo),
        "music": str(music) if music else None,
        "picture_first": True,
        "freeze_pad": False,
        "do_not_remint": ["part01_LOCKED_v04", "part02_LOCKED_v01"],
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"OUT {OUT} ({meta['duration_s']:.3f}s)", flush=True)
    print(json.dumps(meta, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
