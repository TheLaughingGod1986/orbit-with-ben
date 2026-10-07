#!/usr/bin/env python3
"""Review pack for Sun 022 first cut v03 (J0017, #99 6045051575).

Writes review_v03/: per-row sheet, one 1280-wide JPG at the middle of every row,
full-size frames at 0.0 s, 0.5 s, 1.0 s and the last frame, three frames from
row 104 (the end), row 90 and the rows 18/20 crops, row 96 frames from 456.8 s,
clip_check output and loudness.
The video itself stays out of git.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EP = HERE.parent
SHOT = HERE / "shot_list_v01.csv"
FILM = HERE / "sun_film/sun_first_cut_v03.mp4"
WORK = HERE / "sun_film/work_first_cut_v03"
OUT = HERE / "review_v03"
WORDS = EP / "02_Voiceover/words.json"

ROW51_TIMES = [237.0, 238.0, 238.6, 240.0, 241.5, 242.3]
ROW96_TIMES = [456.8, 457.5, 458.2, 459.0, 460.4, 461.2]
ROW104_TIMES = [497.0, 507.0, 517.0]


def probe(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def frame(t: float, dest: Path, width: int | None = None) -> None:
    vf = ["-vf", f"scale={width}:-2"] if width else []
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}",
                    "-i", str(FILM), "-frames:v", "1", *vf, "-q:v", "3", str(dest)], check=True)


def last_frame(dest: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-sseof", "-0.2",
                    "-i", str(FILM), "-update", "1", "-q:v", "2", str(dest)], check=True)


def ebur(path: Path, start: float | None = None, dur: float | None = None) -> dict:
    cmd = ["ffmpeg", "-hide_banner"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}", "-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    summary = err.split("Summary:")[-1]
    i = re.search(r"I:\s*([-\d.]+)\s*LUFS", summary)
    tp = re.search(r"Peak:\s*([-\d.]+)\s*dBFS", summary)
    lra = re.search(r"LRA:\s*([-\d.]+)\s*LU", summary)
    return {"integrated_lufs": float(i.group(1)) if i else None,
            "true_peak_dbtp": float(tp.group(1)) if tp else None,
            "lra_lu": float(lra.group(1)) if lra else None}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    total = probe(FILM)

    shutil.copy2(WORK / "per_row.png", OUT / "sun_first_cut_v03_per_row.png")

    index = []
    for r in rows:
        a, b = float(r["vo_in"]), float(r["vo_out"])
        mid = (a + b) / 2
        name = f"row_{int(r['row']):03d}.jpg"
        frame(mid, OUT / name, 1280)
        index.append({"row": int(r["row"]), "t": round(mid, 2), "source": r["source"], "id": r["id"]})

    frame(0.0, OUT / "full_t0000.jpg")
    frame(0.5, OUT / "full_t0005.jpg")
    frame(1.0, OUT / "full_t0010.jpg")
    last_frame(OUT / "full_last.jpg")

    for t in ROW51_TIMES:
        frame(t, OUT / f"row051_cue_t{t:06.1f}.jpg")
    for t in ROW96_TIMES:
        frame(t, OUT / f"row096_t{t:06.1f}.jpg")
    for t in ROW104_TIMES:
        frame(t, OUT / f"row104_t{t:06.1f}.jpg")

    cc = subprocess.run(["python3", str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
                         str(SHOT), "--words", str(WORDS), "--repeat-ok", "6"],
                        capture_output=True, text=True)
    (OUT / "clip_check.txt").write_text(cc.stdout + cc.stderr + f"\nexit={cc.returncode}\n")

    vo, music = WORK / "vo_spliced.wav", WORK / "music.wav"
    points = []
    for t in (20.0, 120.0, 238.0, 330.0, 457.5, 495.0):
        v = ebur(vo, t - 5.0, 10.0)["integrated_lufs"]
        m = ebur(music, t - 5.0, 10.0)["integrated_lufs"]
        f = ebur(FILM, t - 5.0, 10.0)["integrated_lufs"]
        gap = round(v - m, 1) if v is not None and m is not None else None
        points.append({"t": t, "window_s": 10, "vo_lufs": v, "bed_lufs": m,
                       "vo_minus_bed_lu": gap, "film_lufs": f})
    loud = {"film": FILM.name, "duration_s": round(total, 3), **ebur(FILM),
            "bed_alone": ebur(music), "vo_alone": ebur(vo),
            "vo_to_bed_points": points,
            "note": "Stems measured before the final loudnorm; the gap is VO stem minus bed stem in the same 10 s window."}
    (OUT / "loudness.json").write_text(json.dumps(loud, indent=2))
    (OUT / "rows.json").write_text(json.dumps(index, indent=2))
    print(json.dumps({"clip_check_exit": cc.returncode, **{k: loud[k] for k in
                      ("duration_s", "integrated_lufs", "true_peak_dbtp")}, "points": points}, indent=2))


if __name__ == "__main__":
    main()
