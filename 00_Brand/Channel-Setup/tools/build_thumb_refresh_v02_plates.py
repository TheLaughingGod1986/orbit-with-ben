#!/usr/bin/env python3
"""Rebuild thumb refresh on Studio plate picks — full-bleed, no black box (26 Sep 2026).

Plates: orbit-thumb-plates/picks/<id>_1.jpg (rank 1 = best).
House type: yellow hook / white rest, heavy outline, Liberation/Arial Black.
Does not upload.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
PICKS = ROOT / "orbit-thumb-plates/picks"
REFRESH = ROOT / "00_Brand/Channel-Setup/audits/THUMBNAIL_TITLE_AUDIT_2026-09-25/refresh"
ART = Path("/opt/cursor/artifacts/thumb-refresh-2026-09-25")
PREVIEW = ROOT / "00_Brand/Channel-Setup/tools/thumb_preview.py"

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
    raise SystemExit("No heavy sans font found")


FONT_PATH = resolve_font()
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SW, SH = 1080, 1920
LW, LH = 1280, 720
STROKE_S = 5
STROKE_L = 6


def yellow_key(w: str) -> str:
    return w.upper().strip("?")


def fit_canvas(src: Path, tw: int, th: int) -> Image.Image:
    im = Image.open(src).convert("RGB")
    return ImageOps.fit(im, (tw, th), Image.Resampling.LANCZOS)


def soft_readability(im: Image.Image, strength: float = 0.22) -> Image.Image:
    """Gentle centre darken only — full-bleed picture stays visible (no solid black box)."""
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.04)
    w, h = im.size
    overlay = Image.new("RGB", (w, h), (0, 0, 0))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse(
        (-int(w * 0.1), int(h * 0.15), int(w * 1.1), int(h * 0.85)),
        fill=int(255 * strength / 0.35),
    )
    mask = mask.filter(ImageFilter.GaussianBlur(max(40, w // 12)))
    return Image.composite(Image.blend(im, overlay, strength), im, mask)


def fit_font(draw, text: str, max_w: int, start: int, stroke: int, min_size: int = 36) -> ImageFont.FreeTypeFont:
    size = start
    while size > min_size:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bbox[2] - bbox[0] <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, min_size)


def line_wh(draw, text, font, stroke):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    return b[2] - b[0], b[3] - b[1]


def draw_words(draw, y, words, yellow_words, font, stroke, canvas_w):
    space = draw.textbbox((0, 0), " ", font=font, stroke_width=stroke)[2]
    widths = [line_wh(draw, w, font, stroke)[0] for w in words]
    total = sum(widths) + space * max(0, len(words) - 1)
    x = (canvas_w - total) // 2
    yn = {yellow_key(w) for w in yellow_words}
    for w, ww in zip(words, widths):
        color = YELLOW if yellow_key(w) in yn else WHITE
        draw.text((x + 3, y + 4), w, font=font, fill=BLACK, stroke_width=stroke, stroke_fill=BLACK)
        draw.text((x, y), w, font=font, fill=color, stroke_width=stroke, stroke_fill=BLACK)
        x += ww + space


def compose_short(plate: Path, lines: list[str], yellow: set[str], out: Path, hero: int = 1) -> dict:
    im = soft_readability(fit_canvas(plate, SW, SH), strength=0.20)
    draw = ImageDraw.Draw(im)
    max_w = int(SW * 0.88)  # ≥60% frame width target; aim bigger
    starts = [188 if i == hero else 118 for i in range(len(lines))]
    fonts = [fit_font(draw, line, max_w, start=s, stroke=STROKE_S, min_size=52) for line, s in zip(lines, starts)]
    hero_px = int(getattr(fonts[hero], "size", 80))
    fonts = [
        font
        if i == hero
        else fit_font(draw, line, max_w, start=min(int(getattr(font, "size", 60)), int(hero_px * 0.62)), stroke=STROKE_S, min_size=48)
        for i, (line, font) in enumerate(zip(lines, fonts))
    ]
    heights = [line_wh(draw, line, font, STROKE_S)[1] for line, font in zip(lines, fonts)]
    gap = 16
    block = sum(heights) + gap * (len(lines) - 1)
    # Vertical centre, inside 16:9 centre-crop band
    y = max(int(SH * 0.36), min((SH - block) // 2, int(SH * 0.64) - block))
    for line, font, hh in zip(lines, fonts, heights):
        draw_words(draw, y, line.split(), yellow, font, STROKE_S, SW)
        y += hh + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=94, optimize=True)
    return {"file": str(out), "hook": " / ".join(lines), "plate": str(plate)}


def compose_long(plate: Path, lines: list[str], yellow: set[str], out: Path) -> dict:
    im = soft_readability(fit_canvas(plate, LW, LH), strength=0.18)
    draw = ImageDraw.Draw(im)
    max_w = int(LW * 0.92)
    # Hero = last line (hook)
    fonts = [
        fit_font(draw, line, max_w, start=110 if i == len(lines) - 1 else 82, stroke=STROKE_L, min_size=42)
        for i, line in enumerate(lines)
    ]
    hero = fonts[-1]
    fonts = [
        font
        if i == len(fonts) - 1
        else fit_font(draw, line, max_w, start=min(int(getattr(hero, "size", 90) * 0.72), 86), stroke=STROKE_L, min_size=40)
        for i, (line, font) in enumerate(zip(lines, fonts))
    ]
    heights = [line_wh(draw, line, font, STROKE_L)[1] for line, font in zip(lines, fonts)]
    gap = 10
    block = sum(heights) + gap * (len(lines) - 1)
    y = (LH - block) // 2
    y = max(int(LH * 0.12), min(y, int(LH * 0.78) - block))
    for line, font, hh in zip(lines, fonts, heights):
        draw_words(draw, y, line.split(), yellow, font, STROKE_L, LW)
        y += hh + gap
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=94, optimize=True)
    return {"file": str(out), "hook": " / ".join(lines), "plate": str(plate)}


def try_crop_bottom_caption(src: Path, dest: Path) -> bool:
    """Crop bottom watermark/caption band if bright type is concentrated in lower 18%."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    bottom = im.crop((0, int(h * 0.82), w, h)).resize((80, 20))
    mid = im.crop((0, int(h * 0.35), w, int(h * 0.65))).resize((80, 30))
    def bright_frac(tile):
        pix = list(tile.getdata())
        return sum(1 for r, g, b in pix if r > 200 and g > 180) / len(pix)
    if bright_frac(bottom) < 0.04:
        return False
    if bright_frac(mid) > 0.08:
        # Caption likely also mid-frame — can't clean by bottom crop alone
        return False
    cropped = im.crop((0, 0, w, int(h * 0.82)))
    cropped = ImageOps.fit(cropped, (w, h), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dest, quality=94)
    return True


