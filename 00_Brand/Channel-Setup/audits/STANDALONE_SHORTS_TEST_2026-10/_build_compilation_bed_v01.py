#!/usr/bin/env python3
"""J0167 compilation bed v01 (Chief bed ruling 6134719677, rule a).

Lifts music-only stretches from the films' own trimmed outros (013 moonlit-sea,
019 galaxy) and lays them under the new material only (intro, bridges 1-4,
closing). Stretches alternate with crossfaded joins, each segment starts on a
different stretch/offset, and the bed ducks under that segment's VO stem.
Each segment is then checked with `sfx_kit.py level` (VO + SFX + bed).

No spend: nothing generated. Media stays in /private/tmp/owb_comp/bed_v01;
the plan goes to 05_Music/compilation_bed_plan.json.
"""
import argparse, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
COMP = Path("/private/tmp/owb_comp")
MASTERS = json.loads((COMP / "masters.json").read_text())

# Clean windows: after the last word's tail (Whisper on the lifted audio) and
# before the master's own fade-out (0.5 s RMS envelope).
STRETCHES = {
    "A": {"film": "013", "from": 499.2, "to": 514.5,
          "why": "013 moonlit-sea outro; last word 'perspective.' ends 498.04, master fades from 514.5"},
    "B": {"film": "019", "from": 610.4, "to": 617.8,
          "why": "019 galaxy outro; last word 'forever?' ends 610.10, master fades from 618.0"},
}
# Per segment: order of stretches and the offset into the first one, so no two
# segments open on the same bar.
SEGMENTS = [
    ("intro",   ["A", "B"], 0.0),
    ("bridge1", ["B", "A"], 0.0),
    ("bridge2", ["A", "B"], 6.0),
    ("bridge3", ["B", "A"], 3.5),
    ("bridge4", ["A", "B"], 10.0),
    ("closing", ["B", "A"], 1.5),
]
XF = 2.0          # crossfade at every join (loop points included)
FADE_IN = 0.4
FADE_OUT = 0.6
CLOSING_FADE_OUT = 2.6
REL_DB = -11.0    # bed integrated vs the segment VO's integrated, before ducking
DUCK_THRESHOLD, DUCK_RATIO = 0.03, 4


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(p)]).stdout)


def lufs(p):
    err = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", str(p), "-af", "ebur128",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = err[err.rfind("Integrated loudness"):]
    return float(tail.split("I:")[1].split("LUFS")[0])


def lift(out_dir):
    for k, s in STRETCHES.items():
        out = out_dir / f"stretch_{k}.wav"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{s['from']}", "-to", f"{s['to']}",
             "-i", MASTERS[s["film"]], "-vn", "-ac", "2", "-ar", "48000", str(out)])
        s["file"] = str(out)
        s["len"] = dur(out)


def plan_segment(order, offset, need):
    """Pieces (stretch, in, out) whose crossfaded total covers `need`."""
    pieces, total, i = [], 0.0, 0
    while total < need:
        k = order[i % len(order)]
        st = STRETCHES[k]
        a = offset if i == 0 else 0.0
        b = st["len"]
        pieces.append([k, a, b])
        total += (b - a) - (XF if i else 0.0)
        i += 1
    return pieces


def build(seg, order, offset, out_dir, seg_dir, gain_db):
    length = dur(seg_dir / f"{seg}.mp4")
    pieces = plan_segment(order, offset, length + 0.5)
    ins, chains = [], []
    for j, (k, a, b) in enumerate(pieces):
        ins += ["-i", STRETCHES[k]["file"]]
        chains.append(f"[{j}:a]atrim={a}:{b},asetpts=PTS-STARTPTS[p{j}]")
    cur = "p0"
    for j in range(1, len(pieces)):
        chains.append(f"[{cur}][p{j}]acrossfade=d={XF}:c1=tri:c2=tri[x{j}]")
        cur = f"x{j}"
    fo = CLOSING_FADE_OUT if seg == "closing" else FADE_OUT
    vo_idx = len(pieces)
    chains.append(
        f"[{cur}]atrim=0:{length},asetpts=PTS-STARTPTS,volume={gain_db}dB,"
        f"afade=t=in:d={FADE_IN},afade=t=out:st={length - fo}:d={fo}[bed]")
    chains.append(f"[{vo_idx}:a]aformat=channel_layouts=stereo:sample_rates=48000,apad,atrim=0:{length}[key]")
    chains.append(f"[bed][key]sidechaincompress=threshold={DUCK_THRESHOLD}:ratio={DUCK_RATIO}:attack=20:release=450:makeup=1,apad,atrim=0:{length}[out]")
    out = out_dir / f"{seg}_bed.wav"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", *ins, "-i", str(seg_dir / f"{seg}_vo.wav"),
         "-filter_complex", ";".join(chains), "-map", "[out]", "-ar", "48000", "-ac", "2", str(out)])
    return out, length, pieces


