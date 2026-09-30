#!/usr/bin/env python3
"""Saturn stills v04 — Ben Round 3 (30 Sep 22:21 London). Vertex Free Trial only. No Veo here.

Four stills for Ben OK:
  1. opening — rings from LEFT into Saturn RIGHT half; inner edge meets equator; NO streaks; no Orbit
  2. bare + Orbit — oblate Saturn ~60% frame height; side-lit crescent; Orbit tiny at edge looking back
  3. ice crowd — thin floating white ice layer; black space between/beneath; camera slightly below; not a floor
  4. Orbit in rings — mid-air tumble; sparse floating chunks; eyes wide; one hand reaching; not sitting/waving

Self-check before UAT paste. Remint failures.
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
STILLS_V01 = EP / "04_Generated-Clips" / "stills_v01"
STILLS_V03 = EP / "04_Generated-Clips" / "stills_v03"
OUT = EP / "04_Generated-Clips" / "stills_v04"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v04_for_ben_ok"
)
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)
# Ring look reference (bright blade, fine bands) — composition will be rewritten
RING_LOOK = STILLS_V01 / "saturn_young_rings_v01.png"
# Good oblate bare body from round2c
BARE_BODY = STILLS_V03 / "saturn_bare_v03.png"

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"
USD_PER_IMAGE = 0.039

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint pinprick stars. "
    "Exactly ONE Saturn — soft butterscotch-gold banded gas giant, visibly OBLATE "
    "(about 10 percent wider than tall). NOT Jupiter: no Great Red Spot, no oval storm. "
    "No Earth, no second planet, no humans, no text, no logos, no watermark, no UI."
)

ORBIT_LOCK = (
    "CRITICAL — match the attached Orbit reference EXACTLY. "
    "Approved model: glossy metallic orange rounded floating robot, NO legs. "
    "Large black rounded/curved horizontal visor; two cream eyes with dark pupils; "
    "side arm pods; short stubby orange arms with dark three-finger hands; "
    "one antenna with glowing bulb tip; exactly ONE soft bottom underside glow. "
    "Exactly ONE Orbit. Small garnish. No twin, no second face, no text."
)


STILLS = [
    {
        "file": "saturn_open_rings_v04.png",
        "role": "open-rings-meet-equator",
        "refs": ["ring_look"],
        "prompt": (
            "Use the attached image ONLY for the RING LOOK: bright thin ice blade with fine cream/tan bands. "
            "NEW COMPOSITION (hard): Saturn fills the RIGHT half of the frame — a large butterscotch-gold "
            "OBLATE banded globe on the right. The ring sheet sweeps in from the LEFT side of the frame "
            "and runs into Saturn's equator: the INNER edge of the rings clearly meets / touches the planet's curve. "
            "Near-edge-on thin bright blade. "
            "CRITICAL — NO falling streaks, NO rain lines, NO particles scattering, NO vertical streaks, "
            "NO ice drifting off into empty space. The still is a locked composition only; motion comes later. "
            "No Orbit. No spacecraft. No title. "
            + STYLE
        ),
        "checks": ["no_streaks", "saturn_right", "no_orbit"],
    },
    {
        "file": "saturn_bare_orbit_v04.png",
        "role": "bare-saturn-orbit-tiny",
        "refs": ["orbit", "bare_body"],
        "prompt": (
            ORBIT_LOCK
            + " "
            "Second attached image is the correct bare Saturn body — use THAT planet (oblate, butterscotch bands, NO rings, NO oval storm). "
            "COMPOSITION: bare Saturn fills about 60 percent of the frame HEIGHT, centered-ish, crisp parallel bands, "
            "side-lit with a clear shadowed crescent edge on one side. Empty black space where rings were. "
            "Orbit is TINY at one edge of the frame (far left or far right), looking back at the bare equator — "
            "inquisitive, not waving, not the hero. No rings. No spacecraft. "
            + STYLE
        ),
        "checks": ["orbit_tiny", "oblate", "no_rings"],
    },
    {
        "file": "saturn_ice_chunks_v04.png",
        "role": "ice-crowd-floating",
        "refs": [],
        "prompt": (
            "Camera slightly BELOW the ring plane looking up-along a THIN FLOATING LAYER of bright white "
            "water-ice chunks (a few lightly dust-tinted cream). "
            "CRITICAL: chunks float with BLACK SPACE between them and BLACK SPACE beneath them — "
            "NOT a ground surface, NOT a rubble floor, NOT a horizon of packed rock, NOT a reflective plane. "
            "A sparse-to-moderate crowd of ice suspended in a thin sheet. Saturn LARGE behind the sheet "
            "(butterscotch-gold OBLATE bands, rings continuing as this plane). "
            "No Orbit. No spacecraft. No dark circular hole cut in a floor. "
            + STYLE
        ),
        "checks": ["not_floor", "black_space_beneath", "saturn_large"],
    },
    {
        "file": "saturn_orbit_tumble_v04.png",
        "role": "orbit-tumble-sparse",
        "refs": ["orbit", "ring_look"],
        "prompt": (
            ORBIT_LOCK
            + " "
            "Second image is Saturn with rings for planet identity. "
            "CLOSE: Orbit MID-AIR and TILTED (tumbling), NOT sitting, NOT standing, NOT resting on ice, NOT waving. "
            "Eyes wide (curious). ONE stubby hand reaching for a single passing ice chunk. "
            "Ice chunks are SPARSE and floating at all depths with BLACK SPACE around them; "
            "a few chunks pass close to camera. Thin ring sheet — a crowd of ice in open space, not a floor. "
            "Saturn huge in background WITH rings. Exactly one Orbit. No spacecraft. "
            + STYLE
        ),
        "checks": ["mid_air", "not_waving", "sparse_ice"],
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
    for p in (ORBIT_REF, RING_LOOK, BARE_BODY):
        if not p.is_file():
            raise SystemExit(f"Missing ref: {p}")

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)

    # Clean prior UAT pack images
    for p in list(UAT.glob("*")):
        if p.is_file() and (
            p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            or p.name in {"MANIFEST.json", "README.md", "SHA256.md"}
        ):
            p.unlink()
            print(f"uat_rm {p.name}", flush=True)

    manifest: dict = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "veo": False,
        "ben_round": "3",
        "ben_notes_at": "2026-09-30T22:21+01:00",
        "orbit_reference": str(ORBIT_REF.relative_to(REPO)),
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
            elif ref == "ring_look":
                contents.append(
                    types.Part.from_bytes(data=RING_LOOK.read_bytes(), mime_type="image/png")
                )
            elif ref == "bare_body":
                contents.append(
                    types.Part.from_bytes(data=BARE_BODY.read_bytes(), mime_type="image/png")
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
            "checks_requested": spec["checks"],
            "path": str(dest),
            "uat_path": str(uat_dest),
            "refs": spec["refs"],
        }
        manifest["stills"].append(row)
        print(f"  wrote {nbytes} sha={h}", flush=True)

    manifest["images_generated_this_pass"] = generated
    manifest["estimated_usd_list_price"] = round(generated * USD_PER_IMAGE, 4)
    manifest["billing_note"] = (
        f"Vertex Free Trial {PROJECT}; not AI Studio prepay. "
        f"List estimate ${USD_PER_IMAGE}/image × {generated}."
    )
    manifest["pack_order"] = [s["file"] for s in STILLS]
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (UAT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    sha_lines = ["# SHA-256 — saturn_stills_v04_for_ben_ok", "", "| File | SHA-256 | Bytes |", "|---|---|---:|"]
    for name in manifest["pack_order"]:
        p = UAT / name
        sha_lines.append(f"| `{name}` | `{sha256(p)}` | {p.stat().st_size} |")
    (UAT / "SHA256.md").write_text("\n".join(sha_lines) + "\n")
    (UAT / "README.md").write_text(
        """# Saturn stills v04 — Ben OK (Round 3 · 30 Sep 22:21)

**Vertex only. No Veo on these until Ben OK.**

| # | File | Brief |
|---|---|---|
| 1 | `saturn_open_rings_v04.png` | Saturn RIGHT half; rings from LEFT meet equator; NO streaks; no Orbit |
| 2 | `saturn_bare_orbit_v04.png` | Oblate bare ~60% height; side-lit crescent; Orbit tiny looking back |
| 3 | `saturn_ice_chunks_v04.png` | Thin floating ice layer; black space between/beneath; not a floor |
| 4 | `saturn_orbit_tumble_v04.png` | Mid-air tumble; sparse floating chunks; eyes wide; reaching; not sitting/waving |

Approved separately for Veo already: young rings · Cassini (not in this folder).
"""
    )
    print(
        json.dumps(
            {
                "STILLS_V04_DONE": True,
                "images_generated": generated,
                "estimated_usd": manifest["estimated_usd_list_price"],
                "out": str(OUT),
                "uat": str(UAT),
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