def run_preview(kind: str, thumb: Path, out: Path) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(PREVIEW), kind, str(thumb), "--out", str(out)], capture_output=True, text=True)
    if r.returncode != 0:
        print("PREVIEW FAIL", thumb, r.stderr)
        return False
    print("preview", out)
    return True


SHORT_JOBS = [
    {"id": "DN4L1DkerMM", "lines": ["RUNNING OUT OF", "STARS"], "yellow": {"STARS"}, "hero": 1, "plate_rank": 1, "try_crop": True},
    {"id": "PV50PX-bE4g", "lines": ["NO", "LIGHT"], "yellow": {"NO"}, "hero": 0, "plate_rank": 1},
    {"id": "l1d1ypHxLk0", "lines": ["TOO", "EARLY"], "yellow": {"EARLY"}, "hero": 1, "plate_rank": 1, "needs_plate": True, "reason": "burned-in 'cosmically young' over galaxy core — cannot crop/paint cleanly"},
    {"id": "M-VN84HCNls", "lines": ["DIAMOND", "PLANETS"], "yellow": {"DIAMOND"}, "hero": 0, "plate_rank": 1},
    {"id": "68uTDP2esso", "lines": ["A HIDDEN", "SECRET"], "yellow": {"SECRET"}, "hero": 1, "plate_rank": 1},
    {"id": "SC2WGTl_V5Q", "lines": ["GLASS", "RAIN"], "yellow": {"GLASS"}, "hero": 0, "plate_rank": 1},
    {"id": "9lLZMy8rBJo", "lines": ["WHAT", "REMAINS?"], "yellow": {"REMAINS?"}, "hero": 1, "plate_rank": None},  # keep prior if no pick
    {"id": "CkSECfUfH2Y", "lines": ["SKY GOING", "DARK"], "yellow": {"DARK"}, "hero": 1, "plate_rank": None},
]

