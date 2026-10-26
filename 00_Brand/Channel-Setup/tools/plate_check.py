#!/usr/bin/env python3
"""Plate, end-hold and end-card checks from the Orbit Auditor's 26 Oct 2026 audit (Ben, 26 Oct 2026: audit findings
are written into the rules, not just reported). OWB only; not studio core.

Rules: AGENTS.md -> *Audit rules (Orbit Auditor, 26 Oct 2026)*, mirrored in .cursor/rules/orbit-build-long.mdc,
.cursor/rules/orbit-build-shorts.mdc and STUDIO_PLAYBOOK.md.

Long films (`long`), run on every broadcast export before review:
  FAIL  a plate repeats across beats: two samples at least MIN_GAP_S apart with SSIM >= PLATE_SSIM, unless the later
        occurrence is a deliberate callback named with --callback SEC (Sun h8HGfyShEHI reused its grey-disk plate about
        6 times and the sunspot inset 3 times)
  FAIL  the end hold is the opening plate: SSIM >= END_SSIM between any end-hold sample and any opening sample
        (Sun and Venus VBaYRPp85Sw: 0.98)
  FAIL  SUBSCRIBE burned into the picture (OCR; tesseract needed, otherwise a WARN to check by eye). End screens do
        that job (Sun ~4:00, Venus ~3:30)

Shorts (`short`), run next to gate_shorts_open.py:
  FAIL  runtime outside 22-27 s (--exempt REASON for the compilation, the J0216 test Shorts and Test A)
  FAIL  no end card in the last ~4 s: the linked long's exact title and its id (OCR of --long-title / --long-id)
  WARN  captions not found on most of the runtime (OCR)
  WARN  no house-yellow text in the last ~4 s (the long's id is set in yellow)
  WARN  Orbit big on screen in the first 5 s, or in most of the Short (Orbit is never the hero)

  python3 plate_check.py long  <broadcast.mp4> [--callback 312.0 ...] [--json] [--no-ocr]
  python3 plate_check.py short <short.mp4> --long-id h8HGfyShEHI --long-title "Is the Sun Getting Brighter?" [--json]

Exit 0 = PASS, 1 = FAIL, 2 = tool error. SSIM is global SSIM on small grey frames (gate_shorts_open.ssim).
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_shorts_open as g  # noqa: E402  (shared ffmpeg helpers, ssim, orbit_score)

# ---- long films
SAMPLE_FPS = 1.0          # one sample a second
FW, FH = 64, 36           # 16:9 grey sample
PLATE_SSIM = 0.90         # same plate (calibrated on h8HGfyShEHI / VBaYRPp85Sw, 26 Oct 2026)
MIN_GAP_S = 20.0          # two occurrences at least this far apart are two beats, not one held shot
CALLBACK_TOL_S = 3.0
END_SSIM = 0.90           # end hold vs opening plate (audit measured 0.98 on Sun and Venus)
OPEN_WINDOW = (0.5, 8.0)  # opening plate samples
END_WINDOW_S = 20.0       # end hold = the last 20 s of picture before the fade
DARK_MEAN = 18.0          # black / fade frames are skipped
FLAT_STD = 6.0            # flat chapter-card gradients are skipped
OCR_LONG_EVERY_S = 2.0
SUBSCRIBE_RX = re.compile(r"subscri|scribe", re.I)
# The Venus cue is a small red pill in the lower-right corner that full-frame OCR misses, so the corner is read too.
CORNER_VF = "crop=iw*0.4:ih*0.3:iw*0.6:ih*0.7,scale=iw*3:-2,format=gray,negate"

# ---- shorts
SHORT_BAND = (22.0, 27.0)
END_CARD_S = 4.0
CAPTION_MIN_SHARE = 0.80
TEXT_RATIO = 0.80
ORBIT_HERO_EARLY_S = 5.0
ORBIT_BIG = 0.010         # visor fraction that reads as Orbit big on screen (gate's 0.003 = Orbit present)
ORBIT_PRESENT = g.VISOR_FAIL
ORBIT_MAX_SHARE = 0.50
YELLOW_MIN_FRAC = 0.002


# ----------------------------------------------------------------------------- pure helpers (unit-tested)
def mean_std(px) -> tuple[float, float]:
    n = len(px)
    if n == 0:
        return 0.0, 0.0
    m = sum(px) / n
    return m, (sum((p - m) ** 2 for p in px) / n) ** 0.5


def usable(px) -> bool:
    m, s = mean_std(px)
    return m >= DARK_MEAN and s >= FLAT_STD


def ssim_matrix(frames: list[bytes]):
    """Pairwise SSIM, numpy when present (an 8-min film is ~500 samples), pure Python otherwise."""
    try:
        import numpy as np
    except ImportError:  # pragma: no cover - CI uses tiny inputs
        n = len(frames)
        return [[g.ssim(frames[i], frames[j]) for j in range(n)] for i in range(n)]
    a = np.array([list(f) for f in frames], dtype=np.float64)
    mu = a.mean(1)
    d = a - mu[:, None]
    var = (d * d).mean(1)
    cov = d @ d.T / a.shape[1]
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    num = (2 * mu[:, None] * mu[None, :] + c1) * (2 * cov + c2)
    den = (mu[:, None] ** 2 + mu[None, :] ** 2 + c1) * (var[:, None] + var[None, :] + c2)
    return (num / den).tolist()


def repeated_plates(times: list[float], frames: list[bytes], thr: float = PLATE_SSIM, gap: float = MIN_GAP_S,
                    callbacks: tuple[float, ...] = (), tol: float = CALLBACK_TOL_S) -> list[dict]:
    """Group samples into plates (SSIM >= thr), split each plate into occurrences (runs more than `gap` apart) and
    return every plate seen in two or more beats. Callback occurrences don't count as repeats."""
    keep = [i for i, f in enumerate(frames) if usable(f)]
    if len(keep) < 2:
        return []
    sub = [frames[i] for i in keep]
    m = ssim_matrix(sub)
    parent = list(range(len(keep)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a in range(len(keep)):
        for b in range(a + 1, len(keep)):
            if m[a][b] >= thr:
                parent[find(a)] = find(b)
    groups: dict[int, list[float]] = {}
    for k, i in enumerate(keep):
        groups.setdefault(find(k), []).append(times[i])
    out = []
    for ts in groups.values():
        ts.sort()
        runs: list[list[float]] = [[ts[0], ts[0]]]
        for t in ts[1:]:
            if t - runs[-1][1] > gap:
                runs.append([t, t])
            else:
                runs[-1][1] = t
        beats = [r for r in runs if not any(abs(r[0] - c) <= tol or r[0] - tol <= c <= r[1] + tol for c in callbacks)]
        if len(runs) >= 2 and len(beats) >= 2:
            out.append({"occurrences": len(runs), "counted": len(beats),
                        "at": [round(r[0], 1) for r in runs]})
    out.sort(key=lambda p: -p["occurrences"])
    return out


def end_hold_match(times: list[float], frames: list[bytes], dur: float, open_window=OPEN_WINDOW,
                   end_window: float = END_WINDOW_S) -> tuple[float, float | None, float | None]:
    """Best SSIM between an opening sample and an end-hold sample (the last `end_window` s of usable picture)."""
    good = [(t, f) for t, f in zip(times, frames) if usable(f)]
    opening = [(t, f) for t, f in good if open_window[0] <= t <= open_window[1]]
    if not good or not opening:
        return 0.0, None, None
    last = max(t for t, _ in good)
    ending = [(t, f) for t, f in good if t >= last - end_window and t > open_window[1]]
    best, bt_o, bt_e = 0.0, None, None
    for to, fo in opening:
        for te, fe in ending:
            s = g.ssim(fo, fe)
            if s > best:
                best, bt_o, bt_e = s, to, te
    return best, bt_o, bt_e


def duration_verdict(dur: float, exempt: str | None = None) -> list[str]:
    lo, hi = SHORT_BAND
    if exempt or lo <= dur <= hi:
        return []
    return [f"runtime {dur:.2f} s outside {lo:.0f}-{hi:.0f} s (Audit rules 26 Oct; --exempt only for the listed exceptions)"]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def text_has(ocr: str, want: str, ratio: float = TEXT_RATIO) -> bool:
    """Fuzzy: `want` (title or id) appears in OCR text. Ids compare case-insensitively with l/I/1 and O/0 folded."""
    if not want:
        return False
    fold = str.maketrans({"l": "1", "i": "1", "o": "0"})
    o, w = norm(ocr).translate(fold), norm(want).translate(fold)
    if not w:
        return False
    if w in o:
        return True
    ow, ww = o.replace(" ", ""), w.replace(" ", "")
    if ww in ow:
        return True
    n = len(ww)
    best = max((difflib.SequenceMatcher(None, ow[i:i + n], ww).ratio() for i in range(0, max(1, len(ow) - n + 1))),
               default=0.0)
    return best >= ratio


def has_words(ocr: str) -> bool:
    return bool(re.search(r"[A-Za-z]{3,}", ocr))


def yellow_frac(rgb: bytes) -> float:
    n = len(rgb) // 3
    if n == 0:
        return 0.0
    hit = 0
    for i in range(n):
        r, gg, b = rgb[3 * i], rgb[3 * i + 1], rgb[3 * i + 2]
        if r >= 200 and 160 <= gg <= 235 and b <= 90:
            hit += 1
    return hit / n


# ----------------------------------------------------------------------------- ffmpeg / OCR
def sample_grey(path: Path, fps: float, w: int, h: int) -> tuple[list[float], list[bytes]]:
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h}:flags=area",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    data = g.run(cmd).stdout
    size = w * h
    frames = [data[i:i + size] for i in range(0, len(data) - size + 1, size)]
    times = [(k + 0.5) / fps for k in range(len(frames))]
    return times, frames


def ocr_available() -> bool:
    return shutil.which("tesseract") is not None


def ocr_at(path: Path, t: float, width: int = 1280, vf: str | None = None) -> str:
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "f.png"
        g.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
               "-vf", vf or f"scale={width}:-2", str(png)])
        out = subprocess.run(["tesseract", str(png), "-", "--psm", "11"], capture_output=True, text=True)
        return out.stdout


