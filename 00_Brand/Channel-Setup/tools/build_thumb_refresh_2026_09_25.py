#!/usr/bin/env python3
"""Build Batch A/B thumbnail refresh — PREPARE ONLY (25 Sep 2026).

Does not upload. Uses house compose (yellow hook / white rest, no Orbit).
Plates: scrubbed current custom thumb when no Orbit (and subject fits);
crop-away Orbit when a clean subject remains; else NEEDS PLATE.

Font: Arial Black on macOS, else Liberation Sans Bold / DejaVu Sans Bold.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[3]
REFRESH = ROOT / "00_Brand/Channel-Setup/audits/THUMBNAIL_TITLE_AUDIT_2026-09-25/refresh"
ART = Path("/opt/cursor/artifacts/thumb-refresh-2026-09-25")
PREVIEW = ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"

# Prefer Arial Black; fall back for Linux cloud agents.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Arial Black.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def resolve_font() -> str:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    raise SystemExit("No heavy sans font found (Arial Black / Liberation / DejaVu Bold)")


FONT_PATH = resolve_font()

# --- Short house constants (from build_yellow_white_short_thumbs_v04) ---
SW, SH = 1080, 1920
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STROKE = 4
BAR = int(SH * 0.09)

# --- Long house constants (from build_melodysheep_long_thumbs_v01) ---
LW, LH = 1280, 720
STROKE_TITLE = 5
STROKE_SUB = 3

BATCH_A = [
    {
        "id": "DN4L1DkerMM",
        "old_text": "THIS OCEAN / SHOULDN'T EXIST (wrong Europa plate)",
        "lines": ["RUNNING OUT OF", "STARS"],
        "yellow": {"STARS"},
        "hero": 1,
        "subject_ok": False,  # Europa ice ≠ stars
        "note": "Current thumb is Europa ocean — wrong subject for stars Short",
    },
    {
        "id": "PV50PX-bE4g",
        "old_text": "(Orbit reference grid / no hook)",
        "lines": ["NO", "LIGHT"],
        "yellow": {"NO"},
        "hero": 0,
        "subject_ok": False,
        "note": "Current thumb is Orbit-only",
    },
    {
        "id": "l1d1ypHxLk0",
        "old_text": "next to / 13.8 billion",
        "lines": ["TOO", "EARLY"],
        "yellow": {"EARLY"},
        "hero": 1,
        "subject_ok": False,
        "note": "Current thumb is Orbit + poetic type",
    },
    {
        "id": "M-VN84HCNls",
        "old_text": "carbon under pressure",
        "lines": ["DIAMOND", "PLANETS"],
        "yellow": {"DIAMOND"},
        "hero": 0,
        "subject_ok": False,
        "note": "Current thumb has Orbit on crystals",
    },
    {
        "id": "68uTDP2esso",
        "old_text": "300 million years / after big bang",
        "lines": ["A HIDDEN", "SECRET"],
        "yellow": {"SECRET"},
        "hero": 1,
        "subject_ok": False,
        "note": "Current thumb has Orbit; proposed title note only (not applied)",
        "proposed_title_note": "The Early Universe Is Hiding a Massive Secret",
    },
    {
        "id": "SC2WGTl_V5Q",
        "old_text": "watch the full film (Orbit)",
        "lines": ["GLASS", "RAIN"],
        "yellow": {"GLASS"},
        "hero": 0,
        "subject_ok": False,
        "note": "Current thumb has Orbit on planet",
    },
    {
        "id": "9lLZMy8rBJo",
        "old_text": "stage is empty",
        "lines": ["WHAT", "REMAINS?"],
        "yellow": {"REMAINS?"},
        "hero": 1,
        "subject_ok": True,
        "note": "Ringed planet plate, no Orbit — scrub text, reuse",
    },
    {
        "id": "CkSECfUfH2Y",
        "old_text": "what if you / were here?",
        "lines": ["SKY GOING", "DARK"],
        "yellow": {"DARK"},
        "hero": 1,
        "subject_ok": True,
        "note": "Asteroid / red world plate, no Orbit — scrub text, reuse",
    },
]

BATCH_B = [
    {
        "id": "Yk1tLh23rko",
        "title_name": "Neutron Star",
        "old_text": "YOUR BODY / NEAR A NEUTRON STAR",
        "variants": [
            {"v": "B", "title": ["CRUSHED", "FLAT"], "yellow": {"FLAT"}, "sub": ""},
            {"v": "C", "title": ["YOU'D BE", "FLAT"], "yellow": {"FLAT"}, "sub": ""},
        ],
        "plate_mode": "scrub",  # no Orbit
    },
    {
        "id": "REXYxuLOBoI",
        "title_name": "Last Star",
        "old_text": "WHEN THE LAST STAR DIES",
        "variants": [
            {"v": "B", "title": ["LAST", "LIGHT"], "yellow": {"LIGHT"}, "sub": ""},
            {"v": "C", "title": ["THEN", "DARK"], "yellow": {"DARK"}, "sub": ""},
        ],
        "plate_mode": "scrub",  # prefer red body; asteroid field is weak but usable interim
        "plate_note": "B wants one fading red dwarf on black — current is asteroid field; scrubbed as interim",
    },
    {
        "id": "NbW5G1BpPY0",
        "title_name": "Europa",
        "old_text": "LIFE UNDER THE ICE / MORE WATER THAN EARTH",
        "variants": [
            {"v": "B", "title": ["A HIDDEN", "OCEAN"], "yellow": {"OCEAN"}, "sub": ""},
            {"v": "C", "title": ["OCEAN", "BELOW"], "yellow": {"BELOW"}, "sub": ""},
        ],
        "plate_mode": "scrub",
    },
    {
        "id": "3xrxdmaOwJI",
        "title_name": "Black Hole",
        "old_text": "FALLING IN? (with Orbit)",
        "variants": [
            {"v": "B", "title": ["NO WAY", "OUT"], "yellow": {"OUT"}, "sub": ""},
            {"v": "C", "title": ["FALLING", "IN?"], "yellow": {"FALLING"}, "sub": ""},
        ],
        "plate_mode": "crop_right_hard",
        "force_needs_plate": True,
        "force_reason": "Orbit arm/glove remains on current thumb even after right-half crop; need AI Studio black-hole-only plate",
    },
    {
        "id": "Mo93x0fxB1Q",
        "title_name": "Fermi",
        "old_text": "WHERE IS EVERYBODY? (with Orbit)",
        "variants": [
            {"v": "B", "title": ["WHERE IS", "EVERYONE?"], "yellow": {"EVERYONE?"}, "sub": ""},
            {"v": "C", "title": ["SILENCE"], "yellow": {"SILENCE"}, "sub": ""},
        ],
        "plate_mode": "crop_left_hard",  # dish + galaxy; drop Orbit on right
    },
    {
        "id": "ojk-dfOpAmw",
        "title_name": "Andromeda",
        "old_text": "COMING FOR US?",
        "variants": [
            {"v": "REP", "title": ["WHEN THEY", "MEET"], "yellow": {"MEET"}, "sub": ""},
        ],
        "plate_mode": "scrub",
        "replace": True,
    },
]


def yellow_key(word: str) -> str:
    return word.upper().strip("?")


def orange_orbit_score(im: Image.Image) -> float:
    """Rough fraction of warm-orange pixels (Orbit shell) in the centre band."""
    small = im.convert("RGB").resize((90, 160), Image.Resampling.BILINEAR)
    w, h = small.size
    band = small.crop((w // 4, h // 5, 3 * w // 4, 4 * h // 5))
    pix = list(band.getdata())
    n = len(pix) or 1
    hits = 0
    for r, g, b in pix:
        if r > 140 and 40 < g < 160 and b < 90 and r > g + 30 and r > b + 50:
            hits += 1
    return hits / n


def scrub_text_band(im: Image.Image, kind: str) -> Image.Image:
    """Obliterate old type in the centre band; keep edge subject for atmosphere.

    Soft blur alone left ghost text readable. Core band is solid black; only
    the outer rim is feathered into the plate.
    """
    im = im.convert("RGB").copy()
    w, h = im.size
    corner = im.crop((0, 0, max(8, w // 20), max(8, h // 20)))
    mean = ImageStat.Stat(corner).mean
    fill = tuple(max(0, min(28, int(c))) for c in mean[:3])
    overlay = Image.new("RGB", (w, h), fill)
    # Soft outer mask
    soft = Image.new("L", (w, h), 0)
    dsoft = ImageDraw.Draw(soft)
    # Hard core mask (fully opaque)
    hard = Image.new("L", (w, h), 0)
    dhard = ImageDraw.Draw(hard)
    if kind == "short":
        dsoft.rectangle((0, int(h * 0.28), w, int(h * 0.72)), fill=255)
        soft = soft.filter(ImageFilter.GaussianBlur(28))
        dhard.rectangle((0, int(h * 0.34), w, int(h * 0.66)), fill=255)
    else:
        dsoft.rectangle((int(w * 0.02), int(h * 0.04), int(w * 0.98), int(h * 0.86)), fill=255)
        soft = soft.filter(ImageFilter.GaussianBlur(22))
        dhard.rectangle((int(w * 0.04), int(h * 0.08), int(w * 0.96), int(h * 0.82)), fill=255)
    mask = Image.composite(hard, soft, hard)
    return Image.composite(overlay, im, mask)


def extract_short_plate(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # oar2 is already 9:16; maxres Shorts dumps are 16:9 letterboxed — take centre column.
    if w > h:
        col_w = int(h * 9 / 16)
        x0 = (w - col_w) // 2
        im = im.crop((x0, 0, x0 + col_w, h))
    return ImageOps.fit(im, (SW, SH), Image.Resampling.LANCZOS)


def extract_long_plate(src: Path, mode: str) -> Image.Image:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if mode in ("crop_right", "crop_right_hard"):
        # Hard crop keeps only the black-hole half (Orbit sits left).
        x0 = int(w * (0.62 if mode == "crop_right_hard" else 0.38))
        im = im.crop((x0, 0, w, h))
    elif mode in ("crop_left", "crop_left_hard"):
        x1 = int(w * (0.55 if mode == "crop_left_hard" else 0.72))
        im = im.crop((0, 0, x1, h))
    im = ImageOps.fit(im, (LW, LH), Image.Resampling.LANCZOS)
    return scrub_text_band(im, "long")


def cover_plate_short(plate: Image.Image) -> Image.Image:
    im = plate.convert("RGB")
    if im.size != (SW, SH):
        im = ImageOps.fit(im, (SW, SH), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.08)
    overlay = Image.new("RGB", (SW, SH), (0, 0, 0))
    mask = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(mask).rectangle((0, int(SH * 0.28), SW, int(SH * 0.72)), fill=175)
    mask = mask.filter(ImageFilter.GaussianBlur(80))
    im = Image.composite(Image.blend(im, overlay, 0.50), im, mask)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, SW, BAR), fill=BLACK)
    draw.rectangle((0, SH - BAR, SW, SH), fill=BLACK)
    return im


def cover_plate_long(plate: Image.Image) -> Image.Image:
    im = plate.convert("RGB")
    if im.size != (LW, LH):
        im = ImageOps.fit(im, (LW, LH), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.05)
    overlay = Image.new("RGB", (LW, LH), (0, 0, 0))
    mask = Image.new("L", (LW, LH), 0)
    ImageDraw.Draw(mask).rectangle((0, int(LH * 0.22), LW, int(LH * 0.82)), fill=120)
    mask = mask.filter(ImageFilter.GaussianBlur(48))
    return Image.composite(Image.blend(im, overlay, 0.28), im, mask)


def fit_font(draw, text: str, max_w: int, start: int, stroke: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 28:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 28)


def draw_line_words(draw, y, words, yellow_words, font, stroke, canvas_w, align_left_x=None):
    space = draw.textbbox((0, 0), " ", font=font, stroke_width=stroke)[2]
    widths = []
    for w in words:
        b = draw.textbbox((0, 0), w, font=font, stroke_width=stroke)
        widths.append(b[2] - b[0])
    total = sum(widths) + space * (len(words) - 1)
    x = align_left_x if align_left_x is not None else (canvas_w - total) // 2
    yellow_norm = {yellow_key(yw) for yw in yellow_words}
    for w, ww in zip(words, widths):
        color = YELLOW if yellow_key(w) in yellow_norm else WHITE
        draw.text((x + 3, y + 5), w, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        draw.text((x, y), w, font=font, fill=color, stroke_width=stroke, stroke_fill=BLACK)
        x += ww + space


def compose_short(job: dict, plate: Image.Image, out: Path) -> dict:
    im = cover_plate_short(plate)
    draw = ImageDraw.Draw(im)
    lines = job["lines"]
    hero = int(job.get("hero", 1))
    max_w = int(SW * 0.90)
    starts = [168 if i == hero else 102 for i in range(len(lines))]
    fonts = [fit_font(draw, line, max_w, start=s, stroke=STROKE) for line, s in zip(lines, starts)]
    hero_px = int(getattr(fonts[hero], "size", 44))
    fonts = [
        font if i == hero else fit_font(draw, line, max_w, start=min(int(getattr(font, "size", 44)), int(hero_px * 0.62)), stroke=STROKE)
        for i, (line, font) in enumerate(zip(lines, fonts))
    ]
    heights = []
    for line, font in zip(lines, fonts):
        b = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE)
        heights.append(b[3] - b[1])
    gap = 14
    block = sum(heights) + gap * (len(lines) - 1)
    y = max(int(SH * 0.36), min((SH - block) // 2, int(SH * 0.64) - block))
    for line, font, hh in zip(lines, fonts, heights):
        draw_line_words(draw, y, line.split(" "), job["yellow"], font, STROKE, SW)
        y += hh + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=93, optimize=True)
    return {"id": job["id"], "file": str(out), "hook": " / ".join(lines), "yellow": sorted(job["yellow"])}


def compose_long(job_id: str, variant: dict, plate: Image.Image, out: Path) -> dict:
    im = cover_plate_long(plate)
    draw = ImageDraw.Draw(im)
    title_lines = variant["title"]
    max_w = int(LW * 0.90)
    fonts = [
        fit_font(draw, line, max_w, start=96 if i == len(title_lines) - 1 else 78, stroke=STROKE_TITLE)
        for i, line in enumerate(title_lines)
    ]
    hero = fonts[-1]
    fonts = [
        font
        if i == len(fonts) - 1
        else fit_font(draw, line, max_w, start=min(int(getattr(hero, "size", 72) * 0.72), 78), stroke=STROKE_TITLE)
        for i, (line, font) in enumerate(zip(title_lines, fonts))
    ]
    heights = []
    for line, font in zip(title_lines, fonts):
        b = draw.textbbox((0, 0), line, font=font, stroke_width=STROKE_TITLE)
        heights.append(b[3] - b[1])
    sub = (variant.get("sub") or "").strip()
    gap = 8
    block = sum(heights) + gap * (len(title_lines) - 1)
    if sub:
        sub_font = fit_font(draw, sub, max_w, start=34, stroke=STROKE_SUB)
        sub_h = draw.textbbox((0, 0), sub, font=sub_font, stroke_width=STROKE_SUB)
        sub_h = sub_h[3] - sub_h[1]
        block += 16 + sub_h
    else:
        sub_font = None
        sub_h = 0
    y = int(LH * 0.50 - block / 2)
    y = max(int(LH * 0.12), min(y, int(LH * 0.82) - block))
    for line, font, hh in zip(title_lines, fonts, heights):
        draw_line_words(draw, y, line.split(" "), variant["yellow"], font, STROKE_TITLE, LW)
        y += hh + gap
    if sub and sub_font:
        y += 16 - gap
        draw_line_words(draw, y, sub.split(" "), set(), sub_font, STROKE_SUB, LW)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=93, optimize=True)
    return {
        "id": job_id,
        "variant": variant["v"],
        "file": str(out),
        "title": " / ".join(title_lines),
        "yellow": sorted(variant["yellow"]),
    }


def find_old_short(vid: str) -> Path | None:
    for name in (f"oar2_{vid}.jpg", f"old_{vid}.jpg"):
        p = REFRESH / "old" / name
        if p.exists():
            return p
    return None


def find_old_long(vid: str) -> Path | None:
    p = REFRESH / "old" / f"old_{vid}.jpg"
    return p if p.exists() else None


def run_preview(kind: str, thumb: Path, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(PREVIEW), kind, str(thumb), "--out", str(out)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print("PREVIEW FAIL", thumb, r.stderr)
        return False
    print("preview", out)
    return True


def build_contact_sheet(rows: list[dict], out: Path) -> None:
    """One row per id: label | old | new(s) | phone preview tile."""
    cell_h = 220
    label_w = 220
    gap = 10
    built_rows = []
    for row in rows:
        cells = []
        # label
        lab = Image.new("RGB", (label_w, cell_h), (24, 24, 28))
        d = ImageDraw.Draw(lab)
        font = ImageFont.truetype(FONT_PATH, 18)
        text = f"{row['id']}\n{row.get('kind','')}\n{row.get('status','')}"
        d.multiline_text((8, 20), text, fill=(240, 240, 240), font=font, spacing=6)
        cells.append(lab)

        def fit(path: Path | None, size=(200, 200)):
            if not path or not Path(path).exists():
                blank = Image.new("RGB", size, (40, 40, 45))
                ImageDraw.Draw(blank).text((20, size[1] // 2 - 10), "—", fill=(180, 180, 180), font=font)
                return blank
            im = Image.open(path).convert("RGB")
            return ImageOps.contain(im, size, Image.Resampling.LANCZOS)

        cells.append(fit(Path(row["old"]) if row.get("old") else None, (160, 200)))
        news = row.get("news") or []
        if not news:
            cells.append(fit(None, (160, 200)))
        else:
            for n in news[:3]:
                cells.append(fit(Path(n), (160, 200)))
        if row.get("preview"):
            cells.append(fit(Path(row["preview"]), (220, 200)))
        else:
            cells.append(fit(None, (220, 200)))
        # pad to equal height
        row_im = Image.new("RGB", (sum(c.width for c in cells) + gap * (len(cells) + 1), cell_h + 2 * gap), (12, 12, 14))
        x = gap
        for c in cells:
            y = gap + (cell_h - c.height) // 2
            row_im.paste(c, (x, y))
            x += c.width + gap
        built_rows.append(row_im)

    max_w = max(r.width for r in built_rows)
    total_h = sum(r.height for r in built_rows) + gap
    sheet = Image.new("RGB", (max_w, total_h), (12, 12, 14))
    y = 0
    for r in built_rows:
        sheet.paste(r, (0, y))
        y += r.height
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=90)
    print("contact", out)


def main() -> None:
    REFRESH.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (REFRESH / "shorts").mkdir(exist_ok=True)
    (REFRESH / "longs").mkdir(exist_ok=True)
    (REFRESH / "plates").mkdir(exist_ok=True)
    (REFRESH / "previews").mkdir(exist_ok=True)
    (REFRESH / "contact").mkdir(exist_ok=True)

    log_rows = []
    contact_rows = []
    needs_plate = []

    print(f"font={FONT_PATH}")

    # ---- Batch A ----
    for job in BATCH_A:
        vid = job["id"]
        old = find_old_short(vid)
        if not old:
            print("MISSING old short", vid)
            needs_plate.append(vid)
            log_rows.append(
                {
                    "id": vid,
                    "batch": "A",
                    "old_text": job["old_text"],
                    "new_text": " / ".join(job["lines"]),
                    "plate_source": "MISSING old thumb",
                    "status": "NEEDS PLATE",
                    "preview": None,
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                }
            )
            continue

        plate_img = extract_short_plate(old)
        score = orange_orbit_score(plate_img)
        subject_ok = job["subject_ok"] and score < 0.04
        plate_path = REFRESH / "plates" / f"plate_{vid}.jpg"

        if not subject_ok:
            needs_plate.append(vid)
            reason = job["note"]
            if score >= 0.04:
                reason += f" (orbit_score={score:.3f})"
            log_rows.append(
                {
                    "id": vid,
                    "batch": "A",
                    "old_text": job["old_text"],
                    "new_text": " / ".join(job["lines"]),
                    "yellow": sorted(job["yellow"]),
                    "plate_source": "AI Studio needed",
                    "status": "NEEDS PLATE",
                    "reason": reason,
                    "preview": None,
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                    "proposed_title_note": job.get("proposed_title_note"),
                }
            )
            contact_rows.append(
                {
                    "id": vid,
                    "kind": "short A",
                    "status": "NEEDS PLATE",
                    "old": str(old),
                    "news": [],
                    "preview": None,
                }
            )
            print(f"NEEDS PLATE {vid}: {reason}")
            continue

        plate_scrubbed = scrub_text_band(plate_img, "short")
        plate_scrubbed.save(plate_path, quality=92)
        out = REFRESH / "shorts" / f"cover_{vid}.jpg"
        compose_short(job, plate_scrubbed, out)
        prev = REFRESH / "previews" / f"short_{vid}.jpg"
        ok = run_preview("short", out, prev)
        shutil.copy2(out, ART / f"short_{vid}.jpg")
        log_rows.append(
            {
                "id": vid,
                "batch": "A",
                "old_text": job["old_text"],
                "new_text": " / ".join(job["lines"]),
                "yellow": sorted(job["yellow"]),
                "plate_source": f"current bg scrubbed from {old.name}",
                "status": "BUILT" + (" preview PASS" if ok else " preview FAIL"),
                "preview": str(prev),
                "file": str(out),
                "date_applied": "",
                "impressions": "",
                "ctr": "",
            }
        )
        contact_rows.append(
            {
                "id": vid,
                "kind": "short A",
                "status": "PASS" if ok else "FAIL",
                "old": str(old),
                "news": [str(out)],
                "preview": str(prev),
            }
        )

    # ---- Batch B ----
    for job in BATCH_B:
        vid = job["id"]
        old = find_old_long(vid)
        if not old:
            needs_plate.append(vid)
            log_rows.append(
                {
                    "id": vid,
                    "batch": "B",
                    "old_text": job["old_text"],
                    "new_text": "; ".join(" / ".join(v["title"]) for v in job["variants"]),
                    "plate_source": "MISSING old thumb",
                    "status": "NEEDS PLATE",
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                }
            )
            continue

        mode = job["plate_mode"]
        if job.get("force_needs_plate"):
            needs_plate.append(vid)
            log_rows.append(
                {
                    "id": vid,
                    "batch": "B",
                    "old_text": job["old_text"],
                    "new_text": "; ".join(" / ".join(v["title"]) for v in job["variants"]),
                    "plate_source": "AI Studio needed",
                    "status": "NEEDS PLATE",
                    "reason": job.get("force_reason", "forced"),
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                }
            )
            contact_rows.append(
                {
                    "id": vid,
                    "kind": f"long {job['title_name']}",
                    "status": "NEEDS PLATE",
                    "old": str(old),
                    "news": [],
                    "preview": None,
                }
            )
            print(f"NEEDS PLATE long {vid}: {job.get('force_reason')}")
            continue

        plate = extract_long_plate(old, mode)
        # After crop, re-check Orbit
        score = orange_orbit_score(ImageOps.fit(plate, (90, 160), Image.Resampling.BILINEAR))
        news = []
        # Any remaining Orbit after crop/scrub → Ben needs a clean AI Studio plate.
        if score >= 0.025:
            needs_plate.append(vid)
            log_rows.append(
                {
                    "id": vid,
                    "batch": "B",
                    "old_text": job["old_text"],
                    "new_text": "; ".join(" / ".join(v["title"]) for v in job["variants"]),
                    "plate_source": "AI Studio needed",
                    "status": "NEEDS PLATE",
                    "reason": f"Orbit remains after {mode} (score={score:.3f})",
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                }
            )
            contact_rows.append(
                {
                    "id": vid,
                    "kind": f"long {job['title_name']}",
                    "status": "NEEDS PLATE",
                    "old": str(old),
                    "news": [],
                    "preview": None,
                }
            )
            print(f"NEEDS PLATE long {vid} orbit_score={score:.3f}")
            continue

        plate_path = REFRESH / "plates" / f"plate_{vid}_{mode}.jpg"
        plate.save(plate_path, quality=92)
        plate_src = f"current bg ({mode}) from {old.name}"
        if job.get("plate_note"):
            plate_src += f" — {job['plate_note']}"

        for variant in job["variants"]:
            out = REFRESH / "longs" / f"cover_{variant['v']}_{vid}.jpg"
            compose_long(vid, variant, plate, out)
            prev = REFRESH / "previews" / f"long_{variant['v']}_{vid}.jpg"
            ok = run_preview("long", out, prev)
            shutil.copy2(out, ART / f"long_{variant['v']}_{vid}.jpg")
            news.append(str(out))
            log_rows.append(
                {
                    "id": vid,
                    "batch": "B",
                    "variant": variant["v"],
                    "old_text": job["old_text"],
                    "new_text": " / ".join(variant["title"]),
                    "yellow": sorted(variant["yellow"]),
                    "plate_source": plate_src,
                    "status": "BUILT" + (" preview PASS" if ok else " preview FAIL"),
                    "preview": str(prev),
                    "file": str(out),
                    "replace": bool(job.get("replace")),
                    "date_applied": "",
                    "impressions": "",
                    "ctr": "",
                }
            )

        contact_rows.append(
            {
                "id": vid,
                "kind": f"long {job['title_name']}",
                "status": "BUILT",
                "old": str(old),
                "news": news,
                "preview": str(REFRESH / "previews" / f"long_{job['variants'][0]['v']}_{vid}.jpg"),
            }
        )

    # Contact sheet (split if tall)
    contact1 = REFRESH / "contact" / "contact_sheet_page1.jpg"
    build_contact_sheet(contact_rows, contact1)
    shutil.copy2(contact1, ART / "contact_sheet_page1.jpg")

    manifest = {
        "version": "thumb_refresh_2026-09-25",
        "font": FONT_PATH,
        "note": "PREPARE ONLY — do not upload. Ben applies in Studio.",
        "needs_plate": needs_plate,
        "rows": log_rows,
    }
    (REFRESH / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    shutil.copy2(REFRESH / "MANIFEST.json", ART / "MANIFEST.json")
    print("NEEDS PLATE:", needs_plate)
    print("wrote", REFRESH / "MANIFEST.json")


if __name__ == "__main__":
    main()
