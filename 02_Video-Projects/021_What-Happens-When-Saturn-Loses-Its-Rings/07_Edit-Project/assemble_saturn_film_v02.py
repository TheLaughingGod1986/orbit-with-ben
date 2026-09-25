#!/usr/bin/env python3
"""Saturn picture rebuild assemble. Motion only, except locked act cards.

Keeps the existing Ben Orbit Narrator take and the three Moon score beds.
Does not upload. Does not freeze-extend a short clip.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

EP = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings")
VO_SRC = EP / "02_Voiceover/parts/saturn_rings_vo_v01.mp3"
SPOKEN = Path("/tmp/saturn_vo.txt")
MOTION = EP / "04_Generated-Clips/veo_motion_v02"
OPEN = EP / "04_Generated-Clips/veo_world_v01/veo_open_rings_v01.mp4"
WORK = EP / "07_Edit-Project/saturn_film/work_v02"
OUT = EP / "07_Edit-Project/saturn_film/saturn_film_v02.mp4"
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

# Spoken-clock marks (raw VO seconds).
MARK = {
    "cassini_weigh": 84.4,
    "wondering": 108.0,
    "ice": 135.7,
    "rain": 222.1,
    "cassini_story": 252.3,
    "cassini_end": 314.6,
    "young": 342.0,
    "moon": 404.7,
    "bare": 434.5,
    "standing": 467.9,
}


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
        (140, 90), (310, 180), (520, 70), (780, 220), (1040, 120),
        (180, 520), (640, 600), (980, 480), (1200, 560), (400, 400),
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
    im.convert("RGB").save(path)


def label_png(text: str, path: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 42)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) / 2
    y = H - 120 - th
    draw.rectangle((x - 18, y - 10, x + tw + 18, y + th + 12), fill=(0, 0, 0, 170))
    draw.text((x, y), text, font=f, fill=(255, 255, 255, 255))
    im.save(path)


def write_srt(vo_len: float, path: Path) -> None:
    words = SPOKEN.read_text().strip().split()
    cues = [" ".join(words[i:i + 8]) for i in range(0, len(words), 8)]
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


def build_audio() -> tuple[Path, float, float, float]:
    raw = probe(VO_SRC)
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
    return mixed, vo_len, film, raw


class Pool:
    def __init__(self, name: str) -> None:
        files = sorted(MOTION.glob(f"{name}_*.mp4"))
        self.files = [p for p in files if p.stat().st_size > 100_000]
        self.i = 0
        self.name = name

    def take(self) -> Path:
        if self.i >= len(self.files):
            raise SystemExit(f"pool {self.name} ran out at clip {self.i}")
        path = self.files[self.i]
        self.i += 1
        return path


def usable(path: Path) -> float:
    return max(0.0, probe(path) - 0.08)


def add(segs: list, kind: str, src: Path, start: float, end: float) -> float:
    if end - start < 0.35:
        return start
    segs.append({"kind": kind, "src": str(src), "start": round(start, 3), "end": round(end, 3)})
    return end


def fill(segs: list, pool: Pool, t: float, end: float) -> float:
    while t < end - 0.45:
        src = pool.take()
        dur = min(usable(src), end - t)
        t = add(segs, "video", src, t, t + dur)
    if t < end - 0.8:
        raise SystemExit(f"{pool.name} ended {t:.2f}s, needed {end:.2f}s")
    return t


def timeline(vo_len: float, film: float, raw: float) -> list[dict]:
    scale = vo_len / raw

    def m(name: str) -> float:
        return MARK[name] * scale

    pools = {name: Pool(name) for name in ("rings", "ice", "rain", "cassini", "young", "moon", "bare")}
    cards = {name: WORK / f"card_{name}.png" for name, _title in CARDS}
    segs: list[dict] = []
    t = 0.0
    t = add(segs, "video", OPEN, t, min(usable(OPEN), 8.0))
    t = add(segs, "card", cards["falling"], t, t + CARD)
    t = fill(segs, pools["rings"], t, m("cassini_weigh"))
    t = fill(segs, pools["cassini"], t, t + min(8.0, m("wondering") - t))
    t = fill(segs, pools["rings"], t, m("wondering"))
    orbit1 = MOTION / "orbit_along_v01.mp4"
    t = add(segs, "video", orbit1, t, t + min(usable(orbit1), m("ice") - t))
    t = fill(segs, pools["rings"], t, m("ice"))
    t = add(segs, "card", cards["ice"], t, t + CARD)
    t = fill(segs, pools["ice"], t, m("rain"))
    t = add(segs, "card", cards["rain"], t, t + CARD)
    t = fill(segs, pools["rain"], t, m("cassini_story"))
    t = fill(segs, pools["cassini"], t, m("cassini_end"))
    t = fill(segs, pools["rain"], t, m("young"))
    t = add(segs, "card", cards["young"], t, t + CARD)
    t = fill(segs, pools["young"], t, m("moon"))
    t = fill(segs, pools["moon"], t, m("bare"))
    t = add(segs, "card", cards["bare"], t, t + CARD)
    t = fill(segs, pools["bare"], t, m("standing"))
    orbit2 = MOTION / "orbit_bare_v01.mp4"
    t = add(segs, "video", orbit2, t, t + min(usable(orbit2), film - t))
    t = fill(segs, pools["bare"], t, film)
    if abs(t - film) > 0.8:
        raise SystemExit(f"timeline ended at {t:.2f}, film is {film:.2f}")
    return segs


def video_seg(src: Path, dest: Path, dur: float) -> None:
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-t", f"{dur:.3f}", "-an",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", str(dest),
    ])


def still_seg(src: Path, dest: Path, dur: float) -> None:
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(src),
        "-t", f"{dur:.3f}",
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-an", str(dest),
    ])


def render(mixed: Path, vo_len: float, film: float, raw: float) -> None:
    for name, title in CARDS:
        starfield(title, WORK / f"card_{name}.png")
    segs = timeline(vo_len, film, raw)
    (WORK / "timeline.json").write_text(json.dumps(segs, indent=2))
    kinds = {s["kind"] for s in segs}
    if "still" in kinds:
        raise SystemExit("timeline still contains a frozen science plate")
    pieces = []
    for i, seg in enumerate(segs):
        dest = WORK / f"seg_{i:03d}.mp4"
        dur = seg["end"] - seg["start"]
        src = Path(seg["src"])
        print(f"seg {i:03d} {seg['kind']} {dur:.2f}s {src.name}", flush=True)
        if seg["kind"] == "card":
            still_seg(src, dest, dur)
        else:
            video_seg(src, dest, dur)
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
    scale = vo_len / raw
    labels = [
        ("100 MILLION YEARS", 16.7, 24.0),
        ("10 METRES THICK", 56.2, 64.0),
        ("CASSINI  ·  TWO FIFTHS OF MIMAS", 84.4, 96.0),
        ("10 METRES", 204.2, 212.0),
        ("CASSINI  ·  2004 TO 2017", 252.3, 272.0),
        ("22 DIVES", 272.0, 282.0),
        ("15 SEPTEMBER 2017", 280.8, 292.0),
        ("100 MILLION YEARS", 314.6, 326.0),
        ("100 MILLION YEARS EARLIER", 342.0, 354.0),
        ("4.5 BILLION YEARS", 370.1, 380.0),
        ("A DAY IS ABOUT 10 HOURS", 442.2, 452.0),
        ("100 MILLION YEARS", 492.3, 508.0),
    ]
    inputs = ["-i", str(silent)]
    overlays = []
    for n, (text, a, b) in enumerate(labels):
        png = WORK / f"label_{n:02d}.png"
        label_png(text, png)
        inputs.extend(["-i", str(png)])
        overlays.append((n + 1, a * scale, b * scale))
    chain = ""
    prev = "0:v"
    for idx, (stream, a, b) in enumerate(overlays):
        out = f"v{idx}"
        chain += (
            f"[{prev}][{stream}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[{out}];"
        )
        prev = out
    labeled = WORK / "picture_labeled.mp4"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", chain.rstrip(";"),
        "-map", f"[{prev}]",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        str(labeled),
    ])
    silent.unlink(missing_ok=True)
    srt = WORK / "captions.srt"
    write_srt(vo_len, srt)
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(labeled), "-i", str(mixed), "-i", str(srt),
        "-map", "0:v", "-map", "1:a", "-map", "2:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        "-t", f"{film:.3f}", str(OUT),
    ])
    print(f"OUT {OUT} {probe(OUT):.2f}s {OUT.stat().st_size}", flush=True)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    if not SPOKEN.exists():
        raise SystemExit("missing spoken script at /tmp/saturn_vo.txt")
    for bed in MUSIC:
        if not bed.exists():
            raise SystemExit(f"missing music {bed}")
    if not OPEN.exists():
        raise SystemExit("missing open rings motion")
    mixed, vo_len, film, raw = build_audio()
    render(mixed, vo_len, film, raw)


if __name__ == "__main__":
    main()
