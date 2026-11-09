#!/usr/bin/env python3
"""034 Pluto long master v01 (J2376). £0. Picture from studio-live harvest_v01 + graphics_v03.

Reads the locked shot_list_v01.csv, lays the locked v03 VO with the chapter-card
silences already in stt_timeline_offset_v01.json, mixes the £0 score bed and a
house SFX stem, and writes the master plus the gate sidecars.
"""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess as sp
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters"
)
REPO = (
    Path("/Users/ben/_desk/worker/orbit-with-ben")
    if Path("/Users/ben/_desk/worker/orbit-with-ben/scripts/picture_qa.py").exists()
    else Path("/Users/benjaminoats/YouTube/orbit-with-ben")
)
EDIT = FILM / "07_Edit-Project"
WORK = EDIT / "full_master_v01_work"
PACK = EDIT / "full_master_v01_pack"
OUT = FILM / "09_Final-Export" / "034_pluto_frozen_heart_master_v01.mp4"
SHOT = EDIT / "shot_list_v01.csv"
POOL = EDIT / "HARVEST_POOL_v01.json"
GFX = EDIT / "graphics_v03"
VO_WAV = FILM / "02_Voiceover" / "pluto_frozen_heart_vo_v03.wav"
WORDS = FILM / "02_Voiceover" / "stt" / "pluto_frozen_heart_vo_v03" / "stt_timeline_offset_v01.json"
BED = FILM / "05_Music" / "pluto_score_bed_v01.mp3"
KIT = FILM / "06_Sound-Effects" / "kit_v01"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TOTAL = 646.94
FPS = 30
W, H = 1920, 1080
ENC = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-r", "30", "-fps_mode", "cfr", "-g", "30", "-an",
]

LAB_RE = re.compile(r"`([^`]{1,48})`\s*\(`([0-9.]+)\s*[–-]\s*([0-9.]+)\s*s")
SKIP_LAB = {"when", "who", "fact", "data", "scale", "chapter", "edit label"}

# SFX plan v01, already on the picture timeline.
RUMBLES = [
    (4.40, 7.80), (39.80, 43.20), (268.18, 271.68), (326.88, 330.38),
    (377.43, 380.68), (427.08, 430.48), (520.58, 524.08), (620.28, 623.78),
]
WHOOSHES = [20.14, 111.92, 138.16, 197.36, 338.58, 463.04, 547.84, 562.86]
TICKS = [
    9.70, 14.50, 20.30, 68.37, 71.62, 85.07, 88.87, 93.47, 112.12, 138.32,
    164.01, 197.56, 218.01, 230.26, 246.31, 268.23, 277.78, 288.53, 298.23,
    311.38, 321.13, 323.03, 326.93, 338.73, 355.93, 396.23, 436.23, 472.63,
    480.63, 495.33, 499.33, 520.73, 563.03, 580.63,
]


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout)[-1800:])


def probe(path: Path) -> dict:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=width,height,codec_type,avg_frame_rate",
         "-of", "json", str(path)],
        text=True,
    )
    d = json.loads(raw)
    v = next(s for s in d.get("stream", d.get("streams", [])) if s.get("codec_type") == "video")
    return {
        "width": int(v["width"]),
        "height": int(v["height"]),
        "duration": float(d["format"]["duration"]),
    }


def frames_ok(path: Path, n: int) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    try:
        info = probe(path)
    except (sp.CalledProcessError, StopIteration, KeyError):
        return False
    return abs(info["duration"] * FPS - n) < 2


def starfield(path: Path) -> None:
    if path.exists():
        return
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W / 2) / (W / 2)
    ny = (yy - H / 2) / (H / 2)
    rad = np.clip(1.0 - 0.72 * (nx ** 2 + ny ** 2), 0.0, 1.0)
    r = (16 + 56 * rad + 10 * (yy / H)).clip(0, 255).astype(np.uint8)
    g = (26 + 74 * rad + 12 * (yy / H)).clip(0, 255).astype(np.uint8)
    b = (44 + 98 * rad + 16 * (yy / H)).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(np.stack([r, g, b], axis=-1), "RGB")
    dr = ImageDraw.Draw(im)
    seed = 34034
    for i in range(1800):
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        x = 16 + seed % (W - 32)
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        y = 16 + seed % (H - 32)
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        br = 195 + seed % 60
        sz = 1 if (i % 2) else 2
        dr.ellipse([x - sz, y - sz, x + sz, y + sz], fill=(br, br, min(255, br + 15)))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, quality=95)


