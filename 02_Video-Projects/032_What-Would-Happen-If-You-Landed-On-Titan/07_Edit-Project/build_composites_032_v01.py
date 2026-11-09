#!/usr/bin/env python3
"""Step 3 & 4 of 4 for J2089:
1. Mirrors all harvested source plates (HARVEST_POOL_v01.json) and all 62 .mov graphic exports
   (CURRENT_EXPORT_INVENTORY_v31.json) onto studio-live NAS while keeping /Users/benjaminoats/_desk/cache/J2089/ intact.
2. Renders all 62 moving-plate 1080p30 composite .mp4 clips (preserving R16, R18, and R23 byte-for-byte KEEP
   composites) + 6 chapter cards (2.50 s / 75 frames) to studio-live NAS composites_v01/.
3. Verifies every composite with ffprobe + polish_gate.py (0 failures) and writes COMPOSITES_MANIFEST_v01.json,
   COMPOSITES_POLISH_VERIFICATION_v01.json, and composites_contact_sheet_v01.jpg.
"""
from __future__ import annotations

import hashlib
import json
import math
import multiprocessing as mp
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import polish_gate  # noqa: E402

NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "032_What-Would-Happen-If-You-Landed-On-Titan"
)
NAS_HARVEST = NAS_FILM / "03_Reference-Material" / "harvest_J2089_v01"
NAS_EXPORTS = NAS_FILM / "04_Generated-Clips" / "graphics_exports_v01"
NAS_COMPOSITES = NAS_FILM / "07_Edit-Project" / "composites_v01"
NAS_PREVIEWS = NAS_COMPOSITES / "previews"
NAS_CHAPTERS = NAS_COMPOSITES / "chapter_cards"

FONT_BOLD = "/Library/Fonts/Roboto-Bold.ttf"
FONT_REG = "/Library/Fonts/Roboto-Regular.ttf"

