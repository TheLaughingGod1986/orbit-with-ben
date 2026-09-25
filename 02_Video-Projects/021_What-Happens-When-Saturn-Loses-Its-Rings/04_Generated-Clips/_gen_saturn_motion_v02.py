#!/usr/bin/env python3
"""Saturn picture rebuild. Unique Veo Fast motion. No Flow. No still holds.

World plates are image-to-video from the locked stills. Orbit is two Omni
beats only. Each file is a new generation, played once. Audio is stripped.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_omni import generate_omni_clip  # noqa: E402
from orbit_gemini_veo import resolve_api_key, strip_audio  # noqa: E402
from orbit_voice import CG_SILENT_AUDIO_BLOCK  # noqa: E402

from google import genai
from google.genai import types

EP = REPO / "02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings"
STILLS = EP / "04_Generated-Clips/stills_v01"
OUT = EP / "04_Generated-Clips/veo_motion_v02"
ENV = REPO / "02_Video-Projects/019_Andromeda-Milky-Way-Collision/07_Edit-Project/.env"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
MODEL = "veo-3.1-fast-generate-preview"

NEG_WORLD = (
    "robot, mascot, orange character, spacecraft, probe, satellite, lander, rocket, "
    "text, captions, logos, watermark, second planet, Earth, people, speech, narration, "
    "twin, clone, crowd of ships"
)
NEG_CASSINI = (
    "robot, mascot, orange character, second spacecraft, second probe, lander, rocket, "
    "text, captions, logos, watermark, second planet, Earth, people, speech, narration"
)

MOVES = [
    "The camera drifts slowly along the ring plane.",
    "The camera pushes gently closer.",
    "The camera slides sideways, parallax on the ice.",
    "The camera rises slightly and looks along the sheet.",
    "The camera eases back, revealing more of the one planet.",
    "Particles stream past the lens. The camera stays slow.",
    "The camera banks a few degrees and continues forward.",
    "The camera descends toward the inner edge.",
]


def world_prompt(subject: str, move: str, cassini: bool) -> str:
    craft = (
        "Exactly one spacecraft, the Cassini orbiter already in frame: gold body, "
        "one large white radio dish, three thin antennae. Do not add a second craft. "
        if cassini
        else "No spacecraft. No robot. "
    )
    return (
        f"{subject} {move} Continuous motion for the whole shot. "
        f"One Saturn only, the same pale-gold banded planet. {craft}"
        "No readable text. Silent picture. " + CG_SILENT_AUDIO_BLOCK
    )


# Counts cover the spoken film at native 8s plays. No loops, no freezes.
POOLS: list[dict] = [
    {
        "pool": "rings",
        "n": 15,
        "still": "saturn_open_rings_v01.png",
        "cassini": False,
        "subject": (
            "Saturn's thin bright ice rings. Chunks and grains move on their own paths "
            "and drift inward. The sheet stays thin, not a solid disc."
        ),
    },
    {
        "pool": "ice",
        "n": 11,
        "still": "saturn_ice_chunks_v01.png",
        "cassini": False,
        "subject": (
            "Close on water-ice chunks in Saturn's rings, grains to house-sized boulders, "
            "some cream and some tan with a little dust. They circle. They do not sit."
        ),
    },
    {
        "pool": "rain",
        "n": 8,
        "still": "saturn_open_rings_v01.png",
        "cassini": False,
        "subject": (
            "The smallest ice grains lift off Saturn's ring plane and fall inward along "
            "faint magnetic paths into the pale cloud tops. The sheet thins. No spacecraft."
        ),
    },
    {
        "pool": "cassini",
        "n": 11,
        "still": "saturn_ring_rain_cassini_v01.png",
        "cassini": True,
        "subject": (
            "The same one Cassini orbiter flies the gap between Saturn's inner rings and "
            "the cloud tops. Ice grains fall past it. The gold dish stays the only craft."
        ),
    },
    {
        "pool": "young",
        "n": 8,
        "still": "saturn_young_rings_v01.png",
        "cassini": False,
        "subject": (
            "A younger, broader, brighter white ice sheet around the same one Saturn. "
            "Cleaner ice. No second planet."
        ),
    },
    {
        "pool": "moon",
        "n": 4,
        "still": "saturn_young_rings_v01.png",
        "cassini": False,
        "subject": (
            "Inside the Roche limit, one small icy moon pulls apart into rubble that "
            "spreads into a flat ring around the same one Saturn. No second planet."
        ),
    },
    {
        "pool": "bare",
        "n": 14,
        "still": "saturn_bare_v01.png",
        "cassini": False,
        "subject": (
            "Saturn with no rings. Pale gold bands slide in a fast atmosphere. "
            "The curve of the planet is clean. No ring shadow. No spacecraft."
        ),
    },
]

OMNI = [
    {
        "file": "orbit_along_v01.mp4",
        "still": "saturn_orbit_along_rings_v01.png",
        "prompt": (
            "Exactly one Orbit, the matte orange floater, looks along Saturn's ice rings "
            "and drifts with them. One black visor, two cream eyes with dark pupils, "
            "stubby arms, one antenna, one soft underside glow. He is small in the rings, "
            "not a sticker. Solid orange back if he turns. No second Orbit, no second face, "
            "no legs, no twin thrusters. The rings and one Saturn move behind him. Silent picture."
        ),
    },
    {
        "file": "orbit_bare_v01.mp4",
        "still": "saturn_orbit_bare_v01.png",
        "prompt": (
            "Exactly one tiny Orbit hangs in the later sky beside bare Saturn, no rings. "
            "Matte orange, one black visor, cream eyes with dark pupils, one underside glow. "
            "He is a small figure, not the hero. Saturn's bands keep moving. "
            "No second Orbit, no second face, no legs, no spacecraft, no ring. Silent picture."
        ),
    },
]


def client() -> genai.Client:
    key = resolve_api_key(ENV)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = key
    return genai.Client(api_key=key)


def generate_world(cli: genai.Client, prompt: str, still: Path, dest: Path, cassini: bool) -> None:
    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=NEG_CASSINI if cassini else NEG_WORLD,
    )
    print(f"submit {dest.name}", flush=True)
    t0 = time.time()
    operation = cli.models.generate_videos(
        model=MODEL,
        source=types.GenerateVideosSource(prompt=prompt, image=img),
        config=config,
    )
    while not operation.done:
        time.sleep(12)
        operation = cli.operations.get(operation)
        print(f"  poll {dest.stem} {int(time.time() - t0)}s", flush=True)
    if operation.error:
        raise RuntimeError(f"Veo error: {operation.error}")
    response = operation.response
    if not response or not response.generated_videos:
        raise RuntimeError("Veo returned no videos")
    video = response.generated_videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    cli.files.download(file=video.video)
    video.video.save(str(dest))
    strip_audio(dest)


def jobs(only: str | None) -> list[dict]:
    rows = []
    for pool in POOLS:
        if only and pool["pool"] != only:
            continue
        still = STILLS / pool["still"]
        for i in range(pool["n"]):
            rows.append({
                "file": f"{pool['pool']}_{i:02d}.mp4",
                "still": str(still),
                "prompt": world_prompt(pool["subject"], MOVES[i % len(MOVES)], pool["cassini"]),
                "cassini": pool["cassini"],
                "kind": "veo",
            })
    if only in (None, "orbit"):
        for spec in OMNI:
            rows.append({
                "file": spec["file"],
                "still": str(STILLS / spec["still"]),
                "prompt": spec["prompt"],
                "cassini": False,
                "kind": "omni",
            })
    return rows


def main() -> None:
    only = None
    worker = 0
    workers = 1
    limit = 0
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--only":
            only = args[i + 1]
            i += 2
        elif args[i] == "--worker":
            worker = int(args[i + 1])
            workers = int(args[i + 2])
            i += 3
        elif args[i] == "--limit":
            limit = int(args[i + 1])
            i += 2
        else:
            raise SystemExit(f"unknown arg {args[i]}")
    OUT.mkdir(parents=True, exist_ok=True)
    cli = client()
    manifest = []
    selected = [row for n, row in enumerate(jobs(only)) if n % workers == worker]
    if limit:
        selected = selected[:limit]
    print(f"jobs {len(selected)} worker {worker}/{workers}", flush=True)
    for row in selected:
        dest = OUT / row["file"]
        if dest.exists() and dest.stat().st_size > 100_000:
            print(f"skip {row['file']}", flush=True)
            manifest.append({"file": row["file"], "skipped": True, "bytes": dest.stat().st_size})
            continue
        last_error = ""
        for attempt in range(8):
            try:
                if row["kind"] == "omni":
                    generate_omni_clip(
                        cli,
                        row["prompt"],
                        dest,
                        orbit_ref=Path(row["still"]),
                        identity_ref=ORBIT_REF,
                        aspect_ratio="16:9",
                    )
                    strip_audio(dest)
                else:
                    generate_world(cli, row["prompt"], Path(row["still"]), dest, row["cassini"])
                last_error = ""
                break
            except Exception as exc:
                last_error = str(exc)
                if "429" not in last_error and "RESOURCE_EXHAUSTED" not in last_error:
                    break
                wait = min(180, 25 * (attempt + 1))
                print(f"  quota {dest.name} attempt {attempt + 1} wait {wait}s", flush=True)
                time.sleep(wait)
        if last_error:
            print(f"FAIL {row['file']}: {last_error}", flush=True)
            manifest.append({"file": row["file"], "error": last_error})
            if dest.exists() and dest.stat().st_size < 100_000:
                dest.unlink()
            if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                print("STOP quota exhausted. Existing clips kept. UAT not replaced.", flush=True)
                break
            continue
        try:
            manifest.append({
                "file": row["file"],
                "bytes": dest.stat().st_size,
                "model": MODEL if row["kind"] == "veo" else "gemini-omni-flash-preview",
                "audio_stripped": True,
            })
            print(f"  wrote {dest.name} {dest.stat().st_size}", flush=True)
        except Exception as exc:
            print(f"FAIL {row['file']}: {exc}", flush=True)
            manifest.append({"file": row["file"], "error": str(exc)})
            if dest.exists() and dest.stat().st_size < 100_000:
                dest.unlink()
    stamp = OUT / f"MANIFEST_w{worker}.json"
    stamp.write_text(json.dumps(manifest, indent=2))
    failed = [m for m in manifest if m.get("error")]
    print(f"DONE worker {worker} fail {len(failed)}", flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
