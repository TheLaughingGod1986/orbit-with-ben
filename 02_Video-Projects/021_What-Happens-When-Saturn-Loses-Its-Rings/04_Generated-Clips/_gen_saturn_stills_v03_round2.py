#!/usr/bin/env python3
"""Saturn stills v03 — Ben Round 2 (30 Sep 21:53 London). Vertex Free Trial only. No Veo.

Final pack (6):
  1. opening — keep open_v01 composition/look; reverse rain: INNER edge → equator; Saturn further in; no Orbit
  2. Orbit tumble — approved Orbit model INSIDE thin bright ice sheet; Saturn huge BG; not standing on a floor
  3. ring-crowd — bright white water-ice chunks; Saturn LARGE on horizon; no dark hole
  4. Cassini — WHITE high-gain dish; gold foil on body only; NO spacecraft shadow on clouds
  5. bare Saturn — oblate (~10% wider than tall); butterscotch-gold bands; NO oval storm / not Jupiter
  6. young-rings — KEEP v01 (optional Saturn shadow across rings already OK)

Deletes from UAT pack: any Orbit+Jupiter / along-rings knockoff plates.
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
OPEN_REF = STILLS_V01 / "saturn_open_rings_v01.png"
YOUNG_SRC = STILLS_V01 / "saturn_young_rings_v01.png"

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"
USD_PER_IMAGE = 0.039

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint pinprick stars. "
    "Exactly ONE Saturn — pale butterscotch-gold banded gas giant, visibly OBLATE "
    "(about 10 percent wider than tall). NOT Jupiter: no Great Red Spot, no large oval storm, "
    "no blue zones, no turbulent jovian swirls. "
    "No Earth, no second planet, no moons unless needed for rings only, "
    "no humans, no text, no letters, no numbers, no logos, no watermark, no UI."
)

ORBIT_LOCK = (
    "CRITICAL — match the attached Orbit reference image EXACTLY for the character. "
    "Approved Orbit model: glossy metallic orange rounded floating robot, continuous body, "
    "NO legs. Face = one LARGE BLACK ROUNDED/CURVED HORIZONTAL VISOR across the front "
    "(not a round circular faceplate, not a flat black disc). "
    "Inside the visor: exactly TWO cream/amber circular eyes with dark pupils. "
    "Side arm pods on the body; short stubby orange arms with dark three-finger hands OK when reaching. "
    "One antenna with a small glowing bulb tip. "
    "Exactly ONE soft underside/bottom glow centered under the body. Belly stays orange, not a yellow lamp. "
    "Exactly ONE Orbit. No twin, no clone, no second face, no text, no HUD. "
    "He is SMALL in frame (under about a tenth), a garnish, never a hero poster."
)

# Files that must NOT remain in the Ben UAT pack
UAT_BAN = {
    "saturn_orbit_along_rings_v01.png",
    "saturn_orbit_along_rings_v02.png",
    "saturn_orbit_bare_v01.png",
    "saturn_orbit_bare_v02.png",
    "saturn_open_rings_v01.png",  # superseded by v03 reverse
    "saturn_ice_chunks_v01.png",
    "saturn_ring_rain_cassini_v01.png",
    "saturn_bare_v01.png",
    "saturn_orbit_tumble_sheet_v03.png",  # if a prior partial run used a weaker name
}

STILLS = [
    {
        "file": "saturn_open_rings_v03.png",
        "role": "open-rings-inner-rain",
        "refs": ["open"],  # keep composition/look of v01
        "prompt": (
            "EDIT the attached Saturn opening still. KEEP the same camera angle, lighting, "
            "ring tilt, cream/tan ring lanes, and overall composition/look. "
            "CHANGE the ice motion: reverse it. Ice must stream from the INNER edge of the rings "
            "DOWN into Saturn's equator as faint falling streaks of pale water ice into the atmosphere — "
            "ring rain into the planet. Do NOT scatter ice off the outer edge into empty space. "
            "Bring Saturn a little further into frame (more of the butterscotch-gold banded globe visible) "
            "so the fall into the planet reads clearly at phone size. "
            "Rings remain a thin bright sheet. No Orbit. No spacecraft. No title. "
            + STYLE
        ),
    },
    {
        "file": "saturn_orbit_tumble_sheet_v03.png",
        "role": "orbit-tumble-in-ring",
        "refs": ["orbit"],
        "prompt": (
            ORBIT_LOCK
            + " "
            "CLOSE shot INSIDE Saturn's rings: Orbit is SMALL and mid-TUMBLE through a THIN layer of "
            "bright WHITE water-ice chunks (not grey rock, not a solid floor). "
            "He is floating/tumbling in the crowd — NEVER standing on the ring; the ring is a crowd of ice, not a surface. "
            "One stubby arm / arm pod reaches toward a passing ice chunk. "
            "Visor and gaze along the direction of travel, not looking at the camera. "
            "Saturn is HUGE in the background (banded butterscotch-gold, OBLATE, WITH rings visible as the thin sheet around him). "
            "Open black space above and below the thin blade. No spacecraft. No second robot. "
            + STYLE
        ),
    },
    {
        "file": "saturn_ice_chunks_v03.png",
        "role": "science-ice-crowd",
        "refs": [],
        "prompt": (
            "Inside Saturn's main rings, close through the crowd: countless chunks of bright sunlit WATER ICE — "
            "mostly clean white / pale, a few lightly dust-tinted cream to tan grains. "
            "NOT grey rock, NOT brown stone, NOT a solid disc, NOT a stone roof. "
            "Ice chunks from centimetres to house-sized boulders, packed in a thin horizontal plane. "
            "NO dark circular hole / void gap in the middle of the field — continuous ice crowd. "
            "Saturn is LARGE on the horizon (fills a big share of the background), butterscotch-gold bands, "
            "visibly OBLATE, rings continuing as the plane we are inside. "
            "Open black space above and below the thin sheet. No Orbit. No spacecraft. "
            + STYLE
        ),
    },
    {
        "file": "saturn_ring_rain_cassini_v03.png",
        "role": "science-cassini",
        "refs": [],
        "prompt": (
            "Wide documentary view above Saturn. Saturn's butterscotch-gold cloud tops fill the lower frame "
            "(OBLATE planet, soft bands, NO oval storm). "
            "Rings are a thin bright line above. Between rings and clouds, pale ice grains fall as ring rain "
            "toward the equator. "
            "Exactly ONE Cassini spacecraft, readable size: HIGH-GAIN DISH is WHITE / pale (NOT gold dish). "
            "Gold foil ONLY on the boxy body / bus. One long thin boom. "
            "CRITICAL: the spacecraft casts NO shadow on the clouds — no silhouette, no dark craft-shaped shadow on Saturn. "
            "Lighting does not project the craft onto the atmosphere. No robot. No second craft. No rocket flame. "
            + STYLE
        ),
    },
    {
        "file": "saturn_bare_v03.png",
        "role": "bare-saturn",
        "refs": [],
        "prompt": (
            "Bare Saturn with NO rings at all. The planet is clearly OBLATE — about 10 percent wider than tall. "
            "Soft butterscotch-gold and cream atmospheric bands, calm Saturn-like banding "
            "(NOT Jupiter: no Great Red Spot, no large oval storm, no blue belts, no violent jovian turbulence). "
            "Clean empty black space where the ice sheet was. No ring shadow. One planet only. "
            "No Orbit. No spacecraft. No moons. "
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not ORBIT_REF.is_file():
        raise SystemExit(f"Missing Orbit reference: {ORBIT_REF}")
    if not OPEN_REF.is_file():
        raise SystemExit(f"Missing open reference: {OPEN_REF}")
    if not YOUNG_SRC.is_file():
        raise SystemExit(f"Missing young-rings keep: {YOUNG_SRC}")

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)

    # Wipe prior UAT pack contents (Jupiter/Orbit leftovers + old v01 copies)
    for p in list(UAT.iterdir()):
        if p.is_file() and (
            p.name in UAT_BAN
            or p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            or p.name in {"MANIFEST.json", "README.md", "SHA256.md"}
        ):
            # Remove all images + old manifests; we rewrite the pack clean
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} or p.name in {
                "MANIFEST.json",
                "README.md",
                "SHA256.md",
            }:
                p.unlink()
                print(f"uat_rm {p.name}", flush=True)

    manifest: dict = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "veo": False,
        "ben_round": "2",
        "ben_notes_at": "2026-09-30T21:53+01:00",
        "orbit_reference": str(ORBIT_REF.relative_to(REPO)),
        "open_composition_reference": str(OPEN_REF.relative_to(REPO)),
        "usd_per_image_list_estimate": USD_PER_IMAGE,
        "stills": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    generated = 0
    for spec in STILLS:
        dest = OUT / spec["file"]
        print(f"still {spec['file']} via Vertex/{MODEL}", flush=True)
        contents: list = []
        for ref in spec["refs"]:
            if ref == "orbit":
                contents.append(
                    types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png")
                )
            elif ref == "open":
                contents.append(
                    types.Part.from_bytes(data=OPEN_REF.read_bytes(), mime_type="image/png")
                )
        contents.append(spec["prompt"])

        nbytes = 0
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
                nbytes = save_response(response, dest)
                break
            except RuntimeError as e:
                print(f"  retry {attempt + 1}: {e}", flush=True)
                nbytes = 0
        if not dest.exists() or dest.stat().st_size < 10_000:
            raise SystemExit(f"FAILED {dest}")
        generated += 1
        h = sha256(dest)
        uat_dest = UAT / spec["file"]
        uat_dest.write_bytes(dest.read_bytes())
        row = {
            "file": spec["file"],
            "role": spec["role"],
            "bytes": dest.stat().st_size,
            "sha256": h,
            "model": MODEL,
            "engine": "vertex",
            "new_this_pass": True,
            "path": str(dest),
            "uat_path": str(uat_dest),
            "refs": spec["refs"],
        }
        manifest["stills"].append(row)
        print(f"  wrote {nbytes} sha={h}", flush=True)

    # KEEP young-rings from v01
    young_name = "saturn_young_rings_v01.png"
    young_out = OUT / young_name
    young_uat = UAT / young_name
    data = YOUNG_SRC.read_bytes()
    young_out.write_bytes(data)
    young_uat.write_bytes(data)
    manifest["stills"].append(
        {
            "file": young_name,
            "role": "science-young-KEEP",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "model": "kept-from-v01",
            "engine": "copy",
            "new_this_pass": False,
            "path": str(young_out),
            "uat_path": str(young_uat),
        }
    )
    print(f"keep {young_name} sha={hashlib.sha256(data).hexdigest()}", flush=True)

    # Ensure banned names are gone from OUT too (old partials)
    for name in list(UAT_BAN):
        p = OUT / name
        if p.is_file() and name not in {s["file"] for s in manifest["stills"]}:
            # Don't delete young keep; ban list has superseded opens/orbits
            if name.startswith("saturn_young"):
                continue
            # Leave OUT archive of old files? Prefer quarantine
            rejected = OUT / "_rejected_pre_round2"
            rejected.mkdir(exist_ok=True)
            if p.name not in {s["file"] for s in manifest["stills"]}:
                shutil.move(str(p), str(rejected / p.name))
                print(f"quarantine {p.name}", flush=True)

    manifest["images_generated_this_pass"] = generated
    manifest["estimated_usd_list_price"] = round(generated * USD_PER_IMAGE, 4)
    manifest["billing_note"] = (
        f"Charged to Vertex Free Trial credit on project {PROJECT}; "
        f"not AI Studio prepay. List estimate ${USD_PER_IMAGE}/image × {generated}."
    )
    manifest["pack_order"] = [
        "saturn_open_rings_v03.png",
        "saturn_orbit_tumble_sheet_v03.png",
        "saturn_ice_chunks_v03.png",
        "saturn_ring_rain_cassini_v03.png",
        "saturn_bare_v03.png",
        "saturn_young_rings_v01.png",
    ]
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    sha_lines = ["# SHA-256 — saturn_stills_v03_for_ben_ok", ""]
    sha_lines.append("| File | SHA-256 | Bytes |")
    sha_lines.append("|---|---|---:|")
    for name in manifest["pack_order"]:
        p = UAT / name
        sha_lines.append(f"| `{name}` | `{sha256(p)}` | {p.stat().st_size} |")
    (UAT / "SHA256.md").write_text("\n".join(sha_lines) + "\n")

    (UAT / "README.md").write_text(
        f"""# Saturn stills v03 — Ben OK pack (Round 2 · 30 Sep 21:53)

