#!/usr/bin/env python3
"""J0936 — 028 Fri 4 Dec Short v02. £0 local re-cut of jJ5LkFGyzLI. No upload.

Audit #16: sentence 1 is "Gliese 710 passes at about a fifth of a light-year."
"Gliese 710 passes" is spliced from this Short's own VO (master 188.88–191.08,
the 15.18–17.38 s window of v01). The distance lines stay the locked words:
a fifth of a light-year, one centimeter, 30 centimeters, a ruler, 100 meters,
a football pitch. Pauses inside "Gliese / 710 / passes" are trimmed; the three
words are about 1.4 s, so "fifth" lands near 2.0 s. The audit's 1.45 s figure
does not fit these word lengths once "passes at about a" is said.

Frame 0 is the SDO surface at 23 s (2.2x), not the 32 s close-up used on
the Wed 2 Dec Short. No end card. 1.0 s loop back to that disk. The 100-meter
line is last, so it clears 70% and the 9–14 s title. v01 is left untouched.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

VO_WAV = FILM / "02_Voiceover/star_coming_vo_v01.wav"
WORDS = FILM / "07_Edit-Project/full_master_v03_pack/gliese_words_list.json"
BED = FILM / "05_Music/gliese_score_bed_v03.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
HDIR = FILM / "07_Edit-Project/nasa_pool_v01/028_harvest_v01"
PITCH = FILM / "04_Generated-Clips/01_Raw/veo_v01/football_pitch_veo_v01.mp4"

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0936_fri04_v02")
STEM = "028_short_fri04_scale_v02"

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-12-04"
VIDEO_ID = "jJ5LkFGyzLI"
LONG_TITLE = "What Happens When a Star Passes Through Our Solar System?"
LONG_ID = "F-jImX5h7ws"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
LOOP = 1.00
XFADE = 0.012
ROOM = (2.44, 2.80)
FRAME0_SPEED = 2.2

# Source times on star_coming_vo_v01.wav. Pauses over 0.20 s are their own segments.
# "Gliese 710 passes" is moved to the front. "100 meters" is last so it clears 70%.
SEGMENTS = [
    (188.88, 189.24, "Gliese"),
    (189.80, 190.28, "710"),
    (190.68, 191.08, "passes"),
    (164.74, 166.36, "at about a fifth of a light-year."),
    (178.36, 181.44, "Make the gap between the sun and Earth one centimeter."),
    (182.18, 184.04, "Neptune, our outermost planet,"),
    (184.40, 186.28, "is then 30 centimeters away,"),
    (186.74, 188.10, "about the length of a ruler."),
    (195.68, 198.52, "So the star will not come anywhere near the planets."),
    (191.14, 192.82, "more than 100 meters away,"),
    (193.26, 194.82, "the length of a football pitch."),
]
GAPS = {1: 0.05, 2: 0.05, 3: 0.06, 4: 0.08, 5: 0.08, 6: 0.08, 7: 0.10, 8: 0.10, 9: 0.10, 10: 0.08}
MARKS = {
    "Gliese": (0, 188.88),
    "710": (1, 189.80),
    "passes": (2, 190.68),
    "fifth": (3, 165.30),
    "one": (4, 180.30),
    "thirty": (6, 184.84),
    "hundred": (9, 191.56),
    "meters": (9, 192.08),
    "football": (10, 194.00),
    "pitch": (10, 194.44),
}

LAS = HDIR / "eso_lasilla_ntt.mp4"
SDO = HDIR / "sdo_solar_flare.mp4"
GAIA = HDIR / "gaia_motion_1_6my.mp4"
CROP_9 = "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"


def crop_x(x: int) -> str:
    return (
        f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    )


# SDO surface at 23 s, played at 2.2x so the 0–1.5 s gate stays above 1.50.
# The Wed 2 Dec Short opens on the 32 s close-up.
FRAME0 = (
    23.0,
    SDO,
    "NASA SDO sun, bright surface already in motion",
    1.78,
    CROP_9,
)
# Body plates. Same-file offsets stay more than 10 s apart. The pitch plate
# is swapped onto the shot that says "football".
PLATES = [
    (0.40, LAS, "ESO La Silla at dusk, telescope dome and sky", 1.78, True, crop_x(180)),
    (50.0, SDO, "NASA SDO sun, close view of an active region", 1.78, True, CROP_9),
    (8.0, GAIA, "ESA Gaia Milky Way in motion", 0.89, True, CROP_9),
    (14.5, LAS, "ESO La Silla telescope wall, later in the clip", 1.78, True, crop_x(1100)),
    (0.40, PITCH, "Floodlit football pitch, the scale for 100 meters", 1.97, True, "PITCH"),
]


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fit_font(draw, text, size, max_w, stroke):
    while size > 28:
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) + stroke * 2 <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(FONT, 28)


def centred(draw, y, text, font, fill, stroke):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return draw.textbbox((x, y), text, font=font, stroke_width=stroke)


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise SystemExit(f"expected 48 kHz stereo s16, got {w.getframerate()} {w.getnchannels()}ch")
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    return raw.reshape(-1, 2)


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = np.clip(audio, -1, 1)
    pcm = (pcm * 32767.0).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def build_vo(src: np.ndarray, words_raw: list[dict]) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(ROOM[0] * SR): int(ROOM[1] * SR)]
    for i, (a, b, _label) in enumerate(SEGMENTS):
        if i:
            need = int(GAPS.get(i, 0.10) * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        i0, i1 = int(round(a * SR)), int(round(b * SR))
        clip = src[i0:i1].copy()
        if i and fade_n > 8:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        picked = []
        for w in words_raw:
            ws, we = float(w["start"]), float(w["end"])
            if a - 0.02 <= ws and we <= b + 0.04:
                picked.append(w)
        if not picked:
            raise SystemExit(f"no words in segment {i} {_label}")
        for prev, w in zip(picked, picked[1:]):
            gap = float(w["start"]) - float(prev["end"])
            if gap > 0.20:
                raise SystemExit(f"pause {gap:.2f}s inside segment {i} before {w['text']!r}")
        for w in picked:
            ws, we = float(w["start"]), float(w["end"])
            cap_words.append({
                "word": w["text"],
                "start": round(starts[-1] + (ws - a), 3),
                "end": round(starts[-1] + (we - a), 3),
            })
        parts.append(clip)
        cursor += len(clip)
    audio = np.concatenate(parts, axis=0)
    marks = {}
    for name, (seg, src_t) in MARKS.items():
        a = SEGMENTS[seg][0]
        marks[name] = round(starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def plan_cuts(words: list[dict], vo_end: float) -> list[float]:
    """Cut times after frame 0. First cut is the latest word end at or before 2.90 s."""
    ends = [w["end"] for w in words]
    early = [e for e in ends if 2.05 <= e <= 2.88]
    if not early:
        raise SystemExit(f"no word end inside 2.05–2.88 s: {ends[:12]}")
    first = round(min(2.90, max(early) + 0.03), 3)
    cuts = [first]
    t = first
    guard = 0
    while vo_end - t > 3.80:
        guard += 1
        if guard > 12:
            raise SystemExit(f"cut planner stuck at {t}")
        cands = [w for w in words if t + 2.45 <= w["end"] <= t + 3.72]
        if not cands:
            cands = [w for w in words if t + 2.15 <= w["end"] <= t + 3.72]
        if not cands:
            raise SystemExit(f"no legal cut after {t:.2f} before {vo_end:.2f}")
        punct = [w for w in cands if w["word"][-1:] in ".,?!"]
        pick = (punct or cands)[-1]
        nxt = round(min(pick["end"] + 0.03, t + 3.75), 3)
        if nxt <= t + 0.4:
            raise SystemExit(f"cut did not advance at {t}")
        cuts.append(nxt)
        t = nxt
    tail = vo_end - t
    if tail < 2.05 and len(cuts) >= 2:
        # Give the last shot the previous boundary so it is not a flash.
        cuts.pop()
        t = cuts[-1]
        tail = vo_end - t
    if tail > 3.80:
        raise SystemExit(f"last shot {tail:.2f}s over 3.80")
    return cuts


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "A FIFTH OF A", 96, int(W * 0.90), 8)
    y = int(H * 0.05)
    y += centred(d, y, "A FIFTH OF A", font, WHITE, 8)[3] - y + 8
    centred(d, y, "LIGHT-YEAR", font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["How Close Will", "Gliese 710 Come", "to the Sun?"]
    font = fit_font(d, "Gliese 710 Come", 58, int(W * 0.86), 5)
    gap = d.textbbox((0, 0), "Hg", font=font)[3] + 8
    block = gap * len(rows)
    y = BAND_Y0 + (BAND_H - block) // 2
    for row in rows:
        box = centred(d, y, row, font, WHITE, 5)
        if box[1] < BAND_Y0 or box[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"title outside the 16:9 band: {row} {box}")
        y += gap
    im.save(dest)


def card_frames(dest: Path, card_in: float, card_out: float) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    n = round((card_out - card_in) * FPS)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    font = fit_font(probe, "100 METERS AWAY", 64, int(W * 0.86), 6)
    text_h = probe.textbbox((0, 0), "Hg", font=font)[3]
    for i in range(n):
        t = card_in + i / FPS
        a = min(1.0, (t - card_in) / 0.35, (card_out - t) / 0.30)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        alpha = int(255 * max(0.0, a))
        label = "100 METERS AWAY"
        fill = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)
        y = BAND_Y0 + (BAND_H - text_h - 36) // 2
        box = centred(d, y, label, font, fill, 6)
        if box[1] < BAND_Y0 or box[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"card outside the 16:9 band: {box}")
        prog = min(1.0, max(0.0, (t - card_in) / 0.55))
        full = int(W * 0.62)
        left = (W - full) // 2
        bar_w = int(full * 0.82 * prog)
        by = box[3] + 10
        if bar_w > 4:
            d.rectangle((left, by, left + bar_w, by + 14), fill=fill)
            if by + 14 > BAND_Y0 + BAND_H:
                raise SystemExit("card bar outside the 16:9 band")
        im.save(dest / f"card_{i:04d}.png")
    return n


def caption_pngs(words: list[dict], total: float) -> list[dict]:
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["word"][-1:] in ".,?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    caps = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        stop = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(total, g[-1]["end"] + 0.35)
        if stop <= start:
            continue
        text = " ".join(w["word"].strip(",.?!") for w in g).upper()
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        font = fit_font(d, text, 54, int(W * 0.90), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_plate(src: Path, ss: float, length: float, dest: Path, vf: str, speed: float = 1.0) -> None:
    frames = max(1, round(length * FPS))
    if vf == "PITCH":
        # Soft vertical ramp so the pitch band is not a hard seam (polish_gate).
        run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.25:.3f}",
            "-i", str(src), "-an", "-filter_complex",
            "[0:v]split[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=26[bg];"
            "[b]rotate=0.09:ow=iw:oh=ih:c=black,scale=-2:1420,crop=1080:1420,format=rgba,"
            "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='clip(255*min(Y/220,(H-Y)/220),0,255)'[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,fps=30,format=yuv420p[v]",
            "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest),
        ])
        return
    if speed != 1.0:
        vf = vf.replace("fps=30", f"setpts=PTS/{speed:.3f},fps=30", 1)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length * speed + 0.30:.3f}",
         "-i", str(src), "-an", "-vf", vf,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def black_frac(path: Path, t: float = 0.04) -> float:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    pix = np.frombuffer(raw, dtype=np.uint8)
    return float(np.mean(pix[: 180 * 320] < 30))


def frame0_diff(path: Path) -> float:
    frames = []
    for t in (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5):
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(path), "-frames:v", "1",
            "-vf", "scale=72:128,format=gray", "-f", "rawvideo", "-",
        ])
        frames.append(np.frombuffer(raw, dtype=np.uint8)[: 72 * 128].astype(np.float32).reshape(128, 72))
    y0, y1 = int(128 * 0.28), int(128 * 0.72)
    bands = [f[y0:y1].ravel() for f in frames]
    steps = [float(np.mean(np.abs(a - b)) / 255 * 100) for a, b in zip(bands, bands[1:])]
    return min((steps[i] + steps[i + 1]) / 2 for i in range(len(steps) - 1))


def gray_frames(path: Path, ss: float, length: float) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", str(path),
        "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
    ])
    frames = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
    frames = frames[: frames.size - (frames.size % (320 * 180))]
    return frames.reshape(-1, 320, 180)


def loop_measures(video: Path) -> dict:
    length = dur(video)
    a = gray_frames(video, 0.04, 0.04)[0]
    b = gray_frames(video, max(0.0, length - 0.08), 0.04)[0]
    diff = np.abs(a - b)
    return {
        "whole": round(float(np.mean(diff)), 2),
        "masked": round(float(np.mean(diff[110:240])), 2),
    }


def lufs(path: Path) -> float:
    p = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True)
    line = [ln for ln in p.stderr.splitlines() if "I:" in ln and "LUFS" in ln]
    if not line:
        raise SystemExit(f"no LUFS from {path}")
    return float(line[-1].split("I:")[1].split("LUFS")[0].strip())


def check_words(marks: dict, cap_words: list[dict], total: float) -> None:
    spoken = " ".join(w["word"] for w in cap_words)
    low = spoken.lower()
    for banned in ("full film", "stay, and", "the latest gaia", "closest approach", "in this film", "60%"):
        if banned in low:
            raise SystemExit(f"banned or replaced line still in the stem: {banned}")
    for need in (
        "a fifth of a light-year",
        "one centimeter",
        "30 centimeters",
        "100 meters",
        "football pitch",
        "a ruler",
    ):
        if need not in low:
            raise SystemExit(f"distance line missing: {need}")
    if not low.startswith("gliese 710 passes"):
        raise SystemExit(f"sentence 1 does not open on Gliese 710 passes: {spoken[:80]}")
    if marks["Gliese"] > 0.15:
        raise SystemExit(f"first word at {marks['Gliese']}s")
    if marks["710"] > 1.15:
        raise SystemExit(f"710 ends its start at {marks['710']}s, need the name by 1.15")
    # The locked words "passes at about a" put "fifth" near 2.0 s, not 1.45 s.
    if marks["fifth"] > 2.20:
        raise SystemExit(f"fifth at {marks['fifth']}s, later than the locked words allow")
    if 9.0 <= marks["hundred"] <= 14.0:
        raise SystemExit(f"100 at {marks['hundred']}s is under the 9–14 s banner")
    if marks["hundred"] < 0.70 * total:
        raise SystemExit(f"100 at {marks['hundred']}s is before 70% ({0.70 * total:.2f})")
    if not (18.0 <= total <= 24.4):
        raise SystemExit(f"runtime {total}s outside 18–24")
    for prev, w in zip(cap_words, cap_words[1:]):
        gap = w["start"] - prev["end"]
        if gap > 0.22:
            raise SystemExit(f"pause {gap:.2f}s before {w['word']}")
    print("spoken", spoken, flush=True)


def main() -> None:
    for p in (VO_WAV, WORDS, BED, LAS, SDO, GAIA, PITCH):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    words_raw = json.loads(WORDS.read_text())
    src = read_wav(VO_WAV)
    audio, marks, cap_words = build_vo(src, words_raw)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    cuts = plan_cuts(cap_words, vo_end)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("cuts", cuts, "holds", [round(b - a, 2) for a, b in zip([0.0, *cuts], [*cuts, vo_end])], flush=True)
    check_words(marks, cap_words, total)
    card_in = round(max(14.15, marks["hundred"] - 0.15), 3)
    card_out = round(min(vo_end - 0.15, card_in + 3.50, marks["pitch"] + 1.10), 3)
    if card_out - card_in < 2.40:
        card_out = round(min(vo_end - 0.10, card_in + 3.20), 3)
    if not (card_in <= marks["hundred"] <= marks["meters"] <= card_out - 0.20):
        raise SystemExit(f"teach card {card_in}-{card_out} misses 100 meters {marks['hundred']}-{marks['meters']}")
    if card_in < 14.05:
        raise SystemExit("teach card overlaps the 9–14 s title")
    print("card", card_in, card_out, flush=True)
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    tail = np.zeros((int(round(LOOP * SR)), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    spoken = " ".join(w["word"] for w in cap_words)

    bounds = [0.0, *cuts, vo_end]
    holds = [round(b - a, 3) for a, b in zip(bounds, bounds[1:])]
    print("cutting frame 0", flush=True)
    f0_ss, f0_src, f0_title, f0_up, f0_vf = FRAME0
    cut_plate(f0_src, f0_ss, holds[0], WORK / "s00.mp4", f0_vf, speed=FRAME0_SPEED)
    blk = black_frac(WORK / "s00.mp4")
    motion = frame0_diff(WORK / "s00.mp4")
    print(f"frame0 black {blk:.3f} diff {motion:.2f}", flush=True)
    if blk > 0.30:
        raise SystemExit(f"frame 0 is {blk:.0%} black")
    if motion < 1.50:
        raise SystemExit(f"frame 0 diff {motion:.2f} under 1.50")

    # Shot 0 is frame 0. Later shots take PLATES in order, with the pitch
    # plate moved onto the shot that contains "football".
    body_n = len(holds) - 1
    if body_n > len(PLATES):
        raise SystemExit(f"{body_n} body shots and only {len(PLATES)} plates")
    chosen = list(PLATES[:body_n])
    foot_i = next(i for i, w in enumerate(cap_words) if w["word"].lower().startswith("football"))
    foot_t = cap_words[foot_i]["start"]
    foot_shot = next(i for i in range(body_n) if bounds[i + 1] <= foot_t < bounds[i + 2])
    pitch = next(p for p in PLATES if p[5] == "PITCH")
    # Don't leave two La Silla shots adjacent after the swap.
    chosen[foot_shot] = pitch
    for i in range(1, body_n):
        if chosen[i][1] == chosen[i - 1][1]:
            raise SystemExit(f"back-to-back plates at body shot {i}: {chosen[i][1].name}")

    rows = [{
        "row": "s01_sdo_surface",
        "timeline_in": 0.0, "timeline_out": holds[0],
        "source": f0_src.name, "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss, "speed": FRAME0_SPEED},
    }]
    lines = ["file 's00.mp4'"]
    for i, (ss, source, _title, up, video, vf) in enumerate(chosen):
        length = holds[i + 1]
        t0 = bounds[i + 1]
        print(f"cutting s{i+2:02d} {source.name} @{ss} {length}s", flush=True)
        cut_plate(source, ss, length, WORK / f"s{i+1:02d}.mp4", vf)
        lines.append(f"file 's{i+1:02d}.mp4'")
        rows.append({
            "row": f"s{i+2:02d}_{source.stem}",
            "timeline_in": round(t0, 3), "timeline_out": round(t0 + length, 3),
            "source": source.name, "upscale": up, "video": video,
            "framing": {"offset": ss},
        })

    print("cutting loop", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
         "-vf", "reverse,fps=30,format=yuv420p", "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
    lines.append("file 's_loop.mp4'")
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "loop_sdo_surface.mp4", "upscale": f0_up, "video": True,
        "framing": {"offset": f0_ss, "speed": FRAME0_SPEED},
    })
    (WORK / "list.txt").write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
         "-c", "copy", str(WORK / "picture.mp4")])

    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    print("card frames", card_in, card_out, flush=True)
    card_frames(WORK / "card", card_in, card_out)
    caps = caption_pngs(cap_words, vo_end)
    title_out = min(TITLE_OUT, max(TITLE_IN + 1.0, vo_end - 0.4))

    vo_path = WORK / "stem_vo.wav"
    vo_i = lufs(vo_path)
    bed_raw = WORK / "stem_bed_raw.wav"
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", str(BED),
         "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
    bed_gain = (vo_i - 20.0) - lufs(bed_raw)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
         "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.20,afade=t=out:st={max(0.1, total - 0.55):.3f}:d=0.45",
         str(WORK / "stem_bed.wav")])
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick), "-i", str(tick),
         "-filter_complex",
         f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0|0[w];"
         f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(card_in * 1000)}|{int(card_in * 1000)}[c];"
         f"[2:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(TITLE_IN * 1000)}|{int(TITLE_IN * 1000)}[t];"
         f"[w][c][t]amix=inputs=3:normalize=0,apad=whole_dur={total:.3f}[o]",
         "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
    sfx_gain = (vo_i - 18.0) - lufs(WORK / "stem_sfx_raw.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
         "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
         "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
         "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
         "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(WORK / "mix.wav")])

    final = OUT / f"{STEM}.mp4"
    ff_in = ["-i", str(WORK / "picture.mp4"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "hook.png"),
             "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(WORK / "title.png"),
             "-framerate", str(FPS), "-i", str(WORK / "card" / "card_%04d.png"),
             "-i", str(WORK / "mix.wav")]
    base = 5
    for c in caps:
        ff_in += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(c["png"])]
    fc = [
        f"[1:v]format=rgba,fade=t=out:st={HOOK_END - 0.20:.2f}:d=0.20:alpha=1[hk]",
        f"[0:v][hk]overlay=0:0:enable='lt(t,{HOOK_END})'[v1]",
        f"[2:v]format=rgba,fade=t=in:st={TITLE_IN}:d=0.20:alpha=1,fade=t=out:st={title_out - 0.20:.2f}:d=0.20:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='gte(t,{TITLE_IN})*lt(t,{title_out})'[v2]",
        f"[3:v]setpts=PTS-STARTPTS+{card_in}/TB,format=rgba[cd]",
        f"[v2][cd]overlay=0:0:enable='gte(t,{card_in})*lt(t,{card_out})':eof_action=pass[v3]",
    ]
    last = "v3"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    print("encoding", flush=True)
    run(["ffmpeg", "-y", "-v", "error", *ff_in, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "4:a", *shorts_encode_args(fps=FPS),
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(final)])

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x4", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x4", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.04", "-i", str(final), "-frames:v", "1",
         str(OUT / f"{STEM}_open.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "select='eq(n,0)+eq(n,7)+eq(n,30)+eq(n,60)+eq(n,90)',scale=270:480,tile=5x1",
         "-frames:v", "1", str(OUT / f"{STEM}_open_sheet.jpg")])

    cuts_path = OUT / "cuts_v02.json"
    pool_path = OUT / "pool_v02.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool = [
        {"file_id": f0_src.name, "title": f0_title},
        {"file_id": "loop_sdo_surface.mp4", "title": "Loop back to the NASA SDO sun"},
    ]
    seen = {f0_src.name, "loop_sdo_surface.mp4"}
    for _ss, source, title, _up, _video, _vf in chosen:
        if source.name in seen:
            continue
        seen.add(source.name)
        pool.append({"file_id": source.name, "title": title})
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    mix_lufs = lufs(WORK / "mix.wav")
    longest = max(holds)
    meta = {
        "job": "J0936",
        "version": "v02",
        "air": AIR,
        "youtube_id": VIDEO_ID,
        "related": LONG_ID,
        "planned_title": "How Close Will Gliese 710 Come to the Sun?",
        "replaces_for_review": "028_short_fri04_scale_v01 (scheduled jJ5LkFGyzLI). v01 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": round(dur(final), 3),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "bed": BED.name,
        "brief": {
            "frame_0": "NASA SDO sun, 9:16 centre crop, offset 23.0 s, played at 2.2x.",
            "frame_0_black": round(blk, 3),
            "frame_0_diff": round(motion, 2),
            "first_word_s": marks["Gliese"],
            "surprise_s": marks["fifth"],
            "subject_gliese_s": marks["Gliese"],
            "subject_710_s": marks["710"],
            "passes_s": marks["passes"],
            "first_cut_s": cuts[0],
            "last_word_to_loop_s": LOOP,
            "meta_promise": False,
            "payoff_number_s": marks["hundred"],
            "meters_s": marks["meters"],
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": mix_lufs,
            "runtime_s": total,
            "longest_plate_s": round(longest, 3),
            "fifth_note": (
                "Audit #16 asked for 'a fifth' by 1.45 s. The locked words "
                "'Gliese 710 passes at about a' take longer than that window, "
                "so fifth is as early as this take allows."
            ),
            "loop_sentence": (
                "The length of a football pitch. "
                "Gliese 710 passes at about a fifth of a light-year."
            ),
        },
        "long_title_on_screen": {
            "title": "How Close Will Gliese 710 Come to the Sun?",
            "from_s": TITLE_IN, "to_s": round(title_out, 3),
        },
        "long_in_description": {"title": LONG_TITLE, "id": LONG_ID},
        "hook": "A FIFTH OF A / LIGHT-YEAR (yellow LIGHT-YEAR), 0-2.0 s",
        "teach_card": f"100 METERS AWAY, inside the 16:9 band, {card_in}-{card_out} s",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", VIDEO_ID,
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(OUT / f"{STEM}_meta.json")],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout[-2500:], gate.stderr[-400:], flush=True)

    sfx = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_path), "--sfx", str(WORK / "stem_sfx.wav"),
         "--bed", str(WORK / "stem_bed.wav"), "--minutes", f"{total / 60:.3f}"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_sfx.txt").write_text(sfx.stdout + sfx.stderr)
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
         "--bed", str(BED), "--video", str(final)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_music.txt").write_text(music.stdout + music.stderr)
    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(cuts_path), "--out", str(OUT / "polish_gate_v02.json")],
        capture_output=True, text=True)
    (OUT / "polish_gate_v02.txt").write_text(polish.stdout + polish.stderr)
    pqa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(OUT / "picture_qa_v02")],
        capture_output=True, text=True)
    (OUT / "picture_qa_v02.txt").write_text(pqa.stdout + pqa.stderr)
    print("gate", gate.returncode, "sfx", sfx.returncode, "music", music.returncode,
          "polish", polish.returncode, "picture_qa", pqa.returncode, flush=True)
    print((sfx.stdout or sfx.stderr or "")[-500:], flush=True)
    print((music.stdout or music.stderr or "")[-700:], flush=True)
    print((polish.stdout or polish.stderr or "")[-500:], flush=True)
    print((pqa.stdout or pqa.stderr or "")[-900:], flush=True)
    raise SystemExit(0 if all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)) else 1)


if __name__ == "__main__":
    main()
