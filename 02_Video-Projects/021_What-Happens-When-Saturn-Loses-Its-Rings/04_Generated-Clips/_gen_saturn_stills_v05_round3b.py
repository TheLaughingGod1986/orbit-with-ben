#!/usr/bin/env python3
"""Saturn stills v05 — Ben Round 3b (30 Sep 22:46 London). Vertex Free Trial only. No Veo here.

B OPENING: EDIT saturn_open_rings_v03.png — remove vertical streaks, mirror so Saturn RIGHT,
  rings from LEFT; widen/outpaint right so more Saturn shows. Keep blade look. No Orbit.
C ICE CROWD: reference-guided from approved saturn_orbit_tumble_v04.png — same sparse chunks /
  black space / rings+Saturn behind, NO Orbit, a few chunks closer to camera. No mirrored planet.
D BARE SATURN: keep size/colour from saturn_bare_orbit_v04.png; soft gradual shadowed crescent
  (not straight-cut edge); Orbit smaller, seen from BEHIND (antenna+back), turned toward bare equator.

Self-check before UAT. STOP — no Veo on these until Ben OK.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
STILLS_V03 = EP / "04_Generated-Clips" / "stills_v03"
STILLS_V04 = EP / "04_Generated-Clips" / "stills_v04"
OUT = EP / "04_Generated-Clips" / "stills_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v05_for_ben_ok"
)
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)
OPEN_V03 = STILLS_V03 / "saturn_open_rings_v03.png"
TUMBLE_V04 = STILLS_V04 / "saturn_orbit_tumble_v04.png"
BARE_V04 = STILLS_V04 / "saturn_bare_orbit_v04.png"

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"
USD_PER_IMAGE = 0.039

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint pinprick stars. "
    "Exactly ONE Saturn — soft butterscotch-gold banded gas giant, visibly OBLATE. "
    "NOT Jupiter: no Great Red Spot, no oval storm. "
    "No Earth, no second planet, no humans, no text, no logos, no watermark, no UI."
)

ORBIT_LOCK = (
    "CRITICAL — match the attached Orbit identity reference EXACTLY. "
    "Glossy metallic orange rounded floating robot, NO legs. "
    "Large black curved visor; two cream eyes with dark pupils when face is visible; "
    "stubby orange arms with dark three-finger hands; one antenna with glowing bulb tip; "
    "exactly ONE soft bottom underside glow. Exactly ONE Orbit. Small garnish."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src: Path | bytes, dest: Path) -> None:
    data = src if isinstance(src, bytes) else src.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    chunk = 500 * 1024
    with open(tmp, "wb") as o:
        for i in range(0, len(data), chunk):
            o.write(data[i : i + chunk])
            o.flush()
    tmp.replace(dest)
    if dest.stat().st_size != len(data):
        raise RuntimeError(f"size mismatch writing {dest}")


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


def prepare_open_preedit(work: Path) -> Path:
    """Mirror v03 so Saturn is on the RIGHT; keep blade look. Streaks still present for inpaint."""
    work.mkdir(parents=True, exist_ok=True)
    mirrored = work / "open_v03_mirrored.png"
    img = Image.open(OPEN_V03).convert("RGB")
    img.transpose(Image.FLIP_LEFT_RIGHT).save(mirrored, "PNG")
    print(f"  mirrored {OPEN_V03.name} -> {mirrored.name} size={img.size}", flush=True)
    return mirrored


def generate_edit(client: genai.Client, contents: list, dest: Path) -> int:
    nbytes = 0
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            nbytes = save_response(response, dest)
            if dest.stat().st_size >= 10_000:
                return nbytes
        except Exception as e:
            last_err = e
            print(f"  retry {attempt + 1}: {e}", flush=True)
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"FAILED {dest}: {last_err}")


def main() -> None:
    for p in (OPEN_V03, TUMBLE_V04, BARE_V04, ORBIT_REF):
        if not p.is_file():
            raise SystemExit(f"Missing: {p}")

    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)
    work = OUT / "_work"
    work.mkdir(parents=True, exist_ok=True)

    # Clean prior UAT pack images
    for p in list(UAT.glob("*")):
        if p.is_file() and (
            p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            or p.name in {"MANIFEST.json", "README.md", "SHA256.md"}
        ):
            try:
                p.unlink()
            except OSError as e:
                print(f"uat_rm skip {p.name}: {e}", flush=True)

    manifest: dict = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "veo": False,
        "ben_round": "3b",
        "ben_notes_at": "2026-09-30T22:46+01:00",
        "usd_per_image_list_estimate": USD_PER_IMAGE,
        "stills": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    generated = 0

    # --- B OPENING: edit mirrored v03 ---
    open_dest = OUT / "saturn_open_rings_v05.png"
    print(f"still {open_dest.name} EDIT from v03 (mirror + destreak + widen)", flush=True)
    mirrored = prepare_open_preedit(work)
    open_prompt = (
        "IMAGE EDIT — do NOT invent a new scene from scratch. "
        "The attached image is already mirrored so Saturn is on the RIGHT and the ring blade "
        "sweeps in from the LEFT toward Saturn. "
        "KEEP the ring blade look EXACTLY: bright thin fine-banded cream/white blade, same gaps/bands. "
        "1) REMOVE all vertical streaks / rain lines / falling particle trails under the rings — "
        "replace that region with clean near-black space. "
        "2) WIDEN / OUTPAINT the RIGHT side so MORE of Saturn's disk shows (aim for Saturn filling "
        "roughly the right half of the frame), while the INNER edge of the rings still clearly "
        "meets the planet's equator curve. "
        "3) Do not add Orbit, spacecraft, text, a second planet, or new streak motion. "
        "Preserve lighting and the blade look. "
        + STYLE
    )
    generate_edit(
        client,
        [
            types.Part.from_bytes(data=mirrored.read_bytes(), mime_type="image/png"),
            open_prompt,
        ],
        open_dest,
    )
    generated += 1
    print(f"  wrote {open_dest.stat().st_size} sha={sha256(open_dest)}", flush=True)

    # --- C ICE CROWD: from approved tumble ---
    ice_dest = OUT / "saturn_ice_chunks_v05.png"
    print(f"still {ice_dest.name} from approved Orbit-in-rings ref (NO Orbit)", flush=True)
    ice_prompt = (
        "REFERENCE-GUIDED EDIT of the attached APPROVED still. "
        "Keep the SAME sparse white ice chunks floating at all depths with BLACK SPACE around them, "
        "the same rings plane, and the same Saturn behind. "
        "REMOVE Orbit completely — no orange robot anywhere. "
        "Move a FEW ice chunks CLOSER to camera (foreground floaters) while keeping the crowd sparse. "
        "CRITICAL: no mirrored / reflected planet under the ice; no glass floor; no rubble ground surface; "
        "black space beneath the floating layer. "
        "No spacecraft, no text. "
        + STYLE
    )
    generate_edit(
        client,
        [
            types.Part.from_bytes(data=TUMBLE_V04.read_bytes(), mime_type="image/png"),
            ice_prompt,
        ],
        ice_dest,
    )
    generated += 1
    print(f"  wrote {ice_dest.stat().st_size} sha={sha256(ice_dest)}", flush=True)

    # --- D BARE SATURN ---
    bare_dest = OUT / "saturn_bare_orbit_v05.png"
    print(f"still {bare_dest.name} edit bare+Orbit (soft crescent, Orbit from behind)", flush=True)
    bare_prompt = (
        ORBIT_LOCK
        + " "
        "First attached image is the CURRENT bare-Saturn composition — KEEP the same planet SIZE and COLOUR "
        "(oblate butterscotch bands, ~60% frame height, NO rings). "
        "EDIT: replace the hard/straight-cut right edge of the planet with a SOFT, GRADUAL shadowed crescent "
        "(side-lit; shadow falls off smoothly into space, not a clipped disk edge). "
        "Second attached image is Orbit identity. "
        "Orbit must be SMALLER than in the first image, placed at one edge, seen from BEHIND "
        "(solid matte orange back + antenna stem visible; NO second face / NO rear visor). "
        "Orbit is turned toward the planet's bare equator, NOT facing the camera. "
        "No rings, no spacecraft, no text. "
        + STYLE
    )
    generate_edit(
        client,
        [
            types.Part.from_bytes(data=BARE_V04.read_bytes(), mime_type="image/png"),
            types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png"),
            bare_prompt,
        ],
        bare_dest,
    )
    generated += 1
    print(f"  wrote {bare_dest.stat().st_size} sha={sha256(bare_dest)}", flush=True)

    pack = [
        ("saturn_open_rings_v05.png", "open-edit-from-v03", ["no_streaks", "saturn_right", "blade_kept", "no_orbit"]),
        ("saturn_ice_chunks_v05.png", "ice-from-tumble-ref", ["no_orbit", "sparse_chunks", "no_mirror_planet", "closer_chunks"]),
        ("saturn_bare_orbit_v05.png", "bare-soft-crescent-orbit-back", ["soft_crescent", "orbit_from_behind", "orbit_smaller", "no_rings"]),
    ]
    for fname, role, checks in pack:
        dest = OUT / fname
        h = sha256(dest)
        uat_dest = UAT / fname
        chunk_write(dest, uat_dest)
        if sha256(uat_dest) != h:
            chunk_write(dest, uat_dest)
        manifest["stills"].append(
            {
                "file": fname,
                "role": role,
                "bytes": dest.stat().st_size,
                "sha256": h,
                "model": MODEL,
                "engine": "vertex",
                "checks_requested": checks,
                "path": str(dest),
                "uat_path": str(uat_dest),
            }
        )

    manifest["images_generated_this_pass"] = generated
    manifest["estimated_usd_list_price"] = round(generated * USD_PER_IMAGE, 4)
    manifest["billing_note"] = (
        f"Vertex Free Trial {PROJECT}; not AI Studio prepay. "
        f"List estimate ${USD_PER_IMAGE}/image × {generated}."
    )
    manifest["pack_order"] = [p[0] for p in pack]
    manifest["source_notes"] = {
        "open": "EDIT saturn_open_rings_v03.png (mirror + destreak + widen); not from-scratch",
        "ice": "Reference-guided from APPROVED saturn_orbit_tumble_v04.png; Orbit removed",
        "bare": "EDIT saturn_bare_orbit_v04.png soft crescent + Orbit from behind",
    }
    manifest["self_check"] = {
        "open": "CHECK visually — no streaks; Saturn right; blade look; no Orbit",
        "ice": "CHECK visually — no Orbit; sparse chunks; no mirrored planet under ice",
        "bare": "CHECK visually — soft crescent (not straight cut); Orbit smaller from behind toward equator",
    }
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(OUT / "MANIFEST.json", UAT / "MANIFEST.json")

    sha_lines = [
        "# SHA-256 — saturn_stills_v05_for_ben_ok",
        "",
        "| File | SHA-256 | Bytes |",
        "|---|---|---:|",
    ]
    for name in manifest["pack_order"]:
        p = UAT / name
        sha_lines.append(f"| `{name}` | `{sha256(p)}` | {p.stat().st_size} |")
    sha_text = "\n".join(sha_lines) + "\n"
    (OUT / "SHA256.md").write_text(sha_text)
    chunk_write(sha_text.encode(), UAT / "SHA256.md")

    readme = """# Saturn stills v05 — Ben OK (Round 3b · 30 Sep 22:46)

**Vertex only. No Veo on these until Ben OK.**

Orbit-in-rings v04 is APPROVED separately (Veo already).

| # | File | Brief |
|---|---|---|
| B | `saturn_open_rings_v05.png` | EDIT of v03: destreak + mirror Saturn RIGHT + widen; blade look; no Orbit |
| C | `saturn_ice_chunks_v05.png` | From approved tumble: same sparse ice/Saturn/rings, NO Orbit; closer chunks; no mirrored planet |
| D | `saturn_bare_orbit_v05.png` | Soft gradual crescent; Orbit smaller from behind toward bare equator |
"""
    (OUT / "README.md").write_text(readme)
    chunk_write(readme.encode(), UAT / "README.md")

    print(
        json.dumps(
            {
                "STILLS_V05_DONE": True,
                "images_generated": generated,
                "estimated_usd": manifest["estimated_usd_list_price"],
                "out": str(OUT),
                "uat": str(UAT),
                "sha256": {s["file"]: s["sha256"] for s in manifest["stills"]},
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