**Vertex only. No Veo. No moving cut.**

| # | File | Note |
|---|---|---|
| 1 | `saturn_open_rings_v03.png` | Opening — same look as v01, rain REVERSED (inner edge → equator), Saturn further in, no Orbit |
| 2 | `saturn_orbit_tumble_sheet_v03.png` | Orbit tumble INSIDE thin white ice sheet; Saturn huge BG; approved Orbit model |
| 3 | `saturn_ice_chunks_v03.png` | Bright white water-ice crowd; Saturn large; no dark hole |
| 4 | `saturn_ring_rain_cassini_v03.png` | Cassini white dish; gold foil on body only; no craft shadow on clouds |
| 5 | `saturn_bare_v03.png` | Oblate bare Saturn, butterscotch-gold; not Jupiter |
| 6 | `saturn_young_rings_v01.png` | KEEP from v01 |

Removed from this folder: Orbit+Jupiter / along-rings / old v01 open·ice·cassini·bare plates.

Estimated Vertex list cost this pass: **${manifest['estimated_usd_list_price']:.3f}** ({generated} images × ${USD_PER_IMAGE}).

STOP after Ben OK — no Veo spend.
"""
    )
    print(
        json.dumps(
            {
                "STILLS_V03_ROUND2_DONE": True,
                "images_generated": generated,
                "estimated_usd": manifest["estimated_usd_list_price"],
                "out": str(OUT),
                "uat": str(UAT),
                "pack": manifest["pack_order"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
