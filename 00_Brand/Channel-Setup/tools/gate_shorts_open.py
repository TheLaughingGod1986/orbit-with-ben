#!/usr/bin/env python3
"""Shorts open gate — run on every Short export BEFORE upload (10 Sep 2026 audit fix).

Studio core: identical in orbit-with-ben and history-of-science (edit it in orbit-with-ben only, scripts/core_sync.py).
What differs per channel is in channel_profile.py: the robot-at-frame-0 check (Orbit only; it misfires on HOS's warm
lamp-and-wood frames, so on HOS the Explorer-at-frame-0 rule is checked by eye on the contact sheet) and the
same-background check.

Hard FAILs (STUDIO_PLAYBOOK.md §7 · .cursor/rules/orbit-build-shorts.mdc):

  1. duration ≥ 40 s                                  (existing lock; `--length-test` lifts it to
                                                        ≥ 61 s for the one Chief-OK'd 50–60 s Short
                                                        length test, AGENTS.md, 11 Oct 2026)
  2. first frame (0.3 s) within 10 dHash bits of any   (new — Europa week shipped six
     Short published / scheduled ±14 days of air date   Shorts on one plate; feed saw
                                                        the same video six days running)
  3. Orbit in frame at 0 s (OWB only)                 (new — `TE_HDKAnqms` / `mAAMsbhm88w`
                                                        Orbit-first opens got 0 % feed traffic)
  4. no audio stream, or mean volume below −40 dB      (24 Sep 2026 — four Moon Shorts aired
                                                        with the whole file at about −90 dB)
  5. pushed still at frame 0 (0–1.5 s diff < 1.50)     (24 Oct 2026 — 60% stayed-to-watch gate:
                                                        Mercury vlkj8RQKmH8 opened on a still
                                                        pushed 1.00→1.04 over 5.5 s and got
                                                        32.1 % stayed; calibrated vs mon19 v02)
  6. first cut > 3.0 s (scene-change detect)           (24 Oct 2026 — 60% stayed-to-watch gate)
  7. spoken text contains a meta-promise               (24 Oct 2026 — "stay, and i'll show you",
                                                        "stay and i'll show you", "did you know",
                                                        "wait for it")
  8. integrated loudness outside −14.0 ±0.5 LUFS, or   (26 Oct 2026, Chief c61 — ebur128 peak=true
     true peak above −1.6 dBTP                          on the AAC; loudnorm's −1.5 target was
                                                        landing at −1.4 dBTP)
  9. slow fade-in from black at frame 0, or missing /  (9 Nov 2026, J2429 — first-second rule:
     late on-screen hook text at frame 0 (0.0 s)        KX-XU_AODoI faded from luma 2.2→58.6 and
                                                        got 20.6 % stayed; winners stamp the 2–4
                                                        word hook caption at t=0.0 s on full-bleed
                                                        moving video)
 10. frame 0 not full-bleed 9:16: black bars, a flat   (10 Nov 2026, J2539, LEARNINGS rule 24 — the
     band, or a blurred / mirrored copy as fill, above  Short that aired on 10 Nov opened on a 16:9
     and below a narrower picture band (0.0–0.5 s)      band over blurred fill and passed this gate;
                                                        the Shorts feed barely showed it)

Warnings:

  8. picture barely changes in the first second        (24 Sep 2026 — still globe + caption
                                                        opens held 15–17 % stayed; the moving
                                                        plume open held 46 %)
  9. first VO word starts after 0.15 s                 (24 Oct 2026 — silencedetect on VO/mix)
 10. gap from last word to end > 1.5 s                 (24 Oct 2026 — post-VO tail hold)

Orbit detection is a colour/shape heuristic (matte-orange body + black visor holding
cream eyes). It is calibrated on the 10 Sep frames (Orbit ≥ 0.004 · world ≤ 0.0003) and
it always writes a contact sheet; a human still eyeballs the 0 s frame before upload.

Usage
  python3 gate_shorts_open.py check <short.mp4> --air-date 2026-09-16 [--json]
  python3 gate_shorts_open.py add --id <yt id> --date 2026-09-16 --title "…" (--file <mp4> | --frame <png/jpg>)
  python3 gate_shorts_open.py fetch --id <yt id> --date … --title …     # public Short via yt-dlp
  python3 gate_shorts_open.py list [--days 14] [--air-date …]
  python3 gate_shorts_open.py compare                                     # pairwise table of library

Library: 00_Brand/Channel-Setup/audits/shorts_open_library/library.json (+ frames/<id>.jpg)
Frame-0 lookback (Shorts feed rule R3, Claude ruling 5 Oct 2026): check 2 compares against every
Short within ±14 days of the air date AND the last 10 Shorts aired before it, whichever reaches
further back (`--days`, `--last`).

Exit code 0 = PASS, 1 = FAIL, 2 = tool error.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import channel_profile as channel  # noqa: E402  (this repo's own settings)
ROOT = HERE.parents[2]  # tools → Channel-Setup → 00_Brand → repo root
LIB_DIR = ROOT / "00_Brand/Channel-Setup/audits/shorts_open_library"
LIB_JSON = LIB_DIR / "library.json"
FRAMES = LIB_DIR / "frames"

OPEN_T = 0.3  # seconds — first real frame after any fade-in
LOOKBACK_DAYS = 14
LOOKBACK_LAST = 10  # R3 (5 Oct 2026): never reuse an opening background from the last 10 Shorts
DHASH_FAIL_BITS = 10
DHASH_WARN_BITS = 16
# Background match on a 27x48 grey thumbnail (6 Oct 2026). dHash alone missed dQlOgsDGmtA vs Ih2zhZTbIR0: same Jupiter
# plate, 17 bits apart. Orbit or a caption over the same plate wrecks a global score, so this counts the share of 4x4
# blocks that still match (block SSIM >= BLOCK_SSIM, best of a ±BLOCK_SHIFT px nudge for a slow push-in): overlays only
# knock out the blocks they cover. Scored both ways and averaged. Calibrated 6 Oct on the library (`compare --ssim`,
# 29 thumbs, 351 pairs, Chief b62a3b4): same plate 0.56-1.00 (Jupiter pair 0.56, Europa crops 0.57+), different
# plates 0.18 or less. The first cut (3x3, SSIM >= 0.90, no nudge) scored the Jupiter pair 0.19, below an honest pair.
THUMB_W, THUMB_H = 27, 48
BLOCK = 4
BLOCK_SHIFT = 1
BLOCK_SSIM = 0.70
BG_FAIL = 0.40
BG_WARN = 0.30
FLAT_VAR = 25.0      # a block this flat in both frames (black space, sky) proves nothing, so it isn't counted
MIN_TEXTURED = 12    # fewer textured blocks than this: no verdict (dHash still applies)
DUR_FAIL = 40.0
DUR_BAND = (22.0, 27.0)
# One-off Short length test (Chief OK, 11 Oct 2026, AGENTS.md "Short length test"). Only with --length-test.
TEST_DUR_FAIL = 61.0
TEST_DUR_BAND = (50.0, 60.0)
VISOR_FAIL = 0.003
VISOR_WARN = 0.001
SHEET_TIMES = (0.0, 0.3, 1.0, 2.0, 3.0, 4.0)
# Voiced Orbit Shorts measure about −19 to −28 dB mean; the silent Moon uploads were about −90.
AUDIO_FAIL_DB = -40.0
OPEN_AUDIO_S = 1.5  # the hook line must be audible inside this window
OPEN_AUDIO_WARN_DB = -45.0
# Motion in the first second: mean absolute grey-level change (0–100 scale) summed over
# 0.25 s steps from 0.0 to 1.0 s. Set 24 Sep 2026 on synthetic 9:16 clips cut from the
# Europa long thumbnail: still 0.0 · still + changing caption 0.3 · Ken Burns 1.5 %/s 3.2 ·
# Ken Burns 4.5 %/s 8.3 · fast push-in 44 · handheld shake 39. A zoom on a still image
# warns; a real move clears it easily. Warn only until real exports are measured.
MOTION_TIMES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOTION_WARN = 10.0
# 60% stayed-to-watch ship gate (Chief, 24 Oct 2026, J0918):
# (a) FAIL "pushed still at frame 0" when 0-1.5 s mean frame diff in the central picture band is < FRAME0_DIFF_FAIL.
#     Calibrated on S1-S8 v01 standalone exports (0.13-1.07 -> FAIL) vs mon19_brighter_fuel_short_v02 (2.22 -> PASS).
FRAME0_DIFF_TIMES = (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5)
FRAME0_DIFF_FAIL = 1.50
# (b) FAIL when the first cut comes after 3.0 s (scene-change detect on the picture band).
FIRST_CUT_MAX_S = 3.0
SCDET_THRESHOLD = 10.0
SCDET_SCAN_S = 10.0
# (c) WARN when the first VO word starts after 0.15 s (silencedetect on the VO stem or mix).
VO_ONSET_WARN_S = 0.15
# (d) WARN when the gap from the last word to the end is over 1.5 s.
VO_TAIL_WARN_S = 1.5
# (e) Text lint: FAIL if the script or meta "spoken" field contains a meta-promise.
# (f) Level (Chief c61, 26 Oct 2026): ebur128 peak=true on the AAC. Integrated −14.0 ±0.5 LUFS,
#     true peak ≤ −1.6 dBTP. The old loudnorm TP=−1.5 target was measuring about −1.4 on the file.
LUFS_TARGET = -14.0
LUFS_TOL = 0.5
TP_FAIL_DBTP = -1.6
META_PROMISES = (
    "stay, and i'll show you",
    "stay and i'll show you",
    "did you know",
    "wait for it",
)
# First-second gate (9 Nov 2026, J2429):
# (g) FAIL when frame 0 (0.0 s) fades in from black/dark (e.g. KX-XU_AODoI luma 2.2 at 0.0 s -> 58.6 at 0.5 s, 20.6% stayed).
FRAME0_FADE_LUMA_MAX = 12.0
FRAME0_FADE_MIN_TARGET_LUMA = 20.0
FRAME0_FADE_RATIO_FAIL = 2.25
# (h) FAIL when on-screen hook caption is missing or starts after 0.05 s at frame 0 (calibrated on OWB frame-0 captures:
#     captioned frame 0 scores 0.0231..0.0715 in the 0.08..0.48 H hook band; uncaptioned plate scores 0.0000).
FRAME0_HOOK_EDGE_MIN = 0.005
FRAME0_HOOK_MAX_START_S = 0.05
FRAME0_HOOK_MIN_DIMS = (540, 960)
# Frame-0 full-bleed (10 Nov 2026, J2539, LEARNINGS rule 24): the Short that aired on 10 Nov opened on a 16:9 picture
# band with blurred fill above and below, passed this gate on 9 Nov, and the Shorts feed barely showed it.
# (i) FAIL when the opening picture does not fill the 9:16 frame. Grey FB_W x FB_H frames at FB_TIMES. A frame is
#     padded when it has a pair of straight, full-width horizontal seams, one above and one below the centre and the
#     same distance from it (fill is always centred), and outside them the frame is one of:
#       "bars"     flat (pixel spread <= FB_FLAT_STD) while the band between is not: black bars or a flat colour band;
#       "blur-pad" far softer than the band between (row detail < FB_SOFT_RATIO of it): a blurred copy as fill;
#       "mirror"   the picture's own rows reflected outward from each seam.
#     A seam is a brightness step across FB_SEAM_COLS of the width, or a jump in row detail (soft outside, sharp
#     inside). Row detail = mean absolute left-right difference along a row, so the seam itself adds nothing to it.
#     A caption strip or hook text over a full-frame picture has real picture outside it, so it is none of the three.
#     A planet on black space has no straight full-width seam. Thresholds are first-pass, set on made clips only:
#     read the numbers J2540 tables for real exports before tightening.
FB_W, FB_H = 108, 192
FB_TIMES = (0.0, 0.25, 0.5)
FB_SEAM_RANGE = (0.08, 0.42)   # upper seam row as a share of the height; the lower one mirrors it
FB_SEAM_DIFF = 12              # grey levels across the seam (rows y-2 and y+1, so a 1-row soft edge still counts)
FB_SEAM_COLS = 0.70
FB_SEGS = 4                    # column segments for the row-detail jump
FB_SEG_NEED = 3
FB_SEAM_SYM_ROWS = 3          # the two seams sit within this many rows of the same distance from the centre
FB_SOFT_RATIO = 0.35
FB_DETAIL_FLOOR = 1.5          # the sharp side must carry real detail, or the frame proves nothing (dark space)
FB_FLAT_STD = 3.0
FB_PICTURE_STD = 12.0
FB_MIRROR_ROWS = 8
FB_MIRROR_DIFF = 4.0
FB_MIRROR_VERT = 8.0           # the picture must change this much over FB_MIRROR_ROWS rows for a mirror to count


# ----------------------------------------------------------------------------- ffmpeg
def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def duration_s(path: Path) -> float:
    out = run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    ).stdout.decode().strip()
    return float(out)


def is_video(path: Path) -> bool:
    return path.suffix.lower() in {".mp4", ".mov", ".m4v", ".webm", ".mkv"}


def raw_frame(path: Path, w: int, h: int, t: float | None, pix: str) -> bytes:
    cmd = ["ffmpeg", "-v", "error"]
    if t is not None and is_video(path):
        cmd += ["-ss", f"{t:.3f}"]
    cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", pix, "-"]
    data = run(cmd).stdout
    need = w * h * (1 if pix == "gray" else 3)
    if len(data) < need:
        raise RuntimeError(f"short frame from {path} ({len(data)} < {need})")
    return data[:need]


def save_frame(path: Path, t: float | None, out: Path, w: int = 270) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if t is not None and is_video(path):
        cmd += ["-ss", f"{t:.3f}"]
    cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:-2", "-q:v", "4", str(out)]
    run(cmd)


# ----------------------------------------------------------------------------- hashes
def dhash(path: Path, t: float | None = OPEN_T) -> int:
    g = raw_frame(path, 9, 8, t, "gray")
    bits = 0
    for y in range(8):
        for x in range(8):
            bits = (bits << 1) | (1 if g[y * 9 + x] > g[y * 9 + x + 1] else 0)
    return bits


def thumb(path: Path, t: float | None = OPEN_T) -> str:
    """Frame 0 as an 27x48 grey thumbnail, hex-encoded, for the background SSIM check."""
    return raw_frame(path, THUMB_W, THUMB_H, t, "gray").hex()


def ssim(x: list[int] | bytes, y: list[int] | bytes) -> float:
    """SSIM of two equal-length grey pixel runs. 1.0 = identical."""
    n = min(len(x), len(y))
    if n == 0:
        return 0.0
    mx, my = sum(x[:n]) / n, sum(y[:n]) / n
    vx = sum((v - mx) ** 2 for v in x[:n]) / n
    vy = sum((v - my) ** 2 for v in y[:n]) / n
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(n)) / n
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    return ((2 * mx * my + c1) * (2 * cov + c2)) / ((mx * mx + my * my + c1) * (vx + vy + c2))


def background_match(a: str | bytes, b: str | bytes) -> float:
    """Share of BLOCKxBLOCK blocks that match between two thumbnails (hex or bytes), averaged over both directions.
    An overlay (Orbit, a caption) only removes the blocks it covers, so the same plate under different overlays
    still scores high."""
    x = bytes.fromhex(a) if isinstance(a, str) else a
    y = bytes.fromhex(b) if isinstance(b, str) else b
    if len(x) != THUMB_W * THUMB_H or len(y) != THUMB_W * THUMB_H:
        return 0.0
    return (_block_share(x, y) + _block_share(y, x)) / 2


def _block_share(x: bytes, y: bytes) -> float:
    def var(v):
        m = sum(v) / len(v)
        return sum((p - m) ** 2 for p in v) / len(v)

    def block(img, by, bx):
        return [img[(by + j) * THUMB_W + bx + i] for j in range(BLOCK) for i in range(BLOCK)]

    hits = total = 0
    for by in range(0, THUMB_H - BLOCK + 1, BLOCK):
        for bx in range(0, THUMB_W - BLOCK + 1, BLOCK):
            bx_ = block(x, by, bx)
            if var(bx_) < FLAT_VAR and var(block(y, by, bx)) < FLAT_VAR:
                continue
            total += 1
            best = max(
                ssim(bx_, block(y, by + dy, bx + dx))
                for dy in range(-BLOCK_SHIFT, BLOCK_SHIFT + 1)
                for dx in range(-BLOCK_SHIFT, BLOCK_SHIFT + 1)
                if 0 <= by + dy <= THUMB_H - BLOCK and 0 <= bx + dx <= THUMB_W - BLOCK
            )
            hits += best >= BLOCK_SSIM
    return hits / total if total >= MIN_TEXTURED else 0.0


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def orbit_score(path: Path, t: float | None = OPEN_T) -> dict:
    """Orange body + black visor holding cream eyes → 'visor' fraction."""
    W, H = 72, 128
    d = raw_frame(path, W, H, t, "rgb24")
    cls = bytearray(W * H)
    o = k = 0
    for i in range(W * H):
        r, g, b = d[3 * i], d[3 * i + 1], d[3 * i + 2]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h *= 360
        if 12 <= h <= 42 and s >= 0.5 and v >= 0.45:
            cls[i] = 1  # orange
            o += 1
        elif v < 0.18:
            cls[i] = 2  # dark (visor / space)
            k += 1
        elif v > 0.75 and s < 0.35:
            cls[i] = 3  # cream / white (eyes / stars)
    R = 4
    vis = 0
    for y in range(H):
        for x in range(W):
            if cls[y * W + x] != 2:
                continue
            has_o = has_w = False
            for dy in range(-R, R + 1):
                yy = y + dy
                if not 0 <= yy < H:
                    continue
                row = yy * W
                for dx in range(-R, R + 1):
                    xx = x + dx
                    if not 0 <= xx < W:
                        continue
                    c = cls[row + xx]
                    if c == 1:
                        has_o = True
                    elif c == 3:
                        has_w = True
                if has_o and has_w:
                    break
            if has_o and has_w:
                vis += 1
    n = W * H
    return {"orange_frac": round(o / n, 4), "dark_frac": round(k / n, 4), "visor_frac": round(vis / n, 4)}


def motion_first_second(path: Path) -> float:
    """How much the picture changes between 0 and 1 s (a still or slow drift reads near 0)."""
    W, H = 72, 128
    frames = [raw_frame(path, W, H, t, "gray") for t in MOTION_TIMES]
    total = 0.0
    for a, b in zip(frames, frames[1:]):
        total += sum(abs(x - y) for x, y in zip(a, b)) / (W * H) / 255 * 100
    return round(total, 2)


def frame0_diff_0_1_5s(path: Path, dur: float | None = None) -> float:
    """Sustained mean frame difference across 0–1.5 s in the central picture band (0.28..0.72 H, clear of hook and
    lower-third captions). Uses the minimum 0.5 s window mean inside 0–1.5 s so a 1 s ease-out kick that stalls into a
    pushed still by 1.0–1.5 s (like S1–S8 v01, 0.13–1.07) fails while real moving footage (mon19 v02, 2.22) passes."""
    W, H = 72, 128
    y0, y1 = int(H * 0.28), int(H * 0.72)
    bh = y1 - y0
    if dur is None:
        dur = duration_s(path)
    times = [t for t in FRAME0_DIFF_TIMES if t <= max(0.0, dur - 0.05)]
    if len(times) < 2:
        return 0.0
    frames = [raw_frame(path, W, H, t, "gray")[y0 * W:y1 * W] for t in times]
    steps = [sum(abs(x - y) for x, y in zip(a, b)) / (W * bh) / 255 * 100 for a, b in zip(frames, frames[1:])]
    if len(steps) >= 2:
        val = min((steps[i] + steps[i + 1]) / 2 for i in range(len(steps) - 1))
    else:
        val = steps[0]
    return round(val, 2)


def first_cut_s(path: Path, dur: float | None = None, scan_s: float = SCDET_SCAN_S) -> float | None:
    """First scene cut in the central picture band via ffmpeg scdet, or None if no cut occurs in the scan window."""
    if dur is None:
        dur = duration_s(path)
    limit = min(dur, scan_s)
    cmd = [
        "ffmpeg", "-v", "info", "-nostats", "-t", f"{limit:.3f}", "-i", str(path),
        "-vf", f"crop=iw:ih*0.44:0:ih*0.28,scale=72:56:flags=area,scdet=threshold={SCDET_THRESHOLD}:sc_pass=1",
        "-an", "-f", "null", "-",
    ]
    err = run(cmd).stderr.decode(errors="replace")
    cuts = [float(m.group(1)) for m in re.finditer(r"lavfi\.scd\.time:\s*([0-9.]+)", err) if float(m.group(1)) > 0.10]
    return round(cuts[0], 2) if cuts else None


def first_cut_verdict(cut_s: float | None, dur: float) -> list[str]:
    """(b) FAIL when the first cut comes after 3.0 s."""
    if dur <= FIRST_CUT_MAX_S:
        return []
    if cut_s is None:
        return [f"first cut > {FIRST_CUT_MAX_S:.1f}s (no scene change in first {min(dur, SCDET_SCAN_S):.1f}s)"]
    if cut_s > FIRST_CUT_MAX_S:
        return [f"first cut at {cut_s:.2f}s > {FIRST_CUT_MAX_S:.1f}s (scene-change detect)"]
    return []


def meta_promise_verdict(text: str) -> list[str]:
    """(e) FAIL if spoken text contains a meta-promise."""
    if not text:
        return []
    norm = re.sub(r"\s+", " ", text.lower().replace("\u2019", "'").replace("\u2018", "'").replace("`", "'"))
    for phrase in META_PROMISES:
        if phrase in norm:
            return [f"spoken text contains meta-promise ({phrase!r})"]
    return []


def video_dims(path: Path) -> tuple[int, int]:
    """Return (width, height) of the primary video stream, or (0, 0) if unreadable."""
    try:
        out = run([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path),
        ]).stdout.decode().strip().splitlines()
        if out and "x" in out[0]:
            w, h = out[0].split("x", 1)
            return int(w), int(h)
    except Exception:
        pass
    return 0, 0


def frame0_luma_and_kick(path: Path, dur: float | None = None) -> tuple[float, float, float]:
    """Return (luma_0s, luma_0_5s, kick_0_0_5s) across 0.0–0.5 s for slow fade-in and immediate-kick checks."""
    W, H = 72, 128
    if dur is None:
        dur = duration_s(path)
    f0 = raw_frame(path, W, H, 0.0, "gray")
    t05 = min(0.5, max(0.0, dur - 0.05))
    f05 = raw_frame(path, W, H, t05, "gray") if t05 > 0.0 else f0
    l0 = round(sum(f0) / (W * H), 2)
    l05 = round(sum(f05) / (W * H), 2)
    y0, y1 = int(H * 0.28), int(H * 0.72)
    bh = y1 - y0
    t025 = min(0.25, max(0.0, dur - 0.05))
    f025 = raw_frame(path, W, H, t025, "gray") if t025 > 0.0 else f0
    b0, b025, b05 = f0[y0 * W:y1 * W], f025[y0 * W:y1 * W], f05[y0 * W:y1 * W]
    s1 = sum(abs(x - y) for x, y in zip(b0, b025)) / (W * bh) / 255 * 100
    s2 = sum(abs(x - y) for x, y in zip(b025, b05)) / (W * bh) / 255 * 100
    kick = round((s1 + s2) / 2, 2)
    return l0, l05, kick


def frame0_fade_in_verdict(luma_0s: float, luma_0_5s: float) -> list[str]:
    """(g) FAIL when frame 0 fades in from black/dark (e.g. KX-XU_AODoI luma 2.2 -> 58.6, 20.6% stayed)."""
    ratio = luma_0_5s / max(luma_0s, 1.0)
    if luma_0s <= FRAME0_FADE_LUMA_MAX and luma_0_5s >= FRAME0_FADE_MIN_TARGET_LUMA and ratio >= FRAME0_FADE_RATIO_FAIL:
        return [
            f"slow fade-in from black at frame 0 (luma {luma_0s:.1f} at 0.0s → {luma_0_5s:.1f} at 0.5s) — "
            "start at full brightness"
        ]
    return []


def frame0_hook_text_score(path: Path, t: float | None = 0.0) -> float:
    """Share of pixels in the upper-middle hook band (0.08..0.48 H, 0.08..0.92 W) that match high-contrast
    stroked white or #FFE000 yellow hook caption glyphs at frame 0 (t=0.0 s)."""
    W, H = 108, 192
    d = raw_frame(path, W, H, t, "rgb24")
    y0, y1 = int(H * 0.08), int(H * 0.48)
    x0, x1 = int(W * 0.08), int(W * 0.92)
    hits = 0
    total = max(1, (y1 - y0) * (x1 - x0))
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = (y * W + x) * 3
            r, g, b = d[i], d[i + 1], d[i + 2]
            bright = (r >= 200 and g >= 200 and b >= 200) or (r >= 210 and g >= 175 and b <= 100)
            if not bright:
                continue
            dark_nb = False
            for dy in (-2, -1, 0, 1, 2):
                yy = y + dy
                if not 0 <= yy < H:
                    continue
                for dx in (-2, -1, 0, 1, 2):
                    xx = x + dx
                    if not 0 <= xx < W:
                        continue
                    j = (yy * W + xx) * 3
                    if d[j] <= 65 and d[j + 1] <= 65 and d[j + 2] <= 65:
                        dark_nb = True
                        break
                if dark_nb:
                    break
            if dark_nb:
                hits += 1
    return round(hits / total, 4)


