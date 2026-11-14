#!/usr/bin/env python3
"""J2550 assembly & 5-gate verification for Short 2 (Muons v05) and Short 3 (ISS v14).
Zero API/credit spend (£0). Does NOT overwrite v04 or v13; does NOT upload or touch Studio.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

SCRATCH = Path("/Volumes/MiniWork/scratch/J2550")
WT_REV = Path("/Volumes/MiniWork/scratch/J2550-wt/jobs/reviews/J2550")
NAS_UAT_ROOT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT")
CLOUD_UAT_ROOT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
GERST = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/"
    "02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Gerst_Earth_timelapses_2017.webm"
)

W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
CYAN = (120, 220, 255, 210)


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            text=True,
        )
    )


def measure_ebur128(path: Path) -> tuple[float, float]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    lufs_val = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
    tp_val = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1])
    return lufs_val, tp_val


def mix_levelled(picture: Path, vo: Path, bed_stem: Path, sfx_stem: Path, total: float, out: Path) -> tuple[float, float]:
    raw_mix = out.with_name(f"_{out.stem}_rawmix.mp4")
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", picture, "-i", vo, "-i", bed_stem, "-i", sfx_stem,
            "-filter_complex",
            "[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
            "loudnorm=I=-14:TP=-2.0:LRA=11,aresample=48000[a]",
            "-map", "0:v", "-map", "[a]",
            *shorts_encode_args(fps=FPS),
            "-t", f"{total:.3f}",
            raw_mix,
        ]
    )
    lufs1, _ = measure_ebur128(raw_mix)
    delta = round(-14.0 - lufs1, 2)
    run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", raw_mix, "-c:v", "copy",
            "-af", f"volume={delta}dB,alimiter=limit=-2.0dB:level=false,aresample=48000",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out,
        ]
    )
    lufs2, tp2 = measure_ebur128(out)
    if not (-14.4 <= lufs2 <= -13.6):
        delta2 = round(delta + (-14.0 - lufs2), 2)
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", raw_mix, "-c:v", "copy",
                "-af", f"volume={delta2}dB,alimiter=limit=-2.0dB:level=false,aresample=48000",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out,
            ]
        )
        lufs2, tp2 = measure_ebur128(out)
    raw_mix.unlink(missing_ok=True)
    return lufs2, tp2


def make_2fps_sheet(video: Path, dest: Path) -> None:
    total = dur(video)
    times = [round(i * 0.5, 2) for i in range(int(total * 2) + 1) if round(i * 0.5, 2) <= total - 0.04]
    cols = 6
    rows = (len(times) + cols - 1) // cols
    tw, th = 216, 384
    canvas = Image.new("RGB", (cols * tw, rows * (th + 28)), (0, 0, 0))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 20)
    tmp = dest.parent / f"_tmp_tiles_{dest.stem}"
    tmp.mkdir(parents=True, exist_ok=True)
    for idx, t in enumerate(times):
        tile = tmp / f"t_{idx:03d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(tile)])
        cx, cy = (idx % cols) * tw, (idx // cols) * (th + 28)
        canvas.paste(Image.open(tile), (cx, cy))
        d.text((cx + 6, cy + th + 3), f"{t:.1f}s", font=font, fill=(255, 255, 255))
    shutil.rmtree(tmp)
    canvas.save(dest, quality=90)


def font_for(line_h: float, ratio: float = 0.86) -> ImageFont.FreeTypeFont:
    size = 10
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f = ImageFont.truetype(FONT, size + 1)
        b = probe.textbbox((0, 0), "Hg", font=f)
        if b[3] - b[1] > line_h * ratio:
            return ImageFont.truetype(FONT, size)
        size += 1


def centred(draw, y, text, font, fill, stroke=6):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    stroke_fill = (0, 0, 0, fill[3] if len(fill) == 4 else 255)
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def text_png(dest: Path, rows: list[str], y0: int, cap_h: float, fills: list | None = None, stroke=7) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(cap_h)
    fills = fills or [WHITE] * len(rows)
    while max(d.textlength(t, font=f) for t in rows) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = y0
    for t, c in zip(rows, fills):
        centred(d, y, t, f, c, stroke=stroke)
        y += lh
    im.save(dest)


def stage_uat_copies(files: list[Path], folder_name: str) -> dict:
    staged = {}
    for label, root in (("nas", NAS_UAT_ROOT), ("clouddocs", CLOUD_UAT_ROOT)):
        target = root / folder_name
        target.mkdir(parents=True, exist_ok=True)
        sums = {}
        for src in files:
            dst = target / src.name
            shutil.copy2(src, dst)
            s_hash, d_hash = sha256(src), sha256(dst)
            if s_hash != d_hash:
                raise SystemExit(f"SHA256 mismatch staging {src} -> {dst}")
            sums[src.name] = d_hash
        (target / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2) + "\n")
        staged[label] = {"dir": str(target), "sha256": sums}
    return staged


def build_muons_v05() -> dict:
    print("=== Building Short 2: Muons fri06_muons_ground_v05.mp4 ===", flush=True)
    uploads = json.loads((REPO / "00_Brand/Channel-Setup/social/UPLOADS.json").read_text())
    reg = uploads.get("videos", uploads)["rvug71d7Dqk"]
    here = REPO / "02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground"
    film = here.parents[1]
    out_dir = here / "06_Final-Exports"
    v04 = out_dir / "fri06_muons_ground_v04.mp4"
    v04_sha = sha256(v04)
    if v04_sha != reg["sha256"]:
        raise SystemExit(f"Muons v04 sha256 mismatch vs UPLOADS.json: {v04_sha} != {reg['sha256']}")

    uat_v04 = here / "_work_v02"
    vo_stem = uat_v04 / "stem_vo.wav"
    bed_stem = uat_v04 / "stem_bed.wav"
    sfx_stem = uat_v04 / "stem_sfx.wav"
    bed_mp3 = film / "05_Music/light-speed_score_bed_v01_full.mp3"
    for p in (GERST, vo_stem, bed_stem, sfx_stem, bed_mp3):
        if not p.exists():
            raise SystemExit(f"Missing Muons input: {p}")

    work = SCRATCH / "muons_v05"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    stem = "fri06_muons_ground_v05"
    final = out_dir / f"{stem}.mp4"
    graphic_name = "code_graphic_024_fri06_muons_v05_scale.mp4"
    graphic_out = out_dir / graphic_name
    total = 22.20
    crop = "crop=612:1088:1614:1072"
    up = round(1920 / 1088, 3)  # 1.765x (< 2.0x warn, < 2.35x fail)

    # Build full-frame 9:16 code graphic (3.80 s) over Gerst ss=12.0s aurora/atmosphere with falling muon streaks
    g_base = work / "graphic_base.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "12.000", "-t", "3.800", "-i", str(GERST),
        "-vf", f"{crop},eq=gamma=1.18:brightness=0.03,scale={W}:{H}:flags=lanczos,noise=alls=4:allf=t,fps={FPS},format=yuv420p",
        "-an", "-r", str(FPS), "-t", "3.800", "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", str(g_base),
    ])
    streaks = work / "streaks.png"
    im_s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(im_s)
    for i, x in enumerate(range(80, W, 90)):
        y0 = 140 + (i % 5) * 95
        ds.line([(x, y0), (x - 45, y0 + 680)], fill=CYAN, width=5)
        ds.ellipse([x - 52, y0 + 672, x - 38, y0 + 688], fill=(255, 244, 180, 235))
    im_s.save(streaks)
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(g_base), "-loop", "1", "-i", str(streaks),
        "-filter_complex",
        "[1:v]format=rgba,fade=t=in:d=0.35:alpha=1[s];"
        "[0:v][s]overlay=0:y='-160+85*t':format=auto,format=yuv420p[v]",
        "-map", "[v]", "-an", "-t", "3.800", "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "veryfast", str(graphic_out),
    ])

    # 6 segments summing to 22.20 s; Gerst appears in 5 stretches (>= 18s apart, <= 5 max_stretches)
    segs = [
        (0.00, 3.00, "gerst", 39.0, "eq=gamma=1.06:saturation=1.12", up, "ESA Alexander Gerst ISS Earth orbital timelapse"),
        (3.00, 3.80, "graphic", 0.0, "", 1.0, "Muon streaks over a real ISS Earth view"),
        (6.80, 3.80, "gerst", 96.0, "eq=gamma=1.12:saturation=1.12", up, "ESA Alexander Gerst ISS Earth orbital timelapse"),
        (10.60, 3.80, "gerst", 148.0, "eq=gamma=1.18:brightness=0.03:saturation=1.10", up, "ESA Alexander Gerst ISS Earth orbital timelapse"),
        (14.40, 3.80, "gerst", 114.0, "eq=gamma=1.28:brightness=0.05:saturation=1.12", up, "ESA Alexander Gerst ISS Earth orbital timelapse"),
        (18.20, 4.00, "gerst", 290.0, "eq=gamma=1.08:saturation=1.12", up, "ESA Alexander Gerst ISS Earth orbital timelapse"),
    ]
    seg_files = []
    for i, (t0, length, key, ss, eq_vf, _u, _title) in enumerate(segs):
        dest = work / f"seg_{i:02d}.mp4"
        if key == "graphic":
            run([
                "ffmpeg", "-y", "-v", "error", "-i", str(graphic_out),
                "-an", "-r", str(FPS), "-t", f"{length:.3f}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "veryfast", str(dest),
            ])
        else:
            vf = f"{crop},{eq_vf},scale={W}:{H}:flags=lanczos,noise=alls=4:allf=t,fps={FPS},format=yuv420p"
            run([
                "ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(GERST),
                "-vf", vf, "-an", "-r", str(FPS), "-t", f"{length:.3f}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "veryfast", str(dest),
            ])
        seg_files.append(dest)

    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
    plates_mp4 = work / "plates.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "veryfast", "-r", str(FPS),
        str(plates_mp4),
    ])

    # Load words & render exact v04 text overlays (hook, title, clean 3-line endcard without video ID, 22 captions)
    src_w = json.loads((here / "words.json").read_text())
    w_raw = src_w["words"] if isinstance(src_w, dict) else src_w
    words = [{"w": w["text"], "s": float(w["start"]), "e": float(w["end"])} for w in w_raw]
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["w"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    caps = []
    for i, c in enumerate(chunks):
        start = c[0]["s"]
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else min(c[-1]["e"] + 0.35, total)
        end = min(nxt, c[-1]["e"] + 0.40, total)
        if end <= start:
            end = start + 0.2
        txt = re.sub(r"\bmeters\b", "metres", " ".join(x["w"] for x in c).rstrip(",."), flags=re.I)
        caps.append({"text": txt, "s": round(start, 2), "e": round(end, 2)})

    text_png(work / "hook.png", ["THEY", "LIVE"], 220, H * 0.090, [WHITE, YELLOW], stroke=8)
    text_png(work / "title.png", ["Muons Shouldn't", "Reach the Ground.", "They Do."], 820, H * 0.048, stroke=6)
    text_png(work / "endcard.png", ["What Happens If", "You Travel Near", "Light Speed?"], 980, H * 0.046, [WHITE, WHITE, YELLOW], stroke=6)
    for i, c in enumerate(caps):
        text_png(work / f"cap_{i:02d}.png", [c["text"].upper()], 1460, H * 0.042, stroke=5)

    loop = ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}"]
    inputs = ["-i", str(plates_mp4)]
    for name in ("hook.png", "title.png", "endcard.png"):
        inputs += [*loop, "-i", str(work / name)]
    for i in range(len(caps)):
        inputs += [*loop, "-i", str(work / f"cap_{i:02d}.png")]
    fc = [
        "[1:v]format=rgba,fade=t=out:st=1.90:d=0.25:alpha=1[hk]",
        "[0:v][hk]overlay=0:0:enable='lt(t,2.15)'[v1]",
        "[2:v]format=rgba,fade=t=in:st=9.00:d=0.25:alpha=1,fade=t=out:st=13.75:d=0.25:alpha=1[tt]",
        "[v1][tt]overlay=0:0:enable='between(t,9.0,14.0)'[v2]",
        "[3:v]format=rgba,fade=t=in:st=16.90:d=0.30:alpha=1,fade=t=out:st=20.80:d=0.25:alpha=1[en]",
        "[v2][en]overlay=0:0:enable='between(t,16.9,21.05)'[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{4 + i}:v]overlay=0:0:enable='between(t,{c['s']:.2f},{c['e']:.2f})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    pic_mp4 = work / "picture.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
        "-map", "[v]", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "veryfast",
        "-t", f"{total:.3f}", str(pic_mp4),
    ])

    lufs_val, tp_val = mix_levelled(pic_mp4, vo_stem, bed_stem, sfx_stem, total, final)

    # Cover & sheets
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.15", "-i", str(plates_mp4), "-frames:v", "1", str(work / "plate0.png")])
    im_cov = Image.open(work / "plate0.png").convert("RGB")
    im_cov = ImageEnhance.Color(im_cov).enhance(1.25)
    im_cov = ImageEnhance.Contrast(im_cov).enhance(1.12)
    dc = ImageDraw.Draw(im_cov)
    c_rows = [("SLOW", YELLOW), ("CLOCKS", WHITE)]
    sz = 40
    while True:
        fc_font = ImageFont.truetype(FONT, sz + 4)
        if max(dc.textlength(r, font=fc_font) for r, _ in c_rows) > W * 0.86:
            break
        sz += 4
    fc_font = ImageFont.truetype(FONT, sz)
    lh_c = dc.textbbox((0, 0), "Hg", font=fc_font)[3] + 24
    yc = (H - lh_c * len(c_rows)) // 2
    for r, col in c_rows:
        centred(dc, yc, r, fc_font, col, stroke=10)
        yc += lh_c
    cover_jpg = out_dir / f"{stem}_cover.jpg"
    im_cov.save(cover_jpg, quality=92)
    cover_prev = out_dir / f"{stem}_cover_preview.jpg"
    run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"), "short", str(cover_jpg), "--out", str(cover_prev)])
    sheet_2fps = out_dir / f"{stem}_2fps.jpg"
    make_2fps_sheet(final, sheet_2fps)

    # Cuts & pool
    cuts, pool, seen = [], [], set()
    for i, (t0, length, key, ss, _eq, u, title) in enumerate(segs):
        src_name = graphic_name if key == "graphic" else GERST.name
        cuts.append({
            "row": f"s{i + 1:02d}_{key}",
            "timeline_in": t0,
            "timeline_out": round(t0 + length, 2),
            "source": src_name,
            "upscale": u,
            "framing": {"offset": ss, "crop": "612:1088:1614:1072" if key != "graphic" else "full_9x16"},
            "video": True,
        })
        if src_name not in seen:
            pool.append({"file_id": src_name, "title": title})
            seen.add(src_name)

    rev_dir = WT_REV / "muons_v05"
    rev_dir.mkdir(parents=True, exist_ok=True)
    cuts_p = rev_dir / "cuts_v05.json"
    pool_p = rev_dir / "pool_v05.json"
    cuts_p.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_p.write_text(json.dumps(pool, indent=2) + "\n")
    shutil.copy2(cuts_p, out_dir / "cuts_v05.json")
    shutil.copy2(pool_p, out_dir / "pool_v05.json")

    meta = {
        "job": "J2550",
        "version": "v05",
        "youtube_id": "rvug71d7Dqk",
        "air_date": "2026-11-21",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "replaces_v04_sha256": v04_sha,
        "duration_s": round(dur(final), 3),
        "words": len(words),
        "lufs": lufs_val,
        "true_peak_dbfs": tp_val,
        "end_card": {"start_s": 16.90, "end_s": 21.05, "rows": ["What Happens If", "You Travel Near", "Light Speed?"]},
        "spend": "none",
    }
    meta_p = out_dir / f"{stem}_meta.json"
    meta_p.write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(meta_p, rev_dir / f"{stem}_meta.json")

    # Run all 5 Shorts gates (NOT report-only) + full decode
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--id", "rvug71d7Dqk", "--air-date", "2026-11-21",
         "--vo", str(vo_stem), "--script", str(here / "fri06_muons_ground_vo_v01.txt")],
        capture_output=True, text=True,
    )
    (rev_dir / "gate_v05.txt").write_text(gate.stdout + gate.stderr)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
         "--minutes", f"{total / 60.0:.4f}"],
        capture_output=True, text=True,
    )
    (rev_dir / "sfx_v05.txt").write_text(sfx_chk.stdout + sfx_chk.stderr)

    others = [
        str(p) for p in (REPO / "02_Video-Projects").glob("*/05_Music/*")
        if p.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac"} and p.name != bed_mp3.name
    ]
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(film),
         "--bed", str(bed_mp3), "--video", str(final),
         "--out", str(rev_dir / "music_v05.json"), "--others", *others],
        capture_output=True, text=True,
    )
    (rev_dir / "music_v05.txt").write_text(music.stdout + music.stderr)

    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(cuts_p), "--out", str(rev_dir / "polish_v05.json")],
        capture_output=True, text=True,
    )
    (rev_dir / "polish_v05.txt").write_text(polish.stdout + polish.stderr)

    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_p), "--pool", str(pool_p), "--out-dir", str(work / "pqa")],
        capture_output=True, text=True,
    )
    (rev_dir / "picture_qa_v05.txt").write_text(pqa.stdout + pqa.stderr)

    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, text=True)

    # Assert v04 untouched
    if sha256(v04) != v04_sha:
        raise SystemExit("ERROR: Muons v04 was modified!")

    staged = stage_uat_copies([final, cover_jpg, sheet_2fps, meta_p], "J2550_muons_v05")
    (rev_dir / "safety_copies_v05.json").write_text(json.dumps(staged, indent=2) + "\n")

    exits = {
        "gate": gate.returncode,
        "sfx": sfx_chk.returncode,
        "music": music.returncode,
        "polish": polish.returncode,
        "picture_qa": pqa.returncode,
        "decode": decode.returncode,
    }
    print("MUONS v05 EXITS:", exits)
    print("GATE:\n", (gate.stdout + gate.stderr).strip())
    print("SFX:", (sfx_chk.stdout + sfx_chk.stderr).strip())
    print("POLISH:\n", (polish.stdout + polish.stderr).strip())
    print("MUSIC:\n", (music.stdout + music.stderr).strip()[-300:])
    print("PQA:\n", (pqa.stdout + pqa.stderr).strip())
    if any(exits.values()):
        raise SystemExit(f"Muons v05 failed gate(s): {exits}")
    return {"meta": meta, "exits": exits, "sheet_2fps": str(sheet_2fps), "final": str(final), "nas_mp4": str(NAS_UAT_ROOT / "J2550_muons_v05" / final.name)}


def caption_image_ar2(text: str) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sz = 58
    while sz > 28:
        font = ImageFont.truetype(FONT, sz)
        box = d.textbbox((0, 0), text, font=font, stroke_width=6)
        if box[2] - box[0] <= int(W * 0.72):
            break
        sz -= 2
    font = ImageFont.truetype(FONT, max(28, sz))
    box = d.textbbox((0, 0), text, font=font, stroke_width=6)
    x = (W - (box[2] - box[0])) / 2 - box[0]
    d.text((x, int(H * 0.86)), text, font=font, fill=(245, 248, 255, 255), stroke_width=6, stroke_fill=(8, 16, 28, 255))
    return im


def build_iss_v14() -> dict:
    print("=== Building Short 3: ISS owb_ar2_iss_2030_deorbit_v14.mp4 ===", flush=True)
    uploads = json.loads((REPO / "00_Brand/Channel-Setup/social/UPLOADS.json").read_text())
    reg = uploads.get("videos", uploads)["xdurJQcoiGM"]
    audit = REPO / "00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10"
    out_dir = audit / "06_Final-Exports"
    v13 = out_dir / "owb_ar2_iss_2030_deorbit_v13.mp4"
    v13_sha = sha256(v13)
    if v13_sha != reg["sha256"]:
        raise SystemExit(f"ISS v13 sha256 mismatch vs UPLOADS.json: {v13_sha} != {reg['sha256']}")

    j2229_ar2 = Path("/Users/benjaminoats/_desk/renders/J2229/ar2")
    vo_stem = j2229_ar2 / "stem_vo.wav"
    bed_stem = j2229_ar2 / "stem_bed.wav"
    sfx_stem = j2229_ar2 / "stem_sfx.wav"
    bed_mp3 = audit / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
    script_txt = Path("/Users/benjaminoats/_desk/renders/J2229/ar2_spoken_v13.txt")
    words_json = audit / "02_Voiceover/apophis_ar2_vo_v01_words.json"
    for p in (GERST, v13, vo_stem, bed_stem, sfx_stem, bed_mp3, script_txt, words_json):
        if not p.exists():
            raise SystemExit(f"Missing ISS input: {p}")

    work = SCRATCH / "iss_v14"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    stem = "owb_ar2_iss_2030_deorbit_v14"
    final = out_dir / f"{stem}.mp4"
    total = 552 / FPS  # 18.400 s (frames 0..552)

    # 1. Extract frames 0..443 (0.000-14.767 s) unchanged from v13
    head_mp4 = work / "head_0_443.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(v13),
        "-vf", "trim=start_frame=0:end_frame=443,setpts=PTS-STARTPTS",
        "-an", "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "veryfast",
        str(head_mp4),
    ])

    # 2. Build full-frame 9:16 tail frames 443..552 (109 frames = 3.633 s) from 4K Gerst ss=290.0s (ISS Canadarm2 & docked craft above sunlit Earth)
    tail_raw = work / "tail_raw.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "290.000", "-i", str(GERST),
        "-frames:v", "109",
        "-vf", f"crop=612:1088:1614:1072,eq=gamma=1.06:saturation=1.10,scale={W}:{H}:flags=lanczos,noise=alls=4:allf=t,fps={FPS}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "veryfast",
        str(tail_raw),
    ])

    # Composite exact J2229 captions onto frames 443..552 (t = 14.767..18.400 s)
    raw_words = json.loads(words_json.read_text())
    words = []
    for w in raw_words:
        txt = (w.get("text") or w.get("word") or "").strip()
        if not txt or w.get("type") not in (None, "word"):
            continue
        if txt.lower().startswith("because"):
            continue
        words.append({"word": txt, "start": float(w["start"]), "end": float(w["end"])})
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1:] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    cap_groups = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.45)
        txt = " ".join(w["word"] for w in g).upper().replace(" ,", ",")
        if i + 1 == len(groups) and not txt.endswith((".", "?", "!")):
            txt += "."
        cap_groups.append((start, stop, caption_image_ar2(txt)))

    cap_sky = caption_image_ar2("THE SKY.")
    frames_dir = work / "tail_frames"
    frames_dir.mkdir()
    run(["ffmpeg", "-y", "-v", "error", "-i", str(tail_raw), str(frames_dir / "f_%05d.png")])
    for i, fp in enumerate(sorted(frames_dir.glob("f_*.png"))):
        t = (443 + i) / FPS
        im = Image.open(fp).convert("RGBA")
        if t >= 498 / FPS:  # 16.600 s: J2229 terminal sentence-end caption rule
            if t < 17.59:
                im.alpha_composite(cap_sky)
        else:
            for a, b, c_im in cap_groups:
                if a <= t < b:
                    im.alpha_composite(c_im)
                    break
        im.convert("RGB").save(fp, compress_level=1)

    tail_mp4 = work / "tail_443_552.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames_dir / "f_%05d.png"),
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "veryfast", str(tail_mp4),
    ])
    shutil.rmtree(frames_dir)

    lst = work / "concat.txt"
    lst.write_text(f"file '{head_mp4}'\nfile '{tail_mp4}'\n")
    pic_mp4 = work / "picture.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), "-crf", "14", "-preset", "veryfast",
        str(pic_mp4),
    ])

    lufs_val, tp_val = mix_levelled(pic_mp4, vo_stem, bed_stem, sfx_stem, total, final)

    cover_jpg = out_dir / f"{stem}_cover.jpg"
    shutil.copy2(out_dir / "owb_ar2_iss_2030_deorbit_v13_cover.jpg", cover_jpg)
    sheet_2fps = out_dir / f"{stem}_2fps.jpg"
    make_2fps_sheet(final, sheet_2fps)

    # Cuts & pool (updating only cut 5 from Crew2 720p blur-pad to full-bleed 4K Gerst ss=290.0s)
    cuts = json.loads((j2229_ar2 / "evidence/cuts.json").read_text())
    pool = json.loads((j2229_ar2 / "evidence/pool.json").read_text())
    cuts[-1] = {
        "row": "ar2_05_Gerst_ISS_arm_s5",
        "source": str(GERST),
        "timeline_in": 14.767,
        "timeline_out": 18.4,
        "upscale": round(1920 / 1088, 4),
        "framing": {
            "offset": 290.0,
            "crop": "612:1088:1614:1072",
            "native_speed": True,
            "J2550": "Replaced padded 720p Crew-2 band-over-blur shot with full-frame 9:16 4K ISS Canadarm2 & docked craft orbital pass (upscale 1.765x, 0% padded).",
        },
        "overlays": [],
    }

    rev_dir = WT_REV / "iss_v14"
    rev_dir.mkdir(parents=True, exist_ok=True)
    cuts_p = rev_dir / "cuts_v14.json"
    pool_p = rev_dir / "pool_v14.json"
    cuts_p.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_p.write_text(json.dumps(pool, indent=2) + "\n")

    meta = {
        "job": "J2550",
        "version": "v14",
        "youtube_id": "xdurJQcoiGM",
        "air_date": "2026-11-25",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "replaces_v13_sha256": v13_sha,
        "duration_s": round(dur(final), 3),
        "words": len(words),
        "lufs": lufs_val,
        "true_peak_dbfs": tp_val,
        "spend": "none",
    }
    meta_p = out_dir / f"{stem}_meta.json"
    meta_p.write_text(json.dumps(meta, indent=2) + "\n")
    shutil.copy2(meta_p, rev_dir / f"{stem}_meta.json")

    # Run all 5 Shorts gates (NOT report-only) + full decode
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--id", "xdurJQcoiGM", "--air-date", "2026-11-25",
         "--vo", str(vo_stem), "--script", str(script_txt)],
        capture_output=True, text=True,
    )
    (rev_dir / "gate_v14.txt").write_text(gate.stdout + gate.stderr)

    sfx_chk = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
         "--minutes", f"{total / 60.0:.4f}"],
        capture_output=True, text=True,
    )
    (rev_dir / "sfx_v14.txt").write_text(sfx_chk.stdout + sfx_chk.stderr)

    others = [
        str(p) for p in (REPO / "02_Video-Projects").glob("*/05_Music/*")
        if p.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac"} and p.name != bed_mp3.name
    ]
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(audit),
         "--bed", str(bed_mp3), "--video", str(final),
         "--out", str(rev_dir / "music_v14.json"), "--others", *others],
        capture_output=True, text=True,
    )
    (rev_dir / "music_v14.txt").write_text(music.stdout + music.stderr)

    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(cuts_p), "--out", str(rev_dir / "polish_v14.json")],
        capture_output=True, text=True,
    )
    (rev_dir / "polish_v14.txt").write_text(polish.stdout + polish.stderr)

    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_p), "--pool", str(pool_p), "--out-dir", str(work / "pqa")],
        capture_output=True, text=True,
    )
    (rev_dir / "picture_qa_v14.txt").write_text(pqa.stdout + pqa.stderr)

    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, text=True)

    if sha256(v13) != v13_sha:
        raise SystemExit("ERROR: ISS v13 was modified!")

    staged = stage_uat_copies([final, cover_jpg, sheet_2fps, meta_p], "J2550_iss_v14")
    (rev_dir / "safety_copies_v14.json").write_text(json.dumps(staged, indent=2) + "\n")

    exits = {
        "gate": gate.returncode,
        "sfx": sfx_chk.returncode,
        "music": music.returncode,
        "polish": polish.returncode,
        "picture_qa": pqa.returncode,
        "decode": decode.returncode,
    }
    print("ISS v14 EXITS:", exits)
    print("GATE:\n", (gate.stdout + gate.stderr).strip())
    print("SFX:", (sfx_chk.stdout + sfx_chk.stderr).strip())
    print("POLISH:\n", (polish.stdout + polish.stderr).strip())
    print("MUSIC:\n", (music.stdout + music.stderr).strip()[-300:])
    print("PQA:\n", (pqa.stdout + pqa.stderr).strip())
    if any(exits.values()):
        raise SystemExit(f"ISS v14 failed gate(s): {exits}")
    return {"meta": meta, "exits": exits, "sheet_2fps": str(sheet_2fps), "final": str(final), "nas_mp4": str(NAS_UAT_ROOT / "J2550_iss_v14" / final.name)}


def main() -> None:
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    out = {}
    if which in ("muons", "both"):
        out["muons_v05"] = build_muons_v05()
    if which in ("iss", "both"):
        out["iss_v14"] = build_iss_v14()
    (SCRATCH / "shorts_2_and_3_summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print("ALL DONE:", SCRATCH / "shorts_2_and_3_summary.json")


if __name__ == "__main__":
    main()
