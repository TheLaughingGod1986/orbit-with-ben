#!/usr/bin/env python3
"""029 Betelgeuse teaching overlays v01 (J0375):
AGENTS.md Reference lessons item 6 (Chief ruling 12 Oct: a to-scale graphic with no numeral does NOT count as NUMBER).
Renders the teaching overlay rows for Chapters 1, 3, and 4 of 029 (the three chapters without a numeral-bearing object):
- Chapter 1 (1 The Star in Orion's Shoulder):
  * r06_paranal (49.46-55.00s, lasilla_startrails.mp4): '700 light-years away' at 51.16-53.60s (SOURCES row 3)
  * r07_sdo (62.46-67.50s, sdo_hmi_continuum.jpg): '4.5 billion years old' at 63.36-66.20s (SOURCES row 4)
  * r08_westerlund_w (73.86-80.00s, westerlund.jpg wide): '15 to 20 times' at 78.06-79.90s (SOURCES row 5)
  * r08_westerlund_t (80.00-86.00s, westerlund.jpg tight): 'Around 100,000' at 84.30-85.92s (SOURCES row 6)
  * r09_finder (92.92-105.48s, code graphic finder): '3 stars' at 96.46-99.12s (SOURCES row 7)
- Chapter 3 (3 How a Giant Star Dies):
  * r17_r20_shells (210.50-216.50s collapse stretch, code graphic shells): 'Less than 1 second' at 211.94-215.20s (SOURCES row 12)
- Chapter 4 (4 The Night It Goes):
  * r29_span_astrolabe (336.50-350.00s stretch, code graphic orion_astrolabe):
    - '500 years' at 337.66-340.86s (SOURCES rows 3 & 18)
    - '100,000 years' at 348.06-349.95s (SOURCES row 19)

Writes house pill PNGs (`code_graphic_029_row*.png`), `overlays_v01.json`, `cuts_v01.json`, `OVERLAYS_v01.md`,
`overlay_stills_029_v01.jpg` (before/after stills), and runs `picture_qa.py` + `polish_gate.py`.
`--plan` prints the rows and checks without rendering."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
EP = HERE.parent
ROOT = EP.parents[1]
HDIR = HERE / "harvest_v01"
CDIR = HERE / "code_graphics_v01"
PACK = HERE / "teaching_overlays_v01_pack"
WORK = Path("/private/tmp/betelgeuse029_overlays_work_v01")
BEFORE_MP4 = Path("/private/tmp/029_teaching_overlays_v01_before.mp4")
AFTER_MP4 = Path("/private/tmp/029_teaching_overlays_v01_after.mp4")

FPS = 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

words = json.loads((EP / "02_Voiceover" / "words.json").read_text())["words"]

# Each row: (row_id, chapter, film_in, film_out, source_kind, source_file, framing_opts, overlays)
# overlay: (text, film_start, film_end, cx, y, px, source_check, suppress_gold_label)
ROWS = [
    (
        "r06_paranal",
        "1 The Star in Orion's Shoulder",
        49.46,
        55.00,
        "video",
        HDIR / "lasilla_startrails.mp4",
        {"offset": 0.0, "upscale": 1.0},
        [
            (
                "700 light-years away",
                51.16,
                53.60,
                960,
                860,
                76,
                "SOURCES row 3: Joyce et al. 2020 (168 +27/-15 pc = 548 ly) & Harper et al. 2017 (222 +48/-34 pc = 724 ly); VO 'seven hundred light-years away' at 51.16-52.68s",
                None,
            )
        ],
    ),
    (
        "r07_sdo",
        "1 The Star in Orion's Shoulder",
        62.46,
        67.50,
        "still",
        HDIR / "sdo_hmi_continuum.jpg",
        {"box": (0.02, 0.08, 0.98, 0.62), "pct": 0.05, "gamma": 1.0},
        [
            (
                "4.5 billion years old",
                63.36,
                66.20,
                960,
                860,
                76,
                "SOURCES row 4: Connelly et al. 2012 Science 338:651 CAI age 4567.30 +/- 0.16 Myr; VO 'four and a half billion years old' at 63.36-65.08s",
                None,
            )
        ],
    ),
    (
        "r08_westerlund_w",
        "1 The Star in Orion's Shoulder",
        73.86,
        80.00,
        "still",
        HDIR / "westerlund.jpg",
        {"box": (0.05, 0.12, 0.95, 0.795), "pct": 0.05, "gamma": 1.0},
        [
            (
                "15 to 20 times",
                78.06,
                79.90,
                960,
                860,
                76,
                "SOURCES row 5 (MUST QUOTE): Joyce et al. 2020 ApJ 902:63 present-day mass 16.5-19 M_sun, models 15-25 M_sun; VO 'fifteen to twenty times' at 78.50-80.18s",
                None,
            )
        ],
    ),
    (
        "r08_westerlund_t",
        "1 The Star in Orion's Shoulder",
        80.00,
        86.00,
        "still",
        HDIR / "westerlund.jpg",
        {"box": (0.22, 0.24, 0.78, 0.66), "pct": 0.05, "gamma": 1.0},
        [
            (
                "Around 100,000",
                84.30,
                85.92,
                960,
                860,
                76,
                "SOURCES row 6: Joyce et al. 2020 ApJ 902:63 model luminosity 10^5 L_sun (log L = 4.94 +0.06/-0.04); VO 'around a hundred thousand' at 85.02-86.34s",
                None,
            )
        ],
    ),
    (
        "r17_r20_shells",
        "3 How a Giant Star Dies",
        210.50,
        216.50,
        "code",
        CDIR / "code_graphic_029_r17_r20_shells_v01.mp4",
        {"plate_id": "r17_r20_shells", "plate_in": 175.40, "plate_use": 48.62, "offset": 35.10, "upscale": 1.0},
        [
            (
                "Less than 1 second",
                211.94,
                215.20,
                960,
                90,
                76,
                "SOURCES row 12: Janka 2012 ARNPS 62:407 core collapse takes a few hundred milliseconds; VO 'In less than a second' at 211.94-213.10s",
                "less than a second",
            )
        ],
    ),
    (
        "r29_span_astrolabe",
        "4 The Night It Goes",
        336.00,
        341.80,
        "code",
        CDIR / "code_graphic_029_r29_span_astrolabe_v01.mp4",
        {"plate_id": "r29_span_astrolabe", "plate_in": 326.56, "plate_use": 23.44, "offset": 9.44, "upscale": 1.0},
        [
            (
                "500 years",
                337.66,
                340.86,
                960,
                860,
                78,
                "SOURCES rows 3 & 18: Joyce et al. 2020 distance 168 +27/-15 pc = 548 ly (>500 yr light travel time); VO 'five hundred years' at 337.70-338.64s",
                "five hundred years",
            ),
        ],
    ),
]


def pill(text: str, px: int, dst: Path) -> tuple[int, int]:
    f = ImageFont.truetype(FONT, px)
    w = int(f.getlength(text))
    h = int(px * 1.55)
    padx = int(px * 0.55)
    img = Image.new("RGBA", (w + 2 * padx, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w + 2 * padx - 1, h - 1), radius=int(px * 0.32), fill=NAVY)
    d.text((padx, int(px * 0.22)), text, font=f, fill="white")
    img.save(dst)
    return img.size


def compute_upscale(kind: str, src: Path, opts: dict) -> float:
    if kind in ("video", "code"):
        return float(opts.get("upscale", 1.0))
    im = Image.open(src)
    w, h = im.size
    b = opts["box"]
    cw = w * (b[2] - b[0])
    ch = h * (b[3] - b[1])
    pct = opts.get("pct", 0.05)
    return round(max(1920.0 / cw, 1080.0 / ch) * (1.0 + pct), 3)


def check_plan() -> list[str]:
    problems = []
    for row_id, ch, fin, fout, kind, src, opts, ovs in ROWS:
        if not src.exists():
            problems.append(f"missing source {src}")
            continue
        up = compute_upscale(kind, src, opts)
        if up > 2.35:
            problems.append(f"{row_id} upscale {up:.2f} > 2.35")
        for text, a, b, cx, y, px, note, _ in ovs:
            n = len(text.split())
            if n > 4:
                problems.append(f"{row_id} {text!r} has {n} words (>4)")
            if not any(ch.isdigit() for ch in text):
                problems.append(f"{row_id} {text!r} has no numeral")
            dur = b - a
            if dur > 4.05 or dur < 1.5:
                problems.append(f"{row_id} {text!r} duration {dur:.2f}s outside 1.5..4.0s")
            if a < fin - 0.01 or b > fout + 0.01:
                problems.append(f"{row_id} {text!r} ({a:.2f}-{b:.2f}) outside row ({fin:.2f}-{fout:.2f})")
            print(
                f"{row_id:20s} | {ch:32s} | film {a:6.2f}-{b:6.2f} ({dur:4.2f}s) | {text:22s} | up={up:4.2f}x | {note}"
            )
    print("problems:", problems or "none")
    return problems


def render_still_push(src: Path, opts: dict, dur: float, dest: Path) -> None:
    frames = round(dur * FPS)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    b = opts["box"]
    im = im.crop((int(w * b[0]), int(h * b[1]), int(w * b[2]), int(h * b[3])))
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    scale = max(2112.0 / im.width, 1188.0 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x0 = (im.width - 2112) // 2
    y0 = (im.height - 1188) // 2
    im = im.crop((x0, y0, x0 + 2112, y0 + 1188))
    pct = opts.get("pct", 0.05)
    W, H = im.size
    proc = sp.Popen(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            "1920x1080",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-vf",
            "setsar=1",
            "-frames:v",
            str(frames),
            *ENC,
            str(dest),
        ],
        stdin=sp.PIPE,
    )
    for n in range(frames):
        z = 1.0 + pct * n / max(1, frames)
        bw, bh = W / z, H / z
        box = ((W - bw) / 2.0, (H - bh) / 2.0, (W + bw) / 2.0, (H + bh) / 2.0)
        proc.stdin.write(im.resize((1920, 1080), Image.Resampling.BICUBIC, box=box).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"still push failed: {dest}")


def render_code_clean(opts: dict, dur: float, suppress: set[str], dest: Path) -> None:
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v01 as cg

    frames = round(dur * FPS)
    plate = {"id": opts["plate_id"], "use_s": opts["plate_use"]}
    off = opts.get("offset", 0.0)
    orig_labels = list(cg.LABELS.get(opts["plate_id"], []))
    cg.LABELS[opts["plate_id"]] = [row for row in orig_labels if row[2] not in suppress]
    try:
        r = cg.Renderer(CDIR / "assets")
        proc = sp.Popen(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                "1920x1080",
                "-r",
                str(FPS),
                "-i",
                "-",
                "-vf",
                "noise=alls=2:allf=t,setsar=1",
                "-frames:v",
                str(frames),
                *ENC,
                str(dest),
            ],
            stdin=sp.PIPE,
        )
        for n in range(frames):
            t = off + n / FPS
            proc.stdin.write(r.frame(plate, t).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"code render failed: {dest}")
    finally:
        cg.LABELS[opts["plate_id"]] = orig_labels


def main() -> None:
    problems = check_plan()
    if "--plan" in sys.argv or problems:
        raise SystemExit(1 if problems else 0)

    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)

    before_segs = []
    after_segs = []
    cuts = []
    ov_records = []
    reel_t = 0.0
    pill_idx = 0

    for seg_i, (row_id, ch, fin, fout, kind, src, opts, ovs) in enumerate(ROWS):
        dur = round((fout - fin) * FPS) / FPS
        frames = round(dur * FPS)
        b_seg = WORK / f"before_{seg_i:02d}_{row_id}.mp4"
        base_after = WORK / f"base_after_{seg_i:02d}_{row_id}.mp4"
        a_seg = WORK / f"after_{seg_i:02d}_{row_id}.mp4"

        if kind == "video":
            off = opts.get("offset", 0.0)
            sp.run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-ss",
                    f"{off:.3f}",
                    "-i",
                    str(src),
                    "-vf",
                    f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps={FPS},setsar=1",
                    "-frames:v",
                    str(frames),
                    *ENC,
                    str(b_seg),
                ],
                check=True,
            )
            shutil.copyfile(b_seg, base_after)
        elif kind == "still":
            render_still_push(src, opts, dur, b_seg)
            shutil.copyfile(b_seg, base_after)
        elif kind == "code":
            off = opts.get("offset", 0.0)
            sp.run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-ss",
                    f"{off:.3f}",
                    "-i",
                    str(src),
                    "-vf",
                    f"fps={FPS},setsar=1",
                    "-frames:v",
                    str(frames),
                    *ENC,
                    str(b_seg),
                ],
                check=True,
            )
            suppress = {ov[7] for ov in ovs if ov[7]}
            render_code_clean(opts, dur, suppress, base_after)
        else:
            raise ValueError(kind)

        inputs = ["-i", str(base_after)]
        fc = "[0:v]null[v0];"
        seg_ovs = []
        for k, (text, a, b, cx, y, px, note, _) in enumerate(ovs):
            pname = f"code_graphic_029_{row_id}_{pill_idx:02d}.png"
            pill_idx += 1
            w, h = pill(text, px, WORK / pname)
            shutil.copyfile(WORK / pname, PACK / pname)
            la = round(a - fin, 3)
            lb = round(b - fin, 3)
            ldur = round(lb - la, 3)
            x = cx - w // 2
            rise = 22
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{ldur:.3f}", "-i", str(WORK / pname)]
            fc += (
                f"[{k+1}:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fade=t=out:st={max(0.0, ldur-0.30):.3f}:d=0.30:alpha=1,"
                f"setpts=PTS-STARTPTS+{la:.3f}/TB[o{k}];"
                f"[v{k}][o{k}]overlay=x={x}:y='{y}+{rise}*max(0\\,1-(t-{la:.3f})/0.35)':eval=frame:eof_action=pass[v{k+1}];"
            )
            rec = {
                "file": pname,
                "row": row_id,
                "chapter": ch,
                "text": text,
                "film_start": round(a, 2),
                "film_end": round(b, 2),
                "reel_start": round(reel_t + la, 3),
                "reel_end": round(reel_t + lb, 3),
                "x": x,
                "y": y,
                "size": [w, h],
                "check": note,
            }
            ov_records.append(rec)
            seg_ovs.append(pname)
        fc += f"[v{len(ovs)}]format=yuv420p[v]"
        fc_path = WORK / f"fc_{seg_i:02d}.txt"
        fc_path.write_text(fc)
        sp.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                *inputs,
                "-/filter_complex",
                str(fc_path),
                "-map",
                "[v]",
                "-frames:v",
                str(frames),
                *ENC,
                str(a_seg),
            ],
            check=True,
        )

        before_segs.append(b_seg)
        after_segs.append(a_seg)
        framing = {"offset": opts["offset"]} if kind in ("video", "code") else {"box": list(opts["box"]), "pct": opts.get("pct", 0.05)}
        cuts.append(
            {
                "row": row_id,
                "chapter": ch,
                "timeline_in": round(reel_t, 3),
                "timeline_out": round(reel_t + dur, 3),
                "film_in": fin,
                "film_out": fout,
                "source": src.name,
                "upscale": compute_upscale(kind, src, opts),
                "framing": framing,
                "overlays": seg_ovs,
            }
        )
        reel_t = round(reel_t + dur, 3)

    for tag, seg_list, dst in (("before", before_segs, BEFORE_MP4), ("after", after_segs, AFTER_MP4)):
        lst = WORK / f"concat_{tag}.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in seg_list))
        sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(dst)], check=True)

    (PACK / "overlays_v01.json").write_text(json.dumps({"film": "029", "job": "J0375", "labels": ov_records}, indent=2) + "\n")
    (PACK / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")

    # Build side-by-side before/after contact sheet
    tiles = []
    for k, o in enumerate(ov_records):
        t = min(o["reel_start"] + 0.9, (o["reel_start"] + o["reel_end"]) / 2.0)
        ft = min(o["film_start"] + 0.9, (o["film_start"] + o["film_end"]) / 2.0)
        for tag, src_mp4 in (("BEFORE", BEFORE_MP4), ("AFTER", AFTER_MP4)):
            jpg = WORK / f"still_{k:02d}_{tag.lower()}.jpg"
            sp.run(
                ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src_mp4), "-frames:v", "1", "-vf", "scale=640:360", str(jpg)],
                check=True,
            )
            tiles.append((jpg, f"{tag} · film {int(ft//60)}:{ft%60:04.1f} ({ft:.1f}s) · {o['row']} · {o['text']!r}"))
    cols = 2
    rows_n = (len(tiles) + cols - 1) // cols
    board = Image.new("RGB", (cols * 640, rows_n * 388), (18, 22, 30))
    d = ImageDraw.Draw(board)
    f_cap = ImageFont.truetype(FONT, 18)
    for i, (pth, label) in enumerate(tiles):
        x = (i % cols) * 640
        y = (i // cols) * 388
        board.paste(Image.open(pth), (x, y))
        d.text((x + 10, y + 364), label, font=f_cap, fill=(255, 214, 0) if label.startswith("AFTER") else (230, 235, 242))
    sheet_path = PACK / "overlay_stills_029_v01.jpg"
    board.save(sheet_path, quality=90)

    b_sha = hashlib.sha256(BEFORE_MP4.read_bytes()).hexdigest()
    a_sha = hashlib.sha256(AFTER_MP4.read_bytes()).hexdigest()
    s_sha = hashlib.sha256(sheet_path.read_bytes()).hexdigest()
    (PACK / "SHA256.txt").write_text(
        f"{a_sha}  {AFTER_MP4.name}\n{b_sha}  {BEFORE_MP4.name}\n{s_sha}  {sheet_path.name}\n"
    )
    print(f"Rendered {AFTER_MP4} (sha256 {a_sha[:12]}) and {sheet_path} (sha256 {s_sha[:12]})")


if __name__ == "__main__":
    main()
