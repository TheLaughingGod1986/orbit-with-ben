#!/usr/bin/env python3
"""Saturn first cut v03b — CoS fixes before Ben watches.

On top of v03 polish (4× zoompan, loudnorm, cover/blur fill):
1. Row 93: replace near-black PIA12633 with readable planet still PIA21351
2. Feather blur_bg composites (no hard rectangle seam)
3. Music acrossfade-loop so bed covers full 548.12s with no hard stop
4. Larger house-style chapter cards (readable at phone size)

Delivers to iCloud OWB UAT/saturn_first_cut_v03b/ (no media in git).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

EP = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SHOT = HERE / "shot_list_v03g.csv"
POOL_JSON = HERE / "nasa_pool_v01.json"
POOL_DIR = HERE / "nasa_pool_v01"
VO = EP / "02_Voiceover/parts/saturn_rings_vo_v03b_tightened_LOCK.wav"
CLIPS = EP / "04_Generated-Clips"
GODDARD = HERE / "_uat_v03c_ben1543/SVS_12672_ring_rain.mp4"
WORK = HERE / "saturn_film/work_first_cut_v03b"
OUT_LOCAL = HERE / "saturn_film/saturn_first_cut_v03b.mp4"
REVIEW = HERE / "review"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR = UAT / "saturn_first_cut_v03b"
ART = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-worker/artifacts")

MUSIC = [
    Path(__file__).resolve().parent.parent / "05_Music" / "saturn-rings_score_bed_v01.mp3",
]

# Row 93 temp PIA12633 is near-black limb; use a clean planet disk until Omni.
ROW_STILL_OVERRIDE = {
    "93": "PIA21351",
}

W, H, FPS = 1920, 1080, 24
MAX_COVER = 2.0  # do not upscale past ~2× to fill
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CARD_FONT_SIZE = 104  # house chapter cards — larger than v03's 64

AI_PATHS = {
    "edit_ice_chunks_v07.mp4": CLIPS / "v07/edit_ice_chunks_v07.mp4",
    "veo_young_rings_v01.mp4": CLIPS / "veo_world_v01/veo_young_rings_v01.mp4",
    "veo_bare_saturn_v05.mp4": CLIPS / "veo_v05/veo_bare_saturn_v05.mp4",
    "veo_orbit_tumble_v03_fallback_0-3s.mp4": CLIPS / "v07/veo_orbit_tumble_v03_fallback_0-3s.mp4",
}

CANT_FILL: list[dict] = []  # rows that need blur-bg because cover > 2×


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd[:16]), flush=True)
    subprocess.check_call(cmd)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            text=True,
        ).strip()
    )


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def chunk_write(src: Path | bytes, dest: Path, retries: int = 14) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 256 * 1024):
                    o.write(data[i : i + 256 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.2)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.0 * (attempt + 1))
    Path("/tmp").joinpath(f"uat_stage_{dest.name}").write_bytes(data)


def parse_push(move: str) -> float:
    if not move:
        return 1.06
    m = re.search(r"([\d.]+)\s*%", move)
    if m:
        return 1.0 + float(m.group(1)) / 100.0
    if "slow" in move.lower():
        return 1.07
    return 1.06


def _wrap_title(title: str, font: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    words = title.split()
    if not words:
        return [title]
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), trial, font=font)[2] <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def starfield_card(title: str, path: Path) -> None:
    """Soft space-gradient chapter card — large type, phone-readable."""
    im = Image.new("RGB", (W, H), "#070b14")
    px = im.load()
    for y in range(H):
        t = y / H
        r, g, b = int(7 + 10 * t), int(11 + 16 * t), int(22 + 28 * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(im)
    for x, y in (
        (180, 120), (420, 200), (700, 90), (980, 240), (1400, 140),
        (220, 700), (800, 780), (1200, 640), (1600, 720), (500, 500),
        (300, 400), (1100, 360), (1700, 500),
    ):
        draw.ellipse((x, y, x + 2, y + 2), fill=(210, 216, 230))

    size = CARD_FONT_SIZE
    max_w = W * 0.86
    while size >= 72:
        f = ImageFont.truetype(FONT, size)
        lines = _wrap_title(title, f, max_w)
        widths = [draw.textbbox((0, 0), ln, font=f)[2] for ln in lines]
        heights = [
            draw.textbbox((0, 0), ln, font=f)[3] - draw.textbbox((0, 0), ln, font=f)[1]
            for ln in lines
        ]
        block_h = sum(heights) + 18 * (len(lines) - 1)
        if max(widths) <= max_w and block_h <= H * 0.42:
            break
        size -= 4
    f = ImageFont.truetype(FONT, size)
    lines = _wrap_title(title, f, max_w)
    line_sizes = []
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=f)
        line_sizes.append((bb[2] - bb[0], bb[3] - bb[1]))
    block_h = sum(h for _, h in line_sizes) + 18 * (len(lines) - 1)
    y = (H - block_h) / 2

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    yy = y
    for ln, (tw, th) in zip(lines, line_sizes):
        x = (W - tw) / 2
        sd.text((x, yy + 3), ln, font=f, fill=(0, 0, 0, 110))
        yy += th + 18
    im = im.convert("RGBA")
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    dr = ImageDraw.Draw(im)
    yy = y
    for ln, (tw, th) in zip(lines, line_sizes):
        x = (W - tw) / 2
        dr.text((x, yy), ln, font=f, fill=(244, 246, 250, 255))
        yy += th + 18
    im.convert("RGB").save(path, quality=95)


def caption_png(text: str, path: Path) -> None:
    t = text.strip()
    if t.lower() == "illustration":
        t = "Illustration"
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 28)
    bbox = draw.textbbox((0, 0), t, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = 48, H - 64 - th
    draw.rectangle((x - 12, y - 8, x + tw + 12, y + th + 10), fill=(0, 0, 0, 160))
    draw.text((x, y), t, font=f, fill=(240, 242, 246, 255))
    im.save(path)


def cover_scale(w: int, h: int) -> float:
    return max(W / w, H / h)


def compose_still_frame(still: Path, dest_png: Path, *, row: str, rid: str) -> str:
    """Build a 1920×1080 RGB still with no flat bars.

    Returns framing mode: 'cover' or 'blur_bg'.
    blur_bg uses a feathered FG mask so the composite has no hard rectangle seam.
    """
    im = Image.open(still).convert("RGB")
    sw, sh = im.size
    cov = cover_scale(sw, sh)
    if cov <= MAX_COVER + 1e-9:
        scale = cov
        nw, nh = int(round(sw * scale)), int(round(sh * scale))
        scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        x0 = max(0, (nw - W) // 2)
        y0 = max(0, (nh - H) // 2)
        out = scaled.crop((x0, y0, x0 + W, y0 + H))
        mode = "cover"
    else:
        CANT_FILL.append({
            "row": row, "id": rid, "w": sw, "h": sh,
            "cover": round(cov, 3),
        })
        bg = im.resize(
            (int(round(sw * cov)), int(round(sh * cov))),
            Image.Resampling.LANCZOS,
        )
        bx0 = max(0, (bg.width - W) // 2)
        by0 = max(0, (bg.height - H) // 2)
        bg = bg.crop((bx0, by0, bx0 + W, by0 + H)).filter(ImageFilter.GaussianBlur(40))
        bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.22)
        contain = min(W / sw, H / sh)
        fw, fh = int(round(sw * contain)), int(round(sh * contain))
        fg = im.resize((fw, fh), Image.Resampling.LANCZOS).convert("RGBA")
        # Soft edge — kills the hard-edged rectangle at the FG/BG join.
        feather = max(36, int(min(fw, fh) * 0.045))
        mask = Image.new("L", (fw, fh), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, fw - 1, fh - 1), radius=feather, fill=255,
        )
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
        fg.putalpha(mask)
        out_rgba = bg.convert("RGBA")
        out_rgba.alpha_composite(fg, ((W - fw) // 2, (H - fh) // 2))
        out = out_rgba.convert("RGB")
        mode = "blur_bg"
    out.save(dest_png, quality=95)
    return mode


def still_to_mp4(base_png: Path, dest: Path, dur: float, zoom_end: float) -> None:
    """4× zoompan on a full-frame still (Claude Fix 1)."""
    if dur < 0.25:
        dur = 0.25
    n = max(1, int(round(dur * FPS)))
    z0, z1 = 1.0, min(zoom_end, 1.12)
    zf = f"{z0:.4f}+({z1 - z0:.4f})*on/{max(n - 1, 1)}"
    # Upscale 4× before zoompan so slow pushes are sub-pixel smooth.
    # x/y MUST use iw/zoom (not ow) once upscaled.
    vf = (
        f"scale=7680:-2,"
        f"zoompan=z='{zf}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':"
        f"d={n}:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(base_png),
        "-vf", vf,
        "-frames:v", str(n),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-an",
        str(dest),
    ])


def clip_window(src: Path, dest: Path, src_in: float, src_out: float, caption: str = "") -> None:
    """Motion clips: cover-fill 16:9 (they are already HD / generated)."""
    dur = max(0.25, src_out - src_in)
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},fps={FPS},format=yuv420p"
    )
    if caption.strip():
        cap = WORK / f"_cap_{dest.stem}.png"
        caption_png(caption, cap)
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{src_in:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
            "-i", str(cap),
            "-filter_complex", f"[0:v]{vf}[b];[b][1:v]overlay=0:0",
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
            str(dest),
        ])
    else:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{src_in:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
            "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
            str(dest),
        ])


def resolve_nasa(nasa_id: str, pool: dict) -> Path:
    e = pool[nasa_id]
    p = POOL_DIR / e["section"] / f"{nasa_id}.jpg"
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def build_row_clip(r: dict, pool: dict, dest: Path) -> None:
    src = (r.get("source") or "").strip().upper()
    rid = (r.get("id") or "").strip()
    row_s = str(r["row"])
    if row_s in ROW_STILL_OVERRIDE and src == "NASA":
        print(
            f"  row {row_s}: override still {rid} → {ROW_STILL_OVERRIDE[row_s]}",
            flush=True,
        )
        rid = ROW_STILL_OVERRIDE[row_s]
    dur = float(r["vo_out"]) - float(r["vo_in"])
    cap = (r.get("caption") or "").strip()
    last = r.get("_last", False)

    if src == "CARD":
        png = WORK / f"card_{r['row']}.png"
        starfield_card(rid, png)
        still_to_mp4(png, dest, dur, 1.02)
        return

    if src == "NASA":
        still = resolve_nasa(rid, pool)
        base = WORK / f"still_{int(r['row']):03d}_{rid}.jpg"
        mode = compose_still_frame(still, base, row=row_s, rid=rid)
        zoom = parse_push(r.get("move") or "")
        if last:
            zoom = max(zoom, 1.07)
        print(f"  frame mode={mode} cover={cover_scale(*Image.open(still).size):.3f}", flush=True)
        still_to_mp4(base, dest, dur, zoom)
        if cap:
            cap_png = WORK / f"cap_{r['row']}.png"
            caption_png(cap, cap_png)
            capped = dest.with_name(dest.stem + "_c.mp4")
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(dest), "-i", str(cap_png),
                "-filter_complex", "[0:v][1:v]overlay=0:0",
                "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
                str(capped),
            ])
            capped.replace(dest)
        return

    if src == "GODDARD":
        if not GODDARD.exists():
            raise FileNotFoundError(GODDARD)
        clip_window(GODDARD, dest, float(r["src_in"]), float(r["src_out"]), caption="")
        return

    if src in ("AI", "OMNI"):
        path = AI_PATHS.get(rid)
        if path is None or not path.exists():
            hits = list(CLIPS.rglob(rid))
            if not hits:
                raise FileNotFoundError(rid)
            path = hits[0]
        clip_window(path, dest, float(r["src_in"]), float(r["src_out"]), caption=cap)
        return

    raise ValueError(f"unknown source {src} row {r.get('row')}")


def concat_videos(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat_v.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in paths))
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-an",
        str(dest),
    ])


def build_audio(rows: list[dict], total: float) -> Path:
    vo_parts_dir = WORK / "audio_parts"
    vo_parts_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    vo_cursor = 0.0
    vo_dur = probe(VO)
    for r in rows:
        dur = float(r["vo_out"]) - float(r["vo_in"])
        src = (r.get("source") or "").strip().upper()
        out = vo_parts_dir / f"a_{int(r['row']):03d}.wav"
        if out.exists() and out.stat().st_size > 100:
            # Still advance cursor for content rows
            if src != "CARD" and not r.get("_last"):
                take = min(dur, max(0.0, vo_dur - vo_cursor))
                vo_cursor += take if take >= 0.05 else 0.0
            parts.append(out)
            continue
        if src == "CARD" or r.get("_last"):
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", f"{dur:.3f}", str(out),
            ])
        else:
            take = min(dur, max(0.0, vo_dur - vo_cursor))
            if take < 0.05:
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-t", f"{dur:.3f}", str(out),
                ])
            elif abs(take - dur) < 0.05:
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{vo_cursor:.3f}", "-t", f"{dur:.3f}", "-i", str(VO),
                    "-ar", "44100", "-ac", "2", str(out),
                ])
                vo_cursor += dur
            else:
                tmp = vo_parts_dir / f"a_{int(r['row']):03d}_raw.wav"
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{vo_cursor:.3f}", "-t", f"{take:.3f}", "-i", str(VO),
                    "-ar", "44100", "-ac", "2", str(tmp),
                ])
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(tmp),
                    "-af", f"apad=pad_dur={dur:.3f}", "-t", f"{dur:.3f}",
                    str(out),
                ])
                vo_cursor += take
        parts.append(out)

    print(f"VO consumed {vo_cursor:.2f}s of {vo_dur:.2f}s", flush=True)

    vo_concat = WORK / "vo_timeline.wav"
    lst = WORK / "audio_concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vo_concat),
    ])

    bed = next(m for m in MUSIC if m.exists())
    bed_dur = probe(bed)
    music_raw = WORK / "music_raw.m4a"
    fade_start = max(0.0, total - 10.0)
    # Cover full runtime: if bed is short, acrossfade-loop the head onto the tail
    # so there is no silence and no hard restart click at bed_dur.
    if bed_dur + 0.05 >= total:
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed),
            "-t", f"{total:.3f}",
            "-af", f"volume=0.12,afade=t=out:st={fade_start:.3f}:d=10",
            "-c:a", "aac", "-b:a", "192k", str(music_raw),
        ])
    else:
        cross = min(4.0, bed_dur / 8.0)
        head = (total - bed_dur) + cross
        fc = (
            f"[0:a]asplit=2[m0][m1];"
            f"[m0]atrim=0:{bed_dur:.3f},asetpts=PTS-STARTPTS[main];"
            f"[m1]atrim=0:{head:.3f},asetpts=PTS-STARTPTS[head];"
            f"[main][head]acrossfade=d={cross:.3f}:c1=tri:c2=tri,"
            f"atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
            f"volume=0.12,afade=t=out:st={fade_start:.3f}:d=10[m]"
        )
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed),
            "-filter_complex", fc, "-map", "[m]",
            "-c:a", "aac", "-b:a", "192k", str(music_raw),
        ])
    print(
        f"music bed={bed_dur:.2f}s → timeline={total:.2f}s "
        f"(acrossfade loop if short)",
        flush=True,
    )

    # Claude Fix 2: normalize=0 so VO is not halved; loudnorm to −14 LUFS.
    mixed = WORK / "mix.m4a"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo_concat), "-i", str(music_raw),
        "-filter_complex",
        "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", "192k", str(mixed),
    ])
    return mixed


def measure_lufs(path: Path) -> dict:
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=framelog=verbose",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = p.stderr
    out: dict = {"raw": ""}
    for line in text.splitlines():
        if "I:" in line and "LUFS" in line and "Integrated" not in line:
            # Summary block lines like "    I:         -14.0 LUFS"
            try:
                out["integrated_lufs"] = float(line.split("I:")[1].split("LUFS")[0].strip())
            except ValueError:
                pass
        if "True peak:" in line or "Peak:" in line and "dBFS" in line:
            pass
        if "LRA:" in line and "LU" in line:
            try:
                out["lra"] = float(line.split("LRA:")[1].split("LU")[0].strip())
            except ValueError:
                pass
        if "True peak:" in line:
            try:
                out["true_peak_dbtp"] = float(line.split("True peak:")[1].split("dBTP")[0].strip())
            except ValueError:
                pass
    # Fallback parse summary section
    if "integrated_lufs" not in out:
        m = re.search(r"I:\s*([-\d.]+)\s*LUFS", text)
        if m:
            out["integrated_lufs"] = float(m.group(1))
    out["raw_tail"] = "\n".join(text.splitlines()[-30:])
    return out


def contact_12(video: Path, rows: list[dict], dest: Path) -> None:
    """12 frames: must include Orbit (22), chapter card (6), row 93, t≈518."""
    must = {
        6: "CARD",
        22: "ORBIT",
        93: "R93",
    }
    by_row = {int(r["row"]): r for r in rows}
    times: list[tuple[float, str]] = []
    for rn, lab in must.items():
        r = by_row[rn]
        t = (float(r["vo_in"]) + float(r["vo_out"])) / 2.0
        times.append((t, f"{rn} {lab}"))
    times.append((518.0, "t=518 SEAM"))
    total = float(rows[-1]["vo_out"])
    need = 12 - len(times)
    for i in range(need):
        t = total * (i + 0.5) / need
        if any(abs(t - mt) < 8.0 for mt, _ in times):
            t = min(total - 1.0, t + 12.0)
        times.append((t, f"t={t:.0f}s"))
    times = sorted(times, key=lambda x: x[0])[:12]

    cells = []
    labels = []
    for i, (t, lab) in enumerate(times):
        p = WORK / f"c12_{i:02d}.png"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-update", "1", str(p),
        ])
        cells.append(Image.open(p).convert("RGB").resize((480, 270), Image.Resampling.LANCZOS))
        labels.append(lab)
    cols, nrows = 4, 3
    board = Image.new("RGB", (cols * 480, nrows * 300 + 40), (12, 12, 14))
    dr = ImageDraw.Draw(board)
    dr.text(
        (12, 10),
        "Saturn first cut v03b — 12-frame (Orbit / card / row 93 / t≈518)",
        font=ImageFont.truetype(FONT, 20), fill=(240, 240, 240),
    )
    fnt = ImageFont.truetype(FONT, 16)
    for i, im in enumerate(cells):
        x, y = (i % cols) * 480, 40 + (i // cols) * 300
        board.paste(im, (x, y))
        dr.text((x + 8, y + 274), labels[i], font=fnt, fill=(255, 220, 40))
    board.save(dest)
    print("wrote", dest, board.size)


def per_row_sheet(row_mp4s: list[tuple[dict, Path]], dest: Path) -> None:
    thumbs = []
    for r, mp4 in row_mp4s:
        dur = max(0.1, probe(mp4))
        p = WORK / f"rowmid_{int(r['row']):03d}.png"
        if not p.exists():
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{dur/2:.3f}", "-i", str(mp4), "-frames:v", "1", "-update", "1", str(p),
            ])
        im = Image.open(p).convert("RGB").resize((320, 180), Image.Resampling.LANCZOS)
        lab = Image.new("RGB", (320, 204), (16, 16, 18))
        lab.paste(im, (0, 0))
        ImageDraw.Draw(lab).text(
            (6, 184), f"{r['row']} {r['source'][:1]} {r['id'][:28]}",
            font=ImageFont.truetype(FONT, 14), fill=(230, 230, 230),
        )
        thumbs.append(lab)
    cols = 6
    nrows = math.ceil(len(thumbs) / cols)
    board = Image.new("RGB", (cols * 320, nrows * 204 + 36), (10, 10, 12))
    ImageDraw.Draw(board).text(
        (10, 8), "Saturn first cut v03b — per-row midframes (v03g)",
        font=ImageFont.truetype(FONT, 20), fill=(240, 240, 240),
    )
    for i, im in enumerate(thumbs):
        board.paste(im, ((i % cols) * 320, 36 + (i // cols) * 204))
    board.save(dest, quality=90)
    print("wrote", dest, board.size)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    UAT_DIR.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    CANT_FILL.clear()

    if not VO.exists():
        sys.exit(f"missing locked VO: {VO}")
    if not GODDARD.exists():
        sys.exit(f"missing Goddard HD: {GODDARD}")

    gw, gh = probe_wh(GODDARD)
    print(f"Goddard {GODDARD.name} {gw}x{gh}", flush=True)
    if gh < 1000:
        sys.exit("Goddard file is not HD — refuse Twitter 720p")

    pool = {e["nasa_id"]: e for e in json.loads(POOL_JSON.read_text())}
    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    rows[-1]["_last"] = True
    total = float(rows[-1]["vo_out"])
    print(f"rows={len(rows)} picture_end={total:.2f}s VO={probe(VO):.2f}s", flush=True)

    # Fresh picture rows for v03 (do not reuse v02 letterboxed stills)
    row_mp4s: list[tuple[dict, Path]] = []
    for r in rows:
        dest = WORK / f"row_{int(r['row']):03d}.mp4"
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"reuse row {r['row']}", flush=True)
            # Still record cant-fill for NASA if we can measure from source
            if (r.get("source") or "").upper() == "NASA":
                still = resolve_nasa(r["id"], pool)
                sw, sh = Image.open(still).size
                cov = cover_scale(sw, sh)
                if cov > MAX_COVER + 1e-9 and not any(c["row"] == str(r["row"]) for c in CANT_FILL):
                    CANT_FILL.append({
                        "row": str(r["row"]), "id": r["id"], "w": sw, "h": sh,
                        "cover": round(cov, 3),
                    })
        else:
            print(f"build row {r['row']} {r['source']} {r['id'][:40]}", flush=True)
            build_row_clip(r, pool, dest)
        row_mp4s.append((r, dest))

    picture = WORK / "picture_all.mp4"
    # Rebuild picture if any row is newer than picture_all
    rebuild = True
    if picture.exists() and picture.stat().st_size > 1_000_000:
        newest = max(p.stat().st_mtime for _, p in row_mp4s)
        if picture.stat().st_mtime >= newest - 1:
            rebuild = False
            print(f"reuse picture_all ({picture.stat().st_size} bytes)", flush=True)
    if rebuild:
        concat_videos([p for _, p in row_mp4s], picture)

    audio = build_audio(rows, total)

    fade_pic_start = max(0.0, total - 2.0)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(audio),
        "-filter_complex",
        f"[0:v]fade=t=out:st={fade_pic_start:.3f}:d=2,format=yuv420p[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(OUT_LOCAL),
    ])
    print(f"LOCAL {OUT_LOCAL} {probe(OUT_LOCAL):.2f}s", flush=True)

    lufs = measure_lufs(OUT_LOCAL)
    print(f"LUFS integrated={lufs.get('integrated_lufs')} LRA={lufs.get('lra')}", flush=True)

    vo_lufs = measure_lufs(VO)
    print(
        f"VO-only LUFS integrated={vo_lufs.get('integrated_lufs')} "
        f"LRA={vo_lufs.get('lra')}",
        flush=True,
    )

    contact_12(OUT_LOCAL, rows, WORK / "contact12.png")
    chunk_write(WORK / "contact12.png", UAT_DIR / "saturn_first_cut_v03b_contact12.png")
    shutil.copy2(WORK / "contact12.png", ART / "saturn_first_cut_v03b_contact12.png")

    per_row_sheet(row_mp4s, WORK / "per_row.png")
    chunk_write(WORK / "per_row.png", UAT_DIR / "saturn_first_cut_v03b_per_row.png")
    shutil.copy2(WORK / "per_row.png", REVIEW / "saturn_first_cut_v03b_per_row.png")

    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v03b.mp4")

    h = hashlib.sha256()
    with open(OUT_LOCAL, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)

    cant_sorted = sorted(CANT_FILL, key=lambda x: int(x["row"]))
    (WORK / "CANT_FILL_ROWS.json").write_text(json.dumps(cant_sorted, indent=2))
    chunk_write(
        json.dumps(cant_sorted, indent=2).encode(),
        UAT_DIR / "CANT_FILL_ROWS.json",
    )

    meta = {
        "cut": "v03b",
        "shot_list": "shot_list_v03g.csv",
        "vo": str(VO.name),
        "duration": probe(OUT_LOCAL),
        "sha256": h.hexdigest(),
        "goddard": f"{gw}x{gh}",
        "row93": "PIA21351 (replaced near-black PIA12633; temp until Omni)",
        "row_still_override": ROW_STILL_OVERRIDE,
        "framing": "cover if cover_scale<=2; else feathered blur_bg (no hard seams)",
        "zoompan": "4x scale before zoompan; x/y=iw/zoom",
        "chapter_cards": f"soft starfield, Arial Bold ~{CARD_FONT_SIZE}pt wrapped",
        "loudness": {
            "mix_integrated_lufs": lufs.get("integrated_lufs"),
            "mix_lra": lufs.get("lra"),
            "vo_integrated_lufs": vo_lufs.get("integrated_lufs"),
            "vo_lra": vo_lufs.get("lra"),
        },
        "cant_fill_rows": cant_sorted,
        "cant_fill_count": len(cant_sorted),
        "music": "saturn-rings_score_bed_v01.mp3 acrossfade-looped to full runtime",
        "icloud": str(UAT_DIR),
        "note": "media iCloud only; no force-add to git",
    }
    (WORK / "META.json").write_text(json.dumps(meta, indent=2))
    chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    (ART / "saturn_first_cut_v03b_ARRIVAL.json").write_text(json.dumps(meta, indent=2))
    print("DONE", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
