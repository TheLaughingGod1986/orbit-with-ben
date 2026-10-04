#!/usr/bin/env python3
"""Black Dwarf Short v03 — re-overlay only.

Claude 5979552650: bump frame-0 hook caption to 8–10% of frame height.
Reuse silent picture.mp4 (no Omni re-mint). Same VO / whoosh / title timing as v02.
Do NOT upload.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

W, H = 1080, 1920
FPS = 30
AIR = "2026-10-16"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0)
WHITE = (255, 255, 255)
TARGET_DUR = 26.9  # match v02 pad (Claude 5968735734)

WORK_V02 = HERE / "_work_v02"
WORK = HERE / "_work_v03"
OUT = HERE / "06_Final-Exports"
REVIEW = OUT / "review"
HANDOFF = Path("/Users/benjaminoats/_desk/handoff")
VO = HERE / "friday_black_dwarf_short_vo_v01.wav"
PICTURE = WORK_V02 / "picture.mp4"
TITLE = WORK_V02 / "title.png"
WHOOSH = WORK_V02 / "whoosh.m4a"
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"


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


def make_hook(dest: Path) -> dict:
    """Build NOT (white) / YET (yellow) at 8–10% glyph height of 1920.

    Side-by-side like v02. Max size that fits width with stroke 6 is ~220 → ~8.8%.
    Assert measured glyph height lands in [8.0, 10.0]%.
    """
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    words = [("NOT", WHITE), ("YET", YELLOW)]
    stroke = 6
    gap = 12
    # Prefer ~9% mid; binary-search largest size that fits and stays ≤10%
    lo, hi = 154, 248
    best = None
    while lo <= hi:
        size = (lo + hi) // 2
        font = ImageFont.truetype(FONT, size)
        box_y = draw.textbbox((0, 0), "Y", font=font, stroke_width=stroke)
        gh = box_y[3] - box_y[1]
        pct = 100.0 * gh / H
        widths = []
        for word, _ in words:
            b = draw.textbbox((0, 0), word, font=font, stroke_width=stroke)
            widths.append(b[2] - b[0])
        total = sum(widths) + gap
        fits = total <= W - 32
        in_band = 8.0 <= pct <= 10.0
        if fits and in_band:
            best = (size, font, widths, gh, pct, total)
            lo = size + 1  # try larger
        elif (not fits) or pct > 10.0:
            hi = size - 1
        else:
            # too small (<8%)
            lo = size + 1
    if best is None:
        raise SystemExit("could not find hook font size in 8–10% band that fits width")
    size, font, widths, gh, pct, total = best
    assert 8.0 <= pct <= 10.0, f"glyph pct {pct:.2f} out of band"
    x = (W - total) // 2
    y = int(H * 0.34)
    for (word, color), ww in zip(words, widths):
        draw.text((x, y), word, font=font, fill=color, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        x += ww + gap
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)
    metrics = {
        "font_size": size,
        "stroke": stroke,
        "gap": gap,
        "glyph_h_px": gh,
        "glyph_pct_of_1920": round(pct, 2),
        "total_width": total,
        "y_frac": 0.34,
        "text": "NOT YET",
        "colors": {"NOT": "white", "YET": "yellow"},
    }
    print("HOOK", json.dumps(metrics), flush=True)
    return metrics


def pad_picture(src: Path, dest: Path, target: float) -> float:
    src_s = dur(src)
    if src_s >= target - 0.01:
        shutil.copy2(src, dest)
        return dur(dest)
    pad = target - src_s
    # clone last frame to match v02 26.9s end-hold pad
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(src),
            "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
            "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            str(dest),
        ]
    )
    return dur(dest)


def extract_frame0(mp4: Path, png: Path) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(mp4),
            "-vf", "select=eq(n\\,0)",
            "-frames:v", "1",
            str(png),
        ]
    )


def six_frame_sheet(mp4: Path, dest: Path) -> None:
    """6-frame open contact sheet (0.0–1.0s) if gate sheet is elsewhere."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = WORK / "_sheet_frames"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    # sample 6 frames across first 1.0s
    for i, t in enumerate([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]):
        run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{t:.3f}", "-i", str(mp4),
                "-frames:v", "1",
                "-vf", "scale=270:-1",
                str(tmp / f"f{i}.png"),
            ]
        )
    # tile 1x6
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(tmp / "f0.png"),
            "-i", str(tmp / "f1.png"),
            "-i", str(tmp / "f2.png"),
            "-i", str(tmp / "f3.png"),
            "-i", str(tmp / "f4.png"),
            "-i", str(tmp / "f5.png"),
            "-filter_complex", "hstack=inputs=6",
            "-frames:v", "1",
            str(dest),
        ]
    )


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    HANDOFF.mkdir(parents=True, exist_ok=True)

    for p in (PICTURE, VO, TITLE):
        if not p.exists():
            raise SystemExit(f"missing: {p}")

    whoosh_path = WHOOSH if WHOOSH.exists() else (WORK / "whoosh.m4a")
    if not WHOOSH.exists():
        whoosh(whoosh_path)

    hook_metrics = make_hook(WORK / "hook.png")
    pic_s = pad_picture(PICTURE, WORK / "picture_padded.mp4", TARGET_DUR)
    print(f"PICTURE padded {dur(PICTURE):.3f} → {pic_s:.3f}", flush=True)

    title_start, title_end = 9.0, 14.0
    final = OUT / "friday_black_dwarf_why_none_yet_v03.mp4"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(WORK / "picture_padded.mp4"),
            "-i", str(WORK / "hook.png"),
            "-i", str(TITLE),
            "-i", str(VO),
            "-i", str(whoosh_path),
            "-filter_complex",
            (
                f"[1:v]format=rgba,scale={W}:{H}[hk];"
                f"[2:v]format=rgba,scale={W}:{H}[ttl];"
                f"[0:v][hk]overlay=0:0:enable='between(t,0,2.2)'[v1];"
                f"[v1][ttl]overlay=0:0:enable='between(t,{title_start:.3f},{title_end:.3f})',format=yuv420p[v];"
                f"[3:a]volume=1,apad[va];[4:a]adelay=0|0,volume=0.45[wh];"
                f"[va][wh]amix=inputs=2:duration=first:dropout_transition=0[a]"
            ),
            "-map", "[v]", "-map", "[a]",
            *shorts_encode_args(fps=FPS),
            "-t", f"{pic_s:.3f}",
            "-movflags", "+faststart",
            str(final),
        ]
    )
    final_s = dur(final)

    meta = {
        "file": str(final),
        "version": "v03",
        "duration_s": final_s,
        "vo_s": dur(VO),
        "picture_s": pic_s,
        "picture_src": str(PICTURE),
        "picture_note": f"reused silent picture.mp4; tpad clone to {TARGET_DUR}s (v02 end-hold pad)",
        "title_on_screen": "What Happens When the Last Star Dies?",
        "title_window_s": [title_start, title_end],
        "hook": "NOT YET",
        "hook_metrics": hook_metrics,
        "hook_note": "frame-0 caption 8–10% of frame height (was v02 size 86 ≈ 4%)",
        "air": AIR,
        "claude_ref": "5979552650",
        "claude_thread": "5979552650",
        "orbit_pip_placeholder": False,
        "omni_remint": False,
        "vo": str(VO),
        "upload": False,
        "buffer": False,
    }
    meta_path = OUT / "friday_black_dwarf_why_none_yet_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

    sheet_dir = REVIEW
    gate = subprocess.run(
        [
            sys.executable,
            str(GATE),
            "check",
            str(final),
            "--air-date",
            AIR,
            "--json",
            "--sheet-dir",
            str(sheet_dir),
        ],
        capture_output=True,
        text=True,
    )
    gate_path = OUT / "friday_black_dwarf_why_none_yet_v03_gate.json"
    gate_body = gate.stdout or gate.stderr or "{}\n"
    gate_path.write_text(gate_body)
    print("GATE_STDOUT", gate.stdout, flush=True)
    if gate.stderr:
        print("GATE_STDERR", gate.stderr, flush=True)
    print("GATE_RC", gate.returncode, flush=True)

    frame0 = REVIEW / "friday_black_dwarf_why_none_yet_v03_frame0.png"
    extract_frame0(final, frame0)
    handoff_frame = HANDOFF / "bd_v03_frame0.png"
    shutil.copy2(frame0, handoff_frame)

    # ensure a 6-frame open sheet lives next to review assets
    open_sheet = REVIEW / "friday_black_dwarf_why_none_yet_v03_open_sheet.jpg"
    gate_sheet = None
    try:
        gdata = json.loads(gate_body)
        if isinstance(gdata, list) and gdata:
            gate_sheet = gdata[0].get("contact_sheet")
    except Exception:
        pass
    if gate_sheet and Path(gate_sheet).exists():
        if Path(gate_sheet).resolve() != open_sheet.resolve():
            shutil.copy2(gate_sheet, open_sheet)
    if not open_sheet.exists():
        six_frame_sheet(final, open_sheet)

    print("FINAL", final, flush=True)
    print("META", meta_path, flush=True)
    print("GATE", gate_path, flush=True)
    print("FRAME0", frame0, flush=True)
    print("HANDOFF", handoff_frame, flush=True)
    print("SHEET", open_sheet, flush=True)
    if gate.returncode not in (0, 1):
        raise SystemExit(f"gate tool error {gate.returncode}")
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
