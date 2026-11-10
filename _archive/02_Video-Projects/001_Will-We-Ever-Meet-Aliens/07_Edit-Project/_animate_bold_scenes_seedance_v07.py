#!/usr/bin/env python3
"""Animate bold scenes via Seedance 2.0 Mini on fal — resumable.

Bypasses fal CDN upload (currently 403) by hosting each PNG on litterbox,
then submitting image_url to the fal queue API.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import re
import time
import urllib.request
from pathlib import Path

import httpx


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SCENES = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/scenes"
OUT = ROOT / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
MANIFEST = ROOT / "07_Edit-Project/bold-explainer-v07-seedance-animate-manifest.json"
PROGRESS = ROOT / "07_Edit-Project/bold-explainer-v07-seedance-progress.jsonl"
MODEL_PATH = "bytedance/seedance-2.0/mini/image-to-video"
QUEUE_SUBMIT = f"https://queue.fal.run/{MODEL_PATH}"
DURATION = "5"
RESOLUTION = "720p"
WORKERS = 3
POLL_SEC = 4
TIMEOUT_SEC = 600

BOARD_MOTION = {
    1: "slow push into a silent crowded night sky, soft star drift, faint signal-wave shimmer",
    2: "gentle drift along a light-year corridor, tiny probe motion, scale lines breathing",
    3: "ancient light travelling across a galaxy map, cities rising and fading as soft glows",
    4: "quiet expansion-wave ripple across an empty galactic diagram, contemplative stillness",
    5: "exoplanet catalogue filling with soft appearing worlds, transit shadow drifting",
    6: "habitable-zone orbit motion, atmosphere shimmer on temperate and hostile worlds",
    7: "Drake-chain stages lighting in sequence, clock-hand and forming-star motion",
    8: "deep-time ocean chemistry drift, microbial aeons, a tiny late radio-era spark",
    9: "rare-intelligence bottleneck reveal, one world turning to look back",
    10: "great-filter threshold crossing as luminous gate, cautious hopeful light",
    11: "fragile civilisation systems stressing, lights fading with restrained concern",
    12: "noisy city dimming into efficient quiet society, observational invisibility",
    13: "two radio bubbles narrowly missing across time, dark interval between eras",
    14: "distant observer motif, young world protected, future red-star lights switching on",
    15: "four unresolved scientific paths converging with soft doorway light",
    16: "technosignature fingerprints: radio line, laser pulse, atmosphere, waste-heat glow",
    17: "1977 Wow! pulse spike then empty repeats, evidence stamp remaining unconfirmed",
    18: "teaspoon against an ocean of unsearched sky-frequency grid, incomplete listening",
    19: "planet transit and prism spectrum growing molecular fingerprints",
    20: "evidence ladder climbing from ambiguous chemistry to converging telescopes",
    21: "Martian rivers, Europa ice cracks, Enceladus plume sampling, ice-grain microbe hint",
    22: "populated galaxy that still looks dark, reframing the paradox gently",
    23: "modern tools activating: counting worlds, reading atmospheres, listening, analysing ice",
    24: "archive anomaly resolving into a readable pattern, silence becoming data",
}


def fal_key() -> str:
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    if not key:
        raise SystemExit("FAL_KEY not set")
    return key


def board_for(path: Path) -> int:
    name = path.name
    if "board-" in name:
        return int(re.search(r"board-(\d+)", name).group(1))
    num = int(re.search(r"scene-(\d+)", name).group(1))
    return (num - 1) // 4 + 1


def prompt_for(path: Path) -> str:
    motion = BOARD_MOTION[board_for(path)]
    return (
        "Hand-painted editorial science illustration gently comes alive. "
        f"{motion}. "
        "Stable cinematic camera, smooth and locked — no handheld shake. "
        "Preserve exact composition, colours, paper grain, and illustrated style. "
        "Subtle atmospheric drift and light travel only. "
        "No text, letters, numbers, logos, watermarks, humanoid aliens, or new objects. "
        "Do not morph the artwork into photorealism."
    )


def out_path(source: Path) -> Path:
    return OUT / f"{source.stem}_seedance-mini.mp4"


def is_ready(source: Path) -> bool:
    dest = out_path(source)
    return dest.exists() and dest.stat().st_size > 100_000


def append_progress(record: dict) -> None:
    with PROGRESS.open("a") as handle:
        handle.write(json.dumps(record) + "\n")


def host_image(source: Path) -> str:
    """Public temp URL so fal can fetch the PNG without fal CDN auth."""
    with source.open("rb") as handle:
        response = httpx.post(
            "https://litterbox.catbox.moe/resources/internals/api.php",
            data={"reqtype": "fileupload", "time": "12h"},
            files={"fileToUpload": (source.name, handle, "image/png")},
            timeout=180,
        )
    text = response.text.strip()
    if response.status_code >= 400 or not text.startswith("http"):
        raise RuntimeError(f"litterbox upload failed: {response.status_code} {text[:200]}")
    return text


def queue_generate(image_url: str, prompt: str) -> dict:
    headers = {
        "Authorization": f"Key {fal_key()}",
        "Content-Type": "application/json",
    }
    submit = httpx.post(
        QUEUE_SUBMIT,
        headers=headers,
        json={
            "prompt": prompt,
            "image_url": image_url,
            "resolution": RESOLUTION,
            "duration": DURATION,
            "aspect_ratio": "16:9",
            "generate_audio": False,
        },
        timeout=60,
    )
    if submit.status_code >= 400:
        raise RuntimeError(f"queue submit {submit.status_code}: {submit.text[:400]}")
    payload = submit.json()
    request_id = payload["request_id"]
    status_url = payload.get("status_url") or (
        f"https://queue.fal.run/bytedance/seedance-2.0/requests/{request_id}/status"
    )
    response_url = payload.get("response_url") or (
        f"https://queue.fal.run/bytedance/seedance-2.0/requests/{request_id}"
    )

    started = time.time()
    while True:
        status = httpx.get(status_url, headers=headers, timeout=30).json()
        state = status.get("status")
        if state == "COMPLETED":
            result = httpx.get(response_url, headers=headers, timeout=60).json()
            result["request_id"] = request_id
            return result
        if state in {"FAILED", "ERROR", "CANCELLED"}:
            raise RuntimeError(f"queue {state}: {status}")
        if time.time() - started > TIMEOUT_SEC:
            raise TimeoutError(f"queue timeout after {TIMEOUT_SEC}s ({state})")
        time.sleep(POLL_SEC)


def animate_one(source: Path) -> dict:
    dest = out_path(source)
    if is_ready(source):
        return {
            "scene": source.name,
            "status": "skipped",
            "output": str(dest),
            "bytes": dest.stat().st_size,
        }

    print(f"START {source.name}", flush=True)
    image_url = host_image(source)
    result = queue_generate(image_url, prompt_for(source))
    video_url = result["video"]["url"]
    tmp = dest.with_suffix(".partial.mp4")
    urllib.request.urlretrieve(video_url, tmp)
    tmp.replace(dest)
    record = {
        "scene": source.name,
        "status": "generated",
        "output": str(dest),
        "bytes": dest.stat().st_size,
        "seed": result.get("seed"),
        "request_id": result.get("request_id"),
        "video_url": video_url,
        "image_url": image_url,
    }
    append_progress(record)
    print(f"DONE  {source.name} ({dest.stat().st_size} bytes)", flush=True)
    return record


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = sorted(SCENES.glob("scene-*.png"))
    if len(sources) != 96:
        raise SystemExit(f"Expected 96 scenes, found {len(sources)}")

    pending = [src for src in sources if not is_ready(src)]
    print(
        f"Ready: {96 - len(pending)} / 96; generating {len(pending)} "
        f"with {WORKERS} workers (litterbox + fal queue)",
        flush=True,
    )
    started = time.time()
    results: list[dict] = []
    failures: list[dict] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        future_map = {pool.submit(animate_one, src): src for src in pending}
        for fut in concurrent.futures.as_completed(future_map):
            src = future_map[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                record = {"scene": src.name, "status": "error", "error": str(exc)}
                failures.append(record)
                append_progress(record)
                print(f"FAIL  {src.name}: {exc}", flush=True)

    ready_n = sum(1 for src in sources if is_ready(src))
    manifest = {
        "model": MODEL_PATH,
        "duration": DURATION,
        "resolution": RESOLUTION,
        "transport": "litterbox+fal-queue",
        "elapsed_seconds": round(time.time() - started, 1),
        "ready_clips": ready_n,
        "failures": failures,
        "results": results,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "ready_clips": ready_n,
        "failures": len(failures),
        "elapsed_seconds": manifest["elapsed_seconds"],
        "manifest": str(MANIFEST),
    }, indent=2), flush=True)
    if ready_n < 96:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
