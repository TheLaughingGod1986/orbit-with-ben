#!/usr/bin/env python3
"""J3129: bounded Webb-only revision of J3088. Existing pixels; no generation or Studio writes."""
from pathlib import Path
import argparse, json
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from build_weekly_thumbs_j2834 import W, H, ROOT, WHITE, draw_arrow, draw_top_band, sha256, score_thumb


def add_webb(im, source):
    craft = Image.open(source).convert("RGBA")
    craft = craft.crop(craft.getbbox())
    # J3088 was 236x177. New 267x200 is +13.1% / +13.0%, same 300x225 inset.
    craft.thumbnail((267, 200), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40,475,340,700), radius=20, fill=(17,29,63), outline=(125,155,205), width=3)
    im.paste(craft, (40+(300-craft.width)//2,475+(225-craft.height)//2), craft)

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
    # Origin connector has no arrowhead. Only the pointer inside the loupe identifies a galaxy.
    d = ImageDraw.Draw(im)
    d.line((sx + sr + 10, sy - 3, zx - zr - 16, zy + 6), fill=(10, 14, 28), width=9)
    d.line((sx + sr + 10, sy - 3, zx - zr - 16, zy + 6), fill=WHITE, width=4)
    # Tip stops at the lower core's right edge; axis aims at (945.3, 373.8).
    draw_arrow(im, (1080, 446), (982, 393), color=WHITE,
               shaft_w=6, head_len=21, head_half=11)

    im = ImageEnhance.Color(im).enhance(1.12)
    add_webb(im, craft_dir / "webb_1.png")
    bbox = draw_top_band(im, ["GALAXIES", "TOO", "BRIGHT"], "BRIGHT", tracking=-2, space_scale=0.90)
    out = out_dir / "ziKBPJ6FY0U_B_v08.jpg"
    im.save(out, quality=94, subsampling=0, optimize=True)
    return {
        "video": "ziKBPJ6FY0U",
        "ledger_id": "T039",
        "prior_draft_file": "ziKBPJ6FY0U_B_v07.jpg",
        "film": "004_JWST-Discoveries-That-Change-Everything",
        "live_title": "JWST Found Galaxies That Shouldn't Exist Yet",
        "hook": "GALAXIES TOO BRIGHT",
        "yellow": "BRIGHT",
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
    p.add_argument("--inputs", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    if (a.out/"ziKBPJ6FY0U_B_v08.jpg").exists() or (a.out/"design.json").exists():
        raise SystemExit("Refusing to overwrite existing output")
    sources=json.loads((a.inputs/"SOURCE_MANIFEST.json").read_text())
    for row in sources["inputs"]:
        assert sha256(a.inputs/row["name"]) == row["sha256"], row["name"]
    row=build_jwst(a.inputs,a.out,a.inputs)
    row["inputs"] = sources["inputs"]
    row["source_manifest_sha256"] = sha256(a.inputs/"SOURCE_MANIFEST.json")
    row["source_page"] = sources["urls"]["jades_asset_page"]
    row["credit"] = "NASA, ESA, CSA, STScI, Brant Robertson (UC Santa Cruz), Ben Johnson (CfA), Sandro Tacchella (Cambridge), Phill Cargile (CfA); spacecraft illustration: NASA"
    row["spend"] = 0
    row["status"] = "proposal only; panel, synthesis and elected-Chief exact-file decision required"
    (a.out/"design.json").write_text(json.dumps(row,indent=2)+"\n")
    print(json.dumps(row["score"]))

if __name__ == "__main__": main()