def yellow_mask(rgb: bytes) -> bytes:
    """House-yellow pixels black on white, so OCR reads the yellow id on its own."""
    n = len(rgb) // 3
    out = bytearray(b"\xff" * n)
    for i in range(n):
        r, gg, b = rgb[3 * i], rgb[3 * i + 1], rgb[3 * i + 2]
        if r >= 190 and 150 <= gg <= 240 and b <= 110:
            out[i] = 0
    return bytes(out)


def ocr_yellow_at(path: Path, t: float, w: int = 720, h: int = 1280) -> str:
    rgb = g.raw_frame(path, w, h, t, "rgb24")
    with tempfile.TemporaryDirectory() as td:
        pgm = Path(td) / "y.pgm"
        pgm.write_bytes(b"P5 %d %d 255\n" % (w, h) + yellow_mask(rgb))
        return subprocess.run(["tesseract", str(pgm), "-", "--psm", "11"], capture_output=True, text=True).stdout


# ----------------------------------------------------------------------------- checks
def check_long(path: Path, callbacks: tuple[float, ...] = (), ocr: bool = True) -> dict:
    dur = g.duration_s(path)
    res = {"file": str(path), "kind": "long", "duration_s": round(dur, 2), "fails": [], "warns": []}
    times, frames = sample_grey(path, SAMPLE_FPS, FW, FH)
    reps = repeated_plates(times, frames, callbacks=callbacks)
    res["repeated_plates"] = reps
    for p in reps:
        res["fails"].append(f"plate repeated in {p['counted']} beats at {p['at']} s (SSIM >= {PLATE_SSIM}); "
                            "give each beat its own plate or name the callback with --callback")
    s, to, te = end_hold_match(times, frames, dur)
    res["end_vs_opening_ssim"] = round(s, 3)
    if s >= END_SSIM:
        res["fails"].append(f"end hold is the opening plate (SSIM {s:.3f} at {te:.1f} s vs {to:.1f} s)")
    if ocr and ocr_available():
        hits = []
        t = 1.0
        while t < dur - 0.5:
            if SUBSCRIBE_RX.search(ocr_at(path, t)) or SUBSCRIBE_RX.search(ocr_at(path, t, vf=CORNER_VF)):
                hits.append(round(t, 1))
            t += OCR_LONG_EVERY_S
        res["subscribe_ocr_s"] = hits
        if hits:
            res["fails"].append(f"SUBSCRIBE burned into the picture at {hits} s; end screens do that job")
    else:
        res["warns"].append("SUBSCRIBE OCR skipped (no tesseract / --no-ocr): check by eye that nothing says SUBSCRIBE")
    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    return res


