#!/usr/bin/env python3
"""J0954 — 030 Apophis Short v11. £0 local re-cut. No upload.

Same cut as v10 (audio, VO segments, captions, cuts, overlays, title, hook,
1.00 s forward loop). Only the rock layer changes: a code-rendered two-lobed
asteroid with alpha, so the whole body stays in frame. v10, v05 and every
older file stay untouched.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
SA = REPO / "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SA))
sys.path.insert(0, str(REPO / "04_Audio/tools"))
import _assemble_apophis_short_v05 as v05  # noqa: E402
import _assemble_standalone_shorts_v01 as sa  # noqa: E402
import _render_apophis_rock_v11 as rocklib  # noqa: E402
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402
sys.path.insert(0, str(REPO / "scripts"))
from short_c37 import finish_scan, limiter, loop_metrics, true_peak  # noqa: E402

VO_WAV = HERE / "02_Voiceover/trim/030_apophis_short_vo_v01_trim.wav"
WORDS_JSON = HERE / "02_Voiceover/trim/030_apophis_short_vo_v01_trim_words.json"
ROCK_DIR = Path("/private/tmp/j0954/rock_v11")
OVERLAY = HERE / "code_graphics_v01/code_graphic_030short_r05_scale_v01.mov"
BED_SRC = SA / "05_Music/owb-standalone-shorts_score_bed_v01.mp3"
BED_PLAN = SA / "05_Music/owb-standalone-shorts_score_bed_v01_plan.json"
KIT = SA / "06_Sound-Effects/compilation_kit_v01"
PLATES = Path("/private/tmp/j0932/plates")
WORK = Path("/private/tmp/j0954/work_v11")
OUT = HERE / "06_Final-Exports"
STEM = "030_apophis_short_v11"
FINAL = OUT / f"{STEM}.mp4"
AIR = "2026-10-28"
FPS = 30
SR = 48000
W, H = 1080, 1920
ROCK_FPS = 24
LOOP = 1.00
LEAD = 0.08
# v07 opened the rock at 0.15 s, when only a stub is in frame. 1.50 s is the
# full rock, and it leaves a forward 1 s of rock before frame 0.
ROCK0 = 1.50
ROCK1 = 3.80
OPEN_LEN = 2.40
# Title rides the fourth cut (c42): the cut moves 9.00 → 9.37, and the card
# still ends 0.15 s into the next shot, which is now 13.00.
TITLE_IN = 9.37
TITLE_OUT = 13.00
# (src_start, src_end, gap_after) on the trimmed VO. Stay (3.50–5.95) is not here.
# c42 moves only the starts that were clipping a voiced onset. Gaps stay.
SEGMENTS = [
    (6.12, 6.80, 0.12),    # Apophis, (kept)
    (0.79, 3.34, 0.14),    # will fly closer than some of our satellites.
    (0.07, 0.78, 0.14),    # An asteroid,
    (6.98, 8.84, 0.16),    # 340 metres wide (6.98 keeps /θ/ at 7.00)
    (11.97, 14.52, 0.16),  # on Friday the 13th, 2029.
    (14.86, 17.72, 0.16),  # Many satellites orbit at 36,000.
    (18.04, 18.78, 0.12),  # It will miss.
    (9.24, 9.66, 0.10),    # passes (kept)
    (9.66, 11.66, 0.12),   # 32,000 kilometres up (kept; contiguous with passes)
    (19.18, 20.52, 0.10),  # Half the world can look up (kept)
    (20.85, 21.56, 0.00),  # and watch
]
SPEC = {
    "hook": (("CLOSER", "THAN"), ("SATELLITES",)),
    "yellow": "SATELLITES",
    "title": ("An Asteroid Will Skim Past", "Earth on Friday the 13th"),
}


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lufs(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return float(__import__("re").findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def pcm(path: Path, ss: float, length: float) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
        "-ac", "2", "-ar", str(SR), "-f", "f32le", "-",
    ])
    x = np.frombuffer(raw, dtype=np.float32)
    if x.size % 2:
        x = x[:-1]
    return x.reshape(-1, 2)


def write_wav(path: Path, samples: np.ndarray) -> None:
    import wave
    pcm16 = (np.clip(samples, -1, 1) * 32767.0).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm16.tobytes())


def rms_series(ss: float, length: float, hop: float = 0.01) -> list[tuple[float, float]]:
    x = pcm(VO_WAV, ss, length)
    mono = x.mean(axis=1) if x.size else np.zeros(0, dtype=np.float32)
    hop_n = int(hop * SR)
    rows = []
    for i in range(0, max(0, len(mono) - hop_n + 1), hop_n):
        seg = mono[i:i + hop_n]
        rms = float(np.sqrt(np.mean(seg ** 2)) + 1e-12)
        rows.append((ss + i / SR, 20.0 * np.log10(rms)))
    return rows


_MONO: np.ndarray | None = None


def mono() -> np.ndarray:
    """Whole-file stereo mean. Same RMS the c42 note was measured with."""
    global _MONO
    if _MONO is None:
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(VO_WAV),
            "-ac", "2", "-ar", str(SR), "-f", "f32le", "-",
        ])
        x = np.frombuffer(raw, dtype=np.float32)
        if x.size % 2:
            x = x[:-1]
        _MONO = x.reshape(-1, 2).mean(axis=1)
    return _MONO


def frame_db(t0: float) -> float:
    samples = mono()
    i0 = int(round(t0 * SR))
    i1 = i0 + int(0.01 * SR)
    seg = samples[max(0, i0):max(0, i1)]
    if seg.size == 0:
        return -120.0
    return float(20.0 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12))


def splice_report() -> list[dict]:
    """Hard gate on every splice that is not a continuation of the previous row.

    A start fails when any 10 ms frame in the 30 ms before it is louder than
    −35 dB, or the 10 ms frame at the start is louder than −40 dB. Being inside
    another segment does not excuse it. c42 keeps 6.12 and 19.18 as they are:
    Apophis begins on its own onset, and Half's quiet /h/ is the noted pass.
    """
    rows = []
    prev_b = None
    for a, b, _gap in SEGMENTS:
        contiguous = prev_b is not None and abs(a - prev_b) < 1e-3
        pre = []
        for dt in (0.03, 0.02, 0.01):
            t0 = round(a - dt, 3)
            if t0 < 0:
                continue
            pre.append({"t": t0, "db": round(frame_db(t0), 1)})
        at = round(frame_db(a), 1)
        pre_max = max((p["db"] for p in pre), default=-120.0)
        rule_pass = pre_max <= -35.0 and at <= -40.0
        keep = any(abs(a - kept) < 1e-6 for kept in (6.12, 19.18))
        rows.append({
            "a": a,
            "b": b,
            "contiguous": contiguous,
            "pre_30ms": pre,
            "pre_max_db": pre_max,
            "at_db": at,
            "rule_pass": bool(contiguous or rule_pass),
            "c42_keep": bool(keep and not rule_pass and not contiguous),
            "ok": bool(contiguous or rule_pass or keep),
        })
        prev_b = b
    return rows


def patch_onsets(words: list[dict]) -> None:
    """The aligner starts these words on the vowel. Pull each start back to the onset."""
    fixes = (
        ("an", 0.10, 0.09),
        ("will", 0.82, 0.80),
        ("340", 7.20, 7.00),
        ("on", 12.00, 11.98),
        ("many", 14.92, 14.88),
        ("it", 18.12, 18.07),
        ("and", 20.88, 20.87),
        ("32,000", 9.92, 9.68),
        ("32000", 9.92, 9.68),
    )
    for w in words:
        token = w["word"].lower().rstrip(",.?!")
        for tok, old, new in fixes:
            if token == tok and abs(float(w["start"]) - old) < 0.04:
                w["start"] = new
                break


def _flat(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def hears_32000(text: str) -> bool:
    flat = _flat(text)
    good = ("32000" in flat) or ("thirtytwo" in flat and "thousand" in flat)
    return good or ("32" in flat and "thousand" in flat)


def hears_wrong_thousand(text: str) -> bool:
    flat = _flat(text)
    bad = ("52000", "22000", "42000", "fiftytwothousand", "twentytwothousand", "fortytwothousand")
    return any(b in flat for b in bad)


def hears_340(text: str) -> bool:
    flat = _flat(text)
    if "340" in flat:
        return True
    return "threehundred" in flat and ("forty" in flat or "40" in flat)


def hears_wrong_340(text: str) -> bool:
    """140, one hundred, a hundred, or a bare 40. A real 340 is not a bare 40."""
    if hears_340(text):
        return False
    flat = _flat(text)
    low = text.lower()
    if any(b in flat for b in ("onehundred", "ahundred", "140")):
        return True
    if re.search(r"\b40\b", low) or re.search(r"\bforty\b", low):
        return True
    return False


def asr_gate(mix: Path, wide: list[tuple[str, float, float]]) -> tuple[list[dict], list[dict]]:
    """small.en and medium.en on the payoff windows. Every model must hear 32,000.

    medium.en stops after the first sentence on the 11.6–16.0 s clip ("it will
    miss.") even though the number is in the same clip. Each window is also cut
    into 1.6 s slices so that sentence is transcribed. A slice that hears
    52,000, 22,000 or 42,000 fails the build.

    faster-whisper's PyAV decode passes metadata_errors, which this av build
    rejects, so each clip is decoded with ffmpeg and handed over as samples.
    """
    import faster_whisper.audio as audio
    from faster_whisper import WhisperModel

    audio.decode_audio = lambda input_file, sampling_rate=16000: input_file

    def load_span(a: float, b: float) -> np.ndarray:
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(mix),
            "-ac", "1", "-ar", "16000", "-f", "f32le", "-",
        ])
        return np.frombuffer(raw, dtype=np.float32)

    def spans_for(a: float, b: float) -> list[tuple[float, float]]:
        spans = [(round(a, 3), round(b, 3))]
        t = a
        while t < b - 0.5:
            spans.append((round(t, 3), round(min(b, t + 1.6), 3)))
            t += 1.2
        uniq = []
        for span in spans:
            if span not in uniq and span[1] - span[0] >= 0.8:
                uniq.append(span)
        return uniq

    windows = ((12.4, 15.0), (11.6, 16.0))
    rows = []
    wide_rows = []
    for name in ("small.en", "medium.en"):
        model = WhisperModel(name, device="cpu", compute_type="int8")
        for a, b in windows:
            heard = False
            for sa, sb in spans_for(a, b):
                segs, _info = model.transcribe(
                    load_span(sa, sb), language="en", beam_size=5, temperature=0.0,
                    condition_on_previous_text=False,
                )
                text = " ".join(s.text.strip() for s in segs).strip()
                ok = hears_32000(text)
                wrong = hears_wrong_thousand(text)
                heard = heard or ok
                rows.append({
                    "model": name, "window": [a, b], "slice": [sa, sb],
                    "text": text, "ok": ok, "wrong": wrong,
                })
                print(f"asr {name} {sa:.1f}-{sb:.1f} ok={ok} wrong={wrong} {text!r}", flush=True)
                if wrong:
                    raise SystemExit(f"ASR heard the wrong thousand ({name} {sa:.1f}-{sb:.1f}): {text}")
            if not heard:
                raise SystemExit(f"ASR missed 32,000 ({name} window {a:.1f}-{b:.1f})")
        for label, a, b in wide:
            segs, _info = model.transcribe(
                load_span(a, b), language="en", beam_size=5, temperature=0.0,
                condition_on_previous_text=False,
            )
            text = " ".join(s.text.strip() for s in segs).strip()
            ok = hears_340(text)
            wrong = hears_wrong_340(text)
            wide_rows.append({
                "model": name, "label": label, "window": [round(a, 3), round(b, 3)],
                "text": text, "ok": ok, "wrong": wrong,
            })
            print(f"asr340 {name} {label} {a:.2f}-{b:.2f} ok={ok} wrong={wrong} {text!r}", flush=True)
            if wrong or not ok:
                raise SystemExit(f"ASR missed 340 ({name} {label}): {text}")
        del model
    return rows, wide_rows


def build_vo() -> tuple[np.ndarray, list[dict], float, list[tuple[float, float, float]]]:
    words = json.loads(WORDS_JSON.read_text())["words"]
    patch_onsets(words)
    room = pcm(VO_WAV, 17.78, 0.22)
    pieces = [np.resize(room, (int(round(LEAD * SR)), 2)).astype(np.float32) * 0.15]
    cursor = LEAD
    spans = []
    for i, (a, b, gap) in enumerate(SEGMENTS):
        chunk = pcm(VO_WAV, a, b - a)
        if i == len(SEGMENTS) - 1:
            n = int(round(0.060 * SR))
            ramp = np.linspace(1.0, 0.0, n, dtype=np.float32)[:, None]
            chunk = chunk.copy()
            chunk[-n:] *= ramp
        pieces.append(chunk)
        spans.append((a, b, cursor))
        cursor += len(chunk) / SR
        if gap > 0:
            need = int(round(gap * SR))
            pieces.append(np.resize(room, (need, 2)).astype(np.float32) * 0.15)
            cursor += gap
    spoken = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        for a, b, new_a in spans:
            if a - 0.02 <= mid <= b + 0.02:
                spoken.append({
                    "word": w["word"],
                    "start": round(new_a + (w["start"] - a), 3),
                    "end": round(new_a + (w["end"] - a), 3),
                })
                break
    spoken.sort(key=lambda w: (w["start"], w["end"]))
    text = " ".join(w["word"] for w in spoken).lower()
    if "stay" in text or "i'll show" in text:
        raise SystemExit("Stay line survived the splice")
    return np.concatenate(pieces, axis=0), spoken, cursor, spans


def word_at(words: list[dict], text: str) -> dict:
    hits = [w for w in words if w["word"].lower().rstrip(",.?!") == text.lower()]
    if not hits:
        raise SystemExit(f"missing word {text!r}")
    return hits[0]


def black_pct(im: Image.Image) -> float:
    lum = np.asarray(im.convert("RGB")).astype(np.float32).mean(axis=2)
    return float((lum < 20).mean() * 100)


def load_rock() -> rocklib.CodeRock:
    if not (ROCK_DIR / ".done").exists():
        raise SystemExit(f"rock frames missing: {ROCK_DIR} (render still running or failed)")
    paths = sorted(ROCK_DIR.glob("[0-9][0-9][0-9][0-9].png"))
    if len(paths) < 184:
        raise SystemExit(f"rock frames {len(paths)} < 184")
    return rocklib.CodeRock(paths)


def straight_run(alpha: np.ndarray, thresh: float = 0.80) -> int:
    """Longest horizontal or vertical run of silhouette-edge pixels."""
    m = alpha > thresh
    edge = np.zeros(m.shape, dtype=bool)
    edge[1:] |= m[1:] ^ m[:-1]
    edge[:-1] |= m[:-1] ^ m[1:]
    edge[:, 1:] |= m[:, 1:] ^ m[:, :-1]
    edge[:, :-1] |= m[:, :-1] ^ m[:, 1:]
    ys, xs = np.where(edge)
    if ys.size == 0:
        return 0
    sub = edge[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = 0
    for a in (sub, sub.T):
        padded = np.pad(a, ((0, 0), (1, 1)))
        d = np.diff(padded.astype(np.int8), axis=1)
        for i in np.flatnonzero(a.any(axis=1)):
            s = np.flatnonzero(d[i] == 1)
            e = np.flatnonzero(d[i] == -1)
            n = min(s.size, e.size)
            if n:
                best = max(best, int((e[:n] - s[:n]).max()))
    return best


def rock_gate(rock: rocklib.CodeRock, rows: list, nframes: int, last_t: float) -> dict:
    """Hard fail unless every frame keeps the whole rock inside a 24 px margin."""
    worst = {
        "margin_px": 10_000,
        "area_ratio": 10.0,
        "straight_run_px": 0,
        "margin_t": 0.0,
        "area_t": 0.0,
        "straight_t": 0.0,
    }
    checked = 0
    for f in range(nframes):
        t = f / FPS
        i = max(j for j, r in enumerate(rows) if r[0] <= t + 1e-6)
        s, e, _name, _which, _cx, _cy, _z0, _z1, rk = rows[i]
        if rk is None:
            continue
        span = (last_t - s) if i == len(rows) - 1 else (e - s)
        k = min(max((t - s) / max(span, 1e-6), 0.0), 1.0)
        src_t = rk[0] + (rk[1] - rk[0]) * k
        scale = float(rk[2])
        dx = int(rk[3] + (rk[4] - rk[3]) * k)
        _rgb, alpha, src_area = rock.layer(src_t, scale, dx, rk[5])
        ys, xs = np.where(alpha > 0.04)
        if xs.size == 0:
            raise SystemExit(f"rock missing at {t:.2f}s")
        margin = int(min(xs.min(), ys.min(), W - 1 - xs.max(), H - 1 - ys.max()))
        placed = int((alpha > 0.45).sum())
        ratio = placed / max(1.0, src_area * scale * scale)
        run = straight_run(alpha)
        checked += 1
        if margin < worst["margin_px"]:
            worst["margin_px"] = margin
            worst["margin_t"] = round(t, 3)
        if ratio < worst["area_ratio"]:
            worst["area_ratio"] = round(ratio, 4)
            worst["area_t"] = round(t, 3)
        if run > worst["straight_run_px"]:
            worst["straight_run_px"] = run
            worst["straight_t"] = round(t, 3)
        if margin < 24 or ratio < 0.90 or run > 40:
            raise SystemExit(
                f"rock gate fail at {t:.2f}s margin {margin}px area {ratio:.3f} straight {run}px"
            )
        if f % 90 == 0:
            print(f"  rock gate {f}/{nframes} margin {margin} ratio {ratio:.3f} straight {run}", flush=True)
    worst["frames_checked"] = checked
    worst["pass"] = True
    worst["source"] = "code-rendered two-lobe Apophis, alpha, no matte"
    print("rock gate", json.dumps(worst), flush=True)
    return worst


def extract_overlay() -> list[Path]:
    d = WORK / "overlay"
    if not (d / ".done").exists():
        d.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-v", "error", "-i", OVERLAY, "-vf", f"scale={W}:{H}",
             "-pix_fmt", "rgba", d / "%04d.png"])
        (d / ".done").write_text("ok")
    return sorted(d.glob("*.png"))


def comp(plate: Image.Image, rock: rocklib.CodeRock, src_t: float, place: tuple) -> Image.Image:
    p = np.asarray(plate).astype(np.float32)
    fg, alpha, _area = rock.layer(src_t, *place)
    al = alpha[..., None]
    return Image.fromarray((fg * al + p * (1.0 - al)).clip(0, 255).astype(np.uint8))


def plate(path: Path, cx: float, cy: float) -> sa.Plate:
    pl = sa.Plate(path, "cover", cx, cy)
    pl.im = v05.grade(pl.im)
    return pl


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    vo, words, vo_end, spans = build_vo()
    total = round(vo_end + LOOP, 3)
    nframes = int(round(total * FPS))
    last_t = (nframes - 1) / FPS
    pad_n = int(round(total * SR)) - len(vo)
    if pad_n > 0:
        room = pcm(VO_WAV, 17.78, 0.22)
        vo = np.concatenate([vo, np.resize(room, (pad_n, 2)).astype(np.float32) * 0.15], axis=0)
    closer = word_at(words, "closer")
    num = word_at(words, "32,000")
    first = words[0]
    print(json.dumps({
        "vo_end": round(vo_end, 3), "total": total, "first": first["word"], "first_s": first["start"],
        "closer_s": closer["start"], "num_s": num["start"], "ratio": round(num["start"] / total, 3),
        "spoken": " ".join(w["word"] for w in words),
    }, indent=2))
    if first["start"] > 0.15:
        raise SystemExit("first word late")
    if closer["start"] > 1.50:
        raise SystemExit("closer late")
    if not (18.0 <= total <= 24.0):
        raise SystemExit(f"duration {total} outside 18–24")
    if num["start"] / total < 0.70:
        raise SystemExit("32,000 before 70%")
    if num["start"] < TITLE_OUT:
        raise SystemExit("32,000 still under the title card")
    splices = splice_report()
    print("splice check", json.dumps(splices), flush=True)
    bad = [r for r in splices if not r["ok"]]
    if bad:
        raise SystemExit(f"splice gate failed: {bad}")
    if "--audio-check" in sys.argv:
        print("audio-check only")
        return

    title_in, title_out = TITLE_IN, TITLE_OUT
    ov_start = round(num["start"] - 0.15, 3)
    ov_frames = extract_overlay()
    ov_end = round(min(ov_start + len(ov_frames) / FPS, vo_end - 0.15), 3)

    # Picture. First cut 2.40. No plate over 3.50 s. No Orbit.
    # The loop continues the open's pan, zoom and rock time forward, ending one frame before frame 0.
    span = last_t - vo_end
    cx_rate = (0.72 - 0.38) / OPEN_LEN
    z_rate = (1.18 - 1.06) / OPEN_LEN
    rock_rate = (ROCK1 - ROCK0) / OPEN_LEN
    dx_rate = (180 - (-200)) / OPEN_LEN
    cx_last = 0.38 - cx_rate / FPS
    z_last = 1.06 - z_rate / FPS
    rock_last = ROCK0 - 1.0 / ROCK_FPS
    dx_last = -200 - dx_rate / FPS
    rows = [
        (0.00, 2.40, "aurora_rock_open", "aurora", (0.38, 0.72), 0.48, 1.06, 1.18, (ROCK0, ROCK1, 1.20, -200, 180, -30)),
        (2.40, 5.91, "day_rock_wide", "day", 0.42, 0.58, 1.04, 1.12, (2.50, 4.40, 0.95, 30, 30, -20)),
        (5.91, 9.37, "aurora_rock_date", "aurora", 0.28, 0.64, 1.06, 1.12, (4.40, 6.20, 0.92, -20, -20, 10)),
        (9.37, 12.85, "day_rock_title", "day", 0.62, 0.72, 1.06, 1.14, (6.20, 7.60, 0.88, 40, 40, 30)),
        (12.85, 16.15, "day_scale", "day", 0.50, 0.64, 1.08, 1.14, None),
        (16.15, vo_end, "aurora_rock_watch", "aurora", 0.48, 0.55, 1.10, 1.14, (6.80, 7.40, 0.96, 10, 10, -30)),
        (vo_end, total, "aurora_rock_loop", "aurora",
         (cx_last - cx_rate * span, cx_last), 0.48, z_last - z_rate * span, z_last,
         (rock_last - rock_rate * span, rock_last, 1.20, dx_last - dx_rate * span, dx_last, -30)),
    ]
    for a, b, *_ in rows:
        if b - a > 3.80:
            raise SystemExit(f"plate {b - a:.2f}s too long")
    if rows[0][1] > 2.50:
        raise SystemExit("first cut late")

    print("loading code rock…", flush=True)
    rock = load_rock()
    gate = rock_gate(rock, rows, nframes, last_t)

    aurora = plate(PLATES / "aurora_crop.jpg", 0.5, 0.5)
    day = plate(PLATES / "iss034e048455.jpg", 0.5, 0.5)
    plates = {"aurora": aurora, "day": day}
    hook = sa.hook_png(SPEC)
    title = sa.title_png(SPEC)
    caps = sa.captions(words, vo_end)

    def picture(t: float) -> Image.Image:
        i = max(j for j, r in enumerate(rows) if r[0] <= t + 1e-6)
        s, e, _name, which, cx, cy, z0, z1, rk = rows[i]
        span = (last_t - s) if i == len(rows) - 1 else (e - s)
        k = (t - s) / max(span, 1e-6)
        k = min(max(k, 0.0), 1.0)
        pl = plates[which]
        cx0, cx1 = cx if isinstance(cx, tuple) else (cx, cx)
        pl.cx = cx0 + (cx1 - cx0) * k
        pl.cy = cy
        z = z0 + (z1 - z0) * k
        frame = pl.frame(z)
        if rk is not None:
            src_t = rk[0] + (rk[1] - rk[0]) * k
            dx = rk[3] + (rk[4] - rk[3]) * k
            frame = comp(frame, rock, src_t, (rk[2], int(dx), rk[5]))
        return frame

    f0 = picture(0.02)
    b0 = black_pct(f0)
    print(f"frame0 black {b0:.1f}% upscale open {aurora.upscale(1.18):.2f}")
    if b0 > 25:
        raise SystemExit(f"frame 0 black {b0:.1f}%")
    f0.save(WORK / "frame0.jpg", quality=90)

    if "--stills" in sys.argv:
        sheet_t = [0.0, 1.2, 2.5, 6.5, 10.0, 13.4, total - 0.08]
        tiles = []
        for t in sheet_t:
            im = picture(t).convert("RGBA")
            if t < 2.2:
                im.alpha_composite(hook)
            if title_in <= t < title_out:
                im.alpha_composite(title)
            if ov_start <= t < ov_end:
                im.alpha_composite(Image.open(ov_frames[min(len(ov_frames) - 1, int((t - ov_start) * FPS))]).convert("RGBA"))
            tiles.append(im.convert("RGB").resize((270, 480)))
        sheet = Image.new("RGB", (270 * len(tiles), 480))
        for i, im in enumerate(tiles):
            sheet.paste(im, (270 * i, 0))
        sheet.save(WORK / "stills.jpg", quality=88)
        print("stills", WORK / "stills.jpg")
        return

    raw = WORK / "picture.mp4"
    if "--reuse-picture" in sys.argv and raw.exists():
        print("reusing", raw, flush=True)
    else:
        enc = subprocess.Popen(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-vf", "noise=alls=4:allf=t,format=yuv420p",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", str(raw)],
            stdin=subprocess.PIPE)
        assert enc.stdin is not None
        for f in range(nframes):
            t = f / FPS
            frame = picture(t).convert("RGBA")
            if t < 2.2:
                frame.alpha_composite(hook)
            if title_in <= t < title_out:
                frame.alpha_composite(title)
            if ov_start <= t < ov_end:
                idx = min(len(ov_frames) - 1, int((t - ov_start) * FPS))
                frame.alpha_composite(Image.open(ov_frames[idx]).convert("RGBA"))
            for a, b, im in caps:
                if a <= t < b:
                    frame.alpha_composite(im)
                    break
            enc.stdin.write(frame.convert("RGB").tobytes())
            if f % 90 == 0:
                print(f"  frame {f}/{nframes}", flush=True)
        enc.stdin.close()
        if enc.wait():
            raise SystemExit("picture encode failed")

    vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
    write_wav(vo_stem, vo)
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED_SRC, "-af",
         f"aresample=48000,atrim=0:{total},volume=0.065,afade=t=in:st=0:d=0.25,afade=t=out:st={total - 0.5:.3f}:d=0.5",
         "-ac", "2", bed_stem])
    tick_at = ov_start + 0.35
    run(["ffmpeg", "-y", "-v", "error", "-i", KIT / "sfx_owb_rumble_low_v01.wav",
         "-i", KIT / "sfx_owb_tick_ui_v01.wav", "-filter_complex",
         f"[0:a]aresample=48000,volume=0.40,afade=t=out:st=1.5:d=0.7,atrim=0:2.3[s0];"
         f"[1:a]aresample=48000,volume=0.28,adelay={int(tick_at * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total}[a]",
         "-map", "[a]", "-ac", "2", sfx_stem])
    stems = OUT / f"{STEM}_stems"
    stems.mkdir(exist_ok=True)
    for p in (vo_stem, bed_stem, sfx_stem):
        run(["cp", p, stems / p.name])

    mix = "[1:a][2:a][3:a]amix=inputs=3:duration=longest:normalize=0,"
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", raw, "-i", vo_stem, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", mix + "loudnorm=I=-14:TP=-1:LRA=11:print_format=json[a]",
         "-map", "[a]", "-f", "null", "-"],
        capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = limiter(
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", vo_stem, "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", mix + norm + ",aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}",
         "-movflags", "+faststart", FINAL])

    metrics = finish_scan(FINAL, loop_metrics(FINAL))
    diff = metrics["loop_diff_masked"]
    measured = lufs(FINAL)
    peak = true_peak(FINAL)
    print(
        f"loop_diff_masked {diff:.2f} open_step {metrics['open_median_step']:.2f} "
        f"head {metrics['head_matches']} lufs {measured:.1f} tp {peak:.2f} dur {dur(FINAL):.2f}"
    )
    if peak > -1.0:
        raise SystemExit(f"true peak {peak:.2f} dBTP")
    piece = next(s for s in spans if abs(s[0] - 6.98) < 1e-6)
    an_w = word_at(words, "An")
    on_w = word_at(words, "on")
    wide = [
        ("340-tight", round(piece[2] - 0.05, 3), round(piece[2] + 1.40, 3)),
        ("340-phrase", round(an_w["start"] - 0.02, 3), round(on_w["end"] + 0.05, 3)),
    ]
    transcripts, transcripts_340 = asr_gate(FINAL, wide)

    cuts = []
    for s, e, name, which, cx, cy, z0, z1, rk in rows:
        src_plate = "iss023e058455" if which == "aurora" else "iss034e048455"
        base_up = aurora.upscale(1.0) if which == "aurora" else day.upscale(1.0)
        zmax = max(z0, z1)
        cuts.append({
            "row": name,
            "timeline_in": round(s, 3),
            "timeline_out": round(e, 3),
            "source": f"{name}.mp4",
            "upscale": round(base_up * max(z0, z1), 2),
            "video": True,
            "framing": {"offset": 0.0 if rk is None else rk[0]},
            "plate": src_plate,
        })
    pool = []
    for s, e, name, which, *_rest in rows:
        if "scale" in name:
            title = "NASA ISS day-side Earth under our own Apophis distance card"
        elif which == "day":
            title = "NASA ISS day-side Earth (iss034e048455) with code-rendered asteroid Apophis"
        else:
            title = "NASA ISS aurora Earth limb (iss023e058455) with code-rendered asteroid Apophis"
        pool.append({"file_id": f"{name}.mp4", "title": title})

    meta = {
        "job": "J0954",
        "version": "v11",
        "c45": "whole code-rendered two-lobe Apophis replaces the chopped Veo matte; v10 audio, cuts and loop unchanged",
        "rock_gate": gate,
        "splice_check": splices,
        "asr": transcripts,
        "asr_340": transcripts_340,
        "replaces_for_review": "scheduled v05 BbsyFrV8kCY stays untouched",
        "air_date": AIR,
        "youtube_id": "BbsyFrV8kCY",
        "title_on_screen": " ".join(x for pair in SPEC["title"] for x in pair) if False else "An Asteroid Will Skim Past Earth on Friday the 13th",
        "file": str(FINAL.relative_to(REPO)),
        "sha256": sha256(FINAL),
        "duration_s": round(dur(FINAL), 2),
        "spoken": " ".join(w["word"] for w in words),
        "words": words,
        "spend": "none",
        "frame_0_plate": "iss023e058455 aurora limb + code-rendered whole Apophis, not the dusk plate",
        "brief": {
            "frame_0": "moving code-rendered Apophis on NASA iss023e058455 aurora limb, full-bleed, no Orbit",
            "first_word_s": first["start"],
            "surprise_s": closer["start"],
            "first_cut_s": 2.40,
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": num["start"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff": round(diff, 2),
            "loop_diff_masked": round(diff, 2),
            "open_median_step": round(metrics["open_median_step"], 2),
            "head_matches": metrics["head_matches"],
            "loop": "forward into frame 0, rock src ends one frame before frame 0",
            "true_peak_db": peak,
            "lufs": measured,
            "frame0_black_pct": round(b0, 1),
            "title_window_s": [title_in, title_out],
            "scale_window_s": [ov_start, ov_end],
        },
        "audio": {"stems": {"vo": str((stems / "stem_vo.wav").relative_to(REPO))},
                  "bed": "owb-standalone-shorts_score_bed_v01.mp3",
                  "mix": "two-pass loudnorm -14 LUFS"},
        "cuts": cuts,
        "loop_sentence": "…and watch. Apophis will fly closer than some of our satellites.",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    (OUT / f"{STEM}_cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / f"{STEM}_pool.json").write_text(json.dumps(pool, indent=2) + "\n")

    sheet = OUT / f"{STEM}_2fps.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-i", FINAL, "-vf", "fps=1,scale=180:320,tile=6x4", "-frames:v", "1", sheet])
    phone = OUT / f"{STEM}_PHONE.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.04", "-i", FINAL, "-frames:v", "1", "-vf", "scale=168:298", phone])
    run(["cp", FINAL, OUT / f"{STEM}_PHONE.mp4"])
    print("wrote", FINAL)


if __name__ == "__main__":
    main()