LONG_JOBS = [
    {
        "id": "Yk1tLh23rko",
        "plate_rank": 1,
        "swap": "B",
        "variants": [
            {"v": "B", "lines": ["CRUSHED", "FLAT"], "yellow": {"FLAT"}},
            {"v": "C", "lines": ["YOU'D BE", "FLAT"], "yellow": {"FLAT"}},
        ],
    },
    {
        "id": "REXYxuLOBoI",
        "plate_rank": 1,
        "swap": "B",
        "variants": [
            {"v": "B", "lines": ["LAST", "LIGHT"], "yellow": {"LIGHT"}},
            {"v": "C", "lines": ["THEN", "DARK"], "yellow": {"DARK"}},
        ],
    },
    {
        "id": "NbW5G1BpPY0",
        "plate_rank": 1,
        "swap": "B",
        "variants": [
            {"v": "B", "lines": ["A HIDDEN", "OCEAN"], "yellow": {"OCEAN"}},
            {"v": "C", "lines": ["OCEAN", "BELOW"], "yellow": {"BELOW"}},
        ],
    },
    {
        "id": "3xrxdmaOwJI",
        "plate_rank": 1,
        "swap": "B",
        "variants": [
            {"v": "B", "lines": ["NO WAY", "OUT"], "yellow": {"OUT"}},
            {"v": "C", "lines": ["FALLING", "IN?"], "yellow": {"FALLING"}},
        ],
    },
    {
        "id": "Mo93x0fxB1Q",
        "plate_rank": 1,  # SILENCE plate; also used for B
        "swap": "C",
        "variants": [
            {"v": "B", "lines": ["WHERE IS", "EVERYONE?"], "yellow": {"EVERYONE?"}, "plate_rank": 2},
            {"v": "C", "lines": ["SILENCE"], "yellow": {"SILENCE"}, "plate_rank": 1},
        ],
    },
    {
        "id": "ojk-dfOpAmw",
        "plate_rank": 1,
        "swap": "REP",
        "variants": [
            {"v": "REP", "lines": ["WHEN THEY", "MEET"], "yellow": {"MEET"}},
        ],
    },
]

BASELINE = {
    "DN4L1DkerMM": (95, "1.1%"),
    "PV50PX-bE4g": (7, "0%"),
    "l1d1ypHxLk0": (7, "14.3%"),
    "M-VN84HCNls": (17, "0%"),
    "68uTDP2esso": (46, "0%"),
    "SC2WGTl_V5Q": (13, "0%"),
    "9lLZMy8rBJo": (90, "4.4%"),
    "CkSECfUfH2Y": (28, "7.1%"),
    "Yk1tLh23rko": (202, "2.5%"),
    "REXYxuLOBoI": (142, "2.8%"),
    "NbW5G1BpPY0": (68, "1.5%"),
    "3xrxdmaOwJI": (6, "0%"),
    "Mo93x0fxB1Q": (13, "0%"),
    "ojk-dfOpAmw": (16, "0%"),
}


def old_path(vid: str, short: bool) -> Path | None:
    if short:
        for name in (f"oar2_{vid}.jpg", f"old_{vid}.jpg"):
            p = REFRESH / "old" / name
            if p.exists():
                return p
    p = REFRESH / "old" / f"old_{vid}.jpg"
    return p if p.exists() else None


