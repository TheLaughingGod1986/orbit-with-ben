#!/usr/bin/env python3
"""J0932 c37 — 023 Short lift_two_hours v03. £0 local re-cut. No upload.

v01 (scheduled Jcuiy0a9BFI) and v02 stay untouched.

Opens on "Venus is hot enough to melt lead" from the locked 023 VO.
Cuts "Venus is the planet most like Earth" and "So what happened to it?".
Frame 0 is moving NASA SVS 13887 DAVINCI (glowing atmosphere), not the PIA00254 still.
Ends on "two hours." The v01 "NEARLY 1 KM / DEEP" card stays, on that line.
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
sys.path.insert(0, str(REPO / "scripts"))
from short_c37 import finish_scan, limiter, loop_from_open, loop_metrics, true_peak  # noqa: E402

NAS = Path("/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben") / FILM.name
# FILM.name is the slug; NAS tree keeps the full project folder name.
NAS = Path(
    "/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben"
    "/02_Video-Projects/023_What-Happened-To-Venus"
)
# The iCloud long WAV is dataless on this Mini (resource deadlock). This stem is the
# short's own locked VO, the same 0–23.5 s the word list times (J0232 pack).
VO_WAV = Path("/Users/benjaminoats/_desk/J0232-venus-short/vo_stem.wav")
WORDS_JSON = FILM / "07_Edit-Project/full_rough_v05e_pack/venus_words_list.json"
BED = FILM / "05_Music/venus_score_bed_v01_full.mp3"
BED_NAS = NAS / "05_Music/venus_score_bed_v01_full.mp3"
KIT = REPO / (
    "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
    "/06_Sound-Effects/compilation_kit_v01"
)
DAVINCI = NAS / "07_Edit-Project/nasa_pool_v01/harvest_v03/13887_DAVINCI_PEVAA.mp4"
PARKER = NAS / (
    "07_Edit-Project/nasa_pool_v01/harvest_v04"
    "/svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4"
)
AIA = NAS / "07_Edit-Project/nasa_pool_v01/sdo/AIA171VenusTransit_HD1080.mp4"
WORK = Path("/private/tmp/j0932/work_venus_v03")
OUT = HERE / "06_Final-Exports"
STEM = "venus_two_hours_v03"
FINAL = OUT / f"{STEM}.mp4"
UAT = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/venus_two_hours_v03")
AIR = "2026-10-29"
FPS = 30
SR = 48000
W, H = 1080, 1920
LOOP = 1.00
BAND_H = round(W * 9 / 16)
BAND_Y0 = (H - BAND_H) // 2
LINE_H = round(BAND_H * 0.115)
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 214, 0, 255)
HOOK = [("VENUS MELTS", WHITE), ("LEAD", YELLOW)]
TITLE = ["What Happened", "to Venus?"]
# (src_start, src_end) on the locked long VO. Setup and the agenda question are not here.
# Venus / is hot enough to melt lead / the air…deep / radar lines / two hours.
SEGMENTS = [
    (0.07, 0.51),      # Venus
    (13.49, 15.13),    # is hot enough to melt lead.
    (15.83, 19.01),    # The air presses down like the sea nearly a kilometer deep.
    (5.43, 8.77),      # This is the ground on Venus seen through the clouds by radar.
    (9.51, 10.19),     # Why radar?
    (10.75, 12.81),    # Because ordinary light cannot get through.
    (19.61, 23.53),    # No machine we have landed there could survive it for much more than two hours.
]
# Moving plates only. Times checked clear of burned-in SVS titles and Parker interviews.
# (file, src_in). Frame 0 is DAVINCI's glowing atmosphere (t=100).
# In-points stay inside one shot. Parker cuts to an interview just after 140s,
# and 156s is a still lander frame, so those are not used.
PLATES = [
    (DAVINCI, 100.0, "13887_DAVINCI_PEVAA.mp4", "NASA SVS 13887 DAVINCI glowing Venus atmosphere"),
    (PARKER, 133.0, "svs14095_ParkerVenus.mp4", "NASA SVS 14095 Parker Venus surface"),
    (PARKER, 180.0, "svs14095_ParkerVenus.mp4", "NASA SVS 14095 Parker spacecraft at Venus"),
    (DAVINCI, 16.55, "13887_DAVINCI_PEVAA.mp4", "NASA SVS 13887 DAVINCI probe approaching Venus"),
    (AIA, 15.0, "AIA171VenusTransit_HD1080.mp4", "NASA SDO AIA 171 Venus transit of the Sun"),
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


def build_vo(gap: float) -> tuple[np.ndarray, list[dict], float]:
    words = json.loads(WORDS_JSON.read_text())
    room = pcm(VO_WAV, 2.70, 0.20)
    pieces: list[np.ndarray] = []
    cursor = 0.0
    spans = []
    for i, (a, b) in enumerate(SEGMENTS):
        chunk = fade_edges(pcm(VO_WAV, a, b - a))
        pieces.append(chunk)
        spans.append((a, b, cursor))
        cursor += len(chunk) / SR
        if i < len(SEGMENTS) - 1:
            g = gap
            need = int(round(g * SR))
            pieces.append(np.resize(room, (need, 2)).astype(np.float32) * 0.2)
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


def word_at(words: list[dict], text: str) -> dict:
    hits = [w for w in words if w["word"].lower().rstrip(",.?!") == text.lower()]
    if not hits:
        raise SystemExit(f"missing word {text!r}")
    return hits[-1] if text.lower() == "venus" else hits[0]


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
    rows = [("NEARLY 1 KM", YELLOW), ("DEEP", WHITE)]
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


def cover_vf() -> str:
    return (
        f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},setsar=1,format=yuv420p"
    )


def cut_plate(src: Path, ss: float, length: float, dest: Path, reverse: bool = False) -> None:
    vf = cover_vf()
    if reverse:
        vf += ",reverse"
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
    # Mask the hook band and the caption band, same idea as the v06 Apophis measure.
    a[:70, :] = 0
    b[:70, :] = 0
    a[250:, :] = 0
    b[250:, :] = 0
    return whole, float(np.mean(np.abs(a - b)))


def ensure_bed() -> None:
    if BED.exists() and BED.stat().st_size > 100000:
        return
    if not BED_NAS.exists():
        raise SystemExit(f"missing score bed {BED_NAS}")
    BED.parent.mkdir(parents=True, exist_ok=True)
    run(["cp", "-n", BED_NAS, BED])


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    if not VO_WAV.exists():
        raise SystemExit(f"missing locked VO {VO_WAV}")
    ensure_bed()

    def sentence_gaps(ws: list[dict]) -> list[float]:
        out = []
        for w, nxt in zip(ws, ws[1:]):
            if str(w["word"])[-1:] in ".?!":
                out.append(round(nxt["start"] - w["end"], 3))
        return out

    chosen = None
    fallback = None
    for gap in (0.18, 0.16, 0.20, 0.14, 0.12):
        vo, words, vo_end = build_vo(gap)
        loop_len = min(1.50, max(1.00, round(18.02 - vo_end, 3)))
        total = vo_end + loop_len
        melt = word_at(words, "melt")
        two = word_at(words, "two")
        first = words[0]
        km = word_at(words, "kilometer")
        sg = sentence_gaps(words)
        ok = (
            first["start"] <= 0.15
            and melt["start"] <= 1.50
            and two["start"] / total >= 0.70
            and two["start"] >= 14.05
            and sg
            and max(sg) <= 0.205
            and 17.6 <= total <= 24.0
        )
        if not ok:
            continue
        pack = (gap, vo, words, vo_end, total, melt, two, first, km, loop_len, sg)
        if total >= 18.0:
            chosen = pack
            break
        fallback = fallback or pack
    if chosen is None:
        chosen = fallback
    if chosen is None:
        vo, words, vo_end = build_vo(0.16)
        loop_len = min(1.50, max(1.00, round(18.05 - vo_end, 3)))
        total = vo_end + loop_len
        print(json.dumps({
            "vo_end": round(vo_end, 3), "total": round(total, 3),
            "spoken": " ".join(w["word"] for w in words),
            "melt": word_at(words, "melt")["start"],
            "two": word_at(words, "two")["start"],
            "gaps": sentence_gaps(words),
            "first": words[0],
        }, indent=2))
        raise SystemExit("no gap lands melt, length and the two-hours payoff together")
    gap, vo, words, vo_end, total, melt, two, first, km, loop_len, sg = chosen
    text = " ".join(w["word"] for w in words)
    low = text.lower()
    if "what happened" in low or "most like" in low or "stay, and" in low:
        raise SystemExit("a cut line survived the splice")
    print(json.dumps({
        "gap": gap, "loop": loop_len, "sentence_gaps": sg,
        "vo_end": round(vo_end, 3), "total": round(total, 3),
        "first": first, "melt_s": melt["start"], "two_s": two["start"],
        "two_ratio": round(two["start"] / total, 3), "km_s": km["start"],
        "spoken": text,
    }, indent=2))

    # First cut on the breath after "lead." Four later plates, each 2.8–3.8 s.
    lead_end = word_at(words, "lead")["end"]
    first_cut = round(min(2.30, max(2.05, lead_end + 0.06)), 3)
    n_body = 4
    remain = vo_end - first_cut
    if remain > 3.8 * n_body:
        first_cut = round(min(2.30, first_cut + (remain - 3.8 * n_body)), 3)
        remain = vo_end - first_cut
    span = remain / n_body
    if not (2.8 <= span <= 3.8):
        raise SystemExit(f"body span {span:.2f}s from remain {remain:.2f} (vo_end {vo_end:.2f})")
    cuts_t = [0.0, round(first_cut, 3)]
    t = first_cut
    for i in range(n_body - 1):
        t += span
        cuts_t.append(round(t, 3))
    cuts_t.append(round(vo_end, 3))
    cuts_t.append(round(total, 3))
    for a, b in zip(cuts_t, cuts_t[1:]):
        if b - a > 3.80 + 0.02:
            raise SystemExit(f"plate {b - a:.2f}s too long ({a:.2f}-{b:.2f})")
    if cuts_t[1] > 2.30:
        raise SystemExit("first cut late")
    print("cuts", [round(x, 2) for x in cuts_t])

    card_in = round(max(2.40, km["start"] - 0.15), 3)
    card_out = round(min(card_in + 3.2, 8.6, km["end"] + 1.4), 3)
    if card_out > 8.7 or card_in < 2.2:
        raise SystemExit(f"km card hits the title or the open: {card_in}-{card_out}")

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

    # Five picture spans, then a 1.0 s reverse of the frame-0 plate so the last frame matches.
    spans = list(zip(cuts_t, cuts_t[1:]))
    picture_spans = spans[:-1]
    if len(picture_spans) != len(PLATES):
        raise SystemExit(f"expected {len(PLATES)} plates, got {len(picture_spans)} spans {cuts_t}")
    plates_dir = WORK / "plates"
    plates_dir.mkdir(exist_ok=True)
    seg_files = []
    for i, ((t0, t1), (src, ss, _name, _title)) in enumerate(zip(picture_spans, PLATES)):
        dest = plates_dir / f"p{i:02d}.mp4"
        if not (dest.exists() and dest.stat().st_size > 100_000):
            cut_plate(src, ss, t1 - t0, dest)
        b = black_pct(dest)
        print(f"  plate {i} {t0:.2f}-{t1:.2f} from {ss:.1f}s black {b:.1f}%")
        if i == 0 and b > 25:
            raise SystemExit(f"frame 0 black {b:.1f}%")
        if b > 32:
            raise SystemExit(f"plate {i} black {b:.1f}%")
        seg_files.append(dest)
    tail = plates_dir / "davinci_atmosphere_loop_v03.mp4"
    loop_from_open(seg_files[0], tail, n=int(round(loop_len * FPS)))
    seg_files.append(tail)

    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", "noise=alls=4:allf=t,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-r", str(FPS), "-an", picture])
    # Each plate's -t rounds long. The loop match is the last frame, so the
    # mix follows the picture instead of cutting that frame off.
    total = dur(picture)
    print(f"picture hold {total:.3f}s")

    vo_stem = WORK / "stem_vo.wav"
    bed_stem = WORK / "stem_bed.wav"
    sfx_stem = WORK / "stem_sfx.wav"
    write_wav(vo_stem, vo)
    # Pad the VO with the loop so the mix length is the picture.
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

    # Overlays: hook 0–2.2, title 9–14 but not over the payoff, card on the kilometer line, captions.
    title_out = 14.0
    if two["start"] < title_out:
        title_out = round(two["start"] - 0.3, 3)
    inputs = [picture, WORK / "stem_vo_pad.wav", bed_stem, sfx_stem, ov / "hook.png", ov / "title.png", ov / "card.png"]
    for i in range(len(chunks)):
        inputs.append(ov / f"cap_{i:02d}.png")
    fc = []
    last = "0:v"
    fc.append(f"[4:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=2.0:d=0.2:alpha=1[hk]")
    fc.append(f"[{last}][hk]overlay=enable='lt(t,2.2)'[v1]")
    last = "v1"
    fc.append(
        f"[5:v]format=rgba,fade=t=in:st=9:d=0.25:alpha=1,fade=t=out:st={title_out - 0.25:.2f}:d=0.25:alpha=1[tl]"
    )
    fc.append(f"[{last}][tl]overlay=enable='between(t,9,{title_out:.2f})'[v2]")
    last = "v2"
    fc.append(
        f"[6:v]format=rgba,fade=t=in:st={card_in:.2f}:d=0.35:alpha=1,"
        f"fade=t=out:st={card_out - 0.35:.2f}:d=0.35:alpha=1[cd]"
    )
    fc.append(f"[{last}][cd]overlay=enable='between(t,{card_in:.2f},{card_out:.2f})'[v3]")
    last = "v3"
    for i, c in enumerate(chunks):
        idx = 7 + i
        nxt = f"c{i}"
        # Captions stay off the kilometer card and off the last 0.4 s (loop match).
        enable = f"between(t,{c['s']:.2f},{c['e']:.2f})"
        if c["s"] < card_out and c["e"] > card_in:
            enable = f"between(t,{c['s']:.2f},{min(c['e'], card_in):.2f})"
            if c["e"] <= card_in + 0.05:
                enable = "lt(t,0)"
        fc.append(f"[{idx}:v]format=rgba[{nxt}]")
        out = f"v{4 + i}"
        fc.append(f"[{last}][{nxt}]overlay=enable='{enable}'[{out}]")
        last = out
    fc.append("[1:a][2:a][3:a]amix=inputs=3:duration=first:normalize=0[mix]")
    args = ["ffmpeg", "-y", "-v", "error"]
    for p in inputs:
        args += ["-i", str(p)]
    # Loudnorm print pass is separate so a filter this long stays readable.
    mix_wav = WORK / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", WORK / "stem_vo_pad.wav", "-i", bed_stem, "-i", sfx_stem,
         "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]",
         "-map", "[a]", "-ac", "2", "-ar", str(SR), mix_wav])
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", mix_wav, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    norm = limiter(
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", mix_wav, "-af", norm + ",aresample=48000",
         "-ac", "2", "-ar", str(SR), WORK / "mix_norm.wav"])
    # Picture overlays, then the normalised mix. PNGs loop or they last one frame.
    args = ["ffmpeg", "-y", "-v", "error", "-i", picture]
    for p in (ov / "hook.png", ov / "title.png", ov / "card.png"):
        args += ["-loop", "1", "-i", str(p)]
    for i in range(len(chunks)):
        args += ["-loop", "1", "-i", str(ov / f"cap_{i:02d}.png")]
    args += ["-i", str(WORK / "mix_norm.wav")]
    # Rebuild filter with picture as 0 and overlays starting at 1. Audio is the last input.
    fc2 = []
    last = "0:v"
    n_ov = 3 + len(chunks)
    # inputs: 0 picture, 1 hook, 2 title, 3 card, 4.. captions, last audio
    fc2.append("[1:v]format=rgba[hk]")
    fc2.append(f"[{last}][hk]overlay=enable='lt(t,2.2)'[v1]")
    last = "v1"
    fc2.append("[2:v]format=rgba[tl]")
    fc2.append(f"[{last}][tl]overlay=enable='between(t,9,{title_out:.2f})'[v2]")
    last = "v2"
    fc2.append("[3:v]format=rgba[cd]")
    fc2.append(f"[{last}][cd]overlay=enable='between(t,{card_in:.2f},{card_out:.2f})'[v3]")
    last = "v3"
    for i, c in enumerate(chunks):
        enable = f"between(t,{c['s']:.2f},{min(c['e'], vo_end - 0.15):.2f})"
        if not (c["e"] <= card_in or c["s"] >= card_out):
            # Drop captions that would sit on the kilometer card.
            if c["s"] >= card_in - 0.05 and c["e"] <= card_out + 0.05:
                enable = "lt(t,0)"
        out = f"v{4 + i}"
        fc2.append(f"[{4 + i}:v]format=rgba[cap{i}]")
        fc2.append(f"[{last}][cap{i}]overlay=enable='{enable}'[{out}]")
        last = out
    audio_idx = 1 + n_ov
    run(args + [
        "-filter_complex", ";".join(fc2), "-map", f"[{last}]", "-map", f"{audio_idx}:a",
        *shorts_encode_args(fps=FPS), "-t", f"{total:.3f}", "-movflags", "+faststart", FINAL,
    ])

    metrics = finish_scan(FINAL, loop_metrics(FINAL))
    whole, masked = metrics["whole"], metrics["loop_diff_masked"]
    measured = lufs(FINAL)
    peak = true_peak(FINAL)
    b0 = black_pct(FINAL, 0.06)
    print(f"loop_diff whole {whole:.2f} masked {masked:.2f} lufs {measured:.1f} tp {peak:.2f} dur {dur(FINAL):.2f} black {b0:.1f}")
    if peak > -1.0:
        raise SystemExit(f"true peak {peak:.2f} dBTP")

    cuts = []
    pool = []
    for i, (t0, t1) in enumerate(picture_spans):
        _src, ss, name, title = PLATES[i]
        cuts.append({
            "row": f"s{i + 1:02d}",
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "source": name,
            "src_in": ss,
            "upscale": 1.78,
            "video": True,
            "framing": {"offset": ss},
        })
        pool.append({"file_id": name, "title": title, "src_in": ss})
    cuts.append({
        "row": "s_loop",
        "timeline_in": round(vo_end, 3),
        "timeline_out": round(total, 3),
        "source": "davinci_atmosphere_loop_v03.mp4",
        "src_in": 0.0,
        "upscale": 1.78,
        "video": True,
        "framing": {"offset": 0.0},
        "note": "1.0s reverse of the frame-0 atmosphere, last frame equals frame 0",
    })
    pool.append({
        "file_id": "davinci_atmosphere_loop_v03.mp4",
        "title": "NASA SVS 13887 DAVINCI atmosphere returned to frame 0",
        "src_in": 0.0,
    })
    meta = {
        "job": "J0932",
        "version": "v03",
        "youtube_id": "Jcuiy0a9BFI",
        "replaces_for_review": "scheduled v01 Jcuiy0a9BFI stays untouched",
        "air_date": AIR,
        "title_on_screen": "What Happened to Venus?",
        "related": "VBaYRPp85Sw",
        "file": str(FINAL.relative_to(REPO)),
        "sha256": sha256(FINAL),
        "duration_s": round(dur(FINAL), 2),
        "spoken": text,
        "words": words,
        "spend": "none",
        "frame_0_plate": "13887_DAVINCI_PEVAA.mp4 at 100s, glowing atmosphere, full-bleed",
        "brief": {
            "frame_0": "moving NASA SVS 13887 DAVINCI atmosphere, full-bleed, no Orbit",
            "first_word_s": first["start"],
            "surprise_s": melt["start"],
            "surprise_word": "melt",
            "first_cut_s": first_cut,
            "last_word_to_loop_s": round(total - word_at(words, "hours")["end"], 3),
            "meta_promise": False,
            "payoff_number_s": two["start"],
            "payoff_word": "two hours",
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": round(whole, 2),
            "loop_diff_masked": round(masked, 2),
            "lufs": measured,
            "frame0_black_pct": round(b0, 1),
            "title_window_s": [9.0, title_out],
            "scale_window_s": [card_in, card_out],
            "scale_text": ["NEARLY 1 KM", "DEEP"],
        },
        "audio": {
            "vo": "023 locked venus_vo_v01.wav, spliced, no new TTS",
            "bed": "venus_score_bed_v01_full.mp3",
            "mix": "two-pass loudnorm -14 LUFS",
        },
        "cuts": cuts,
        "loop_sentence": "…for much more than two hours. Venus is hot enough to melt lead.",
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
    UAT.mkdir(parents=True, exist_ok=True)
    for p in (
        FINAL, OUT / f"{STEM}_2fps.jpg", OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_meta.json",
    ):
        run(["cp", p, UAT / p.name])
    print("wrote", FINAL)


if __name__ == "__main__":
    main()
