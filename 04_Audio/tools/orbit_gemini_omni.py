#!/usr/bin/env python3
"""Orbit CG via Gemini Omni Flash API (gemini-omni-flash-preview).

Primary picture path for Omni-forward longs.
Flow Playwright is backup only when this API is down.
Not ElevenLabs Image & Video.
Keeps native Omni SFX unless the caller strips audio.
"""
from __future__ import annotations

import base64
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ORBIT_REF = (
    REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
DEFAULT_MODEL = "gemini-omni-flash-preview"

SFX_LOCK = (
    " Native space rumble and whoosh SFX only. No speech, no narration, no lyrics, "
    "no readable text, no logo, no title."
)


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def _video_bytes(interaction) -> bytes:
    ov = getattr(interaction, "output_video", None)
    if ov is not None:
        data = getattr(ov, "data", None)
        if data:
            raw = data if isinstance(data, (bytes, bytearray)) else base64.b64decode(data)
            if len(raw) > 50_000:
                return bytes(raw)
        uri = getattr(ov, "uri", None)
        if uri:
            raise RuntimeError(f"URI delivery not downloaded: {uri}")
    steps = getattr(interaction, "steps", None) or []
    for step in steps:
        contents = getattr(step, "content", None) or []
        if isinstance(step, dict):
            contents = step.get("content") or []
        for item in contents:
            if isinstance(item, dict):
                if item.get("type") == "video" and item.get("data"):
                    return base64.b64decode(item["data"])
            else:
                if getattr(item, "type", None) == "video" and getattr(item, "data", None):
                    data = item.data
                    return data if isinstance(data, (bytes, bytearray)) else base64.b64decode(data)
    raise RuntimeError("Omni API returned no video bytes")


def generate_omni_clip(
    client,
    prompt: str,
    dest: Path,
    *,
    orbit_ref: Path | None = None,
    identity_ref: Path | None = None,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "16:9",
) -> dict:
    """One ~8s Omni Flash clip.

    orbit_ref is the I2V start frame (composition). identity_ref is the
    canonical Orbit still, attached as a second image when the start frame
    is not already that still — so scale/camera stay locked without turning
    Orbit into a knockoff.
    """
    ref = orbit_ref or ORBIT_REF
    if not ref.exists():
        raise SystemExit(f"Orbit ref missing: {ref}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    ident = identity_ref if identity_ref and identity_ref.resolve() != ref.resolve() else None
    if ident is not None:
        print(
            f"  identity baked into start frame ({ref.name}); Omni I2V allows one image only",
            flush=True,
        )
    print(f"  submit model={model} → {dest.name}", flush=True)
    interaction = client.interactions.create(
        model=model,
        input=[
            {"type": "image", "data": _b64(ref), "mime_type": "image/png"},
            {"type": "text", "text": prompt + SFX_LOCK},
        ],
        response_format={"type": "video", "aspect_ratio": aspect_ratio},
        generation_config={"video_config": {"task": "image_to_video"}},
    )
    dest.write_bytes(_video_bytes(interaction))
    size = dest.stat().st_size
    if size < 200_000:
        raise RuntimeError(f"download too small: {dest} ({size} bytes)")
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": size,
        "model": model,
        "engine": "gemini-api-omni",
        "orbit_ref": str(ref),
        "interaction_id": getattr(interaction, "id", None),
    }
