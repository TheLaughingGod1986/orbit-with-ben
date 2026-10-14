#!/usr/bin/env python3
"""Assemble Monday Saturn Short v02 — Claude FAIL 5968302935 picture splits.

Cuts at 6.6 / 9.8 / 13.8 / 19.0 s. Covers stay. No Studio upload.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

import build_yellow_white_short_thumbs_v04 as t4  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

UAT = REPO / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/_uat_v03e"
CLIPS = REPO / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/04_Generated-Clips"
OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v02"
COVER_DIR = HERE / "08_Covers"
STILLS = HERE / "_work_v02_stills"

PLATE = UAT / "monday_ring_rain_ITS_FALLING_v03e.mp4"
PLATE_RAW = UAT / "monday_ring_rain_raw.mp4"
TUMBLE = CLIPS / "v07/veo_orbit_tumble_v03_fallback_0-3s.mp4"
VO = HERE / "monday_saturn_short_vo_v02_how_long.wav"

PIA17150 = STILLS / "PIA17150_fill_w5.png"
PIA21439 = STILLS / "PIA21439_9x16.png"
PIA21345 = STILLS / "PIA21345_9x16.png"

W, H = 1080, 1920
FPS = 30
LONG_TITLE = "How Long Do Saturn's Rings Have Left?"
AIR = "2026-10-12"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255)

# Absolute cut points (Claude)
T0_TEACH = 6.6
T1_DIVE = 9.8
T2_DIST = 13.8
T3_LOOP = 19.0


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return float(out)


def whoosh(dest: Path) -> None:
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=0.45:sample_rate=48000",
            "-af", "highpass=f=300,lowpass=f=2200,afade=t=in:st=0:d=0.02,afade=t=out:st=0.12:d=0.33,volume=0.55",
            str(dest),
        ]
    )


def norm_clip(src: Path, dest: Path, start: float, length: float, *, vf: str | None = None) -> None:
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start:.3f}", "-i", str(src),
        "-t", f"{length:.3f}",
    ]
    if vf:
        cmd += ["-vf", vf]
    cmd += [
        "-an", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(dest),
    ]
    run(cmd)


def still_push(src: Path, dest: Path, length: float, *, zoom_end: float = 1.06) -> None:
    # ~6% push when zoom_end=1.06
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"zoompan=z='min({zoom_end},1+0.0009*on)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS}"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-i", str(src),
            "-vf", vf, "-t", f"{length:.3f}", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dest),
        ]
    )


def loop_plate(src: Path, dest: Path, length: float, start: float = 0.4) -> None:
    usable = max(0.5, dur(src) - start - 0.2)
    reps = int(length // usable) + 2
    parts = []
    for i in range(reps):
        p = dest.parent / f"_loop_part_{i:02d}.mp4"
        norm_clip(
            src, p, start, usable,
            vf=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1",
        )
        parts.append(p)
    concat = dest.parent / "_loop_concat.txt"
    concat.write_text("\n".join(f"file '{p}'" for p in parts) + "\n")
    raw = dest.parent / "_loop_raw.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(raw)])
    norm_clip(raw, dest, 0.0, length)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 44)
    words = LONG_TITLE.replace("?", "").split()
    mid = len(words) // 2
    rows = [" ".join(words[:mid]), " ".join(words[mid:]) + "?"]
    y = int(H * 0.20)
    for row in rows:
        box = draw.textbbox((0, 0), row, font=font, stroke_width=5)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), row, font=font, fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += 56
    im.save(dest)


def build_cover() -> Path:
    """Reuse existing PASS cover if present; else rebuild."""
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    cover = COVER_DIR / "cover_monday-saturn-falling.jpg"
    if cover.exists() and cover.stat().st_size > 20_000:
        return cover
    plate_src = PLATE_RAW if PLATE_RAW.exists() else PLATE
    frame = COVER_DIR / "_plate_frame.png"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "2.0", "-i", str(plate_src), "-frames:v", "1", str(frame)])
    job = {
        "id": "monday-saturn-falling",
        "plate": frame,
        "out_dir": COVER_DIR,
        "lines": ["HOW LONG?", "FALLING"],
        "yellow": {"FALLING"},
        "hero": 1,
        "related": "55AEQwvs36g",
        "uk": "2026-10-12T11:30:00+01:00",
        "role": "monday_saturn",
    }
    t4.compose(job)
    im = Image.open(cover).convert("RGB")
    crop_h = int(t4.W * 9 / 16)
    y0 = (t4.H - crop_h) // 2
    im.crop((0, y0, t4.W, y0 + crop_h)).save(COVER_DIR / "cover_monday-saturn-falling_16x9.jpg", quality=90)
    return cover


def assemble() -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (PLATE, TUMBLE, VO, PIA17150, PIA21439, PIA21345):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")

    vo_s = dur(VO)
    head_s = 1.5
    tumble_s = 3.0
    mid_s = T0_TEACH - head_s - tumble_s  # 2.1
    teach1_s = T1_DIVE - T0_TEACH  # 3.2
    dive_s = T2_DIST - T1_DIVE  # 4.0
    dist_s = T3_LOOP - T2_DIST  # 5.2
    loop_s = max(3.5, vo_s + 0.6 - T3_LOOP)
    total = T3_LOOP + loop_s
    total = min(total, 39.0)

    scale_crop = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"

    # 0–1.5 plate head
    norm_clip(PLATE, WORK / "head.mp4", 0.05, head_s, vf=scale_crop)
    # 1.5–4.5 Orbit tumble
    tumble_vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H}:(iw-ow)/2:(ih-oh)/2,setsar=1"
    )
    norm_clip(TUMBLE, WORK / "tumble.mp4", 0.0, tumble_s, vf=tumble_vf)
    # 4.5–6.6 continue raining plate (no Orbit)
    norm_clip(PLATE, WORK / "mid.mp4", 0.6, mid_s, vf=scale_crop)
    # 6.6–9.8 PIA17150 reframed + push ~6%
    still_push(PIA17150, WORK / "teach1.mp4", teach1_s, zoom_end=1.06)
    # 9.8–13.8 Grand Finale dive illustration
    still_push(PIA21439, WORK / "dive.mp4", dive_s, zoom_end=1.05)
    # 13.8–19.0 rings at a distance
    still_push(PIA21345, WORK / "dist.mp4", dist_s, zoom_end=1.08)
    # 19.0–end plate loop
    loop_plate(PLATE, WORK / "loop.mp4", loop_s, start=0.5)

    parts = [
        WORK / "head.mp4",
        WORK / "tumble.mp4",
        WORK / "mid.mp4",
        WORK / "teach1.mp4",
        WORK / "dive.mp4",
        WORK / "dist.mp4",
        WORK / "loop.mp4",
    ]
    concat = WORK / "concat.txt"
    concat.write_text("\n".join(f"file '{p}'" for p in parts) + "\n")
    silent = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
    pic_s = dur(silent)

    title = WORK / "title.png"
    title_png(title)
    title_start, title_end = 9.0, min(14.0, pic_s - loop_s)

    whoosh(WORK / "whoosh.m4a")
    final = OUT / "monday_saturn_rings_already_falling_v02.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(silent),
            "-i", str(title),
            "-i", str(VO),
            "-i", str(WORK / "whoosh.m4a"),
            "-filter_complex",
            (
                f"[1:v]format=rgba,scale={W}:{H}[ttl];"
                f"[0:v][ttl]overlay=0:0:enable='between(t,{title_start:.3f},{title_end:.3f})',format=yuv420p[v];"
                f"[2:a]volume=1,apad[va];[3:a]adelay=0|0,volume=0.45[wh];"
                f"[va][wh]amix=inputs=2:duration=first:dropout_transition=0[a]"
            ),
            "-map", "[v]", "-map", "[a]",
            *shorts_encode_args(fps=FPS),
            "-t", f"{pic_s:.3f}",
            "-movflags", "+faststart",
            str(final),
        ]
    )
    meta = {
        "file": str(final),
        "version": "v02",
        "duration_s": dur(final),
        "vo_s": vo_s,
        "picture_s": pic_s,
        "cuts_s": [0.0, head_s, head_s + tumble_s, T0_TEACH, T1_DIVE, T2_DIST, T3_LOOP],
        "segments": {
            "head_s": head_s,
            "tumble_s": tumble_s,
            "mid_plate_s": mid_s,
            "pia17150_s": teach1_s,
            "pia21439_s": dive_s,
            "pia21345_s": dist_s,
            "loop_s": loop_s,
        },
        "orbit_in_s": head_s,
        "title_on_screen": LONG_TITLE,
        "title_window_s": [title_start, title_end],
        "air": AIR,
        "claude_fix": "5968302935",
        "stills": {
            "pia17150": str(PIA17150),
            "pia21439": str(PIA21439),
            "pia21345": str(PIA21345),
        },
        "vo": str(VO),
    }
    (OUT / "monday_saturn_rings_already_falling_v02_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    return final


def main() -> None:
    final = assemble()
    cover = build_cover()
    print("COVER", cover, flush=True)
    gate = subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(final), "--air-date", AIR, "--json",
        ],
        capture_output=True,
        text=True,
    )
    print(gate.stdout)
    print(gate.stderr, file=sys.stderr)
    (OUT / "monday_saturn_rings_already_falling_v02_gate.json").write_text(gate.stdout or gate.stderr or "{}\n")
    if gate.returncode not in (0, 1):
        raise SystemExit(f"gate tool error {gate.returncode}")
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