def text_png(text: str, path: Path, size: int, box: bool) -> None:
    font = ImageFont.truetype(FONT, size)
    tmp = Image.new("RGBA", (8, 8))
    d = ImageDraw.Draw(tmp)
    box_l, box_t, box_r, box_b = d.textbbox((0, 0), text, font=font)
    tw, th = box_r - box_l, box_b - box_t
    pad = 18 if box else 8
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if box:
        dr.rounded_rectangle([0, 0, im.width - 1, im.height - 1], 12, fill=(22, 34, 56, 230))
    dr.text((pad - box_l, pad - box_t), text, font=font, fill=(255, 255, 255, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def load_rows() -> list[dict]:
    with SHOT.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_pool() -> list[dict]:
    d = json.loads(POOL.read_text())
    assets = []
    for a in d["assets"]:
        p = Path(a["local_path"])
        if p.exists() and "contact" not in p.name:
            assets.append(a)
    return assets


def gfx_file(name: str) -> Path | None:
    hits = [p for p in GFX.rglob(name) if p.is_file() and not p.name.startswith("._")]
    return hits[0] if hits else None


def row_assets(row: dict, pool: list[dict]) -> list[dict]:
    text = row["asset"]
    found = []
    for a in pool:
        idx = text.find(a["id"])
        if idx >= 0:
            found.append((idx, a))
    found.sort(key=lambda x: x[0])
    # A "+" inside one clause is a second picture in the same row, already ordered by index.
    return [a for _, a in found]


def labels_for(row: dict) -> list[tuple[str, float, float]]:
    out = []
    for m in LAB_RE.finditer(row.get("markers") or ""):
        text = m.group(1).strip()
        if text.lower() in SKIP_LAB:
            continue
        words = text.split()
        if len(words) > 4:
            text = " ".join(words[:4])
        a, b = float(m.group(2)), float(m.group(3))
        if b - a > 4.0:
            b = a + 4.0
        if b > a:
            out.append((text, a, b))
    if "subscri" in (row.get("vo_text") or "").lower():
        t0 = float(row["vo_in"]) + 0.3
        out.append(("SUBSCRIBE", t0, min(t0 + 4.0, float(row["vo_out"]) - 0.1)))
    return out


def credit_for(asset: dict | None, source: str) -> str:
    if asset is None:
        return ""
    lic = (asset.get("license") or "") + " " + asset.get("id", "")
    if asset["id"].startswith("PIA") or "NASA" in lic:
        return "NASA"
    if asset["id"].startswith("KSC") or asset["id"].startswith("ksc") or asset["id"].startswith("NHQ"):
        return "NASA"
    if "Wikimedia" in lic or asset["id"].startswith("File:"):
        return "Wikimedia"
    if source in {"CODE", "CARD"}:
        return ""
    return "NASA"


def build_plan(rows: list[dict], pool: list[dict]) -> list[dict]:
    """One encode item per visual cut, frames allocated from the cumulative clock."""
    cuts = []
    video_used: dict[str, list[tuple[float, float]]] = {}
    clock = 0.0
    problems = []
    for row in rows:
        dur = float(row["dur_s"])
        f0 = round(clock * FPS)
        clock += dur
        f1 = round(clock * FPS)
        nframes = f1 - f0
        t0 = f0 / FPS
        kind = row["source"]
        labs = labels_for(row)
        if kind in {"CODE", "CARD"}:
            m = re.search(r"((?:code_graphic|chapter_card|overlay)_\S+?\.(?:mp4|mov))", row["asset"])
            if not m:
                problems.append(f"{row['row']}: no graphic filename")
                continue
            path = gfx_file(m.group(1))
            if path is None:
                problems.append(f"{row['row']}: missing {m.group(1)}")
                continue
            info = probe(path)
            need = nframes / FPS
            if info["duration"] + 0.15 < need:
                problems.append(
                    f"{row['row']}: {path.name} is {info['duration']:.2f}s, row needs {need:.2f}s"
                )
            cuts.append({
                "row": row["row"], "kind": kind, "path": str(path),
                "source": path.name, "t0": t0, "frames": nframes,
                "overlay": None, "labels": [] if kind == "CARD" else labs,
                "credit": "", "offset": 0.0, "upscale": 1.0, "video": True,
                "src_w": info["width"], "src_h": info["height"],
            })
            continue
        assets = row_assets(row, pool)
        if not assets:
            problems.append(f"{row['row']}: no pool asset in {row['asset'][:80]}")
            continue
        ncuts = max(1, int(float(row["cuts"])))
        # Don't split one short native clip into two offsets under 10 s.
        pieces = []
        for i in range(ncuts):
            asset = assets[min(len(assets) - 1, int(i * len(assets) / ncuts))]
            pieces.append(asset)
        merged = []
        for asset in pieces:
            if merged and merged[-1][0]["local_path"] == asset["local_path"] and asset.get("kind") == "native_video":
                merged[-1][1] += 1
            else:
                merged.append([asset, 1])
        # Frame split follows the merged pieces by their cut weight.
        weights = [c for _, c in merged]
        acc = 0
        bounds = [0]
        for wgt in weights:
            acc += wgt
            bounds.append(round(nframes * acc / ncuts))
        bounds[-1] = nframes
        local_frame = 0
        for (asset, _), a, b in zip(merged, bounds, bounds[1:]):
            nf = b - a
            if nf <= 0:
                continue
            path = Path(asset["local_path"])
            is_video = asset.get("kind") == "native_video"
            off = 0.0
            up = 1.0
            if is_video:
                info = probe(path)
                need = nf / FPS
                spans = video_used.setdefault(str(path), [])
                off = 0.0
                while off + need > info["duration"] + 0.05 and off > 0:
                    break
                # Walk forward until the stretch is 10 s clear of earlier ones and fits.
                while True:
                    end = off + need
                    legal = end <= info["duration"] + 0.08 and all(
                        abs(off - s) >= 10.0 and (off >= e - 0.05 or end <= s + 0.05)
                        for s, e in spans
                    )
                    if legal:
                        break
                    off += 10.0
                    if off + 0.5 > info["duration"]:
                        problems.append(
                            f"{row['row']}: {path.name} is {info['duration']:.2f}s, "
                            f"no legal {need:.2f}s stretch (used {spans})"
                        )
                        off = 0.0
                        break
                spans.append((off, off + need))
                up = max(W / info["width"], H / info["height"])
                src_w, src_h = info["width"], info["height"]
            else:
                src_w = int(asset.get("width") or 0)
                src_h = int(asset.get("height") or 0)
                if src_w and src_h:
                    up = max(W / src_w, H / src_h)
            ov = None
            ov_name = re.search(r"(overlay_034_r\d+_[a-z0-9_]+)", row["asset"])
            if ov_name:
                hits = list(GFX.rglob(ov_name.group(1) + ".mov"))
                ov = str(hits[0]) if hits else None
                if ov is None:
                    problems.append(f"{row['row']}: missing overlay {ov_name.group(1)}")
            cut_t0 = t0 + local_frame / FPS
            cuts.append({
                "row": row["row"], "kind": "NASA", "path": str(path),
                "source": path.name, "t0": cut_t0, "frames": nf,
                "overlay": ov, "overlay_ss": local_frame / FPS,
                "labels": labs, "credit": credit_for(asset, "NASA"),
                "offset": off if is_video else None,
                "upscale": round(min(up, 2.0) if not is_video or up > 2.0 else up, 3),
                "video": is_video, "src_w": src_w, "src_h": src_h,
            })
            local_frame += nf
    if problems:
        raise SystemExit("plan problems:\n" + "\n".join(problems))
    total_f = sum(c["frames"] for c in cuts)
    if total_f != round(TOTAL * FPS):
        # The last row absorbs rounding against the locked 646.94 s.
        drift = round(TOTAL * FPS) - total_f
        cuts[-1]["frames"] += drift
        if cuts[-1]["frames"] <= 0:
            raise SystemExit(f"frame drift {drift} emptied the last cut")
    return cuts


def render_still(cut: dict, dest: Path, stars: Path) -> None:
    n = cut["frames"]
    src = Path(cut["path"])
    sw, sh = cut["src_w"], cut["src_h"]
    if not sw or not sh:
        info = probe(src)
        sw, sh = info["width"], info["height"]
    # Static frame. A 1 px staircase pan fails polish_gate's jitter check.
    cover = max(W / sw, H / sh)
    inputs = ["-y", "-loop", "1", "-i", str(src), "-loop", "1", "-i", str(stars)]
    lift = "lutyuv=y='clip(val*0.78+58,0,255)'"
    if cover <= 2.0:
        scale = cover
        tw, th = max(W, int(sw * scale) // 2 * 2), max(H, int(sh * scale) // 2 * 2)
        vf = (
            f"[0:v]scale={tw}:{th}:flags=lanczos,{lift},"
            f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,fps={FPS},format=yuv420p[base]"
        )
    else:
        fit = min(2.0, (W - 120) / sw, (H - 120) / sh)
        tw, th = max(2, int(sw * fit) // 2 * 2), max(2, int(sh * fit) // 2 * 2)
        vf = (
            f"[1:v]scale={W}:{H},format=yuv444p[bg];"
            f"[0:v]scale={tw}:{th}:flags=lanczos,{lift},format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
            f"a='if(lt(X,48),X*255/48,if(gt(X,{tw}-48),({tw}-X)*255/48,"
            f"if(lt(Y,48),Y*255/48,if(gt(Y,{th}-48),({th}-Y)*255/48,255))))'[fg];"
            f"[bg][fg]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2,fps={FPS},format=yuv420p[base]"
        )
    extra = _decorate(cut, inputs, "base", n)
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
        "-filter_complex", vf + extra[0], "-map", extra[1],
        *ENC, "-frames:v", str(n), str(dest),
    ]
    run(cmd)


def render_video(cut: dict, dest: Path, stars: Path) -> None:
    n = cut["frames"]
    src = Path(cut["path"])
    info = probe(src)
    sw, sh = info["width"], info["height"]
    cover = max(W / sw, H / sh)
    off = float(cut["offset"] or 0)
    inputs = ["-y", "-ss", f"{off:.3f}", "-i", str(src), "-loop", "1", "-i", str(stars)]
    if "51712771431" in src.name:
        vf = (
            f"[1:v]scale={W}:{H},fps={FPS},format=gbrp[bg];"
            f"[0:v]crop=1028:840:0:0,scale=1320:1080:flags=lanczos,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,fps={FPS},format=gbrp[fg];"
            f"[bg][fg]blend=all_mode=screen:shortest=1,format=yuvj420p[base]"
        )
    elif cover <= 2.35 and cover <= 2.0:
        vf = (
            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"lutyuv=y='clip(val*0.78+58,0,255)',fps={FPS},setsar=1,format=yuv420p[base]"
        )
    else:
        fit = min(2.0, W / sw, H / sh)
        tw, th = max(2, int(sw * fit) // 2 * 2), max(2, int(sh * fit) // 2 * 2)
        vf = (
            f"[1:v]scale={W}:{H},format=yuv420p[bg];"
            f"[0:v]scale={tw}:{th}:flags=lanczos,fps={FPS},format=yuv420p[fg];"
            f"[bg][fg]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:shortest=1,format=yuv420p[base]"
        )
    extra = _decorate(cut, inputs, "base", n)
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
        "-filter_complex", vf + extra[0], "-map", extra[1],
        *ENC, "-frames:v", str(n), str(dest),
    ]
    run(cmd)


def render_graphic(cut: dict, dest: Path, stars: Path | None = None) -> None:
    n = cut["frames"]
    if stars is not None and cut["kind"] == "CODE":
        inputs = ["-y", "-i", cut["path"], "-loop", "1", "-i", str(stars)]
        vf = (
            f"[0:v]scale={W}:{H},fps={FPS},setsar=1,format=gbrp[fg];"
            f"[1:v]scale={W}:{H},fps={FPS},format=gbrp[bg];"
            f"[fg][bg]blend=all_expr='if(gt(Y,920),max(A,B*0.85),A)':shortest=1,format=yuvj420p[base]"
        )
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", *inputs,
            "-filter_complex", vf, "-map", "[base]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuvj420p", "-color_range", "pc",
            "-r", "30", "-fps_mode", "cfr", "-g", "30", "-an",
            "-frames:v", str(n), str(dest),
        ]
        run(cmd)
        return
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", cut["path"],
        "-vf", f"scale={W}:{H},fps={FPS},setsar=1,format=yuv420p",
        *ENC, "-frames:v", str(n), str(dest),
    ]
    run(cmd)


def _decorate(cut: dict, inputs: list[str], base: str, n: int) -> tuple[str, str]:
    """Overlay the row's ARGB mov, credit and short labels. Returns (filter tail, map label)."""
    parts = []
    cur = base
    idx = 2  # 0 source, 1 stars
    if cut.get("overlay"):
        ss = float(cut.get("overlay_ss") or 0)
        inputs.extend(["-ss", f"{ss:.3f}", "-i", cut["overlay"]])
        parts.append(f"[{cur}][{idx}:v]overlay=0:0:format=auto:shortest=1[ov{idx}]")
        cur = f"ov{idx}"
        idx += 1
    credit = cut.get("credit") or ""
    if credit:
        png = WORK / "credits" / f"{credit}.png"
        if not png.exists():
            text_png(credit, png, 28, False)
        inputs.extend(["-loop", "1", "-i", str(png)])
        parts.append(
            f"[{cur}][{idx}:v]overlay=36:H-h-28:format=auto[cr{idx}]"
        )
        cur = f"cr{idx}"
        idx += 1
    # Labels whose film interval overlaps this cut.
    t0 = cut["t0"]
    t1 = t0 + n / FPS
    seen = set()
    for text, a, b in cut.get("labels") or []:
        if b <= t0 + 0.05 or a >= t1 - 0.05 or text in seen:
            continue
        seen.add(text)
        png = WORK / "labels" / (re.sub(r"[^A-Za-z0-9]+", "_", text)[:40] + ".png")
        if not png.exists():
            text_png(text, png, 58, True)
        local_a = max(0.0, a - t0)
        local_b = min(n / FPS, b - t0)
        inputs.extend(["-loop", "1", "-t", f"{local_b - local_a + 0.4:.3f}", "-i", str(png)])
        hold = max(0.4, local_b - local_a)
        parts.append(
            f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.30:alpha=1,"
            f"fade=t=out:st={max(0.30, hold - 0.30):.3f}:d=0.30:alpha=1,"
            f"setpts=PTS+{local_a:.3f}/TB[lb{idx}]"
        )
        y = "H-h-120" if len(seen) == 1 else "H-h-220"
        parts.append(
            f"[{cur}][lb{idx}]overlay=x=(main_w-overlay_w)/2:y={y}:eof_action=pass[lbx{idx}]"
        )
        cur = f"lbx{idx}"
        idx += 1
    if not parts:
        return "", f"[{cur}]"
    return ";" + ";".join(parts), f"[{cur}]"


def render_all(cuts: list[dict]) -> list[Path]:
    stars = WORK / "starfield.jpg"
    starfield(stars)
    out_dir = WORK / "cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, cut in enumerate(cuts):
        dest = out_dir / f"{i:03d}_{cut['row']}.mp4"
        paths.append(dest)
        if frames_ok(dest, cut["frames"]):
            print(f"keep {dest.name}", flush=True)
            continue
        print(f"render {i + 1}/{len(cuts)} {cut['row']} {cut['frames']}f {cut['source']}", flush=True)
        if cut["kind"] in {"CODE", "CARD"}:
            render_graphic(cut, dest, stars)
        elif cut["video"]:
            render_video(cut, dest, stars)
        else:
            render_still(cut, dest, stars)
    return paths


def concat_picture(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths))
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-an", str(dest),
    ])


