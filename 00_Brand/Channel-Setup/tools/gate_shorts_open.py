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
 10. the picture does not fill 9:16: black bars, a flat   (10 Nov 2026, J2539, LEARNINGS rule 24 — the
     band, a blurred copy or a mirrored copy above and    Short that aired on 10 Nov opened on a 16:9 band
     below a picture band. At the opening (frame 0, or    over blurred fill, passed this gate on 9 Nov and
     most frames to 0.5 s), or on more than 10% of the    the feed barely showed it. 11 Nov 2026, J2546: the
     frames sampled once a second over the whole Short.   rule was set on 56 real frames labelled by eye, and
     An end card the cut's meta names is judged apart.    the whole Short is sampled, not only its opening.)

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
# Full-bleed (10 Nov 2026, J2539, LEARNINGS rule 24; made right on real frames 11 Nov 2026, J2546): the Short that
# aired on 10 Nov opened on a 16:9 picture band with blurred fill above and below, passed this gate on 9 Nov, and
# the Shorts feed barely showed it. An audit by eye then found the same look inside eight more scheduled Shorts.
# (i) FAIL when the picture does not fill the 9:16 frame: at the opening, or on more than FB_CLIP_MAX_SHARE of the
#     frames sampled once a second over the whole Short. Grey FB_W x FB_H frames.
#     What marks a padded frame, measured on 56 frames labelled by eye (jobs/reviews/J2545): fill has no fine
#     detail. A blurred, enlarged copy is smooth at one-pixel spacing, and a flat band has nothing at all. A real
#     picture nearly always has some, even a soft wall behind a subject. So a frame is padded when
#       - the outer top and the outer bottom (FB_TOP, FB_BOTTOM: outside the picture band of any shape from 16:9
#         to square) each have at most FB_OUT_MAX of their pixels sharp, with caption rows left out, and
#       - the middle (FB_MIDDLE) has at least FB_MID_MIN of its pixels sharp: there is a picture between them, and
#       - the outside is fill and not the picture's own plain background:
#           "blur-pad" it still holds a picture (smooth brightness spread of FB_PICTURE_STD or more on a side),
#                      or its top and bottom differ in brightness by FB_SIDES_MEAN or more, or it is plain with a
#                      straight edge above and below the picture;
#           "bars"     it is one flat shade (spread <= FB_UNIFORM_STD on both sides, the same shade top and
#                      bottom) AND the picture has a straight edge above and below. Without the edges it is a
#                      subject on a plain backdrop, a planet on black space, and passes.
#       "mirror" is looked for on its own: the picture's rows reflected outward from a seam above and below.
#     Sharp = the second difference (left-right or up-down) is FB_SHARP grey levels or more.
#     A caption row has FB_CAPTION_PIXELS or more pixels both bright and very sharp; FB_CAPTION_GROW rows each
#     side go with it. A side with fewer than FB_MIN_ROWS rows left cannot be judged, and the frame passes.
#     A straight edge = FB_SEAM_COLS of the columns step by FB_SEAM_STEP across one row, and at most FB_SEAM_QUIET
#     of them step four rows further out (a planet's curved limb, or picture texture, steps there too).
#     Known limits, named in the test: a light, feathered blur under a large hook caption still reads as sharp;
#     a dark graphic on a dark backdrop of another colour is one shade in grey.
FB_W, FB_H = 108, 192
FB_TIMES = (0.0, 0.25, 0.5)
FB_TOP = (3, 42)               # rows; outside the band of any picture from 16:9 (rows 66-126) to square (42-150)
FB_TOP_MORE = (42, 54)         # added when captions leave too few rows above: still outside a 16:9 or 4:3 band
FB_BOTTOM = (150, 189)
FB_BOTTOM_MORE = (138, 150)
FB_MIDDLE = (76, 116)          # inside the band of any picture from 16:9 to square
FB_SHARP = 8                   # grey levels of second difference
FB_OUT_MAX = 0.08              # labelled frames: padded 0.064 at most, full 0.102 at least
FB_MID_MIN = 0.06              # labelled frames: padded 0.08 at least; a smooth full frame (an eclipse) 0.03
FB_CAPTION_BRIGHT = 180
FB_CAPTION_SHARP = 28
FB_CAPTION_PIXELS = 3
FB_CAPTION_GROW = 4
FB_MIN_ROWS = 10
FB_UNIFORM_STD = 3.0
FB_UNIFORM_MEAN = 6.0
FB_PICTURE_STD = 10.0          # spread of 6-pixel block means along the rows: brightness that is not fine detail
FB_SIDES_MEAN = 15.0
FB_SEAM_ROWS = (24, 90)        # where the upper edge may sit; the lower one mirrors it
FB_SEAM_STEP = 3.0
FB_SEAM_COLS = 0.60
FB_SEAM_QUIET = 0.25
FB_SEAM_SYM_ROWS = 4           # the two edges sit within this many rows of the same distance from the centre
FB_DETAIL_FLOOR = 1.5          # row detail a real picture carries (reported; the made-frame tests read it)
FB_MIRROR_RANGE = (0.16, 0.42) # upper mirror seam as a share of the height
FB_MIRROR_SYM_ROWS = 3
FB_MIRROR_ROWS = 8
FB_MIRROR_DIFF = 4.0
FB_MIRROR_VERT = 8.0           # the picture must change this much over FB_MIRROR_ROWS rows for a mirror to count
FB_CLIP_STEP_S = 1.0           # the whole Short: one frame a second
FB_CLIP_MAX_SHARE = 0.10
# A frame can look padded with no straight edge where the picture meets the fill: a blurred copy with feathered
# edges, or a full-frame shot whose own top and bottom are soft (tissue walls round vessels, a smooth nebula
# behind hook text). One frame cannot always tell the two apart (J2557, J2560), so such frames count for less.
FB_EDGE_RATIO = 2.5            # an edge: the step across one row is this many times the change just outside it
FB_EDGE_SHARE = 0.65           # labelled frames: a soft full frame 0.54 at most; a padded frame with a clear edge 0.69 at least
FB_CLIP_SOFT_SHARE = 0.15      # padded-looking frames, with or without an edge: this share of the Short before it fails
# Cuts Ben OK'd by watching before the whole-Short rule existed. Their padded stretches are measured and said, as a
# warning: the cut he OK'd must still be able to go up as the fallback while its full-frame version waits for his
# watch. Matched by the file's sha256, so a re-cut is never covered. The opening rule has no such list.
FB_OKD_BEFORE_RULE = Path(__file__).resolve().parent / "full_bleed_okd_before_rule.json"


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


# ----------------------------------------------------------------------------- full-bleed (J2539, J2546)
def _fb_row_detail(g: bytes) -> list[float]:
    """Per row of an FB_W x FB_H grey frame: mean absolute left-right difference."""
    W = FB_W
    out = []
    for y in range(FB_H):
        row = g[y * W:(y + 1) * W]
        out.append(sum(abs(row[x + 1] - row[x]) for x in range(W - 1)) / (W - 1))
    return out


def _fb_std(g: bytes, y0: int, y1: int) -> float:
    v = g[max(0, y0) * FB_W:max(0, y1) * FB_W]
    if not v:
        return 0.0
    m = sum(v) / len(v)
    return (sum((p - m) ** 2 for p in v) / len(v)) ** 0.5


def _fb_avg(vals: list[float], y0: int, y1: int) -> float:
    v = vals[max(0, y0):max(0, y1)]
    return sum(v) / len(v) if v else 0.0


def _fb_sharpness(g: bytes) -> bytearray:
    """Per pixel: the larger of the left-right and the up-down second difference (0 on the frame's edge where one
    cannot be taken). Fine detail is large here; a blurred enlargement is close to 0 even where it has contrast."""
    W, H = FB_W, FB_H
    out = bytearray(W * H)
    for y in range(H):
        o = y * W
        row = g[o:o + W]
        up = g[o - W:o] if y > 0 else None
        dn = g[o + W:o + 2 * W] if y < H - 1 else None
        for x in range(W):
            h = abs(row[x - 1] - 2 * row[x] + row[x + 1]) if 0 < x < W - 1 else 0
            v = abs(up[x] - 2 * row[x] + dn[x]) if up is not None and dn else 0
            out[o + x] = min(255, h if h > v else v)
    return out


def _fb_caption_rows(g: bytes, sharp: bytearray) -> list[bool]:
    """Rows that carry lettering (pixels both bright and very sharp), with FB_CAPTION_GROW rows each side for the
    outline and the glow. A hook or a subtitle over the fill must not make the fill look like picture."""
    W, H = FB_W, FB_H
    hit = []
    for y in range(H):
        o = y * W
        n = sum(1 for x in range(W) if g[o + x] >= FB_CAPTION_BRIGHT and sharp[o + x] >= FB_CAPTION_SHARP)
        hit.append(n >= FB_CAPTION_PIXELS)
    return [any(hit[max(0, y - FB_CAPTION_GROW):y + FB_CAPTION_GROW + 1]) for y in range(H)]


def _fb_side(g: bytes, sharp: bytearray, caption: list[bool], zone: tuple[int, int], more: tuple[int, int]) -> dict | None:
    """One outer zone with its caption rows left out: share of sharp pixels, brightness mean and spread, and the
    spread of 6-pixel block means (brightness that is not fine detail). None when too few rows are left."""
    W = FB_W
    rows = [y for y in range(*zone) if not caption[y]]
    if len(rows) < FB_MIN_ROWS:
        rows += [y for y in range(*more) if not caption[y]]
    if len(rows) < FB_MIN_ROWS:
        return None
    n = len(rows) * W
    hits = tot = 0
    blocks = []
    for y in rows:
        o = y * W
        row = g[o:o + W]
        hits += sum(1 for x in range(W) if sharp[o + x] >= FB_SHARP)
        tot += sum(row)
        blocks += [sum(row[x:x + 6]) / 6 for x in range(0, W - W % 6, 6)]
    mean = tot / n
    var = sum((g[y * W + x] - mean) ** 2 for y in rows for x in range(W)) / n
    bm = sum(blocks) / len(blocks)
    return {
        "share": hits / n, "mean": mean, "std": var ** 0.5,
        "smooth_std": (sum((v - bm) ** 2 for v in blocks) / len(blocks)) ** 0.5, "rows": len(rows),
    }


def _fb_step_share(g: bytes, y: int) -> float:
    """Share of columns whose brightness steps by FB_SEAM_STEP or more across row y (two rows each side)."""
    W = FB_W
    if y < 2 or y + 2 >= FB_H:
        return 0.0
    a0, a1, b0, b1 = (y - 2) * W, (y - 1) * W, (y + 1) * W, (y + 2) * W
    return sum(1 for x in range(W) if abs(g[b0 + x] + g[b1 + x] - g[a0 + x] - g[a1 + x]) >= 2 * FB_SEAM_STEP) / W


def _fb_edges(g: bytes) -> tuple[int, int, float] | None:
    """A straight edge above the picture and another below it, the same distance from the centre: (upper row,
    lower row, the smaller share of columns that step). Four rows further out almost nothing may step, so a
    planet's curved limb and the texture inside a picture are not edges."""
    H = FB_H
    memo: dict[int, float] = {}

    def share(y: int) -> float:
        if y not in memo:
            memo[y] = _fb_step_share(g, y)
        return memo[y]

    best = None
    for u in range(*FB_SEAM_ROWS):
        if share(u) < FB_SEAM_COLS or share(u - 4) > FB_SEAM_QUIET:
            continue
        for low in range(H - 1 - u - FB_SEAM_SYM_ROWS, H - 1 - u + FB_SEAM_SYM_ROWS + 1):
            if share(low) >= FB_SEAM_COLS and share(low + 4) <= FB_SEAM_QUIET:
                score = min(share(u), share(low))
                if best is None or score > best[2]:
                    best = (u, low, score)
    return best


def _fb_edge_share(g: bytes) -> tuple[float, float]:
    """The clearest straight edge above the picture, and below it: the share of columns where the brightness steps
    across one row by FB_SEAM_STEP or more and by far more than it changes just outside that row. A blurred fill
    changes slowly right up to the picture and then steps, all along one row. A soft part of a real picture has no
    such row: where its detail begins differs from column to column."""
    W, H = FB_W, FB_H

    def share(y: int, d: int) -> float:              # d = -1: the fill is above row y; +1: it is below
        far0, far1 = (y + 5 * d) * W, (y + 4 * d) * W
        near0, near1 = (y + 2 * d) * W, (y + d) * W
        in0, in1 = (y - d) * W, (y - 2 * d) * W
        n = 0
        for x in range(W):
            near = g[near0 + x] + g[near1 + x]
            step = abs(g[in0 + x] + g[in1 + x] - near)
            drift = abs(near - g[far0 + x] - g[far1 + x])
            if step >= 2 * FB_SEAM_STEP and step >= FB_EDGE_RATIO * drift + 2:
                n += 1
        return n / W

    lo, hi = FB_SEAM_ROWS
    return (max(share(y, -1) for y in range(lo, hi)),
            max(share(y, 1) for y in range(H - 1 - hi, H - 1 - lo)))


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


def _fb_mirror(g: bytes) -> tuple[int, int, float, float] | None:
    """Mirrored fill has no brightness step at its seam, so it is looked for on its own."""
    H = FB_H
    memo: dict[int, tuple[float, float]] = {}

    def diff(y: int) -> tuple[float, float]:
        if y not in memo:
            memo[y] = _fb_mirror_diff(g, y)
        return memo[y]

    for u in range(int(H * FB_MIRROR_RANGE[0]), int(H * FB_MIRROR_RANGE[1]) + 1):
        md_u, mv_u = diff(u)
        if md_u > FB_MIRROR_DIFF or mv_u < FB_MIRROR_VERT:
            continue
        for low in range(H - u - FB_MIRROR_SYM_ROWS, H - u + FB_MIRROR_SYM_ROWS + 1):
            md_l, mv_l = diff(low)
            if md_l <= FB_MIRROR_DIFF and mv_l >= FB_MIRROR_VERT:
                return u, low, md_u, md_l
    return None


def full_bleed_frame(g: bytes) -> dict:
    """Measure one FB_W x FB_H grey frame. 'kind' is None (the picture fills the frame), 'bars', 'blur-pad' or
    'mirror'; 'why' says which evidence decided it. 'edge' is True when a straight edge was found where the picture
    meets the fill, False when the frame only looks padded (soft above and below a detailed middle). The other keys
    are the numbers behind it, for the report."""
    H = FB_H
    det = _fb_row_detail(g)
    fifth = H // 5
    out: dict = {
        "kind": None,
        "why": None,
        "detail_top": round(_fb_avg(det, 0, fifth), 2),
        "detail_centre": round(_fb_avg(det, int(H * 0.38), int(H * 0.62)), 2),
        "detail_bottom": round(_fb_avg(det, H - fifth, H), 2),
        "std_top": round(_fb_std(g, 0, fifth), 2),
        "std_bottom": round(_fb_std(g, H - fifth, H), 2),
        "seam_rows": None,
        "edge": None,
        "sharp_top": None,
        "sharp_middle": None,
        "sharp_bottom": None,
    }
    mirror = _fb_mirror(g)
    if mirror:
        out.update(kind="mirror", why="the picture's rows are reflected outward above and below it", edge=True,
                   seam_rows=[mirror[0], mirror[1]], mirror_diff=[round(mirror[2], 2), round(mirror[3], 2)])
        return out
    sharp = _fb_sharpness(g)
    caption = _fb_caption_rows(g, sharp)
    top = _fb_side(g, sharp, caption, FB_TOP, FB_TOP_MORE)
    bottom = _fb_side(g, sharp, caption, FB_BOTTOM, FB_BOTTOM_MORE)
    m0, m1 = FB_MIDDLE
    middle = sum(1 for i in range(m0 * FB_W, m1 * FB_W) if sharp[i] >= FB_SHARP) / ((m1 - m0) * FB_W)
    out["sharp_middle"] = round(middle, 3)
    if top is None or bottom is None:
        return out                                   # captions cover an outer zone: it cannot be judged
    out.update(
        sharp_top=round(top["share"], 3), sharp_bottom=round(bottom["share"], 3),
        outside_std=[round(top["std"], 2), round(bottom["std"], 2)],
        outside_mean=[round(top["mean"], 1), round(bottom["mean"], 1)],
        outside_smooth_std=[round(top["smooth_std"], 2), round(bottom["smooth_std"], 2)],
    )
    if max(top["share"], bottom["share"]) > FB_OUT_MAX or middle < FB_MID_MIN:
        return out                                   # real detail outside, or no picture in the middle
    edges = _fb_edges(g)
    if edges:
        out.update(seam_rows=[edges[0], edges[1]], seam_step_share=round(edges[2], 3))
    uniform = (max(top["std"], bottom["std"]) <= FB_UNIFORM_STD
               and abs(top["mean"] - bottom["mean"]) <= FB_UNIFORM_MEAN)
    if uniform:
        if edges:
            out.update(kind="bars", why="one flat shade above and below, with a straight edge at the picture", edge=True)
        return out                                   # no straight edges: a subject on its own plain backdrop
    if max(top["smooth_std"], bottom["smooth_std"]) >= FB_PICTURE_STD:
        out.update(kind="blur-pad", why="no fine detail above or below, yet a picture's brightness is there")
    elif abs(top["mean"] - bottom["mean"]) >= FB_SIDES_MEAN:
        out.update(kind="blur-pad", why="no fine detail above or below, and the two differ in brightness")
    elif edges:
        out.update(kind="blur-pad", why="plain above and below, with a straight edge at the picture")
    if out["kind"]:
        if edges:
            out["edge"] = True
        else:
            share = _fb_edge_share(g)
            out.update(edge_share=[round(share[0], 3), round(share[1], 3)], edge=max(share) >= FB_EDGE_SHARE)
            if not out["edge"]:
                out["why"] += "; no straight edge where a picture would meet its fill"
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


def _fb_numbers(f: dict) -> str:
    if f["kind"] == "mirror":
        return f"mirror difference {f['mirror_diff'][0]} / {f['mirror_diff'][1]}"
    return (f"sharp pixels above/middle/below {f['sharp_top']:.0%}/{f['sharp_middle']:.0%}/{f['sharp_bottom']:.0%}: "
            f"{f['why']}")


def frame0_full_bleed_verdict(frames: list[dict]) -> list[str]:
    """(i) FAIL when the frame at 0.0 s, or most of the frames to 0.5 s, show a picture band with fill above and
    below it and a straight edge between them. A frame that only looks padded is for frame0_full_bleed_note()."""
    bad = [f for f in frames if f.get("kind") and f.get("edge", True)]
    if not bad:
        return []
    if not ((frames[0].get("kind") and frames[0].get("edge", True)) or len(bad) * 2 > len(frames)):
        return []
    f = bad[0]
    kinds = " / ".join(sorted({b["kind"] for b in bad}))
    return [
        f"frame 0 is not full-bleed 9:16: {kinds} above and below a picture band on {len(bad)}/{len(frames)} frames "
        f"from 0.0 to 0.5 s (at {f['t']:.2f}s, {_fb_numbers(f)}) — reframe the opening shot to fill 1080x1920"
    ]


def frame0_full_bleed_note(frames: list[dict]) -> list[str]:
    """A warning when the opening only looks padded: soft above and below a detailed middle, no straight edge."""
    soft = [f for f in frames if f.get("kind") and not f.get("edge", True)]
    if not soft or frame0_full_bleed_verdict(frames):
        return []
    f = soft[0]
    return [
        f"the opening may not be full-bleed 9:16: soft above and below a detailed middle on {len(soft)}/{len(frames)} "
        f"frames from 0.0 to 0.5 s (at {f['t']:.2f}s, {_fb_numbers(f)}). No straight edge was found, so this is "
        "not a FAIL: look at frame 0 and say which it is"
    ]


def end_card_window(meta: dict | None, dur: float) -> tuple[float, float] | None:
    """The stretch the cut's own meta file names as its end card, in seconds, or None. Only what the meta says:
    a share of the length is never used as a stand-in (Chief ruling on J2545, 11 Nov 2026)."""
    if not isinstance(meta, dict):
        return None
    w = meta.get("end_card_window_s")
    if isinstance(w, (list, tuple)) and len(w) == 2 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in w):
        a, b = float(w[0]), float(w[1])
    else:
        card = meta.get("end_card")
        start = card.get("start_s") if isinstance(card, dict) else None
        if not isinstance(start, (int, float)) or isinstance(start, bool):
            return None
        length = card.get("len_s")
        a = float(start)
        b = a + float(length) if isinstance(length, (int, float)) and not isinstance(length, bool) else dur
    a, b = max(0.0, a), min(dur, b)
    return (a, b) if b > a else None


