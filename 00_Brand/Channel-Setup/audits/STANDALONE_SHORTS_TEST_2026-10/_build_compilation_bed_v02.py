#!/usr/bin/env python3
"""J0167 compilation bed v02: same stretches and laying as v01, with a computed gain curve in place of the sidechain duck.

v01's sidechain duck held the bed a median 18-23 LU under the VO, which music_gate's gap test on the laid score read as
"the music nearly stops" next to the films' own audio (final v01, intro 0:03 for 50.5 s). v02 lays the bed un-ducked at
REL_DB under the segment VO's integrated loudness, then dips it only on the 100 ms steps where sfx_kit's bed rule needs
it (VO speaking and the bed within MARGIN LU of the VO's momentary), spread over the 400 ms momentary window and
ramped. Each segment is re-checked with `sfx_kit.py level`; on a FAIL the margin grows by 1.5 LU and it rebuilds.

  python3 _build_compilation_bed_v02.py [--segments /private/tmp/owb_comp/segments_v04] [--out-dir .../bed_v02]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "scripts"))
import _build_compilation_bed_v01 as v01  # noqa: E402
import sfx_kit  # noqa: E402

COMP = v01.COMP
SR = 48000
STEP = int(sfx_kit.STEP * SR)
REL_DB = -12.0
MARGIN = 11.5
SPREAD = 4  # steps either side: the 400 ms momentary window


def read(p):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(SR),
                          "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def write(p, a):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-",
                    "-c:a", "pcm_s24le", str(p)], input=a.astype(np.float32).tobytes(), check=True)


def dip(bed_path, vo_path, margin):
    vo_m, vo_i = sfx_kit.ebur128(vo_path)
    bed_m, _ = sfx_kit.ebur128(bed_path)
    n = min(len(vo_m), len(bed_m))
    need = np.zeros(n)
    for t in range(n):
        v, b = vo_m[t], bed_m[t]
        if v > sfx_kit.SILENT and v >= vo_i - sfx_kit.SPEAKING_WITHIN and b > sfx_kit.SILENT:
            need[t] = max(0.0, b - (v - margin))
    att = np.array([need[max(0, t - SPREAD):t + SPREAD + 1].max() for t in range(n)])
    a = read(bed_path)
    x = np.arange(len(a)) / STEP
    curve = np.interp(x, np.arange(n), -att, right=-att[-1] if n else 0.0)
    a *= (10 ** (curve / 20)).astype(np.float32)[:, None]
    write(bed_path, a)
    return float(att.max()) if n else 0.0, float(np.median(att)) if n else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", default=str(COMP / "segments_v04"))
    ap.add_argument("--out-dir", default=str(COMP / "bed_v02"))
    ap.add_argument("--plan", default=str(HERE / "05_Music/compilation_bed_plan_v02.json"))
    a = ap.parse_args()
    seg_dir, out_dir = Path(a.segments), Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    v01.DUCK_RATIO = 1  # sidechaincompress at ratio 1 passes the bed through un-ducked
    v01.lift(out_dir)
    rows, ok_all = [], True
    for seg, order, offset in v01.SEGMENTS:
        vo = seg_dir / f"{seg}_vo.wav"
        vo_i = v01.lufs(vo)
        gain = round(vo_i + REL_DB - v01.lufs(v01.STRETCHES[order[0]]["file"]), 1)
        margin = MARGIN
        for _ in range(5):
            bed, length, pieces = v01.build(seg, order, offset, out_dir, seg_dir, gain)
            worst, med = dip(bed, vo, margin)
            ok, msg = v01.level(seg, seg_dir, bed, length)
            if ok:
                break
            margin += 1.5
        ok_all &= ok
        sm, sl = v01.speech_margin(seg_dir, seg, bed)
        print(f"{seg}: {length:.2f} s, gain {gain:+.1f} dB, margin {margin} LU, dip max {worst:.1f} dB median "
              f"{med:.1f} dB, bed {'PASS' if ok else 'FAIL'}, under VO while speaking: median {sm} LU, least {sl} LU"
              f"\n  " + "\n  ".join(msg.splitlines()), flush=True)
        rows.append({"segment": seg, "length_s": round(length, 2), "file": str(bed), "vo_lufs": vo_i,
                     "bed_gain_db": gain, "dip_margin_lu": margin, "dip_max_db": round(worst, 1),
                     "bed_level": "PASS" if ok else "FAIL", "under_vo_speaking_lu": {"median": sm, "least": sl},
                     "level_report": msg, "pieces": [{"stretch": k, "from": s0, "to": s1} for k, s0, s1 in pieces]})
    plan = {"job": "J0167", "by": "cursor", "supersedes": "compilation_bed_plan.json (v01)",
            "ruling": "Chief #99 6134719677 rule (a), as v01",
            "method": f"v01 stretches and crossfades, laid un-ducked at {REL_DB} LU under the segment VO, then a computed "
                      f"dip only where sfx_kit's bed rule needs it (VO speaking, bed within {MARGIN} LU of VO momentary), "
                      f"spread over the 400 ms window; margin +1.5 LU per failed level check",
            "why": "final v01 music_gate gap FAIL: v01's sidechain duck sat the bed 18-23 LU under the VO",
            "stretches": {k: {kk: v for kk, v in s.items() if kk != "file"} for k, s in v01.STRETCHES.items()},
            "segments": rows}
    Path(a.plan).write_text(json.dumps(plan, indent=2) + "\n")
    print("plan", a.plan)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