def frame0_hook_text_verdict(hook_edge_0s: float, meta: dict, dims: tuple[int, int] = (1080, 1920)) -> list[str]:
    """(h) FAIL when on-screen hook text is missing or starts after 0.05 s at frame 0."""
    has_meta_key = any(k in meta for k in ("hook_caption", "hook_text", "on_screen_hook"))
    if has_meta_key:
        raw = next((meta[k] for k in ("hook_caption", "hook_text", "on_screen_hook") if k in meta), None)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            return ["missing on-screen hook text at frame 0 (meta hook_caption/hook_text is empty) — stamp 2–4 word hook at 0.0s"]
        if isinstance(raw, dict):
            txt = str(raw.get("text") or raw.get("caption") or "").strip()
            start = raw.get("start_s", raw.get("start", raw.get("t_start", 0.0)))
            if not txt:
                return ["missing on-screen hook text at frame 0 (meta hook text is empty) — stamp 2–4 word hook at 0.0s"]
            if isinstance(start, (int, float)) and float(start) > FRAME0_HOOK_MAX_START_S:
                return [
                    f"late on-screen hook text at frame 0 (starts at {float(start):.2f}s > {FRAME0_HOOK_MAX_START_S:.2f}s) — "
                    "stamp 2–4 word hook at 0.0s"
                ]
    w, h = dims
    enforce_pixels = has_meta_key or (w >= FRAME0_HOOK_MIN_DIMS[0] and h >= FRAME0_HOOK_MIN_DIMS[1])
    if enforce_pixels and hook_edge_0s < FRAME0_HOOK_EDGE_MIN:
        return [
            f"missing on-screen hook text at frame 0 (hook_edge {hook_edge_0s:.4f} < {FRAME0_HOOK_EDGE_MIN:.3f}) — "
            "stamp 2–4 word hook caption at 0.0s"
        ]
    return []


