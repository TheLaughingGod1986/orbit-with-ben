#!/usr/bin/env python3
"""Sun 022 first cut v03 (J0017), on Claude's v02 review (#99 6045051575).

Changes from v02, everything else is the v02 assembler:
- Row 1: SVS 13778 from 91.0 s (prominence already above the limb and moving at 0.0 s).
- Row 104: SVS 13778 from 96.6 s, a later stretch of the same clip, held to the end (no overlap with row 1).
- Row 3: off 13778 (so no clip is used for more than 2 stretches), onto SVS 11517 at 14.0 s (limb flare).
- Row 44: SVS 11112 from 36.0 s (clean limb, past the NASA HELIOPHYSICS title card).
- Row 96: clocks.mp4 re-rendered at 6.5 s ("hours to days"); in at 1.3 s so the first clock is lit at
  456.80 s and the climb lights last, at about 460.0 s.
- Row 90: s39-610-037 film edge-print digits masked to black (they sit on black sky).
- Rows 18, 20: SVS 3548 / 3549 cropped above the burned-in date line.
- Young-Sun grade (rows 53, 55, left disc of 71): -30% brightness, warm-neutral gold, no green.
- Loudness: two-pass loudnorm on the final mp4 audio to -14 LUFS, true peak target -2.0 dBTP.

Media stays out of git: output goes to iCloud OWB UAT/sun_first_cut_v03/.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("v01", HERE / "_assemble_sun_first_cut_v01.py")
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)
sat = v1.sat

EP = v1.EP
WORK_V02 = HERE / "sun_film/work_first_cut_v02"
WORK = HERE / "sun_film/work_first_cut_v03"
OUT_LOCAL = HERE / "sun_film/sun_first_cut_v03.mp4"
UAT_DIR = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/sun_first_cut_v03")
MUSIC = EP / "05_Music/sun-brighter_score_bed_v01.mp3"
OMNI_81 = EP / "04_Generated-Clips/01_Raw/omni_v01/sun_orbit_row81_omni_v01.mp4"
OMNI_81_IN = 0.5
SUB_ROW = 51
SUB_DUR = 4.0
# Black boxes over burnt-in text, in source pixels (x0, y0, x1, y1).
MASKS = {
    "PIA21218": (0, 1420, 390, 1500),
    "PIA19876": (0, 765, 320, 792),
    "s39-610-037": (330, 2700, 640, 3650),
}
# (clip, in-point) for SVS rows picked by eye in the v02 review.
SVS_PICK = {
    1: ("SVS 13778", 91.0),
    3: ("SVS 11517", 14.0),
    44: ("SVS 11112", 36.0),
    104: ("SVS 13778", 96.6),
}
CODE_IN = {96: 1.3}
# Keep the frame above the burned-in date line (source rows, of 1080).
CROP_BOTTOM = {"svs3548": 990, "svs3549": 990}
YOUNG_RGB = (1.12, 0.98, 0.76)
LOUD_I, LOUD_TP = -14.0, -2.0
REBUILD_ROWS = {1, 3, 18, 20, 44, 53, 55, 71, 90, 96, 104}

v1.WORK = WORK
sat.WORK = WORK
v1.OUT_LOCAL = OUT_LOCAL
v1.MUSIC = MUSIC

_ensure_still = v1.ensure_still


def ensure_still(nasa_id: str, pool: dict) -> Path:
    p = _ensure_still(nasa_id, pool)
    box = MASKS.get(nasa_id)
    if not box:
        return p
    clean = WORK / f"clean_{nasa_id}.jpg"
    if not clean.exists():
        im = Image.open(p).convert("RGB")
        x0, y0, x1, y1 = box
        ref = im.crop((x1, y0, min(im.width, x1 + (x1 - x0)), y1)).resize((1, 1), Image.Resampling.BOX)
        ImageDraw.Draw(im).rectangle(box, fill=ref.getpixel((0, 0)))
        im.save(clean, quality=97)
    return clean


v1.ensure_still = ensure_still

_graded = v1.graded


def graded(still: Path, grade: str, dest: Path) -> Path:
    g = (grade or "").lower()
    if not ("young" in g or "-30%" in g):
        return _graded(still, grade, dest)
    im = ImageEnhance.Brightness(Image.open(still).convert("RGB")).enhance(0.70)
    rm, gm, bm = YOUNG_RGB
    r, gg, b = im.split()
    im = Image.merge("RGB", (r.point(lambda v: min(255, int(v * rm))),
                             gg.point(lambda v: min(255, int(v * gm))),
                             b.point(lambda v: int(v * bm))))
    im.save(dest, quality=95)
    return dest


v1.graded = graded

_motion = v1.motion_mp4


def motion_mp4(src: Path, dest: Path, src_in: float, dur: float) -> None:
    keep = CROP_BOTTOM.get(Path(src).stem)
    if not keep:
        return _motion(src, dest, src_in, dur)
    w = int(round(v1.W * keep / v1.H / 2)) * 2
    vf = (f"crop={w}:{keep}:(iw-{w})/2:0,scale={v1.W}:{v1.H},fps={v1.FPS},format=yuv420p")
    v1.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{src_in:.3f}",
            "-t", f"{dur:.3f}", "-i", src, "-vf", vf, "-frames:v", int(round(dur * v1.FPS)),
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", dest])


v1.motion_mp4 = motion_mp4

_build_row = v1.build_row


def build_row(r: dict, pool: dict, dest: Path, uses: dict) -> None:
    row = int(r["row"])
    dur = float(r["vo_out"]) - float(r["vo_in"])
    if row == 81:
        v1.motion_mp4(OMNI_81, dest, OMNI_81_IN, dur)
        v1.NOTES.append(f"row 81: Omni take kept, {OMNI_81_IN:.1f}-{OMNI_81_IN + dur:.2f} s, audio stripped")
        return
    if row in SVS_PICK:
        rid, t0 = SVS_PICK[row]
        v1.motion_mp4(v1.svs_path(rid), dest, t0, dur)
        v1.NOTES.append(f"row {row}: {rid} {t0:.1f}-{t0 + dur:.2f} s")
        return
    if row in CODE_IN:
        clip = v1.CODE / r["id"].strip()
        v1.motion_mp4(clip, dest, CODE_IN[row], dur)
        v1.NOTES.append(f"row {row}: {clip.name} {CODE_IN[row]:.1f}-{CODE_IN[row] + dur:.2f} s")
        return
    if row == 67:
        v1.NOTES.append("row 67: Omni take rejected by Claude (orange planet-Sun), fallback s04-41-1206")
    _build_row(r, pool, dest, uses)


v1.build_row = build_row


def needs_rebuild(r: dict) -> bool:
    return int(r["row"]) in REBUILD_ROWS


def cue_png(dest: Path) -> None:
    im = Image.new("RGBA", (v1.W, v1.H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(v1.FONT, 40)
    label = "SUBSCRIBE"
    bb = dr.textbbox((0, 0), label, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad_x, pad_y = 34, 20
    bw, bh = tw + 2 * pad_x, th + 2 * pad_y
    x1, y1 = v1.W - 80, v1.H - 90
    x0, y0 = x1 - bw, y1 - bh
    dr.rounded_rectangle((x0, y0, x1, y1), radius=12, fill=(204, 0, 0, 235))
    dr.text((x0 + pad_x, y0 + pad_y - bb[1]), label, font=f, fill=(255, 255, 255, 255))
    im.save(dest)


def two_pass_loudnorm(path: Path) -> dict:
    """Measure, then a linear loudnorm on the audio only; the picture is copied."""
    flt = f"loudnorm=I={LOUD_I}:TP={LOUD_TP}:LRA=11"
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", flt + ":print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])
    second = (f"{flt}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    tmp = path.with_name(path.stem + "_ln.mp4")
    v1.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path, "-map", "0:v", "-map", "0:a",
            "-c:v", "copy", "-af", second, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", tmp])
    tmp.replace(path)
    return {"pass1": {k: m[k] for k in ("input_i", "input_tp", "input_lra", "target_offset")},
            "target": {"I": LOUD_I, "TP": LOUD_TP}}


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(v1.SHOT.open(newline="", encoding="utf-8")))
    total = float(rows[-1]["vo_out"])
    rebuilt = []
    for r in rows:
        name = f"row_{int(r['row']):03d}.mp4"
        dest, old = WORK / name, WORK_V02 / name
        if needs_rebuild(r):
            rebuilt.append(int(r["row"]))
            dest.unlink(missing_ok=True)
        elif not dest.exists() and old.exists():
            shutil.copy2(old, dest)
    print(f"v03: rebuilding rows {rebuilt}", flush=True)

    sub = next(r for r in rows if int(r["row"]) == SUB_ROW)
    cue = WORK / "subscribe_cue.png"
    cue_png(cue)
    st = float(sub["vo_in"]) + 0.3
    loud: dict = {}

    _run = v1.run

    def run(cmd):
        cmd = [str(c) for c in cmd]
        final = str(OUT_LOCAL) == cmd[-1] and "-filter_complex" in cmd
        if final:
            i = cmd.index("-filter_complex")
            fc = cmd[i + 1].split(";")
            last = fc[-1]
            src = last.split("fade=t=out")[0]
            n_in = cmd.count("-i")
            fc[-1] = (f"[{n_in}:v]format=rgba,fade=t=in:st={st:.2f}:d=0.3:alpha=1,"
                      f"fade=t=out:st={st + SUB_DUR - 0.3:.2f}:d=0.3:alpha=1[sub];"
                      f"{src}[sub]overlay=0:0:enable='between(t,{st:.2f},{st + SUB_DUR:.2f})'[vs];"
                      f"[vs]fade=t=out" + last.split("fade=t=out", 1)[1])
            cmd[i + 1] = ";".join(fc)
            j = cmd.index("-filter_complex")
            cmd[j:j] = ["-loop", "1", "-t", f"{total:.3f}", "-i", str(cue)]
        _run(cmd)
        if final:
            loud.update(two_pass_loudnorm(OUT_LOCAL))

    v1.run = run
    v1.UAT_DIR = UAT_DIR
    real_chunk = sat.chunk_write

    def chunk_write(src, dest):
        name = Path(dest).name.replace("_v01", "_v03")
        return real_chunk(src, Path(dest).with_name(name))

    sat.chunk_write = chunk_write
    v1.main()

    meta_path = WORK / "META.json"
    meta = json.loads(meta_path.read_text())
    meta.update({"cut": "sun_first_cut_v03", "music": MUSIC.name, "rebuilt_rows": rebuilt,
                 "subscribe_cue": [round(st, 2), round(st + SUB_DUR, 2)], "loudnorm_two_pass": loud})
    meta.pop("music_temp", None)
    meta_path.write_text(json.dumps(meta, indent=2))
    sat.chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    print("V03", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    sys.exit(main())
