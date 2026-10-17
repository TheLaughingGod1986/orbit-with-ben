#!/usr/bin/env python3
"""028 Gliese 710 teaching overlays v01 (J0375, from J0360 TEACHING_GATE_PREP_v01.md):
AGENTS.md Reference lessons item 6 (Chief ruling 12 Oct: a to-scale graphic with no numeral does NOT count as NUMBER).
Renders the 7 harvest-plate teaching overlay rows for Chapters 3-6 of 028 (the four chapters without a numeral-bearing object):
- Chapter 3 (3 Into the Oort Cloud):
  * r24_sunrise (251.18-257.00s, iss_sunrise.jpg): 'In 8 minutes' at 252.76-255.20s (SOURCES row 13)
- Chapter 4 (4 The Comet Shower):
  * r26_hale_bopp (281.74-287.60s, comet_a3.jpg wide): 'About 10 extra comets' at 285.02-287.45s (SOURCES row 15)
  * r26_a3 (287.60-293.52s, comet_a3.jpg tight): '3 to 4 million' at 291.38-293.40s (SOURCES row 15)
- Chapter 5 (5 A New Brightest Star):
  * r29_twilight (348.20-354.40s, conjunction.tif): 'About 3 times brighter' at 348.20-351.20s (SOURCES row 18)
  * r31_moon_2 (369.00-373.20s, moon_lro.jpg): 'Every 35 years' at 371.04-373.05s (SOURCES row 20)
- Chapter 6 (6 It Has Happened Before):
  * r33_wise_craft (387.72-394.00s, wise_craft.jpg): 'About 70,000 years ago' at 387.72-391.20s (SOURCES row 21)
  * r34_sky_wide (403.30-412.00s, gaia_edr3_sky.png): '2.8 million years ago' at 403.46-407.20s (SOURCES row 22)

Writes house pill PNGs (`code_graphic_028_row*.png`), `overlays_v01.json`, `cuts_v01.json`, `OVERLAYS_v01.md`,
`overlay_stills_028_v01.jpg` (before/after stills), and runs `picture_qa.py` + `polish_gate.py`.
`--plan` prints the rows and checks without rendering."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
EP = HERE.parent
ROOT = EP.parents[1]
HDIR = HERE / "nasa_pool_v01" / "028_harvest_v01"
PACK = HERE / "teaching_overlays_v01_pack"
WORK = Path("/private/tmp/gliese028_overlays_work_v01")
BEFORE_MP4 = Path("/private/tmp/028_teaching_overlays_v01_before.mp4")
AFTER_MP4 = Path("/private/tmp/028_teaching_overlays_v01_after.mp4")

FPS = 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
NAVY = (23, 36, 55, 220)
ENC = ["-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p"]

# (row_id, chapter, film_in, film_out, src_file, box, pct, gamma, lift, ovs)
# Each ov in ovs: (ov_text, ov_in, ov_out, cx, y, px, check)
ROWS = [
    (
        "r04_shower_shell",
        "0 Open",
        18.02,
        23.02,
        HERE / "code_graphics_v02" / "code_graphic_028_r04_shower_shell_v02.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "1.3 million years",
                18.50,
                21.50,
                960,
                90,
                78,
                "SOURCES row 1: Bailer-Jones 2022 ApJL 935:L9 closest approach in 1.292 Myr (90% CI 1.257-1.334 Myr); VO 'one point three million years' at 18.50-20.58s",
            )
        ],
    ),
    (
        "r06_milky_way",
        "1 The Star Heading Our Way",
        42.78,
        50.10,
        HDIR / "eso_mw_lasilla.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "62 light-years away",
                45.08,
                48.00,
                960,
                860,
                78,
                "SOURCES row 2: Bailer-Jones 2022 ApJL 935:L9 Gaia DR3 parallax 52.433 mas (19.072 pc = 62.20 ly in Serpens); VO 'about 62 light-years away' at 45.08-46.90s",
            )
        ],
    ),
    (
        "r07_kdwarf",
        "1 The Star Heading Our Way",
        54.30,
        57.54,
        HERE / "code_graphics_v02" / "code_graphic_028_r07_kdwarf_v02.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "About 60%",
                55.54,
                57.40,
                960,
                90,
                78,
                "SOURCES row 3: Fernandez-Puig et al. 2026 Table 1 mass 0.595 +/- 0.013 M_sun (~60% Sun's mass); VO 'about 60%' at 55.54-56.52s",
            )
        ],
    ),
    (
        "r13_star_trails",
        "2 How Close Will It Come?",
        126.90,
        133.84,
        HDIR / "eso_startrails.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "In 1 million years",
                128.08,
                130.80,
                960,
                860,
                78,
                "SOURCES row 1: Bailer-Jones 2022 ApJL 935:L9 closest approach in 1.292 Myr (90% CI 1.257-1.334 Myr); VO 'in a million years' at 128.08-129.00s",
            )
        ],
    ),
    (
        "r15_gaia_craft",
        "2 How Close Will It Come?",
        147.76,
        154.00,
        HDIR / "gaia_craft.jpg",
        (0.04, 0.08, 0.96, 0.90),
        0.05,
        0.95,
        0.0,
        [
            (
                "1 billion stars",
                151.54,
                153.80,
                520,
                860,
                78,
                "SOURCES row 9: Gaia Collaboration Vallenari et al. 2023 A&A 674:A1 Gaia DR3 1.806 billion sources; VO 'more than a billion stars' at 151.54-152.90s",
            )
        ],
    ),
    (
        "r15_16_path",
        "2 How Close Will It Come?",
        166.90,
        169.80,
        HERE / "code_graphics_v02" / "code_graphic_028_r15_16_path_v02.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "10 to 13,000 times",
                167.40,
                169.75,
                960,
                90,
                76,
                "SOURCES row 10: Bailer-Jones 2022 ApJL 935:L9 0.0636 pc = 13,118 AU & de la Fuente Marcos 2022 RNAAS 6:136 0.051 pc = 10,520 AU; VO 'about 10 to 13,000 times' at 167.30-169.56s",
            )
        ],
    ),
    (
        "r16_sunrise_break",
        "2 How Close Will It Come?",
        169.80,
        175.50,
        HDIR / "iss_sunrise.jpg",
        (0.02, 0.16, 0.74, 0.64),
        0.05,
        0.68,
        8.0,
        [
            (
                "5 times closer",
                172.40,
                175.10,
                960,
                860,
                78,
                "SOURCES row 10: Bailer-Jones 2022 ApJL 935:L9 Hipparcos ~0.311 pc vs Gaia DR3 0.0636 pc (~4.89x, five times closer); VO 'five times closer' at 172.56-173.65s",
            )
        ],
    ),
    (
        "r17_neptune",
        "2 How Close Will It Come?",
        181.50,
        186.50,
        HDIR / "neptune.jpg",
        (0.04, 0.22, 0.96, 0.74),
        0.05,
        0.85,
        6.0,
        [
            (
                "30 centimetres away",
                184.54,
                186.35,
                960,
                860,
                76,
                "SOURCES row 11: NASA Neptune Fact Sheet a = 30.07 AU => 30.1 cm at 1 AU = 1 cm scale; VO '30 centimeters away' at 184.84-186.30s",
            )
        ],
    ),
    (
        "r24_sunrise",
        "3 Into the Oort Cloud",
        251.18,
        257.00,
        HDIR / "iss_sunrise.jpg",
        (0.05, 0.12, 0.95, 0.72),
        0.05,
        0.72,
        6.0,
        [
            (
                "In 8 minutes",
                252.76,
                255.20,
                960,
                860,
                78,
                "SOURCES row 13 (MUST QUOTE): NASA Oort Cloud Facts 'takes a little over eight minutes to reach Earth' (499.0 s = 8.32 min at 1 AU); VO 'in eight minutes' at 252.76-253.74s",
            )
        ],
    ),
    (
        "r26_hale_bopp",
        "4 The Comet Shower",
        281.74,
        287.60,
        HDIR / "comet_a3.jpg",
        (0.05, 0.04, 0.85, 0.49),
        0.05,
        0.55,
        12.0,
        [
            (
                "About 10 extra comets",
                285.02,
                287.45,
                960,
                860,
                76,
                "SOURCES row 15 (MUST QUOTE): Berski & Dybczynski 2016 A&A 595:L10 'mean density of approximately ten comets per year, lasting for 3 to 4 Myr'; VO 'about 10 extra comets' at 285.02-286.52s",
            )
        ],
    ),
    (
        "r26_a3",
        "4 The Comet Shower",
        287.60,
        293.52,
        HDIR / "comet_a3.jpg",
        (0.18, 0.08, 0.78, 0.42),
        0.05,
        0.55,
        12.0,
        [
            (
                "3 to 4 million",
                291.38,
                293.40,
                960,
                860,
                78,
                "SOURCES row 15 (MUST QUOTE): Berski & Dybczynski 2016 A&A 595:L10 'lasting for 3 to 4 Myr'; VO 'three to four million' at 291.38-292.90s",
            )
        ],
    ),
    (
        "r29_twilight",
        "5 A New Brightest Star",
        348.20,
        354.40,
        HDIR / "conjunction.tif",
        (0.05, 0.10, 0.95, 0.76),
        0.05,
        0.85,
        0.0,
        [
            (
                "About 3 times brighter",
                348.20,
                351.20,
                960,
                860,
                76,
                "SOURCES row 18: Berski & Dybczynski 2016 perihelion V = -2.7 mag vs Sirius V = -1.46 mag (3.13x brighter); VO 'about three times brighter' at 348.14-349.38s",
            )
        ],
    ),
    (
        "r31_moon_2",
        "5 A New Brightest Star",
        369.00,
        373.20,
        HDIR / "moon_lro.jpg",
        (0.04, 0.16, 0.96, 0.68),
        0.05,
        0.95,
        0.0,
        [
            (
                "Every 35 years",
                371.04,
                373.05,
                960,
                860,
                78,
                "SOURCES row 20: Berski & Dybczynski 2016 proper motion 52.28 arcsec/yr vs Moon ~1860 arcsec (35.58 yr); VO 'every 35 years' at 371.50-372.96s",
            )
        ],
    ),
    (
        "r33_wise_craft",
        "6 It Has Happened Before",
        387.72,
        394.00,
        HDIR / "wise_craft.jpg",
        (0.04, 0.08, 0.96, 0.92),
        0.05,
        0.95,
        0.0,
        [
            (
                "About 70,000 years ago",
                387.72,
                391.20,
                960,
                860,
                76,
                "SOURCES row 21: Mamajek et al. 2015 ApJL 800:L17 Scholz's Star flyby 70 +15/-10 kya; VO 'About 70,000 years ago' at 387.72-389.46s",
            )
        ],
    ),
    (
        "r33_traffic",
        "6 It Has Happened Before",
        395.50,
        401.00,
        HERE / "code_graphics_v02" / "code_graphic_028_r33_traffic_v02.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "Less than 1 light-year",
                396.58,
                399.20,
                960,
                860,
                76,
                "SOURCES row 21: Mamajek et al. 2015 ApJL 800:L17 Scholz's Star passed 0.25 +0.11/-0.07 pc = 0.82 ly (<1 ly) from the Sun; VO 'less than a light-year' at 396.58-397.66s",
            )
        ],
    ),
    (
        "r34_sky_wide",
        "6 It Has Happened Before",
        403.30,
        412.00,
        HDIR / "gaia_edr3_sky.png",
        (0.05, 0.05, 0.95, 0.95),
        0.05,
        0.90,
        0.0,
        [
            (
                "2.8 million years ago",
                403.46,
                407.20,
                960,
                860,
                76,
                "SOURCES row 22: Bailer-Jones 2022 ApJL 935:L9 HD 7977 close encounter 2.8 Myr ago (-2.761 Myr); VO 'about 2.8 million years ago' at 403.46-405.62s",
            ),
            (
                "HD 7977",
                408.80,
                411.50,
                960,
                860,
                78,
                "SOURCES row 22: Bailer-Jones 2022 ApJL 935:L9 solar-type G3 dwarf HD 7977 passed within <0.05 pc (P=1/3) 2.8 Myr ago; VO 'called HD 7977' at 408.52-410.50s",
            ),
        ],
    ),
    (
        "r35_lasilla_ntt",
        "6 It Has Happened Before",
        426.50,
        431.50,
        HDIR / "eso_lasilla_ntt.mp4",
        None,
        0.0,
        1.0,
        0.0,
        [
            (
                "1 star among billions",
                427.40,
                430.50,
                960,
                860,
                76,
                "SOURCES row 23: Bailer-Jones et al. 2018 A&A 616:A37 encounter rate 19.7 +/- 2.2 per Myr within 1 pc (~0.20 per Myr within 0.1 pc); VO 'one star among billions' at 427.50-429.16s",
            )
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


def compute_upscale(src: Path, box: tuple[float, float, float, float] | None, pct: float) -> float:
    if box is None:
        return 1.0
    im = Image.open(src)
    w, h = im.size
    cw = w * (box[2] - box[0])
    ch = h * (box[3] - box[1])
    return round(max(1920.0 / cw, 1080.0 / ch) * (1.0 + pct), 3)


def check_plan() -> list[str]:
    problems = []
    for row_id, ch, fin, fout, src, box, pct, gamma, lift, ovs in ROWS:
        if not src.exists():
            problems.append(f"missing source {src}")
            continue
        up = compute_upscale(src, box, pct)
        if up > 2.35:
            problems.append(f"{row_id} upscale {up:.2f} > 2.35")
        for text, a, b, cx, y, px, note in ovs:
            n = len(text.split())
            if n > 4:
                problems.append(f"{row_id} {text!r} has {n} words (>4)")
            if not any(c.isdigit() for c in text):
                problems.append(f"{row_id} {text!r} has no numeral")
            dur = b - a
            if dur > 4.05 or dur < 1.5:
                problems.append(f"{row_id} {text!r} duration {dur:.2f}s outside 1.5..4.0s")
            if a < fin - 0.01 or b > fout + 0.01:
                problems.append(f"{row_id} {text!r} ({a:.2f}-{b:.2f}) outside row ({fin:.2f}-{fout:.2f})")
            print(f"{row_id:18s} | {ch:26s} | film {a:6.2f}-{b:6.2f} ({dur:4.2f}s) | {text:24s} | up={up:4.2f}x | {note}")
    print("problems:", problems or "none")
    return problems


def render_still_push(src: Path, box: tuple[float, float, float, float], pct: float, gamma: float, lift: float, dur: float, dest: Path) -> None:
    frames = round(dur * FPS)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])))
    if gamma != 1.0 or lift != 0.0:
        arr = np.asarray(im, dtype=np.float32) / 255.0
        arr = np.clip((arr ** gamma) * 255.0 + lift, 0.0, 255.0).astype(np.uint8)
        im = Image.fromarray(arr)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    scale = max(2112.0 / im.width, 1188.0 / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x0 = (im.width - 2112) // 2
    y0 = (im.height - 1188) // 2
    im = im.crop((x0, y0, x0 + 2112, y0 + 1188))
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
        b_crop = ((W - bw) / 2.0, (H - bh) / 2.0, (W + bw) / 2.0, (H + bh) / 2.0)
        proc.stdin.write(im.resize((1920, 1080), Image.Resampling.BICUBIC, box=b_crop).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"still push failed: {dest}")


def render_code_clean_028(plate_id: str, plate_use: float, asset: str, off: float, dur: float, dest: Path) -> None:
    sys.path.insert(0, str(HERE))
    import build_code_graphics_v02 as cg

    frames = round(dur * FPS)
    boards = json.loads((HERE / "PLATE_BOARDS_v02.json").read_text())["plates"]
    plate = next(p for p in boards if p["id"] == plate_id)
    orig_labels = list(cg.LABELS.get(plate_id, []))
    cg.LABELS[plate_id] = []
    try:
        r = cg.Renderer(HERE / "code_graphics_v02" / "assets")
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
            t = off + n / FPS
            proc.stdin.write(r.frame(plate, t).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError(f"code render failed: {dest}")
    finally:
        cg.LABELS[plate_id] = orig_labels


VIDEO_OFFSETS = {
    "r04_shower_shell": 0.0,
    "r06_milky_way": 0.0,
    "r07_kdwarf": 0.0,
    "r13_star_trails": 2.0,
    "r15_16_path": 12.90,
    "r33_traffic": 1.50,
    "r35_lasilla_ntt": 2.74,
}


def main() -> None:
    problems = check_plan()
    if "--plan" in sys.argv or problems:
        raise SystemExit(1 if problems else 0)

    WORK.mkdir(parents=True, exist_ok=True)
    PACK.mkdir(parents=True, exist_ok=True)
    for old_png in PACK.glob("code_graphic_028_*.png"):
        old_png.unlink()

    before_segs = []
    after_segs = []
    cuts = []
    ov_records = []
    reel_t = 0.0
    pill_idx = 0

    for seg_i, (row_id, ch, fin, fout, src, box, pct, gamma, lift, ovs) in enumerate(ROWS):
        dur = round((fout - fin) * FPS) / FPS
        frames = round(dur * FPS)
        b_seg = WORK / f"before_{seg_i:02d}_{row_id}.mp4"
        base_after = WORK / f"base_after_{seg_i:02d}_{row_id}.mp4"
        a_seg = WORK / f"after_{seg_i:02d}_{row_id}.mp4"

        if box is None:
            off = VIDEO_OFFSETS.get(row_id, 0.0)
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
            if row_id in ("r04_shower_shell", "r07_kdwarf", "r33_traffic"):
                render_code_clean_028(row_id, 0.0, "", off, dur, base_after)
            else:
                shutil.copyfile(b_seg, base_after)
        else:
            render_still_push(src, box, pct, gamma, lift, dur, b_seg)
            shutil.copyfile(b_seg, base_after)

        inputs = ["-i", str(base_after)]
        fc = "[0:v]null[v0];"
        seg_ovs = []
        for k, (text, a, b, cx, y, px, note) in enumerate(ovs):
            pname = f"code_graphic_028_{row_id}_{pill_idx:02d}.png"
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
        cuts.append(
            {
                "row": row_id,
                "chapter": ch,
                "timeline_in": round(reel_t, 3),
                "timeline_out": round(reel_t + dur, 3),
                "film_in": fin,
                "film_out": fout,
                "source": src.name,
                "upscale": compute_upscale(src, box, pct),
                "framing": {"offset": VIDEO_OFFSETS.get(row_id, 0.0)} if box is None else {"box": list(box), "pct": pct},
                "overlays": seg_ovs,
            }
        )
        reel_t = round(reel_t + dur, 3)

    for tag, seg_list, dst in (("before", before_segs, BEFORE_MP4), ("after", after_segs, AFTER_MP4)):
        lst = WORK / f"concat_{tag}.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in seg_list))
        sp.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(dst)], check=True)

    (PACK / "overlays_v01.json").write_text(json.dumps({"film": "028", "job": "J0489", "labels": ov_records}, indent=2) + "\n")
    (PACK / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")

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
    sheet_path = PACK / "overlay_stills_028_v01.jpg"
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
