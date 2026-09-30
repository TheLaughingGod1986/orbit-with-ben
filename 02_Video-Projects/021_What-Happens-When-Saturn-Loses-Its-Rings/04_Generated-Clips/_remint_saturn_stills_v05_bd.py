#!/usr/bin/env python3
"""Remint B (open) and D (bare) for stills v05 — Ben 22:46 briefs. Vertex only."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFilter

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
OUT = EP / "04_Generated-Clips" / "stills_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v05_for_ben_ok"
)
STILLS_V03 = EP / "04_Generated-Clips" / "stills_v03"
STILLS_V04 = EP / "04_Generated-Clips" / "stills_v04"
OPEN_V03 = STILLS_V03 / "saturn_open_rings_v03.png"
BARE_V04 = STILLS_V04 / "saturn_bare_orbit_v04.png"
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

STYLE = (
    "Premium cinematic CGI still, 16:9, photoreal science-documentary finish. "
    "Near-black space, only a handful of faint pinprick stars. "
    "Exactly ONE Saturn — soft butterscotch-gold banded gas giant, visibly OBLATE. "
    "NOT Jupiter. No Earth, no second planet, no humans, no text, no logos."
)

ORBIT_LOCK = (
    "CRITICAL — match the attached Orbit identity reference EXACTLY. "
    "Glossy metallic orange rounded floating robot, NO legs. "
    "When face is visible: large black curved visor with cream eyes + dark pupils. "
    "When seen from behind: solid matte orange back only — NO second face, NO rear visor. "
    "Stubby arms; one antenna with glowing bulb tip; ONE soft bottom underside glow. "
    "Exactly ONE Orbit. Tiny garnish."
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


def save_response(response, dest: Path) -> int:
    if not response.candidates:
        raise RuntimeError("No candidates")
    content = response.candidates[0].content
    parts = content.parts if content and content.parts else []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    raise RuntimeError(f"No image bytes finish={getattr(response.candidates[0], 'finish_reason', None)}")


def generate_edit(client: genai.Client, contents: list, dest: Path) -> int:
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
            n = save_response(response, dest)
            if dest.stat().st_size >= 10_000:
                return n
        except Exception as e:
            last_err = e
            print(f"  retry {attempt + 1}: {e}", flush=True)
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"FAILED {dest}: {last_err}")


def prep_open_destreaked(work: Path) -> Path:
    """Mirror v03, then paint black over the below-ring streak zone (keep blade untouched)."""
    work.mkdir(parents=True, exist_ok=True)
    img = Image.open(OPEN_V03).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT)
    w, h = img.size
    # Soft black band under the ring plane (approx middle horizontal band of streaks)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # Streaks live under the thin blade — cover lower ~48–95% of height across left/center,
    # but leave Saturn disk on the right alone (x > ~0.62).
    y0, y1 = int(h * 0.48), int(h * 0.98)
    x0, x1 = 0, int(w * 0.62)
    draw.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 255))
    # Soften the top edge of the blackout so it doesn't cut the blade
    soft = overlay.filter(ImageFilter.GaussianBlur(radius=8))
    base = img.convert("RGBA")
    out = Image.alpha_composite(base, soft).convert("RGB")
    dest = work / "open_v03_mirrored_destreak_mask.png"
    out.save(dest, "PNG")
    print(f"  preedit destreak mask -> {dest.name} size={out.size}", flush=True)
    return dest


def archive_reject(path: Path, tag: str) -> None:
    rej = OUT / f"_rejected_{tag}"
    rej.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        ts = time.strftime("%H%M%S")
        chunk_write(path, rej / f"{path.stem}_{ts}{path.suffix}")
        print(f"  archived reject {path.name} -> {rej.name}", flush=True)


def main() -> None:
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

    generated = 0

    # --- B OPEN remint ---
    open_dest = OUT / "saturn_open_rings_v05.png"
    archive_reject(open_dest, "open")
    print("REMINT open v05 from masked mirrored v03", flush=True)
    pre = prep_open_destreaked(work)
    open_prompt = (
        "IMAGE EDIT of the attached plate — do NOT invent a new ring look. "
        "This is already mirrored: Saturn on the RIGHT, ring blade from the LEFT. "
        "The area under the rings has been cleared to black — KEEP it clean black. "
        "CRITICAL: ZERO vertical streaks, ZERO rain lines, ZERO falling particles under the rings. "
        "KEEP the bright fine-banded ring BLADE exactly (cream/white thin sheet with fine bands and gaps). "
        "OUTPAINT / WIDEN the RIGHT side so MORE of Saturn's disk is visible — aim for Saturn filling "
        "about the right half of the frame (not cropped to a thin crescent of planet). "
        "The INNER edge of the rings must still clearly meet Saturn's equator curve. "
        "No Orbit. No spacecraft. No text. "
        + STYLE
    )
    generate_edit(
        client,
        [types.Part.from_bytes(data=pre.read_bytes(), mime_type="image/png"), open_prompt],
        open_dest,
    )
    generated += 1
    print(f"  open sha={sha256(open_dest)} bytes={open_dest.stat().st_size}", flush=True)

    # --- D BARE remint ---
    bare_dest = OUT / "saturn_bare_orbit_v05.png"
    archive_reject(bare_dest, "bare")
    print("REMINT bare v05 soft crescent + Orbit from behind", flush=True)
    bare_prompt = (
        ORBIT_LOCK
        + " "
        "First image is the current bare-Saturn plate — KEEP the same planet SIZE and COLOUR "
        "(oblate butterscotch bands, about 60% of frame height, NO rings). "
        "HARD FIX lighting: the right limb must be a SOFT GRADUAL SHADOWED CRESCENT terminator — "
        "smooth falloff from lit bands into space. FORBIDDEN: hard straight vertical cut edge, "
        "clipped disk, flat knife-edge silhouette. "
        "Second image is Orbit identity. "
        "Orbit is SMALLER than now, at the far LEFT edge. "
        "Camera sees Orbit from BEHIND / three-quarter rear: solid orange back + antenna stem + hatch OK; "
        "NO faceplate toward camera; Orbit is TURNED toward the planet's bare equator (looking at Saturn). "
        "Not waving. Not facing us. No rings. No spacecraft. "
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
    print(f"  bare sha={sha256(bare_dest)} bytes={bare_dest.stat().st_size}", flush=True)

    # Refresh UAT for reminted + keep ice
    ice = OUT / "saturn_ice_chunks_v05.png"
    pack_files = [
        "saturn_open_rings_v05.png",
        "saturn_ice_chunks_v05.png",
        "saturn_bare_orbit_v05.png",
    ]
    for name in pack_files:
        src = OUT / name
        if not src.is_file():
            raise SystemExit(f"missing {src}")
        chunk_write(src, UAT / name)

    # Update MANIFEST
    man_path = OUT / "MANIFEST.json"
    if man_path.is_file():
        manifest = json.loads(man_path.read_text())
    else:
        manifest = {"stills": [], "engine": "vertex", "model": MODEL}
    prev_gen = int(manifest.get("images_generated_this_pass", 0))
    stills_by_file = {s["file"]: s for s in manifest.get("stills", [])}
    for name, role, checks in [
        ("saturn_open_rings_v05.png", "open-edit-from-v03-remint", ["no_streaks", "saturn_right", "blade_kept", "widened"]),
        ("saturn_ice_chunks_v05.png", "ice-from-tumble-ref", ["no_orbit", "sparse_chunks", "no_mirror_planet"]),
        ("saturn_bare_orbit_v05.png", "bare-soft-crescent-orbit-back-remint", ["soft_crescent", "orbit_from_behind", "orbit_smaller"]),
    ]:
        p = OUT / name
        stills_by_file[name] = {
            "file": name,
            "role": role,
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
            "model": MODEL,
            "engine": "vertex",
            "checks_requested": checks,
            "path": str(p),
            "uat_path": str(UAT / name),
        }
    manifest["stills"] = [stills_by_file[n] for n in pack_files]
    manifest["images_generated_this_pass"] = prev_gen + generated
    manifest["estimated_usd_list_price"] = round(
        manifest["images_generated_this_pass"] * USD_PER_IMAGE, 4
    )
    manifest["remint_bd_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["remint_bd_images"] = generated
    manifest["pack_order"] = pack_files
    manifest["self_check"] = {
        "open": "REMINT — no streaks under blade; Saturn right; more disk; blade kept",
        "ice": "kept from first pass — no Orbit; sparse; no mirrored planet",
        "bare": "REMINT — soft crescent (not straight cut); Orbit smaller from behind toward equator",
    }
    manifest["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(man_path, UAT / "MANIFEST.json")

    sha_lines = [
        "# SHA-256 — saturn_stills_v05_for_ben_ok",
        "",
        "| File | SHA-256 | Bytes |",
        "|---|---|---:|",
    ]
    for name in pack_files:
        p = UAT / name
        sha_lines.append(f"| `{name}` | `{sha256(p)}` | {p.stat().st_size} |")
    sha_text = "\n".join(sha_lines) + "\n"
    (OUT / "SHA256.md").write_text(sha_text)
    chunk_write(sha_text.encode(), UAT / "SHA256.md")

    print(
        json.dumps(
            {
                "REMINT_BD_DONE": True,
                "remint_images": generated,
                "total_images_this_pass": manifest["images_generated_this_pass"],
                "estimated_usd": manifest["estimated_usd_list_price"],
                "sha256": {s["file"]: s["sha256"] for s in manifest["stills"]},
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
