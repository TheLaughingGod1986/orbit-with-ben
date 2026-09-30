#!/usr/bin/env python3
"""Saturn Orbit tumble still v03 — Vertex only (Free Trial credit).

First Orbit beat (Ben 30 Sep 21:39): Orbit tumbles through the thin ring sheet
with the camera, grabbing at passing ice. Bare-Saturn Orbit plate stays v02.

Canonical reference:
  01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
from pathlib import Path

from google import genai
from google.genai import types

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
STILLS_V01 = EP / "04_Generated-Clips" / "stills_v01"
STILLS_V02 = EP / "04_Generated-Clips" / "stills_v02"
OUT = EP / "04_Generated-Clips" / "stills_v03"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v03_for_ben_ok"
)
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"
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
    "text, logos, watermark, Earth globe, humans, spacecraft."
)

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint stars. "
    "Exactly one pale-gold banded Saturn far below / beyond the ring plane. "
    "No second planet, no Earth, no humans, no text, no letters, no numbers, no logos, no watermark, no UI."
)

TUMBLE = {
    "file": "saturn_orbit_tumble_sheet_v03.png",
    "role": "orbit-tumble-through-sheet",
    "prompt": (
        IDENTITY
        + " "
        + NEGATIVE
        + " "
        "ACTION: Orbit tumbles through the thin bright ice ring sheet with the camera. "
        "He is mid-tumble, body tilted, one stubby arm reaching toward a passing ice chunk, "
        "visor and gaze along the direction of travel through the sheet, not looking at the camera. "
        "Pale water-ice chunks pack the plane around him — the sheet is absurdly thin the other way; "
        "you can see open black space above and below the blade. Saturn's banded atmosphere sits far "
        "below the inner edge. Exactly ONE Orbit. "
        + STYLE
    ),
}

# Pack for Ben: world plates from v01 + bare Orbit from v02 + new tumble.
PACK_COPY = [
    (STILLS_V01 / "saturn_open_rings_v01.png", "saturn_open_rings_v01.png"),
    (STILLS_V01 / "saturn_ice_chunks_v01.png", "saturn_ice_chunks_v01.png"),
    (STILLS_V01 / "saturn_ring_rain_cassini_v01.png", "saturn_ring_rain_cassini_v01.png"),
    (STILLS_V01 / "saturn_young_rings_v01.png", "saturn_young_rings_v01.png"),
    (STILLS_V01 / "saturn_bare_v01.png", "saturn_bare_v01.png"),
    (STILLS_V02 / "saturn_orbit_bare_v02.png", "saturn_orbit_bare_v02.png"),
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
        "note": "v03 adds Orbit tumble-through-sheet (first Orbit beat). Bare Orbit stays v02. World plates from v01.",
        "stills": [],
        "pack": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    dest = OUT / TUMBLE["file"]
    print(f"still {TUMBLE['file']} via Vertex/{MODEL}", flush=True)
    nbytes = 0
    for attempt in range(3):
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=ref_bytes, mime_type="image/png"),
                TUMBLE["prompt"],
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
            nbytes = 0
    if not dest.exists() or dest.stat().st_size < 10_000:
        raise SystemExit(f"FAILED {dest}")
    sha = hashlib.sha256(dest.read_bytes()).hexdigest()
    uat_dest = UAT / TUMBLE["file"]
    uat_dest.write_bytes(dest.read_bytes())
    row = {
        "file": TUMBLE["file"],
        "role": TUMBLE["role"],
        "bytes": dest.stat().st_size,
        "sha256": sha,
        "model": MODEL,
        "engine": "vertex",
        "orbit_reference_attached": True,
        "path": str(dest),
        "uat_path": str(uat_dest),
        "new_this_pass": True,
    }
    manifest["stills"].append(row)
    print(f"  wrote {nbytes} sha={sha}", flush=True)

    for src, name in PACK_COPY:
        if not src.is_file():
            print(f"  WARN missing pack source {src}", flush=True)
            continue
        out_p = OUT / name
        uat_p = UAT / name
        data = src.read_bytes()
        out_p.write_bytes(data)
        uat_p.write_bytes(data)
        manifest["pack"].append(
            {
                "file": name,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "source": str(src),
            }
        )

    # Also copy tumble into pack list for UAT README clarity
    manifest["pack"].insert(
        0,
        {
            "file": TUMBLE["file"],
            "sha256": sha,
            "bytes": dest.stat().st_size,
            "source": str(dest),
            "new_this_pass": True,
        },
    )

    n_new = 1
    manifest["images_generated_this_pass"] = n_new
    manifest["estimated_usd_list_price"] = round(n_new * USD_PER_IMAGE, 4)
    manifest["billing_note"] = (
        "Charged to Vertex Free Trial credit on project "
        f"{PROJECT}; not AI Studio prepay. List estimate ${USD_PER_IMAGE}/image."
    )
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "README.md").write_text(
        """# Saturn stills v03 — for Ben OK

**New this pass:** `saturn_orbit_tumble_sheet_v03.png` — first Orbit beat: tumble through the thin sheet (picture card only; no moving cut yet).

**Kept:** world plates from v01 · bare-Saturn Orbit from v02 (`saturn_orbit_bare_v02.png`).

**Retired for beat 1:** `saturn_orbit_along_rings_v02.png` (along-the-plane hover) — replaced by the tumble card.

Frame 0 / open still unchanged: `saturn_open_rings_v01.png` (ring sheet already falling, no Orbit).

STOP after you OK — no moving cut.
"""
    )
    print(
        json.dumps(
            {
                "STILLS_V03_DONE": True,
                "images_generated": n_new,
                "estimated_usd": manifest["estimated_usd_list_price"],
                "out": str(OUT),
                "uat": str(UAT),
                "tumble_sha256": sha,
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
