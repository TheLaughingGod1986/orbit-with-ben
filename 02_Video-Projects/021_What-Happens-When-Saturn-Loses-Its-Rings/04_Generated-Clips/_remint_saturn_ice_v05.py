#!/usr/bin/env python3
"""Remint ice crowd Veo v05 — first take invented Saturn+rings and looked floor-like."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from orbit_gemini_veo import strip_audio  # noqa: E402
from orbit_voice import CG_SILENT_AUDIO_BLOCK  # noqa: E402
from google import genai
from google.genai import types

OUT = (
    REPO
    / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/04_Generated-Clips/veo_v05"
)
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_veo_v05_for_ben_ok"
)
STILL = (
    REPO
    / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/04_Generated-Clips/stills_v05/saturn_ice_chunks_v05.png"
)


def chunk_write(src: Path, dest: Path) -> None:
    data = src.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    with open(tmp, "wb") as o:
        for i in range(0, len(data), 500 * 1024):
            o.write(data[i : i + 500 * 1024])
            o.flush()
    tmp.replace(dest)


def main() -> None:
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    client = genai.Client(
        vertexai=True,
        project="gen-lang-client-0538779324",
        location="us-central1",
        http_options={"api_version": "v1"},
    )
    prompt = (
        "From this exact still: camera drifts FORWARD at CONSTANT HEIGHT through a sparse "
        "crowd of jagged icy ring chunks floating in BLACK VOID. "
        "Chunk density UNCHANGED throughout — black empty space between EVERY chunk. "
        "NO planet, NO Saturn, NO rings, NO ground, NO floor, NO pile, NO rubble heap, "
        "NO boulders gathering below, NO horizon. Chunks stay suspended in void at different depths. "
        "No Orbit, no robot, no spacecraft, no text. Silent picture."
    )
    neg = (
        "planet, Saturn, rings, ground, floor, surface, pile, rubble heap, horizon, "
        "robot, Orbit, spacecraft, text, Earth, explosion"
    )
    dest = OUT / "veo_ice_chunks_v05.mp4"
    if dest.is_file():
        arch = OUT / "_rejected" / f"veo_ice_chunks_v05_try1_{hashlib.sha256(dest.read_bytes()).hexdigest()[:8]}.mp4"
        arch.parent.mkdir(exist_ok=True)
        dest.replace(arch)
        print("archived", arch.name, flush=True)
    img = types.Image.from_file(location=str(STILL))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        generate_audio=False,
        negative_prompt=neg,
    )
    print("submit ice remint", flush=True)
    op = client.models.generate_videos(
        model="veo-3.1-fast-generate-001",
        source=types.GenerateVideosSource(prompt=prompt + " " + CG_SILENT_AUDIO_BLOCK, image=img),
        config=config,
    )
    t0 = time.time()
    while not op.done:
        time.sleep(15)
        op = client.operations.get(op)
        print("poll", int(time.time() - t0), op.done, flush=True)
    resp = op.response or getattr(op, "result", None)
    videos = getattr(resp, "generated_videos", None) if resp else None
    if not videos:
        videos = getattr(getattr(op, "result", None), "generated_videos", None)
    v = videos[0].video
    if hasattr(v, "save"):
        v.save(str(dest))
    elif getattr(v, "video_bytes", None):
        dest.write_bytes(v.video_bytes)
    elif getattr(v, "uri", None):
        subprocess.run(["gcloud", "storage", "cp", v.uri, str(dest)], check=True)
    strip_audio(dest)
    # contact
    dur = float(
        json.loads(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(dest)]
            )
        )["format"]["duration"]
    )
    times = [0.05, dur / 3, 2 * dur / 3, max(0.05, dur - 0.08)]
    frames = []
    work = OUT / "_work"
    work.mkdir(exist_ok=True)
    for i, t in enumerate(times):
        p = work / f"ice_r2_{i}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(dest), "-frames:v", "1", str(p)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        frames.append(Image.open(p).convert("RGB"))
    h = max(im.height for im in frames) // 2
    resized = [im.resize((int(im.width * h / im.height), h)) for im in frames]
    gap = 8
    w = sum(im.width for im in resized) + gap * 3
    sheet = Image.new("RGB", (w, h + 40), (12, 12, 16))
    d = ImageDraw.Draw(sheet)
    x = 0
    for im, t in zip(resized, times):
        sheet.paste(im, (x, 32))
        d.text((x + 4, 4), f"{t:.2f}s", fill=(220, 220, 230))
        x += im.width + gap
    cs = OUT / "_contact" / "veo_ice_chunks_v05_contact.png"
    sheet.save(cs)
    for src in (dest, cs):
        chunk_write(src, UAT / src.name)
    print(
        "ICE_REMINT",
        hashlib.sha256(dest.read_bytes()).hexdigest(),
        dest.stat().st_size,
        flush=True,
    )


if __name__ == "__main__":
    main()