# ----------------------------------------------------------------------------- frame-0 full-bleed (J2539)
def _fb_row_stats(g: bytes) -> tuple[list[float], list[list[float]]]:
    """Per row of an FB_W x FB_H grey frame: (detail, detail in each of FB_SEGS equal column segments).
    Detail = mean absolute left-right difference."""
    W = FB_W
    seg_w = W // FB_SEGS
    det, segs = [], []
    for y in range(FB_H):
        row = g[y * W:(y + 1) * W]
        d = [abs(row[x + 1] - row[x]) for x in range(W - 1)]
        det.append(sum(d) / (W - 1))
        segs.append([sum(d[s * seg_w:(s + 1) * seg_w - 1]) / (seg_w - 1) for s in range(FB_SEGS)])
    return det, segs


def _fb_std(g: bytes, y0: int, y1: int) -> float:
    v = g[max(0, y0) * FB_W:max(0, y1) * FB_W]
    if not v:
        return 0.0
    m = sum(v) / len(v)
    return (sum((p - m) ** 2 for p in v) / len(v)) ** 0.5


def _fb_avg(vals: list[float], y0: int, y1: int) -> float:
    v = vals[max(0, y0):max(0, y1)]
    return sum(v) / len(v) if v else 0.0


def _fb_step_share(g: bytes, y: int) -> float:
    """Share of columns with a brightness step of FB_SEAM_DIFF or more between rows y-2 and y+1."""
    if y < 2 or y + 1 >= FB_H:
        return 0.0
    a, b = (y - 2) * FB_W, (y + 1) * FB_W
    return sum(1 for x in range(FB_W) if abs(g[a + x] - g[b + x]) >= FB_SEAM_DIFF) / FB_W


