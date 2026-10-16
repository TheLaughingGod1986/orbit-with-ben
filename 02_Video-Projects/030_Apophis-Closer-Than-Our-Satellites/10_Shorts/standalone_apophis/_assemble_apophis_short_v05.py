#!/usr/bin/env python3
"""030 Apophis standalone Short v05 (J0226, Chief frame review of v04 at 08:47Z). Does not upload or schedule. No spend.

v05 fixes (Chief queue ruling 2026-10-15T08:47Z):
1) Eliminate dark halo around rock on aurora (~9-13 s) with true unpremultiplied straight alpha (`fg * alpha + bg * (1 - alpha)`)
   and smooth exterior-belt brightness envelope alpha so dark sky bays bridged by closing become transparent (alpha=0)
   while strictly interior craters remain 100% opaque (alpha=1.0), plus edge color decontamination for semi-transparent
   feather pixels (`0 < alpha < 0.96`).
2) Eliminate left-edge glow line (garbage matte): tighten warm-neutral + texture garbage matte (`x > 50`, `mad > 2.8`),
   shave 8 px off the left sunlit silhouette edge to cut Veo's blue/white rim-light line, and tone-map any residual
   high-luminance low-texture left-edge pixels.
3) Keep mix -14.4 LUFS, 22.07 s duration, and DATA 36k/32k overlay unchanged.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SA = REPO / "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(SA))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
import _assemble_standalone_shorts_v01 as sa  # noqa: E402

PLATES = Path("/private/tmp/owb_030_short/plates")
WORK = Path("/private/tmp/owb_030_short/build_v05")
FRAMES = Path("/private/tmp/owb_030_short/build_v01")
KIT = Path("/private/tmp/owb_sa_shorts/sfx_kit_v01")
BED = SA / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
VO_DIR = HERE / "02_Voiceover"
STEM = "030_apophis_short_vo_v01"
VEO = HERE / "04_Generated-Clips/veo_v01/apophis_rock_tumble_veo_v01.mp4"
OMNI = HERE / "04_Generated-Clips/omni_v01/orbit_geo_sat_omni_v01.mp4"
OVERLAY = HERE / "code_graphics_v01/code_graphic_030short_r05_scale_v01.mov"
OUT = HERE / "06_Final-Exports"
FINAL_STEM = "030_apophis_short_v05"
AIR = "2026-10-22"

W, H, FPS = sa.W, sa.H, sa.FPS
QW, QH = W // 4, H // 4
HOOK_END, TITLE, HOLD, MAX_TOTAL = 2.2, (9.0, 14.0), 0.5, 25.5  # gate_shorts_open floor is 22.0 s
BAND = (656, 1264)
LOOP_XFADE = 0.5
MAX_GAP, LEAD, TAIL = 0.40, 0.10, 0.35
VO_GAIN, BED_GAIN, BED_HOLD_GAIN, RUMBLE_GAIN = 1.0, 0.065, 0.35, 0.45
FIX = {"meters": "metres", "kilometers": "kilometres"}
SPEC = {"hook": (("CLOSER", "THAN"), ("SATELLITES",)), "yellow": "SATELLITES",
        "title": ("An Asteroid Will Skim Past", "Earth on Friday the 13th")}


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pause_trim() -> tuple[Path, list[dict], dict]:
    raw = json.loads((VO_DIR / "stt" / STEM / "stt_raw.json").read_text())
    words = [w for w in raw["words"] if w.get("type", "word") == "word"]
    src = VO_DIR / f"{STEM}.wav"
    total = sa.dur(src)
    keep, a = [], max(0.0, words[0]["start"] - LEAD)
    for prev, nxt in zip(words, words[1:]):
        if nxt["start"] - prev["end"] > MAX_GAP:
            keep.append((a, prev["end"] + MAX_GAP / 2))
            a = nxt["start"] - MAX_GAP / 2
    keep.append((a, min(total, words[-1]["end"] + TAIL)))

    def remap(t: float) -> float:
        out = 0.0
        for s, e in keep:
            if t <= e:
                return round(out + max(0.0, t - s), 3)
            out += e - s
        return round(out, 3)

    trim_dir = VO_DIR / "trim"
    trim_dir.mkdir(exist_ok=True)
    dest = trim_dir / f"{STEM}_trim.wav"
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                    f"afade=t=out:st={e - s - 0.01:.3f}:d=0.01[p{i}];" for i, (s, e) in enumerate(keep))
    concat = "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", parts + concat, "-map", "[out]",
         "-ar", "48000", dest])
    mapped = []
    for w in words:
        word = w["text"].strip()
        core = word.rstrip(".,?!")
        mapped.append({"word": FIX.get(core.lower(), core) + word[len(core):],
                       "start": remap(w["start"]), "end": remap(w["end"])})
    (trim_dir / f"{STEM}_trim_words.json").write_text(json.dumps({"stem": STEM, "words": mapped}, indent=1) + "\n")
    meta = {"source_s": round(total, 2), "trimmed_s": round(sa.dur(dest), 2), "segments": len(keep),
            "max_gap_s": MAX_GAP}
    (trim_dir / "pause_trim_meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    return dest, mapped, meta


def frames_of(video: Path, name: str, size: tuple[int, int], rgba: bool = False) -> list[Path]:
    d = FRAMES / f"frames_{name}"
    if not (d / ".done").exists():
        d.mkdir(parents=True, exist_ok=True)
        vf = f"scale={size[0]}:{size[1]}:flags=lanczos" + (",format=rgba" if rgba else "")
        args = ["ffmpeg", "-y", "-v", "error"] + (["-c:v", "prores"] if rgba else []) + ["-i", video, "-vf", vf]
        run(args + [d / ("%04d.png" if rgba else "%04d.jpg")] + ([] if rgba else ["-q:v", "2"]))
        (d / ".done").write_text("ok")
    return sorted(d.glob("*.png" if rgba else "*.jpg"))


def cropped(nasa_id: str, bottom: int = 40) -> Path:
    """The landscape ISS plates carry a white strip along the bottom edge; crop it off."""
    out = WORK / f"{nasa_id}_crop.jpg"
    im = Image.open(PLATES / f"{nasa_id}.jpg")
    im.crop((0, 0, im.width, im.height - bottom)).save(out, quality=95)
    return out


def grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.18)
    return im


def lowered(src: Path, pad: int = 900) -> Path:
    """The plate with dark sky added above it, so in a 9:16 cover crop its limb sits below the 16:9 band."""
    out = WORK / f"{src.stem}_lowered.jpg"
    im = Image.open(src).convert("RGB")
    top = np.asarray(im)[:12].astype(np.float32).mean(axis=(0, 1))
    sky = np.linspace(0.55, 1.0, pad, dtype=np.float32)[:, None, None] * top[None, None, :]
    canvas = Image.new("RGB", (im.width, im.height + pad))
    canvas.paste(Image.fromarray(np.broadcast_to(sky, (pad, im.width, 3)).astype(np.uint8)), (0, 0))
    canvas.paste(im, (0, pad))
    canvas.save(out, quality=95)
    return out


_YY = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None]
_XX = np.linspace(0.0, 1.0, W, dtype=np.float32)[None, :]
_HORIZ = (1.0 - _XX) ** 1.2


def dusk_feather(im: Image.Image) -> Image.Image:
    """Feather the dark Earth silhouette below the sunset limb so horizontal std >= 4 above lower captions."""
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(axis=2, keepdims=True)
    dark_w = np.clip((40.0 - lum) / 40.0, 0.0, 1.0)
    v_env = np.clip((_YY - 0.58) / 0.15, 0.0, 1.0)
    lift = np.dstack([28.0 * _HORIZ * v_env, 18.0 * _HORIZ * v_env, 12.0 * _HORIZ * v_env])
    return Image.fromarray(np.clip(a + lift * dark_w, 0, 255).astype(np.uint8))


def dim_band(im: Image.Image, k: float = 0.55) -> Image.Image:
    """Grade the plate down inside the 16:9 band (feathered edges) and lift dark sky so mean >= 30."""
    a = np.asarray(im).astype(np.float32)
    y = np.arange(H, dtype=np.float32)
    ramp = np.clip(np.minimum(y - (BAND[0] - 220), (BAND[1] + 220) - y) / 220.0, 0.0, 1.0)
    a *= (1.0 - (1.0 - k) * ramp)[:, None, None]
    lum = a.mean(axis=2, keepdims=True)
    dark_w = np.clip((42.0 - lum) / 42.0, 0.0, 1.0)
    lift = np.dstack([14.0 + 22.0 * _HORIZ, 18.0 + 20.0 * _HORIZ, 28.0 + 24.0 * _HORIZ])
    return Image.fromarray(np.clip(a + lift * dark_w, 0, 255).astype(np.uint8))


def gblur(arr_f: np.ndarray, radius: float) -> np.ndarray:
    im = Image.fromarray(arr_f.clip(0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)


def q_main_and_holes(mask_full_u8: np.ndarray, close_r: float = 3.0, erode_r: float = 2.5) -> tuple[np.ndarray, np.ndarray]:
    """Find the main connected component gate and strictly interior crater holes."""
    q_im = Image.fromarray(mask_full_u8).resize((QW, QH), Image.BILINEAR)
    q_u8 = ((np.asarray(q_im) > 80) * 255).astype(np.uint8)
    if not (q_u8 > 0).any():
        z = np.zeros((H, W), dtype=np.uint8)
        return z.astype(np.float32), z

    dens_im = Image.fromarray(q_u8).filter(ImageFilter.GaussianBlur(6))
    dens = np.asarray(dens_im).astype(np.float32) * (q_u8 > 0)
    sy, sx = np.unravel_index(np.argmax(dens), q_u8.shape)
    cc_bridge = ((np.asarray(Image.fromarray(q_u8).filter(ImageFilter.GaussianBlur(2.2))) > 35) * 255).astype(np.uint8)
    cc_im = Image.fromarray(cc_bridge).copy()
    ImageDraw.floodfill(cc_im, (int(sx), int(sy)), 128)
    cc_u8 = (((np.asarray(cc_im) == 128) & (q_u8 > 0)) * 255).astype(np.uint8)

    gate_q = Image.fromarray(((np.asarray(cc_im) == 128) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    gate_full = np.asarray(gate_q.resize((W, H), Image.BILINEAR)).astype(np.float32)
    main_gate = (gate_full > 40.0).astype(np.float32)

    pad_q = np.zeros((QH + 2, QW + 2), dtype=np.uint8)
    closed_q = Image.fromarray(cc_u8).filter(ImageFilter.GaussianBlur(close_r))
    closed_u8 = ((np.asarray(closed_q) > 55) * 255).astype(np.uint8)
    pad_q[1:-1, 1:-1] = closed_u8
    bg_im = Image.fromarray(pad_q).copy()
    ImageDraw.floodfill(bg_im, (0, 0), 128)
    for ry in range(0, QH + 2, 6):
        if pad_q[ry, QW + 1] == 0:
            ImageDraw.floodfill(bg_im, (QW + 1, ry), 128)
        if pad_q[ry, 0] == 0:
            ImageDraw.floodfill(bg_im, (0, ry), 128)
    solid_q = ((np.asarray(bg_im)[1:-1, 1:-1] != 128) * 255).astype(np.uint8)
    inner_q = Image.fromarray(solid_q).filter(ImageFilter.GaussianBlur(close_r + 1.2))
    inner_u8 = ((np.asarray(inner_q) > 235) * 255).astype(np.uint8)
    inner_full = np.asarray(Image.fromarray(inner_u8).resize((W, H), Image.BILINEAR))
    return main_gate, ((inner_full > 127) * 255).astype(np.uint8)


class Rock:
    """Full-res unpremultiplied straight-alpha Veo rock matte (v05): zero dark halo on aurora, zero left-edge glow."""

    def __init__(self, paths: list[Path]):
        self.paths = paths
        self.raw_cache: dict[int, tuple[Image.Image, Image.Image]] = {}

    def _raw_pair(self, i: int) -> tuple[Image.Image, Image.Image]:
        if i in self.raw_cache:
            return self.raw_cache[i]
        im = Image.open(self.paths[i]).convert("RGB")
        a = np.asarray(im).astype(np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        lum = (r + g + b) / 3.0

        # 1. Local texture & warm-neutral check to reject Veo blue/white left-edge glow
        gray_im = Image.fromarray(lum.clip(0, 255).astype(np.uint8))
        mean = np.asarray(gray_im.filter(ImageFilter.BoxBlur(4))).astype(np.float32)
        mad = np.asarray(Image.fromarray(np.abs(lum - mean).clip(0, 255).astype(np.uint8))
                         .filter(ImageFilter.BoxBlur(5))).astype(np.float32)
        hp1 = np.abs(lum - gblur(lum, 1.5))

        warm = np.clip(1.0 - (b - r - 1.5) / 6.0, 0.0, 1.0)
        x_grid = np.arange(W, dtype=np.float32)[None, :]
        y_grid = np.arange(H, dtype=np.float32)[:, None]

        # Garbage matte: require texture + warm-neutral + exclude left edge glow (x <= 50)
        tex_seed = ((mad > 2.8) & (warm > 0.55) & (lum > 30.0) & (x_grid > 50)).astype(np.uint8) * 255
        tex_gate, _ = q_main_and_holes(tex_seed)
        garb = (gblur(tex_gate * 255.0, 8.0) > 45.0).astype(np.float32) * warm
        clean_lum = lum * garb

        # 2. Sunlit core (lum > 125)
        lit_raw = ((clean_lum > 125.0) * 255).astype(np.uint8)
        lit_gate, _ = q_main_and_holes(lit_raw, close_r=2.5, erode_r=2.0)
        lit_eroded = ((gblur(lit_raw.astype(np.float32) * lit_gate, 4.2) > 165.0) * 255.0).astype(np.float32)
        lit_open = ((gblur(lit_eroded, 4.2) > 90.0) * 255).astype(np.uint8)
        _, lit_inner = q_main_and_holes(lit_open, close_r=3.2, erode_r=2.2)
        lit_solid = np.maximum(lit_open, lit_inner).astype(np.float32)

        # Shave 8 px off the left sunlit edge to cut any Veo left-edge glow rim line
        shave_left = np.pad(lit_solid, ((0, 0), (8, 0)), mode="constant")[:, :-8]
        lit_solid = np.minimum(lit_solid, shave_left)

        pad = 36
        lit_pad = np.pad(lit_solid, pad, mode="edge").astype(np.float32)
        l_dil = ((gblur(lit_pad, 9.0) > 60.0) * 255.0).astype(np.float32)
        l_ero = ((gblur(l_dil, 9.0) > 195.0) * 255.0).astype(np.float32)
        l_op_ero = ((gblur(l_ero, 5.5) > 190.0) * 255.0).astype(np.float32)
        l_op_dil = ((gblur(l_op_ero, 5.5) > 65.0) * 255.0).astype(np.float32)
        lit_sil_f = gblur(l_op_dil, 2.5)[pad:-pad, pad:-pad]
        lit_sil_mask = lit_sil_f > 127.0

        # 3. Shadow-side terminator zone
        has_row = lit_sil_mask.any(axis=1)
        first_x = np.where(has_row, np.argmax(lit_sil_mask, axis=1), W)
        has_col = lit_sil_mask.any(axis=0)
        first_y = np.where(has_col, np.argmax(lit_sil_mask, axis=0), H)
        shadow_zone = (x_grid >= (first_x[:, None] + 38)) & (y_grid >= (first_y[None, :] + 38))

        term_raw = (((clean_lum > 58.0) & (mad > 3.0) & shadow_zone) * 255.0).astype(np.float32)
        term_open = ((gblur(term_raw, 4.5) > 140.0) * 255).astype(np.uint8)

        combined = np.maximum((lit_sil_f > 127.0).astype(np.uint8) * 255, term_open)
        main_gate, inner_holes = q_main_and_holes(combined, close_r=3.2, erode_r=2.2)
        combined = np.maximum((combined.astype(np.float32) * main_gate).astype(np.uint8), inner_holes)

        comb_pad = np.pad(combined, pad, mode="edge").astype(np.float32)
        c_dil = ((gblur(comb_pad, 12.0) > 60.0) * 255.0).astype(np.float32)
        c_ero = ((gblur(c_dil, 12.0) > 195.0) * 255.0).astype(np.float32)[pad:-pad, pad:-pad]

        has_rock_light = (gblur(clean_lum, 6.0) > 28.0) | (inner_holes > 0) | (~shadow_zone)
        c_carved = (c_ero > 127.0) & has_rock_light
        c_carved_pad = np.pad((c_carved * 255.0).astype(np.float32), pad, mode="edge")
        c_smooth_f = gblur(c_carved_pad, 7.0)[pad:-pad, pad:-pad]

        sil_f = np.where(~shadow_zone, lit_sil_f, np.maximum(lit_sil_f, c_smooth_f))
        sil_gate, sil_inner = q_main_and_holes(((sil_f > 127.0) * 255).astype(np.uint8), close_r=2.8, erode_r=2.0)
        sil_f = np.maximum(sil_f * sil_gate, sil_inner.astype(np.float32))
        op_pad = np.pad(sil_f, 36, mode="edge")
        op_ero = ((gblur(op_pad, 11.5) > 200.0) * 255.0).astype(np.float32)
        op_dil = gblur(op_ero, 11.5)[36:-36, 36:-36]
        op_mask = ((op_dil > 55.0) * 255.0).astype(np.float32)
        sil_f = np.minimum(sil_f, gblur(op_mask, 4.5))

        # 4. Base silhouette alpha (tight 2-px anti-aliased edge)
        sil_pad = np.pad(sil_f, 24, mode="edge")
        sil_tight = gblur(sil_pad, 3.0)[24:-24, 24:-24]
        alpha_sil = np.clip((sil_tight - 172.0) / (244.0 - 172.0), 0.0, 1.0)
        final_gate, _ = q_main_and_holes(((alpha_sil > 0.02) * 255).astype(np.uint8), close_r=1.5, erode_r=2.0)
        alpha_sil = alpha_sil * final_gate

        # 5. Strictly interior core (eroded ~18 px inside the silhouette):
        #    Inside inner_core, alpha = 1.0 (interior craters remain 100% opaque).
        #    In the outer 18 px boundary belt (1 - inner_core), modulate by smooth local rock brightness so dark
        #    exterior pockets bridged by closing become transparent (alpha = 0) with zero dark halo!
        inner_core = np.clip((gblur(np.pad((alpha_sil > 0.95).astype(np.float32) * 255.0, 24, mode="edge"), 9.5)[24:-24, 24:-24] - 215.0) / 32.0, 0.0, 1.0)
        bright_env = gblur(np.maximum(clean_lum, (lit_inner > 0).astype(np.float32) * 160.0), 4.0)
        lum_alpha_outer = np.clip((bright_env - 68.0) / (122.0 - 68.0), 0.0, 1.0)
        raw_alpha = alpha_sil * (inner_core + (1.0 - inner_core) * lum_alpha_outer)

        ra_u8 = ((raw_alpha > 0.45) * 255).astype(np.uint8)
        ra_gate, ra_inner = q_main_and_holes(ra_u8, close_r=2.0, erode_r=2.0)
        ra_solid = np.maximum(ra_u8.astype(np.float32) * ra_gate, ra_inner.astype(np.float32))
        ra_pad = np.pad(ra_solid, 16, mode="edge")
        ra_ero = ((gblur(ra_pad, 3.8) > 175.0) * 255.0).astype(np.float32)
        ra_dil = ((gblur(ra_ero, 3.8) > 80.0) * 255.0).astype(np.float32)
        ra_feather = gblur(ra_dil, 2.0)[16:-16, 16:-16]
        alpha = np.clip((ra_feather - 135.0) / (242.0 - 135.0), 0.0, 1.0) * ra_gate

        # 6. True unpremultiplied color decontamination for semi-transparent edge pixels (0 < alpha < 0.96)
        interior_rock = ((alpha > 0.94) & (lum > 105.0)).astype(np.float32)
        w_in = np.maximum(gblur(interior_rock * 255.0, 5.0) / 255.0, 1e-4)
        rgb_extrap = np.dstack([gblur(a[..., c] * interior_rock, 5.0) / w_in for c in range(3)])
        has_extrap = (w_in > 0.02)[..., None].astype(np.float32)
        w_in2 = np.maximum(gblur(interior_rock * 255.0, 14.0) / 255.0, 1e-4)
        rgb_extrap2 = np.dstack([gblur(a[..., c] * interior_rock, 14.0) / w_in2 for c in range(3)])
        edge_fill = np.clip(rgb_extrap * has_extrap + rgb_extrap2 * (1.0 - has_extrap), 100.0, 210.0)

        semi_edge = np.clip((0.96 - alpha) / 0.65, 0.0, 1.0)[..., None] * (alpha > 0.0)[..., None].astype(np.float32)
        rgb_unpremult = a * (1.0 - semi_edge) + np.maximum(a, edge_fill) * semi_edge

        # Tone-map any flat white left-edge glow on the immediate 10-px left edge
        shift_r10 = np.pad((alpha > 0.1).astype(np.float32), ((0, 0), (10, 0)), mode="constant")[:, :-10]
        left_edge_10 = ((alpha > 0.1) & (shift_r10 < 0.5)).astype(np.float32)
        left_glow_w = (gblur(left_edge_10 * 255.0, 2.5) / 255.0) * np.clip((lum - 210.0) / 25.0, 0.0, 1.0) * np.clip((4.0 - hp1) / 3.0, 0.0, 1.0)
        rgb_unpremult = rgb_unpremult * (1.0 - left_glow_w[..., None]) + np.minimum(rgb_unpremult, edge_fill) * left_glow_w[..., None]

        im_rgb = Image.fromarray(rgb_unpremult.clip(0, 255).astype(np.uint8), "RGB")
        im_a = Image.fromarray((alpha * 255.0).clip(0, 255).astype(np.uint8), "L")
        self.raw_cache[i] = (im_rgb, im_a)
        return im_rgb, im_a

    def layer(self, src_t: float, scale: float, dx: int, dy: int) -> tuple[np.ndarray, np.ndarray]:
        i = min(len(self.paths) - 1, max(0, int(round(src_t * 24))))
        im_rgb, im_a = self._raw_pair(i)
        if scale != 1.0:
            sz = (round(W * scale), round(H * scale))
            im_rgb = im_rgb.resize(sz, Image.BILINEAR)
            im_a = im_a.resize(sz, Image.BILINEAR)
        c_rgb = Image.new("RGB", (W, H), (0, 0, 0))
        c_a = Image.new("L", (W, H), 0)
        xy = ((W - im_rgb.width) // 2 + dx, (H - im_rgb.height) // 2 + dy)
        c_rgb.paste(im_rgb, xy)
        c_a.paste(im_a, xy)
        return np.asarray(c_rgb).astype(np.float32), np.asarray(c_a).astype(np.float32) / 255.0


def comp(plate: Image.Image, rock: Rock, src_t: float, place: tuple[float, int, int]) -> Image.Image:
    p = np.asarray(plate).astype(np.float32)
    fg, alpha = rock.layer(src_t, *place)
    al = alpha[..., None]
    return Image.fromarray((fg * al + p * (1.0 - al)).clip(0, 255).astype(np.uint8))


def main() -> None:
    test = "--test" in sys.argv
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    vo, words, trim_meta = pause_trim()
    t_of = {}
    for w in words:
        t_of.setdefault(w["word"].rstrip(".,?!").lower(), w)
    last_end = words[-1]["end"]
    total = round(min(last_end + HOLD, MAX_TOTAL), 3)
    nframes = int(round(total * FPS))
    stay = t_of["stay"]["start"]
    close_end = t_of["close"]["end"]
    n36 = t_of["36,000"]["start"]

    veo = Rock(frames_of(VEO, "veo", (W, H)))
    omni = frames_of(OMNI, "omni", (W, H))
    ov_frames = frames_of(OVERLAY, "overlay", (W, H), rgba=True)
    ov_start = round(n36 - 0.5, 3)
    ov_end = ov_start + len(ov_frames) / FPS
    loop_start = round(ov_end, 3)

    dusk = sa.Plate(cropped("iss023e057948"), "cover", 0.30, 0.50)
    night = sa.Plate(cropped("iss023e058455"), "cover", 0.55, 0.50)
    night_low = sa.Plate(cropped("iss023e058455"), "cover", 0.15, 0.80)
    dusk_low = sa.Plate(lowered(cropped("iss023e057948")), "cover", 0.40, 0.70)
    for pl in (dusk, night, night_low, dusk_low):
        pl.im = grade(pl.im)

    omni_src0 = 1.6
    # (start, end, label, plate, zoom_from, zoom_to, rock: (src_from, src_to, scale, dx, dy) or None, kind)
    rows = [
        (0.0, stay, "iss023e057948 + Veo rock", dusk, 1.0, 1.08, (0.6, 3.0, 0.9, 0, -240), "rock"),
        (stay, close_end + 0.15, "Omni Orbit + geo satellite", None, 1.0, 1.0, None, "orbit"),
        (close_end + 0.15, TITLE[0], "iss023e058455 dark framing + Veo rock", night_low, 1.0, 1.06, (2.6, 4.8, 0.82, 60, -330), "rock"),
        (TITLE[0], TITLE[1], "iss023e058455 + Veo rock (title)", night, 1.04, 1.12, (4.8, 8.0, 0.95, 168, 60), "rock"),
        (TITLE[1], loop_start, "iss023e057948 lowered, band dimmed (DATA overlay)", dusk_low, 1.0, 1.08, None,
         "plate"),
        (loop_start, total, "iss023e057948 + Veo rock (loop to frame 0)", dusk, 1.08, 1.0, (3.0, 0.6, 0.9, 0, -240),
         "loop"),
    ]

    def picture(t: float) -> Image.Image:
        i = max(j for j, r in enumerate(rows) if r[0] <= t)
        s, e, _, plate, z0, z1, rk, kind = rows[i]
        k = (t - s) / max(e - s, 1e-3)
        if kind == "orbit":
            src = omni_src0 + (t - s)
            idx = min(len(omni) - 1, int(round(src * 24)))
            return Image.open(omni[idx]).convert("RGB")
        if i == 0:
            x = min(t / sa.OPEN_PUSH_S, 1.0)
            z = z0 * (1 + 0.18 * (1 - (1 - x) ** 2)) + (z1 - z0) * k
        else:
            z = z0 + (z1 - z0) * sa.ease(k)
        frame = plate.frame(z)
        if plate is dusk:
            frame = dusk_feather(frame)
        if kind == "plate":
            frame = dim_band(frame)
        if rk is not None:
            src_t = rk[0] + (rk[1] - rk[0]) * k
            frame = comp(frame, veo, src_t, rk[2:])
        if kind == "loop" and t - s < LOOP_XFADE:
            prev = rows[i - 1][3].frame(rows[i - 1][5])
            if rows[i - 1][7] == "plate":
                prev = dim_band(prev)
            frame = Image.blend(prev, frame, sa.ease((t - s) / LOOP_XFADE))
        return frame

    hook, title = sa.hook_png(SPEC), sa.title_png(SPEC)
    caps = sa.captions(words, total)

    # Save Chief's requested 6.7 / 10.0 / 12.5 s full-res edge crops
    crop_specs = [
        (6.7, (200, 100, 800, 1000), "06.7s"),
        (10.0, (450, 250, 1080, 950), "10.0s"),
        (12.5, (350, 300, 1080, 1050), "12.5s"),
    ]
    for ct, box, label in crop_specs:
        full_im = picture(ct)
        full_im.crop(box).save(OUT / f"{FINAL_STEM}_crop_{label}.jpg", quality=95)

    if test:
        times = [0.0, 1.0, stay + 0.8, 6.7, 10.0, 12.5, ov_start + 2.0, loop_start + 1.0, total - 0.05]
        tiles = []
        for t in times:
            f = picture(t).convert("RGBA")
            f.convert("RGB").save(WORK / f"test_full_{t:05.2f}.jpg", quality=92)
            if t < HOOK_END:
                f.alpha_composite(hook)
            if TITLE[0] <= t < TITLE[1]:
                f.alpha_composite(title)
            if ov_start <= t < ov_end:
                f.alpha_composite(Image.open(ov_frames[int((t - ov_start) * FPS)]).convert("RGBA"))
            tiles.append(f.convert("RGB").resize((270, 480)))
        sheet = Image.new("RGB", (270 * len(tiles), 480))
        for i, im in enumerate(tiles):
            sheet.paste(im, (270 * i, 0))
        sheet.save(WORK / "test_sheet.jpg", quality=88)
        print(json.dumps({"total": total, "stay": stay, "close_end": close_end, "n36": n36, "ov": [ov_start, ov_end],
                          "loop": loop_start, "trim": trim_meta, "sheet": str(WORK / "test_sheet.jpg")}))
        return

    raw = WORK / "picture.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "noise=alls=4:allf=t,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "14", str(raw)], stdin=subprocess.PIPE)
    for f in range(nframes):
        t = f / FPS
        frame = picture(t).convert("RGBA")
        if t < HOOK_END:
            frame.alpha_composite(hook)
        if TITLE[0] <= t < TITLE[1]:
            frame.alpha_composite(title)
        if ov_start <= t < ov_end:
            frame.alpha_composite(Image.open(ov_frames[min(len(ov_frames) - 1, int((t - ov_start) * FPS))])
                                  .convert("RGBA"))
        for a, b, im in caps:
            if a <= t < b:
                frame.alpha_composite(im)
                break
        enc.stdin.write(frame.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("picture encode failed")

    tick_at = ov_start + 0.5
    vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo, "-af", f"aresample=48000,volume={VO_GAIN},apad,atrim=0:{total}",
         "-ac", "2", vo_stem])
    hold_ramp = f"if(lt(t,{last_end}),{BED_GAIN},{BED_GAIN}+({BED_HOLD_GAIN}-{BED_GAIN})*min((t-{last_end})/0.6,1))"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total},volume='{hold_ramp}':eval=frame,afade=t=in:st=0:d=0.3,"
         f"afade=t=out:st={total - 0.6:.3f}:d=0.6", "-ac", "2", bed_stem])
    run(["ffmpeg", "-y", "-v", "error", "-i", KIT / "sfx_owb_rumble_low_v01.wav", "-i", KIT / "sfx_owb_tick_ui_v01.wav",
         "-filter_complex",
         f"[0:a]aresample=48000,volume={RUMBLE_GAIN},afade=t=out:st=1.6:d=0.8,atrim=0:2.4[s0];"
         f"[1:a]aresample=48000,volume=0.3,adelay={int(tick_at * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_stem])
    stems_dir = OUT / f"{FINAL_STEM}_stems"
    stems_dir.mkdir(exist_ok=True)
    for p in (vo_stem, bed_stem, sfx_stem):
        run(["cp", p, stems_dir / p.name])

    final = OUT / f"{FINAL_STEM}.mp4"
    mix = "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-i", vo_stem, "-i", bed_stem,
                            "-i", sfx_stem, "-filter_complex",
                            mix + "loudnorm=I=-14:TP=-1:LRA=11:print_format=json[a]", "-map", "[a]", "-f", "null", "-"],
                           capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", vo_stem, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", mix + norm + ",aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}",
         "-movflags", "+faststart", final])

    sheet = OUT / f"{FINAL_STEM}_frames.jpg"
    times = sorted({round(min(x, total - 0.1), 2) for x in
                    [0.0, 1.0, 2.5, *(r[0] + 0.6 for r in rows[1:]), 6.7, 10.0, 12.5, ov_start + 2.0, total - 0.1]})
    tiles = []
    for i, t in enumerate(times):
        p = WORK / f"sheet_{i}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-vf", "scale=270:480", p])
        tiles.append(p)
    canvas = Image.new("RGB", (270 * len(tiles), 500), (0, 0, 0))
    dd = ImageDraw.Draw(canvas)
    for i, (p, t) in enumerate(zip(tiles, times)):
        canvas.paste(Image.open(p), (270 * i, 0))
        dd.text((270 * i + 6, 482), f"{t:.1f}s", fill=(255, 255, 255))
    canvas.save(sheet, quality=90)

    cuts = [{"row": i + 1, "start_s": round(r[0], 3), "end_s": round(r[1], 3), "picture": r[2], "kind": r[7],
             "zoom": [r[4], r[5]], **({"veo_src_s": [r[6][0], r[6][1]]} if r[6] else {})}
            for i, r in enumerate(rows)]
    cuts[1]["omni_src_s"] = [omni_src0, round(omni_src0 + rows[1][1] - rows[1][0], 3)]
    meta = {
        "job": "J0226", "air_provisional": AIR, "title_on_screen": " ".join(SPEC["title"]),
        "file": str(final.relative_to(REPO)), "frames": str(sheet.relative_to(REPO)), "sha256": sha256(final),
        "duration_s": sa.dur(final), "vo": str(vo.relative_to(REPO)), "pause_trim": trim_meta,
        "words": len(words), "last_word_end_s": last_end, "spoken": " ".join(w["word"] for w in words),
        "hook": f"CLOSER THAN / SATELLITES (yellow SATELLITES), 0-{HOOK_END} s", "title_window_s": TITLE,
        "overlay": {"file": str(OVERLAY.relative_to(REPO)), "row": "code_graphic_030short_r05_scale_v01",
                    "window_s": [ov_start, round(ov_end, 3)], "spoken": "Many satellites orbit at 36,000",
                    "word_36000_s": n36},
        "cuts": cuts,
        "audio": {"bed": str(BED.relative_to(REPO)), "bed_gain": BED_GAIN, "bed_hold_gain": BED_HOLD_GAIN,
                  "sfx": f"rumble at 0 s (gain {RUMBLE_GAIN}), one tick at {tick_at:.2f} s",
                  "stems": str(stems_dir.relative_to(REPO)), "mix": "two-pass loudnorm -14 LUFS, -1 dBTP"},
        "grain": "noise=alls=4:allf=t", "spend": "none",
        "plates": "plates_v01.json (graded: contrast 1.10, colour 1.18)",
        "edge_crops": [
            str((OUT / f"{FINAL_STEM}_crop_06.7s.jpg").relative_to(REPO)),
            str((OUT / f"{FINAL_STEM}_crop_10.0s.jpg").relative_to(REPO)),
            str((OUT / f"{FINAL_STEM}_crop_12.5s.jpg").relative_to(REPO)),
        ],
    }
    (OUT / f"{FINAL_STEM}_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(final), "--air-date", AIR, "--id", "BbsyFrV8kCY"], capture_output=True, text=True)
    (OUT / f"{FINAL_STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo_stem),
                            "--sfx", str(sfx_stem), "--bed", str(bed_stem), "--minutes", f"{total / 60:.3f}"],
                           capture_output=True, text=True)
    (OUT / f"{FINAL_STEM}_sfx_level.txt").write_text(level.stdout + level.stderr)
    print(f"== {final.name} {meta['duration_s']:.2f}s gate={gate.returncode} level={level.returncode}")
    print(gate.stdout[-2500:], level.stdout[-1200:], flush=True)


if __name__ == "__main__":
    main()
