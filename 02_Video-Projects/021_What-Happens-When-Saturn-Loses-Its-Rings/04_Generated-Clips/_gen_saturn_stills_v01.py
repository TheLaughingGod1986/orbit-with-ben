#!/usr/bin/env python3
"""Saturn rings stills. Gemini image API only. No Veo, no Omni, no Flow."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import resolve_api_key  # key loader only

from google import genai
from google.genai import types

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
OUT = EP / "04_Generated-Clips" / "stills_v01"
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)
ENV = REPO / "02_Video-Projects" / "019_Andromeda-Milky-Way-Collision" / "07_Edit-Project" / ".env"
MODEL = "gemini-2.5-flash-image"

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint stars. "
    "Exactly one Saturn, a pale-gold banded gas giant. No second planet, no Earth, no moons in frame, "
    "no humans, no text, no letters, no numbers, no logos, no watermark, no UI, no diagram, no arrows. "
    "No robot unless this prompt explicitly asks for the one orange robot."
)

STILLS = [
    {
        "file": "saturn_open_rings_v01.png",
        "role": "open-rings",
        "orbit": False,
        "prompt": (
            "Saturn's rings only, seen almost edge-on as a vast thin blade of pale water ice. "
            "Particles of ice drift inward toward Saturn's curve, which fills one side of the frame. "
            "The sheet is enormous sideways and only metres thick. Sunlight on clean ice, a few warmer dust lanes. "
            "No robot. No spacecraft. No title. "
            + STYLE
        ),
    },
    {
        "file": "saturn_ice_chunks_v01.png",
        "role": "science-ice",
        "orbit": False,
        "prompt": (
            "Inside Saturn's rings, close: countless chunks of water ice, grains to house-sized boulders, "
            "sunlit and pale, a few dust-darkened grains. Not rock, not a solid disc, not a stone roof. "
            "Open black space above and below the thin plane. Saturn's pale curve is distant and small. "
            "No robot. No spacecraft. "
            + STYLE
        ),
    },
    {
        "file": "saturn_ring_rain_cassini_v01.png",
        "role": "science-rain",
        "orbit": False,
        "prompt": (
            "Wide documentary view of ring rain. Saturn's pale gold cloud tops fill the bottom half of the frame. "
            "The rings are a thin bright line across the top. Between them, a visible shower of pale ice grains "
            "falls downward into the atmosphere. Exactly one spacecraft, large enough to see: Cassini, one gold "
            "parabolic dish, a boxy body, one long thin boom. No second craft, no rocket flame, no robot. "
            + STYLE
        ),
    },
    {
        "file": "saturn_young_rings_v01.png",
        "role": "science-young",
        "orbit": False,
        "prompt": (
            "The same one Saturn when the rings were newer: a wider, brighter, fiercely white ice sheet, "
            "cleaner and more massive, wrapped around the pale-gold planet. No dust-brown lanes yet. "
            "No robot. No spacecraft. No second planet. "
            + STYLE
        ),
    },
    {
        "file": "saturn_bare_v01.png",
        "role": "bare-saturn",
        "orbit": False,
        "prompt": (
            "Saturn with no rings. Pale gold cloud bands, a clean equator, empty black space where the ice sheet was. "
            "No ring shadow on the clouds. One planet only. No robot. No spacecraft. No moons. "
            + STYLE
        ),
    },
    {
        "file": "saturn_orbit_along_rings_v01.png",
        "role": "orbit-along-rings",
        "orbit": True,
        "prompt": (
            "Match the attached reference exactly for the one robot: solid matte orange rounded body, no legs, "
            "one large black curved visor that is the only face, two cream eyes with dark pupils, "
            "short stubby orange arms, dark three-finger hands, one antenna with a glowing tip. "
            "Exactly one small soft glow centered under the body. The belly stays matte orange, not a lamp, "
            "not twin jets, not side engines. No second face, no twin, no text. "
            "He is small, under a tenth of the frame, on the left, visor turned along the ring plane, not at the camera. "
            "Saturn's pale ice rings and one Saturn fill the rest of the picture. No spacecraft. "
            + STYLE
        ),
    },
    {
        "file": "saturn_orbit_bare_v01.png",
        "role": "orbit-bare",
        "orbit": True,
        "prompt": (
            "Match the attached reference exactly for the one robot: solid matte orange rounded body, no legs, "
            "one large black curved visor that is the only face, two cream eyes with dark pupils, "
            "short stubby orange arms, dark three-finger hands, one antenna with a glowing tip. "
            "Exactly one small soft glow centered under the body. Belly is matte orange, never a glowing yellow lamp. "
            "No twin jets, no second face, no twin, no text. "
            "He is tiny at the far left edge, a small garnish, three-quarter view, eyes looking at the planet, not at the camera. "
            "Bare Saturn with no rings fills the right of the frame: pale gold bands, empty equator, black space. "
            "No spacecraft. No ring. "
            + STYLE
        ),
    },
]


def save_response(response, dest: Path) -> None:
    parts = []
    if response.candidates:
        content = response.candidates[0].content
        if content and content.parts:
            parts = content.parts
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return
    raise RuntimeError(f"No image bytes returned for {dest.name}")


def main() -> None:
    key = resolve_api_key(ENV)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = key
    client = genai.Client(api_key=key)
    OUT.mkdir(parents=True, exist_ok=True)
    if not ORBIT_REF.exists():
        raise SystemExit(f"Missing Orbit reference: {ORBIT_REF}")

    manifest = []
    for spec in STILLS:
        dest = OUT / spec["file"]
        if dest.exists() and dest.stat().st_size > 10_000:
            print(f"skip {spec['file']}", flush=True)
            manifest.append({"file": spec["file"], "role": spec["role"], "bytes": dest.stat().st_size, "skipped": True})
            continue
        contents: list = []
        if spec["orbit"]:
            contents.append(types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png"))
        contents.append(spec["prompt"])
        print(f"still {spec['file']}", flush=True)
        response = None
        for attempt in range(3):
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            try:
                save_response(response, dest)
                break
            except RuntimeError:
                reason = None
                if response.candidates:
                    reason = getattr(response.candidates[0], "finish_reason", None)
                print(f"  retry {attempt + 1} finish={reason}", flush=True)
                response = None
        if response is None or not dest.exists():
            raise RuntimeError(f"No image bytes returned for {dest.name}")
        manifest.append(
            {
                "file": spec["file"],
                "role": spec["role"],
                "bytes": dest.stat().st_size,
                "model": MODEL,
                "engine": "gemini-image-still",
                "veo": False,
                "omni": False,
                "orbit_reference_attached": spec["orbit"],
            }
        )
        print(f"  wrote {dest.stat().st_size}", flush=True)
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print("STILLS_DONE", flush=True)


if __name__ == "__main__":
    main()
