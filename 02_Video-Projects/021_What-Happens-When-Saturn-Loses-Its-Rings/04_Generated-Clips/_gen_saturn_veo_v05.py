#!/usr/bin/env python3
"""Saturn Veo Fast v05 — Ben reject of v04 (1 Oct 11:15). Vertex only. NO Orbit in Veo.

  OPEN: fine ice grains already drifting at frame 0 into equator; no explosion/spray/outward.
  BARE: planet-only start still (Orbit removed); slow push; no other objects.
  ICE: constant-height drift; chunk density unchanged; black space between chunks; no ground/pile.

Orbit motion = Omni separately (§5–6). Pack: OWB UAT/saturn_veo_v05_for_ben_ok/
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import strip_audio  # noqa: E402
from orbit_voice import CG_SILENT_AUDIO_BLOCK  # noqa: E402

from google import genai
from google.genai import types

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
CLIPS = EP / "04_Generated-Clips"
OUT = CLIPS / "veo_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_veo_v05_for_ben_ok"
)
CONTACT = OUT / "_contact"
WORK = OUT / "_work"

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "veo-3.1-fast-generate-001"
IMG_MODEL = "gemini-2.5-flash-image"
USD_PER_SECOND = 0.15
DURATION = 8

BARE_V06 = CLIPS / "stills_v06" / "saturn_bare_orbit_v06.png"
OPEN_V06 = CLIPS / "stills_v06" / "saturn_open_rings_v06.png"
ICE_V05 = CLIPS / "stills_v05" / "saturn_ice_chunks_v05.png"
BARE_PLANET = OUT / "stills" / "saturn_bare_planet_only_v05.png"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src: Path | bytes, dest: Path, retries: int = 8) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 500 * 1024):
                    o.write(data[i : i + 500 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.2)
            if dest.stat().st_size == len(data) and sha256(dest) == hashlib.sha256(data).hexdigest():
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"chunk_write failed {dest}")


def save_image_response(response, dest: Path) -> None:
    for part in response.candidates[0].content.parts or []:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return
    raise RuntimeError("no image bytes")


def make_bare_planet_still(client: genai.Client) -> Path:
    """Remove Orbit from bare v06 — planet only."""
    BARE_PLANET.parent.mkdir(parents=True, exist_ok=True)
    if BARE_PLANET.is_file() and BARE_PLANET.stat().st_size > 50_000:
        print(f"reuse bare planet still {BARE_PLANET.name}", flush=True)
        return BARE_PLANET
    prompt = (
        "IMAGE EDIT of the attached 16:9 still. REMOVE the small orange robot completely. "
        "Fill that area with clean near-black starfield matching the rest of space. "
        "KEEP bare Saturn (no rings) exactly — same size, bands, soft shadowed crescent on the right. "
        "Result: planet ONLY in black space. No robot, no Orbit, no spacecraft, no rings, no text."
    )
    print("make bare planet-only still from v06", flush=True)
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=IMG_MODEL,
                contents=[
                    "Base still (remove Orbit):",
                    types.Part.from_bytes(data=BARE_V06.read_bytes(), mime_type="image/png"),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            save_image_response(response, BARE_PLANET)
            if BARE_PLANET.stat().st_size > 50_000:
                break
        except Exception as e:
            print(f"  still retry {attempt}: {e}", flush=True)
            time.sleep(6 * (attempt + 1))
    chunk_write(BARE_PLANET, UAT / BARE_PLANET.name)
    return BARE_PLANET


CLIPS_SPEC = [
    {
        "file": "veo_open_rings_v05.mp4",
        "still": OPEN_V06,
        "prompt": (
            "Continuous cinematic motion from this exact still: fine ice grains are ALREADY "
            "drifting off the inner ring edge at frame 0, falling gently into Saturn's equator. "
            "Slow steady camera push toward the planet. "
            "NO explosion, NO spray, NO debris flying outward, NO ring seam breakup, NO shatter. "
            "Keep the fine-banded ring blade continuous. Near-black clean space. "
            "No robot, no Orbit, no spacecraft, no text, no second planet. Silent picture."
        ),
    },
    {
        "file": "veo_bare_saturn_v05.mp4",
        "still": BARE_PLANET,  # filled at runtime
        "prompt": (
            "Continuous cinematic motion from this exact still: bare Saturn alone (no rings) "
            "in near-black space. Slow steady camera push toward the planet. "
            "No other objects. No robot, no Orbit, no spacecraft, no rings, no text, "
            "no second planet. Silent picture."
        ),
    },
    {
        "file": "veo_ice_chunks_v05.mp4",
        "still": ICE_V05,
        "prompt": (
            "Continuous cinematic motion from this exact still: camera drifts forward at "
            "CONSTANT HEIGHT through a sparse crowd of jagged icy ring chunks. "
            "Chunk density unchanged throughout — black space between every chunk. "
            "NO ground, NO floor, NO pile, NO rubble heap, NO boulders gathering below. "
            "Chunks stay floating in void at different depths. "
            "No robot, no Orbit, no spacecraft, no text, no planet Earth. Silent picture."
        ),
    },
]


def generate_veo(client: genai.Client, prompt: str, still: Path, dest: Path) -> None:
    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=DURATION,
        aspect_ratio="16:9",
        resolution="720p",
        generate_audio=False,
        negative_prompt=(
            "robot, mascot, orange character, Orbit, spacecraft, humanoid, arms, hands, "
            "explosion, outward spray, shatter, debris blast, ground, floor, rubble pile, "
            "text, captions, logos, watermark, second planet, Earth, people, speech, narration"
        ),
    )
    full = prompt.strip() + " " + CG_SILENT_AUDIO_BLOCK
    print(f"submit {dest.name} model={MODEL} still={still.name}", flush=True)
    t0 = time.time()
    operation = client.models.generate_videos(
        model=MODEL,
        source=types.GenerateVideosSource(prompt=full, image=img),
        config=config,
    )
    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        print(f"  poll {dest.stem} {int(time.time() - t0)}s done={operation.done}", flush=True)
    if getattr(operation, "error", None):
        raise RuntimeError(f"Veo error: {operation.error}")
    response = operation.response or getattr(operation, "result", None)
    videos = getattr(response, "generated_videos", None) if response else None
    if not videos:
        result = getattr(operation, "result", None)
        videos = getattr(result, "generated_videos", None) if result else None
    if not videos:
        raise RuntimeError(f"Veo returned no videos: {operation}")
    video = videos[0].video
    dest.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(client.files, "download"):
        try:
            client.files.download(file=video)
        except Exception as e:
            print(f"  download note: {e}", flush=True)
    if hasattr(video, "save"):
        video.save(str(dest))
    elif getattr(video, "video_bytes", None):
        dest.write_bytes(video.video_bytes)
    elif getattr(video, "uri", None):
        subprocess.run(["gcloud", "storage", "cp", video.uri, str(dest)], check=True)
    else:
        raise RuntimeError(f"Unknown video payload: {video!r}")
    strip_audio(dest)


def contact_sheet(mp4: Path, dest: Path, labels: list[str] | None = None) -> list[float]:
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(mp4)]
    )
    dur = float(json.loads(probe)["format"]["duration"])
    times = [0.05, dur / 3, 2 * dur / 3, max(0.05, dur - 0.08)]
    frames: list[Image.Image] = []
    WORK.mkdir(parents=True, exist_ok=True)
    for i, t in enumerate(times):
        p = WORK / f"_cs_{mp4.stem}_{i}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(p)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        frames.append(Image.open(p).convert("RGB"))
    h = max(im.height for im in frames) // 2
    resized = [im.resize((int(im.width * h / im.height), h)) for im in frames]
    gap = 8
    w = sum(im.width for im in resized) + gap * (len(resized) - 1)
    sheet = Image.new("RGB", (w, h + 40), (12, 12, 16))
    draw = ImageDraw.Draw(sheet)
    x = 0
    for im, t in zip(resized, times):
        sheet.paste(im, (x, 32))
        draw.text((x + 4, 4), f"{t:.2f}s", fill=(220, 220, 230))
        x += im.width + gap
    if labels:
        draw.text((4, h + 20), " | ".join(labels), fill=(180, 180, 190))
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    return times


def main() -> None:
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    client = genai.Client(
        vertexai=True,
        project=PROJECT,
        location=LOCATION,
        http_options={"api_version": "v1"},
    )
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)
    CONTACT.mkdir(parents=True, exist_ok=True)

    bare = make_bare_planet_still(client)
    CLIPS_SPEC[1]["still"] = bare

    manifest: dict = {
        "engine": "vertex",
        "project": PROJECT,
        "model": MODEL,
        "ben_order": "2026-10-01T11:15 London — Veo v05 world re-runs; Orbit never Veo",
        "duration_seconds": DURATION,
        "clips": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    for spec in CLIPS_SPEC:
        still = Path(spec["still"])
        dest = OUT / spec["file"]
        if not still.is_file():
            raise SystemExit(f"missing still {still}")
        generate_veo(client, spec["prompt"], still, dest)
        if dest.stat().st_size < 50_000:
            raise SystemExit(f"too small {dest}")
        chunk_write(dest, UAT / dest.name)
        cs = CONTACT / f"{dest.stem}_contact.png"
        times = contact_sheet(dest, cs)
        chunk_write(cs, UAT / cs.name)
        row = {
            "file": dest.name,
            "still": still.name,
            "still_sha256": sha256(still),
            "sha256": sha256(dest),
            "bytes": dest.stat().st_size,
            "contact": cs.name,
            "contact_times": times,
            "section6": "N/A world plate — no Orbit (Veo)",
            "estimated_usd": round(DURATION * USD_PER_SECOND, 4),
        }
        manifest["clips"].append(row)
        print(f"  wrote {dest.name} sha={row['sha256'][:12]}…", flush=True)

    n = len(manifest["clips"])
    manifest["estimated_usd_list_price"] = round(n * DURATION * USD_PER_SECOND, 4)
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST_VEO.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write((OUT / "MANIFEST_VEO.json").read_bytes(), UAT / "MANIFEST_VEO.json")
    print(json.dumps({"VEO_V05_DONE": True, **{k: manifest[k] for k in ("estimated_usd_list_price",)}}, indent=2))


if __name__ == "__main__":
    main()