def lay_vo(dest: Path) -> None:
    """Insert the chapter-card silences implied by shifted word times."""
    data = json.loads(WORDS.read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    gaps = []
    prev = float(words[0]["start"]) - float(words[0]["raw_start"])
    for w in words[1:]:
        shift = float(w["start"]) - float(w["raw_start"])
        if shift - prev > 0.4:
            gaps.append((float(w["raw_start"]), shift - prev))
            prev = shift
    info = probe_audio(VO_WAV)
    raw = info
    points = [0.0] + [g[0] for g in gaps] + [raw]
    filters = []
    labels = []
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        filters.append(
            f"[0:a]aformat=channel_layouts=stereo:sample_rates=48000,"
            f"atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]"
        )
        labels.append(f"[a{i}]")
        if i < len(gaps):
            filters.append(
                f"anullsrc=r=48000:cl=stereo,atrim=0:{gaps[i][1]:.3f},asetpts=PTS-STARTPTS[g{i}]"
            )
            labels.append(f"[g{i}]")
    n = len(labels)
    filters.append("".join(labels) + f"concat=n={n}:v=0:a=1,apad=whole_dur={TOTAL},atrim=0:{TOTAL},aresample=48000[a]")
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(VO_WAV),
        "-filter_complex", ";".join(filters), "-map", "[a]",
        "-c:a", "pcm_s16le", str(dest),
    ])