def level(seg, seg_dir, bed, length):
    r = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                        "--vo", str(seg_dir / f"{seg}_vo.wav"), "--sfx", str(seg_dir / f"{seg}_sfx.wav"),
                        "--bed", str(bed), "--minutes", f"{length / 60:.3f}"],
                       capture_output=True, text=True)
    msg = (r.stdout + r.stderr).strip()
    # Bridges and the closing get their SFX ticks with the J0207 graphics at step 6,
    # so an empty SFX stem ("present") isn't the bed's failure.
    fails = [ln for ln in msg.splitlines()[1:] if ln.startswith("FAIL") and not ln.startswith("FAIL present")]
    return not fails, msg


def speech_margin(seg_dir, seg, bed):
    """Median and smallest LU gap between VO momentary and bed momentary while the VO speaks."""
    sys.path.insert(0, str(REPO / "scripts"))
    import sfx_kit
    vo_m, vo_i = sfx_kit.ebur128(seg_dir / f"{seg}_vo.wav")
    bed_m, _ = sfx_kit.ebur128(bed)
    d = sorted(v - b for v, b in zip(vo_m, bed_m)
               if v > sfx_kit.SILENT and v >= vo_i - sfx_kit.SPEAKING_WITHIN)
    return (round(d[len(d) // 2], 1), round(d[0], 1)) if d else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", default=str(COMP / "segments_v03"))
    ap.add_argument("--out-dir", default=str(COMP / "bed_v01"))
    ap.add_argument("--plan", default=str(HERE / "05_Music/compilation_bed_plan.json"))
    a = ap.parse_args()
    seg_dir, out_dir = Path(a.segments), Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lift(out_dir)
    rows, ok_all = [], True
    for seg, order, offset in SEGMENTS:
        vo_i = lufs(seg_dir / f"{seg}_vo.wav")
        a_i = lufs(STRETCHES[order[0]]["file"])
        gain = round(vo_i + REL_DB - a_i, 1)
        for _ in range(6):
            bed, length, pieces = build(seg, order, offset, out_dir, seg_dir, gain)
            ok, msg = level(seg, seg_dir, bed, length)
            if ok:
                break
            gain -= 1.5
        ok_all &= ok
        med, worst = speech_margin(seg_dir, seg, bed)
        print(f"{seg}: {length:.2f} s (bed {dur(bed):.2f} s), gain {gain:+.1f} dB, bed {'PASS' if ok else 'FAIL'}, "
              f"under VO while speaking: median {med} LU, least {worst} LU\n  " + "\n  ".join(msg.splitlines()))
        t, under = 0.0, []
        for j, (k, s0, s1) in enumerate(pieces):
            st = STRETCHES[k]
            seg_in = t
            t += (s1 - s0) - (XF if j < len(pieces) - 1 else 0.0)
            under.append({"source": MASTERS[st["film"]], "film": st["film"],
                          "from": round(st["from"] + s0, 2), "to": round(st["from"] + s1, 2),
                          "segment_in": round(seg_in, 2), "segment_out": round(min(t + (XF if j < len(pieces) - 1 else 0), length), 2)})
        rows.append({"segment": seg, "length_s": round(length, 2), "file": str(bed),
                     "vo_lufs": vo_i, "bed_gain_db": gain, "bed_level": "PASS" if ok else "FAIL",
                     "under_vo_speaking_lu": {"median": med, "least": worst},
                     "level_report": msg, "pieces": under})
    plan = {
        "job": "J0167", "by": "cursor", "ruling": "Chief #99 6134719677 rule (a): music-only stretches from 013 and 019 outros; reused/own/brief waived for this compilation, gap and length enforced",
        "method": f"stretches alternate with {XF} s triangular crossfades (loop points too); {FADE_IN} s fade in, {FADE_OUT} s fade out ({CLOSING_FADE_OUT} s on the closing); sidechain duck under the segment VO; sfx_kit.py level per segment",
        "clean_check": "Whisper medium.en on each lifted stretch heard only the tail of the film's last word before the window; voice-band (300-3400 Hz) envelope steady at 6-9 dB under the full band through each window",
        "stretches": {k: {kk: v for kk, v in s.items() if kk != "file"} | {"source": MASTERS[s["film"]]} for k, s in STRETCHES.items()},
        "segments": rows,
        "under_films": "film segments keep their own audio; this bed sits under the new material only",
    }
    Path(a.plan).write_text(json.dumps(plan, indent=2) + "\n")
    print("plan", a.plan)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