def check_short(path: Path, long_id: str | None, long_title: str | None, exempt: str | None = None,
                ocr: bool = True) -> dict:
    dur = g.duration_s(path)
    res = {"file": str(path), "kind": "short", "duration_s": round(dur, 2), "fails": [], "warns": []}
    res["fails"] += duration_verdict(dur, exempt)
    if exempt:
        res["exempt"] = exempt
    end_ts = [max(0.0, dur - x) for x in (3.6, 2.6, 1.6, 0.6)]
    # yellow id
    yf = max(yellow_frac(g.raw_frame(path, 90, 160, t, "rgb24")) for t in end_ts)
    res["end_yellow_frac"] = round(yf, 4)
    if yf < YELLOW_MIN_FRAC and not exempt:
        res["warns"].append("no house-yellow text in the last ~4 s (the linked long's id is set in yellow)")
    # Orbit never the hero
    samples = [i * 0.5 for i in range(int(dur / 0.5))]
    vis = [(t, g.orbit_score(path, t)["visor_frac"]) for t in samples]
    early_big = [t for t, v in vis if t <= ORBIT_HERO_EARLY_S and v >= ORBIT_BIG]
    share = sum(1 for _, v in vis if v >= ORBIT_PRESENT) / max(1, len(vis))
    res["orbit_share"] = round(share, 2)
    if early_big:
        res["warns"].append(f"Orbit big on screen at {early_big} s (first {ORBIT_HERO_EARLY_S:.0f} s): Orbit is never the hero")
    if share > ORBIT_MAX_SHARE:
        res["warns"].append(f"Orbit in {share:.0%} of the Short: Orbit is never the hero")
    if ocr and ocr_available():
        cap_ts = [t + 0.5 for t in range(int(dur - END_CARD_S))]
        caps = [has_words(ocr_at(path, t, 720)) for t in cap_ts]
        cshare = sum(caps) / max(1, len(caps))
        res["caption_share"] = round(cshare, 2)
        if cshare < CAPTION_MIN_SHARE:
            res["warns"].append(f"captions found on {cshare:.0%} of 1 s samples (< {CAPTION_MIN_SHARE:.0%}): captions run the whole way")
        if not exempt:
            end_txt = " ".join(ocr_at(path, t, 720) for t in end_ts)
            res["end_ocr"] = re.sub(r"\s+", " ", end_txt).strip()[:300]
            if not long_id or not long_title:
                res["fails"].append("pass --long-id and --long-title: the last ~4 s must show both")
            else:
                if not text_has(end_txt, long_title):
                    res["fails"].append(f"end card: exact long title not found in the last ~4 s ({long_title!r})")
                id_txt = end_txt + " " + " ".join(ocr_yellow_at(path, t) for t in end_ts)
                if not text_has(id_txt, long_id, 0.85):
                    res["fails"].append(f"end card: long id {long_id} not found in the last ~4 s")
    else:
        res["warns"].append("OCR skipped (no tesseract / --no-ocr): check captions and the end card by eye")
    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    lo = sp.add_parser("long")
    lo.add_argument("mp4", type=Path)
    lo.add_argument("--callback", type=float, action="append", default=[],
                    help="time (s) of a deliberate callback occurrence; repeatable")
    sh = sp.add_parser("short")
    sh.add_argument("mp4", type=Path)
    sh.add_argument("--long-id")
    sh.add_argument("--long-title")
    sh.add_argument("--exempt", help="compilation | J0216 | Test A (named exceptions only)")
    for p in (lo, sh):
        p.add_argument("--json", action="store_true")
        p.add_argument("--no-ocr", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "long":
            res = check_long(a.mp4, tuple(a.callback), not a.no_ocr)
        else:
            res = check_short(a.mp4, a.long_id, a.long_title, a.exempt, not a.no_ocr)
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError, ValueError) as e:
        print(f"plate_check: tool error: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{res['verdict']}  {res['kind']}  {res['file']}  ({res['duration_s']} s)")
        for f in res["fails"]:
            print(f"  FAIL  {f}")
        for w in res["warns"]:
            print(f"  WARN  {w}")
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