def _fb_seam(g: bytes, det: list[float], segs: list[list[float]], y: int, upper: bool) -> tuple[bool, float, float]:
    """Is there a straight seam at row y (the first picture row for the upper seam, the first fill row for the
    lower one)? Returns (seam, brightness-step share, outside/inside row-detail ratio). The detail jump must show in
    FB_SEG_NEED of the FB_SEGS column segments, on every one of the three rows each side, so the curved edge of a
    planet on black space is not a seam."""
    share = _fb_step_share(g, y)
    out_rows = range(y - 4, y - 1) if upper else range(y + 1, y + 4)
    in_rows = range(y + 1, y + 4) if upper else range(y - 4, y - 1)
    if min(out_rows) < 0 or max(out_rows) >= FB_H or min(in_rows) < 0 or max(in_rows) >= FB_H:
        return share >= FB_SEAM_COLS, round(share, 3), 1.0
    outside = sum(det[r] for r in out_rows) / 3
    inside = sum(det[r] for r in in_rows) / 3
    ratio = outside / inside if inside > 0 else 1.0
    jumps = 0
    for s in range(FB_SEGS):
        sharp = min(segs[r][s] for r in in_rows)
        soft = max(segs[r][s] for r in out_rows)
        if sharp >= FB_DETAIL_FLOOR and soft <= FB_SOFT_RATIO * sharp:
            jumps += 1
    seam = share >= FB_SEAM_COLS or jumps >= FB_SEG_NEED
    return seam, round(share, 3), round(ratio, 3)


def _fb_mirror_diff(g: bytes, y: int) -> tuple[float, float]:
    """(mirror difference, vertical change) at row y. Mirror difference = mean absolute difference of the
    FB_MIRROR_ROWS rows above row y against the rows from y down, reflected. Vertical change = the same measure
    between row y and the row FB_MIRROR_ROWS - 1 below it. A small mirror difference only means a mirrored frame
    when the picture really changes from row to row (a soft or flat picture matches itself any way up)."""
    W = FB_W
    if y - FB_MIRROR_ROWS < 0 or y + FB_MIRROR_ROWS > FB_H:
        return 255.0, 0.0
    tot = 0
    for k in range(FB_MIRROR_ROWS):
        a, b = (y - 1 - k) * W, (y + k) * W
        tot += sum(abs(g[a + x] - g[b + x]) for x in range(W))
    a, b = y * W, (y + FB_MIRROR_ROWS - 1) * W
    vert = sum(abs(g[a + x] - g[b + x]) for x in range(W)) / W
    return tot / (FB_MIRROR_ROWS * W), vert