def build_contact(rows: list[dict]) -> list[Path]:
    font = ImageFont.truetype(FONT_PATH, 15)
    font_sm = ImageFont.truetype(FONT_PATH, 13)
    cell_h, label_w, gap = 240, 300, 8
    built = []
    for row in rows:
        lab = Image.new("RGB", (label_w, cell_h), (18, 20, 26))
        d = ImageDraw.Draw(lab)
        base = BASELINE.get(row["id"])
        base_s = f"{base[0]} impr / {base[1]}" if base else "—"
        txt = (
            f"{row['id']}\n{row['kind']}\nAPPLY: {row['mode'].upper()}\n"
            f"PICK: {row.get('pick','—')}\n{row['status']}\nbase: {base_s}\nplate: {row.get('plate_note','')[:42]}"
        )
        d.multiline_text((8, 10), txt, fill=(255, 210, 90), font=font_sm, spacing=3)

        def fit(p: Path | None, size=(160, 200)):
            if not p or not Path(p).exists():
                b = Image.new("RGB", size, (42, 42, 48))
                ImageDraw.Draw(b).text((20, size[1] // 2 - 8), "—", fill=(160, 160, 160), font=font)
                return b
            return ImageOps.contain(Image.open(p).convert("RGB"), size, Image.Resampling.LANCZOS)

        cells = [lab, fit(Path(row["old"]) if row.get("old") else None)]
        news = row.get("news") or []
        if not news:
            cells.append(fit(None))
        else:
            for n in news[:3]:
                im = fit(Path(n))
                star = row.get("star")
                if star and (f"cover_{star}_" in n or (row["kind"].startswith("short") and row["status"] == "READY")):
                    ImageDraw.Draw(im).rectangle((2, 2, im.width - 3, im.height - 3), outline=(255, 230, 0), width=3)
                cells.append(im)
        cells.append(fit(Path(row["preview"]) if row.get("preview") else None, (220, 200)))
        row_im = Image.new("RGB", (sum(c.width for c in cells) + gap * (len(cells) + 1), cell_h + 2 * gap), (8, 8, 10))
        x = gap
        for c in cells:
            row_im.paste(c, (x, gap + (cell_h - c.height) // 2))
            x += c.width + gap
        built.append(row_im)

    mid = (len(built) + 1) // 2
    outs = []
    for i, page in enumerate([built[:mid], built[mid:]], 1):
        if not page:
            continue
        max_w = max(r.width for r in page)
        sheet = Image.new("RGB", (max_w, sum(r.height for r in page) + gap + 40), (8, 8, 10))
        ImageDraw.Draw(sheet).text(
            (12, 10),
            f"Orbit thumb refresh v02 plates — page {i}/2 — full-bleed · yellow = swap pick · APPLY SWAP",
            fill=(230, 230, 230),
            font=font_sm,
        )
        y = 36
        for r in page:
            sheet.paste(r, (0, y))
            y += r.height
        out = REFRESH / "contact" / f"contact_sheet_page{i}.jpg"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=90)
        (ART / "contact").mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, ART / "contact" / out.name)
        shutil.copy2(out, ART / out.name)
        outs.append(out)
        print("contact", out)
    return outs


def main() -> None:
    print("font=", FONT_PATH)
    for d in ("shorts", "longs", "previews", "plates", "contact", "old"):
        (REFRESH / d).mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    for d in ("shorts", "longs", "previews", "contact"):
        (ART / d).mkdir(parents=True, exist_ok=True)

    # Clear prior bad black-box covers
    for p in (REFRESH / "longs").glob("cover_*.jpg"):
        p.unlink()
    for p in (REFRESH / "shorts").glob("cover_*.jpg"):
        p.unlink()
    for p in (ART / "longs").glob("*.jpg"):
        p.unlink()
    for p in ART.glob("long_*.jpg"):
        p.unlink()
    for p in ART.glob("short_*.jpg"):
        p.unlink()

    log_rows = []
    contact_rows = []
    needs_plate = []

    # ---- Shorts ----
    for job in SHORT_JOBS:
        vid = job["id"]
        old = old_path(vid, True)
        if job.get("needs_plate"):
            needs_plate.append(vid)
            log_rows.append(
                {
                    "id": vid,
                    "batch": "A",
                    "new_text": " / ".join(job["lines"]),
                    "plate_source": "AI Studio needed",
                    "status": "NEEDS PLATE",
                    "reason": job.get("reason"),
                }
            )
            contact_rows.append(
                {
                    "id": vid,
                    "kind": "short A",
                    "mode": "swap",
                    "pick": " / ".join(job["lines"]),
                    "status": "NEEDS PLATE",
                    "old": str(old) if old else None,
                    "news": [],
                    "plate_note": job.get("reason", "NEEDS PLATE")[:48],
                }
            )
            print("NEEDS PLATE", vid, job.get("reason"))
            continue

        plate = None
        plate_note = ""
        if job.get("plate_rank"):
            cand = PICKS / f"{vid}_{job['plate_rank']}.jpg"
            if not cand.exists():
                needs_plate.append(vid)
                print("missing pick", cand)
                continue
            if job.get("try_crop"):
                cleaned = REFRESH / "plates" / f"plate_{vid}_cropped.jpg"
                if try_crop_bottom_caption(cand, cleaned):
                    plate = cleaned
                    plate_note = f"picks/{vid}_1 bottom-caption cropped"
                else:
                    needs_plate.append(vid)
                    reason = "burned-in captions mid-frame; bottom crop insufficient"
                    log_rows.append(
                        {
                            "id": vid,
                            "batch": "A",
                            "new_text": " / ".join(job["lines"]),
                            "plate_source": "AI Studio needed",
                            "status": "NEEDS PLATE",
                            "reason": reason,
                        }
                    )
                    contact_rows.append(
                        {
                            "id": vid,
                            "kind": "short A",
                            "mode": "swap",
                            "pick": " / ".join(job["lines"]),
                            "status": "NEEDS PLATE",
                            "old": str(old) if old else None,
                            "news": [],
                            "plate_note": reason,
                        }
                    )
                    print("NEEDS PLATE", vid, reason)
                    continue
            else:
                plate = cand
                plate_note = f"picks/{vid}_{job['plate_rank']}.jpg"
        else:
            # No new pick — reuse prior scrubbed plate only if it exists and was good; else skip rebuild keep old cover if present
            prior = REFRESH / "shorts" / f"cover_{vid}.jpg"
            # Prefer regenerating from previous clean plate file if we saved one
            prior_plate = REFRESH / "plates" / f"plate_{vid}.jpg"
            if prior_plate.exists():
                plate = prior_plate
                plate_note = f"prior plate_{vid}.jpg (no new pick)"
            else:
                # leave as-was from last good build if cover exists — still rebuild from oar2 scrub? Better: keep NEEDS if no pick
                # For 9lLZ / CkSE we had scrubbed covers — Ben didn't attach picks; keep using previous good plate file if present
                # Fall back: use old oar2 centre as plate but soft only (no black scrub box)
                oar = REFRESH / "old" / f"oar2_{vid}.jpg"
                alt = REFRESH / "old" / f"old_{vid}.jpg"
                src = oar if oar.exists() else alt
                if not src:
                    print("skip short no plate", vid)
                    continue
                # Extract 9:16 centre from letterboxed maxres
                im = Image.open(src).convert("RGB")
                w, h = im.size
                if w > h:
                    col = int(h * 9 / 16)
                    x0 = (w - col) // 2
                    im = im.crop((x0, 0, x0 + col, h))
                plate = REFRESH / "plates" / f"plate_{vid}_from_old.jpg"
                ImageOps.fit(im, (SW, SH), Image.Resampling.LANCZOS).save(plate, quality=92)
                plate_note = f"from old thumb centre ({src.name}) — no Studio pick"

        out = REFRESH / "shorts" / f"cover_{vid}.jpg"
        compose_short(plate, job["lines"], job["yellow"], out, hero=int(job.get("hero", 1)))
        prev = REFRESH / "previews" / f"short_{vid}.jpg"
        ok = run_preview("short", out, prev)
        shutil.copy2(out, ART / "shorts" / out.name)
        shutil.copy2(out, ART / f"short_{vid}.jpg")
        shutil.copy2(prev, ART / "previews" / prev.name)
        log_rows.append(
            {
                "id": vid,
                "batch": "A",
                "new_text": " / ".join(job["lines"]),
                "plate_source": plate_note,
                "status": "BUILT preview PASS" if ok else "BUILT preview FAIL",
                "file": str(out),
                "preview": str(prev),
            }
        )
        contact_rows.append(
            {
                "id": vid,
                "kind": "short A",
                "mode": "swap",
                "pick": " / ".join(job["lines"]),
                "status": "READY" if ok else "FAIL",
                "old": str(old) if old else None,
                "news": [str(out)],
                "preview": str(prev),
                "plate_note": plate_note,
                "star": "A",
            }
        )

    # ---- Longs ----
    for job in LONG_JOBS:
        vid = job["id"]
        old = old_path(vid, False)
        news = []
        for variant in job["variants"]:
            rank = variant.get("plate_rank", job["plate_rank"])
            plate = PICKS / f"{vid}_{rank}.jpg"
            if not plate.exists():
                print("missing", plate)
                continue
            # copy plate into refresh for provenance
            plate_dest = REFRESH / "plates" / f"plate_{vid}_{rank}.jpg"
            shutil.copy2(plate, plate_dest)
            out = REFRESH / "longs" / f"cover_{variant['v']}_{vid}.jpg"
            compose_long(plate, variant["lines"], variant["yellow"], out)
            prev = REFRESH / "previews" / f"long_{variant['v']}_{vid}.jpg"
            ok = run_preview("long", out, prev)
            shutil.copy2(out, ART / "longs" / out.name)
            shutil.copy2(out, ART / f"long_{variant['v']}_{vid}.jpg")
            shutil.copy2(prev, ART / "previews" / prev.name)
            news.append(str(out))
            log_rows.append(
                {
                    "id": vid,
                    "batch": "B",
                    "variant": variant["v"],
                    "swap_pick": variant["v"] == job["swap"],
                    "new_text": " / ".join(variant["lines"]),
                    "plate_source": f"picks/{vid}_{rank}.jpg",
                    "status": "BUILT preview PASS" if ok else "BUILT preview FAIL",
                    "file": str(out),
                    "preview": str(prev),
                }
            )
        pick_prev = REFRESH / "previews" / f"long_{job['swap']}_{vid}.jpg"
        contact_rows.append(
            {
                "id": vid,
                "kind": f"long {vid}",
                "mode": "swap",
                "pick": f"{job['swap']} " + " / ".join(next(v["lines"] for v in job["variants"] if v["v"] == job["swap"])),
                "status": "READY",
                "old": str(old) if old else None,
                "news": news,
                "preview": str(pick_prev) if pick_prev.exists() else (news[0] if news else None),
                "plate_note": f"picks/{vid}_*.jpg full-bleed",
                "star": job["swap"],
            }
        )

    # Jupiter check-only: preview plate but don't apply
    jup = PICKS / "-jmMROGoZCM_1.jpg"
    if jup.exists():
        dest = REFRESH / "plates" / "plate_-jmMROGoZCM_1.jpg"
        shutil.copy2(jup, dest)
        # run preview on plate alone as a long thumb without text? skip — just note in contact
        contact_rows.append(
            {
                "id": "-jmMROGoZCM",
                "kind": "long Jupiter",
                "mode": "swap",
                "pick": "(later — plate saved, not applied)",
                "status": "DEFERRED",
                "old": None,
                "news": [str(dest)],
                "preview": None,
                "plate_note": "picks/-jmMROGoZCM_1.jpg check only",
            }
        )

    build_contact(contact_rows)
    manifest = {
        "version": "thumb_refresh_v02_studio_plates_2026-09-26",
        "note": "PREPARE ONLY. Full-bleed plates from Studio downloads. No black box. No Studio upload.",
        "font": FONT_PATH,
        "needs_plate": needs_plate,
        "rows": log_rows,
        "swap_picks": {j["id"]: j["swap"] for j in LONG_JOBS},
    }
    (REFRESH / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    shutil.copy2(REFRESH / "MANIFEST.json", ART / "MANIFEST.json")
    print("NEEDS PLATE:", needs_plate)
    print("wrote", REFRESH / "MANIFEST.json")


if __name__ == "__main__":
    main()