def okd_before_rule(path: Path, listed: Path | None = None) -> dict | None:
    """The entry for this exact file in the list of cuts Ben OK'd before the whole-Short rule, or None."""
    listed = listed or FB_OKD_BEFORE_RULE
    try:
        cuts = json.loads(listed.read_text()).get("cuts") or []
    except (OSError, ValueError, AttributeError):
        return None
    wanted = {str(c.get("sha256") or "").lower(): c for c in cuts if isinstance(c, dict) and c.get("ok")}
    if not wanted:
        return None
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return wanted.get(h.hexdigest())


def clip_full_bleed(path: Path, dur: float | None = None) -> list[dict]:
    """full_bleed_frame() for one frame every FB_CLIP_STEP_S over the whole Short, each with its time 't'."""
    if dur is None:
        dur = duration_s(path)
    out = []
    t = 0.0
    while t < dur - 0.05:
        m = full_bleed_frame(raw_frame(path, FB_W, FB_H, t, "gray"))
        m["t"] = round(t, 2)
        out.append(m)
        t += FB_CLIP_STEP_S
    return out


def padded_stretches(frames: list[dict]) -> list[tuple[float, float, str]]:
    """Runs of padded sampled frames as (first second, last second + one step, kinds). A kind found without a
    straight edge is named so: 'blur-pad, no edge'."""
    out: list[tuple[float, float, str]] = []
    run_start = None
    kinds: set[str] = set()
    last = 0.0
    for f in frames:
        if f.get("kind"):
            if run_start is None:
                run_start, kinds = f["t"], set()
            kinds.add(f["kind"] if f.get("edge", True) else f["kind"] + ", no edge")
            last = f["t"]
        elif run_start is not None:
            out.append((run_start, last + FB_CLIP_STEP_S, " / ".join(sorted(kinds))))
            run_start = None
    if run_start is not None:
        out.append((run_start, last + FB_CLIP_STEP_S, " / ".join(sorted(kinds))))
    return out


