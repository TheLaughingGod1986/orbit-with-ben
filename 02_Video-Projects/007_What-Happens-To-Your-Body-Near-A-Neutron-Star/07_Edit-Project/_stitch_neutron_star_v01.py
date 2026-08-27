#!/usr/bin/env python3
"""Stitch Neutron Star Parts 01–08 + 10s last-picture hold.

Ship target 7–9 min. No brand sting. No baked subscribe. No /go/.
Soft-join parts (xfade + acrossfade). Hold is AFTER VO — not freeze-pad under narration.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
PARTS_DIR = HERE / "parts"
OUT_DIR = EP / "09_Final-Export"
WORK = HERE / "parts/_work_stitch_v01"
QC = EP / "_qc_stitch_v01"
HOLD_S = 10.0
XFADE = 0.40
# Chapter joins: 0.4s xfade reads as a hard cut when VO has no tail.
# index = join into the next part (0 = P01→P02).
JOIN_XFADE = {
    0: 1.10,  # remnant fill → Orbit + distant star
    1: 1.20,  # space / mercy-runs-out → Earth kitchen lead
    2: 1.20,  # visor CU → grey-ball cinema skip
    3: 1.20,  # P04 → P05
    4: 1.20,  # P05 → P06
    5: 2.00,  # P06 where-spent → P07 remnant (VO both say "second")
    6: 2.00,  # P07 abort → P08 remnant fill
    7: 2.00,  # P08 refuse-landing → close (turn away / jewel)
}
JOIN_TRANS = {
    1: "fadeblack",  # space → kitchen
    2: "fadeblack",  # visor CU → grey-ball cinema skip
}

PARTS = [
    PARTS_DIR / "neutron_star_part-01_cursor_rough_v12.mp4",
    PARTS_DIR / "neutron_star_part-02_cursor_rough_v01.mp4",
    PARTS_DIR / "neutron_star_part-03_cursor_rough_v02.mp4",
    PARTS_DIR / "neutron_star_part-04_cursor_rough_v01.mp4",
    PARTS_DIR / "neutron_star_part-05_cursor_rough_v02.mp4",
    PARTS_DIR / "neutron_star_part-06_cursor_rough_v02.mp4",
    PARTS_DIR / "neutron_star_part-07_cursor_rough_v04.mp4",
    PARTS_DIR / "neutron_star_part-08_cursor_rough_v01.mp4",
    PARTS_DIR / "neutron_star_part-09_close_rough_v01.mp4",
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
    QC.mkdir(parents=True, exist_ok=True)
    parts = list(PARTS)
    close = PARTS_DIR / "neutron_star_part-09_close_rough_v01.mp4"
    if close in parts and (not close.exists() or close.stat().st_size < 200_000):
        print("skip close — Part 09 rough not built yet", flush=True)
        parts = [p for p in parts if p != close]
    missing = [p for p in parts if not p.exists() or p.stat().st_size < 200_000]
    if missing:
        raise SystemExit("missing parts:\n" + "\n".join(str(p) for p in missing))

    beds = []
    for i, src in enumerate(parts, 1):
        bed = WORK / f"part_{i:02d}.mp4"
        reuse = (
            bed.exists()
            and bed.stat().st_size > 1_000_000
            and bed.stat().st_mtime >= src.stat().st_mtime
        )
        if reuse:
            print(f"reuse {bed.name}", flush=True)
        else:
            print(f"encode {bed.name} from {src.name}", flush=True)
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,format=yuv420p",
                "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
                "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
                str(bed),
            ])
        beds.append(bed)

    n = len(beds)
    durs = [probe(b) for b in beds]
    xfades = [float(JOIN_XFADE.get(i, XFADE)) for i in range(n - 1)]
    trans = [str(JOIN_TRANS.get(i, "fade")) for i in range(n - 1)]
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + durs[i - 1] - xfades[i - 1])
    joined_dur = offsets[-1] + durs[-1]

    ins: list[str] = []
    for b in beds:
        ins += ["-i", str(b)]
    filters = []
    vprev, aprev = "0:v", "0:a"
    for i in range(1, n):
        vout, aout = f"v{i}", f"a{i}"
        xd = xfades[i - 1]
        tr = trans[i - 1]
        filters.append(
            f"[{vprev}][{i}:v]xfade=transition={tr}:duration={xd:.3f}:offset={offsets[i]:.3f}[{vout}]"
        )
        filters.append(f"[{aprev}][{i}:a]acrossfade=d={xd:.3f}[{aout}]")
        vprev, aprev = vout, aout

    joined = WORK / "joined_01_08.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *ins,
        "-filter_complex", ";".join(filters),
        "-map", f"[{vprev}]", "-map", f"[{aprev}]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{joined_dur:.3f}",
        str(joined),
    ])

    # 10s last-picture hold AFTER VO — last real frame, not a baked fade-to-black.
    hold_at = max(0.05, joined_dur - 0.12)
    hold_frame = WORK / "hold_frame.jpg"
    hold_clip = WORK / "hold_10s.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{hold_at:.3f}", "-i", str(joined), "-frames:v", "1", "-q:v", "2",
        str(hold_frame),
    ])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(hold_frame),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", f"{HOLD_S:.3f}",
        "-vf", "scale=1920:1080,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(hold_clip),
    ])

    master = OUT_DIR / "neutron_star_broadcast_v01.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(joined), "-i", str(hold_clip),
        "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-movflags", "+faststart",
        str(master),
    ])

    dur = probe(master)
    for t, name in [
        (0.5, "t00_5"),
        (2.5, "t02_5"),
        (8.0, "t08"),
        (15.0, "t15"),
        (max(0.0, durs[0] - 2.4), "p01_prejoin"),
        (max(0.0, durs[0] - 1.0), "p01_end"),
        (offsets[1] + 0.2, "p02_join_in"),
        (offsets[1] + 1.4, "p02_after_join"),
        (max(0.0, offsets[2] - 1.6), "p02_prejoin"),
        (offsets[2] + 0.3, "p03_join_in"),
        (offsets[2] + 1.5, "p03_after_join"),
        (max(0.0, offsets[3] - 1.6), "p03_prejoin"),
        (offsets[3] + 0.3, "p04_join_in"),
        (offsets[3] + 1.5, "p04_after_join"),
        (joined_dur - 2.0, "p08_last2s"),
        (joined_dur + 1.0, "hold_plus1"),
        (max(0.0, dur - 0.3), "t_last"),
    ]:
        t = min(max(0.05, t), max(0.05, dur - 0.08))
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(master), "-frames:v", "1", "-q:v", "2",
            str(QC / f"qc_{name}.jpg"),
        ])

    print(f"joined {joined} {probe(joined):.3f}s")
    print(f"master {master} {dur:.3f}s  hold={HOLD_S:.1f}s")
    print(f"part durs {[round(d, 2) for d in durs]}")
    print(f"xfades {[round(x, 2) for x in xfades]} trans={trans}")
    print(f"offsets {[round(o, 2) for o in offsets]}")
    minutes = dur / 60.0
    if not (7.0 <= minutes <= 9.2):
        print(f"WARN duration {minutes:.2f} min is outside 7–9 target", flush=True)
    else:
        print(f"duration {minutes:.2f} min — inside 7–9 ship target", flush=True)


if __name__ == "__main__":
    main()
