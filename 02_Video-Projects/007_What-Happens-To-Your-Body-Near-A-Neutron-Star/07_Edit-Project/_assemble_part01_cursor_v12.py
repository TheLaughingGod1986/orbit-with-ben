#!/usr/bin/env python3
"""Assemble Neutron Star Part 01 v12: remnant-first picture recut. VO+music stay.

VO lock (do not rewrite): “Orbit hangs in the dark. A tiny orange figure against
a star that looks almost ordinary. Then the numbers arrive, and ordinary dies.”
0–~6.5s star only. The v12 banks-in take has TWO Orbits baked in — skip it.
First Orbit in this minute is the later tumble plate (one character). Do not xfade twin plates.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

EP = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star")
HERE = Path(__file__).resolve().parent
PLATES = json.loads((HERE / "parts/part-01_omni_plates_cursor_v12.json").read_text())
RAW = EP / "04_Generated-Clips/01_Raw/part-01"
VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.wav"
if not VO.exists():
    VO = EP / "02_Voiceover/parts/neutron_star_part-01_vo_v01.mp3"
MUSIC = EP / "05_Music/neutron_star_part01_score_bed_v01.mp3"
OUT_DIR = HERE / "parts"
WORK = HERE / "parts/_work_part01_cursor_v12"
QC = EP / "_qc_p01_cursor_v12"
XFADE = 0.40


def probe(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def letterbox_vf(src: Path) -> str:
    """Fill 1920x1080. If Omni baked 2.35:1 bars, crop them first."""
    detect = subprocess.check_output(
        [
            "ffmpeg", "-hide_banner", "-i", str(src), "-t", "1.2",
            "-vf", "cropdetect=24:16:0", "-f", "null", "-",
        ],
        stderr=subprocess.STDOUT, text=True,
    )
    crops = [ln.split("crop=")[-1].strip() for ln in detect.splitlines() if "crop=" in ln]
    fill = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,fps=24,format=yuv420p"
    )
    if not crops:
        return fill
    last = crops[-1]
    try:
        w, h, x, y = (int(p) for p in last.split(":"))
    except ValueError:
        return fill
    if "almost-ordinary-star" in src.name:
        # Leftover is 1280x720 with 2.35:1 bars. Crop bars, then push in so the star fills.
        return (
            "crop=1280:576:0:72,scale=2560:1152,crop=1920:1080:320:36,"
            "fps=24,format=yuv420p"
        )
    if 480 <= h <= 620 and w >= 1100:
        return f"crop={w}:{h}:{x}:{y},{fill}"
    return fill


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QC.mkdir(parents=True, exist_ok=True)
    plates = [p for p in PLATES["plates"] if not p.get("skip")]
    clips = []
    for plate in plates:
        src = RAW / plate["file"]
        if not src.exists() or src.stat().st_size < 200_000:
            raise SystemExit(f"missing plate {src}")
        clips.append(src)

    beds = []
    for i, (src, plate) in enumerate(zip(clips, plates), 1):
        bed = WORK / f"bed_{i:02d}.mp4"
        vf = letterbox_vf(src)
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        ss = plate.get("ss")
        if ss:
            cmd += ["-ss", f"{float(ss):.2f}"]
        cmd += ["-i", str(src)]
        tlim = plate.get("t")
        if tlim:
            cmd += ["-t", f"{float(tlim):.2f}"]
        cmd += [
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            str(bed),
        ]
        print(f"bed {i:02d} {src.name} vf={vf} ss={ss} t={tlim}", flush=True)
        run(cmd)
        beds.append(bed)

    n = len(beds)
    durs = [probe(b) for b in beds]
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + durs[i - 1] - XFADE)
    out_dur = offsets[-1] + durs[-1]

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

    vo_dur = probe(VO)
    pic_dur = probe(picture)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"Picture {pic_dur:.2f}s shorter than VO {vo_dur:.2f}s — generate more plates, do not freeze-pad"
        )
    if not MUSIC.exists():
        raise SystemExit(f"missing music {MUSIC}")
    music_dur = probe(MUSIC)
    # Last VO line ends on the file. Keep leftover unique remnant-rising
    # so the P01→P02 join can breathe instead of chopping into Orbit.
    # Never freeze-pad: tail is only unused 1× motion already in picture.mp4.
    post_vo_tail = min(2.40, pic_dur - vo_dur, music_dur - vo_dur)
    if post_vo_tail < 0.80:
        raise SystemExit(
            f"Need leftover unique picture after VO for the P01→P02 join "
            f"(pic {pic_dur:.2f}s vo {vo_dur:.2f}s music {music_dur:.2f}s)"
        )
    master_dur = vo_dur + post_vo_tail
    rough = OUT_DIR / "neutron_star_part-01_cursor_rough_v12.mp4"
    graph = (
        f"[0:v]trim=0:{master_dur:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]apad=whole_dur={master_dur:.3f},atrim=0:{master_dur:.3f},"
        "asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][vo_sc];"
        f"[2:a]atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS,"
        "loudnorm=I=-28:LRA=9:TP=-3,"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        f"[0:a]volume=0.08,apad=whole_dur={master_dur:.3f},"
        f"atrim=0:{master_dur:.3f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo[omni];"
        "[music][vo_sc]sidechaincompress="
        "threshold=0.018:ratio=8:attack=20:release=500[ducked];"
        "[vo][ducked][omni]amix=inputs=3:weights='1 0.55 0.28':normalize=0,"
        "alimiter=limit=0.90:level=false[a]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(VO), "-i", str(MUSIC),
        "-filter_complex", graph,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-t", f"{master_dur:.3f}",
        str(rough),
    ])

    open15 = OUT_DIR / "neutron_star_part-01_cursor_open15_v12.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(rough), "-t", "15",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(open15),
    ])
    first8 = OUT_DIR / "_audit_open7/p01_v12_first8.mp4"
    first8.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(rough), "-t", "8",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        str(first8),
    ])

    last = max(0.1, master_dur - 2.0)
    for t, name in [
        (0.5, "t00_5"),
        (2.5, "t02_5"),
        (3.0, "t03"),
        (3.4, "t03_4"),
        (4.0, "t04"),
        (4.4, "t04_4"),
        (5.0, "t05"),
        (6.0, "t06"),
        (7.0, "t07"),
        (7.8, "t07_8"),
        (8.0, "t08"),
        (15.0, "t15"),
        (25.0, "t25"),
        (54.0, "t54"),
        (61.0, "t61"),
        (65.0, "t65"),
        (68.0, "t68"),
        (last, "t_last2s"),
    ]:
        dest = QC / f"qc_{name}.jpg"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(rough), "-frames:v", "1", "-q:v", "2", str(dest),
        ])

    print(f"rough {rough} {probe(rough):.3f}s")
    print(f"open15 {open15} {probe(open15):.3f}s")
    print(f"first8 {first8} {probe(first8):.3f}s")
    print(f"vo {VO} {vo_dur:.2f}s  picture {pic_dur:.2f}s  post_vo_tail={post_vo_tail:.2f}s")
    print(f"plates used {len(clips)} xfade={XFADE}")
    print(f"offsets {[round(o, 2) for o in offsets]}")


if __name__ == "__main__":
    main()
