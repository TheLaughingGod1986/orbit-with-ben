#!/usr/bin/env python3
"""Saturn world plates on Veo Fast. Image-to-video from stills. No Orbit binding. No Flow."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import resolve_api_key, strip_audio
from orbit_voice import CG_SILENT_AUDIO_BLOCK

from google import genai
from google.genai import types

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
STILLS = EP / "04_Generated-Clips" / "stills_v01"
OUT = EP / "04_Generated-Clips" / "veo_world_v01"
ENV = REPO / "02_Video-Projects" / "019_Andromeda-Milky-Way-Collision" / "07_Edit-Project" / ".env"
MODEL = "veo-3.1-fast-generate-preview"

CLIPS = [
    {
        "file": "veo_open_rings_v01.mp4",
        "still": "saturn_open_rings_v01.png",
        "prompt": (
            "Continuous slow drift through Saturn's thin ice ring plane. Pale ice particles move inward "
            "toward the one pale-gold planet. The sheet stays thin. No robot, no spacecraft, no text, no second planet. "
        ),
    },
    {
        "file": "veo_ring_rain_v01.mp4",
        "still": "saturn_ring_rain_cassini_v01.png",
        "prompt": (
            "Continuous motion: pale ice grains fall from the ring line down into Saturn's cloud tops. "
            "Exactly one Cassini spacecraft, the gold dish already in frame, drifts between the rings and the planet. "
            "Do not add a second craft. No robot, no text, no second planet. "
        ),
    },
    {
        "file": "veo_young_rings_v01.mp4",
        "still": "saturn_young_rings_v01.png",
        "prompt": (
            "Continuous slow move along a younger, brighter white ice sheet around the same one Saturn. "
            "The rings gleam. No robot, no spacecraft, no text, no second planet. "
        ),
    },
]


def generate_world(client, prompt: str, still: Path, dest: Path) -> None:
    img = types.Image.from_file(location=str(still))
    # Developer API has no generate_audio switch. Prompt stays silent; strip whatever comes back.
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=(
            "robot, mascot, orange character, text, captions, logos, watermark, "
            "second planet, Earth, people, speech, narration"
        ),
    )
    full = prompt.strip() + " " + CG_SILENT_AUDIO_BLOCK
    print(f"submit {dest.name} model={MODEL}", flush=True)
    t0 = time.time()
    operation = client.models.generate_videos(
        model=MODEL,
        source=types.GenerateVideosSource(prompt=full, image=img),
        config=config,
    )
    while not operation.done:
        time.sleep(12)
        operation = client.operations.get(operation)
        print(f"  poll {dest.stem} {int(time.time() - t0)}s", flush=True)
    if operation.error:
        raise RuntimeError(f"Veo error: {operation.error}")
    response = operation.response
    if not response or not response.generated_videos:
        raise RuntimeError("Veo returned no videos")
    video = response.generated_videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    strip_audio(dest)


def main() -> None:
    key = resolve_api_key(ENV)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = key
    client = genai.Client(api_key=key)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for spec in CLIPS:
        dest = OUT / spec["file"]
        still = STILLS / spec["still"]
        if dest.exists() and dest.stat().st_size > 100_000:
            print(f"skip {spec['file']}", flush=True)
            manifest.append({"file": spec["file"], "bytes": dest.stat().st_size, "skipped": True})
            continue
        if not still.exists():
            raise SystemExit(f"missing still {still}")
        try:
            generate_world(client, spec["prompt"], still, dest)
            manifest.append({
                "file": spec["file"],
                "still": spec["still"],
                "bytes": dest.stat().st_size,
                "model": MODEL,
                "audio_stripped": True,
                "orbit_bound": False,
            })
            print(f"  wrote {dest.stat().st_size}", flush=True)
        except Exception as exc:
            print(f"FAIL {spec['file']}: {exc}", flush=True)
            manifest.append({"file": spec["file"], "error": str(exc)})
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print("VEO_DONE", flush=True)


if __name__ == "__main__":
    main()
