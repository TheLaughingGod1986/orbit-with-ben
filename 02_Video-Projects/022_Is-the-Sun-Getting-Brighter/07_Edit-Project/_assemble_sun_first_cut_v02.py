#!/usr/bin/env python3
"""Sun 022 first cut v02 (J0001), on Claude's v01 rulings (#99 6042034289, 6043236182).

Changes from v01, everything else is the v01 assembler:
- Sun score bed (05_Music/sun-brighter_score_bed_v01.mp3, 525 s) replaces the Moon stand-in.
- Rows 51 and 91 back on SVS 5649 (full 1024p copy); the 16:9 cover crop removes its date stamp.
- Row 81: Omni take KEEP, 0.5 s in (Claude: usable 0.5-6.0 s), audio stripped.
- Row 67: Omni take REJECTED, stays on fallback s04-41-1206.
- PIA21218 corner timestamp and PIA19876 caption line masked to black (both sit on black sky),
  so every use is clean, including both discs of the compare.
- 4 s lower-right subscribe cue under row 51 (the subscribe line), no Orbit.

Rows untouched by those changes are reused from the v01 work folder.
Media stays out of git: output goes to iCloud OWB UAT/sun_first_cut_v02/.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("v01", HERE / "_assemble_sun_first_cut_v01.py")
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)
sat = v1.sat

EP = v1.EP
WORK_V01 = v1.WORK
WORK = HERE / "sun_film/work_first_cut_v02"
OUT_LOCAL = HERE / "sun_film/sun_first_cut_v02.mp4"
UAT_DIR = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/sun_first_cut_v02")
MUSIC = EP / "05_Music/sun-brighter_score_bed_v01.mp3"
OMNI_81 = EP / "04_Generated-Clips/01_Raw/omni_v01/sun_orbit_row81_omni_v01.mp4"
OMNI_81_IN = 0.5
SUB_ROW = 51
SUB_DUR = 4.0
# Black boxes over burnt-in text, in source pixels (x0, y0, x1, y1).
MASKS = {
    "PIA21218": (0, 1420, 390, 1500),
    "PIA19876": (0, 765, 320, 792),
}
REBUILD_ROWS = {20, 51, 67, 81, 91}

v1.WORK = WORK
sat.WORK = WORK
v1.OUT_LOCAL = OUT_LOCAL
v1.MUSIC = MUSIC
v1.SVS_IN = {**v1.SVS_IN}

_ensure_still = v1.ensure_still


def ensure_still(nasa_id: str, pool: dict) -> Path:
    p = _ensure_still(nasa_id, pool)
    box = MASKS.get(nasa_id)
    if not box:
        return p
    clean = WORK / f"clean_{nasa_id}.jpg"
    if not clean.exists():
        im = Image.open(p).convert("RGB")
        ImageDraw.Draw(im).rectangle(box, fill=(0, 0, 0))
        im.save(clean, quality=97)
    return clean


v1.ensure_still = ensure_still

_build_row = v1.build_row


def build_row(r: dict, pool: dict, dest: Path, uses: dict) -> None:
    row = int(r["row"])
    if row == 81:
        dur = float(r["vo_out"]) - float(r["vo_in"])
        v1.motion_mp4(OMNI_81, dest, OMNI_81_IN, dur)
        v1.NOTES.append(f"row 81: Omni take kept, {OMNI_81_IN:.1f}-{OMNI_81_IN + dur:.2f} s, audio stripped")
        return
    if row == 67:
        v1.NOTES.append("row 67: Omni take rejected by Claude (orange planet-Sun), fallback s04-41-1206")
    _build_row(r, pool, dest, uses)


v1.build_row = build_row


def needs_rebuild(r: dict) -> bool:
    if int(r["row"]) in REBUILD_ROWS or r["source"].strip().upper() == "EDIT":
        return True
    text = " ".join(r.get(k, "") for k in ("id", "fallback"))
    return any(k in text for k in MASKS)


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


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(v1.SHOT.open(newline="", encoding="utf-8")))
    total = float(rows[-1]["vo_out"])
    rebuilt = []
    for r in rows:
        name = f"row_{int(r['row']):03d}.mp4"
        dest, old = WORK / name, WORK_V01 / name
        if needs_rebuild(r):
            rebuilt.append(int(r["row"]))
        elif not dest.exists() and old.exists():
            shutil.copy2(old, dest)
    print(f"v02: rebuilding rows {rebuilt}", flush=True)

    sub = next(r for r in rows if int(r["row"]) == SUB_ROW)
    cue = WORK / "subscribe_cue.png"
    cue_png(cue)
    st = float(sub["vo_in"]) + 0.3

    # Run the v01 pipeline with the cue spliced into its final overlay chain.
    _run = v1.run

    def run(cmd):
        cmd = [str(c) for c in cmd]
        if str(OUT_LOCAL) == cmd[-1] and "-filter_complex" in cmd:
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

    v1.run = run
    v1.UAT_DIR = UAT_DIR
    real_chunk = sat.chunk_write

    def chunk_write(src, dest):
        name = Path(dest).name.replace("_v01", "_v02")
        return real_chunk(src, Path(dest).with_name(name))

    sat.chunk_write = chunk_write
    v1.main()

    meta_path = WORK / "META.json"
    meta = json.loads(meta_path.read_text())
    meta.update({"cut": "sun_first_cut_v02", "music": MUSIC.name, "rebuilt_rows": rebuilt,
                 "subscribe_cue": [round(st, 2), round(st + SUB_DUR, 2)]})
    meta.pop("music_temp", None)
    meta_path.write_text(json.dumps(meta, indent=2))
    sat.chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    print("V02", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    sys.exit(main())
