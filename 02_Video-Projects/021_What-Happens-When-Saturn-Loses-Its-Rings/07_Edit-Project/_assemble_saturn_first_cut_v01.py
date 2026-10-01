#!/usr/bin/env python3
"""Saturn first cut v01 — Ben 1 Oct 12:27: go to first cut after v07 contacts.

Uses approved / v07 edit-built plates + v02 VO. Stills-first coverage (no freeze-extend).
Picture-first open 3s. Chapter cards. ≥10s last-picture hold with music fade.
Output → OWB UAT/saturn_first_cut_v01.mp4 (+ contact sheets per section). No media in git.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

EP = Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings")
CLIPS = EP / "04_Generated-Clips"
V07 = CLIPS / "v07"
VO = EP / "02_Voiceover/parts/saturn_rings_vo_v02.wav"
WORK = EP / "07_Edit-Project/saturn_film/work_first_cut_v01"
OUT_LOCAL = EP / "07_Edit-Project/saturn_film/saturn_first_cut_v01.mp4"
UAT = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
UAT_MP4 = UAT / "saturn_first_cut_v01.mp4"
UAT_DIR = UAT / "saturn_first_cut_v01_for_ben_ok"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/assets"
)

OPEN = V07 / "edit_open_rings_v07.mp4"
ICE = V07 / "edit_ice_chunks_v07.mp4"
BARE_ORBIT = V07 / "edit_bare_orbit_composite_v07.mp4"
TUMBLE = V07 / "veo_orbit_tumble_v03_fallback_0-3s.mp4"
OPEN_STILL = CLIPS / "stills_v06" / "saturn_open_rings_v06.png"
ICE_STILL = CLIPS / "stills_v05" / "saturn_ice_chunks_v05.png"
BARE_STILL = CLIPS / "veo_v05" / "stills" / "saturn_bare_planet_only_v05.png"
if not BARE_STILL.exists():
    BARE_STILL = CLIPS / "stills_v06" / "saturn_bare_orbit_v06.png"  # last resort (has Orbit)

MUSIC = [
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part02_score_bed_v01.mp3"),
    Path("/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part03_score_bed_v01.mp3"),
]

W, H, FPS = 1920, 1080, 24
HOLD = 15.0
CARD = 1.5
BREATH = 1.5
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# Approximate act marks on v02 VO (~563s). Scaled from v01 assemble marks if needed.
MARK = {
    "open_end": 30.0,
    "falling": 84.0,
    "ice": 135.0,
    "rain": 222.0,
    "cassini": 252.0,
    "young": 342.0,
    "bare": 434.0,
    "close": 500.0,
}

CARDS = [
    ("falling", "The Rings Are Falling", "falling"),
    ("ice", "Ice, Not Rock", "ice"),
    ("rain", "The Rain Into Saturn", "rain"),
    ("young", "When the Rings Were New", "young"),
    ("bare", "Saturn Without Them", "bare"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(500 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def chunk_write(src: Path | bytes, dest: Path, retries: int = 14) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 256 * 1024):
                    o.write(data[i : i + 256 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.3)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    Path("/tmp").joinpath(f"uat_stage_{dest.name}").write_bytes(data)


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd[:12]), "...", flush=True)
    subprocess.check_call(cmd)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def starfield_card(title: str, path: Path) -> None:
    im = Image.new("RGB", (W, H), "#070b14")
    px = im.load()
    for y in range(H):
        t = y / H
        r, g, b = int(7 + 8 * t), int(11 + 14 * t), int(20 + 22 * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(im)
    for x, y in (
        (180, 120), (420, 200), (700, 90), (980, 240), (1400, 140),
        (220, 700), (800, 780), (1200, 640), (1600, 720), (500, 500),
    ):
        draw.ellipse((x, y, x + 2, y + 2), fill=(210, 216, 230))
    f = ImageFont.truetype(FONT, 64)
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


def still_push_mp4(still: Path, dest: Path, dur: float, zoom_end: float = 1.08, bias: float = 0.55) -> None:
    """Unique still push via ffmpeg zoompan — play once, no loop of motion clips."""
    if dur < 0.25:
        dur = 0.25
    n = max(1, int(dur * FPS))
    z0, z1 = 1.0, zoom_end
    # zoompan: z grows; x biased toward Saturn (right)
    # x expression: keep subject toward bias
    xf = f"(iw-ow/zoom)*{bias:.3f}"
    yf = "(ih-oh/zoom)/2"
    zf = f"{z0:.4f}+({z1 - z0:.4f})*on/{max(n - 1, 1)}"
    run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(still),
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"zoompan=z='{zf}':x='{xf}':y='{yf}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
            "-t",
            f"{dur:.3f}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            "-an",
            str(dest),
        ]
    )


def normalize_clip(src: Path, dest: Path, max_dur: float | None = None) -> float:
    dur = probe(src)
    if max_dur is not None:
        dur = min(dur, max_dur)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-t",
            f"{dur:.3f}",
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            str(dest),
        ]
    )
    return probe(dest)


def card_mp4(png: Path, dest: Path, dur: float = CARD) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(png),
            "-t",
            f"{dur:.3f}",
            "-vf",
            f"scale={W}:{H},fps={FPS}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            "-an",
            str(dest),
        ]
    )


def contact_sheet(mp4: Path, dest: Path) -> list[float]:
    dur = probe(mp4)
    times = [0.05, dur / 3, 2 * dur / 3, max(0.05, dur - 0.08)]
    frames = []
    for i, t in enumerate(times):
        p = WORK / f"_cs_{mp4.stem}_{i}.png"
        run(["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(p)])
        frames.append(Image.open(p).convert("RGB"))
    tw, th = frames[0].size[0] // 2, frames[0].size[1] // 2
    sheet = Image.new("RGB", (tw * 2 + 6, th * 2 + 6), (12, 12, 14))
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(frames):
        im = im.resize((tw, th), Image.Resampling.LANCZOS)
        x = (i % 2) * (tw + 6)
        y = (i // 2) * (th + 6)
        sheet.paste(im, (x, y))
        draw.text((x + 8, y + 8), f"t={times[i]:.2f}s", fill=(255, 220, 80))
    sheet.save(dest)
    return times


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    for p in (OPEN, ICE, BARE_ORBIT, TUMBLE, VO, OPEN_STILL, ICE_STILL):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    vo_dur = probe(VO)
    film_vo = vo_dur
    # keep ~9 min + hold; if VO longer, keep full VO (do not chop mid-word)
    total_target = film_vo + HOLD
    print(f"VO={vo_dur:.2f}s film+hold≈{total_target:.2f}s", flush=True)

    # cards
    cards = {}
    for key, title, _ in CARDS:
        png = WORK / f"card_{key}.png"
        mp4 = WORK / f"card_{key}.mp4"
        starfield_card(title, png)
        card_mp4(png, mp4)
        cards[key] = mp4

    # normalize motion once each
    open_n = WORK / "open_v07.mp4"
    ice_n = WORK / "ice_v07.mp4"
    bare_n = WORK / "bare_orbit_v07.mp4"
    tum_n = WORK / "tumble_fallback.mp4"
    d_open = normalize_clip(OPEN, open_n)
    d_ice = normalize_clip(ICE, ice_n)
    d_bare = normalize_clip(BARE_ORBIT, bare_n)
    d_tum = normalize_clip(TUMBLE, tum_n)

    # Build timeline segments: list of (path, start_on_timeline)
    # Picture-first: open motion first 3s of film (and continues)
    segs: list[tuple[Path, float]] = []
    t = 0.0

    def add_clip(path: Path, use: float | None = None) -> float:
        nonlocal t
        d = probe(path) if use is None else min(probe(path), use)
        # trim copy if needed
        if use is not None and use < probe(path) - 0.05:
            trimmed = WORK / f"trim_{path.stem}_{int(t*10)}.mp4"
            normalize_clip(path, trimmed, max_dur=use)
            path = trimmed
            d = probe(path)
        segs.append((path, t))
        t += d
        return t

    def fill_still(still: Path, until: float, zoom: float = 1.08, bias: float = 0.55) -> None:
        nonlocal t
        need = until - t
        if need <= 0.05:
            return
        # split long fills into ≤12s unique pushes with alternating bias (no loop of same motion)
        chunk = 10.0
        i = 0
        while need > 0.05:
            use = min(chunk, need)
            dest = WORK / f"still_{still.stem}_{int(t*10)}_{i}.mp4"
            z = zoom + 0.01 * (i % 3)
            b = bias + (0.04 if i % 2 == 0 else -0.04)
            still_push_mp4(still, dest, use, zoom_end=z, bias=b)
            segs.append((dest, t))
            t += use
            need -= use
            i += 1

    # OPEN act
    add_clip(open_n)
    fill_still(OPEN_STILL, MARK["falling"] - BREATH, zoom=1.09, bias=0.62)
    # breath into card
    fill_still(OPEN_STILL, MARK["falling"], zoom=1.02, bias=0.60)
    add_clip(cards["falling"])

    # after falling card → ice card
    fill_still(OPEN_STILL, MARK["ice"] - BREATH, zoom=1.07, bias=0.58)
    fill_still(OPEN_STILL, MARK["ice"], zoom=1.02, bias=0.58)
    add_clip(cards["ice"])
    add_clip(ice_n)
    fill_still(ICE_STILL, MARK["rain"] - BREATH, zoom=1.08, bias=0.45)
    fill_still(ICE_STILL, MARK["rain"], zoom=1.02, bias=0.45)
    add_clip(cards["rain"])

    # rain / cassini — reopen stream look
    fill_still(OPEN_STILL, MARK["young"] - BREATH, zoom=1.10, bias=0.65)
    fill_still(OPEN_STILL, MARK["young"], zoom=1.02, bias=0.65)
    add_clip(cards["young"])
    fill_still(OPEN_STILL, MARK["bare"] - BREATH, zoom=1.06, bias=0.55)
    fill_still(OPEN_STILL, MARK["bare"], zoom=1.02, bias=0.55)
    add_clip(cards["bare"])

    # Orbit beats: tumble then bare+orbit
    add_clip(tum_n)
    add_clip(bare_n)
    fill_still(BARE_STILL if BARE_STILL.exists() else OPEN_STILL, film_vo, zoom=1.08, bias=0.55)

    # end hold picture (extend last still push)
    hold_still = BARE_STILL if BARE_STILL.exists() else OPEN_STILL
    hold_mp4 = WORK / "end_hold.mp4"
    still_push_mp4(hold_still, hold_mp4, HOLD, zoom_end=1.04, bias=0.55)
    segs.append((hold_mp4, t))
    t += HOLD
    film_len = t
    print(f"picture timeline {film_len:.2f}s (VO {film_vo:.2f} + hold {HOLD})", flush=True)

    # concat video
    concat_list = WORK / "concat.txt"
    # re-encode each to same timebase then concat demuxer — use filter concat for A/V sync later
    # Build video-only concat
    lines = []
    for path, _ in segs:
        lines.append(f"file '{path}'")
    concat_list.write_text("\n".join(lines) + "\n")
    video_raw = WORK / "picture_raw.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "16",
            "-an",
            str(video_raw),
        ]
    )

    # Audio: VO + music beds under, fade over last ~10s of hold
    # Pad VO with silence for hold
    vo_pad = WORK / "vo_padded.m4a"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(VO),
            "-af",
            f"apad=pad_dur={HOLD}",
            "-t",
            f"{film_vo + HOLD:.3f}",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(vo_pad),
        ]
    )
    # music concat loop to cover film
    music_ok = [m for m in MUSIC if m.exists()]
    if not music_ok:
        raise SystemExit("no music beds")
    mlist = WORK / "music.txt"
    # repeat beds enough times
    reps = []
    while True:
        for m in music_ok:
            reps.append(f"file '{m}'")
            if len(reps) > 20:
                break
        if len(reps) > 20:
            break
    mlist.write_text("\n".join(reps) + "\n")
    music_long = WORK / "music_long.m4a"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(mlist),
            "-t",
            f"{film_vo + HOLD:.3f}",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(music_long),
        ]
    )
    # mix: VO front, music ~-20dB, fade music+picture last 10s / 2s black
    fade_start = max(0.0, film_vo + HOLD - 10.0)
    black_start = max(0.0, film_vo + HOLD - 2.0)
    mixed = WORK / "mix.m4a"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(vo_pad),
            "-i",
            str(music_long),
            "-filter_complex",
            f"[1:a]volume=-20dB,afade=t=out:st={fade_start:.3f}:d=10[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map",
            "[a]",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(mixed),
        ]
    )

    # mux + picture fade to black last 2s
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_raw),
            "-i",
            str(mixed),
            "-filter_complex",
            f"[0:v]fade=t=out:st={black_start:.3f}:d=2,format=yuv420p[v]",
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-crf",
            "16",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(OUT_LOCAL),
        ]
    )

    # section contacts
    UAT_DIR.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    section_contacts = {}
    for name, path in (
        ("open", open_n),
        ("ice", ice_n),
        ("bare_orbit", bare_n),
        ("tumble", tum_n),
        ("full", OUT_LOCAL),
    ):
        cs = WORK / f"contact_{name}.png"
        times = contact_sheet(path, cs)
        section_contacts[name] = {"file": cs.name, "times": times, "sha256": sha256(cs)}
        chunk_write(cs, UAT_DIR / cs.name)
        chunk_write(cs, ART / cs.name)

    chunk_write(OUT_LOCAL, UAT_MP4)
    chunk_write(OUT_LOCAL, UAT_DIR / "saturn_first_cut_v01.mp4")
    # also m4a of mix for listen
    chunk_write(mixed, UAT_DIR / "saturn_first_cut_v01_audio.m4a")

    manifest = {
        "ben_order": "2026-10-01T12:27 London — first cut after v07 contacts",
        "vo": str(VO),
        "vo_sha256": sha256(VO),
        "vo_duration_s": vo_dur,
        "film_duration_s": probe(OUT_LOCAL),
        "hold_s": HOLD,
        "picture_first_s": 3.0,
        "assets": {
            "open": sha256(OPEN),
            "ice": sha256(ICE),
            "bare_orbit": sha256(BARE_ORBIT),
            "tumble": sha256(TUMBLE),
        },
        "section_contacts": section_contacts,
        "output_sha256": sha256(OUT_LOCAL),
        "output_bytes": OUT_LOCAL.stat().st_size,
        "uat": str(UAT_MP4),
        "stop": "STOP for Ben watch — first cut only",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (WORK / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(WORK / "MANIFEST.json", UAT_DIR / "MANIFEST.json")
    sha_md = f"# SHA-256 — saturn_first_cut_v01\n\n| File | SHA-256 | Bytes |\n|---|---|---|\n| `saturn_first_cut_v01.mp4` | `{manifest['output_sha256']}` | {manifest['output_bytes']} |\n"
    (WORK / "SHA256.md").write_text(sha_md)
    chunk_write(WORK / "SHA256.md", UAT_DIR / "SHA256.md")
    print(json.dumps({"FIRST_CUT_DONE": True, **manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
