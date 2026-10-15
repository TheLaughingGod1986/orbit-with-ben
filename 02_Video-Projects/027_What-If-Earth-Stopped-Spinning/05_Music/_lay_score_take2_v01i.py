#!/usr/bin/env python3
"""027 Earth Spin v01i (J0265): lay the take-2 bed by chapter (Polish pass 2) and mux VO + bed + SFX. No spend.

  python3 _lay_score_take2_v01i.py --plan
  python3 _lay_score_take2_v01i.py --bed earth-spin_score_bed_v02.mp3 [--sections 0,25,95,180,250,360] [--bed-db -22]

Each chapter plays its own section of the one take-2 bed (BED_BRIEF_take2.md asks for both moods in one bed, so no
second cue is spent). Section k of the bed starts at --sections[k] (bed seconds; the defaults are the brief's own
times) and is laid from the chapter card, with a 3 s crossfade centred on each card (Polish pass 2: 2-4 s, never a
dip). Past the last word (7:22.8) the bed holds, then fades over the last 3 s. If the take's contour lands its
section changes elsewhere, pass the measured times with --sections; the film side doesn't move.
Writes earth-spin_score_take2_laid_v01i.wav (+ _plan.json, so music_gate sees the brief) here, then
/private/tmp/027_EarthSpin_rough_v01i_scored.mp4 (v01i picture copied, mix -14 LUFS / -1 dBTP), and runs
music_gate and sfx_kit level --bed into SCORE_GATES_v01i.json."""
from pathlib import Path
import argparse, json, subprocess as sp, sys

HERE = Path(__file__).resolve().parent
EP = HERE.parent
REPO = EP.parent.parent
MASTER = Path("/private/tmp/027_EarthSpin_rough_v01i.mp4")
WORK = Path("/private/tmp/earth027_score_v01i")
SFX = EP / "06_Sound-Effects/stem_sfx_v01i.wav"
OUT = Path("/private/tmp/027_EarthSpin_rough_v01i_scored.mp4")
XF = 3.0
LAST_WORD = 442.82
FADE = 3.0

# (chapter, card in v01i (s), mood, what the brief asks for, brief section start in the bed (s))
CHAPTERS = [
    ("Open", 0.0, "awe", "light and curious", 0.0),
    ("The Sudden Stop", 23.26, "explain", "taut rising pulse, peaks and eases, never crashes", 25.0),
    ("The Speed You Cannot Feel", 93.5, "explain", "relaxed and airy, the everyday spin", 95.0),
    ("A Slow Stop", 175.32, "awe", "spacious and slow, a planet that has stopped turning", 180.0),
    ("Earth Is Already Slowing", 248.38, "explain", "gently ticking and curious, clocks and tides", 250.0),
    ("Keeping Score", 356.78, "awe", "warm and grounded, close on a held chord", 360.0),
]


def dur(p):
    return float(sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def layout(film_s, sections):
    rows = []
    for k, (name, card, mood, ask, _) in enumerate(CHAPTERS):
        lay_in = 0.0 if k == 0 else card - XF / 2
        lay_out = film_s if k == len(CHAPTERS) - 1 else CHAPTERS[k + 1][1] + XF / 2
        b_in = max(0.0, sections[k] - (0.0 if k == 0 else XF / 2))
        rows.append(dict(chapter=name, mood=mood, brief=ask, card=card, lay_in=round(lay_in, 3), lay_out=round(lay_out, 3),
                         bed_in=round(b_in, 3), bed_out=round(b_in + lay_out - lay_in, 3),
                         crossfade=None if k == 0 else [round(card - XF / 2, 3), round(card + XF / 2, 3)]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bed", type=Path); ap.add_argument("--plan", action="store_true")
    ap.add_argument("--sections", default=",".join(str(c[4]) for c in CHAPTERS))
    ap.add_argument("--bed-db", type=float, default=-22.0, help="bed gain against the -14 LUFS VO")
    a = ap.parse_args()
    sections = [float(x) for x in a.sections.split(",")]
    assert len(sections) == len(CHAPTERS)
    film_s = dur(MASTER) if MASTER.exists() else 446.339
    rows = layout(film_s, sections)
    if a.plan or not a.bed:
        for r in rows:
            xf = f"xfade {mmss(r['crossfade'][0])}-{mmss(r['crossfade'][1])}" if r["crossfade"] else "start"
            print(f"{mmss(r['lay_in'])}-{mmss(r['lay_out'])}  {r['mood']:7} {r['chapter']:26} bed {mmss(r['bed_in'])}-{mmss(r['bed_out'])}  {xf}")
        print(f"hold past last word {mmss(LAST_WORD)}, fade {mmss(film_s - FADE)}-{mmss(film_s)}")
        return 0
    bed = a.bed if a.bed.is_absolute() else HERE / a.bed
    need = rows[-1]["bed_out"]
    if dur(bed) < need:
        sys.exit(f"bed is {dur(bed):.1f} s; the last section needs {need:.1f} s (pass --sections or a continuation)")
    WORK.mkdir(parents=True, exist_ok=True)
    parts = [f"[0:a]atrim={r['bed_in']}:{r['bed_out']},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[s{k}]"
             for k, r in enumerate(rows)]
    chain, prev = [], "s0"
    for k in range(1, len(rows)):
        chain.append(f"[{prev}][s{k}]acrossfade=d={XF}:c1=tri:c2=tri[x{k}]"); prev = f"x{k}"
    chain.append(f"[{prev}]atrim=0:{film_s},afade=t=out:st={film_s - FADE}:d={FADE},volume={a.bed_db}dB[bed]")
    laid = HERE / "earth-spin_score_take2_laid_v01i.wav"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(bed), "-filter_complex", ";".join(parts + chain), "-map", "[bed]", str(laid)], check=True)
    src_plan = bed.with_name(bed.stem + "_plan.json")
    plan = json.loads(src_plan.read_text()) if src_plan.exists() else {}
    plan.update(audio_file=laid.name, laid_from=bed.name, laid_for="rough_v01i", chapters=rows, crossfade_s=XF, bed_db=a.bed_db)
    laid.with_name(laid.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    vo = WORK / "stem_vo_v01i.wav"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(MASTER), "-map", "0:a", "-ac", "2", "-ar", "48000", str(vo)], check=True)
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(MASTER), "-i", str(vo), "-i", str(laid), "-i", str(SFX), "-filter_complex",
            "[1:a][2:a][3:a]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1:LRA=11[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(OUT)], check=True)
    gates = {}
    r = sp.run([sys.executable, str(REPO / "scripts/music_gate.py"), str(EP), "--bed", str(laid), "--video", str(OUT),
                "--out", str(WORK / "music_gate.json")], capture_output=True, text=True)
    gates["music_gate"] = dict(exit=r.returncode, out=r.stdout.strip()[-1500:])
    r = sp.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level", "--vo", str(vo), "--sfx", str(SFX), "--bed", str(laid),
                "--minutes", f"{film_s / 60:.2f}"], capture_output=True, text=True)
    gates["sfx_level"] = dict(exit=r.returncode, out=r.stdout.strip())
    (HERE / "SCORE_GATES_v01i.json").write_text(json.dumps(dict(bed=bed.name, laid=laid.name, cut=str(OUT), gates=gates), indent=2) + "\n")
    print(json.dumps(gates, indent=2))
    return 1 if any(g["exit"] for g in gates.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
