#!/usr/bin/env python3
"""Black Dwarf Short v04 — re-overlay only (Claude 5979587053).

Two-line centred stack: NOT (white) above, YET (yellow) below.
Each line glyph height 8–10% of 1920; each line width ≤ 80% of 1080.
Place in upper third (~22–40% height). Black stroke as v03.
Reuse silent picture.mp4 (no Omni remint). Gate then upload if PASS.
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
TARGET_DUR = 26.9  # match v02 pad
MAX_LINE_W = int(W * 0.80)  # ≤ 864
Y_TOP_FRAC = 0.22
Y_BOT_FRAC = 0.40
LINE_GAP = 28
STROKE = 6

WORK_V02 = HERE / "_work_v02"
WORK = HERE / "_work_v04"
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
    """Stack NOT (white) / YET (yellow), centred, Claude 5979587053 bands."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    lines = [("NOT", WHITE), ("YET", YELLOW)]
    lo, hi = 154, 280
    best = None
    while lo <= hi:
        size = (lo + hi) // 2
        font = ImageFont.truetype(FONT, size)
        box_y = draw.textbbox((0, 0), "Y", font=font, stroke_width=STROKE)
        gh = box_y[3] - box_y[1]
        pct = 100.0 * gh / H
        widths = []
        heights = []
        for word, _ in lines:
            b = draw.textbbox((0, 0), word, font=font, stroke_width=STROKE)
            widths.append(b[2] - b[0])
            heights.append(b[3] - b[1])
        max_w = max(widths)
        fits = max_w <= MAX_LINE_W
        in_band = 8.0 <= pct <= 10.0
        block_h = heights[0] + LINE_GAP + heights[1]
        # Prefer mid-band (~9%); take largest that fits bands
        if fits and in_band:
            best = (size, font, widths, heights, gh, pct, max_w, block_h)
            lo = size + 1
        elif (not fits) or pct > 10.0:
            hi = size - 1
        else:
            lo = size + 1
    if best is None:
        raise SystemExit("could not find two-line hook font size in 8–10% band with width ≤80%")
    size, font, widths, heights, gh, pct, max_w, block_h = best
    assert 8.0 <= pct <= 10.0, f"glyph pct {pct:.2f} out of band"
    assert max_w <= MAX_LINE_W, f"line width {max_w} > {MAX_LINE_W}"

    # Place block in upper third: top of first glyphs ~22%, bottom ≤~40%
    y0 = int(H * Y_TOP_FRAC)
    # textbbox top offset: drawing at y places the top of the ink near y for Arial Black
    # Prefer keeping bottom of second line near 40% if block is shorter
    y_bot_target = int(H * Y_BOT_FRAC)
    if y0 + block_h < y_bot_target:
        # nudge down slightly so block sits more in the 22–40 band centre
        slack = y_bot_target - (y0 + block_h)
        y0 = y0 + slack // 3  # keep toward upper third

    placed = []
    y = y0
    for (word, color), ww, hh in zip(lines, widths, heights):
        x = (W - ww) // 2
        draw.text((x, y), word, font=font, fill=color, stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
        placed.append({
            "word": word,
            "x": x,
            "y": y,
            "width": ww,
            "height": hh,
            "y_frac": round(y / H, 4),
            "y_bottom_frac": round((y + hh) / H, 4),
        })
        y += hh + LINE_GAP

    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)
    metrics = {
        "layout": "two_line_stack",
        "font_size": size,
        "stroke": STROKE,
        "line_gap": LINE_GAP,
        "glyph_h_px": gh,
        "glyph_pct_of_1920": round(pct, 2),
        "max_line_width": max_w,
        "max_line_width_pct_of_1080": round(100.0 * max_w / W, 2),
        "max_line_w_limit": MAX_LINE_W,
        "block_h_px": block_h,
        "block_top_frac": placed[0]["y_frac"],
        "block_bottom_frac": placed[-1]["y_bottom_frac"],
        "y_band_target": [Y_TOP_FRAC, Y_BOT_FRAC],
        "lines": placed,
        "text": "NOT / YET",
        "colors": {"NOT": "white", "YET": "yellow"},
        "claude_ref": "5979587053",
    }
    print("HOOK", json.dumps(metrics), flush=True)
    return metrics


def pad_picture(src: Path, dest: Path, target: float) -> float:
    src_s = dur(src)
    if src_s >= target - 0.01:
        shutil.copy2(src, dest)
        return dur(dest)
    pad = target - src_s
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
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = WORK / "_sheet_frames"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
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
    final = OUT / "friday_black_dwarf_why_none_yet_v04.mp4"
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
        "version": "v04",
        "duration_s": final_s,
        "vo_s": dur(VO),
        "picture_s": pic_s,
        "picture_src": str(PICTURE),
        "picture_note": f"reused silent picture.mp4; tpad clone to {TARGET_DUR}s (v02 end-hold pad)",
        "title_on_screen": "What Happens When the Last Star Dies?",
        "title_window_s": [title_start, title_end],
        "hook": "NOT / YET",
        "hook_metrics": hook_metrics,
        "hook_note": "two-line stack NOT white / YET yellow; 8–10% glyph; ≤80% width; upper third (Claude 5979587053)",
        "air": AIR,
        "claude_ref": "5979587053",
        "claude_thread": "5979587053",
        "orbit_pip_placeholder": False,
        "omni_remint": False,
        "vo": str(VO),
        "upload": False,
        "buffer": False,
        "replaces_scheduled_id": "mZ82-ijANk4",
    }
    meta_path = OUT / "friday_black_dwarf_why_none_yet_v04_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)

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
            str(REVIEW),
        ],
        capture_output=True,
        text=True,
    )
    gate_path = OUT / "friday_black_dwarf_why_none_yet_v04_gate.json"
    gate_body = gate.stdout or gate.stderr or "{}\n"
    gate_path.write_text(gate_body)
    print("GATE_STDOUT", gate.stdout, flush=True)
    if gate.stderr:
        print("GATE_STDERR", gate.stderr, flush=True)
    print("GATE_RC", gate.returncode, flush=True)

    frame0 = REVIEW / "friday_black_dwarf_why_none_yet_v04_frame0.png"
    extract_frame0(final, frame0)
    handoff_frame = HANDOFF / "bd_v04_frame0.png"
    shutil.copy2(frame0, handoff_frame)

    open_sheet = REVIEW / "friday_black_dwarf_why_none_yet_v04_open_sheet.jpg"
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