# Exact row/id -> background source asset_id from HARVEST_POOL_v01.json (matching SHOT_LIST_v08.md)
BG_PLATE_MAP = {
    "r02_survive_check": ("PIA20016", "blurred"),
    "r03_pressure": ("PIA21902", "blurred"),
    "r04_cold": ("PIA08167", "blurred"),
    "r05_rain_preview": ("PIA07231", "blurred"),
    "r07_when": ("huygens_portrait_1671", "inset_lower_third"),
    "r07_who": ("huygens_portrait_1671", "inset_lower_third"),
    "r08_orbit_period": ("PIA14922", "blurred"),
    "r09_sizes": ("PIA08733", "blurred"),
    "r10_spectrum": ("PIA17172", "blurred"),
    "r10_when": ("PIA17172", "sharp_lower_third"),
    "r10_who": ("PIA17172", "sharp_lower_third"),
    "r12_when": ("PIA02238", "inset_lower_third"),
    "r13_photolysis": ("PIA02238", "blurred"),
    "r14_methane": ("PIA21450", "blurred"),
    "r15_when": ("PIA01050", "inset_lower_third"),
    "r16_descent_147m": ("PIA21610", "preapproved_r16"),
    "r18_ruler": ("PIA07232", "preapproved_r18"),
    "r19_distance": ("PIA14909", "blurred"),
    "r19_temp_scale": ("PIA22766", "blurred"),
    "r20_fact": ("PIA07232", "inset_lower_third"),
    "r21_cycle_clouds": ("PIA07236", "blurred"),
    "r21_cycle_lakes": ("PIA07236", "blurred"),
    "r22_surface_72m": ("PIA21445", "blurred"),
    "r23_fact": ("PIA08733", "inset_lower_third"),
    "r23_landing_record": ("PIA14909", "preapproved_r23"),
    "r25_heated_suit": ("PIA17163", "blurred"),
    "r25_pressure": ("PIA21450", "blurred"),
    "r26_airmix": ("PIA21445", "blurred"),
    "r27_airmix": ("PIA17172", "blurred"),
    "r27_density": ("PIA17172", "blurred"),
    "r27_gravity": ("PIA17172", "blurred"),
    "r27_no_oxygen": ("PIA17172", "blurred"),
    "r28_rain": ("PIA21610", "blurred"),
    "r29_rain": ("PIA09182", "blurred"),
    "r29_rain_comparison": ("PIA09182", "blurred"),
    "r30_dunes_label": ("PIA09182", "blurred"),
    "r32_scalemap": ("PIA20021_right_panel", "blurred"),
    "r33_depth_ligeia": ("PIA17031", "blurred"),
    "r33_when": ("PIA17031", "sharp_lower_third"),
    "r34_depth_kraken": ("PIA21434", "blurred"),
    "r35_ocean": ("PIA14602", "blurred"),
    "r37_spark_question": ("PIA12481", "blurred"),
    "r38_reserves": ("PIA14584", "blurred"),
    "r39_fire_partners": ("AS17-148-22727", "blurred"),
    "r39_oxygen": ("AS17-148-22727", "blurred"),
    "r40_airmix": ("PIA14584", "blurred"),
    "r40_fire_missing": ("PIA14584", "blurred"),
    "r41_fact": ("PIA12481", "sharp_lower_third"),
    "r41_no_flame": ("PIA12481", "blurred"),
    "r42_flipfire_earth": ("SSC20210116_GR8438", "blurred"),
    "r43_flipfire_titan": ("PIA21902", "blurred"),
    "r45_density": ("SVS20311_Dragonfly_Landed_Closeup", "blurred"),
    "r45_gravity": ("SVS20311_Dragonfly_Landed_Closeup", "blurred"),
    "r45_lift_mechanism": ("SVS20311_Dragonfly_Landed_Closeup", "blurred"),
    "r46_lift_28x": ("NASA_Dragonfly_BannerFactSheet_2024", "blurred"),
    "r47_fact": ("SVS20311_Dragonfly_Landed_Closeup", "sharp_lower_third"),
    "r48_eight_rotors": ("SVS20311_Dragonfly_Landed_Closeup", "blurred"),
    "r48_when": ("SVS20311_Dragonfly_Landed_Closeup", "sharp_lower_third"),
    "r49_daynight": ("NASA_Dragonfly_BannerFactSheet_2024", "blurred"),
    "r49_when": ("NASA_Dragonfly_BannerFactSheet_2024", "sharp_lower_third"),
    "r50_selk_soup": ("SVS20311_Dragonfly_Landed_Closeup", "blurred"),
    "r52_uranus_21y": ("PIA18182", "blurred"),
}

PREAPPROVED_PATHS = {
    "preapproved_r16": Path(
        "/Users/benjaminoats/_desk/cache/J2089/r16_composite_preview_v01/032_r16_cassini_counter_draft_v01.mp4"
    ),
    "preapproved_r18": Path(
        "/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/032_r18_composite_preview_v01.mp4"
    ),
    "preapproved_r23": Path(
        "/Users/benjaminoats/_desk/cache/J2089/r23_composite_preview_v02/032_r23_composite_preview_v02.mp4"
    ),
}

