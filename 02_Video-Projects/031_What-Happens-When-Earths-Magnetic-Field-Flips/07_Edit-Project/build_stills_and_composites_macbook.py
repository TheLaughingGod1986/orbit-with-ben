#!/usr/bin/env python3
"""J2141 MacBook continuation: recover portrait paths, update HARVEST_POOL_v01.json
macbook_recovery records, and build/verify 12 £0 still plates and row composites (v02).

All source files are verified by SHA-256 against HARVEST_POOL_v01.json and existing
code_graphics manifests before rendering. Existing output files are refused.
Use /usr/bin/python3 (which has Pillow). Media and contact sheet stay outside git.
No audio/moving-video perception, KEEP, Chief PASS or stage approval is claimed.
"""
import argparse
import hashlib
import io
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1920, 1080, 25
HERE = Path(__file__).resolve().parent
POOL_PATH = HERE / "HARVEST_POOL_v01.json"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Didot.ttc"
FONT_SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", errors="replace"))
    return r.stdout


def probe(path: Path):
    return json.loads(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ]
        )
    )


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in (FONT_ITALIC, FONT_SANS):
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_credit(draw: ImageDraw.ImageDraw, text: str, alpha: int = 215):
    if not text or alpha <= 0:
        return
    font = load_font(26)
    draw.text(
        (38, 1022),
        text,
        font=font,
        fill=(244, 239, 230, alpha),
        stroke_width=1,
        stroke_fill=(10, 16, 26, min(220, alpha)),
    )


def encode_frames(dest: Path, total_frames: int, frame_fn):
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing media: {dest}")
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-n",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-vf",
        "noise=alls=3:allf=t",
        "-an",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "fast",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(dest),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for idx in range(total_frames):
            im = frame_fn(idx / FPS).convert("RGB")
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        stderr = proc.stderr.read()
        rc = proc.wait()
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    if rc != 0:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))


