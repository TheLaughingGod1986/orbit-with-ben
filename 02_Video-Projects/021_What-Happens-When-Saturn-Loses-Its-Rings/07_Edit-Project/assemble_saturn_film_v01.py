#!/usr/bin/env python3
"""Assemble the Saturn rings long. Stills held, Veo played once, VO continuous.

Ben Orbit Narrator stays the voice. The Moon score beds are the underscore,
ducked under the narration. Veo audio is not used. No upload.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

EP = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings")
VO_SRC = EP / "02_Voiceover/parts/saturn_rings_vo_v01.mp3"
SPOKEN = EP / "02_Voiceover/parts/saturn_rings_vo_v01.txt"
STILLS = EP / "04_Generated-Clips/stills_v01"
VEO = EP / "04_Generated-Clips/veo_world_v01"
WORK = EP / "07_Edit-Project/saturn_film/work"
OUT = EP / "07_Edit-Project/saturn_film/saturn_film.mp4"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MUSIC = [
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part02_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part03_score_bed_v01.mp3"),
]
CARDS = [
    ("falling", "The Rings Are Falling"),
    ("ice", "Ice, Not Rock"),
    ("rain", "The Rain Into Saturn"),
    ("young", "When the Rings Were New"),
    ("bare", "Saturn Without Them"),
]
HOLD = 10.0
CARD = 1.5
W, H, FPS = 1280, 720, 24


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
            text=True,
        ).strip()
    )


def vol_mean(path: Path) -> float:
    p = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in p.stderr.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0].strip())
    raise RuntimeError(f"no mean volume for {path}")


def starfield(title: str, path: Path) -> None:
    im = Image.new("RGB", (W, H), "#070b14")
    px = im.load()
    for y in range(H):
        t = y / H
        r, g, b = int(7 + 8 * t), int(11 + 14 * t), int(20 + 22 * t)
        for x in range(0, W, 2):
            px[x, y] = (r, g, b)
            px[x + 1, y] = (r, g, b)
    draw = ImageDraw.Draw(im)
    for x, y in (
        (240, 160), (410, 280), (700, 120), (980, 340), (1260, 180),
        (1540, 260), (1760, 140), (320, 860), (1500, 900), (860, 780),
    ):
        draw.ellipse((x, y, x + 2, y + 2), fill=(210, 216, 230))
    f = ImageFont.truetype(FONT, 54)
    bbox = draw.textbbox((0, 0), title, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) / 2
    y = (H - th) / 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x, y + 2), title, font=f, fill=(0, 0, 0, 90))
    im = im.convert("RGBA")
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text((x, y), title, font=f, fill=(244, 246, 250, 255))
    im.convert("RGB").save(path, quality=95)


def write_srt(vo_len: float, path: Path) -> None:
    text = SPOKEN.read_text().strip()
    words = text.split()
    # ~8 words a cue, timed across the spoken length only.
    cues = []
    size = 8
    for i in range(0, len(words), size):
        cues.append(" ".join(words[i:i + size]))
    step = vo_len / len(cues)

    def ts(sec: float) -> str:
        sec = max(0.0, sec)
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = sec % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    lines = []
    for n, cue in enumerate(cues, start=1):
        a = (n - 1) * step
        b = min(vo_len, n * step)
        lines.append(f"{n}\n{ts(a)} --> {ts(b)}\n{cue}\n")
    path.write_text("\n".join(lines))


def build_audio() -> tuple[Path, float, float]:
    raw = probe(VO_SRC)
    # Spoken film stays inside 7–9, and the 10s end hold has to fit in that file.
    target_vo = raw
    if raw + HOLD > 540:
        target_vo = 540 - HOLD - 0.4
    tempo = raw / target_vo
    vo = WORK / "vo_full.m4a"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO_SRC),
        "-af", f"atempo={tempo:.6f},apad=pad_dur={HOLD:.3f}",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", str(vo),
    ])
    film = probe(vo)
    vo_len = film - HOLD
    print(f"vo raw {raw:.2f}s fitted {vo_len:.2f}s film {film:.2f}s tempo {tempo:.4f}", flush=True)
    if not 420 <= film <= 540:
        raise SystemExit(f"film audio {film:.2f}s outside 7–9 min")

    # Sequence the three existing beds twice. Encode straight to aac — no pcm wav.
    inputs = ["-i", str(vo)]
    for _ in range(2):
        for bed in MUSIC:
            inputs.extend(["-i", str(bed)])
    chain = "[1:a][2:a]acrossfade=d=2:c1=tri:c2=tri[a01];"
    prev = "a01"
    for i in range(3, 7):
        nxt = f"a0{i}"
        chain += f"[{prev}][{i}:a]acrossfade=d=2:c1=tri:c2=tri[{nxt}];"
        prev = nxt
    fade_st = max(0.0, film - HOLD)
    mixed = WORK / "master.m4a"
    # First pass writes the bed so we can measure it without a giant wav: measure via volumedetect on the graph.
    # Target the bed about -22 dB before the mix. Moon beds sit near -16 to -20 already; a fixed 0.18 keeps them under the voice.
    gain = 0.16
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex",
        chain
        + f"[{prev}]volume={gain:.3f},afade=t=out:st={fade_st:.3f}:d={HOLD:.3f},atrim=0:{film:.3f},asetpts=PTS-STARTPTS[mu];"
        + "[0:a][mu]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(mixed),
    ])
    print(f"master {probe(mixed):.2f}s mean {vol_mean(mixed):.1f} dB", flush=True)
    return mixed, vo_len, film


def still_seg(src: Path, dest: Path, dur: float) -> None:
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(src),
        "-t", f"{dur:.3f}",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-an", str(dest),
    ])


def video_seg(src: Path, dest: Path, dur: float) -> None:
    # Play the motion once. Do not freeze-extend a short clip.
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-t", f"{dur:.3f}", "-an",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", str(dest),
    ])


def add(segs: list, kind: str, src: Path, start: float, end: float) -> float:
    if end - start < 0.35:
        return start
    segs.append({"kind": kind, "src": str(src), "start": round(start, 3), "end": round(end, 3)})
    return end


def veo_len(path: Path, cap: float = 8.0) -> float:
    if not path.exists() or path.stat().st_size < 100_000:
        return 0.0
    return min(cap, probe(path) - 0.05)


def timeline(vo_len: float, film: float) -> list[dict]:
    scale = vo_len / probe(VO_SRC)
    ice = 136.9 * scale
    rain = 218.2 * scale
    young = 343.2 * scale
    bare = 433.6 * scale
    orbit1 = 100.0 * scale
    orbit2 = 495.0 * scale
    cards = {name: WORK / f"card_{name}.png" for name, _title in CARDS}
    segs: list[dict] = []
    t = 0.0
    open_still = STILLS / "saturn_open_rings_v01.png"
    open_veo = VEO / "veo_open_rings_v01.mp4"
    open_motion = veo_len(open_veo)
    if open_motion >= 2.0:
        t = add(segs, "video", open_veo, t, min(t + open_motion, ice - CARD))
        t = add(segs, "card", cards["falling"], t, t + CARD)
    else:
        t = add(segs, "still", open_still, t, 3.2)
        t = add(segs, "card", cards["falling"], t, t + CARD)
    t = add(segs, "still", open_still, t, orbit1)
    t = add(segs, "still", STILLS / "saturn_orbit_along_rings_v01.png", t, ice)
    t = add(segs, "card", cards["ice"], t, t + CARD)
    t = add(segs, "still", STILLS / "saturn_ice_chunks_v01.png", t, rain)
    t = add(segs, "card", cards["rain"], t, t + CARD)
    rain_veo = VEO / "veo_ring_rain_v01.mp4"
    rain_motion = veo_len(rain_veo)
    if rain_motion >= 2.0:
        t = add(segs, "video", rain_veo, t, min(t + rain_motion, young - CARD))
    t = add(segs, "still", STILLS / "saturn_ring_rain_cassini_v01.png", t, young)
    t = add(segs, "card", cards["young"], t, t + CARD)
    young_veo = VEO / "veo_young_rings_v01.mp4"
    young_motion = veo_len(young_veo)
    if young_motion >= 2.0:
        t = add(segs, "video", young_veo, t, min(t + young_motion, bare - CARD))
    t = add(segs, "still", STILLS / "saturn_young_rings_v01.png", t, bare)
    t = add(segs, "card", cards["bare"], t, t + CARD)
    t = add(segs, "still", STILLS / "saturn_bare_v01.png", t, orbit2)
    t = add(segs, "still", STILLS / "saturn_orbit_bare_v01.png", t, film)
    if abs(t - film) > 0.2:
        raise SystemExit(f"timeline ended at {t:.2f}, film is {film:.2f}")
    return segs


def render(mixed: Path, vo_len: float, film: float) -> None:
    for name, title in CARDS:
        starfield(title, WORK / f"card_{name}.png")
    segs = timeline(vo_len, film)
    (WORK / "timeline.json").write_text(json.dumps(segs, indent=2))
    pieces = []
    for i, seg in enumerate(segs):
        dest = WORK / f"seg_{i:02d}.mp4"
        dur = seg["end"] - seg["start"]
        src = Path(seg["src"])
        print(f"seg {i:02d} {seg['kind']} {dur:.2f}s {src.name}", flush=True)
        if seg["kind"] == "video":
            video_seg(src, dest, dur)
        else:
            still_seg(src, dest, dur)
        pieces.append(dest)
    listing = WORK / "video_concat.txt"
    listing.write_text("".join(f"file '{p.name}'\n" for p in pieces))
    silent = WORK / "picture.mp4"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(silent),
    ])
    for piece in pieces:
        piece.unlink(missing_ok=True)
    srt = WORK / "captions.srt"
    write_srt(vo_len, srt)
    # Burn captions for the spoken length. The end hold has no new lines.
    subprocess.run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(silent), "-i", str(mixed),
        "-vf", "subtitles=captions.srt:force_style='FontName=Arial,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48'",
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT),
    ], check=True, cwd=WORK)
    print(f"OUT {OUT} {probe(OUT):.2f}s {OUT.stat().st_size}", flush=True)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    for bed in MUSIC:
        if not bed.exists():
            raise SystemExit(f"missing music {bed}")
    mixed, vo_len, film = build_audio()
    render(mixed, vo_len, film)


if __name__ == "__main__":
    main()
