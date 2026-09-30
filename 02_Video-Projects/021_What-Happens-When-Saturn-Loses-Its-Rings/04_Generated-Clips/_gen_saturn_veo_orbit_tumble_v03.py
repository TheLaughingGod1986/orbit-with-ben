#!/usr/bin/env python3
"""Saturn Veo Fast — APPROVED Orbit-in-rings tumble (Ben 30 Sep 22:46). Vertex Free Trial.

Still: stills_v04/saturn_orbit_tumble_v04.png (APPROVED)
Motion: slow drift, Orbit tumbling and grabbing the chunk, ice floating past camera.
8s · 16:9 · generate_audio=False · strip audio. Append to veo_approved_v03 pack.
Never AI Studio prepay.
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
STILL = EP / "04_Generated-Clips" / "stills_v04" / "saturn_orbit_tumble_v04.png"
FILE = "veo_orbit_tumble_v03.mp4"

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "veo-3.1-fast-generate-001"
USD_PER_SECOND = 0.15
DURATION = 8

PROMPT = (
    "Continuous slow camera drift through this sparse ring ice. "
    "Exactly ONE orange Orbit robot stays on-model from the still: "
    "matte/glossy metallic orange rounded floater, large black curved visor, "
    "two cream eyes with dark pupils, stubby arms, one antenna with glowing tip, "
    "ONE soft underside glow only. "
    "Orbit tumbles slowly mid-air and grabs / reaches for the nearby ice chunk with one hand. "
    "Sparse white ice chunks float past the camera at different depths with black space around them. "
    "Saturn and rings stay in the background. "
    "No second Orbit, no second face, no waving hello, no sitting on ice, no text, no spacecraft. "
    "Silent picture."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src_bytes: bytes, dest: Path) -> None:
    """Write via temp + rename; avoid iCloud EDEADLK empty placeholders."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    chunk = 500 * 1024
    with open(tmp, "wb") as o:
        for i in range(0, len(src_bytes), chunk):
            o.write(src_bytes[i : i + chunk])
            o.flush()
    tmp.replace(dest)


def generate_one(client: genai.Client, dest: Path) -> None:
    img = types.Image.from_file(location=str(STILL))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=DURATION,
        aspect_ratio="16:9",
        resolution="720p",
        generate_audio=False,
        negative_prompt=(
            "second robot, twin Orbit, second face, waving, sitting on ice, standing on ice, "
            "text, captions, logos, watermark, second planet, Earth, people, speech, narration, "
            "spacecraft, Cassini"
        ),
    )
    full = PROMPT.strip() + " " + CG_SILENT_AUDIO_BLOCK
    print(f"submit {dest.name} model={MODEL} still={STILL.name}", flush=True)
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
        result = getattr(operation, "result", None)
        videos = getattr(result, "generated_videos", None) if result else None
    if not videos:
        raise RuntimeError(f"Veo returned no videos: {operation}")
    video = videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
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
        import subprocess

        print(f"  fetching uri {v.uri}", flush=True)
        subprocess.run(["gcloud", "storage", "cp", v.uri, str(dest)], check=True)
    else:
        raise RuntimeError(f"Unknown video payload: {v!r}")
    strip_audio(dest)


def main() -> None:
    if not STILL.is_file():
        raise SystemExit(f"missing still {STILL}")

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

    dest = OUT / FILE
    generate_one(client, dest)
    if dest.stat().st_size < 50_000:
        raise SystemExit(f"too small {dest}")

    h = sha256(dest)
    data = dest.read_bytes()
    uat_dest = UAT / FILE
    chunk_write(data, uat_dest)
    if sha256(uat_dest) != h:
        # retry once
        chunk_write(data, uat_dest)
    if sha256(uat_dest) != h:
        raise SystemExit(f"UAT sha mismatch {uat_dest}")

    row = {
        "file": FILE,
        "still": str(STILL),
        "bytes": dest.stat().st_size,
        "sha256": h,
        "model": MODEL,
        "engine": "vertex",
        "audio_stripped": True,
        "duration_seconds": DURATION,
        "estimated_usd": round(DURATION * USD_PER_SECOND, 4),
        "path": str(dest),
        "uat_path": str(uat_dest),
        "ben_approved": "2026-09-30T22:46+01:00",
        "motion": "slow drift; Orbit tumbling and grabbing chunk; ice floating past camera",
    }

    # Merge into existing MANIFEST if present
    man_path = OUT / "MANIFEST.json"
    if man_path.is_file():
        manifest = json.loads(man_path.read_text())
    else:
        manifest = {
            "engine": "vertex",
            "project": PROJECT,
            "location": LOCATION,
            "model": MODEL,
            "ai_studio_prepay": False,
            "duration_seconds": DURATION,
            "usd_per_second_list_estimate": USD_PER_SECOND,
            "clips": [],
        }
    clips = [c for c in manifest.get("clips", []) if c.get("file") != FILE]
    clips.append(row)
    manifest["clips"] = clips
    manifest["clips_count"] = len(clips)
    manifest["estimated_usd_list_price"] = round(
        sum(c.get("estimated_usd", DURATION * USD_PER_SECOND) for c in clips), 4
    )
    manifest["billing_note"] = (
        f"Vertex Free Trial {PROJECT}; model {MODEL}; "
        f"list estimate includes Orbit tumble + prior approved clips. Not AI Studio prepay."
    )
    manifest["orbit_tumble_finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(man_path.read_bytes(), UAT / "MANIFEST.json")
    (OUT / "README.md").write_text(
        f"""# Saturn Veo approved v03

Vertex `{MODEL}` · audio stripped · Free Trial only.

| Clip | Still |
|---|---|
| `veo_young_rings_v03.mp4` | young rings v01 |
| `veo_cassini_ring_rain_v03.mp4` | Cassini v03 |
| `veo_orbit_tumble_v03.mp4` | Orbit tumble v04 APPROVED |

Estimated pack list cost: **${manifest['estimated_usd_list_price']:.2f}**
"""
    )
    chunk_write((OUT / "README.md").read_bytes(), UAT / "README.md")
    print(
        json.dumps(
            {
                "VEO_ORBIT_TUMBLE_DONE": True,
                "file": FILE,
                "sha256": h,
                "bytes": dest.stat().st_size,
                "estimated_usd": row["estimated_usd"],
                "pack_estimated_usd": manifest["estimated_usd_list_price"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