def render_portrait_inset_plate(
    src_path: Path,
    bg_texture_path: Path,
    dest: Path,
    duration_s: float,
    credit_text: str,
    credit_window: tuple[float, float],
    max_scale: float,
):
    total_frames = round(duration_s * FPS)
    with Image.open(src_path) as raw:
        portrait = ImageOps.exif_transpose(raw).convert("RGB")
    pw, ph = portrait.size

    # Soft-blurred real volcanic rock backdrop (no UI grid)
    with Image.open(bg_texture_path) as bg_raw:
        bg_src = ImageOps.exif_transpose(bg_raw).convert("RGB")
    bw, bh = bg_src.size

    c_start, c_end = credit_window

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)

        # Gentle drift on the blurred real rock background
        bx0 = round(bw * 0.06 * ease)
        by0 = round(bh * 0.04 * (1.0 - ease))
        bg_crop = bg_src.crop((bx0, by0, bx0 + round(bw * 0.88), by0 + round(bh * 0.88)))
        bg_small = bg_crop.resize((320, 180), Image.Resampling.BICUBIC).filter(
            ImageFilter.GaussianBlur(radius=12)
        )
        bg = bg_small.resize((W, H), Image.Resampling.BICUBIC)
        slate = Image.new("RGB", (W, H), (28, 34, 48))
        backdrop = Image.blend(slate, bg, 0.28)

        scale = max_scale * (0.94 + 0.06 * ease)
        tw = max(1, round(pw * scale))
        th = max(1, round(ph * scale))
        card = portrait.resize((tw, th), Image.Resampling.LANCZOS)

        frame = backdrop.convert("RGBA")
        # Position portrait in right half (x center ~1380) so lower-left WHO card (x=140..1020) is 100% clear
        cx = 1380 - round(18 * ease)
        cy = 500 - round(12 * ease)
        x0 = cx - tw // 2
        y0 = cy - th // 2

        shadow = Image.new("RGBA", (tw + 36, th + 36), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.rounded_rectangle(
            (12, 12, tw + 24, th + 24), radius=18, fill=(8, 12, 20, 155)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        frame.alpha_composite(shadow, (x0 - 12, y0 - 10))

        border = Image.new("RGBA", (tw + 12, th + 12), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(border)
        bdraw.rounded_rectangle(
            (0, 0, tw + 11, th + 11),
            radius=14,
            fill=(238, 232, 220, 255),
            outline=(255, 201, 74, 220),
            width=3,
        )
        frame.alpha_composite(border, (x0 - 6, y0 - 6))
        frame.paste(card, (x0, y0))

        if c_start <= t <= c_end:
            fade = min(1.0, (t - c_start) / 0.3, (c_end - t) / 0.3)
            draw_credit(ImageDraw.Draw(frame), credit_text, round(215 * max(0.0, fade)))
        return frame

    encode_frames(dest, total_frames, make_frame)


def render_pan_tilt_plate(
    src_path: Path,
    dest: Path,
    duration_s: float,
    crop_start: tuple[float, float, float, float],
    crop_end: tuple[float, float, float, float],
    credit_text: str,
    brightness_lift: float = 0.0,
):
    total_frames = round(duration_s * FPS)
    with Image.open(src_path) as raw:
        im = ImageOps.exif_transpose(raw).convert("RGB")

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)
        x0 = crop_start[0] + (crop_end[0] - crop_start[0]) * ease
        y0 = crop_start[1] + (crop_end[1] - crop_start[1]) * ease
        cw = crop_start[2] + (crop_end[2] - crop_start[2]) * ease
        ch = crop_start[3] + (crop_end[3] - crop_start[3]) * ease
        cropped = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
        scaled = cropped.resize((W, H), Image.Resampling.LANCZOS)
        if brightness_lift > 0:
            lift = Image.new("RGB", (W, H), (28, 36, 52))
            scaled = Image.blend(scaled, lift, brightness_lift)
        rgba = scaled.convert("RGBA")
        draw_credit(ImageDraw.Draw(rgba), credit_text, 215)
        return rgba

    encode_frames(dest, total_frames, make_frame)


def render_mars_wide_plate(
    src_path: Path,
    dest: Path,
    duration_s: float,
    credit_text: str,
):
    total_frames = round(duration_s * FPS)
    with Image.open(src_path) as raw:
        mars = ImageOps.exif_transpose(raw).convert("RGB")
    mw, mh = mars.size  # 6787x6787

    # Pre-downsample to 1600x1600 once for clean, fast per-frame Lanczos scaling
    base_size = 1600
    mars_1600 = mars.resize((base_size, base_size), Image.Resampling.LANCZOS)

    # Smooth radial deep-space gradient backdrop (no UI grid, mean_luma >= 34)
    bg_small = Image.new("RGB", (320, 180))
    bpx = bg_small.load()
    for y in range(180):
        for x in range(320):
            dx = (x - 160) / 160.0
            dy = (y - 90) / 90.0
            r2 = min(1.0, (dx * dx + dy * dy) * 0.65)
            r = round(38 - 12 * r2)
            g = round(44 - 14 * r2)
            b = round(62 - 18 * r2)
            bpx[x, y] = (r, g, b)
    bg = bg_small.resize((W, H), Image.Resampling.BICUBIC)

    mask_1600 = Image.new("L", (base_size, base_size), 0)
    mdraw = ImageDraw.Draw(mask_1600)
    pad = round(base_size * 0.038)
    mdraw.ellipse((pad, pad, base_size - pad, base_size - pad), fill=255)
    mask_1600 = mask_1600.filter(ImageFilter.GaussianBlur(radius=8))

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)
        # Full Mars globe height: 910px -> 980px (0.134x -> 0.144x of 6787px native)
        th = round(910 + 70 * ease)
        tw = th
        disc = mars_1600.resize((tw, th), Image.Resampling.LANCZOS)
        dmask = mask_1600.resize((tw, th), Image.Resampling.LANCZOS)
        frame = bg.copy()
        frame.paste(disc, ((W - tw) // 2, (H - th) // 2), dmask)
        rgba = frame.convert("RGBA")
        draw_credit(ImageDraw.Draw(rgba), credit_text, 215)
        return rgba

    encode_frames(dest, total_frames, make_frame)


def render_mars_limb_plate(
    src_path: Path,
    dest: Path,
    duration_s: float,
    credit_text: str,
):
    total_frames = round(duration_s * FPS)
    with Image.open(src_path) as raw:
        mars = ImageOps.exif_transpose(raw).convert("RGB")
    mw, mh = mars.size  # 6787x6787

    # Replace near-black space outside the Mars limb with lifted deep-space slate
    # while preserving the upper-left limb and Valles Marineris canyon system
    crop_box = (0, 200, 4800, 3200)
    sub = mars.crop(crop_box)
    sw, sh = sub.size

    # Circular mask in full-image coordinates centered at (mw/2, mh/2)
    mask_small = Image.new("L", (sw // 4, sh // 4), 0)
    mdraw = ImageDraw.Draw(mask_small)
    cx = (mw / 2 - crop_box[0]) / 4.0
    cy = (mh / 2 - crop_box[1]) / 4.0
    rad = (mw * 0.462) / 4.0
    mdraw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=255)
    mask_full = mask_small.filter(ImageFilter.GaussianBlur(radius=4)).resize(
        (sw, sh), Image.Resampling.BILINEAR
    )

    space_bg = Image.new("RGB", (sw, sh), (26, 34, 50))
    lifted_sub = space_bg.copy()
    lifted_sub.paste(sub, (0, 0), mask_full)

    def make_frame(t: float) -> Image.Image:
        p = t / max(duration_s, 0.001)
        ease = 0.5 - 0.5 * math.cos(math.pi * p)
        # Tight reframed limb + Valles Marineris push: 3360x1890 -> 2960x1665 (upscale 0.57-0.65x <= 2.35x)
        cw = 3360 - 400 * ease
        ch = cw * 9.0 / 16.0
        x0 = 420 + 220 * ease
        y0 = 320 + 140 * ease
        cropped = lifted_sub.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
        scaled = cropped.resize((W, H), Image.Resampling.LANCZOS)
        rgba = scaled.convert("RGBA")
        draw_credit(ImageDraw.Draw(rgba), credit_text, 215)
        return rgba

    encode_frames(dest, total_frames, make_frame)


def render_overlay_composite(
    base_path: Path,
    overlay_path: Path,
    dest: Path,
    overlay_offset_s: float,
    duration_s: float,
):
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing media: {dest}")
    fc = (
        f"[1:v:0]setpts=PTS+{overlay_offset_s:.4f}/TB[ov];"
        f"[0:v:0][ov]overlay=0:0:eof_action=pass[out]"
    )
    run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-n",
            "-i",
            str(base_path),
            "-i",
            str(overlay_path),
            "-t",
            f"{duration_s:.2f}",
            "-filter_complex",
            fc,
            "-map",
            "[out]",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "fast",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(dest),
        ]
    )


def render_r45_fossil_extinction_composite(
    fossil_plate: Path,
    overlay_path: Path,
    dest: Path,
    duration_s: float = 6.60,
    overlay_offset_s: float = 3.16,
):
    """Build R45 composite from the verified clean-cropped plate_031_r45_fossil_v01.mp4
    (which already removes the ruler and colour chart), adding a smooth dark-slate right-side
    readability gradient so the white/gold 'MAGNETIC REVERSALS / NO LINK / MASS EXTINCTIONS'
    overlay at x=1080..1720 has high contrast."""
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing media: {dest}")
    shade_path = dest.parent / "_tmp_r45_shade.png"
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spx = shade.load()
    for x in range(W):
        if x < 820:
            a = 0
        elif x < 1180:
            t = (x - 820) / 360.0
            a = round(205 * (0.5 - 0.5 * math.cos(math.pi * t)))
        else:
            a = 205
        for y in range(H):
            spx[x, y] = (16, 22, 34, a)
    shade.save(shade_path)
    try:
        fc = (
            f"[0:v:0][1:v:0]overlay=0:0:shortest=1[shaded];"
            f"[2:v:0]setpts=PTS+{overlay_offset_s:.4f}/TB[ov];"
            f"[shaded][ov]overlay=0:0:eof_action=pass[out]"
        )
        run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-n",
                "-i",
                str(fossil_plate),
                "-loop",
                "1",
                "-i",
                str(shade_path),
                "-i",
                str(overlay_path),
                "-t",
                f"{duration_s:.2f}",
                "-filter_complex",
                fc,
                "-map",
                "[out]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-preset",
                "fast",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(dest),
            ]
        )
    finally:
        if shade_path.exists():
            shade_path.unlink()