def full_bleed_frame(g: bytes) -> dict:
    """Measure one FB_W x FB_H grey frame. 'kind' is None (the picture fills the frame), 'bars', 'blur-pad' or
    'mirror'. The other keys are the numbers behind it, for the gate's report."""
    H = FB_H
    det, segs = _fb_row_stats(g)
    fifth = H // 5
    c0, c1 = int(H * 0.38), int(H * 0.62)
    out: dict = {
        "kind": None,
        "detail_top": round(_fb_avg(det, 0, fifth), 2),
        "detail_centre": round(_fb_avg(det, c0, c1), 2),
        "detail_bottom": round(_fb_avg(det, H - fifth, H), 2),
        "std_top": round(_fb_std(g, 0, fifth), 2),
        "std_bottom": round(_fb_std(g, H - fifth, H), 2),
        "seam_rows": None,
    }
    lo, hi = int(H * FB_SEAM_RANGE[0]), int(H * FB_SEAM_RANGE[1])
    for u in range(lo, hi + 1):
        # mirrored fill has no brightness step at the seam, so it is looked for on its own
        for low in range(H - u - FB_SEAM_SYM_ROWS, H - u + FB_SEAM_SYM_ROWS + 1):
            md_u, mv_u = _fb_mirror_diff(g, u)
            md_l, mv_l = _fb_mirror_diff(g, low)
            if max(md_u, md_l) <= FB_MIRROR_DIFF and min(mv_u, mv_l) >= FB_MIRROR_VERT:
                out.update(kind="mirror", seam_rows=[u, low], mirror_diff=[round(md_u, 2), round(md_l, 2)])
                return out
        up_ok, up_share, up_ratio = _fb_seam(g, det, segs, u, True)
        if not up_ok:
            continue
        for low in range(H - u - FB_SEAM_SYM_ROWS, H - u + FB_SEAM_SYM_ROWS + 1):
            low_ok, low_share, low_ratio = _fb_seam(g, det, segs, low, False)
            if not low_ok:
                continue
            std_out = max(_fb_std(g, 0, u - 2), _fb_std(g, low + 2, H))
            std_pic = _fb_std(g, u + 1, low - 1)
            det_out = max(_fb_avg(det, 0, u - 2), _fb_avg(det, low + 2, H))
            det_pic = _fb_avg(det, u + 1, low - 1)
            kind = None
            if std_out <= FB_FLAT_STD and std_pic >= FB_PICTURE_STD:
                kind = "bars"
            elif det_pic >= FB_DETAIL_FLOOR and det_out < FB_SOFT_RATIO * det_pic:
                kind = "blur-pad"
            if kind:
                out.update(
                    kind=kind, seam_rows=[u, low], seam_step_share=[up_share, low_share],
                    seam_detail_ratio=[up_ratio, low_ratio],
                    picture_share_of_height=round((low - u) / H, 3),
                    std_outside=round(std_out, 2), std_picture=round(std_pic, 2),
                    detail_outside=round(det_out, 2), detail_picture=round(det_pic, 2),
                )
                return out
    return out


def frame0_full_bleed(path: Path, dur: float | None = None) -> list[dict]:
    """full_bleed_frame() for the frames at FB_TIMES (0.0 to 0.5 s), each with its time 't'."""
    if dur is None:
        dur = duration_s(path)
    out = []
    for t in FB_TIMES:
        tt = min(t, max(0.0, dur - 0.05))
        m = full_bleed_frame(raw_frame(path, FB_W, FB_H, tt, "gray"))
        m["t"] = t
        out.append(m)
    return out


def frame0_full_bleed_verdict(frames: list[dict]) -> list[str]:
    """(i) FAIL when the frame at 0.0 s, or most of the frames to 0.5 s, show a picture band with fill above and below."""
    bad = [f for f in frames if f.get("kind")]
    if not bad:
        return []
    if not (frames[0].get("kind") or len(bad) * 2 > len(frames)):
        return []
    f = bad[0]
    kinds = " / ".join(sorted({b["kind"] for b in bad}))
    if f["kind"] == "bars":
        nums = f"spread outside {f['std_outside']} vs picture {f['std_picture']}"
    elif f["kind"] == "blur-pad":
        nums = f"row detail outside {f['detail_outside']} vs picture {f['detail_picture']}"
    else:
        nums = f"mirror difference {f['mirror_diff'][0]} / {f['mirror_diff'][1]}"
    u, low = f["seam_rows"]
    return [
        f"frame 0 is not full-bleed 9:16: {kinds} above and below a picture band on {len(bad)}/{len(frames)} frames "
        f"from 0.0 to 0.5 s (band from {u / FB_H:.0%} to {low / FB_H:.0%} of the height at {f['t']:.2f}s, {nums}) — "
        "reframe the opening shot to fill 1080x1920"
    ]


# ----------------------------------------------------------------------------- library
def load_lib() -> dict:
    if LIB_JSON.exists():
        return json.loads(LIB_JSON.read_text())
    return {"about": f"first-frame dHash of every {channel.NAME} Short (live + scheduled) — gate_shorts_open.py", "entries": []}


def save_lib(lib: dict) -> None:
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    lib["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    lib["entries"].sort(key=lambda e: (e["date"], e["id"]))
    LIB_JSON.write_text(json.dumps(lib, indent=2, ensure_ascii=False) + "\n")


def upsert(lib: dict, entry: dict) -> None:
    lib["entries"] = [e for e in lib["entries"] if e["id"] != entry["id"]]
    lib["entries"].append(entry)


def window(lib: dict, air: date, days: int, last: int = 0, exclude: str | None = None) -> list[dict]:
    """Entries within ±days of air, plus the `last` most recent entries aired before it (R3)."""
    lo, hi = air - timedelta(days=days), air + timedelta(days=days)
    live = [e for e in lib["entries"] if e.get("status", "live") != "retired" and e["id"] != exclude]
    out = [e for e in live if lo <= date.fromisoformat(e["date"]) <= hi]
    if last > 0:
        before = sorted((e for e in live if date.fromisoformat(e["date"]) < air), key=lambda e: (e["date"], e["id"]))
        seen = {e["id"] for e in out}
        out += [e for e in before[-last:] if e["id"] not in seen]
    return out


def add_entry(lib: dict, vid: str, d: str, title: str, src: Path, source: str, t: float | None, status: str = "live") -> dict:
    h = dhash(src, t)
    sc = orbit_score(src, t) if channel.ROBOT_FRAME0_CHECK else None
    frame = FRAMES / f"{vid}.jpg"
    save_frame(src, t, frame)
    entry = {
        "id": vid,
        "date": d,
        "title": title,
        "dhash": f"{h:016x}",
        "thumb": thumb(src, t),
        **({"orbit": sc} if sc else {}),
        "source": source,
        "frame": str(frame.relative_to(ROOT)),
        "status": status,
        "added_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    upsert(lib, entry)
    return entry


# ----------------------------------------------------------------------------- audio
def has_audio(path: Path) -> bool:
    out = run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)]
    ).stdout.decode().strip()
    return bool(out)


def mean_volume_db(path: Path, start: float = 0.0, length: float | None = None) -> float:
    cmd = ["ffmpeg", "-v", "info", "-nostats", "-ss", f"{start:.3f}"]
    if length is not None:
        cmd += ["-t", f"{length:.3f}"]
    cmd += ["-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"]
    err = run(cmd).stderr.decode(errors="replace")
    for line in err.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0])
    return -91.0  # volumedetect prints nothing for pure digital silence on some builds


def silence_intervals(audio_path: Path, noise_db: float = -35.0, min_dur: float = 0.02) -> list[tuple[float, float]]:
    """Silence intervals (start_s, end_s) via ffmpeg silencedetect."""
    dur = duration_s(audio_path)
    cmd = [
        "ffmpeg", "-v", "info", "-nostats", "-i", str(audio_path), "-vn",
        "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-",
    ]
    err = run(cmd).stderr.decode(errors="replace")
    starts: list[float] = []
    out: list[tuple[float, float]] = []
    for line in err.splitlines():
        ms = re.search(r"silence_start:\s*(-?[0-9.]+)", line)
        if ms:
            starts.append(max(0.0, float(ms.group(1))))
        me = re.search(r"silence_end:\s*([0-9.]+)", line)
        if me and starts:
            out.append((starts.pop(0), float(me.group(1))))
    if starts:
        out.append((starts[0], dur))
    return out


def _export_stem_prefix(path: Path) -> str:
    """Export stem with trailing version suffix (_vNN[a-z]) stripped."""
    stripped = re.sub(r"_v\d+[a-z]?$", "", path.stem, flags=re.IGNORECASE)
    return stripped or path.stem


def _export_stem_prefixes(path: Path) -> tuple[str, ...]:
    """Candidate scoped prefixes for this export (full stem, version-stripped stem, and slug without trailing _short)."""
    base = _export_stem_prefix(path)
    out = [base.lower(), path.stem.lower()]
    no_short = re.sub(r"_short$", "", base, flags=re.IGNORECASE)
    if no_short != base and len(no_short) >= 4 and not no_short.isdigit():
        out.append(no_short.lower())
    return tuple(dict.fromkeys(p for p in out if p))


