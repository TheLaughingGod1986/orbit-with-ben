#!/usr/bin/env python3
"""J0932 — 023 Short lift_95pct_wide v03. £0 local re-cut. No upload.

Scheduled v02 (YC65mdh6Hgg) stays untouched. This file is the next number up.

Keeps the locked opening ("Venus is ninety-five percent as wide as Earth").
Trims the 3.50–3.96 s pause to 0.15 s and the 6.06–6.88 s pause to 0.20 s.
Frame 0 is moving NASA SVS 14095 WISPR / Magellan 3rd flyby, cropped onto the
Venus limb (the full square is ~55% black). No end card. 1.0 s matched loop.
The v02 FOUR-FIFTHS MASS card stays, on that line.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

NAS = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben"
    "/02_Video-Projects/023_What-Happened-To-Venus"
)
VO_WAV = NAS / "02_Voiceover/venus_vo_v01.wav"
WORDS_JSON = FILM / "07_Edit-Project/full_rough_v05e_pack/venus_words_list.json"
BED = FILM / "05_Music/venus_score_bed_v01_full.mp3"
KIT = REPO / (
    "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
    "/06_Sound-Effects/compilation_kit_v01"
)
WISPR = NAS / "07_Edit-Project/nasa_pool_v01/harvest_v04/svs14095_WISPR_Magellan_3rdFlyby.mp4"
DAVINCI = NAS / "07_Edit-Project/nasa_pool_v01/harvest_v03/13887_DAVINCI_PEVAA.mp4"
AIA = NAS / "07_Edit-Project/nasa_pool_v01/sdo/AIA171VenusTransit_HD1080.mp4"
HMI = NAS / "07_Edit-Project/nasa_pool_v01/sdo/HMIVenusTransit_HD1080.mp4"
PARKER = NAS / (
    "07_Edit-Project/nasa_pool_v01/harvest_v04"
    "/svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4"
)
STEAM = NAS / "04_Generated-Clips/01_Raw/plates_v01/venus_ch3_plateB_steam_lid_v01.mp4"
OCEAN = NAS / "04_Generated-Clips/01_Raw/plates_v01/venus_ch3_plateA_ocean_nasa_v01.mp4"

WORK = Path("/private/tmp/j0932/work_venus_size_v03")
OUT = HERE / "06_Final-Exports"
STEM = "venus_95pct_wide_v03"
FINAL = OUT / f"{STEM}.mp4"
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / STEM
UAT_ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
) / STEM
AIR = "2026-11-02"
FPS = 30
SR = 48000
W, H = 1080, 1920
LOOP = 1.00
# Long-VO clock. Short t = long t - T0. "Venus" is at 46.98 (short 0.08).
T0 = 46.90
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
HOOK = [("95%", YELLOW), ("AS WIDE", WHITE)]
TITLE = ["What Happened", "to Venus?"]
# (long_start, long_end). The two named pauses are the gaps between these.
SEGMENTS = [
    (46.90, 50.40),   # Venus … Earth,
    (50.86, 52.96),   # with about four-fifths of its mass.
    (53.78, 69.04),   # It formed … closer to the sun.
]
GAPS = (0.15, 0.20)
# (file, src_in, crop or "", file_id, credit, upscale)
# Left 9:16 of the square WISPR limb (full-frame black ~55%), with a 48 px
# slide across 2.4 s so the centre band keeps moving. Upscale stays 1.85x.
WISPR_VF = (
    "crop=585:1040:'min(48,48*t/2.4)':0,"
    "scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
)
COVER_VF = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,setsar=1,format=yuv420p"
)
PLATES = [
    (WISPR, 0.05, WISPR_VF, "svs14095_WISPR_Magellan_3rdFlyby.mp4",
     "NASA SVS 14095 WISPR Magellan 3rd flyby, Venus limb", 1.85),
    (STEAM, 4.0, COVER_VF, "venus_ch3_plateB_steam_lid_v01.mp4",
     "Venus globe, steam-lid plate", 1.78),
    (DAVINCI, 100.0, COVER_VF, "13887_DAVINCI_PEVAA.mp4",
     "NASA SVS 13887 DAVINCI glowing Venus atmosphere", 1.78),
    (HMI, 24.4, COVER_VF, "HMIVenusTransit_HD1080.mp4",
     "NASA SDO HMI Venus transit of the Sun", 1.78),
    (PARKER, 192.4, COVER_VF, "svs14095_ParkerVenus.mp4",
     "NASA SVS 14095 Parker Venus surface", 1.78),
    (OCEAN, 8.4, COVER_VF, "venus_ch3_plateA_ocean_nasa_v01.mp4",
     "Venus globe plate", 1.78),
    (AIA, 24.4, COVER_VF, "AIA171VenusTransit_HD1080.mp4",
     "NASA SDO AIA 171 Venus transit of the Sun", 1.78),
]


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
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


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


def fade_edges(chunk: np.ndarray, n: int = 360) -> np.ndarray:
    chunk = chunk.copy()
    n = min(n, len(chunk) // 4)
    if n < 2:
        return chunk
    ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    chunk[:n] *= ramp
    chunk[-n:] *= ramp[::-1]
    return chunk


def build_vo() -> tuple[np.ndarray, list[dict], float]:
    words = json.loads(WORDS_JSON.read_text())
    room = pcm(VO_WAV, 50.50, 0.20)
    pieces: list[np.ndarray] = []
    cursor = 0.0
    spans = []
    for i, (a, b) in enumerate(SEGMENTS):
        chunk = fade_edges(pcm(VO_WAV, a, b - a))
        pieces.append(chunk)
        spans.append((a, b, cursor))
        cursor += len(chunk) / SR
        if i < len(SEGMENTS) - 1:
            g = GAPS[i]
            need = int(round(g * SR))
            pieces.append(np.resize(room, (need, 2)).astype(np.float32) * 0.35)
            cursor += g
    spoken = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        for a, b, new_a in spans:
            if a - 0.02 <= mid <= b + 0.02:
                spoken.append({
                    "word": w["text"],
                    "start": round(new_a + (w["start"] - a), 3),
                    "end": round(new_a + (w["end"] - a), 3),
                })
                break
    spoken.sort(key=lambda w: (w["start"], w["end"]))
    return np.concatenate(pieces, axis=0), spoken, cursor


def word_at(words: list[dict], text: str, which: int = 0) -> dict:
    hits = [w for w in words if w["word"].lower().rstrip(",.?!") == text.lower()]
    if not hits:
        raise SystemExit(f"missing word {text!r}")
    return hits[which]


def font_for(px: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, max(24, round(px)))


def centred(draw, y, text, font, fill, stroke=6):
    b = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (b[2] - b[0])) // 2 - b[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return list(draw.textbbox((x, y), text, font=font, stroke_width=stroke))


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(H * 0.085 / 0.72)
    while max(d.textlength(t, font=f) for t, _ in HOOK) > W * 0.86:
        f = ImageFont.truetype(FONT, f.size - 2)
    lh = d.textbbox((0, 0), "Hg", font=f)[3] + 18
    y = 220
    for t, c in HOOK:
        centred(d, y, t, f, c, stroke=7)
        y += lh
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H)
    while max(d.textlength(r, font=f) for r in TITLE) > W * 0.88:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - gap * len(TITLE)) // 2
    for r in TITLE:
        bb = centred(d, y, r, f, WHITE)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"title outside the 16:9 band: {r} {bb}")
        y += gap
    im.save(dest)


def card_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = [("FOUR-FIFTHS", YELLOW), ("MASS", WHITE)]
    f = font_for(LINE_H)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.86:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 16
    y = BAND_Y0 + (BAND_H - gap * len(rows)) // 2
    for t, c in rows:
        bb = centred(d, y, t, f, c)
        if bb[1] < BAND_Y0 or bb[3] > BAND_Y0 + BAND_H:
            raise SystemExit(f"card outside the 16:9 band: {t} {bb}")
        y += gap
    im.save(dest)


def caption_png(dest: Path, text: str) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font_for(LINE_H * 0.92)
    label = text.upper()
    while d.textlength(label, font=f) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    centred(d, BAND_Y0 + BAND_H + 56, label, f, WHITE, stroke=6)
    im.save(dest)


def caption_chunks(words: list[dict], vo_end: float) -> list[dict]:
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[,.?!]$", w["word"]):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        start = c[0]["start"]
        nxt = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else vo_end
        end = min(nxt, c[-1]["end"] + 0.35, vo_end)
        text = " ".join(w["word"] for w in c).rstrip(",.")
        out.append({"text": text, "s": round(start, 2), "e": round(max(start + 0.2, end), 2)})
    return out


def cut_plate(src: Path, ss: float, length: float, dest: Path, vf: str, reverse: bool = False) -> None:
    if reverse:
        vf = vf + ",reverse"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length:.3f}", "-i", src,
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p", "-r", str(FPS), dest,
    ])


def black_pct(video: Path, t: float = 0.08) -> float:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
        "-vf", "scale=96:170,format=rgb24", "-f", "rawvideo", "-",
    ])
    im = np.frombuffer(raw, dtype=np.uint8).reshape(170, 96, 3).astype(np.float32)
    return float((im.mean(axis=2) < 20).mean() * 100)


def loop_diff(video: Path) -> tuple[float, float]:
    def gray(t: float) -> np.ndarray:
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
            "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-",
        ])
        return np.frombuffer(raw, dtype=np.uint8).astype(np.float32).reshape(320, 180)
    a, b = gray(0.04), gray(max(0.0, dur(video) - 0.08))
    whole = float(np.mean(np.abs(a - b)))
    a[:70, :] = 0
    b[:70, :] = 0
    a[250:, :] = 0
    b[250:, :] = 0
    return whole, float(np.mean(np.abs(a - b)))


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (VO_WAV, WORDS_JSON, BED, WISPR, DAVINCI, AIA, HMI, PARKER, STEAM, OCEAN):
        if not p.exists() or p.stat().st_size < 1000:
            raise SystemExit(f"missing {p}")

    vo, words, vo_end = build_vo()
    total = vo_end + LOOP
    first = words[0]
    surprise = word_at(words, "ninety-five")
    fifths = word_at(words, "four-fifths")
    mass = word_at(words, "mass")
    second = word_at(words, "second")
    sun = words[-1]
    text = " ".join(w["word"] for w in words)
    low = text.lower()
    if "stay, and" in low or "full film" in low or "what happened" in low:
        raise SystemExit("a cut line survived the splice")
    if first["word"].lower() != "venus" or first["start"] > 0.15:
        raise SystemExit(f"first word late: {first}")
    if surprise["start"] > 1.50:
        raise SystemExit(f"ninety-five late: {surprise}")
    if not (18.0 <= total <= 24.0):
        raise SystemExit(f"length {total:.2f}s outside 18-24")
    if second["start"] / total < 0.70:
        raise SystemExit(f"second Earth at {second['start']:.2f} is under 70% of {total:.2f}")
    print(json.dumps({
        "vo_end": round(vo_end, 3), "total": round(total, 3),
        "first": first, "ninety_five": surprise["start"],
        "four_fifths": fifths["start"], "mass_end": mass["end"],
        "second": second["start"], "second_ratio": round(second["start"] / total, 3),
        "sun_end": sun["end"], "spoken": text,
    }, indent=2))

    first_cut = 2.50
    n_body = len(PLATES) - 1
    remain = vo_end - first_cut
    span = remain / n_body
    if not (2.8 <= span <= 3.8):
        raise SystemExit(f"body span {span:.2f}s from remain {remain:.2f}")
    if first_cut > 2.80:
        raise SystemExit("first cut late")
    cuts_t = [0.0, first_cut]
    t = first_cut
    for _ in range(n_body - 1):
        t += span
        cuts_t.append(round(t, 3))
    cuts_t.append(round(vo_end, 3))
    cuts_t.append(round(total, 3))
    for a, b in zip(cuts_t, cuts_t[1:]):
        if b - a > 3.80 + 0.02:
            raise SystemExit(f"plate {b - a:.2f}s too long ({a:.2f}-{b:.2f})")
    print("cuts", [round(x, 2) for x in cuts_t], "span", round(span, 2))

    card_in = round(max(2.40, fifths["start"] - 0.12), 3)
    card_out = round(min(card_in + 3.2, mass["end"] + 0.8, 8.6), 3)
    if card_out - card_in > 4.0 or card_in < 2.2 or card_out > 8.7:
        raise SystemExit(f"card window {card_in}-{card_out}")
    title_out = 14.0

    if "--vo-only" in sys.argv:
        return

    ov = WORK / "ov"
    ov.mkdir(exist_ok=True)
    hook_png(ov / "hook.png")
    title_png(ov / "title.png")
    card_png(ov / "card.png")
    chunks = caption_chunks(words, vo_end)
    for i, c in enumerate(chunks):
        caption_png(ov / f"cap_{i:02d}.png", c["text"])

    spans = list(zip(cuts_t, cuts_t[1:]))
    picture_spans = spans[:-1]
    if len(picture_spans) != len(PLATES):
        raise SystemExit(f"expected {len(PLATES)} plates, got {len(picture_spans)}")
    plates_dir = WORK / "plates"
    plates_dir.mkdir(exist_ok=True)
    seg_files = []
    for i, ((t0, t1), plate) in enumerate(zip(picture_spans, PLATES)):
        src, ss, vf, _name, _title, _up = plate
        dest = plates_dir / f"p{i:02d}.mp4"
        cut_plate(src, ss, t1 - t0, dest, vf)
        b = black_pct(dest)
        print(f"  plate {i} {t0:.2f}-{t1:.2f} from {ss:.2f}s black {b:.1f}%")
        if i == 0 and b > 30:
            raise SystemExit(f"frame 0 black {b:.1f}%")
        if b > 35:
            raise SystemExit(f"plate {i} black {b:.1f}%")
        if i == 0:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gso", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py")
            gso = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gso)
            dlt = gso.frame0_diff_0_1_5s(dest, t1 - t0)
            vis = gso.orbit_score(dest, 0.3)["visor_frac"]
            print(f"  frame0 diff {dlt:.2f} visor {vis:.4f}")
            if dlt < 1.50 or vis >= 0.003:
                raise SystemExit(f"frame 0 would fail the open gate (diff {dlt:.2f}, visor {vis:.4f})")
        seg_files.append(dest)
    tail = plates_dir / "wispr_limb_loop_v03.mp4"
    cut_plate(PLATES[0][0], PLATES[0][1], LOOP, tail, PLATES[0][2], reverse=True)
    seg_files.append(tail)

    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", "noise=alls=4:allf=t,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-r", str(FPS), "-an", picture])

    vo_stem = WORK / "stem_vo.wav"
    bed_stem = WORK / "stem_bed.wav"
    sfx_stem = WORK / "stem_sfx.wav"
    write_wav(vo_stem, vo)
    run(["ffmpeg", "-y", "-v", "error", "-i", vo_stem, "-af",
         f"apad,atrim=0:{total:.3f}", "-ac", "2", "-ar", str(SR), WORK / "stem_vo_pad.wav"])
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total:.3f},volume=0.06,afade=t=in:st=0:d=0.25,"
         f"afade=t=out:st={total - 0.4:.3f}:d=0.4", "-ac", "2", bed_stem])
    run(["ffmpeg", "-y", "-v", "error", "-i", KIT / "sfx_owb_whoosh_soft_v01.wav",
         "-i", KIT / "sfx_owb_tick_ui_v01.wav", "-filter_complex",
         f"[0:a]aresample=48000,volume=0.08,atrim=0:1.2[s0];"
         f"[1:a]aresample=48000,volume=0.06,adelay={int(card_in * 1000)}:all=1[tk];"
         f"[s0][tk]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:{total:.3f}[a]",
         "-map", "[a]", "-ac", "2", sfx_stem])

    mix_wav = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", WORK / "stem_vo_pad.wav", "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]",
         "-map", "[a]", "-ac", "2", "-ar", str(SR), mix_wav])
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", mix_wav, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = (
        f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", mix_wav, "-af", norm + ",aresample=48000",
         "-ac", "2", "-ar", str(SR), WORK / "mix_norm.wav"])

    args = ["ffmpeg", "-y", "-v", "error", "-i", picture]
    for p in (ov / "hook.png", ov / "title.png", ov / "card.png"):
        args += ["-loop", "1", "-i", str(p)]
    for i in range(len(chunks)):
        args += ["-loop", "1", "-i", str(ov / f"cap_{i:02d}.png")]
    args += ["-i", str(WORK / "mix_norm.wav")]
    fc = []
    lastv = "0:v"
    fc.append("[1:v]format=rgba[hk]")
    fc.append(f"[{lastv}][hk]overlay=enable='lt(t,2.2)'[v1]")
    lastv = "v1"
    fc.append("[2:v]format=rgba[tl]")
    fc.append(f"[{lastv}][tl]overlay=enable='between(t,9,{title_out:.2f})'[v2]")
    lastv = "v2"
    fc.append("[3:v]format=rgba[cd]")
    fc.append(f"[{lastv}][cd]overlay=enable='between(t,{card_in:.2f},{card_out:.2f})'[v3]")
    lastv = "v3"
    for i, c in enumerate(chunks):
        enable = f"between(t,{c['s']:.2f},{min(c['e'], vo_end - 0.15):.2f})"
        if not (c["e"] <= card_in or c["s"] >= card_out):
            if c["s"] >= card_in - 0.05 and c["e"] <= card_out + 0.05:
                enable = "lt(t,0)"
        outv = f"v{4 + i}"
        fc.append(f"[{4 + i}:v]format=rgba[cap{i}]")
        fc.append(f"[{lastv}][cap{i}]overlay=enable='{enable}'[{outv}]")
        lastv = outv
    audio_idx = 4 + len(chunks)
    run(args + [
        "-filter_complex", ";".join(fc), "-map", f"[{lastv}]", "-map", f"{audio_idx}:a",
        *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}", "-movflags", "+faststart", FINAL,
    ])

    whole, masked = loop_diff(FINAL)
    measured = lufs(FINAL)
    b0 = black_pct(FINAL, 0.06)
    print(f"loop_diff whole {whole:.2f} masked {masked:.2f} lufs {measured:.1f} dur {dur(FINAL):.2f} black {b0:.1f}")
    if masked > 15:
        raise SystemExit(f"loop_diff masked {masked:.2f} over 15")
    if b0 > 30:
        raise SystemExit(f"final frame 0 black {b0:.1f}%")

    cuts, pool = [], []
    for i, (t0, t1) in enumerate(picture_spans):
        _src, ss, _vf, name, title, up = PLATES[i]
        cuts.append({
            "row": f"s{i + 1:02d}",
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "source": name,
            "src_in": ss,
            "upscale": up,
            "video": True,
            "framing": {"offset": ss},
        })
        pool.append({"file_id": name, "title": title, "src_in": ss})
    cuts.append({
        "row": "s_loop",
        "timeline_in": round(vo_end, 3),
        "timeline_out": round(total, 3),
        "source": "wispr_limb_loop_v03.mp4",
        "src_in": 0.0,
        "upscale": 1.85,
        "video": True,
        "framing": {"offset": 0.05},
        "note": "1.0s reverse of the frame-0 WISPR limb, last frame equals frame 0",
    })
    pool.append({
        "file_id": "wispr_limb_loop_v03.mp4",
        "title": "NASA SVS 14095 WISPR Venus limb returned to frame 0",
        "src_in": 0.05,
    })
    meta = {
        "job": "J0932",
        "version": "v03",
        "youtube_id": "YC65mdh6Hgg",
        "replaces_for_review": "scheduled v02 YC65mdh6Hgg stays untouched",
        "air_date": AIR,
        "title_on_screen": "What Happened to Venus?",
        "related": "VBaYRPp85Sw",
        "file": str(FINAL.relative_to(REPO)),
        "sha256": sha256(FINAL),
        "duration_s": round(dur(FINAL), 2),
        "spoken": text,
        "words": words,
        "spend": "none",
        "frame_0_plate": "svs14095_WISPR_Magellan_3rdFlyby.mp4 left 9:16 crop of the Venus limb",
        "frame_0_note": (
            "The square WISPR 3rd-flyby frame is about 55% black. "
            "Frame 0 crops the left limb so Venus fills the 9:16 frame, "
            "then slides 48 px across 2.4 s so the centre band keeps moving."
        ),
        "brief": {
            "frame_0": "moving NASA SVS 14095 WISPR Magellan 3rd flyby, Venus limb, full-bleed, no Orbit",
            "first_word_s": first["start"],
            "surprise_s": surprise["start"],
            "surprise_word": "ninety-five",
            "first_cut_s": first_cut,
            "last_word_to_loop_s": round(total - sun["end"], 3),
            "meta_promise": False,
            "payoff_number_s": second["start"],
            "payoff_word": "second Earth",
            "hook_number_s": surprise["start"],
            "hook_number_word": "ninety-five",
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": round(whole, 2),
            "loop_diff_masked": round(masked, 2),
            "lufs": measured,
            "frame0_black_pct": round(b0, 1),
            "title_window_s": [9.0, title_out],
            "scale_window_s": [card_in, card_out],
            "scale_text": ["FOUR-FIFTHS", "MASS"],
            "pauses_trimmed": ["3.50-3.96 to 0.15", "6.06-6.88 to 0.20"],
        },
        "audio": {
            "vo": "023 locked venus_vo_v01.wav, pause-trimmed, no new TTS",
            "bed": "venus_score_bed_v01_full.mp3",
            "mix": "two-pass loudnorm -14 LUFS",
        },
        "cuts": cuts,
        "loop_sentence": "…closer to the sun. Venus is ninety-five percent as wide as Earth.",
    }
    (OUT / f"{STEM}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    (OUT / f"{STEM}_cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT / f"{STEM}_pool.json").write_text(json.dumps(pool, indent=2) + "\n")
    (WORK / "words.json").write_text(json.dumps(words, indent=2) + "\n")
    run(["ffmpeg", "-y", "-v", "error", "-i", FINAL, "-vf", "fps=2,scale=180:320,tile=8x4",
         "-frames:v", "1", OUT / f"{STEM}_2fps.jpg"])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0.04", "-i", FINAL, "-frames:v", "1",
         "-vf", "scale=168:298", OUT / f"{STEM}_PHONE.jpg"])
    stems = OUT / f"{STEM}_stems"
    stems.mkdir(exist_ok=True)
    for src, name in (
        (vo_stem, "stem_vo.wav"),
        (bed_stem, "stem_bed.wav"),
        (sfx_stem, "stem_sfx.wav"),
    ):
        run(["cp", src, stems / name])
    for dest_dir in (UAT_NAS, UAT_ICLOUD):
        dest_dir.mkdir(parents=True, exist_ok=True)
        for p in (
            FINAL, OUT / f"{STEM}_2fps.jpg", OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_meta.json",
        ):
            run(["cp", p, dest_dir / p.name])
    print("wrote", FINAL)


if __name__ == "__main__":
    main()
