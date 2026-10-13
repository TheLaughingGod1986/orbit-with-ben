#!/usr/bin/env python3
"""OWB compilation film (J0167) step 7: gates on the final join.

Writes a QA copy of the cut list (upscale per source, film bodies marked as footage at offset 0 so polish_gate
doesn't push-check a 9-minute body as a still) and a pool naming every source, then runs:
  - picture_qa.py (with polish_gate) on the final mp4
  - sfx_kit.py level on the VO, SFX and bed stems
  - music_gate.py on the laid score (new-material bed + the films' own audio under their bodies), under Chief's
    bed ruling #99 6134719677 rule (a): own/brief/reused waived for this compilation, gap and length enforced
  - a frame sheet of every join (0.6 s before, on, 0.6 s after)

  python3 _qa_compilation_v01.py [--final /private/tmp/owb_comp/final_v01] [--out qa_compilation_v01]
"""
import argparse
import json
import subprocess as sp
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
UPSCALE = {"021": 1.0, "013": 1.0, "019": 1.5, "007": 1.5, "005": 1.5, "comp": 1.0}
TITLES = {
    "saturn_first_cut_v03f": "OWB 021 passed master (Saturn rings film)",
    "MOON_LEAVING_FULL_v04_WATCH_THIS": "OWB 013 passed master (Moon leaving film)",
    "andromeda_collision_rough_v06": "OWB 019 uploaded master (Andromeda collision film)",
    "neutron_star_STUDIO_OWNER": "OWB 007 uploaded master (neutron star film)",
    "last_star_STUDIO_OWNER": "OWB 005 uploaded master (last star film)",
}
BODY_FILM = {"body_021": "saturn_first_cut_v03f", "body_013": "MOON_LEAVING_FULL_v04_WATCH_THIS",
             "body_019": "andromeda_collision_rough_v06", "body_007": "neutron_star_STUDIO_OWNER",
             "body_005": "last_star_STUDIO_OWNER"}


def run(cmd, log):
    log.write(f"$ {' '.join(map(str, cmd))}\n")
    log.flush()
    r = sp.run(list(map(str, cmd)), capture_output=True, text=True)
    log.write(r.stdout + r.stderr + f"exit {r.returncode}\n\n")
    log.flush()
    return r.returncode, r.stdout + r.stderr


def qa_cuts(final: Path, out: Path) -> Path:
    cuts = json.loads((final / "cuts.json").read_text())
    for c in cuts:
        c["upscale"] = UPSCALE.get(c.get("film"), 1.0)
        if c["source"] in BODY_FILM or c.get("overlay"):
            c.setdefault("framing", {})["offset"] = 0
    p = out / "cuts_qa.json"
    p.write_text(json.dumps(cuts, indent=1))
    pool = [{"source": s, "title": t} for s, t in TITLES.items()]
    pool += [{"source": b, "title": f"{TITLES[s]}, trimmed body"} for b, s in BODY_FILM.items()]
    (out / "pool_qa.json").write_text(json.dumps(pool, indent=1))
    return p


def join_sheet(final: Path, out: Path) -> Path:
    from PIL import Image, ImageDraw
    a = json.loads((final / "assembly.json").read_text())
    video = Path(a["file"])
    joins = [(p["start_s"], f"{a['pieces'][i - 1]['name']} > {p['name']}") for i, p in enumerate(a["pieces"]) if i]
    w, h = 480, 270
    sheet = Image.new("RGB", (w * 3, h * len(joins)), (20, 20, 20))
    for j, (t, name) in enumerate(joins):
        for i, dt in enumerate((-0.6, 0.0, 0.6)):
            raw = sp.run(["ffmpeg", "-v", "error", "-ss", f"{max(t + dt, 0):.3f}", "-i", str(video), "-frames:v", "1",
                          "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
            im = Image.frombytes("RGB", (w, h), raw)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, w, 20], fill=(0, 0, 0))
            m, s = divmod(t + dt, 60)
            d.text((6, 4), f"{int(m)}:{s:05.2f}  {name}  {dt:+.1f}s", fill=(255, 210, 0))
            sheet.paste(im, (i * w, j * h))
    p = out / "joins_sheet.jpg"
    sheet.save(p, quality=82)
    return p


def laid_score(final: Path) -> Path:
    p = final / "score_laid.wav"
    if not p.exists():
        sp.run(["ffmpeg", "-v", "error", "-y", "-i", str(final / "stem_bed.wav"), "-i", str(final / "stem_film.wav"),
                "-filter_complex", "amix=inputs=2:normalize=0", str(p)], check=True)
    return p


def floored(final: Path, key: str) -> Path:
    """A copy of a stem with a -120 dBFS noise floor. ffmpeg's ebur128 prints no line for digital silence, so on the
    VO stem (silent under every film body) sfx_kit's 100 ms steps drifted ~9 min off the bed's and judged the wrong
    moments (final v02: VO at 9:58 against the bed at 0:55)."""
    d = final / "floored"
    d.mkdir(exist_ok=True)
    p = d / f"stem_{key}.flac"
    if not p.exists():
        sp.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(final / f"stem_{key}.wav"), "-f", "lavfi",
                "-i", "anoisesrc=a=0.000001:c=white:r=48000", "-filter_complex",
                "[1:a]aformat=channel_layouts=stereo[n];[0:a][n]amix=inputs=2:duration=first:normalize=0",
                "-c:a", "flac", str(p)], check=True)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", default="/private/tmp/owb_comp/final_v01")
    ap.add_argument("--out", default=str(HERE / "qa_compilation_v01"))
    a = ap.parse_args()
    final, out = Path(a.final), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    video = Path(json.loads((final / "assembly.json").read_text())["file"])
    minutes = json.loads((final / "assembly.json").read_text())["duration_s"] / 60
    res = {"job": "J0167", "video": str(video), "minutes": round(minutes, 2)}
    with open(out / "qa_run.log", "w") as log:
        cuts = qa_cuts(final, out)
        res["picture_qa"], txt = run([sys.executable, REPO / "scripts/picture_qa.py", video, "--cuts", cuts,
                                      "--pool", out / "pool_qa.json", "--out-dir", out], log)
        res["picture_qa_tail"] = txt.strip().splitlines()[-1] if txt.strip() else ""
        res["sfx_level"], txt = run([sys.executable, REPO / "scripts/sfx_kit.py", "level", "--vo", floored(final, "vo"),
                                     "--sfx", floored(final, "sfx"), "--bed", floored(final, "bed"),
                                     "--minutes", f"{minutes:.3f}", "--out", out / "sfx_level.json"], log)
        res["sfx_level_out"] = txt.strip()
        score = laid_score(final)
        res["music_gate"], txt = run([sys.executable, REPO / "scripts/music_gate.py", HERE, "--bed", score,
                                      "--video", video, "--out", out / "music_gate.json"], log)
        res["music_gate_out"] = txt.strip()
        res["joins_sheet"] = str(join_sheet(final, out))
    (out / "qa_summary.json").write_text(json.dumps(res, indent=1))
    print("done", json.dumps({k: v for k, v in res.items() if not k.endswith("_out")}))


if __name__ == "__main__":
    main()
