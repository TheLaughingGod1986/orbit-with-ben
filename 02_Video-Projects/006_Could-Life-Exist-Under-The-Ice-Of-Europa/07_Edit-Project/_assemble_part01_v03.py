#!/usr/bin/env python3
"""Assemble Europa Part 01 rough v03 — soft A/V crossfades, no freeze, VO mix."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
VO = EP / "02_Voiceover/parts/europa_part-01_vo_v01.mp3"
PLATES_JSON = EP / "07_Edit-Project/parts/part-01_omni_plates_v03.json"
CLIPS = EP / "04_Generated-Clips/01_Raw/part-01"
OUT_DIR = EP / "07_Edit-Project/parts"
WORK = OUT_DIR / "_work_part01_v03"
MASTER = OUT_DIR / "europa_part-01_rough_v03.mp4"
XFADE = 0.40  # picture + SFX blend at each join (keeps A/V locked)


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


def make_bed(src: Path, bed: Path) -> float:
    src_dur = probe(src)
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p"
    )
    run(
        [
            "ffmpeg", "-y", "-i", str(src), "-t", f"{src_dur:.3f}",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            str(bed),
        ]
    )
    return probe(bed)


def main() -> None:
    plan = json.loads(PLATES_JSON.read_text())
    vo_dur = probe(VO)
    available: list[tuple[dict, Path]] = []
    for plate in plan["plates"]:
        src = CLIPS / plate["file"]
        if not (src.exists() and src.stat().st_size > 500_000):
            raise SystemExit(f"missing plate: {src.name}")
        available.append((plate, src))

    WORK.mkdir(parents=True, exist_ok=True)
    beds: list[Path] = []
    durs: list[float] = []
    for plate, src in available:
        bed = WORK / f"bed_{plate['id']}.mp4"
        d = make_bed(src, bed)
        if d <= XFADE + 0.2:
            raise SystemExit(f"bed too short for xfade: {bed.name} ({d:.2f}s)")
        beds.append(bed)
        durs.append(d)
        print(f"bed {plate['id']} use={d:.2f}s ({plate['slug']})", flush=True)

    n = len(beds)
    inputs: list[str] = []
    for b in beds:
        inputs += ["-i", str(b)]
    inputs += ["-i", str(VO)]

    fc: list[str] = []
    if n == 1:
        fc.append("[0:v]null[vout]")
        fc.append("[0:a]volume=0.22[sfx]")
        out_dur = durs[0]
    else:
        # Pair xfade + acrossfade so Omni SFX never hard-stops at picture cuts.
        v_prev, a_prev = "0:v", "0:a"
        running = durs[0]
        for i in range(1, n):
            offset = running - XFADE
            v_out = "vout" if i == n - 1 else f"v{i}"
            a_out = "a_xf" if i == n - 1 else f"a{i}"
            fc.append(
                f"[{v_prev}][{i}:v]xfade=transition=fade:duration={XFADE:.3f}:offset={offset:.3f}[{v_out}]"
            )
            fc.append(
                f"[{a_prev}][{i}:a]acrossfade=d={XFADE:.3f}:c1=tri:c2=tri[{a_out}]"
            )
            v_prev, a_prev = v_out, a_out
            running = running + durs[i] - XFADE
        fc.append(f"[{a_prev}]volume=0.22[sfx]")
        out_dur = running

    vo_idx = n
    fc.append(
        f"[{vo_idx}:a]volume=1.0[vo];"
        f"[sfx][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
    )
    master_dur = min(out_dur, vo_dur)
    print(
        f"xfade={XFADE}s joins={n - 1} picture≈{out_dur:.2f}s master={master_dur:.2f}s",
        flush=True,
    )
    run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[aout]",
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
