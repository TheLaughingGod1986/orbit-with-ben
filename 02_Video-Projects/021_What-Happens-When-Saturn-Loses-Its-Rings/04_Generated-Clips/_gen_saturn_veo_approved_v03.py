#!/usr/bin/env python3
"""Saturn Veo Fast — ONLY the two Ben-approved stills (Round 3). Vertex Free Trial.

Approved:
  - young rings (stills_v01/saturn_young_rings_v01.png)
  - Cassini (stills_v03/saturn_ring_rain_cassini_v03.png) — white dish, no craft shadow

8s · 16:9 · generate_audio=False · strip audio after download.
Never AI Studio prepay / never GEMINI_API_KEY for this pass.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import strip_audio  # noqa: E402
from orbit_voice import CG_SILENT_AUDIO_BLOCK  # noqa: E402

from google import genai
from google.genai import types

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
OUT = EP / "04_Generated-Clips" / "veo_approved_v03"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_veo_approved_v03"
)

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
# Vertex GA Fast (not AI Studio preview id)
MODEL = "veo-3.1-fast-generate-001"
# Vertex list price ballpark for Veo 3 Fast video (USD per second of output). Report after run.
USD_PER_SECOND = 0.15
DURATION = 8

CLIPS = [
    {
        "file": "veo_young_rings_v03.mp4",
        "still": EP
        / "04_Generated-Clips"
        / "stills_v01"
        / "saturn_young_rings_v01.png",
        "prompt": (
            "Continuous slow move along a younger, broader, brighter white ice sheet around "
            "the same one Saturn. Cleaner ice gleams. Soft camera drift along the ring plane. "
            "No robot, no spacecraft, no text, no second planet, no Earth. Silent picture."
        ),
    },
    {
        "file": "veo_cassini_ring_rain_v03.mp4",
        "still": EP
        / "04_Generated-Clips"
        / "stills_v03"
        / "saturn_ring_rain_cassini_v03.png",
        "prompt": (
            "Continuous motion from this still: pale fine ice grains fall from the thin ring line "
            "down into Saturn's butterscotch cloud tops as ring rain. "
            "Exactly one Cassini spacecraft already in frame — WHITE high-gain dish, gold foil on the body only — "
            "drifts slowly between the rings and the planet. Do not cast a craft shadow on the clouds. "
            "Do not add a second craft. No robot, no text, no second planet. Silent picture."
        ),
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_one(client: genai.Client, prompt: str, still: Path, dest: Path) -> None:
    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=DURATION,
        aspect_ratio="16:9",
        resolution="720p",
        generate_audio=False,
        negative_prompt=(
            "robot, mascot, orange character, text, captions, logos, watermark, "
            "second planet, Earth, people, speech, narration, second spacecraft"
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
    videos = None
    if response is not None:
        videos = getattr(response, "generated_videos", None)
    if not videos:
        # some SDK shapes nest under result
        result = getattr(operation, "result", None)
        videos = getattr(result, "generated_videos", None) if result else None
    if not videos:
        raise RuntimeError(f"Veo returned no videos: {operation}")
    video = videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Download — Vertex may return bytes or a file handle
    v = video.video
    if hasattr(client.files, "download"):
        try:
            client.files.download(file=v)
        except Exception as e:
            print(f"  download note: {e}", flush=True)
    if hasattr(v, "save"):
        v.save(str(dest))
    elif getattr(v, "video_bytes", None):
        dest.write_bytes(v.video_bytes)
    elif getattr(v, "uri", None):
        # GCS URI — fetch via gsutil / google storage
        uri = v.uri
        print(f"  fetching uri {uri}", flush=True)
        import subprocess

        subprocess.run(["gcloud", "storage", "cp", uri, str(dest)], check=True)
    else:
        raise RuntimeError(f"Unknown video payload: {v!r}")
    strip_audio(dest)


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

    manifest: dict = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "duration_seconds": DURATION,
        "usd_per_second_list_estimate": USD_PER_SECOND,
        "clips": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    for spec in CLIPS:
        still = spec["still"]
        dest = OUT / spec["file"]
        if not still.is_file():
            raise SystemExit(f"missing still {still}")
        generate_one(client, spec["prompt"], still, dest)
        if dest.stat().st_size < 50_000:
            raise SystemExit(f"too small {dest}")
        uat_dest = UAT / spec["file"]
        uat_dest.write_bytes(dest.read_bytes())
        h = sha256(dest)
        row = {
            "file": spec["file"],
            "still": str(still),
            "bytes": dest.stat().st_size,
            "sha256": h,
            "model": MODEL,
            "engine": "vertex",
            "audio_stripped": True,
            "duration_seconds": DURATION,
            "estimated_usd": round(DURATION * USD_PER_SECOND, 4),
            "path": str(dest),
            "uat_path": str(uat_dest),
        }
        manifest["clips"].append(row)
        print(f"  wrote {dest.stat().st_size} sha={h}", flush=True)

    n = len(manifest["clips"])
    manifest["clips_count"] = n
    manifest["estimated_usd_list_price"] = round(n * DURATION * USD_PER_SECOND, 4)
    manifest["billing_note"] = (
        f"Vertex Free Trial {PROJECT}; model {MODEL}; "
        f"list estimate ${USD_PER_SECOND}/s × {DURATION}s × {n} clips = "
        f"${manifest['estimated_usd_list_price']:.2f}. Not AI Studio prepay."
    )
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "README.md").write_text(
        f"""# Saturn Veo approved v03 — young rings + Cassini

Ben Round 3: Veo ONLY on these two approved stills. Vertex `{MODEL}`. Audio stripped.

| Clip | Still |
|---|---|
| `veo_young_rings_v03.mp4` | `saturn_young_rings_v01.png` |
| `veo_cassini_ring_rain_v03.mp4` | `saturn_ring_rain_cassini_v03.png` |

Estimated list cost: **${manifest['estimated_usd_list_price']:.2f}**
"""
    )
    print(json.dumps({"VEO_APPROVED_V03_DONE": True, **{k: manifest[k] for k in ("estimated_usd_list_price", "clips_count", "model")}}, indent=2), flush=True)


if __name__ == "__main__":
    main()
