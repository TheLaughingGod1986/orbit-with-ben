#!/usr/bin/env python3
"""J3088: two proposed thumbnail revisions. No generation or YouTube writes.
Reuses the J2983 plate recipe; preserves that builder and all prior media.
NASA spacecraft icons are separate story insets, never a scale comparison.
"""
from pathlib import Path
import argparse, json
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from build_weekly_thumbs_j2834 import (W, H, ROOT, WHITE, FONT_PATH,
    starfield_bg, draw_arrow, draw_top_band, sha256, score_thumb)


def add_craft(im, source, box, label):
    craft = Image.open(source).convert("RGBA")
    if label == "CASSINI":
        # Crop the long antenna tips, retaining the complete bus and high-gain dish.
        craft = craft.crop((0, 1200, 1550, 2400))
    craft = craft.crop(craft.getbbox())
    craft.thumbnail((box[2]-box[0]-20, box[3]-box[1]-48), Image.Resampling.LANCZOS)
    # A separate rounded inset makes the illustrative, non-scale relationship explicit.
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=20, fill=(17, 29, 63), outline=(125, 155, 205), width=3)
    x = box[0]+(box[2]-box[0]-craft.width)//2
    y = box[1]+8
    im.paste(craft, (x,y), craft)
    d.text((box[0]+14,box[3]-37),label,font=ImageFont.truetype(FONT_PATH,25),fill="white")

def build_compilation(plates: Path, out_dir: Path, craft_dir: Path) -> dict:

    sat_path = plates / "PIA08329.tif" if (plates / "PIA08329.tif").exists() else plates / "PIA08329.jpg"
    sat_raw = Image.open(sat_path).convert("RGB")

    sat_rot = sat_raw.rotate(-10.0, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=(0, 0, 0))
    rw, rh = sat_rot.size
    cw, ch = 1640, 922
    cx0 = rw // 2 - cw // 2
    cy0 = rh // 2 - int(ch * 0.565)
    crop = sat_rot.crop((cx0, max(0, cy0), cx0 + cw, max(0, cy0) + ch)).resize((W, H), Image.Resampling.LANCZOS)

    bg = starfield_bg(19, (13, 21, 58), (24, 52, 132), gx=640.0, gy=445.0, gr=580.0)
    bg_arr = np.asarray(bg).astype(np.float32)

    s_arr = np.asarray(crop).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W]
    scx = (rw * 0.5 - cx0) * (W / cw)
    scy = (rh * 0.5 - max(0, cy0)) * (H / ch)
    sr_globe = 232.0 * (W / cw)
    dist_globe = np.hypot(xx - scx, (yy - scy) * 1.07)
    inside_globe = np.clip((sr_globe - dist_globe) / 10.0, 0.0, 1.0)[..., None]

    ring_lum = 0.299 * s_arr[:, :, 0] + 0.587 * s_arr[:, :, 1] + 0.114 * s_arr[:, :, 2]
    s_lifted = np.power(np.clip(s_arr, 0.0, 1.0), 0.80)
    halo_mask = np.clip(1.0 - ring_lum * 2.8, 0.0, 1.0)
    main_mask = 1.0 - halo_mask
    graded = np.zeros_like(s_lifted)
    r_ch = s_lifted[:, :, 0] * (1.36 * main_mask + 1.05 * halo_mask)
    g_ch = s_lifted[:, :, 1] * (1.12 * main_mask + 1.10 * halo_mask)
    b_ch = s_lifted[:, :, 2] * (0.82 * main_mask + 1.48 * halo_mask)
    graded[:, :, 0] = r_ch / (1.0 + 0.22 * r_ch * r_ch)
    graded[:, :, 1] = g_ch / (1.0 + 0.22 * g_ch * g_ch)
    graded[:, :, 2] = b_ch / (1.0 + 0.18 * b_ch * b_ch)

    globe_dark = np.clip(graded * 255.0 * 1.22 + np.array([4.0, 7.0, 18.0]), 0.0, 255.0)
    ring_alpha = np.clip((ring_lum - 0.025) * 4.2, 0.0, 1.0)[..., None]
    halo_screen = 255.0 * (1.0 - (1.0 - bg_arr / 255.0) * (1.0 - np.clip(graded * 1.10, 0.0, 1.0)))
    outer_comp = halo_screen * (1.0 - ring_alpha * 0.65) + np.clip(graded * 255.0 * 1.24, 0.0, 255.0) * (
        ring_alpha * 0.65
    )

    comp = inside_globe * globe_dark + (1.0 - inside_globe) * outer_comp
    im = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.16)
    im = ImageEnhance.Color(im).enhance(1.30)

    p_tip = (scx - sr_globe * 1.04, scy - sr_globe * 0.22)
    p_tail = (p_tip[0] - 105.0, p_tip[1] - 60.0)
    draw_arrow(im, p_tail, p_tip, color=WHITE, shaft_w=8, head_len=28.0, head_half=16.0)

    add_craft(im, craft_dir / "cassini.png", (30, 438, 310, 700), "CASSINI")
    bbox = draw_top_band(im, ["RINGS", "ARE", "LEAVING"], "LEAVING", tracking=-3, space_scale=0.82)
    out = out_dir / "m09jUdwC5hk_B_v06.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "m09jUdwC5hk",
        "ledger_id": "T037",
        "prior_draft_file": "m09jUdwC5hk_B_v05.jpg",
        "film": "005_The-Last-Star-In-The-Universe (owb_compilation_v05)",
        "live_title": "How Long Will Anything in Space Last?",
        "proposed_title_b": "How Long Will the Universe Last? (Until the Last Star Dies)",
        "reserve_title_b": "When Will Saturn's Rings, the Moon and the Last Star Die?",
        "hook": "RINGS ARE LEAVING",
        "yellow": "LEAVING",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "sources": [
            f"NASA/JPL/Space Science Institute {sat_path.name} (Cassini 'In Saturn's Shadow' backlit Saturn & rings mosaic PIA08329, public domain)",
        ],
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }

