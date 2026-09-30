#!/usr/bin/env python3
"""Saturn Orbit stills v02 — Vertex only (Free Trial credit). No AI Studio prepay.

Remints ONLY the two character plates after Ben rejected stills_v01 Orbit
(round circular faceplate / knockoff proportions). World plates stay v01.

Canonical reference:
  01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
OUT = EP / "04_Generated-Clips" / "stills_v02"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v02_for_ben_ok"
)
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)

# Vertex Free Trial project (ADC). Never GEMINI_API_KEY / AI Studio prepay.
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"

# Approximate Vertex list price for Gemini 2.5 Flash Image output images (USD).
# Free Trial credit is billed against this; report after run.
USD_PER_IMAGE = 0.039

IDENTITY = (
    "CRITICAL — match the attached Orbit reference image EXACTLY. "
    "This is the same character used on Jupiter/Andromeda. "
    "Solid matte orange continuous rounded body (head+torso one piece). "
    "NO legs — hover only. "
    "Face = one LARGE BLACK CURVED HORIZONTAL VISOR (widescreen band across the front), "
    "NOT a round circular faceplate, NOT a flat black disc face, NOT a full-sphere black front. "
    "Inside that curved visor: exactly TWO cream/amber circular eyes with dark pupils. "
    "Short stubby orange arms with dark three-finger hands. "
    "One antenna with a small glowing bulb tip. "
    "Exactly ONE soft underside glow centered under the body. Belly stays matte orange. "
    "No second face, no twin, no clone, no reflection duplicate, no text, no HUD. "
    "Premium CGI 3D polish, not a flat toy, not chibi knockoff. "
    "He is a small garnish (under a tenth of the frame), never a hero poster."
)

NEGATIVE = (
    "Forbidden: round circular black faceplate, disc face, full-front black circle, "
    "blank solid white eyes with no pupils, slit LED eyes, glowing yellow belly lamp, "
    "twin thrusters, legs, second robot, second visor on the back, cartoon 2D cel, "
    "text, logos, watermark, Earth globe, humans."
)

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint stars. "
    "Exactly one pale-gold banded Saturn. No second planet, no Earth, no moons unless needed for rings only. "
    "No humans, no text, no letters, no numbers, no logos, no watermark, no UI."
)

STILLS = [
    {
        "file": "saturn_orbit_along_rings_v02.png",
        "role": "orbit-along-rings",
        "prompt": (
            IDENTITY
            + " "
            + NEGATIVE
            + " "
            "Place him small on the LEFT, visor turned along the ring plane (not at the camera). "
            "Saturn's pale ice rings and one Saturn fill the rest of the picture. No spacecraft. "
            + STYLE
        ),
    },
    {
        "file": "saturn_orbit_bare_v02.png",
        "role": "orbit-bare",
        "prompt": (
            IDENTITY
            + " "
            + NEGATIVE
            + " "
            "He is tiny at the far LEFT edge, three-quarter view, eyes looking at the planet, not at the camera. "
            "Bare Saturn with NO rings fills the right of the frame: pale gold bands, empty equator, black space. "
            "No spacecraft. No ring. "
            + STYLE
        ),
    },
]


def save_response(response, dest: Path) -> int:
    if not response.candidates:
        raise RuntimeError(f"No candidates for {dest.name}")
    content = response.candidates[0].content
    parts = content.parts if content and content.parts else []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    reason = getattr(response.candidates[0], "finish_reason", None)
    raise RuntimeError(f"No image bytes for {dest.name} finish={reason}")


def main() -> None:
    if not ORBIT_REF.exists():
        raise SystemExit(f"Missing Orbit reference: {ORBIT_REF}")
    # Force Vertex — strip AI Studio keys from this process.
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)

    ref_bytes = ORBIT_REF.read_bytes()
    manifest = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "orbit_reference": str(ORBIT_REF.relative_to(REPO)),
        "ai_studio_prepay": False,
        "usd_per_image_list_estimate": USD_PER_IMAGE,
        "stills": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    for spec in STILLS:
        dest = OUT / spec["file"]
        print(f"still {spec['file']} via Vertex/{MODEL}", flush=True)
        response = None
        for attempt in range(3):
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    types.Part.from_bytes(data=ref_bytes, mime_type="image/png"),
                    spec["prompt"],
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            try:
                nbytes = save_response(response, dest)
                break
            except RuntimeError as e:
                print(f"  retry {attempt + 1}: {e}", flush=True)
                response = None
                nbytes = 0
        if not dest.exists() or dest.stat().st_size < 10_000:
            raise SystemExit(f"FAILED {dest}")
        sha = hashlib.sha256(dest.read_bytes()).hexdigest()
        uat_dest = UAT / spec["file"]
        uat_dest.write_bytes(dest.read_bytes())
        row = {
            "file": spec["file"],
            "role": spec["role"],
            "bytes": dest.stat().st_size,
            "sha256": sha,
            "model": MODEL,
            "engine": "vertex",
            "orbit_reference_attached": True,
            "path": str(dest),
            "uat_path": str(uat_dest),
        }
        manifest["stills"].append(row)
        print(f"  wrote {nbytes} sha={sha}", flush=True)

    n = len(manifest["stills"])
    manifest["images"] = n
    manifest["estimated_usd_list_price"] = round(n * USD_PER_IMAGE, 4)
    manifest["billing_note"] = (
        "Charged to Vertex Free Trial credit on project "
        f"{PROJECT}; not AI Studio prepay. List estimate ${USD_PER_IMAGE}/image."
    )
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # Also note why v01 failed
    (OUT / "WHY_V01_REJECTED.md").write_text(
        """# Why Saturn stills_v01 Orbit was rejected (Ben 30 Sep 21:26)

Ben: "Wrong orbit character" against `saturn_orbit_along_rings_v01.png`.

## Canonical reference used for v02

`01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png`
(symlink twin: `orbit-cg-canonical-16x9-v01.png`)

Same lock as Jupiter (`020_…/stills_v01` MANIFEST) and channel rules
(`orbit-character-consistency.mdc`).

## What was wrong on v01

v01 attached the reference but the model drifted to a **knockoff**:
a round circular black faceplate / disc face with big eyes on a sphere,
instead of Orbit's locked **large black curved horizontal visor** with cream
eyes + pupils inside that visor. Proportions read chibi / different mascot.

World plates (no Orbit) were not reminted.
"""
    )
    print(json.dumps({
        "STILLS_V02_DONE": True,
        "images": n,
        "estimated_usd": manifest["estimated_usd_list_price"],
        "out": str(OUT),
        "uat": str(UAT),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