def clip_full_bleed_verdict(frames: list[dict], end_card: tuple[float, float] | None = None) -> tuple[list[str], list[str]]:
    """(fails, warns) for the whole Short, on the frames sampled outside the end card. FAIL when more than
    FB_CLIP_MAX_SHARE of them are padded with a straight edge at the picture, or more than FB_CLIP_SOFT_SHARE look
    padded, edge or no edge. Fewer is a warning that names the seconds. A padded end card is said, not failed: it
    is judged apart from the shots."""
    def in_card(f: dict) -> bool:
        return end_card is not None and end_card[0] <= f["t"] < end_card[1]

    body = [f for f in frames if not in_card(f)]
    card = [f for f in frames if in_card(f)]
    fails, warns = [], []
    bad = [f for f in body if f.get("kind")]
    edged = [f for f in bad if f.get("edge", True)]
    runs = ", ".join(f"{a:.0f}-{b:.0f}s ({k})" for a, b, k in padded_stretches(body))
    if body and (len(edged) > FB_CLIP_MAX_SHARE * len(body) or len(bad) > FB_CLIP_SOFT_SHARE * len(body)):
        left_out = f", end card {end_card[0]:.1f}-{end_card[1]:.1f}s left out" if end_card else ""
        if len(edged) > FB_CLIP_MAX_SHARE * len(body):
            share = f"{len(bad) / len(body):.0%}, limit {FB_CLIP_MAX_SHARE:.0%}"
        else:
            share = (f"{len(bad) / len(body):.1%}; {len(edged)} with a straight edge at the picture; "
                     f"limit {FB_CLIP_SOFT_SHARE:.0%} when no edge is found")
        fails.append(
            f"the picture does not fill 9:16 on {len(bad)}/{len(body)} frames sampled once a second "
            f"({share}{left_out}): {runs} — make every shot fill "
            "1080x1920 (crop and scale, or other picture; no blurred, mirrored or flat band)"
        )
    elif bad and not edged:
        warns.append(
            f"the picture may not fill 9:16 on {len(bad)}/{len(body)} sampled frames: {runs}. They are soft above "
            "and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those "
            "seconds and say which it is"
        )
    elif bad:
        warns.append(f"the picture does not fill 9:16 on {len(bad)}/{len(body)} sampled frames: {runs}")
    if any(f.get("kind") for f in card):
        warns.append(
            f"the end card ({end_card[0]:.1f}-{end_card[1]:.1f}s) sits on fill, not a full 9:16 picture: "
            "judged apart from the shots"
        )
    return fails, warns


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
    opening = frame0_full_bleed_verdict(res["frame0_full_bleed"])
    res["fails"] += opening
    res["warns"] += frame0_full_bleed_note(res["frame0_full_bleed"])
    # The whole Short, one frame a second. The end card is judged apart, only where the cut's meta names it.
    card = end_card_window(meta, dur)
    res["end_card_window_s"] = list(card) if card else None
    res["clip_full_bleed"] = clip_full_bleed(path, dur)
    res["padded_stretches_s"] = [[a, b, k] for a, b, k in padded_stretches(res["clip_full_bleed"])]
    clip_fails, clip_warns = clip_full_bleed_verdict(res["clip_full_bleed"], card)
    okd = okd_before_rule(path) if clip_fails else None
    res["okd_before_full_bleed_rule"] = okd
    if okd:
        clip_warns += [f"{f} [not a FAIL for this file: OK'd before the rule ({okd['ok']}); a re-cut is not covered]"
                       for f in clip_fails]
        clip_fails = []
    res["fails"] += clip_fails
    res["warns"] += clip_warns

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
                    band = (f"  edge rows {m['seam_rows'][0]}-{m['seam_rows'][1]} of {FB_H}" if m.get("seam_rows") else "")
                    print(
                        f"   full-bleed {m['t']:.2f}s  {m['kind'] or 'fills the frame'}  "
                        f"sharp above/middle/below={m['sharp_top']}/{m['sharp_middle']}/{m['sharp_bottom']}  "
                        f"detail top/centre/bottom={m['detail_top']}/{m['detail_centre']}/{m['detail_bottom']}  "
                        f"spread top/bottom={m['std_top']}/{m['std_bottom']}{band}"
                    )
                clip = r.get("clip_full_bleed") or []
                if clip:
                    runs = ", ".join(f"{a:.0f}-{b:.0f}s ({k})" for a, b, k in r.get("padded_stretches_s") or []) or "none"
                    card = r.get("end_card_window_s")
                    print(
                        f"   full-bleed whole Short  {sum(1 for m in clip if m['kind'])}/{len(clip)} frames padded, "
                        f"one a second  padded stretches: {runs}"
                        + (f"  end card {card[0]:.1f}-{card[1]:.1f}s judged apart" if card else "  no end card named in meta")
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