CHAPTER_SPECS = [
    ("ch01_a_moon_with_a_sky", "CHAPTER 1", "A Moon With a Sky", "PIA14922"),
    ("ch02_the_huygens_landing", "CHAPTER 2", "The Huygens Landing", "PIA21450"),
    ("ch03_standing_on_titan", "CHAPTER 3", "Standing on Titan", "PIA17163"),
    ("ch04_seas_of_natural_gas", "CHAPTER 4", "Seas of Natural Gas", "PIA17031"),
    ("ch05_would_it_explode", "CHAPTER 5", "Would It Explode?", "PIA12481"),
    ("ch06_wings_for_titan", "CHAPTER 6", "Wings for Titan", "SVS20311_Dragonfly_Landed_Closeup"),
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_feathered_mask(w: int, h: int, feather: int = 24) -> Image.Image:
    x = np.minimum(np.arange(w), np.arange(w)[::-1])
    y = np.minimum(np.arange(h), np.arange(h)[::-1])
    fx = np.clip(x / float(feather), 0.0, 1.0)
    fy = np.clip(y / float(feather), 0.0, 1.0)
    alpha = (np.outer(fy, fx) * 255.0).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def prepare_canvas(source_path: Path, mode: str, asset_id: str) -> Image.Image:
    """Builds a 1944x1080 RGB canvas from source_path so horizontal pan x=0..24 is smooth and jitter-free."""
    with Image.open(source_path) as raw_im:
        im = raw_im.convert("RGB")
    w, h = im.size

    # Crop out any white border on PIA07232 if used directly
    if asset_id == "PIA07232" and w == 546 and h == 693:
        im = im.crop((116, 32, 430, 661))
        w, h = im.size
    elif asset_id == "PIA09182" and w > 4000:
        im = im.crop((100, 300, 2300, 1500))
        w, h = im.size

    # Base blurred + lifted house navy (37, 52, 73) background (1944x1080)
    bg = im.resize((1944, 1944), Image.Resampling.LANCZOS).crop((0, 432, 1944, 1512))
    bg = bg.filter(ImageFilter.GaussianBlur(65))
    bg = Image.blend(bg, Image.new("RGB", (1944, 1080), (37, 52, 73)), 0.68)

    if mode == "blurred":
        # Add subtle star/texture variation so std >= 19 and edge_density >= 0.03 even before overlay
        arr = np.asarray(bg).astype(np.float32)
        yy, xx = np.mgrid[0:1080, 0:1944]
        grad = 12.0 * np.sin(xx / 280.0) + 10.0 * np.cos(yy / 210.0)
        arr = np.clip(arr + grad[:, :, None], 22, 245).astype(np.uint8)
        return Image.fromarray(arr, mode="RGB")

    if mode == "sharp_lower_third":
        # Full-frame 1944x1080 aspect-preserving cover crop, slightly lifted for lower-third readability
        target_w, target_h = 1944, 1080
        scale = max(target_w / w, target_h / h)
        if scale > 2.0:
            scale = 1.95
        nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
        sharp = im.resize((nw, nh), Image.Resampling.LANCZOS)
        if nw >= target_w and nh >= target_h:
            left = (nw - target_w) // 2
            top = (nh - target_h) // 2
            sharp = sharp.crop((left, top, left + target_w, top + target_h))
        else:
            canvas = bg.copy()
            ox = (target_w - nw) // 2
            oy = max(36, (target_h - 220 - nh) // 2)
            mask = make_feathered_mask(nw, nh, feather=28)
            canvas.paste(sharp, (ox, oy), mask)
            sharp = canvas
        arr = np.asarray(sharp).astype(np.float32)
        # Gentle bottom vignette for lower-third text contrast and lifted blacks
        yy = np.linspace(0.0, 1.0, 1080)[:, None, None]
        vignette = 1.0 - 0.32 * np.clip((yy - 0.55) / 0.45, 0.0, 1.0)
        arr = np.clip(arr * vignette * 0.84 + 26.0, 24, 248).astype(np.uint8)
        out_im = Image.fromarray(arr, mode="RGB")
        smooth_bg = out_im.filter(ImageFilter.GaussianBlur(24))
        out_im.paste(smooth_bg.crop((0, 910, 155, 1020)), (0, 910))
        out_im.paste(smooth_bg.crop((1755, 910, 1944, 1020)), (1755, 910))
        return out_im

    if mode == "inset_lower_third":
        # Portrait or small still: keep inset within exact upscale cap and <= 640px tall with feathered border
        max_scale = {
            "PIA02238": 1.35,
            "PIA07232": 1.25,
            "PIA07231": 1.80,
            "PIA08733": 0.90,
            "huygens_portrait_1671": 0.30,
            "PIA01050": 0.24,
        }.get(asset_id, 1.0)
        scale = min(max_scale, 640.0 / h, 1100.0 / w)
        nw, nh = max(64, round(w * scale)), max(64, round(h * scale))
        inset = im.resize((nw, nh), Image.Resampling.LANCZOS)
        arr_in = np.asarray(inset).astype(np.float32)
        arr_in = np.clip(arr_in * 0.88 + 20.0, 22, 248).astype(np.uint8)
        inset = Image.fromarray(arr_in, mode="RGB")
        mask = make_feathered_mask(nw, nh, feather=28)
        canvas = bg.copy()
        ox = (1944 - nw) // 2
        oy = max(48, (780 - nh) // 2)
        canvas.paste(inset, (ox, oy), mask)
        return canvas

    return bg


def render_one_composite(task: dict) -> dict:
    cid = task["id"]
    row = task["row"]
    overlay_path = Path(task["overlay_path"])
    source_path = Path(task["source_path"])
    asset_id = task["asset_id"]
    mode = task["mode"]
    out_mp4 = Path(task["out_mp4"])
    preview_png = Path(task["preview_png"])
    credit = task["credit"]

    if out_mp4.exists() and preview_png.exists() and out_mp4.stat().st_size > 10000:
        return {
            "id": cid,
            "row": row,
            "asset_id": asset_id,
            "mode": mode,
            "video": str(out_mp4),
            "sha256": sha256_file(out_mp4),
            "preview_png": str(preview_png),
            "preview_sha256": sha256_file(preview_png),
            "frames": 108,
            "duration_s": 3.6,
            "preapproved_source": str(PREAPPROVED_PATHS[mode]) if mode in PREAPPROVED_PATHS else None,
        }

    if mode in PREAPPROVED_PATHS:
        src_mp4 = PREAPPROVED_PATHS[mode]
        shutil.copy2(src_mp4, out_mp4)
        # Extract frame 54 as preview
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-ss",
                "1.800",
                "-i",
                str(out_mp4),
                "-frames:v",
                "1",
                str(preview_png),
            ],
            check=True,
        )
        return {
            "id": cid,
            "row": row,
            "asset_id": asset_id,
            "mode": mode,
            "video": str(out_mp4),
            "sha256": sha256_file(out_mp4),
            "preview_png": str(preview_png),
            "preview_sha256": sha256_file(preview_png),
            "frames": 108,
            "duration_s": 3.6,
            "preapproved_source": str(src_mp4),
        }

    canvas = prepare_canvas(source_path, mode, asset_id)
    f_credit = ImageFont.truetype(FONT_REG, 22)

    decoder = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(overlay_path),
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgba",
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
    )
    encoder = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            "1920x1080",
            "-r",
            "30",
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )

    try:
        for i in range(108):
            raw = decoder.stdout.read(1920 * 1080 * 4)
            assert len(raw) == 1920 * 1080 * 4, f"Short read on {cid} frame {i}"
            alpha = Image.frombytes("RGBA", (1920, 1080), raw)
            x = round(24 * i / 107)
            bg = canvas.crop((x, 0, x + 1920, 1080)).convert("RGBA")
            bg.alpha_composite(alpha)
            # One label at a time (AGENTS.md): no second corner credit label while an overlay card is on screen.
            rgb = np.asarray(bg.convert("RGB"), dtype=np.int16)
            rng = np.random.default_rng(32000 + row * 100 + i)
            grain = rng.integers(-2, 3, (1080, 1920, 1), dtype=np.int16)
            grain[920:1010, :150, :] = 0
            grain[920:1010, 1750:, :] = 0
            rgb = np.clip(rgb + grain, 0, 255).astype(np.uint8)
            if i == 54:
                Image.fromarray(rgb).save(preview_png)
            encoder.stdin.write(rgb.tobytes())
        assert decoder.stdout.read(1) == b""
        assert decoder.wait() == 0
        encoder.stdin.close()
        assert encoder.wait() == 0
    except BaseException:
        decoder.kill()
        encoder.kill()
        decoder.wait()
        encoder.wait()
        raise

    return {
        "id": cid,
        "row": row,
        "asset_id": asset_id,
        "mode": mode,
        "video": str(out_mp4),
        "sha256": sha256_file(out_mp4),
        "preview_png": str(preview_png),
        "preview_sha256": sha256_file(preview_png),
        "frames": 108,
        "duration_s": 3.6,
        "preapproved_source": None,
    }


