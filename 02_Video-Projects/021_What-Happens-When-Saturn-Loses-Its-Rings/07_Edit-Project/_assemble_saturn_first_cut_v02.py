#!/usr/bin/env python3
"""Saturn first cut v02 — assemble from shot_list_v03g.csv + locked VO.

Ben 1 Oct evening: OK assemble with temp PIA12633 in row 93.
Claude assembler notes: fit-to-height for ~1020 square stills; fill only large
originals; Goddard from local 1080p HD muted; VO untouched with silence at cards;
end hold music fade; 12-frame contact + per-row midframes to iCloud (no media in git).

Does not upload. Does not freeze-extend short motion clips.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

EP = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SHOT = HERE / "shot_list_v03g.csv"
POOL_JSON = HERE / "nasa_pool_v01.json"
POOL_DIR = HERE / "nasa_pool_v01"
VO = EP / "02_Voiceover/parts/saturn_rings_vo_v03b_tightened_LOCK.wav"
CLIPS = EP / "04_Generated-Clips"
GODDARD = HERE / "_uat_v03c_ben1543/SVS_12672_ring_rain.mp4"
WORK = HERE / "saturn_film/work_first_cut_v02"
OUT_LOCAL = HERE / "saturn_film/saturn_first_cut_v02.mp4"
REVIEW = HERE / "review"  # local only; copy sheets to iCloud (Ben: no media in git)
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_DIR = UAT / "saturn_first_cut_v02"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/assets"
)

MUSIC = [
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part02_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part03_score_bed_v01.mp3"),
]

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
# Large originals may fill 16:9; everything else fit-to-height on black (~1.06x for 1020).
FILL_IDS = {
    "PIA11667", "PIA06193", "PIA17474", "PIA17218", "PIA21345",
    "PIA11141", "PIA16842", "PIA10081",
    "PIA21439", "PIA22767", "PIA21440", "PIA22766", "PIA22768",  # Grand Finale illustrations
}

AI_PATHS = {
    "edit_ice_chunks_v07.mp4": CLIPS / "v07/edit_ice_chunks_v07.mp4",
    "veo_young_rings_v01.mp4": CLIPS / "veo_world_v01/veo_young_rings_v01.mp4",
    "veo_bare_saturn_v05.mp4": CLIPS / "veo_v05/veo_bare_saturn_v05.mp4",
    "veo_orbit_tumble_v03_fallback_0-3s.mp4": CLIPS / "v07/veo_orbit_tumble_v03_fallback_0-3s.mp4",
}


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd[:14]), flush=True)
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
            time.sleep(0.25)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.0 * (attempt + 1))
    Path("/tmp").joinpath(f"uat_stage_{dest.name}").write_bytes(data)


def parse_push(move: str) -> float:
    """Return zoom end factor from 'push 6%' / 'slow push 7%'."""
    if not move:
        return 1.06
    m = re.search(r"([\d.]+)\s*%", move)
    if m:
        return 1.0 + float(m.group(1)) / 100.0
    if "slow" in move.lower():
        return 1.07
    return 1.06


def starfield_card(title: str, path: Path) -> None:
    im = Image.new("RGB", (W, H), "#070b14")
    px = im.load()
    for y in range(H):
        t = y / H
        r, g, b = int(7 + 8 * t), int(11 + 14 * t), int(20 + 22 * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(im)
    for x, y in (
        (180, 120), (420, 200), (700, 90), (980, 240), (1400, 140),
        (220, 700), (800, 780), (1200, 640), (1600, 720), (500, 500),
    ):
        draw.ellipse((x, y, x + 2, y + 2), fill=(210, 216, 230))
    f = ImageFont.truetype(FONT, 64)
    bbox = draw.textbbox((0, 0), title, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) / 2
    y = (H - th) / 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x, y + 2), title, font=f, fill=(0, 0, 0, 90))
    im = im.convert("RGBA")
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text((x, y), title, font=f, fill=(244, 246, 250, 255))
    im.convert("RGB").save(path)


def caption_png(text: str, path: Path) -> None:
    """Small lower-left caption; consistent Title case for Illustration."""
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


def still_to_mp4(still: Path, dest: Path, dur: float, zoom_end: float, fill: bool) -> None:
    """Ken-Burns still. Contain on black unless fill=True (large original / illustration).

    Square ~1020 pool stills → fit-to-height (~1.06x) via contain. Wider-than-16:9
    stills fit-to-width instead (pad cannot shrink). Never crop-upscale a small pool
    still to fill 16:9 (~1.9x).
    """
    if dur < 0.25:
        dur = 0.25
    n = max(1, int(round(dur * FPS)))
    z0, z1 = 1.0, min(zoom_end, 1.12)  # keep push gentle on letterboxed stills
    zf = f"{z0:.4f}+({z1 - z0:.4f})*on/{max(n - 1, 1)}"
    xf = "(iw-ow/zoom)/2"
    yf = "(ih-oh/zoom)/2"
    if fill:
        pre = (
            f"scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},"
        )
    else:
        # contain inside 1920x1080 on black (even dims)
        pre = (
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
            f"scale=trunc(iw/2)*2:trunc(ih/2)*2,"
        )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(still),
        "-vf",
        f"{pre}zoompan=z='{zf}':x='{xf}':y='{yf}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
        "-frames:v", str(n),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-an",
        str(dest),
    ])


def clip_window(src: Path, dest: Path, src_in: float, src_out: float, caption: str = "") -> None:
    dur = max(0.25, src_out - src_in)
    vf = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,fps={FPS},format=yuv420p"
    if caption.strip():
        cap = WORK / f"_cap_{dest.stem}.png"
        caption_png(caption, cap)
        # overlay caption for full duration
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
    dur = float(r["vo_out"]) - float(r["vo_in"])
    cap = (r.get("caption") or "").strip()
    last = r.get("_last", False)

    if src == "CARD":
        png = WORK / f"card_{r['row']}.png"
        starfield_card(rid, png)
        still_to_mp4(png, dest, dur, 1.02, fill=True)
        return

    if src == "NASA":
        still = resolve_nasa(rid, pool)
        fill = rid in FILL_IDS
        # Grand Finale illustrations by title
        title = (pool[rid].get("title") or "").lower()
        if "illustration" in title or "artist concept" in title:
            fill = True
        zoom = parse_push(r.get("move") or "")
        if last:
            zoom = max(zoom, 1.07)
        still_to_mp4(still, dest, dur, zoom, fill=fill)
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
            # search
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
    """VO with silence inserted at CARD rows; music under all; fade on end hold."""
    vo_parts_dir = WORK / "audio_parts"
    vo_parts_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    vo_cursor = 0.0
    vo_dur = probe(VO)
    for r in rows:
        dur = float(r["vo_out"]) - float(r["vo_in"])
        src = (r.get("source") or "").strip().upper()
        out = vo_parts_dir / f"a_{int(r['row']):03d}.wav"
        if src == "CARD" or r.get("_last"):
            # silence (music carries)
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", f"{dur:.3f}", str(out),
            ])
        else:
            # take next `dur` seconds from VO
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
                # pad short leftover VO to row length
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

    # leftover VO (if any) is unused — first cut may leave ~4–5 s; log it
    print(f"VO consumed {vo_cursor:.2f}s of {vo_dur:.2f}s", flush=True)

    vo_concat = WORK / "vo_timeline.wav"
    lst = WORK / "audio_concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vo_concat),
    ])

    # Music bed looped to total, quiet under VO, fade last 10s of end hold.
    # Beds are mp3 — re-encode on join (cannot -c copy into m4a).
    music_raw = WORK / "music_raw.m4a"
    mlist = WORK / "music_concat.txt"
    mlist.write_text("".join(f"file '{m.resolve()}'\n" for m in MUSIC if m.exists()))
    music_joined = WORK / "music_joined.mp3"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(mlist),
        "-c:a", "libmp3lame", "-q:a", "2", str(music_joined),
    ])
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-stream_loop", "-1", "-i", str(music_joined),
        "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "192k", str(music_raw),
    ])

    # Mix: VO primary, music ~-20 dB, fade music over last 10s, picture will fade separately
    mixed = WORK / "mix.m4a"
    fade_start = max(0.0, total - 10.0)
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(vo_concat), "-i", str(music_raw),
        "-filter_complex",
        f"[1:a]volume=0.12,afade=t=out:st={fade_start:.3f}:d=10[m];"
        f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0,alimiter=limit=0.95",
        "-c:a", "aac", "-b:a", "192k", str(mixed),
    ])
    return mixed


def contact_12(video: Path, dest: Path) -> None:
    dur = probe(video)
    # 12 frames evenly across the cut
    times = [dur * (i + 0.5) / 12 for i in range(12)]
    cells = []
    for i, t in enumerate(times):
        p = WORK / f"c12_{i:02d}.png"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-update", "1", str(p),
        ])
        cells.append(Image.open(p).convert("RGB").resize((480, 270), Image.Resampling.LANCZOS))
    cols, rows = 4, 3
    board = Image.new("RGB", (cols * 480, rows * 270 + 40), (12, 12, 14))
    dr = ImageDraw.Draw(board)
    dr.text((12, 10), "Saturn first cut v02 — 12-frame contact", font=ImageFont.truetype(FONT, 22), fill=(240, 240, 240))
    for i, im in enumerate(cells):
        board.paste(im, ((i % cols) * 480, 40 + (i // cols) * 270))
    board.save(dest)
    print("wrote", dest, board.size)


def per_row_sheet(row_mp4s: list[tuple[dict, Path]], dest: Path) -> None:
    """One mid-frame per row, labelled — for Claude review (iCloud, not git)."""
    thumbs = []
    for r, mp4 in row_mp4s:
        dur = max(0.1, probe(mp4))
        p = WORK / f"rowmid_{int(r['row']):03d}.png"
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
    rows = math.ceil(len(thumbs) / cols)
    board = Image.new("RGB", (cols * 320, rows * 204 + 36), (10, 10, 12))
    ImageDraw.Draw(board).text(
        (10, 8), "Saturn first cut v02 — per-row midframes (v03g)",
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

    if not VO.exists():
        sys.exit(f"missing locked VO: {VO}")
    if not GODDARD.exists():
        sys.exit(f"missing Goddard HD: {GODDARD}")
    if not SHOT.exists():
        sys.exit(f"missing shot list: {SHOT}")

    # Confirm Goddard is 1080p
    gw, gh = probe_wh(GODDARD)
    print(f"Goddard {GODDARD.name} {gw}x{gh}", flush=True)
    if gh < 1000:
        sys.exit("Goddard file is not HD — refuse Twitter 720p")

    pool = {e["nasa_id"]: e for e in json.loads(POOL_JSON.read_text())}
    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    rows[-1]["_last"] = True
    total = float(rows[-1]["vo_out"])
    print(f"rows={len(rows)} picture_end={total:.2f}s VO={probe(VO):.2f}s", flush=True)

    row_mp4s: list[tuple[dict, Path]] = []
    for r in rows:
        dest = WORK / f"row_{int(r['row']):03d}.mp4"
        if dest.exists() and dest.stat().st_size > 1000:
            # allow resume
            print(f"reuse row {r['row']}", flush=True)
        else:
            print(f"build row {r['row']} {r['source']} {r['id'][:40]}", flush=True)
            build_row_clip(r, pool, dest)
        row_mp4s.append((r, dest))

    picture = WORK / "picture_all.mp4"
    if picture.exists() and picture.stat().st_size > 1_000_000:
        print(f"reuse picture_all ({picture.stat().st_size} bytes)", flush=True)
    else:
        concat_videos([p for _, p in row_mp4s], picture)

    audio = build_audio(rows, total)

    # Mux + picture fade last 2s
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

    c12 = UAT_DIR / "saturn_first_cut_v02_contact12.png"
    contact_12(OUT_LOCAL, WORK / "contact12.png")
    chunk_write(WORK / "contact12.png", c12)
    shutil.copy2(WORK / "contact12.png", ART / "saturn_first_cut_v02_contact12.png")

    per_row = UAT_DIR / "saturn_first_cut_v02_per_row.png"
    per_row_sheet(row_mp4s, WORK / "per_row.png")
    chunk_write(WORK / "per_row.png", per_row)
    # Also keep a local review copy (not committed)
    shutil.copy2(WORK / "per_row.png", REVIEW / "saturn_first_cut_v02_per_row.png")

    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v02.mp4")
    # sha
    h = hashlib.sha256()
    with open(OUT_LOCAL, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)
    meta = {
        "shot_list": "shot_list_v03g.csv",
        "vo": str(VO.name),
        "duration": probe(OUT_LOCAL),
        "sha256": h.hexdigest(),
        "goddard": f"{gw}x{gh}",
        "row93": "NASA PIA12633 temp until Omni",
        "icloud": str(UAT_DIR),
        "note": "per-row sheet in iCloud only (Ben: no media in git)",
    }
    (UAT_DIR / "ARRIVAL.json").write_text(json.dumps(meta, indent=2))
    (WORK / "META.json").write_text(json.dumps(meta, indent=2))
    print("DONE", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
