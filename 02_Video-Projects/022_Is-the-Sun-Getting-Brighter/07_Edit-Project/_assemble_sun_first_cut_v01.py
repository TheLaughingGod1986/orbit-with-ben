#!/usr/bin/env python3
"""Sun 022 first cut v01 from shot_list_v01.csv (J0001).

Reuses the Saturn v03b framing helpers (cover / feathered blur fill, <=2.35x).
Adds: pan / drift / pull moves, young and future Sun grades, two-disc compare,
lower-third chapter cards, the two VO pickups spliced at the lock's loudness,
SVS stretches (muted), and a 16 s hold on SVS 11517 to the end.

Media stays out of git: output goes to iCloud OWB UAT/sun_first_cut_v01/.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

EP = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ROOT = EP.parent
SAT = ROOT / "021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/_assemble_saturn_first_cut_v03b.py"
_spec = importlib.util.spec_from_file_location("sat", SAT)
sat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sat)

SHOT = HERE / "shot_list_v01.csv"
POOL_JSON = HERE / "nasa_pool_v01.json"
POOL_DIR = HERE / "nasa_pool_v01"
VO = EP / "02_Voiceover/parts/sun_brighter_vo_v01.wav"
PICKUPS = [
    # (pickup wav, lock mute start, lock mute end, pickup start)
    (EP / "02_Voiceover/sun_pickup_over_in_a_day_v01.wav", 41.85, 43.70, 41.90),
    (EP / "02_Voiceover/sun_pickup_three_clocks_v01.wav", 456.75, 460.40, 456.80),
]
CLIPS = EP / "04_Generated-Clips"
SVS = CLIPS / "svs"
CODE = CLIPS / "code_graphics"
WORK = HERE / "sun_film/work_first_cut_v01"
OUT_LOCAL = HERE / "sun_film/sun_first_cut_v01.mp4"
UAT_DIR = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/sun_first_cut_v01")
# No Sun score bed exists yet: temp bed, swap before final OK.
MUSIC = ROOT / "013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3"

W, H, FPS = sat.W, sat.H, sat.FPS
FONT = sat.FONT
sat.WORK = WORK
NOTES: list[str] = []


def run(cmd):
    sat.run([str(c) for c in cmd])


def svs_path(rid: str) -> Path:
    n = rid.replace("SVS", "").strip()
    for ext in (".mp4", ".mov"):
        p = SVS / f"svs{n}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(rid)


def playable(p: Path) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() not in ("", "N/A")


def stretch_window(path: Path, spec: str, dur: float, uses: dict) -> float:
    """Pick a clean stretch: stretch k of 3 across the clip, skipping 2 s at each end."""
    L = sat.probe(path)
    m = re.search(r"stretch\s*(\d)", spec or "")
    k = int(m.group(1)) if m else uses.get(path.name, 0) + 1
    uses[path.name] = uses.get(path.name, 0) + 1
    usable = max(0.0, L - 4.0 - dur)
    start = 2.0 + usable * (k - 1) / 2.0
    return max(0.0, min(start, L - dur - 0.05))


def ensure_still(nasa_id: str, pool: dict) -> Path:
    e = pool[nasa_id]
    p = POOL_DIR / e["section"] / f"{nasa_id}.jpg"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        print(f"fetch {nasa_id} {e['orig']}", flush=True)
        req = urllib.request.Request(e["orig"], headers={"User-Agent": "Mozilla/5.0"})
        p.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return p


def graded(still: Path, grade: str, dest: Path) -> Path:
    g = (grade or "").lower()
    if not g or "plate" in g:
        return still
    im = Image.open(still).convert("RGB")
    if "young" in g or "-30%" in g:
        im = ImageEnhance.Brightness(im).enhance(0.70)
        r, gg, b = im.split()
        r = r.point(lambda v: min(255, int(v * 1.04)))
        b = b.point(lambda v: int(v * 0.88))
        im = Image.merge("RGB", (r, gg, b))
    elif "future" in g or "+10%" in g:
        im = ImageEnhance.Brightness(im).enhance(1.10)
        w, h = im.size
        big = im.resize((int(w * 1.04), int(h * 1.04)), Image.Resampling.LANCZOS)
        x0, y0 = (big.width - w) // 2, (big.height - h) // 2
        im = big.crop((x0, y0, x0 + w, y0 + h))
    else:
        return still
    im.save(dest, quality=95)
    return dest


def parse_move(move: str) -> tuple[str, float]:
    mv = (move or "").lower()
    m = re.search(r"([\d.]+)\s*%", mv)
    p = float(m.group(1)) / 100.0 if m else 0.04
    if mv.startswith("pan l-r"):
        return "pan_lr", p
    if mv.startswith("pan r-l"):
        return "pan_rl", p
    if mv.startswith("drift up"):
        return "drift_up", p
    if mv.startswith("pull"):
        return "pull", p
    return "push", p


def still_move_mp4(base_png: Path, dest: Path, dur: float, move: str) -> None:
    kind, p = parse_move(move)
    n = max(1, int(round(dur * FPS)))
    d = max(n - 1, 1)
    zmax = 1.0 + min(p, 0.12)
    if kind == "push":
        z, x, y = f"1+{p:.4f}*on/{d}", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif kind == "pull":
        z, x, y = f"{zmax:.4f}-{p:.4f}*on/{d}", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    elif kind == "pan_lr":
        z, x, y = f"{zmax:.4f}", f"(iw-iw/zoom)*on/{d}", "(ih-ih/zoom)/2"
    elif kind == "pan_rl":
        z, x, y = f"{zmax:.4f}", f"(iw-iw/zoom)*(1-on/{d})", "(ih-ih/zoom)/2"
    else:
        z, x, y = f"{zmax:.4f}", "(iw-iw/zoom)/2", f"(ih-ih/zoom)*(1-on/{d})"
    vf = (f"scale=7680:-2,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", base_png,
         "-vf", vf, "-frames:v", n, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
         "-an", dest])


def motion_mp4(src: Path, dest: Path, src_in: float, dur: float) -> None:
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"fps={FPS},format=yuv420p")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{src_in:.3f}",
         "-t", f"{dur:.3f}", "-i", src, "-vf", vf, "-frames:v", int(round(dur * FPS)),
         "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", dest])


def concat(parts: list[Path], dest: Path) -> None:
    lst = dest.with_suffix(".txt")
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-an", dest])


def still_row(rid: str, r: dict, pool: dict, dest: Path, dur: float, move: str = "") -> None:
    still = ensure_still(rid, pool)
    still = graded(still, r.get("grade", ""), WORK / f"grade_{int(r['row']):03d}.jpg")
    base = WORK / f"still_{int(r['row']):03d}_{rid}.jpg"
    sat.compose_still_frame(still, base, row=str(r["row"]), rid=rid)
    still_move_mp4(base, dest, dur, move or r.get("move", ""))


def two_disc(r: dict, pool: dict, dest: Path, dur: float) -> None:
    still = ensure_still("PIA21218", pool)
    young = graded(still, "young", WORK / "two_disc_young.jpg")
    canvas = Image.new("RGB", (W, H), (4, 5, 8))
    for i, src in enumerate((young, still)):
        im = Image.open(src).convert("RGB")
        s = min((W / 2 - 60) / im.width, (H - 160) / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.Resampling.LANCZOS)
        canvas.paste(im, (int(W / 4 + i * W / 2 - im.width / 2), (H - im.height) // 2))
    base = WORK / "two_disc.jpg"
    canvas.save(base, quality=95)
    still_move_mp4(base, dest, dur, "push 3%")


def build_row(r: dict, pool: dict, dest: Path, uses: dict) -> None:
    src = r["source"].strip().upper()
    rid = r["id"].strip()
    dur = float(r["vo_out"]) - float(r["vo_in"])
    row = int(r["row"])

    if src == "NASA":
        still_row(rid, r, pool, dest, dur)
        return
    if src == "EDIT":
        two_disc(r, pool, dest, dur)
        return
    if src == "OMNI":
        fb = r["fallback"].replace("NASA ", "")
        fid, _, rest = fb.partition(" ")
        mv = rest.split("(")[0].strip()
        NOTES.append(f"row {row}: OMNI not generated in v01, fallback {fid} {mv}")
        still_row(fid, {**r, "grade": ""}, pool, dest, dur, mv)
        return
    if src == "CODE":
        clip = CODE / rid
        m = re.search(r"from\s*([\d.]+)\s*s", r["src_in"])
        start = float(m.group(1)) if m else 0.0
        start = min(start, max(0.0, sat.probe(clip) - dur))
        motion_mp4(clip, dest, start, min(dur, sat.probe(clip) - start))
        return
    if src == "GODDARD":
        if row == 18:
            a, b = WORK / "r018a.mp4", WORK / "r018b.mp4"
            motion_mp4(svs_path("SVS 3548"), a, 0.0, dur / 2)
            motion_mp4(svs_path("SVS 3549"), b, 0.0, dur - dur / 2)
            concat([a, b], dest)
            return
        try:
            path = svs_path(rid)
            ok = playable(path)
        except FileNotFoundError:
            ok = False
        if not ok:
            fb = r["fallback"].replace("NASA ", "").replace("(mute)", "").strip()
            if fb.startswith("SVS"):
                path = svs_path(fb)
            elif fb:
                NOTES.append(f"row {row}: {rid} unusable, fallback still {fb}")
                still_row(fb, r, pool, dest, dur, "push 4%")
                return
            else:
                path = svs_path("SVS 10925")
            NOTES.append(f"row {row}: {rid} unusable, used {path.name}")
        L = sat.probe(path)
        if L - 0.1 < dur:
            a, b = WORK / f"r{row:03d}a.mp4", WORK / f"r{row:03d}b.mp4"
            motion_mp4(path, a, 0.0, L - 0.1)
            still_row("PIA19876", r, pool, b, dur - (L - 0.1), "push 4%")
            concat([a, b], dest)
            NOTES.append(f"row {row}: {path.name} only {L:.2f}s, tail on PIA19876 (no slow-mo/loop)")
            return
        start = stretch_window(path, r["src_in"], dur, uses)
        motion_mp4(path, dest, start, dur)
        return
    raise ValueError(f"row {row}: unknown source {src}")


def card_png(title: str, dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = ImageFont.truetype(FONT, 64)
    dr = ImageDraw.Draw(im)
    bb = dr.textbbox((0, 0), title, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = 110, H - 150 - th
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((x - 30, y - 26, x + tw + 30, y + th + 34), fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    dr = ImageDraw.Draw(im)
    dr.rectangle((x - 30, y - 26, x - 22, y + th + 34), fill=(255, 140, 40, 255))
    dr.text((x, y - bb[1]), title, font=f, fill=(246, 246, 250, 255))
    im.save(dest)


def lufs_window(path: Path, start: float, dur: float) -> float:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
                        "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s*([-\d.]+)\s*LUFS", p.stderr)
    return float(m[-1])


def build_vo(total: float) -> Path:
    """Lock VO with each pickup laid over its muted span, gain-matched to the lock at that splice."""
    inputs = ["-i", str(VO)]
    mute = "+".join(f"between(t,{a:.3f},{b:.3f})" for _, a, b, _ in PICKUPS)
    fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume='if({mute},0,1)':eval=frame[l]"]
    mix = ["[l]"]
    for i, (wav, a, b, at) in enumerate(PICKUPS, start=1):
        lock = (lufs_window(VO, a - 6.0, 6.0) + lufs_window(VO, b, 6.0)) / 2.0
        pick = lufs_window(wav, 0.0, sat.probe(wav))
        gain = lock - pick
        NOTES.append(f"pickup {wav.stem}: lock {lock:.1f} LUFS at splice, pickup {pick:.1f}, gain {gain:+.1f} dB")
        inputs += ["-i", str(wav)]
        ms = int(round(at * 1000))
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,"
                  f"afade=t=in:d=0.02,adelay={ms}|{ms}[p{i}]")
        mix.append(f"[p{i}]")
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,"
              f"apad=whole_dur={total:.3f},atrim=0:{total:.3f}[vo]")
    out = WORK / "vo_spliced.wav"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
         "-filter_complex", ";".join(fc), "-map", "[vo]", out])
    return out


def build_mix(vo: Path, total: float) -> Path:
    bed_dur = sat.probe(MUSIC)
    fade = max(0.0, total - 12.0)
    music = WORK / "music.wav"
    if bed_dur + 0.05 >= total:
        fc = f"[0:a]atrim=0:{total:.3f},volume=0.12,afade=t=out:st={fade:.3f}:d=12[m]"
    else:
        cross = min(4.0, bed_dur / 8.0)
        loops = int(total // (bed_dur - cross)) + 1
        chain = "".join(f"[m{i}]" for i in range(loops))
        fc = f"[0:a]asplit={loops}" + chain + ";"
        prev = "m0"
        for i in range(1, loops):
            fc += f"[{prev}][m{i}]acrossfade=d={cross:.3f}:c1=tri:c2=tri[x{i}];"
            prev = f"x{i}"
        fc += f"[{prev}]atrim=0:{total:.3f},volume=0.12,afade=t=out:st={fade:.3f}:d=12[m]"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", MUSIC,
         "-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2", music])
    mixed = WORK / "mix.m4a"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", vo, "-i", music,
         "-filter_complex",
         "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:a", "aac", "-b:a", "192k", mixed])
    return mixed


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    pool = {e["nasa_id"]: e for e in json.loads(POOL_JSON.read_text())}
    rows = list(csv.DictReader(SHOT.open(newline="", encoding="utf-8")))
    total = float(rows[-1]["vo_out"])
    print(f"rows={len(rows)} total={total:.2f}s VO={sat.probe(VO):.2f}s", flush=True)

    uses: dict = {}
    parts = []
    for r in rows:
        dest = WORK / f"row_{int(r['row']):03d}.mp4"
        if not (dest.exists() and dest.stat().st_size > 1000):
            print(f"build row {r['row']} {r['source']} {r['id']}", flush=True)
            build_row(r, pool, dest, uses)
        parts.append(dest)

    picture = WORK / "picture_all.mp4"
    concat(parts, picture)

    cards = [(float(r["vo_in"]), r["caption"].split(":", 1)[1].strip())
             for r in rows if r["caption"].startswith("CHAPTER CARD")]
    inputs, fc, prev = ["-i", str(picture)], [], "[0:v]"
    for i, (t, title) in enumerate(cards, start=1):
        png = WORK / f"card_{i}.png"
        card_png(title, png)
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        st = t + 0.7
        fc.append(f"[{i}:v]format=rgba,fade=t=in:st={st:.2f}:d=0.4:alpha=1,"
                  f"fade=t=out:st={st + 2.1:.2f}:d=0.4:alpha=1[c{i}]")
        fc.append(f"{prev}[c{i}]overlay=0:0:enable='between(t,{st:.2f},{st + 2.5:.2f})'[v{i}]")
        prev = f"[v{i}]"
    fc.append(f"{prev}fade=t=out:st={total - 2.0:.3f}:d=2,format=yuv420p[v]")

    vo = build_vo(total)
    mix = build_mix(vo, total)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs, "-i", mix,
         "-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{len(cards) + 1}:a",
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", OUT_LOCAL])

    dur = sat.probe(OUT_LOCAL)
    lufs = sat.measure_lufs(OUT_LOCAL)
    sat.REVIEW = HERE / "review"
    sat.REVIEW.mkdir(exist_ok=True)
    sheet = WORK / "per_row.png"
    sat.per_row_sheet([(r, p) for r, p in zip(rows, parts)], sheet)
    h = hashlib.sha256(OUT_LOCAL.read_bytes()).hexdigest()
    meta = {
        "cut": "sun_first_cut_v01", "shot_list": SHOT.name, "vo": VO.name,
        "duration": dur, "sha256": h, "mix_lufs": lufs.get("integrated_lufs"),
        "true_peak": lufs.get("true_peak_dbtp"), "music_temp": MUSIC.name,
        "cant_fill_rows": sat.CANT_FILL, "notes": NOTES,
    }
    (WORK / "META.json").write_text(json.dumps(meta, indent=2))
    UAT_DIR.mkdir(parents=True, exist_ok=True)
    sat.chunk_write(OUT_LOCAL, UAT_DIR / OUT_LOCAL.name)
    sat.chunk_write(sheet, UAT_DIR / "sun_first_cut_v01_per_row.png")
    sat.chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    print("DONE", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    sys.exit(main())