def build_jwst(plates: Path, out_dir: Path, craft_dir: Path) -> dict:

    field_raw = Image.open(plates / "JADES_GS_z14_0_field.jpg").convert("RGB")
    cutout_raw = Image.open(plates / "JADES_GS_z14_0_cutout.png").convert("RGB")
    fw, fh = field_raw.size

    gx_full = fw * 0.600500
    gy_full = fh * 0.463664

    field_rot = field_raw.rotate(
        -28.0, resample=Image.Resampling.BICUBIC, expand=False, center=(gx_full, gy_full), fillcolor=(6, 8, 18)
    )

    sx_target, sy_target = 468, 434
    cw, ch = 1920, 1080
    x0 = int(round(gx_full - (sx_target / W) * cw))
    y0 = int(round(gy_full - (sy_target / H) * ch))
    x0 = max(0, min(fw - cw, x0))
    y0 = max(0, min(fh - ch, y0))
    sx = int(round((gx_full - x0) * (W / cw)))
    sy = int(round((gy_full - y0) * (H / ch)))

    crop = field_rot.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.Resampling.LANCZOS)
    c_arr = np.asarray(crop).astype(np.float32)

    lum = (0.299 * c_arr[:, :, 0] + 0.587 * c_arr[:, :, 1] + 0.114 * c_arr[:, :, 2]) / 255.0
    star_glare = np.clip((lum - 0.44) / 0.56, 0.0, 1.0) ** 1.35
    glare_blur = (
        np.asarray(Image.fromarray((star_glare * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(
            np.float32
        )
        / 255.0
    )
    dim_factor = 1.0 - 0.34 * np.maximum(star_glare, glare_blur * 0.75)
    c_arr = c_arr * dim_factor[..., None]

    norm = np.clip(c_arr / 255.0, 0.0, 1.0)
    lifted = np.power(norm, 0.82)
    yy, xx = np.mgrid[0:H, 0:W]
    radial = np.exp(-(((xx - 660.0) ** 2) / (680.0**2) + ((yy - 420.0) ** 2) / (460.0**2)))
    sky_r = 12.0 + 13.0 * radial
    sky_g = 19.0 + 19.0 * radial
    sky_b = 52.0 + 44.0 * radial
    out_arr = np.zeros_like(c_arr)
    out_arr[:, :, 0] = 255.0 * (1.0 - (1.0 - lifted[:, :, 0] * 1.26) * (1.0 - sky_r / 255.0))
    out_arr[:, :, 1] = 255.0 * (1.0 - (1.0 - lifted[:, :, 1] * 1.15) * (1.0 - sky_g / 255.0))
    out_arr[:, :, 2] = 255.0 * (1.0 - (1.0 - lifted[:, :, 2] * 1.12) * (1.0 - sky_b / 255.0))
    im = Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8))
    im = ImageEnhance.Color(im).enhance(1.45)

    cw_cut, ch_cut = cutout_raw.size
    gcx, gcy = cw_cut // 2 + 6, ch_cut // 2 + 5
    cut_rot = cutout_raw.rotate(-28.0, resample=Image.Resampling.BICUBIC, expand=False, center=(gcx, gcy))
    ghalf = 32
    zoom_d = 440
    gal_patch = cut_rot.crop((gcx - ghalf, gcy - ghalf, gcx + ghalf, gcy + ghalf)).resize(
        (zoom_d, zoom_d), Image.Resampling.BICUBIC
    )
    gp = np.asarray(gal_patch).astype(np.float32) / 255.0
    gp_clean = np.power(np.clip((gp - 0.022) / 0.978, 0.0, 1.0), 0.68)
    ly, lx = np.mgrid[0:zoom_d, 0:zoom_d]
    lr = np.hypot(lx - zoom_d * 0.5, ly - zoom_d * 0.5)
    center_focus = 0.45 + 0.55 / (1.0 + np.exp((lr - 106.0) / 22.0))
    gp_clean = gp_clean * center_focus[..., None]

    loupe_arr = np.zeros((zoom_d, zoom_d, 3), dtype=np.float32)
    loupe_bg = np.array([14.0, 18.0, 54.0], dtype=np.float32)[None, None, :]
    sig_r = np.clip(gp_clean[:, :, 0] * 2.25, 0.0, 1.0)
    sig_g = np.clip(gp_clean[:, :, 1] * 1.24, 0.0, 1.0)
    sig_b = np.clip(gp_clean[:, :, 2] * 0.88, 0.0, 1.0)
    loupe_arr[:, :, 0] = 255.0 * (1.0 - (1.0 - sig_r) * (1.0 - loupe_bg[:, :, 0] / 255.0))
    loupe_arr[:, :, 1] = 255.0 * (1.0 - (1.0 - sig_g) * (1.0 - loupe_bg[:, :, 1] / 255.0))
    loupe_arr[:, :, 2] = 255.0 * (1.0 - (1.0 - sig_b) * (1.0 - loupe_bg[:, :, 2] / 255.0))
    gal_loupe = Image.fromarray(np.clip(loupe_arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    gal_loupe = ImageEnhance.Contrast(gal_loupe).enhance(1.25)
    gal_loupe = ImageEnhance.Color(gal_loupe).enhance(1.34)

    zx, zy = 950, 373
    zmask = Image.new("L", (zoom_d, zoom_d), 0)
    ImageDraw.Draw(zmask).ellipse((4, 4, zoom_d - 5, zoom_d - 5), fill=255)
    im.paste(gal_loupe, (zx - zoom_d // 2, zy - zoom_d // 2), zmask)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    zr = zoom_d // 2
    od.ellipse((zx - zr - 6, zy - zr - 6, zx + zr + 6, zy + zr + 6), outline=(0, 0, 0, 242), width=18)
    od.ellipse((zx - zr, zy - zr, zx + zr, zy + zr), outline=(255, 230, 0, 255), width=10)

    sr = 34
    od.ellipse((sx - sr - 3, sy - sr - 3, sx + sr + 3, sy + sr + 3), outline=(0, 0, 0, 240), width=13)
    od.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), outline=(255, 230, 0, 255), width=7)

    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw_arrow(
        im,
        (sx + sr + 10, sy - 3),
        (zx - zr - 16, zy + 6),
        color=WHITE,
        shaft_w=15,
        head_len=42.0,
        head_half=24.0,
    )

    im = ImageEnhance.Color(im).enhance(1.12)
    add_craft(im, craft_dir / "webb_1.png", (40, 475, 340, 700), "WEBB")
    bbox = draw_top_band(im, ["BABY", "GALAXIES"], "GALAXIES", tracking=-2, space_scale=0.90)
    out = out_dir / "ziKBPJ6FY0U_B_v07.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "ziKBPJ6FY0U",
        "ledger_id": "T039",
        "prior_draft_file": "ziKBPJ6FY0U_B_v06.jpg",
        "film": "004_JWST-Discoveries-That-Change-Everything",
        "live_title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "proposed_title_b": "James Webb Telescope: The Galaxies That Shouldn't Exist Yet",
        "reserve_title_b": "Why Did JWST Find Galaxies That Shouldn't Exist Yet?",
        "hook": "BABY GALAXIES",
        "yellow": "GALAXIES",
        "file": str(out.relative_to(ROOT)) if str(out).startswith(str(ROOT)) else str(out),
        "abs_file": str(out),
        "bytes": out.stat().st_size,
        "sha256": sha256(out),
        "origin_circle_px": [sx, sy, sr],
        "loupe_px": [zx, zy, zoom_d // 2],
        "sources": [
            "NASA/ESA/CSA/STScI JADES-GS-z14-0 NIRCam deep field & pullout (STScI-01HZ083EXXCJNE64ERAH2ER2FM / STScI-01HZ08HBSZYHDA52NPPB1BP4SR, spectroscopically confirmed z=14.32 galaxy ~290-300 Myr after the Big Bang, public domain)",
        ],
        "script_verification": "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md Scene 04 line 143: 'Some of the galaxies Webb confirmed are luminous when the universe was only about three hundred million years old.'",
        "hook_box": bbox,
        "score": score_thumb(out, "long"),
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--plates",type=Path,required=True)
    p.add_argument("--craft-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    for name in ("m09jUdwC5hk_B_v06.jpg", "ziKBPJ6FY0U_B_v07.jpg"):
        if (args.out/name).exists():
            raise SystemExit("Refusing to overwrite existing candidate: "+name)
    rows=[build_compilation(args.plates,args.out,args.craft_dir),build_jwst(args.plates,args.out,args.craft_dir)]
    (args.out/"designs.json").write_text(json.dumps(rows,indent=2)+"\n")
    for row in rows: print(row["video"],row["score"])

if __name__ == "__main__": main()
