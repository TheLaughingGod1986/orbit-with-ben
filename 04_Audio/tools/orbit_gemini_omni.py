#!/usr/bin/env python3
"""Orbit CG via Gemini Omni Flash API (gemini-omni-flash-preview).

Primary picture path for Omni-forward longs.
Flow Playwright is backup only when this API is down.
Not ElevenLabs Image & Video.
Keeps native Omni SFX unless the caller strips audio.
"""
from __future__ import annotations

import base64
import json
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ORBIT_REF = (
    REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
DEFAULT_MODEL = "gemini-omni-flash-preview"
# Vertex serves Omni (Interactions API) from the `global` location only.
# Regional endpoints (e.g. us-central1) answer every Omni call with
# 500 "Internal error encountered" (seen 1-4 Oct 2026), even an empty request.
OMNI_VERTEX_LOCATION = "global"

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


def _ensure_global_vertex(client):
    """Return a client that targets Vertex `global` when `client` is a regional Vertex client.

    Gemini API (api-key) clients are returned unchanged.
    """
    api = getattr(client, "_api_client", None)
    if not getattr(api, "vertexai", False):
        return client
    loc = getattr(api, "location", None)
    if loc == OMNI_VERTEX_LOCATION:
        return client
    from google import genai

    print(
        f"  Omni on Vertex is global-only; switching location {loc!r} -> {OMNI_VERTEX_LOCATION!r}",
        flush=True,
    )
    return genai.Client(
        vertexai=True,
        project=getattr(api, "project", None),
        location=OMNI_VERTEX_LOCATION,
        credentials=getattr(api, "_credentials", None),
    )


def _orbit_sidecar(start: Path) -> Path:
    return start.with_suffix(".json")


def write_orbit_source_sidecar(start: Path, source: Path = ORBIT_REF, **extra) -> Path:
    """Record that `start` was composited from the canonical Orbit still.

    Call this from whatever script composites an Orbit start frame.
    """
    side = _orbit_sidecar(start)
    try:
        rel = str(source.resolve().relative_to(REPO.resolve()))
    except ValueError:
        rel = str(source)
    side.write_text(json.dumps({"orbit_source": rel, **extra}, indent=2) + "\n")
    return side


def assert_orbit_start_frame(start: Path) -> str:
    """Raise unless an Orbit-shot start frame derives from the canonical still."""
    canon = ORBIT_REF.resolve()
    if start.resolve() == canon:
        return "canonical (start frame is ORBIT_REF)"
    side = _orbit_sidecar(start)
    if not side.exists():
        raise SystemExit(
            f"Orbit shot blocked: {start.name} has no sidecar {side.name} with orbit_source. "
            f"Composite the start frame from {ORBIT_REF.name} and call write_orbit_source_sidecar()."
        )
    try:
        src = json.loads(side.read_text()).get("orbit_source")
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"Orbit shot blocked: unreadable sidecar {side}: {e}")
    if not src:
        raise SystemExit(f"Orbit shot blocked: {side.name} has no orbit_source")
    sp = Path(src)
    sp = sp if sp.is_absolute() else REPO / sp
    if sp.resolve() != canon:
        raise SystemExit(
            f"Orbit shot blocked: {side.name} orbit_source={src} is not the canonical "
            f"{ORBIT_REF.relative_to(REPO)}"
        )
    return src


def generate_omni_clip(
    client,
    prompt: str,
    dest: Path,
    *,
    orbit_ref: Path | None = None,
    identity_ref: Path | None = None,
    orbit_shot: bool = False,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "16:9",
) -> dict:
    """One ~8s Omni Flash clip.

    orbit_ref is the I2V start frame (composition). Omni I2V takes exactly ONE
    image, so identity_ref is never sent: it only marks the shot as an Orbit
    shot. For an Orbit shot the start frame must already contain the canonical
    Orbit — either it IS ORBIT_REF, or it has a sidecar `<start>.json` whose
    `orbit_source` points at ORBIT_REF (see write_orbit_source_sidecar).
    Otherwise this raises, so Orbit can't drift off-model between shots.
    """
    ref = orbit_ref or ORBIT_REF
    if not ref.exists():
        raise SystemExit(f"Orbit ref missing: {ref}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    if orbit_shot or identity_ref is not None:
        src = assert_orbit_start_frame(ref)
        print(
            "  identity_ref NOT sent (I2V = one image); start frame must already contain "
            f"canonical Orbit — {ref.name} orbit_source={src}",
            flush=True,
        )
    client = _ensure_global_vertex(client)
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
