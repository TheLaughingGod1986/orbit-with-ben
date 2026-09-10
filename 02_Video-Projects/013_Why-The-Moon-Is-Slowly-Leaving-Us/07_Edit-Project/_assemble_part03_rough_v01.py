#!/usr/bin/env python3
"""Assemble Moon Leaving Part 03 rough: world plates + VO + ducked score bed."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PLATES = PROJ / "04_Generated-Clips/part03/flow_world_v01"
VO = PROJ / "02_Voiceover/parts/moon_leaving_part-03_vo_v01.wav"
MUSIC = PROJ / "05_Music/moon-leaving-part03_score_bed_v01.mp3"
WORK = PROJ / "07_Edit-Project/parts/_work_p03_v01"
OUT = PROJ / "07_Edit-Project/parts/moon_leaving_part-03_rough_v01.mp4"
META = PROJ / "07_Edit-Project/parts/moon_leaving_part-03_rough_v01_meta.json"
PLATE_MAP = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
TARGET_PLATES = 18


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


def pick_plates(need: int) -> list[Path]:
    files = sorted(
        [f for f in PLATES.glob("*.mp4") if f.stat().st_size > 200_000],
        key=lambda p: p.stat().st_mtime,
    )
    # Prefer newly minted p03_XX_*, then harvest/gallery/click — all unique files.
    minted = sorted([f for f in files if f.name.startswith("p03_0")], key=lambda p: p.name)
    other_p03 = [f for f in files if f.name.startswith("p03_") and f not in minted]
    rest = [f for f in files if f not in minted and f not in other_p03]
    ordered = minted + other_p03 + rest
    # de-dupe by md5
    import hashlib

    seen: set[str] = set()
    unique: list[Path] = []
    for f in ordered:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        unique.append(f)
    if len(unique) < need:
        raise SystemExit(
            f"need {need} unique plates, have {len(unique)} in {PLATES}"
        )
    return unique[:need]


def main() -> None:
    for p in (VO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    vo_dur = probe(VO)
    need = max(TARGET_PLATES, int(vo_dur // 8) + (1 if vo_dur % 8 > 0.5 else 0))
    # VO ~136.7s → 18 * 8 = 144; we'll trim picture to VO length.
    need = max(18, need)
    plates = pick_plates(need)
    WORK.mkdir(parents=True, exist_ok=True)

    beds: list[Path] = []
    for i, src in enumerate(plates, 1):
        bed = WORK / f"bed_{i:02d}.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(src),
                "-an",
                "-vf",
                "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-t",
                "8",
                str(bed),
            ]
        )
        beds.append(bed)

    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{b}'\n" for b in beds))
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
            str(concat),
            "-c",
            "copy",
            str(picture),
        ]
    )

    pic_dur = probe(picture)
    master = min(pic_dur, vo_dur)
    if pic_dur + 0.05 < vo_dur - 1.0:
        raise SystemExit(
            f"picture too short: pic={pic_dur:.2f}s vo={vo_dur:.2f}s "
            "(freeze-pad forbidden; mint more plates)"
        )

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
            str(picture),
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

    plate_rows = [
        {"i": i, "name": p.name, "path": str(p), "dur": probe(WORK / f"bed_{i:02d}.mp4")}
        for i, p in enumerate(plates, 1)
    ]
    PLATE_MAP.write_text(json.dumps(plate_rows, indent=2) + "\n")
    META.write_text(
        json.dumps(
            {
                "out": str(OUT),
                "duration_s": probe(OUT),
                "vo": str(VO),
                "music": str(MUSIC),
                "plates": [p.name for p in plates],
                "picture_first": True,
                "orbit_in_open": False,
                "amix_weights": "1 0.55",
                "sidechain": "threshold=0.018:ratio=8:attack=20:release=500",
            },
            indent=2,
        )
        + "\n"
    )
    print(f"OUT {OUT} ({probe(OUT):.3f}s)")

    if UAT.exists():
        dest = UAT / "moon_leaving_part-03_rough_v01.mp4"
        shutil.copy2(OUT, dest)
        status = UAT / "moon_leaving_part-03_STATUS.txt"
        status.write_text(
            "Part 03 (Why It Drifts) — ROUGH v01 ready for watch\n"
            f"File: {dest.name}\n"
            f"Duration: {probe(OUT):.1f}s\n"
            "World-only plates + VO + ducked score. No Orbit in open.\n"
            "Parts 01/02 LOCKED files remain unchanged.\n"
        )
        print(f"UAT {dest}")
    else:
        print("UAT folder missing — rough left in Edit-Project/parts/")


if __name__ == "__main__":
    main()