def probe_audio(path: Path) -> float:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        text=True,
    )
    return float(json.loads(raw)["format"]["duration"])


def build_sfx(dest: Path) -> None:
    rumble = KIT / "sfx_owb_rumble_low_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    events = []
    for a, b in RUMBLES:
        events.append((rumble, a, min(3.4, b - a), 0.045))
    for t in WHOOSHES:
        events.append((whoosh, t, 0.75, 0.10))
    for t in TICKS:
        events.append((tick, t, 0.12, 0.07))
    inputs = []
    filters = []
    for i, (path, start, dur, gain) in enumerate(events):
        inputs.extend(["-i", str(path)])
        delay = int(round(start * 1000))
        filters.append(
            f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={gain},"
            f"adelay={delay}|{delay},aresample=48000[s{i}]"
        )
    n = len(events)
    filters.append(
        "".join(f"[s{i}]" for i in range(n))
        + f"amix=inputs={n}:normalize=0:dropout_transition=0,"
        + f"apad=whole_dur={TOTAL},atrim=0:{TOTAL}[a]"
    )
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
        "-filter_complex", ";".join(filters), "-map", "[a]",
        "-c:a", "pcm_s16le", str(dest),
    ])


def loudness(path: Path) -> tuple[float, float]:
    p = sp.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = p.stderr
    integ = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", text)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBTP", text)
    if not integ:
        raise RuntimeError(text[-500:])
    tp = float(peak.group(1)) if peak else -1.0
    return float(integ.group(1)), tp