def _is_scoped_to_export(cand: Path, path: Path) -> bool:
    """True when cand's filename starts with this export's stem (version suffix stripped)."""
    cname = cand.name.lower()
    for prefix in _export_stem_prefixes(path):
        if cname.startswith(prefix) and (len(cname) == len(prefix) or not cname[len(prefix)].isalnum()):
            return True
    return False


def load_sidecar_meta(path: Path, meta_path: Path | None = None) -> dict:
    """Load <stem>_meta.json beside the Short export if present (or explicit --meta)."""
    if meta_path:
        candidates = [meta_path]
    else:
        prefix = _export_stem_prefix(path)
        candidates = [
            path.with_name(f"{path.stem}_meta.json"),
            path.with_name(f"{prefix}_meta.json"),
            path.parent.parent / f"{path.stem}_meta.json",
            path.parent.parent / f"{prefix}_meta.json",
        ]
    for p in candidates:
        if p and p.is_file():
            try:
                data = json.loads(p.read_text())
                if isinstance(data, dict):
                    return data
            except ValueError:
                pass
    return {}


def _resolve_candidate(raw: object, path: Path) -> Path | None:
    if isinstance(raw, dict):
        raw = raw.get("file") or raw.get("path") or raw.get("vo")
    if not isinstance(raw, str) or not raw:
        return None
    for cand in (Path(raw), ROOT / raw, path.parent / raw, path.parent.parent / raw):
        if cand.is_file():
            return cand
    return None


def find_vo_stem(path: Path, meta: dict, vo_path: Path | None = None) -> Path | None:
    """Locate the isolated VO stem scoped to this export if available on disk; returns None to fall back to the mix."""
    if vo_path and vo_path.is_file():
        return vo_path
    audio_meta = meta.get("audio")
    stems = audio_meta.get("stems") if isinstance(audio_meta, dict) else None
    vo_from_stems = stems.get("vo") if isinstance(stems, dict) else None
    for raw in (vo_from_stems, meta.get("vo")):
        p = _resolve_candidate(raw, path)
        if p is not None:
            return p
    for base in (path.parent, path.parent.parent):
        for pat in ("*_vo*.wav", "*_vo*.mp3"):
            for cand in sorted(base.glob(pat)):
                if cand.is_file() and "_raw" not in cand.name and _is_scoped_to_export(cand, path):
                    return cand
    return None


def _words_for(path: Path, meta: dict) -> list[dict]:
    caps = meta.get("captions")
    if isinstance(caps, list) and caps and isinstance(caps[0], dict):
        return caps
    for raw in (meta.get("words_file"), meta.get("words_path")):
        p = _resolve_candidate(raw, path)
        if p is not None:
            try:
                data = json.loads(p.read_text())
                words = data.get("words", data) if isinstance(data, dict) else data
                if isinstance(words, list) and words:
                    return words
            except ValueError:
                pass
    for base in (path.parent, path.parent.parent):
        for cand in sorted(base.glob("*_words.json")):
            if cand.is_file() and _is_scoped_to_export(cand, path):
                try:
                    raw = json.loads(cand.read_text())
                    words = raw.get("words", raw) if isinstance(raw, dict) else raw
                    if isinstance(words, list) and words:
                        return words
                except ValueError:
                    pass
    return []


def vo_timing(path: Path, dur: float, meta: dict, vo_path: Path | None = None) -> tuple[float, float, str]:
    """Return (vo_onset_s, last_word_end_s, vo_src) from silencedetect on the VO stem or mix, plus metadata."""
    vo_src = find_vo_stem(path, meta, vo_path)
    vo_src_str = str(vo_src) if vo_src is not None else "mix"
    src = vo_src or path
    src_dur = duration_s(src) if src != path else dur
    intervals = silence_intervals(src, noise_db=-35.0)
    sd_onset = intervals[0][1] if intervals and intervals[0][0] <= 0.05 else 0.0
    if intervals and intervals[-1][1] >= src_dur - 0.08:
        sd_last_end = intervals[-1][0]
    else:
        sd_last_end = src_dur

    words = _words_for(path, meta)
    meta_onset = None
    if words:
        first = words[0]
        raw_on = first.get("start") if "start" in first else first.get("s")
        if isinstance(raw_on, (int, float)):
            meta_onset = float(raw_on)

    if vo_src is not None:
        onset_s = float(sd_onset)
    else:
        onset_s = max(float(sd_onset), float(meta_onset)) if meta_onset is not None else float(sd_onset)

    meta_last_end: float | None = None
    if isinstance(meta.get("last_word_end_s"), (int, float)):
        meta_last_end = float(meta["last_word_end_s"])
    elif words:
        last = words[-1]
        raw_e = last.get("end") if "end" in last else last.get("e")
        if isinstance(raw_e, (int, float)):
            meta_last_end = float(raw_e)
    elif isinstance(meta.get("vo_s"), (int, float)):
        vo_start = meta.get("vo_start_s")
        if onset_s == 0.0 and (vo_start is None or (isinstance(vo_start, (int, float)) and float(vo_start) == 0.0)):
            meta_last_end = float(meta["vo_s"])

    last_end_s = float(meta_last_end) if meta_last_end is not None else float(sd_last_end)
    return round(onset_s, 3), round(min(dur, max(0.0, last_end_s)), 3), vo_src_str


def vo_timing_verdict(onset_s: float | None, last_word_end_s: float | None, dur: float) -> tuple[list[str], float | None]:
    """(c) WARN when VO onset > 0.15 s; (d) WARN when gap from last word to end > 1.5 s."""
    warns: list[str] = []
    tail_gap: float | None = None
    if onset_s is not None and onset_s > VO_ONSET_WARN_S:
        warns.append(f"first VO word starts at {onset_s:.2f}s > {VO_ONSET_WARN_S:.2f}s — trim leading silence")
    if last_word_end_s is not None:
        tail_gap = round(max(0.0, dur - last_word_end_s), 2)
        if tail_gap > VO_TAIL_WARN_S:
            warns.append(
                f"gap from last word to end is {tail_gap:.2f}s > {VO_TAIL_WARN_S:.1f}s "
                f"(last word {last_word_end_s:.2f}s, duration {dur:.2f}s)"
            )
    return warns, tail_gap


def spoken_text_for(path: Path, meta: dict, script_path: Path | None = None, spoken: str | None = None) -> str:
    """Gather spoken text from explicit args, <stem>_meta.json, captions, or this export's VO transcript."""
    parts: list[str] = []
    if spoken:
        parts.append(spoken)
    if script_path and script_path.is_file():
        parts.append(script_path.read_text(errors="replace"))
    for k in ("spoken", "script", "spoken_end_line"):
        if isinstance(meta.get(k), str):
            parts.append(meta[k])
    words = _words_for(path, meta)
    if words:
        parts.append(" ".join(str(w.get("word") or w.get("text") or "").strip() for w in words))
    for base in (path.parent, path.parent.parent):
        for pat in ("*_vo*.txt", "stt/*_transcript.txt", "*_transcript.txt"):
            for cand in sorted(base.glob(pat)):
                if cand.is_file() and _is_scoped_to_export(cand, path):
                    parts.append(cand.read_text(errors="replace"))
    return "\n".join(p for p in parts if p)


# ----------------------------------------------------------------------------- check
def contact_sheet(path: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = duration_s(path)
    with tempfile.TemporaryDirectory() as td:
        tiles = []
        for i, t in enumerate(SHEET_TIMES):
            if t >= dur - 0.05:
                continue
            p = Path(td) / f"t{i}.png"
            save_frame(path, t, p, w=216)
            tiles.append(p)
        if len(tiles) == 1:
            shutil.copy(tiles[0], out)
            return
        inputs = []
        for p in tiles:
            inputs += ["-i", str(p)]
        run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", f"hstack=inputs={len(tiles)}", str(out)])


def aac_loudness(path: Path) -> tuple[float | None, float | None]:
    """Integrated LUFS and true peak (dBTP) via ebur128=peak=true. None if ffmpeg cannot read them."""
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True)
    integrated = peak = None
    for ln in p.stderr.splitlines():
        if "I:" in ln and "LUFS" in ln:
            integrated = float(ln.split("I:")[1].split("LUFS")[0].strip())
        if "Peak:" in ln and "dBFS" in ln:
            peak = float(ln.split("Peak:")[1].split("dBFS")[0].strip())
    return integrated, peak