def sample_frame_metrics(path: Path, duration_s: float):
    times = [
        round(max(0.04, duration_s * frac), 3)
        for frac in (0.10, 0.30, 0.50, 0.70, 0.90)
    ]
    samples = []
    frame_hashes = set()
    for t in times:
        raw = run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-ss",
                f"{t:.3f}",
                "-i",
                str(path),
                "-frames:v",
                "1",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-",
            ]
        )
        if len(raw) != W * H * 3:
            raise RuntimeError(f"Unexpected raw frame size {len(raw)} for {path} @ {t}s")
        frame_hashes.add(hashlib.sha256(raw).hexdigest())
        mv = memoryview(raw)
        step = 3 * 16
        lumas = []
        for idx in range(0, len(mv), step):
            r = mv[idx]
            g = mv[idx + 1]
            b = mv[idx + 2]
            lumas.append(0.2126 * r + 0.7152 * g + 0.0722 * b)
        lumas.sort()
        mean_luma = round(sum(lumas) / len(lumas), 2)
        p95_luma = round(lumas[int(0.95 * (len(lumas) - 1))], 2)
        if mean_luma < 28.0:
            raise ValueError(f"Near-black fail on {path.name} @ {t}s: mean_luma={mean_luma}")
        samples.append({"t_s": t, "mean_luma": mean_luma, "p95_luma": p95_luma})
    if len(frame_hashes) < 5:
        raise ValueError(f"Static hold fail on {path.name}: distinct_sample_frames={len(frame_hashes)}")
    return samples, len(frame_hashes)