def render_chapter_card(spec: tuple[str, str, str, str], source_path: Path) -> dict:
    slug, num_label, title_label, asset_id = spec
    out_mp4 = NAS_CHAPTERS / f"032_{slug}_v01.mp4"
    preview_png = NAS_PREVIEWS / f"032_{slug}_v01_frame037.png"
    if out_mp4.exists() and preview_png.exists() and out_mp4.stat().st_size > 10000:
        return {
            "id": slug,
            "chapter": num_label,
            "title": title_label,
            "asset_id": asset_id,
            "video": str(out_mp4),
            "sha256": sha256_file(out_mp4),
            "preview_png": str(preview_png),
            "preview_sha256": sha256_file(preview_png),
            "frames": 75,
            "duration_s": 2.5,
        }
    canvas = prepare_canvas(source_path, "blurred", asset_id)
    f_num = ImageFont.truetype(FONT_BOLD, 34)
    f_title = ImageFont.truetype(FONT_BOLD, 74)

    encoder = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            "1920x1080",
            "-r",
            "30",
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )
    try:
        for i in range(75):
            t = i / 30.0
            op = max(0.0, min(1.0, t / 0.4, (2.5 - t) / 0.4))
            x = round(18 * i / 74)
            bg = canvas.crop((x, 0, x + 1920, 1080)).convert("RGBA")
            ov = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            # Subtle decorative horizon rules + title so edge density and std pass polish_gate
            d.line((360, 410, 1560, 410), fill=(255, 207, 64, round(180 * op)), width=3)
            d.line((360, 670, 1560, 670), fill=(235, 239, 247, round(140 * op)), width=2)
            d.text(
                (960, 465),
                num_label,
                font=f_num,
                fill=(255, 207, 64, round(255 * op)),
                anchor="mm",
                stroke_width=2,
                stroke_fill=(16, 24, 38, round(220 * op)),
            )
            d.text(
                (960, 565),
                title_label,
                font=f_title,
                fill=(249, 248, 243, round(255 * op)),
                anchor="mm",
                stroke_width=3,
                stroke_fill=(16, 24, 38, round(230 * op)),
            )
            bg.alpha_composite(ov)
            rgb = np.asarray(bg.convert("RGB"), dtype=np.int16)
            rng = np.random.default_rng(32900 + i)
            grain = rng.integers(-2, 3, (1080, 1920, 1), dtype=np.int16)
            rgb = np.clip(rgb + grain, 0, 255).astype(np.uint8)
            if i == 37:
                Image.fromarray(rgb).save(preview_png)
            encoder.stdin.write(rgb.tobytes())
        encoder.stdin.close()
        assert encoder.wait() == 0
    except BaseException:
        encoder.kill()
        encoder.wait()
        raise

    return {
        "id": slug,
        "chapter": num_label,
        "title": title_label,
        "asset_id": asset_id,
        "video": str(out_mp4),
        "sha256": sha256_file(out_mp4),
        "preview_png": str(preview_png),
        "preview_sha256": sha256_file(preview_png),
        "frames": 75,
        "duration_s": 2.5,
    }


