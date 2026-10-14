#!/usr/bin/env python3
"""Monday Saturn Short v03 — J0104 end-card recut.

Keeps v02 picture 0–19.0 s and v02's audio stream bit for bit (copied, not
re-encoded). From 19.0 s to the end: graded PIA06193 Saturn with the long's
exact listing title and a yellow video id, inside the 16:9 centre band.
No Studio upload.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

OUT = HERE / "06_Final-Exports"
WORK = HERE / "_work_v03"
SRC = OUT / "monday_saturn_rings_already_falling_v02.mp4"
SATURN = HERE / "PIA06193_orig.jpg"
FINAL = OUT / "monday_saturn_rings_already_falling_v03.mp4"

W, H = 1080, 1920
FPS = 30
CUT = 19.0
LONG_TITLE = "How Long Do Saturn's Rings Have Left?"
LONG_ID = "55AEQwvs36g"
TITLE_ROWS = ["How Long Do", "Saturn's Rings", "Have Left?"]
AIR = "2026-10-12"
SELF_ID = "Qn56D6TOi0k"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
CREDIT_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
BAND_H = round(W * 9 / 16)  # 608
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)  # ~70 px, 11–12% of the 16:9 frame height


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def video_encode_args() -> list[str]:
    args = shorts_encode_args(fps=FPS)
    return args[: args.index("-c:a")]


def card_background(dest: Path) -> None:
    src = Image.open(SATURN).convert("RGB")
    # Saturn system sits in the upper third, clear of the text band.
    sat_w = int(W * 1.02)
    scale = sat_w / (src.width * 0.48)
    big = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    cx = big.width // 2
    cy = int(big.height * 0.45)
    bg = Image.new("RGB", (W, H), (0, 0, 0))
    x0 = cx - W // 2
    y0 = cy - int(H * 0.20)
    bg.paste(big.crop((x0, max(0, y0), x0 + W, max(0, y0) + H)), (0, max(0, -y0)))
    bg = ImageEnhance.Brightness(bg).enhance(0.62)
    bg = ImageEnhance.Contrast(bg).enhance(1.08)
    shade = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(shade)
    d.rectangle((0, BAND_Y0 - 40, W, BAND_Y0 + BAND_H + 40), fill=110)
    shade = shade.filter(ImageFilter.GaussianBlur(60))
    bg = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), bg, shade)
    bg.save(dest)


def text_overlay(dest: Path) -> dict:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    rows = [(r, WHITE) for r in TITLE_ROWS] + [(LONG_ID, YELLOW)]
    size = 10
    while True:
        font = ImageFont.truetype(FONT, size + 1)
        box = draw.textbbox((0, 0), "Hg", font=font)
        if box[3] - box[1] > LINE_H * 0.86:
            break
        size += 1
    font = ImageFont.truetype(FONT, size)
    gap = LINE_H + 8
    block = gap * len(rows) + 16
    y = BAND_Y0 + (BAND_H - block) // 2
    placed = []
    for i, (row, colour) in enumerate(rows):
        if i == len(rows) - 1:
            y += 16
        box = draw.textbbox((0, 0), row, font=font, stroke_width=5)
        x = (W - (box[2] - box[0])) // 2 - box[0]
        draw.text((x, y), row, font=font, fill=colour, stroke_width=5, stroke_fill=(0, 0, 0, 255))
        bb = draw.textbbox((x, y), row, font=font, stroke_width=5)
        placed.append({"text": row, "bbox": list(bb)})
        y += gap
    cfont = ImageFont.truetype(CREDIT_FONT, 22)
    credit = "NASA / JPL / Space Science Institute · PIA06193"
    cb = draw.textbbox((0, 0), credit, font=cfont)
    draw.text(((W - (cb[2] - cb[0])) // 2, H - 90), credit, font=cfont, fill=(200, 200, 200, 200))
    im.save(dest)
    return {"font_px": size, "line_h_px": LINE_H, "band": [BAND_Y0, BAND_Y0 + BAND_H], "rows": placed}


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    for p in (SRC, SATURN):
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
    total = dur(SRC)
    card_s = total - CUT
    bg = WORK / "card_bg.png"
    txt = WORK / "card_text.png"
    card_background(bg)
    layout = text_overlay(txt)
    for row in layout["rows"]:
        if row["bbox"][1] < layout["band"][0] or row["bbox"][3] > layout["band"][1] or row["bbox"][0] < 0 or row["bbox"][2] > W:
            raise SystemExit(f"text outside 16:9 band: {row}")

    frames = round(card_s * FPS) + 2
    push = (
        f"scale={W*2}:{H*2},zoompan=z='1+0.03*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS}"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(SRC),
            "-loop", "1", "-framerate", str(FPS), "-i", str(bg),
            "-loop", "1", "-framerate", str(FPS), "-i", str(txt),
            "-filter_complex",
            (
                f"[0:v]trim=0:{CUT:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1[head];"
                f"[1:v]{push},trim=0:{card_s:.3f},setpts=PTS-STARTPTS[bgv];"
                f"[2:v]format=rgba,trim=0:{card_s:.3f},setpts=PTS-STARTPTS[t];"
                f"[bgv][t]overlay=0:0,format=yuv420p,setsar=1[card];"
                f"[head][card]concat=n=2:v=1:a=0[v]"
            ),
            "-map", "[v]", "-map", "0:a",
            *video_encode_args(),
            "-c:a", "copy",
            "-t", f"{total:.3f}",
            "-movflags", "+faststart",
            str(FINAL),
        ]
    )
    meta = {
        "file": str(FINAL),
        "version": "v03",
        "job": "J0104",
        "source": str(SRC),
        "source_sha256": sha256(SRC),
        "sha256": sha256(FINAL),
        "duration_s": dur(FINAL),
        "source_duration_s": total,
        "kept_s": [0.0, CUT],
        "audio": "v02 audio stream copied unchanged",
        "end_card": {
            "start_s": CUT,
            "title": LONG_TITLE,
            "video_id": LONG_ID,
            "background": "PIA06193 (Cassini Saturn mosaic), graded, ~3% push",
            **layout,
        },
        "air": AIR,
    }
    (OUT / "monday_saturn_rings_already_falling_v03_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    gate = subprocess.run(
        [
            sys.executable,
            str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
            "check", str(FINAL), "--air-date", AIR, "--id", SELF_ID, "--json",
        ],
        capture_output=True,
        text=True,
    )
    print(gate.stdout)
    print(gate.stderr, file=sys.stderr)
    (OUT / "monday_saturn_rings_already_falling_v03_gate.json").write_text(gate.stdout or gate.stderr or "{}\n")
    if gate.returncode not in (0, 1):
        raise SystemExit(f"gate tool error {gate.returncode}")
    raise SystemExit(gate.returncode)


if __name__ == "__main__":
    main()
