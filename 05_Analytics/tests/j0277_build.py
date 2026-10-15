"""J0277: house type on the Orbit plates. Artwork stays in _desk, not git.

Shadow lift clears the Packaging near-black gate (luma < 26 on more than 30%
of the frame). Hook words are drawn after the lift so the type stays sharp.
"""
from pathlib import Path
import hashlib
import json
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/Users/benjaminoats/_desk/J0277-thumbnails")
SRC = Path("/Users/benjaminoats/_desk/J0271-thumbnails")
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
JOBS = [
    ("fermi", "Mo93x0fxB1Q", [("ALIENS", False), ("HIDING?", True)], (48, 36), 108),
    ("europa", "NbW5G1BpPY0", [("A HIDDEN", False), ("OCEAN", True)], (36, 40), 92),
    ("jwst", "ziKBPJ6FY0U", [("GALAXIES", False), ("TOO SOON?", True)], (36, 36), 96),
]


def lift(im: Image.Image, floor: float = 40, falloff: float = 90) -> Image.Image:
    arr = np.asarray(im).astype(np.float32)
    luma = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
    need = np.clip(floor - luma, 0, None)
    weight = np.clip((falloff - luma) / falloff, 0, 1)
    add = need * weight
    arr[:, :, 0] += add * 0.55
    arr[:, :, 1] += add * 0.70
    arr[:, :, 2] += add * 1.25
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main() -> None:
    manifest = []
    for slug, video, lines, pos, size in JOBS:
        art = ROOT / "art" / f"{slug}.png"
        im = lift(Image.open(art).convert("RGB"))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, size)
        x, y = pos
        for words, yellow in lines:
            draw.text(
                (x, y),
                words,
                font=font,
                fill="#FFD400" if yellow else "white",
                stroke_width=6,
                stroke_fill="#071127",
                anchor="lt",
            )
            y += int(size * 1.02)
        out = ROOT / f"{slug}_B_v02.jpg"
        im.save(out, quality=90, optimize=True)
        if out.stat().st_size >= 2_000_000:
            im.save(out, quality=82, optimize=True)
        if out.stat().st_size >= 2_000_000:
            raise SystemExit(f"{out} is over 2 MB")
        a = ROOT / f"{slug}_A_live.jpg"
        if not a.exists():
            shutil.copy(SRC / f"{slug}_A_live.jpg", a)
        sheet = Image.new("RGB", (760, 380), "#24334a")
        sd = ImageDraw.Draw(sheet)
        label = ImageFont.truetype(FONT, 16)
        for i, (path, title) in enumerate([(a, "A  live"), (out, "B  Orbit v02")]):
            ox = 15 + i * 380
            sd.text((ox, 8), title, font=label, fill="white")
            src = Image.open(path).convert("RGB")
            sheet.paste(src.resize((168, 94), Image.Resampling.LANCZOS), (ox, 40))
            sheet.paste(src.resize((360, 202), Image.Resampling.LANCZOS), (ox, 155))
        sheet_path = ROOT / f"{slug}_AB_v02.jpg"
        sheet.save(sheet_path, quality=94)
        manifest.append({
            "slug": slug,
            "video": video,
            "hook": " ".join(words for words, _ in lines),
            "art": str(art),
            "b": str(out),
            "a": str(a),
            "sheet": str(sheet_path),
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "bytes": out.stat().st_size,
            "dimensions": [1280, 720],
            "source": "Cursor image gen on J0277 (Codex out of usage); Arial Black after a shadow lift",
            "orbit": True,
            "status": "parked for Chief",
        })
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
