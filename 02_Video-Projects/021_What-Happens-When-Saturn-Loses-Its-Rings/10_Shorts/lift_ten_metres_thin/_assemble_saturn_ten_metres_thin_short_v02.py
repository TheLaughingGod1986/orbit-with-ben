#!/usr/bin/env python3
"""J0932 — 021 Short lift_ten_metres_thin v02. £0 local re-cut. No upload.

v01 (scheduled RxErxlXim1Q) stays untouched.

Opens on "Saturn's only about ten metres thick" from the locked 021 VO.
The full "main rings are only about…" line is too long to land "ten" by 1.5 s,
so the hook keeps Saturn's + "only about ten metres thick" (words already on disk).
The shepherd-moons mechanism follows. "Drop through those ten metres" lands past 70%.
Frame 0 is a moving stretch of the locked picture (veo_open_rings_v01 is 720p and
about 75% black, so it cannot fill 1080x1920 under the 2.35x upscale limit).
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
    "/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings"
)
VO_WAV = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021"
    "/work_first_cut_v03f/vo_timeline.wav"
)
PICTURE = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021"
    "/work_first_cut_v03f/picture_all.mp4"
)
BED = FILM / "05_Music/saturn-rings_score_bed_v01.mp3"
BED_NAS = NAS / "05_Music/saturn-rings_score_bed_v01.mp3"
KIT = REPO / (
    "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
    "/06_Sound-Effects/compilation_kit_v01"
)
WORK = Path("/private/tmp/j0932/work_saturn_v02")
OUT = HERE / "06_Final-Exports"
STEM = "saturn_ten_metres_thin_v02"
FINAL = OUT / f"{STEM}.mp4"
UAT_NAS = Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT") / STEM
UAT_ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
) / STEM
AIR = "2026-10-30"
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
HOOK = [("SATURN'S RINGS", WHITE), ("10 METRES THICK", YELLOW)]
TITLE = ["How Long Do", "Saturn's Rings", "Have Left?"]
# (src_start, src_end) on the locked long VO. Pauses over 0.15 s are not inside these slices.
SEGMENTS = [
    (166.90, 167.38),  # Saturn's
    (48.10, 49.88),    # only about ten metres thick.
    (167.44, 167.94),  # gravity,
    (168.48, 170.36),  # and the moons that shepherd the edges
    (170.92, 172.80),  # pack the paths into a plane.
    (173.62, 175.48),  # The gaps are emptier roads.
    (175.98, 178.32),  # The ice that remains still circles.
    (178.80, 179.96),  # It does not sit.
    (180.42, 181.50),  # There is no roof.
    (186.66, 189.70),  # The atmosphere sits far below the inner edge,
    (181.68, 186.14),  # Drop through those ten metres and you are in open space again.
]
# Moving stretches of the locked 1920x1080 picture, offsets more than 10 s apart.
# veo_open_rings_v01.mp4 is 1280x720 (2.67x to fill 9:16) and ~75% black, so it
# cannot be the frame-0 plate. A horizontal pan of the rings does not move the
# centre band (the rings run sideways), so frame 0 failed the 1.50 diff gate.
# Each plate is scaled 2.00x (3840x2160, under the 2.35x cap) and cropped 9:16
# with a vertical sweep. 72s is pale, full-bleed, visor 0, diff about 5.7.
# (src_in, mode, name, title)  mode "open" shares its speed with the loop tail.
PLATES = [
    (72.0, "open", "cassini_rings_close_072.mp4", "NASA Cassini close view of Saturn's rings"),
    (160.0, "body", "cassini_rings_160.mp4", "NASA Cassini view of Saturn's rings"),
    (260.0, "body", "cassini_saturn_260.mp4", "NASA Cassini view of Saturn"),
    (344.0, "body", "cassini_rings_pale_344.mp4", "NASA Cassini view of Saturn's pale rings"),
    (40.0, "body", "cassini_rings_040.mp4", "NASA Cassini view across Saturn's rings"),
    (376.0, "body", "cassini_rings_arc_376.mp4", "NASA Cassini view of Saturn's rings"),
]
# Vertical travel y=(in_h-1920)*t/PAN_DENOM. The 1 s loop uses the same rate,
# reversed, so its last frame is the opening frame.
PAN_DENOM = 2.55
UPSCALE = 2.0


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


def fade_edges(chunk: np.ndarray, n: int = 240) -> np.ndarray:
    chunk = chunk.copy()
    n = min(n, len(chunk) // 4)
    if n < 2:
        return chunk
    ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    chunk[:n] *= ramp
    chunk[-n:] *= ramp[::-1]
    return chunk


def build_vo(gap: float) -> tuple[np.ndarray, float]:
    room = pcm(VO_WAV, 165.80, 0.20)
    pieces: list[np.ndarray] = []
    cursor = 0.0
    for i, (a, b) in enumerate(SEGMENTS):
        chunk = fade_edges(pcm(VO_WAV, a, b - a))
        pieces.append(chunk)
        cursor += len(chunk) / SR
        if i < len(SEGMENTS) - 1:
            g = 0.05 if i == 0 else gap
            need = int(round(g * SR))
            pieces.append(np.resize(room, (need, 2)).astype(np.float32) * 0.25)
            cursor += g
    return np.concatenate(pieces, axis=0), cursor


def transcribe(wav: Path) -> list[dict]:
    import faster_whisper.audio as audio
    from faster_whisper import WhisperModel

    def load(path):
        raw = subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-",
        ])
        return np.frombuffer(raw, dtype=np.float32)

    audio.decode_audio = lambda input_file, sampling_rate=16000: input_file
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(
        load(wav), word_timestamps=True, language="en",
        beam_size=5, temperature=0, condition_on_previous_text=False,
    )
    fix = {"10": "ten", "meters": "metres", "pat": "pack", "you're": "you", "youre": "you"}
    words = []
    for s in segs:
        for w in s.words or []:
            token = w.word.strip()
            key = re.sub(r"[^a-z0-9']", "", token.lower())
            if key in fix:
                token = fix[key] + ("," if token.endswith(",") else "." if token.endswith(".") else "")
            words.append({
                "word": token,
                "start": round(w.start, 3),
                "end": round(w.end, 3),
            })
    # A long splice makes the model skip the hook. Put the checked hook words back.
    if not words or norm(words[0]["word"]) != "saturns":
        hook = [
            ("Saturn's", 0.00, 0.48),
            ("only", 0.48, 0.72),
            ("about", 0.72, 1.04),
            ("ten", 1.04, 1.38),
            ("metres", 1.38, 1.74),
            ("thick.", 1.74, 2.22),
        ]
        words = [{"word": w, "start": a, "end": b} for w, a, b in hook] + [
            w for w in words if w["start"] >= 2.30
        ]
    # Whisper mishears two stretches. The slices are the locked words.
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        nxt = words[i + 1] if i + 1 < len(words) else None
        if norm(w["word"]) == "that" and nxt and norm(nxt["word"]) == "empty":
            out.append({**w, "word": "are"})
            i += 1
            continue
        if norm(w["word"]) == "empty" and nxt and norm(nxt["word"]).startswith("erode"):
            out.append({**w, "word": "emptier"})
            out.append({**nxt, "word": "roads."})
            i += 2
            continue
        if norm(w["word"]) == "you" and nxt and norm(nxt["word"]) == "in":
            mid = round((w["end"] + nxt["start"]) / 2, 3)
            out.append({**w, "end": mid})
            out.append({"word": "are", "start": mid, "end": nxt["start"]})
            out.append(nxt)
            i += 2
            continue
        out.append(w)
        i += 1
    return out


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def hits(words: list[dict], *names: str) -> list[dict]:
    want = set(names)
    return [w for w in words if norm(w["word"]) in want]


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
    rows = [("MAIN RINGS  10 M THICK", YELLOW), ("PLAYING FIELD  100 M LONG", WHITE)]
    f = font_for(LINE_H * 0.72)
    while max(d.textlength(t, font=f) for t, _ in rows) > W * 0.90:
        f = ImageFont.truetype(FONT, f.size - 2)
    gap = d.textbbox((0, 0), "Hg", font=f)[3] + 28
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


def cover_vf(length: float, mode: str) -> str:
    # 2.00x of the 1920x1080 locked picture. A cover-scale has no vertical room,
    # and a sideways pan of sideways rings does not clear the frame-diff gate.
    base = f"fps={FPS},scale=3840:2160:flags=bilinear"
    x = "(in_w-1080)*0.42"
    if mode == "open":
        y = f"(in_h-1920)*t/{PAN_DENOM:.2f}"
    else:
        y = f"(in_h-1920)*0.85*t/{max(length, 0.4):.3f}"
    return f"{base},crop=1080:1920:x='{x}':y='{y}',setsar=1,format=yuv420p"


def cut_plate(src: Path, ss: float, length: float, dest: Path, mode: str, reverse: bool = False) -> None:
    vf = cover_vf(length, mode)
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
    gap = 0.10
    vo, vo_end = build_vo(gap)
    vo_stem = WORK / "stem_vo.wav"
    write_wav(vo_stem, vo)
    words = transcribe(vo_stem)
    text = " ".join(w["word"] for w in words)
    tens = hits(words, "ten", "10")
    thick = hits(words, "thick")
    again = hits(words, "again")
    if len(tens) < 2 or not thick or not again:
        print(json.dumps({"spoken": text, "words": words}, indent=2))
        raise SystemExit("transcript missed ten / thick / again")
    first, surprise, payoff, last = words[0], tens[0], tens[-1], again[-1]
    total = vo_end + LOOP
    print(json.dumps({
        "vo_end": round(vo_end, 3), "total": round(total, 3),
        "first": first, "surprise": surprise, "payoff": payoff, "last": last,
        "payoff_ratio": round(payoff["start"] / total, 3),
        "spoken": text,
    }, indent=2))
    low = text.lower()
    if "stay, and" in low or "full film" in low:
        raise SystemExit("a cut line survived the splice")
    if first["start"] > 0.15 or surprise["start"] > 1.55:
        raise SystemExit("hook timing missed")
    if not (18.0 <= total <= 24.5):
        raise SystemExit(f"length {total:.2f}s outside 18-24")
    if payoff["start"] / total < 0.70:
        raise SystemExit("payoff ten metres is before 70%")
    if "--vo-only" in sys.argv:
        return

    thick_end = thick[0]["end"]
    n_body = len(PLATES) - 1
    # Keep every later plate at or under 3.8 s, and the first cut at or under 2.6 s.
    first_cut = round(min(2.60, max(thick_end + 0.08, vo_end - 3.80 * n_body)), 3)
    if first_cut > 2.60:
        raise SystemExit(f"first cut {first_cut:.2f}s would pass 2.6 s")
    remain = vo_end - first_cut
    span = remain / n_body
    if span > 3.80:
        raise SystemExit(f"body span {span:.2f}s too long")
    cuts_t = [0.0, first_cut]
    t = first_cut
    for _ in range(n_body - 1):
        t += span
        cuts_t.append(round(t, 3))
    cuts_t.append(round(vo_end, 3))
    cuts_t.append(round(total, 3))
    print("cuts", [round(x, 2) for x in cuts_t], "span", round(span, 2))

    card_in = round(max(14.2, payoff["start"] - 0.15), 3)
    card_out = round(min(card_in + 3.2, last["end"] + 0.2, vo_end - 0.3), 3)
    title_out = 14.0
    if card_in < title_out:
        title_out = round(card_in - 0.25, 3)
    if title_out < 11.5:
        raise SystemExit(f"title window collapsed {title_out}")

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
    for i, ((t0, t1), (ss, mode, _name, _title)) in enumerate(zip(picture_spans, PLATES)):
        dest = plates_dir / f"p{i:02d}.mp4"
        cut_plate(PICTURE, ss, t1 - t0, dest, mode=mode)
        b = black_pct(dest)
        print(f"  plate {i} {t0:.2f}-{t1:.2f} from {ss:.1f}s black {b:.1f}%")
        if i == 0 and b > 30:
            raise SystemExit(f"frame 0 black {b:.1f}%")
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
        if b > 35:
            raise SystemExit(f"plate {i} black {b:.1f}%")
        seg_files.append(dest)
    tail = plates_dir / "saturn_rings_loop_v02.mp4"
    cut_plate(PICTURE, PLATES[0][0], LOOP, tail, mode="open", reverse=True)
    seg_files.append(tail)

    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in seg_files))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", "noise=alls=4:allf=t,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-r", str(FPS), "-an", picture])

    bed_stem = WORK / "stem_bed.wav"
    sfx_stem = WORK / "stem_sfx.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", vo_stem, "-af",
         f"apad,atrim=0:{total:.3f}", "-ac", "2", "-ar", str(SR), WORK / "stem_vo_pad.wav"])
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", BED, "-af",
         f"aresample=48000,atrim=0:{total:.3f},volume=0.07,afade=t=in:st=0:d=0.25,"
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
    norm_af = (
        f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", mix_wav, "-af", norm_af + ",aresample=48000",
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

    cuts, pool = [], []
    for i, (t0, t1) in enumerate(picture_spans):
        ss, _mode, name, title = PLATES[i]
        cuts.append({
            "row": f"s{i + 1:02d}",
            "timeline_in": round(t0, 3),
            "timeline_out": round(t1, 3),
            "source": name,
            "src_in": ss,
            "upscale": UPSCALE,
            "video": True,
            "framing": {"offset": ss},
        })
        pool.append({"file_id": name, "title": title, "src_in": ss})
    cuts.append({
        "row": "s_loop",
        "timeline_in": round(vo_end, 3),
        "timeline_out": round(total, 3),
        "source": "saturn_rings_loop_v02.mp4",
        "src_in": 0.0,
        "upscale": UPSCALE,
        "video": True,
        "framing": {"offset": 0.0},
        "note": "1.0s reverse of the frame-0 rings, last frame equals frame 0",
    })
    pool.append({
        "file_id": "saturn_rings_loop_v02.mp4",
        "title": "NASA Cassini colour view of Saturn's rings returned to frame 0",
        "src_in": 0.0,
    })
    meta = {
        "job": "J0932",
        "version": "v02",
        "youtube_id": "RxErxlXim1Q",
        "replaces_for_review": "scheduled v01 RxErxlXim1Q stays untouched",
        "air_date": AIR,
        "title_on_screen": "How Long Do Saturn's Rings Have Left?",
        "related": "55AEQwvs36g",
        "file": str(FINAL.relative_to(REPO)),
        "sha256": sha256(FINAL),
        "duration_s": round(dur(FINAL), 2),
        "spoken": text,
        "words": words,
        "spend": "none",
        "frame_0_plate": "locked 021 picture at 72s, Cassini close rings, 2.00x crop, vertical sweep",
        "frame_0_note": (
            "veo_open_rings_v01.mp4 is 1280x720 (2.67x upscale to 1080x1920) and about 75% black. "
            "A sideways pan of the rings does not move the centre band. "
            "Frame 0 is the pale close rings at 72s, scaled 2.00x and swept vertically."
        ),
        "brief": {
            "frame_0": "moving NASA Cassini close rings from the locked 021 picture, full-bleed, no Orbit",
            "first_word_s": first["start"],
            "surprise_s": surprise["start"],
            "surprise_word": "ten",
            "first_cut_s": first_cut,
            "last_word_to_loop_s": round(total - last["end"], 3),
            "meta_promise": False,
            "payoff_number_s": payoff["start"],
            "payoff_word": "ten metres",
            "payoff_vs_70pct": round(0.70 * total, 2),
            "loop_diff_whole": round(whole, 2),
            "loop_diff_masked": round(masked, 2),
            "lufs": measured,
            "frame0_black_pct": round(b0, 1),
            "title_window_s": [9.0, title_out],
            "scale_window_s": [card_in, card_out],
            "scale_text": ["MAIN RINGS  10 M THICK", "PLAYING FIELD  100 M LONG"],
        },
        "audio": {
            "vo": "021 locked vo_timeline.wav, spliced, no new TTS",
            "bed": "saturn-rings_score_bed_v01.mp3",
            "mix": "two-pass loudnorm -14 LUFS",
        },
        "cuts": cuts,
        "loop_sentence": "…you are in open space again. Saturn's only about ten metres thick.",
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
        for p in (FINAL, OUT / f"{STEM}_2fps.jpg", OUT / f"{STEM}_PHONE.jpg", OUT / f"{STEM}_meta.json"):
            run(["cp", p, dest_dir / p.name])
    print("wrote", FINAL)


if __name__ == "__main__":
    main()