def level_verdict(path: Path) -> tuple[list[str], dict]:
    integrated, peak = aac_loudness(path)
    info = {"lufs": integrated, "true_peak_dbtp": peak}
    fails: list[str] = []
    if integrated is None or peak is None:
        fails.append("could not read integrated loudness / true peak (ebur128 peak=true)")
        return fails, info
    lo, hi = LUFS_TARGET - LUFS_TOL, LUFS_TARGET + LUFS_TOL
    if not (lo <= integrated <= hi):
        fails.append(
            f"integrated loudness {integrated:.1f} LUFS outside {lo:.1f}..{hi:.1f} "
            "(target -14.0)"
        )
    if peak > TP_FAIL_DBTP:
        fails.append(f"true peak {peak:.1f} dBTP above {TP_FAIL_DBTP:.1f}")
    return fails, info


def duration_verdict(dur: float, length_test: bool = False) -> tuple[list[str], list[str]]:
    """(fails, warns) for the duration. length_test: the one Chief-OK'd 50–60 s test Short (11 Oct 2026)."""
    fail_at, band = (TEST_DUR_FAIL, TEST_DUR_BAND) if length_test else (DUR_FAIL, DUR_BAND)
    if dur >= fail_at:
        return [f"duration {dur:.1f}s ≥ {fail_at:.0f}s"], []
    if not (band[0] <= dur <= band[1] + 0.5):
        return [], [f"duration {dur:.1f}s outside {band[0]:.0f}–{band[1]:.0f}s band"]
    return [], []


def check(path: Path, air: date, days: int, lib: dict, sheet_dir: Path | None, self_id: str | None = None,
          last: int = LOOKBACK_LAST, length_test: bool = False, report_only: bool = False,
          meta_path: Path | None = None, script_path: Path | None = None, vo_path: Path | None = None,
          spoken: str | None = None) -> dict:
    res: dict = {"file": str(path), "air_date": air.isoformat(), "fails": [], "warns": [], "stayed_fails": []}
    dur = duration_s(path)
    res["duration_s"] = round(dur, 2)
    if length_test:
        res["length_test"] = True
    if report_only:
        res["report_only"] = True
    fails, warns = duration_verdict(dur, length_test)
    res["fails"] += fails
    res["warns"] += warns
    meta = load_sidecar_meta(path, meta_path)

    if not has_audio(path):
        res["audio"] = {"stream": False}
        res["fails"].append("no audio stream — the narrator is missing")
    else:
        whole = mean_volume_db(path)
        opening = mean_volume_db(path, 0.0, OPEN_AUDIO_S)
        res["audio"] = {"stream": True, "mean_db": whole, "open_mean_db": opening}
        if whole < AUDIO_FAIL_DB:
            res["fails"].append(f"soundtrack mean {whole:.1f} dB < {AUDIO_FAIL_DB:.0f} dB — silent or near-silent file")
        elif opening < OPEN_AUDIO_WARN_DB:
            res["warns"].append(f"first {OPEN_AUDIO_S:.1f}s mean {opening:.1f} dB — hook line may start late")
        if whole >= AUDIO_FAIL_DB:
            onset_s, last_end_s, vo_src = vo_timing(path, dur, meta, vo_path)
            vo_warns, tail_gap_s = vo_timing_verdict(onset_s, last_end_s, dur)
            res["vo_src"] = vo_src
            res["vo_onset_s"] = onset_s
            res["last_word_end_s"] = last_end_s
            res["tail_gap_s"] = tail_gap_s
            res["warns"] += vo_warns
            # Level is a ship fail (Chief c61). report_only keeps it out of fails so the
            # upcoming-shorts report and the stayed-gate tests still separate hard fails.
            if not report_only:
                lvl_fails, lvl = level_verdict(path)
                res["level"] = lvl
                res["fails"] += lvl_fails

    motion = motion_first_second(path)
    res["motion_0_1s"] = motion
    if motion < MOTION_WARN:
        res["warns"].append(
            f"picture barely changes in the first second (motion {motion:.1f} < {MOTION_WARN:.0f}) — "
            "trim the clip's ease-in so frame 0 is already mid-action"
        )

    f0_diff = frame0_diff_0_1_5s(path, dur)
    res["frame0_diff_0_1_5s"] = f0_diff
    if f0_diff < FRAME0_DIFF_FAIL:
        res["stayed_fails"].append(
            f"pushed still at frame 0 (mean 0–1.5 s frame diff {f0_diff:.2f} < {FRAME0_DIFF_FAIL:.2f}) — "
            "use moving footage"
        )

    luma_0s, luma_0_5s, kick_0_0_5s = frame0_luma_and_kick(path, dur)
    res["frame0_luma_0s"] = luma_0s
    res["frame0_luma_0_5s"] = luma_0_5s
    res["frame0_kick_0_0_5s"] = kick_0_0_5s
    res["stayed_fails"] += frame0_fade_in_verdict(luma_0s, luma_0_5s)

    hook_edge_0s = frame0_hook_text_score(path, 0.0)
    res["frame0_hook_edge_0s"] = hook_edge_0s
    dims = video_dims(path)
    res["stayed_fails"] += frame0_hook_text_verdict(hook_edge_0s, meta, dims)

    # Rule 24 is a hard fail in every mode: --report-only still reports it as a FAIL, with the numbers.
    res["frame0_full_bleed"] = frame0_full_bleed(path, dur)
    res["fails"] += frame0_full_bleed_verdict(res["frame0_full_bleed"])

    cut1 = first_cut_s(path, dur)
    res["first_cut_s"] = cut1
    res["stayed_fails"] += first_cut_verdict(cut1, dur)

    text = spoken_text_for(path, meta, script_path, spoken)
    res["stayed_fails"] += meta_promise_verdict(text)

    if report_only:
        res["warns"] += [f"[report-only] {m}" for m in res["stayed_fails"]]
    else:
        res["fails"] += res["stayed_fails"]

    h = dhash(path)
    th = thumb(path)
    res["dhash"] = f"{h:016x}"
    near = []
    for e in window(lib, air, days, last, exclude=self_id):
        dist = hamming(h, int(e["dhash"], 16))
        sim = round(background_match(th, e["thumb"]), 3) if channel.BACKGROUND_SSIM_CHECK and e.get("thumb") else None
        if sim is not None and sim >= BG_WARN and dist > DHASH_WARN_BITS:
            tag = "FAIL" if sim >= BG_FAIL else "warn"
            msg = f"same opening background as {e['id']} ({e['date']} · {e['title']}): {sim:.0%} of blocks match, dHash {dist} bits"
            (res["fails"] if tag == "FAIL" else res["warns"]).append(msg)
        if dist <= DHASH_WARN_BITS:
            near.append({"id": e["id"], "date": e["date"], "title": e["title"], "bits": dist, "ssim": sim,
                         "source": e.get("source", "")})
    near.sort(key=lambda x: x["bits"])
    res["near_opens"] = near
    for n in near:
        approx = " [studio capture — approximate]" if n["source"] == "studio_player_capture" else ""
        if n["bits"] <= DHASH_FAIL_BITS:
            res["fails"].append(f"open plate {n['bits']} bits from {n['id']} ({n['date']} · {n['title']}){approx}")
        else:
            res["warns"].append(f"open plate {n['bits']} bits from {n['id']} ({n['date']}){approx}")

    if channel.ROBOT_FRAME0_CHECK:
        sc = orbit_score(path)
        res["orbit"] = sc
        if sc["visor_frac"] >= VISOR_FAIL:
            res["fails"].append(f"Orbit in frame at 0 s (visor {sc['visor_frac']:.4f} ≥ {VISOR_FAIL}) — picture-first lock")
        elif sc["visor_frac"] >= VISOR_WARN:
            res["warns"].append(f"possible Orbit at 0 s (visor {sc['visor_frac']:.4f}) — eyeball the sheet")

    if sheet_dir is not None:
        sheet = sheet_dir / f"{path.stem}_open_sheet.jpg"
        contact_sheet(path, sheet)
        res["contact_sheet"] = str(sheet)
    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    return res