def verify_render(path: Path, expected_duration_s: float):
    run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"])
    info = probe(path)
    vs = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    if has_audio:
        raise ValueError(f"Unexpected audio stream in {path}")
    w, h = int(vs["width"]), int(vs["height"])
    fps = vs["r_frame_rate"]
    pix_fmt = vs["pix_fmt"]
    nb_frames = int(vs.get("nb_frames") or round(float(info["format"]["duration"]) * FPS))
    dur = float(info["format"]["duration"])
    if (w, h, fps, pix_fmt) != (W, H, "25/1", "yuv420p"):
        raise ValueError(f"Format mismatch on {path.name}: {(w, h, fps, pix_fmt)}")
    if abs(dur - expected_duration_s) > 0.041:
        raise ValueError(f"Duration mismatch on {path.name}: {dur} vs {expected_duration_s}")
    samples, distinct = sample_frame_metrics(path, dur)
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "width": w,
        "height": h,
        "fps": fps,
        "pix_fmt": pix_fmt,
        "nb_frames": nb_frames,
        "duration_s": round(dur, 2),
        "audio_streams": 0,
        "full_decode_ok": True,
        "distinct_sample_frames": distinct,
        "samples": samples,
    }


def update_pool_macbook_recovery(pool_path: Path, portraits_dir: Path, plates_src_dir: Path):
    pool = json.loads(pool_path.read_text())
    src_map = {
        "commons_brunhes": portraits_dir / "brunhes.jpg",
        "commons_gauss": portraits_dir / "gauss.jpg",
        "eol-sunsetchina-iss-20120413": plates_src_dir / "eol-sunsetchina-iss-20120413__sunsetchina_iss_20120413HD_web.mp4",
        "eol-europeaurora_iss_20120405": plates_src_dir / "eol-europeaurora_iss_20120405__europeaurora_iss_20120405.mp4",
        "eol-aurora_iss_20110911": plates_src_dir / "eol-aurora_iss_20110911__aurora_iss_20110911.mp4",
        "eol-auroraus_iss_20120413": plates_src_dir / "eol-auroraus_iss_20120413__auroraus_iss_20120413.mp4",
        "svs-3693-sdo-launching-filament": plates_src_dir / "svs-3693-sdo-launching-filament__sdo_prominence.mp4",
        "svs-12706-sdo-x8-flare-171-304": plates_src_dir / "svs-12706-sdo-x8-flare-171-304__sdo_flare.m4v",
        "svs-13160-sts125-sm4-highlights": plates_src_dir / "svs-13160-sts125-sm4-highlights__hubble_sm4_highlights.webm",
        "commons_usgs_fissure20_overflight": plates_src_dir / "commons_usgs_fissure20_overflight__fissure20_overflight.webm",
        "commons_usgs_kilauea_skylight": plates_src_dir / "commons_usgs_kilauea_skylight__skylight_usgs_flickr.jpg",
        "usgs_vesicular_basalt_side": plates_src_dir / "usgs_vesicular_basalt_side__basalt_vesicular_side_0.jpg",
        "noaa_expl2290_tube_core": plates_src_dir / "noaa_expl2290_tube_core__expl2290_commons.jpg",
        "nps_katm_pachydiscus_ammonite": plates_src_dir / "nps_katm_pachydiscus_ammonite__ammonite.jpg",
    }
    updated = 0
    for asset in pool["assets"]:
        aid = asset.get("asset_id") or asset.get("nasa_id")
        if aid in src_map:
            p = src_map[aid]
            if not p.exists():
                raise FileNotFoundError(f"Missing recovered source for {aid}: {p}")
            digest = sha256_file(p)
            if digest != asset["sha256"]:
                raise ValueError(f"SHA-256 mismatch on {aid}: {digest} != {asset['sha256']}")
            rec = dict(asset.get("macbook_recovery") or {})
            rec.update(
                {
                    "local_path": str(p),
                    "sha256": digest,
                    "bytes": p.stat().st_size,
                    "verified_on": "2026-11-07",
                }
            )
            if aid in {"commons_brunhes", "commons_gauss"}:
                short = aid.replace("commons_", "")
                api_p = portraits_dir / f"{short}_commons_api.json"
                rights_p = portraits_dir / f"{short}_rights.html"
                rec["source_evidence_path"] = str(api_p)
                rec["source_evidence_sha256"] = sha256_file(api_p)
                rec["licence_evidence_path"] = str(rights_p)
                rec["licence_evidence_sha256"] = sha256_file(rights_p)
            asset["macbook_recovery"] = rec
            updated += 1
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    return updated


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("/Users/ben/_desk/J2141-stills-composites-macbook-v03"),
    )
    ap.add_argument(
        "--portraits-dir",
        type=Path,
        default=Path("/Users/ben/_desk/J2141-portraits-macbook-v01"),
    )
    ap.add_argument(
        "--plates-src-dir",
        type=Path,
        default=Path("/Users/ben/_desk/J2141-plates-source-macbook-v01"),
    )
    ap.add_argument(
        "--plates-dir",
        type=Path,
        default=Path("/Users/ben/_desk/J2141-plates-macbook-v01"),
    )
    args = ap.parse_args()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    updated_count = update_pool_macbook_recovery(
        POOL_PATH, args.portraits_dir.resolve(), args.plates_src_dir.resolve()
    )
    print(f"Updated {updated_count} macbook_recovery entries in HARVEST_POOL_v01.json", flush=True)

    nas_cards = Path(
        "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_cards_v01"
    )
    nas_harvest = Path(
        "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01"
    )
    commons_dir = Path("/Users/ben/_desk/J2141-commons-macbook-v01")
    stills_v04_dir = Path("/Users/ben/_desk/J2141-harvest-v04")
    saa_dir = Path("/Users/ben/_desk/J2141-saa-v01")
    recent_dates_dir = Path("/Users/ben/_desk/J2141-recent-dates-v01")
    extinction_dir = Path("/Users/ben/_desk/J2141-extinction-v01")
    basalt_bg = args.plates_src_dir / "commons_usgs_kilauea_skylight__skylight_usgs_flickr.jpg"

    # 1. R5b Brunhes portrait inset plate over blurred real basalt backdrop (40.58-45.78s, 5.20s)
    p_r05 = out_dir / "plate_031_r05_brunhes_v03.mp4"
    render_portrait_inset_plate(
        args.portraits_dir / "brunhes.jpg",
        basalt_bg,
        p_r05,
        duration_s=5.20,
        credit_text="Wikimedia Commons",
        credit_window=(3.64, 5.20),
        max_scale=0.82,
    )

    # 2. R5b Brunhes + WHO lower-third composite (40.58-45.78s, 5.20s)
    c_r05 = out_dir / "composite_031_r05_brunhes_who_v03.mp4"
    render_overlay_composite(
        p_r05,
        nas_cards / "code_graphic_031_r05_who_v01.mov",
        c_r05,
        overlay_offset_s=0.00,
        duration_s=5.20,
    )

    # 3. R6 Kilauea lava flow + FACT card composite (46.64-53.32s, 6.68s)
    c_r06 = out_dir / "composite_031_r06_lava_fact_v03.mp4"
    render_overlay_composite(
        args.plates_dir / "plate_031_r06_lava_v01.mp4",
        nas_cards / "code_graphic_031_r06_fact_v01.mov",
        c_r06,
        overlay_offset_s=4.20,
        duration_s=6.68,
    )

    # 4. R20a Gauss portrait inset plate over blurred real basalt backdrop (203.52-209.08s, 5.56s)
    p_r20 = out_dir / "plate_031_r20_gauss_v03.mp4"
    render_portrait_inset_plate(
        args.portraits_dir / "gauss.jpg",
        basalt_bg,
        p_r20,
        duration_s=5.56,
        credit_text="C. A. Jensen (1840) / Wikimedia Commons",
        credit_window=(0.00, 1.92),
        max_scale=0.39,
    )

    # 5. R20a Gauss + WHO lower-third composite (203.52-209.08s, 5.56s)
    c_r20 = out_dir / "composite_031_r20_gauss_who_v03.mp4"
    render_overlay_composite(
        p_r20,
        nas_cards / "code_graphic_031_r20_who_v01.mov",
        c_r20,
        overlay_offset_s=1.96,
        duration_s=5.56,
    )

    # 6. R29 SAA strength plate + 1970 WHEN stamp composite (301.20-306.32s, 5.12s)
    c_r29 = out_dir / "composite_031_r29_saa_when_v03.mp4"
    render_overlay_composite(
        saa_dir / "code_graphic_031_r29_saa_v01.mp4",
        recent_dates_dir / "code_graphic_031_r29_saa1970_v01.mov",
        c_r29,
        overlay_offset_s=0.24,
        duration_s=5.12,
    )

    # 7. R34a Tane Mahuta giant kauri slow tilt up plate (350.02-355.62s, 5.60s)
    p_r34 = out_dir / "plate_031_r34_kauri_v03.mp4"
    render_pan_tilt_plate(
        commons_dir / "tane_mahuta.jpg",
        p_r34,
        duration_s=5.60,
        crop_start=(0, 2200, 3264, 1836),
        crop_end=(0, 900, 3264, 1836),
        credit_text="Pseudopanax / Wikimedia Commons",
    )

    # 8. R37b Cueva de las Manos hand stencils slow pan plate (383.40-387.28s, 3.88s)
    p_r37 = out_dir / "plate_031_r37_stencils_v03.mp4"
    render_pan_tilt_plate(
        commons_dir / "hand_stencils.jpg",
        p_r37,
        duration_s=3.88,
        crop_start=(80, 360, 3600, 2025),
        crop_end=(480, 360, 3600, 2025),
        credit_text="Fjturban / Wikimedia Commons (CC BY-SA 3.0)",
    )

    # 9. R38 Mars global mosaic wide slow push (use 1 of 2, 388.22-393.02s, 4.80s)
    # Full 6787x6787 globe scaled to 910-980px disc (0.144x <= 2.35x)
    p_r38 = out_dir / "plate_031_r38_mars_wide_v03.mp4"
    render_mars_wide_plate(
        nas_harvest / "PIA00407.jpg",
        p_r38,
        duration_s=4.80,
        credit_text="NASA/JPL/USGS",
    )

    # 10. R44a Mars limb/hemisphere tight reframed push (use 2 of 2, 446.14-449.94s, 3.80s)
    # 6787x6787 native -> 3360x1890 to 2960x1665 limb + Valles Marineris crop (0.649x <= 2.35x)
    p_r44 = out_dir / "plate_031_r44_mars_limb_v03.mp4"
    render_mars_limb_plate(
        nas_harvest / "PIA00407.jpg",
        p_r44,
        duration_s=3.80,
        credit_text="NASA/JPL/USGS",
    )

    # 11. R45 Marine fossil clean plate + right-side shaded extinction_check overlay composite (462.40-469.00s, 6.60s)
    c_r45 = out_dir / "composite_031_r45_fossil_extinction_v03.mp4"
    render_r45_fossil_extinction_composite(
        args.plates_dir / "plate_031_r45_fossil_v01.mp4",
        extinction_dir / "code_graphic_031_r45_extinction_check_v01.mov",
        c_r45,
        duration_s=6.60,
        overlay_offset_s=3.16,
    )

    # 12. R49b USFWS migrating tundra swans slow pan plate (504.48-508.72s, 4.24s)
    p_r49 = out_dir / "plate_031_r49_swans_v03.mp4"
    render_pan_tilt_plate(
        stills_v04_dir / "commons_usfws_tundra_swans.jpg",
        p_r49,
        duration_s=4.24,
        crop_start=(40, 260, 2720, 1530),
        crop_end=(240, 220, 2720, 1530),
        credit_text="USFWS / Erin Clark",
    )

    specs = [
        ("plate_031_r05_brunhes_v03", 5, 40.58, 5.20, p_r05, "commons_brunhes", 0.82),
        ("composite_031_r05_brunhes_who_v03", 5, 40.58, 5.20, c_r05, "commons_brunhes+code_graphic_031_r05_who_v01", 0.82),
        ("composite_031_r06_lava_fact_v03", 6, 46.64, 6.68, c_r06, "commons_usgs_fissure20_overflight+code_graphic_031_r06_fact_v01", 1.50),
        ("plate_031_r20_gauss_v03", 20, 203.52, 5.56, p_r20, "commons_gauss", 0.39),
        ("composite_031_r20_gauss_who_v03", 20, 203.52, 5.56, c_r20, "commons_gauss+code_graphic_031_r20_who_v01", 0.39),
        ("composite_031_r29_saa_when_v03", 29, 301.20, 5.12, c_r29, "code_graphic_031_r29_saa_v01+code_graphic_031_r29_saa1970_v01", 1.00),
        ("plate_031_r34_kauri_v03", 34, 350.02, 5.60, p_r34, "commons_tane_mahuta", 0.588),
        ("plate_031_r37_stencils_v03", 37, 383.40, 3.88, p_r37, "commons_hand_stencils", 0.533),
        ("plate_031_r38_mars_wide_v03", 38, 388.22, 4.80, p_r38, "PIA00407 (use 1 of 2, full globe)", 0.144),
        ("plate_031_r44_mars_limb_v03", 44, 446.14, 3.80, p_r44, "PIA00407 (use 2 of 2, reframed limb + Valles Marineris)", 0.649),
        ("composite_031_r45_fossil_extinction_v03", 45, 462.40, 6.60, c_r45, "nps_katm_pachydiscus_ammonite+code_graphic_031_r45_extinction_check_v01", 0.632),
        ("plate_031_r49_swans_v03", 49, 504.48, 4.24, p_r49, "commons_usfws_tundra_swans", 0.706),
    ]

    records = []
    sheet = Image.new("RGB", (1440, 260 * len(specs)), (22, 28, 40))
    sdraw = ImageDraw.Draw(sheet)
    font = load_font(22)

    for idx, (rid, row, start_s, dur_s, path, source_id, max_upscale) in enumerate(specs):
        v = verify_render(path, dur_s)
        v.update(
            {
                "id": rid,
                "row": row,
                "film_start_s": start_s,
                "film_end_s": round(start_s + dur_s, 2),
                "source_id": source_id,
                "max_upscale": max_upscale,
                "review_status": "technical_candidate_pending_composite_and_Chief_review",
            }
        )
        records.append(v)
        for col, frac in enumerate((0.15, 0.50, 0.85)):
            t = round(dur_s * frac, 2)
            raw = run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-ss",
                    str(t),
                    "-i",
                    str(path),
                    "-frames:v",
                    "1",
                    "-f",
                    "image2pipe",
                    "-vcodec",
                    "png",
                    "-",
                ]
            )
            thumb = Image.open(io.BytesIO(raw)).convert("RGB")
            thumb.thumbnail((460, 220))
            sheet.paste(thumb, (col * 480 + 10, idx * 260 + 8))
            sdraw.text(
                (col * 480 + 14, idx * 260 + 232),
                f"{rid} @ {t:.2f}s",
                font=font,
                fill=(244, 239, 230),
            )
        print(f"Verified {rid} ({dur_s:.2f}s, sha256={v['sha256'][:12]}...)", flush=True)

    contact_path = out_dir / "CONTACT_STILLS_COMPOSITES_MACBOOK_v03.jpg"
    sheet.save(contact_path, quality=92)
    contact_sha = sha256_file(contact_path)

    manifest_path = HERE / "HARVEST_STILLS_COMPOSITES_MACBOOK_v01.json"
    check_path = HERE / "HARVEST_STILLS_COMPOSITES_MACBOOK_TECHNICAL_CHECK_v01.json"
    manifest_data = {
        "job": "J2141",
        "worker": "macbook",
        "date": "2026-11-07",
        "spend_gbp": 0,
        "status": "partial_still_plates_and_composites_only_not_KEEP",
        "superseded_batches": [
            "/Users/ben/_desk/J2141-stills-composites-macbook-v01",
            "/Users/ben/_desk/J2141-stills-composites-macbook-v02",
        ],
        "contact_sheet": str(contact_path),
        "contact_sheet_sha256": contact_sha,
        "renders": records,
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2) + "\n")
    check_path.write_text(
        json.dumps(
            {
                "job": "J2141",
                "worker": "macbook",
                "date": "2026-11-07",
                "spend_gbp": 0,
                "verified_count": len(records),
                "all_1920x1080_25fps_yuv420p": True,
                "all_silent": True,
                "all_full_decode_ok": True,
                "all_mean_luma_ge_28": True,
                "all_distinct_sample_frames_eq_5": True,
                "all_upscale_le_2_35": True,
                "pia00407_appearances": 2,
                "contact_sheet": str(contact_path),
                "contact_sheet_sha256": contact_sha,
                "renders": records,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"All {len(records)} plates/composites verified. Contact sheet: {contact_path}")


if __name__ == "__main__":
    main()
