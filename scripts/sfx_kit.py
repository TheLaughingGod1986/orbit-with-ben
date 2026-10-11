#!/usr/bin/env python3
"""House sound-effects kit and SFX level check (Polish pass, Astrum ref, Chief 11 Oct 2026). Standard library only.

  python3 scripts/sfx_kit.py make --out-dir <film>/06_Sound-Effects/kit_v01 [--house owb|hos] [--seed 11]
  python3 scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> [--bed <music stem>] [--minutes <cut length>] [--out <json>]

make   Writes our own synthesised SFX as 48 kHz stereo WAVs, peak -12 dBFS, plus sfx_kit_manifest.json (sha256, seed,
       source "own synthesis"). Nothing is downloaded, bought or generated on a paid API, so there's no licence to
       track and no credit spent. The same --seed gives the same files.
         owb: rumble_low (4 s, deep swell under violent or huge shots), whoosh_soft (0.9 s, fly-throughs and fast
              moves), tick_ui (50 ms, a label, line, bar or timeline marker appearing)
         hos: rumble_low (the same), whoosh_soft (warmer, lower), tick_ink (a pen tap: a card or chart line inking in)
level  Reads EBU R128 momentary loudness (ffmpeg ebur128, 100 ms steps) of the separate stems and checks the SFX rule:
         under   FAIL the SFX stem's integrated loudness is less than 12 LU under the VO's
         speech  FAIL while the VO speaks (VO momentary within 10 LU of its integrated), the SFX is less than 10 LU under
                 the VO's momentary for 0.3 s or more (the bed rule, applied to SFX)
         gaps    FAIL in a VO pause the SFX is less than 6 LU under the VO's integrated (a rumble may swell in a pause,
                 never to speech level)
         bed     FAIL (with --bed) the bed is less than 10 LU under the VO's momentary while the VO speaks, for 0.3 s+
         present FAIL no SFX hit at all; WARN (with --minutes) fewer than 1 hit a minute in a long
Exit 1 on any FAIL. Whether each hit suits its shot is judged by ear in Chief's review."""
from __future__ import annotations

import argparse, hashlib, json, math, random, re, struct, subprocess as sp, sys, wave
from pathlib import Path

SR = 48000
PEAK_DBFS = -12.0
STEP = 0.1                # ebur128 prints every 100 ms
SFX_UNDER_I = 12.0        # SFX integrated at least 12 LU under VO integrated
SPEECH_UNDER = 10.0       # while VO speaks, SFX (and bed) at least 10 LU under VO momentary
GAP_UNDER_I = 6.0         # in a VO pause, SFX at least 6 LU under VO integrated
SPEAKING_WITHIN = 10.0    # VO momentary within 10 LU of its integrated = speaking
RUN_S = 0.3               # a breach must last this long to count
HIT_FLOOR = -50.0         # SFX momentary above this = a hit is sounding
SILENT = -70.0