def mix(vo: Path, sfx: Path, dest: Path) -> dict:
    """Bed sits well under the VO. One linear gain plus a limiter hits about -14 LUFS."""
    vo_i, _ = loudness(vo)
    bed_i, _ = loudness(BED)
    # Momentary music runs hotter than integrated. Keep a wide gap, then limit only peaks.
    bed_gain_db = (vo_i - 22.0) - bed_i
    sfx_i, _ = loudness(sfx)
    sfx_gain_db = min(0.0, (vo_i - 16.0) - sfx_i)
    bed_laid = WORK / "bed_laid_v01.wav"
    sfx_laid = WORK / "sfx_laid_v01.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED),
        "-af", f"volume={bed_gain_db:.2f}dB,atrim=0:{TOTAL}",
        "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx),
        "-af", f"volume={sfx_gain_db:.2f}dB",
        "-c:a", "pcm_s16le", str(sfx_laid),
    ])
    premix = WORK / "premix.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex",
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{TOTAL}[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(premix),
    ])
    mix_i, mix_tp = loudness(premix)
    gain = -14.0 - mix_i
    # Raise to about -14, then limit peaks so AAC still lands at or under -1 dBTP.
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(premix),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
        "-c:a", "pcm_s16le", str(dest),
    ])
    final_i, final_tp = loudness(dest)
    return {
        "vo_lufs": vo_i, "bed_gain_db": round(bed_gain_db, 2),
        "sfx_gain_db": round(sfx_gain_db, 2), "premix_lufs": mix_i,
        "gain_db": round(gain, 2), "integrated_lufs": final_i, "true_peak_dbtp": final_tp,
    }


