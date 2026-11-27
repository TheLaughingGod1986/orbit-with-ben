#!/usr/bin/env python3
"""Build 37 s vertical 9:16 social trailer (608x1080, 24 fps CFR) for OWB:064 from master v02.

Follows STUDIO_PLAYBOOK.md §12:
  - Vertical 30–60 s cut (37.0 s total: 32.85 s opening hook + 4.15 s "Full film on YouTube" end card)
  - Full-bleed centre-framed 9:16 crop (zero letterbox bars)
  - Ends cleanly on "Full film on YouTube" with exact title "Every Planet Explained in 12 Minutes"
  - Output written to NAS 11_Upload-Package/Trailer/ with verified SHA-256
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess as sp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes"
)
MASTER = NAS_FILM / "09_Final-Export/064_every_planet_explained_master_v02.mp4"
END_IMG_SRC = NAS_FILM / "03_Reference-Material/harvest_J3022_v01/PIA11141.jpg"
WORK = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch")) / "J3023_064_trailer_v01"
OUT_LOCAL = WORK / "064_every_planet_explained_trailer.mp4"
OUT_NAS = NAS_FILM / "11_Upload-Package/Trailer/064_every_planet_explained_trailer.mp4"

W, H = 608, 1080
FPS = 24
CLIP_END = 32.85   # Clean sentence end after Colombo 1965 beat (R04b out)
CARD_DUR = 4.15    # Total = 37.00 s


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-1500:])


def make_end_card_png(dest: Path) -> None:
    with Image.open(END_IMG_SRC) as raw:
        im = raw.convert("RGB")
    # Crop centre 9:16 vertical slice of real Cassini Saturn
    sw, sh = im.size
    target_w = int(sh * W / H)
    ox = (sw - target_w) // 2
    bg = im.crop((ox, 0, ox + target_w, sh)).resize((W, H), Image.Resampling.LANCZOS)
    # Darken slightly for crisp legible house typography
    overlay = Image.new("RGBA", (W, H), (8, 15, 30, 145))
    canvas = Image.alpha_composite(bg.convert("RGBA"), overlay)
    dr = ImageDraw.Draw(canvas)

    f_big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    f_med = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
    f_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)

    # Top title block
    lines = [
        ("EVERY PLANET", f_big, (255, 224, 0, 255), 250),
        ("EXPLAINED", f_big, (255, 255, 255, 255), 312),
        ("IN 12 MINUTES", f_med, (215, 232, 252, 255), 382),
        ("Mercury to Neptune", f_sm, (185, 210, 240, 255), 432),
    ]
    for text, font, col, y in lines:
        bb = dr.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        dr.text(((W - tw) // 2, y), text, font=font, fill=col, stroke_width=2, stroke_fill=(6, 12, 22, 255))

    # Bottom pill: "Full film on YouTube"
    pill_text = "Full film on YouTube"
    bb = dr.textbbox((0, 0), pill_text, font=f_med)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    bx0, by0, bx1, by1 = (W - tw) // 2 - 34, 710, (W + tw) // 2 + 34, 710 + th + 36
    dr.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(14, 26, 48, 235), outline=(255, 224, 0, 255), width=3)
    dr.text(((W - tw) // 2 - bb[0], by0 + 18 - bb[1]), pill_text, font=f_med, fill=(255, 255, 255, 255))

    ch = "Orbit With Ben"
    bb2 = dr.textbbox((0, 0), ch, font=f_sm)
    dr.text(((W - (bb2[2] - bb2[0])) // 2, by1 + 26), ch, font=f_sm, fill=(255, 224, 0, 240))

    canvas.convert("RGB").save(dest, "PNG")


def main() -> None:
    assert MASTER.exists(), f"Master v02 missing: {MASTER}"
    WORK.mkdir(parents=True, exist_ok=True)
    card_png = WORK / "end_card.png"
    make_end_card_png(card_png)

    part1 = WORK / "part1.mp4"
    part2 = WORK / "part2.mp4"
    # Part 1: 0..32.85 s full-bleed centre crop of master v02
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(MASTER), "-t", f"{CLIP_END:.3f}",
        "-vf", f"crop=ih*608/1080:ih,scale={W}:{H},setsar=1,fps={FPS}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        str(part1),
    ])

    # Part 2: 4.15 s "Full film on YouTube" end card with gentle music bed tail from master v02 (690..694.15 s)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-t", f"{CARD_DUR:.3f}", "-i", str(card_png),
        "-ss", "690.0", "-t", f"{CARD_DUR:.3f}", "-i", str(MASTER),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", f"scale={W}:{H},setsar=1,fps={FPS},fade=t=in:st=0:d=0.35:color=#080f1e,fade=t=out:st={CARD_DUR-0.6:.3f}:d=0.6:color=#080f1e",
        "-af", f"afade=t=in:st=0:d=0.35,afade=t=out:st={CARD_DUR-0.8:.3f}:d=0.8",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        str(part2),
    ])

    lst = WORK / "concat.txt"
    lst.write_text(f"file '{part1}'\nfile '{part2}'\n", encoding="utf-8")
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-movflags", "+faststart", str(OUT_LOCAL),
    ])

    OUT_NAS.parent.mkdir(parents=True, exist_ok=True)
    local_sha = sha256(OUT_LOCAL)
    shutil.copy2(OUT_LOCAL, OUT_NAS)
    nas_sha = sha256(OUT_NAS)
    assert local_sha == nas_sha, "Trailer NAS checksum mismatch!"

    info = json.loads(sp.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,avg_frame_rate,codec_type",
        "-of", "json", str(OUT_NAS),
    ], text=True))
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    print(json.dumps({
        "file": str(OUT_NAS),
        "sha256": nas_sha,
        "bytes": OUT_NAS.stat().st_size,
        "width": v["width"],
        "height": v["height"],
        "avg_frame_rate": v["avg_frame_rate"],
        "duration": float(info["format"]["duration"]),
    }, indent=2))


if __name__ == "__main__":
    main()
