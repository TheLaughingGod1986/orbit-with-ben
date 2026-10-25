#!/usr/bin/env python3
"""J0932 c37 measures. loop_diff averages the kept rows only, on frame 0 and the last frame."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import numpy as np

# 270×480 is the same 9:16 mask Chief used (kept rows 105–375 of 480).
W, H = 270, 480
KEEP = (105, 375)


def decode_gray(video: Path) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(video),
        "-vf", f"scale={W}:{H},format=gray",
        "-f", "rawvideo", "-",
    ])
    frame = W * H
    n = len(raw) // frame
    if n < 2:
        raise SystemExit(f"{video.name}: only {n} frames")
    return np.frombuffer(raw[: n * frame], dtype=np.uint8).reshape(n, H, W)


def head_matches(fr: np.ndarray, n_tail: int = 5, head_frames: int = 90) -> list[int]:
    """Best match in the opening for each of the last n_tail frames.

    A reversed tail walks this list downward (10, 8, 5, 3, 0). A forward tail
    that ends one frame before frame 0 does not.
    """
    y0, y1 = KEEP
    head_n = min(head_frames, max(2, fr.shape[0] - n_tail - 1))
    head = fr[:head_n, y0:y1].astype(np.float32)
    out = []
    for i in range(fr.shape[0] - n_tail, fr.shape[0]):
        frame = fr[i, y0:y1].astype(np.float32)
        diffs = np.mean(np.abs(head - frame[None]), axis=(1, 2))
        out.append(int(np.argmin(diffs)))
    return out


def loop_metrics(video: Path) -> dict:
    fr = decode_gray(video)
    a = fr[0].astype(np.float32)
    b = fr[-1].astype(np.float32)
    y0, y1 = KEEP
    whole = float(np.mean(np.abs(a - b)))
    masked = float(np.mean(np.abs(a[y0:y1] - b[y0:y1])))
    centre = fr[:, y0:y1].astype(np.float32)
    steps = np.mean(np.abs(centre[1:] - centre[:-1]), axis=(1, 2))
    cut = next((i for i, s in enumerate(steps[:90]) if s > 28.0), min(45, len(steps)))
    window = steps[: max(8, cut)]
    med = float(np.median(window)) if len(window) else 0.0
    matches = head_matches(fr)
    return {
        "frames": int(fr.shape[0]),
        "whole": whole,
        "loop_diff_masked": masked,
        "open_median_step": med,
        "head_matches": matches,
        "steps": steps,
        "frames_arr": fr,
    }


def finish_scan(video: Path, metrics: dict | None = None) -> dict:
    """Fail a shot under 0.40 s, a ≥3-frame freeze, or an ≥80% black frame after 0.5 s."""
    m = metrics if metrics is not None else loop_metrics(video)
    fr = m["frames_arr"]
    steps = m["steps"]
    fps = 30.0
    for i in range(int(round(0.5 * fps)), fr.shape[0]):
        pct = float((fr[i] < 20).mean() * 100.0)
        if pct >= 80.0:
            raise SystemExit(f"black frame {pct:.0f}% at {i / fps:.2f}s")
    run = 0
    for i, s in enumerate(steps):
        if float(s) < 0.35:
            run += 1
            if run >= 3:
                t = (i - run + 1) / fps
                raise SystemExit(f"freeze of {run} frames at {t:.2f}s (step {float(s):.2f})")
        else:
            run = 0
    spikes = [i for i, s in enumerate(steps) if float(s) > 40.0]
    for a, b in zip(spikes, spikes[1:]):
        # Adjacent spikes are one hard cut (two big steps). A shot under 0.40 s
        # has at least one frame of picture between two cuts.
        if 1 < (b - a) < 12:
            raise SystemExit(f"shot {(b - a) / fps:.3f}s at {a / fps:.2f}s")
    masked = float(m["loop_diff_masked"])
    med = float(m["open_median_step"])
    matches = list(m.get("head_matches") or [])
    if masked > 15.0:
        raise SystemExit(f"loop_diff_masked {masked:.2f} > 15")
    if med > 0.4 and masked > 2.0 * med:
        raise SystemExit(f"loop_diff_masked {masked:.2f} > 2× open step {med:.2f}")
    # (b) the last frame is not a copy of frame 0.
    if med > 0.4 and masked < 0.5 * med:
        raise SystemExit(f"loop tail copies frame 0 ({masked:.2f} < 0.5× open step {med:.2f})")
    # (c) head matches of the last 5 frames must not walk backwards toward frame 0.
    if any(b < a for a, b in zip(matches, matches[1:])):
        raise SystemExit(f"loop tail reverses (head matches {matches})")
    # A one-frame dark flash is two big steps with a darker frame between them.
    for i in range(1, fr.shape[0] - 1):
        if float(steps[i - 1]) > 40.0 and float(steps[i]) > 40.0:
            if float(fr[i].mean()) + 30.0 < float(fr[i - 1].mean()):
                raise SystemExit(f"one-frame flash at {i / fps:.2f}s")
    vdur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
        text=True))
    adur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0", str(video)],
        text=True))
    if abs(vdur - adur) > 0.03:
        raise SystemExit(f"audio {adur:.3f}s vs video {vdur:.3f}s")
    return m


def forward_preroll(src: Path, ss: float, dest: Path, vf: str, seconds: float = 1.0, fps: int = 30) -> None:
    """Play source [ss-seconds, ss) forward. The last frame is one frame before ss.

    vf's t starts at 0 on this clip. The open plate must use the same crop and
    speed with t continued from `seconds`, and its in-point must be ss.
    """
    if ss + 1e-3 < seconds:
        raise SystemExit(f"{src.name}: in-point {ss:.3f}s has no {seconds:.2f}s pre-roll")
    n = int(round(seconds * fps))
    if n < 8:
        raise SystemExit(f"loop too short ({n} frames)")
    start = ss - seconds
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start:.4f}", "-t", f"{seconds:.4f}", "-i", str(src),
        "-vf", f"{vf},trim=end_frame={n},setpts=PTS-STARTPTS",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p", "-r", str(fps), str(dest),
    ], check=True)


def loop_from_open(plate: Path, dest: Path, n: int = 30) -> None:
    """Tail whose last frame is the open plate's second frame, at that plate's crop."""
    if n < 8:
        raise SystemExit(f"loop too short ({n} frames)")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(plate),
        "-vf", f"trim=start_frame=1:end_frame={n + 1},setpts=PTS-STARTPTS,reverse,setpts=PTS-STARTPTS",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p", "-r", "30", str(dest),
    ], check=True)


def limiter(norm_af: str) -> str:
    """Hold true peak at or under −1.0 dBTP. 0.891 is −1.0 dB."""
    return norm_af + ",alimiter=limit=0.891:level=disabled"


def true_peak(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    hits = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    if not hits:
        raise SystemExit(f"no true peak from {path.name}")
    return float(hits[-1])
