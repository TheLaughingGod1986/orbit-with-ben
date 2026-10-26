#!/usr/bin/env python3
"""J0935 — 025 Thu 12 Nov length-test Short v02. £0 local re-cut of N42gKBbD7tE. No upload.

Audit #8 / Chief ruling: keep the ~54 s length-test story. Lead with
"Martian wind … swept its panels clean" so "wind" is by 1.5 s. Open on moving
Gale footage instead of the PIA22909 still (PIA26673 is mon09 v02's frame 0).
First cut 2.50 s, later plates under 3.8 s, no end card, 1.0 s matched loop.

Words come from the locked long VO already on disk. v01 is not overwritten.
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

POOL = FILM / "07_Edit-Project/nasa_pool_v01"
LONG_WAV = Path("/private/tmp/j0935_wed11_v03/long.wav")
LONG_WORDS = FILM / "02_Voiceover/words.json"
STILLS = Path("/tmp/j0935_thu12_stills")
BED = FILM / "05_Music/mars-robot_score_bed_v02_full.mp3"
KIT = FILM / "06_Sound-Effects/kit_v01"
BED_FROM = 180.0

OUT = HERE / "06_Final-Exports"
WORK = Path("/private/tmp/j0935_thu12_v02")
STEM = "thu12_length_test_dust_v02"

W, H, FPS = 1080, 1920, 30
SR = 48000
AIR = "2026-11-12"
LONG_TITLE = "Could a Robot Survive on Mars?"
LONG_ID = "Js6EQJ8qDi8"
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
YELLOW = (255, 214, 0, 255)
WHITE = (255, 255, 255, 255)
HOOK = ("THE", "WIND")
HOOK_END = 2.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
FIRST_CUT = 2.50
MAX_PLATE = 3.70
LOOP = 1.00
XFADE = 0.012

# (start, end, gap_before) on the locked long. The 0.40 s pause before "swept"
# is cut. "Why does dust matter…" after "turning off." stays out.
CLIPS = [
    (258.88, 261.26, 0.00),  # Martian wind and passing dust devils
    (261.54, 263.02, 0.06),  # swept its panels clean.
    (254.74, 256.96, 0.10),  # Opportunity should have starved within months.
    (257.28, 258.86, 0.10),  # Instead, again and again,
    (263.68, 306.90, 0.10),  # The team … the sky turning off.
]
MARKS = {
    "Martian": (0, 258.94),
    "wind": (0, 259.42),
    "clean_end": (1, 262.98),
    "fourteen": (4, 273.42),
    "off_end": (4, 306.82),
}

GALE = POOL / "gale_desert/JPL-20200303-MSLf-0001.mp4"
EDL = POOL / "launch_edl/JPL-20210222-M2020f-0001.mp4"
GIF = POOL / "dusk_plain/PIA26673.gif"
GALE_NAME = "JPL-20200303-MSLf-0001.mp4"
EDL_NAME = "JPL-20210222-M2020f-0001.mp4"
EDL_VF = "crop=495:880:712:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"

def gale_vf(ss: float) -> str:
    """Crops wed11 v03 already cleared of panorama gutters."""
    if ss < 30:
        x = 656
    elif ss < 50:
        x = 1200
    elif ss < 110:
        x = 80
    else:
        x = 1100
    return f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"

# Frame 0 is the descent at 154 s (f0diff 4.5). Gale at 58 s looked still
# (f0diff 0.25) and the gate missed the cut. Gale 19.7 s is the first cut.
# Windows are the ones wed11 v03 cleared. Stills are held, not panned.
# No still-to-still. Open offset 154 s is not used again.
BODY = [
    ("gale", 19.7),
    ("still", "PIA18079"),
    ("edl", 96.0),
    ("still", "PIA17759"),
    ("gale", 70.0),
    ("still", "PIA22520"),
    ("edl", 124.0),
    ("still", "PIA06739"),
    ("gif", 0.0),
    ("still", "PIA07372"),
    ("gale", 58.0),
    ("still", "PIA17956"),
    ("gale", 42.0),
    ("gale", 130.0),
]
OPEN_SS = 154.0

TITLES = {
    GALE_NAME: "Curiosity Gale panorama, moving",
    EDL_NAME: "Perseverance descent, moving",
    "PIA26673.gif": "Curiosity dusk clouds, moving",
    "PIA18079.jpg": "Opportunity solar panels after a cleaning event",
    "PIA07458.jpg": "Spirit dust devils on the plain",
    "PIA17759.jpg": "Opportunity self-portrait on Mars",
    "PIA22520.jpg": "Curiosity view of the 2018 dust storm",
    "PIA22330.jpg": "Mars surface after the dust storm",
    "PIA06739.jpg": "Opportunity shadow on the Martian ground",
    "PIA07372.jpg": "Opportunity self-portrait on the plain",
    "PIA22928.jpg": "Opportunity tracks on Mars",
    "PIA17956.jpg": "Opportunity shadow on a Martian slope",
}


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


def centred(draw, y, text, font, fill, stroke) -> int:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2 - box[0]
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return box[3] - box[1]


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2 or w.getsampwidth() != 2:
            raise SystemExit(f"expected 48 kHz stereo s16, got {path}")
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


def build_vo(src: np.ndarray, words: list) -> tuple[np.ndarray, dict[str, float], list[dict]]:
    fade_n = int(XFADE * SR)
    parts: list[np.ndarray] = []
    starts: list[float] = []
    cursor = 0
    cap_words: list[dict] = []
    room = src[int(263.15 * SR): int(263.40 * SR)]
    for i, (a, b, gap) in enumerate(CLIPS):
        if gap > 0:
            need = int(gap * SR)
            tone = np.resize(room, (need, 2)).astype(np.float32) * 0.35
            parts.append(tone)
            cursor += need
        clip = src[int(a * SR): int(b * SR)].copy()
        if i and fade_n > 8 and parts:
            n = min(fade_n, len(parts[-1]) // 2, len(clip) // 2)
            ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
            parts[-1][-n:] *= (1 - ramp)
            clip[:n] *= ramp
            parts[-1][-n:] += clip[:n]
            clip = clip[n:]
            cursor -= n
        starts.append(cursor / SR)
        for w in words:
            ws, we = float(w["start"]), float(w["end"])
            if a - 0.02 <= ws and we <= b + 0.04:
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
        a = CLIPS[seg][0]
        marks[name] = round(starts[seg] + (src_t - a), 3)
    return audio, marks, cap_words


def hook_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = fit_font(d, "WIND", 168, int(W * 0.86), 8)
    y = int(H * 0.05)
    y += centred(d, y, HOOK[0], font, WHITE, 8) + 8
    centred(d, y, HOOK[1], font, YELLOW, 8)
    im.save(dest)


def title_png(dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = ["Could a Robot", "Survive on Mars?"]
    font = fit_font(d, max(rows, key=len), 78, int(W * 0.88), 5)
    y = int(H * 0.08)
    for row in rows:
        y += centred(d, y, row, font, WHITE, 5) + 12
    im.save(dest)


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
        font = fit_font(d, text, 64, int(W * 0.72), 6)
        centred(d, int(H * 0.78), text, font, WHITE, 6)
        p = WORK / f"cap_{i:02d}.png"
        im.save(p)
        caps.append({"text": text, "s": round(start, 3), "e": round(stop, 3), "png": p})
    return caps


def cut_video(src: Path, ss: float, length: float, vf: str, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{length + 0.20:.3f}",
         "-i", str(src), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def cut_gif(length: float, dest: Path) -> None:
    frames = max(1, round(length * FPS))
    vf = ("crop=576:1024:224:0,scale=1152:2048:flags=lanczos,"
          "minterpolate=fps=30:mi_mode=blend,"
          "crop=1080:1920:x='8+18*t':y='8+16*t',fps=30,setsar=1,format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-ignore_loop", "0", "-i", str(GIF), "-an",
         "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])


def still_window(path: Path) -> tuple[int, int, int, int, int, float]:
    im = Image.open(path)
    w, h = im.size
    ch = h
    cw = int(round(ch * 9 / 16))
    if cw > int(w * 0.90):
        cw = int(w * 0.86)
        ch = min(h, int(round(cw * 16 / 9)))
        cw = int(round(ch * 9 / 16))
    up = 1080 / cw
    if up > 2.30:
        raise SystemExit(f"{path.name} upscale {up:.2f} over 2.30")
    x0 = max(0, (w - cw) // 2)
    pan = 0
    y0 = max(0, (h - ch) // 2)
    return x0, y0, cw, ch, pan, round(up, 3)


def cut_still(path: Path, length: float, dest: Path) -> float:
    x0, y0, cw, ch, pan, up = still_window(path)
    frames = max(1, round(length * FPS))
    vf = (
        f"crop={cw}:{ch}:x='{x0}+{pan}*t/{length:.3f}':y={y0},"
        f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    )
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS),
         "-i", str(path), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", "-frames:v", str(frames), str(dest)])
    return up


def gray_frame_n(path: Path, n: int) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path),
        "-vf", f"select=eq(n\\,{n}),scale=180:320,format=gray",
        "-frames:v", "1", "-f", "rawvideo", "-"])
    frame = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
    return frame[: 320 * 180].reshape(320, 180)


def loop_measures(video: Path) -> dict:
    n = int(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(video)], text=True).strip())
    a = gray_frame_n(video, 0)
    b = gray_frame_n(video, max(0, n - 1))
    diff = np.abs(a - b)
    return {
        "whole": round(float(np.mean(diff)), 2),
        "masked": round(float(np.mean(diff[110:240])), 2),
        "frames": n,
    }


def _scaled(im: Image.Image, alpha: float) -> Image.Image:
    if alpha >= 0.99:
        return im
    r, g, b, a = im.split()
    a = a.point(lambda p, k=alpha: int(p * k))
    return Image.merge("RGBA", (r, g, b, a))


def _paste(base: Image.Image, layer: Image.Image, alpha: float = 1.0) -> None:
    piece = _scaled(layer, alpha)
    box = piece.getbbox()
    if not box:
        return
    crop = piece.crop(box)
    base.paste(crop, box[:2], crop)


def burn_picture(picture: Path, mix: Path, caps: list[dict], total: float, dest: Path) -> None:
    """Draw the hook, title and captions in Python and encode once.

    This ffmpeg has no drawtext or libass. One overlay input per caption line
    (about 50) stalled the mux in swap on 26 Oct. Pasting the live line onto
    each frame keeps a single encode.
    """
    hook = Image.open(WORK / "hook.png").convert("RGBA")
    title = Image.open(WORK / "title.png").convert("RGBA")
    layers = [(c["s"], c["e"], Image.open(c["png"]).convert("RGBA")) for c in caps]
    frame_bytes = W * H * 3
    dec = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(picture), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", str(mix), "-map", "0:v", "-map", "1:a", *shorts_encode_args(fps=FPS),
         "-shortest", str(dest)],
        stdin=subprocess.PIPE)
    assert dec.stdout is not None and enc.stdin is not None
    i = 0
    try:
        while True:
            raw = dec.stdout.read(frame_bytes)
            if len(raw) < frame_bytes:
                break
            im = Image.frombytes("RGB", (W, H), raw)
            t = i / FPS
            if t < HOOK_END:
                fade = 1.0 if t < HOOK_END - 0.20 else (HOOK_END - t) / 0.20
                _paste(im, hook, fade)
            if TITLE_IN <= t < TITLE_OUT:
                inn = 1.0 if t > TITLE_IN + 0.20 else (t - TITLE_IN) / 0.20
                out = 1.0 if t < TITLE_OUT - 0.20 else (TITLE_OUT - t) / 0.20
                _paste(im, title, min(inn, out))
            for s, e, layer in layers:
                if s <= t < e:
                    _paste(im, layer)
                    break
            enc.stdin.write(im.tobytes())
            i += 1
            if i % 300 == 0:
                print(f"burn {i}", flush=True)
    finally:
        enc.stdin.close()
        dec.stdout.close()
        dec.wait()
    print(f"burned {i} frames", flush=True)
    code = enc.wait()
    if code != 0:
        raise SystemExit(f"encode failed ({code})")


def lufs(path: Path) -> float:
    p = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
        capture_output=True, text=True)
    line = [ln for ln in (p.stderr or "").splitlines() if "I:" in ln and "LUFS" in ln]
    if not line:
        raise SystemExit(f"no LUFS from {path}\n{(p.stderr or '')[-500:]}")
    return float(line[-1].split("I:")[1].split("LUFS")[0].strip())


def main() -> None:
    if not LONG_WAV.exists():
        raise SystemExit(f"missing locked long VO {LONG_WAV}. No new TTS.")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    for kind, spec in [("gale", None), ("edl", None), ("gif", None)]:
        pass
    for src in (GALE, EDL, GIF):
        if not src.exists():
            raise SystemExit(f"missing plate {src}")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    src = read_wav(LONG_WAV)
    words = json.loads(LONG_WORDS.read_text())["words"]
    audio, marks, cap_words = build_vo(src, words)
    vo_end = round(len(audio) / SR, 3)
    total = round(vo_end + LOOP, 3)
    spoken = " ".join(w["word"] for w in cap_words)
    print("marks", json.dumps(marks), "vo_end", vo_end, "total", total, flush=True)
    print("spoken", spoken, flush=True)
    if marks["Martian"] > 0.15:
        raise SystemExit(f"first word at {marks['Martian']}s, need ≤0.15")
    if marks["wind"] > 1.50:
        raise SystemExit(f"wind at {marks['wind']}s, need ≤1.50")
    if marks["Martian"] > 2.50:
        raise SystemExit(f"Martian at {marks['Martian']}s, need ≤2.50")
    if 9.0 <= marks["fourteen"] < 14.0:
        raise SystemExit(f"fourteen at {marks['fourteen']}s lands under the 9–14 s title")
    payoff_at = 0.70 * total
    if marks["fourteen"] < payoff_at:
        print(f"NOTE fourteen at {marks['fourteen']}s is before 70% ({payoff_at:.2f}s); "
              "ruling keeps the story order and fixes the opening only", flush=True)
    if not (50.0 <= total <= 60.5):
        raise SystemExit(f"runtime {total}s outside the 50–60 s length test")
    tail_gap = total - marks["off_end"]
    if tail_gap > 1.50:
        raise SystemExit(f"last word to loop {tail_gap:.2f}s over 1.5")
    tail = np.zeros((int(LOOP * SR), 2), np.float32)
    write_wav(WORK / "stem_vo.wav", np.concatenate([audio, tail], axis=0))
    (WORK / "vo_marks.json").write_text(json.dumps({
        "marks": marks, "vo_end": vo_end, "total": total, "spoken": spoken,
    }, indent=2) + "\n")
    if "--vo-only" in sys.argv:
        print("vo-only ok", flush=True)
        return

    body = vo_end - FIRST_CUT
    n = len(BODY)
    hold = body / n
    if hold > 3.80:
        raise SystemExit(f"plate hold {hold:.2f}s over 3.8 with {n} body plates")
    print(f"plates body={n} hold={hold:.2f}s", flush=True)

    rows = []
    t = FIRST_CUT
    # (name, src_path or None, ss, source, up, length, tin, kind)
    specs = []
    specs.append(("s00", EDL, OPEN_SS, EDL_NAME, 2.18, FIRST_CUT, 0.0, "edl"))
    for i, (kind, spec) in enumerate(BODY):
        length = round(hold, 3) if i < n - 1 else round(vo_end - t, 3)
        name = f"s{i+1:02d}"
        if kind == "gale":
            specs.append((name, GALE, float(spec), GALE_NAME, 1.78, length, t, kind))
        elif kind == "edl":
            specs.append((name, EDL, float(spec), EDL_NAME, 2.18, length, t, kind))
        elif kind == "gif":
            specs.append((name, GIF, 0.0, "PIA26673.gif", 2.00, length, t, kind))
        else:
            specs.append((name, STILLS / f"{spec}.jpg", 0.0, f"{spec}.jpg", 0.0, length, t, kind))
        t = round(t + length, 3)

    reuse = "--finish-only" in sys.argv
    for name, src_p, ss, source, up, length, tin, kind in specs:
        dest = WORK / f"{name}.mp4"
        if reuse and dest.exists() and dest.stat().st_size > 10000:
            print(f"reuse {name}", flush=True)
            if kind == "still":
                up = still_window(src_p)[5]
        else:
            print(f"cutting {name} {source} @{ss} {length}s", flush=True)
            if kind == "still":
                up = cut_still(src_p, length, dest)
            elif kind == "gif":
                cut_gif(length, dest)
            else:
                vf = gale_vf(ss) if kind == "gale" else EDL_VF
                cut_video(src_p, ss, length, vf, dest)
        framing = {"offset": ss} if kind != "still" else {}
        rows.append({
            "row": name, "timeline_in": round(tin, 3), "timeline_out": round(tin + length, 3),
            "source": source, "upscale": up, "video": kind != "still",
            "framing": framing,
        })

    if reuse and (WORK / "s_loop.mp4").exists() and (WORK / "picture.mp4").exists():
        print("reuse picture", flush=True)
    else:
        print("cutting loop", flush=True)
        run(["ffmpeg", "-y", "-v", "error", "-t", f"{LOOP:.3f}", "-i", str(WORK / "s00.mp4"),
             "-vf", "reverse,fps=30,format=yuv420p", "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
             "-frames:v", str(round(LOOP * FPS)), str(WORK / "s_loop.mp4")])
        lines = [f"file '{name}.mp4'" for name, *_ in specs] + ["file 's_loop.mp4'"]
        (WORK / "list.txt").write_text("\n".join(lines) + "\n")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(WORK / "list.txt"),
             "-c", "copy", str(WORK / "picture.mp4")])
    rows.append({
        "row": "s_loop", "timeline_in": round(vo_end, 3), "timeline_out": total,
        "source": "end_card_loop_" + EDL_NAME, "upscale": 2.18, "video": True,
        "framing": {"offset": OPEN_SS},
    })
    hook_png(WORK / "hook.png")
    title_png(WORK / "title.png")
    caps = caption_pngs(cap_words, vo_end)
    print(f"captions {len(caps)}", flush=True)

    vo_path = WORK / "stem_vo.wav"
    if reuse and (WORK / "mix.wav").exists() and (WORK / "stem_bed.wav").exists() and (WORK / "stem_sfx.wav").exists():
        print("reuse mix", flush=True)
    else:
        vo_i = lufs(vo_path)
        bed_raw = WORK / "stem_bed_raw.wav"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{BED_FROM}", "-i", str(BED),
             "-t", f"{total:.3f}", "-ac", "2", "-ar", str(SR), str(bed_raw)])
        bed_i = lufs(bed_raw)
        bed_gain = (vo_i - 28.0) - bed_i
        run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_raw),
             "-af", f"volume={bed_gain:.2f}dB,afade=t=in:st=0:d=0.25,afade=t=out:st={max(0.1, total - 0.6):.3f}:d=0.5",
             str(WORK / "stem_bed.wav")])
        whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
        tick = KIT / "sfx_owb_tick_ui_v01.wav"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(whoosh), "-i", str(tick),
             "-filter_complex",
             f"[0:a]aresample={SR},aformat=channel_layouts=stereo,adelay=0:all=1[w];"
             f"[1:a]aresample={SR},aformat=channel_layouts=stereo,adelay={int(TITLE_IN * 1000)}:all=1[t];"
             f"[w][t]amix=inputs=2:normalize=0,apad=whole_dur={total:.3f}[o]",
             "-map", "[o]", "-t", f"{total:.3f}", str(WORK / "stem_sfx_raw.wav")])
        sfx_i = lufs(WORK / "stem_sfx_raw.wav")
        sfx_gain = (vo_i - 18.0) - sfx_i
        run(["ffmpeg", "-y", "-v", "error", "-i", str(WORK / "stem_sfx_raw.wav"),
             "-af", f"volume={sfx_gain:.2f}dB", str(WORK / "stem_sfx.wav")])
        run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(WORK / "stem_bed.wav"),
             "-i", str(WORK / "stem_sfx.wav"), "-filter_complex",
             "[0:a][1:a][2:a]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
             "-map", "[o]", "-ar", str(SR), "-t", f"{total:.3f}", str(WORK / "mix.wav")])

    final = OUT / f"{STEM}.mp4"
    print("encoding", flush=True)
    burn_picture(WORK / "picture.mp4", WORK / "mix.wav", caps, total, final)

    loop = loop_measures(final)
    print("loop_diff", loop, flush=True)
    if loop["masked"] > 15:
        raise SystemExit(f"text-masked loop_diff {loop['masked']} over 15")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=2,scale=180:320,tile=8x8", "-frames:v", "1", str(OUT / f"{STEM}_2fps.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final),
         "-vf", "fps=1,scale=135:240,tile=6x8", "-frames:v", "1", str(OUT / f"{STEM}_PHONE.jpg")])

    cuts_path = OUT / "cuts_v02.json"
    pool_path = OUT / "pool_v02.json"
    cuts_path.write_text(json.dumps(rows, indent=2) + "\n")
    pool_items = [{"file_id": k, "title": v} for k, v in TITLES.items()]
    pool_items.append({"file_id": "end_card_loop_" + EDL_NAME, "title": "Loop back to the frame-0 descent"})
    pool_path.write_text(json.dumps(pool_items, indent=2) + "\n")

    meta = {
        "job": "J0935",
        "version": "v02",
        "test": "Short length test, 50-60 s",
        "air": AIR,
        "related": LONG_ID,
        "planned_title": "How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?",
        "replaces_for_review": "thu12_length_test_dust_v01 (scheduled N42gKBbD7tE). v01 not overwritten.",
        "file": str(final.relative_to(REPO)),
        "sha256": sha256(final),
        "duration_s": dur(final),
        "spoken": spoken,
        "spend": "none",
        "orbit": "none on screen",
        "loop_sentence": "…the sky turning off. Martian wind and passing dust devils swept its panels clean.",
        "brief": {
            "frame_0": f"{EDL_NAME} Perseverance descent at {OPEN_SS}s, moving, 9:16 crop, no Orbit",
            "first_word_s": marks["Martian"],
            "surprise_s": marks["wind"],
            "first_cut_s": FIRST_CUT,
            "last_word_to_loop_s": round(total - marks["off_end"], 3),
            "meta_promise": False,
            "payoff_number_s": marks["fourteen"],
            "payoff_vs_70pct": round(payoff_at, 2),
            "wind_s": marks["wind"],
            "clean_end_s": marks["clean_end"],
            "loop_diff_whole": loop["whole"],
            "loop_diff_masked": loop["masked"],
            "loop_diff": loop["masked"],
            "lufs": lufs(WORK / "mix.wav"),
        },
        "long_title_on_screen": {"title": LONG_TITLE, "from_s": TITLE_IN, "to_s": TITLE_OUT},
        "hook": "THE / WIND (yellow WIND), 0-2.0 s",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["brief"], indent=2), flush=True)

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", AIR, "--id", "N42gKBbD7tE", "--length-test",
         "--sheet-dir", str(OUT), "--vo", str(vo_path), "--meta", str(meta_path)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    print(gate.stdout[-2500:], gate.stderr[-800:], flush=True)

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
    for name, proc in (("sfx", sfx), ("music", music), ("polish", polish), ("picture_qa", pqa)):
        if proc.returncode != 0:
            print(f"--- {name} ---", flush=True)
            print((proc.stdout or "")[-2500:], (proc.stderr or "")[-800:], flush=True)
    raise SystemExit(0 if all(r.returncode == 0 for r in (gate, sfx, music, polish, pqa)) else 1)


if __name__ == "__main__":
    main()