# ---------- make ----------
def _onepole(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    y, out = 0.0, []
    for v in x:
        y = (1 - a) * v + a * y
        out.append(y)
    return out


def _highpass(x, fc):
    lo = _onepole(x, fc)
    return [a - b for a, b in zip(x, lo)]


def _norm(chs, peak_db=PEAK_DBFS):
    m = max(abs(v) for ch in chs for v in ch) or 1.0
    g = 10 ** (peak_db / 20) / m
    return [[v * g for v in ch] for ch in chs]


def rumble(rng, secs=4.0):
    n = int(SR * secs)
    chs = []
    for _ in range(2):
        b, white = 0.0, []
        for _ in range(n):
            b = 0.995 * b + rng.uniform(-1, 1)   # brown-ish noise
            white.append(b)
        low = _onepole(_onepole(white, 90), 90)
        low = _highpass(low, 22)                 # no DC / sub-sonic thump
        chs.append(low)
    env = [math.sin(math.pi * min(1.0, i / (0.45 * n))) ** 2 if i < 0.45 * n
           else (1 - (i - 0.45 * n) / (0.55 * n)) ** 1.5 for i in range(n)]
    return _norm([[v * e for v, e in zip(ch, env)] for ch in chs])


def whoosh(rng, secs=0.9, lo=500.0, hi=3200.0):
    n = int(SR * secs)
    noise = [rng.uniform(-1, 1) for _ in range(n)]
    out, y_lo, y_hp = [], 0.0, 0.0
    for i, v in enumerate(noise):
        p = i / n
        fc = lo + (hi - lo) * math.sin(math.pi * p)          # sweep up and back down
        a = math.exp(-2 * math.pi * fc / SR)
        y_lo = (1 - a) * v + a * y_lo                         # low-pass at the moving cutoff
        ah = math.exp(-2 * math.pi * (fc * 0.35) / SR)
        y_hp = (1 - ah) * y_lo + ah * y_hp                    # take off the lows under it
        env = math.sin(math.pi * p) ** 3
        out.append((y_lo - y_hp) * env)
    left = [v * math.cos(0.5 * math.pi * (0.2 + 0.6 * i / n)) for i, v in enumerate(out)]   # pans left to right
    right = [v * math.sin(0.5 * math.pi * (0.2 + 0.6 * i / n)) for i, v in enumerate(out)]
    return _norm([left, right])


def tick_ui(rng, secs=0.05, f=2400.0):
    n = int(SR * secs)
    s = [(math.sin(2 * math.pi * f * i / SR) + 0.25 * math.sin(2 * math.pi * 2 * f * i / SR))
         * math.exp(-i / (SR * 0.008)) * min(1.0, i / 24) for i in range(n)]
    return _norm([s, s])


def tick_ink(rng, secs=0.06):
    n = int(SR * secs)
    burst = [rng.uniform(-1, 1) * math.exp(-i / (SR * 0.004)) for i in range(n)]
    band = _highpass(_onepole(burst, 6000), 1500)
    thump = [0.5 * math.sin(2 * math.pi * 900 * i / SR) * math.exp(-i / (SR * 0.006)) for i in range(n)]
    s = [a + b for a, b in zip(band, thump)]
    return _norm([s, s])


KITS = {
    "owb": [("rumble_low", rumble, {}), ("whoosh_soft", whoosh, {}), ("tick_ui", tick_ui, {})],
    "hos": [("rumble_low", rumble, {}), ("whoosh_soft", whoosh, {"lo": 300.0, "hi": 1800.0, "secs": 1.0}),
            ("tick_ink", tick_ink, {})],
}


def write_wav(path, chs):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        frames = bytearray()
        for l, r in zip(*chs):
            frames += struct.pack("<hh", int(max(-1, min(1, l)) * 32767), int(max(-1, min(1, r)) * 32767))
        w.writeframes(bytes(frames))


def make(out_dir: Path, house="owb", seed=11):
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, fn, kw in KITS[house]:
        rng = random.Random(f"{house}:{name}:{seed}")
        chs = fn(rng, **kw)
        path = out_dir / f"sfx_{house}_{name}_v01.wav"
        write_wav(path, chs)
        rows.append(dict(file=path.name, seconds=round(len(chs[0]) / SR, 3), peak_dbfs=PEAK_DBFS,
                         sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    manifest = dict(kit=house, seed=seed, source="own synthesis (scripts/sfx_kit.py), no third-party samples",
                    licence="ours; no attribution needed", spend="none", files=rows)
    (out_dir / "sfx_kit_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


# ---------- level ----------
LINE = re.compile(r"t:\s*([\d.]+).*?M:\s*(-?[\d.]+|-inf).*?I:\s*(-?[\d.]+|-inf) LUFS")
SUMMARY_I = re.compile(r"Integrated loudness:\s*I:\s*(-?[\d.]+|-inf) LUFS", re.S)


def parse_ebur128(stderr: str):
    """Momentary loudness every 100 ms, and the integrated figure from the summary."""
    m_series = []
    for line in stderr.splitlines():
        hit = LINE.search(line)
        if hit:
            v = hit.group(2)
            m_series.append(SILENT if v == "-inf" else max(SILENT, float(v)))
    s = SUMMARY_I.search(stderr)
    integ = float(s.group(1)) if s and s.group(1) != "-inf" else SILENT
    return m_series, integ


def ebur128(path: Path):
    r = sp.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-filter_complex", "ebur128=peak=none",
                "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"sfx_kit: ffmpeg could not read {path}: {r.stderr[-300:]}")
    return parse_ebur128(r.stderr)


def _runs(flags):
    """(start, length) in steps for each run of True."""
    out, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i - start)); start = None
    return out


def _mmss(steps):
    t = steps * STEP
    return f"{int(t // 60)}:{t % 60:04.1f}"


def judge(vo_m, vo_i, sfx_m, sfx_i, bed_m=None, minutes=None):
    n = min(len(vo_m), len(sfx_m), len(bed_m) if bed_m is not None else 10 ** 9)
    vo_m, sfx_m = vo_m[:n], sfx_m[:n]
    fails, warns, need = [], [], max(1, round(RUN_S / STEP))
    speaking = [v > SILENT and v >= vo_i - SPEAKING_WITHIN for v in vo_m]
    hits = _runs([s > HIT_FLOOR for s in sfx_m])
    if not hits:
        fails.append("present: no SFX hit anywhere in the stem")
    elif minutes and len(hits) < minutes:
        warns.append(f"present: {len(hits)} hits in {minutes:.1f} min (fewer than 1 a minute)")
    if hits and sfx_i > vo_i - SFX_UNDER_I:
        fails.append(f"under: SFX integrated {sfx_i:.1f} LUFS is {vo_i - sfx_i:.1f} LU under the VO ({vo_i:.1f}); needs {SFX_UNDER_I:.0f}")
    for s, ln in _runs([sp_ and x > SILENT and x > v - SPEECH_UNDER for sp_, x, v in zip(speaking, sfx_m, vo_m)]):
        if ln >= need:
            fails.append(f"speech: SFX within {SPEECH_UNDER:.0f} LU of the VO at {_mmss(s)} for {ln * STEP:.1f} s")
    for s, ln in _runs([not sp_ and x > vo_i - GAP_UNDER_I for sp_, x in zip(speaking, sfx_m)]):
        if ln >= need:
            fails.append(f"gaps: SFX within {GAP_UNDER_I:.0f} LU of the VO's level in a pause at {_mmss(s)} for {ln * STEP:.1f} s")
    if bed_m is not None:
        for s, ln in _runs([sp_ and b > SILENT and b > v - SPEECH_UNDER for sp_, b, v in zip(speaking, bed_m[:n], vo_m)]):
            if ln >= need:
                fails.append(f"bed: music within {SPEECH_UNDER:.0f} LU of the VO at {_mmss(s)} for {ln * STEP:.1f} s")
    return dict(verdict="FAIL" if fails else "PASS", vo_integrated=vo_i, sfx_integrated=sfx_i, hits=len(hits),
                fails=fails, warns=warns)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("make"); mk.add_argument("--out-dir", type=Path, required=True)
    mk.add_argument("--house", choices=sorted(KITS), default="owb"); mk.add_argument("--seed", type=int, default=11)
    lv = sub.add_parser("level")
    lv.add_argument("--vo", type=Path, required=True); lv.add_argument("--sfx", type=Path, required=True)
    lv.add_argument("--bed", type=Path); lv.add_argument("--minutes", type=float); lv.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "make":
        m = make(a.out_dir, a.house, a.seed)
        for f in m["files"]:
            print(f"{f['file']}  {f['seconds']} s  sha256 {f['sha256'][:12]}")
        return 0
    vo_m, vo_i = ebur128(a.vo)
    sfx_m, sfx_i = ebur128(a.sfx)
    bed_m = ebur128(a.bed)[0] if a.bed else None
    res = judge(vo_m, vo_i, sfx_m, sfx_i, bed_m, a.minutes)
    if a.out:
        a.out.write_text(json.dumps(res, indent=2) + "\n")
    print(f"SFX level {res['verdict']}: VO {vo_i:.1f} LUFS, SFX {sfx_i:.1f} LUFS, {res['hits']} hits")
    for line in res["fails"]:
        print("FAIL", line)
    for line in res["warns"]:
        print("WARN", line)
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