# ----------------------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="gate one or more Short exports")
    c.add_argument("files", nargs="+", type=Path)
    c.add_argument("--air-date", default=date.today().isoformat())
    c.add_argument("--days", type=int, default=LOOKBACK_DAYS)
    c.add_argument("--last", type=int, default=LOOKBACK_LAST, help="also compare the last N Shorts aired before --air-date (R3)")
    c.add_argument("--sheet-dir", type=Path, default=Path(tempfile.gettempdir()) / f"{channel.SLUG}_shorts_gate")
    c.add_argument("--id", default=None, help="candidate's own YouTube id (skips its library entry on re-check)")
    c.add_argument("--json", action="store_true")
    c.add_argument("--length-test", action="store_true",
                   help="the one Chief-OK'd 50-60 s Short length test (AGENTS.md, 11 Oct 2026): band 50-60 s, FAIL at 61 s")
    c.add_argument("--report-only", action="store_true",
                   help="report 60%% stayed-to-watch gate findings (pushed still, first cut >3s, meta-promise) as warnings so scheduled Shorts do not flip to FAIL silently")
    c.add_argument("--meta", type=Path, default=None, help="explicit <stem>_meta.json path")
    c.add_argument("--script", type=Path, default=None, help="explicit script/transcript file for meta-promise lint")
    c.add_argument("--vo", type=Path, default=None, help="explicit VO stem path for onset/tail silencedetect")

    a = sub.add_parser("add", help="register a published/scheduled Short from a local file or frame")
    a.add_argument("--id", required=True)
    a.add_argument("--date", required=True, help="air date YYYY-MM-DD (UK)")
    a.add_argument("--title", required=True)
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", type=Path)
    g.add_argument("--frame", type=Path, help="0.3 s frame image (e.g. Studio player capture)")
    a.add_argument("--source", default=None)
    a.add_argument("--status", default="live", choices=["live", "scheduled", "retired"])

    f = sub.add_parser("fetch", help="register a PUBLIC Short by downloading its first second")
    f.add_argument("--id", required=True)
    f.add_argument("--date", required=True)
    f.add_argument("--title", required=True)

    s = sub.add_parser("status", help="mark an entry live/scheduled/retired (retired = private, no longer compared)")
    s.add_argument("--id", required=True)
    s.add_argument("--status", required=True, choices=["live", "scheduled", "retired"])

    l = sub.add_parser("list")
    l.add_argument("--air-date", default=date.today().isoformat())
    l.add_argument("--days", type=int, default=LOOKBACK_DAYS)
    l.add_argument("--last", type=int, default=LOOKBACK_LAST)
    l.add_argument("--all", action="store_true")

    cmp_ = sub.add_parser("compare", help="pairwise dHash distances inside the library")
    cmp_.add_argument("--ssim", action="store_true", help="print the 30 closest background matches (calibration)")
    sub.add_parser("thumbs", help="backfill the SSIM thumbnail of every entry from its saved frame")

    ns = ap.parse_args(argv)
    lib = load_lib()

    if ns.cmd == "check":
        air = date.fromisoformat(ns.air_date)
        results = [
            check(p.resolve(), air, ns.days, lib, ns.sheet_dir, ns.id, ns.last, ns.length_test,
                  ns.report_only, ns.meta, ns.script, ns.vo)
            for p in ns.files
        ]
        if ns.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            for r in results:
                db = r["audio"].get("mean_db")
                audio = f"{db:.1f}dB" if db is not None else "none"
                cut_s = f"{r['first_cut_s']}s" if r.get("first_cut_s") is not None else "none"
                vo_on = f"{r['vo_onset_s']:.2f}s" if r.get("vo_onset_s") is not None else "none"
                tail_s = f"{r['tail_gap_s']:.2f}s" if r.get("tail_gap_s") is not None else "none"
                vo_src = r.get("vo_src", "none")
                print(
                    f"{r['verdict']}  {Path(r['file']).name}  dur={r['duration_s']}s  audio={audio}  "
                    f"motion={r['motion_0_1s']}  f0diff={r.get('frame0_diff_0_1_5s')}  cut1={cut_s}  "
                    f"vo_onset={vo_on}  tail_gap={tail_s}  vo_src={vo_src}  dhash={r['dhash']}"
                    + (f"  visor={r['orbit']['visor_frac']}" if r.get("orbit") else "")
                )
                for m in r.get("frame0_full_bleed", []):
                    band = (f"  band rows {m['seam_rows'][0]}-{m['seam_rows'][1]} of {FB_H}" if m.get("seam_rows") else "")
                    print(
                        f"   full-bleed {m['t']:.2f}s  {m['kind'] or 'fills the frame'}  "
                        f"detail top/centre/bottom={m['detail_top']}/{m['detail_centre']}/{m['detail_bottom']}  "
                        f"spread top/bottom={m['std_top']}/{m['std_bottom']}{band}"
                    )
                for x in r["fails"]:
                    print(f"   FAIL  {x}")
                for x in r["warns"]:
                    print(f"   warn  {x}")
                if r.get("contact_sheet"):
                    print(f"   sheet {r['contact_sheet']}")
        return 1 if any(r["fails"] for r in results) else 0

    if ns.cmd == "add":
        src = (ns.file or ns.frame).resolve()
        t = OPEN_T if ns.file else None
        e = add_entry(lib, ns.id, ns.date, ns.title, src, ns.source or ("local_export" if ns.file else "frame"), t, ns.status)
        save_lib(lib)
        print(json.dumps(e, indent=2, ensure_ascii=False))
        return 0

    if ns.cmd == "fetch":
        if not shutil.which("yt-dlp"):
            print("yt-dlp missing", file=sys.stderr)
            return 2
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / f"{ns.id}.mp4"
            run(
                ["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=720]/b", "--download-sections", "*0-2",
                 "--force-keyframes-at-cuts", "-o", str(out), f"https://www.youtube.com/shorts/{ns.id}"]
            )
            e = add_entry(lib, ns.id, ns.date, ns.title, out, "yt-dlp_public", OPEN_T, "live")
        save_lib(lib)
        print(json.dumps(e, indent=2, ensure_ascii=False))
        return 0

    if ns.cmd == "status":
        for e in lib["entries"]:
            if e["id"] == ns.id:
                e["status"] = ns.status
                save_lib(lib)
                print(json.dumps(e, indent=2, ensure_ascii=False))
                return 0
        print("id not in library", file=sys.stderr)
        return 2

    if ns.cmd == "list":
        air = date.fromisoformat(ns.air_date)
        rows = lib["entries"] if ns.all else window(lib, air, ns.days, ns.last)
        for e in rows:
            print(f"{e['date']}  {e['id']}  {e['dhash']}" + (f"  visor={e['orbit']['visor_frac']:.4f}" if e.get("orbit") else "") + f"  {e.get('status','live'):9s} {e['title']}")
        return 0

    if ns.cmd == "thumbs":
        done = 0
        for e in lib["entries"]:
            frame = ROOT / e.get("frame", "")
            if e.get("frame") and frame.exists():
                e["thumb"] = thumb(frame, None)
                done += 1
            else:
                print(f"no frame for {e['id']} ({e.get('frame')}); re-add it from its file")
        save_lib(lib)
        print(f"thumbnails: {done}/{len(lib['entries'])}")
        return 0
    if ns.cmd == "compare":
        es = [e for e in lib["entries"] if e.get("status") != "retired"]
        if ns.ssim:
            pairs = sorted(((background_match(a_["thumb"], b_["thumb"]), a_, b_) for i, a_ in enumerate(es) for b_ in es[i + 1:]
                            if a_.get("thumb") and b_.get("thumb")), key=lambda p: -p[0])
            for s, a_, b_ in pairs[:30]:
                print(f"bg match {s:.0%}  {a_['id']} ({a_['date']})  ↔  {b_['id']} ({b_['date']})")
            print(f"{len(pairs)} pairs; FAIL ≥ {BG_FAIL:.0%}, warn ≥ {BG_WARN:.0%}")
            return 0
        for i, a_ in enumerate(es):
            for b_ in es[i + 1:]:
                bits = hamming(int(a_["dhash"], 16), int(b_["dhash"], 16))
                if bits <= DHASH_WARN_BITS:
                    tag = "FAIL" if bits <= DHASH_FAIL_BITS else "warn"
                    print(f"{tag} {bits:2d} bits  {a_['id']} ({a_['date']})  ↔  {b_['id']} ({b_['date']})")
        return 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr.decode(errors="replace"))
        raise SystemExit(2)