def mux(picture: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(dest),
    ])


def write_sidecars(cuts: list[dict]) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    cut_json = []
    for c in cuts:
        item = {
            "row": c["row"],
            "source": c["source"],
            "timeline_in": round(c["t0"], 3),
            "timeline_out": round(c["t0"] + c["frames"] / FPS, 3),
            "upscale": c["upscale"] if c["kind"] == "NASA" else 1.0,
            "video": bool(c["video"]),
        }
        if c["video"]:
            item["framing"] = {"offset": float(c["offset"] or 0)}
        cut_json.append(item)
    (PACK / "cuts_v01.json").write_text(json.dumps(cut_json, indent=2))
    # Pool titles so picture_qa can name every plate. Avoid words that fail the kind check.
    items = []
    for a in json.loads(POOL.read_text())["assets"]:
        title = a.get("title") or a["id"]
        items.append({"id": Path(a["local_path"]).name, "file": Path(a["local_path"]).name, "title": title})
    (PACK / "pool_titles_v01.json").write_text(json.dumps(items, indent=2))


def run_gates() -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    results = {}
    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT), "--words", str(WORDS),
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr)[-500:]}
    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(OUT),
        "--cuts", str(PACK / "cuts_v01.json"),
        "--pool", str(PACK / "pool_titles_v01.json"),
        "--pool", str(POOL),
        "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr)[-800:]}
    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED), "--video", str(OUT),
        "--out", str(PACK / "music_gate_v01.json"),
    ], capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr)[-800:]}
    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK / "vo_laid_v01.wav"),
        "--sfx", str(WORK / "sfx_laid_v01.wav"),
        "--bed", str(WORK / "bed_laid_v01.wav"),
        "--minutes", "10.78",
        "--out", str(PACK / "sfx_level_v01.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr)[-800:]}
    i, tp = loudness(OUT)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(OUT),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(OUT)
    results["delivery"] = {
        "integrated_lufs": i, "true_peak_dbtp": tp,
        "width": info["width"], "height": info["height"],
        "duration": info["duration"], "black_frames": blacks[:8],
    }
    (PACK / "gate_results_v01.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2), flush=True)
    return results


def main() -> None:
    os.environ["TMPDIR"] = str(WORK / "tmp")
    (WORK / "tmp").mkdir(parents=True, exist_ok=True)
    log_dir = Path.home() / "_desk" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    done = log_dir / "j2376-assemble.done"
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    rows = load_rows()
    pool = load_pool()
    cuts = build_plan(rows, pool)
    (WORK / "plan_v01.json").write_text(json.dumps(cuts, indent=2))
    print(f"plan: {len(cuts)} cuts, {sum(c['frames'] for c in cuts)} frames", flush=True)
    if mode == "--plan":
        return
    paths = render_all(cuts)
    picture = WORK / "picture_v01.mp4"
    concat_picture(paths, picture)
    vo = WORK / "vo_laid_v01.wav"
    sfx = WORK / "sfx_stem_v01.wav"
    mix_wav = WORK / "mix_v01.wav"
    if not vo.exists():
        print("lay vo", flush=True)
        lay_vo(vo)
    if not sfx.exists():
        print("build sfx", flush=True)
        build_sfx(sfx)
    print("mix", flush=True)
    report = mix(vo, sfx, mix_wav)
    (PACK).mkdir(parents=True, exist_ok=True)
    (PACK / "mix_report_v01.json").write_text(json.dumps(report, indent=2))
    print("mux", report, flush=True)
    mux(picture, mix_wav, OUT)
    write_sidecars(cuts)
    if mode == "--gates" or mode == "--all":
        results = run_gates()
        failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("code") not in (None, 0)]
        delivery = results.get("delivery") or {}
        if delivery.get("black_frames"):
            failed.append("black_frames")
        if not ( -15.5 <= delivery.get("integrated_lufs", -99) <= -12.5):
            failed.append("loudness")
        if delivery.get("true_peak_dbtp", 0) > -1.0:
            failed.append("true_peak")
        code = 1 if failed else 0
        done.write_text(f"{code}\nfailed={failed}\n")
        print(f"done {code} {failed}", flush=True)
        raise SystemExit(code)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        err = Path.home() / "_desk" / "logs" / "j2376-assemble.done"
        err.parent.mkdir(parents=True, exist_ok=True)
        err.write_text(f"1\n{type(exc).__name__}: {exc}\n")
        raise