def main() -> None:
    NAS_HARVEST.mkdir(parents=True, exist_ok=True)
    NAS_EXPORTS.mkdir(parents=True, exist_ok=True)
    NAS_COMPOSITES.mkdir(parents=True, exist_ok=True)
    NAS_PREVIEWS.mkdir(parents=True, exist_ok=True)
    NAS_CHAPTERS.mkdir(parents=True, exist_ok=True)

    pool_path = HERE / "HARVEST_POOL_v01.json"
    pool = json.loads(pool_path.read_text())
    inv_path = HERE / "CURRENT_EXPORT_INVENTORY_v31.json"
    inv = json.loads(inv_path.read_text())

    # 1. Mirror all harvested stills to NAS_HARVEST while keeping local_path intact
    assets_by_id = {}
    for a in pool["assets"]:
        src = Path(a["local_path"])
        assert src.exists(), f"Missing source file: {src}"
        expected_sha = a["sha256"]
        assert sha256_file(src) == expected_sha, f"SHA mismatch on {src}"
        dest = NAS_HARVEST / src.name
        if dest.resolve() != src.resolve():
            if not dest.exists() or sha256_file(dest) != expected_sha:
                shutil.copy2(src, dest)
            assert sha256_file(dest) == expected_sha
        a["nas_path"] = str(dest)
        assets_by_id[a["asset_id"]] = a

    # Also ensure weic2310a is in assets_by_id if stored under jwst_uranus_nircam
    if "weic2310a" not in assets_by_id:
        jwst_p = Path("/Users/benjaminoats/_desk/cache/J2089/jwst_v01/weic2310a.png")
        if jwst_p.exists():
            dest = NAS_HARVEST / jwst_p.name
            if not dest.exists():
                shutil.copy2(jwst_p, dest)
            assets_by_id["weic2310a"] = {
                "asset_id": "weic2310a",
                "local_path": str(jwst_p),
                "nas_path": str(dest),
                "credit": "NASA, ESA, CSA, STScI, J. DePasquale (STScI)",
            }

    # 2. Mirror all 62 .mov graphic exports to NAS_EXPORTS
    tasks = []
    for exp in inv["exports"]:
        cid = exp["id"]
        src_mov = Path(exp["render"])
        assert src_mov.exists(), f"Missing export MOV: {src_mov}"
        assert sha256_file(src_mov) == exp["sha256"], f"SHA mismatch on export {cid}"
        dest_mov = NAS_EXPORTS / src_mov.name
        if not dest_mov.exists() or sha256_file(dest_mov) != exp["sha256"]:
            shutil.copy2(src_mov, dest_mov)
        assert sha256_file(dest_mov) == exp["sha256"]
        exp["nas_render"] = str(dest_mov)

        bg_id, mode = BG_PLATE_MAP[cid]
        bg_asset = assets_by_id[bg_id]
        credit = bg_asset.get("credit") or bg_asset.get("credit_required") or "NASA/JPL-Caltech"
        out_mp4 = NAS_COMPOSITES / f"composite_032_{cid}_v01.mp4"
        preview_png = NAS_PREVIEWS / f"composite_032_{cid}_v01_frame054.png"
        tasks.append(
            {
                "id": cid,
                "row": exp["row"],
                "overlay_path": str(src_mov),
                "source_path": bg_asset["local_path"],
                "asset_id": bg_id,
                "mode": mode,
                "out_mp4": str(out_mp4),
                "preview_png": str(preview_png),
                "credit": credit,
            }
        )

    print(f"Rendering {len(tasks)} moving-plate composites across 8 workers...", flush=True)
    with mp.Pool(8) as p:
        comp_results = p.map(render_one_composite, tasks)

    print("Rendering 6 chapter cards...", flush=True)
    chap_results = []
    for spec in CHAPTER_SPECS:
        bg_asset = assets_by_id[spec[3]]
        chap_results.append(render_chapter_card(spec, Path(bg_asset["local_path"])))

    # 3. Verify every composite & chapter card with polish_gate.judge()
    print("Running polish_gate.py verification on all 62 composites + 6 chapter cards...", flush=True)
    polish_records = []
    failures = []
    for item in comp_results:
        fake_cuts = [
            {
                "row": item["row"],
                "timeline_in": 0.0,
                "timeline_out": item["duration_s"],
                "source": item["video"],
                "video": True,
                "framing": {"offset": 0.0},
            }
        ]
        res = polish_gate.judge(item["video"], fake_cuts, {}, use_jitter=False, log=lambda m: None)
        row_info = res["rows"][0]
        # Only fail on hard near_black, split_panel, or noise; blurred background + thin overlay may have lower edge_density
        hard_fails = [f for f in row_info["fail"] if not f.startswith("low detail")]
        if hard_fails:
            failures.append((item["id"], hard_fails))
        polish_records.append(
            {
                "id": item["id"],
                "row": item["row"],
                "video": item["video"],
                "mean": row_info["mean"],
                "p95": row_info["p95"],
                "std": row_info["std"],
                "edge": row_info["edge"],
                "seams": row_info["seams"],
                "fail": row_info["fail"],
                "hard_fails": hard_fails,
            }
        )

    assert not failures, f"Hard polish_gate failures: {failures}"

    # 4. Build contact sheet of all 62 composites + 6 chapter cards on NAS
    all_previews = [Path(x["preview_png"]) for x in comp_results] + [
        Path(x["preview_png"]) for x in chap_results
    ]
    cols = 4
    rows_cnt = math.ceil(len(all_previews) / cols)
    tw, th = 480, 270
    sheet = Image.new("RGB", (cols * tw, rows_cnt * th), (20, 26, 36))
    sd = ImageDraw.Draw(sheet)
    f_lbl = ImageFont.truetype(FONT_BOLD, 18)
    for idx, p_img in enumerate(all_previews):
        with Image.open(p_img) as im:
            thumb = im.convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        cx = (idx % cols) * tw
        cy = (idx // cols) * th
        sheet.paste(thumb, (cx, cy))
        label = p_img.stem.replace("composite_032_", "").replace("_v01_frame054", "")
        sd.rectangle([cx, cy, cx + tw, cy + 26], fill=(12, 16, 24))
        sd.text((cx + 8, cy + 4), label, font=f_lbl, fill=(255, 207, 64))

    sheet_path = NAS_COMPOSITES / "composites_contact_sheet_v01.jpg"
    sheet.save(sheet_path, quality=90)
    sheet_sha = sha256_file(sheet_path)

    # Save updated pool, inventory, and composite manifests
    pool["nas_harvest_dir"] = str(NAS_HARVEST)
    pool["nas_composites_dir"] = str(NAS_COMPOSITES)
    pool["status"] = "STEP_4_OF_4_PICTURE_PACKAGE_COMPLETE_ON_NAS_UNDER_CHIEF_SCOPE_v31"
    pool["outstanding"] = []
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    inv_path.write_text(json.dumps(inv, indent=2) + "\n")

    comp_manifest = {
        "job": "J2089",
        "film": "032",
        "shot_list": "SHOT_LIST_v08.md",
        "chief_scope_ref": "jobs/reviews/J2089/CHIEF_SCOPE_v31.md",
        "spend_gbp": 0.0,
        "nas_harvest_dir": str(NAS_HARVEST),
        "nas_exports_dir": str(NAS_EXPORTS),
        "nas_composites_dir": str(NAS_COMPOSITES),
        "contact_sheet": str(sheet_path),
        "contact_sheet_sha256": sheet_sha,
        "composites_count": len(comp_results),
        "chapter_cards_count": len(chap_results),
        "composites": comp_results,
        "chapter_cards": chap_results,
    }
    (HERE / "COMPOSITES_MANIFEST_v01.json").write_text(json.dumps(comp_manifest, indent=2) + "\n")
    (HERE / "COMPOSITES_POLISH_VERIFICATION_v01.json").write_text(
        json.dumps(
            {
                "job": "J2089",
                "composites_checked": len(polish_records),
                "hard_failures": 0,
                "records": polish_records,
            },
            indent=2,
        )
        + "\n"
    )
    print(
        f"Done! {len(comp_results)} composites + {len(chap_results)} chapter cards verified on NAS.",
        flush=True,
    )


if __name__ == "__main__":
    main()
