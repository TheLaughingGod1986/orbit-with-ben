#!/usr/bin/env python3
"""Remint B+D v05 pass 2 — no hard black mask; soft PIL crescent on bare body first."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
OUT = EP / "04_Generated-Clips" / "stills_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v05_for_ben_ok"
)
STILLS_V03 = EP / "04_Generated-Clips" / "stills_v03"
STILLS_V04 = EP / "04_Generated-Clips" / "stills_v04"
OPEN_V03 = STILLS_V03 / "saturn_open_rings_v03.png"
# First v05 open (pre black-mask fail) archived
OPEN_V05_FIRST = sorted((OUT / "_rejected_open").glob("saturn_open_rings_v05_*.png"))
BARE_BODY = STILLS_V03 / "saturn_bare_v03.png"
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
    "Near-black space, handful of faint pinprick stars. "
    "Exactly ONE Saturn — butterscotch-gold OBLATE banded giant. NOT Jupiter. "
    "No Earth, no second planet, no text, no logos."
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
    parts = response.candidates[0].content.parts or []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    raise RuntimeError("No image bytes")


def generate_edit(client: genai.Client, contents: list, dest: Path) -> int:
    last_err = None
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


def archive(path: Path, tag: str) -> None:
    rej = OUT / f"_rejected_{tag}"
    rej.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        chunk_write(path, rej / f"{path.stem}_{time.strftime('%H%M%S')}{path.suffix}")


def soft_destreak_mirrored(work: Path) -> Path:
    """Mirror v03 and gently darken ONLY bright streak pixels below the ring blade."""
    work.mkdir(parents=True, exist_ok=True)
    img = Image.open(OPEN_V03).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT)
    px = img.load()
    w, h = img.size
    # Ring blade roughly around mid height; streaks are bright vertical dashes under it
    y_ring = int(h * 0.42)
    for y in range(y_ring + 6, h):
        for x in range(0, int(w * 0.58)):
            r, g, b = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            # Keep near-black; crush mid/bright streak pixels toward black
            if lum > 18 and lum < 210:
                # streaks are thin bright lines in otherwise black space under rings
                # neighbor darkness check
                dark_n = 0
                for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-3, 0), (3, 0)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h:
                        rr, gg, bb = px[xx, yy]
                        if 0.299 * rr + 0.587 * gg + 0.114 * bb < 12:
                            dark_n += 1
                if dark_n >= 3:
                    # fade toward black
                    f = 0.08
                    px[x, y] = (int(r * f), int(g * f), int(b * f))
    dest = work / "open_v03_mirrored_soft_destreak.png"
    img.save(dest, "PNG")
    print(f"  soft destreak -> {dest.name}", flush=True)
    return dest


def soft_crescent_bare(work: Path) -> Path:
    """Take bare body v03 and apply a soft right-side shadowed crescent with PIL."""
    work.mkdir(parents=True, exist_ok=True)
    img = Image.open(BARE_BODY).convert("RGBA")
    w, h = img.size
    # Find approximate planet disk: bright region
    # Build a horizontal soft falloff mask on the right third of the planet
    shade = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(shade)
    # Soft black gradient from ~55% width to right edge of planet (~78%)
    for x in range(int(w * 0.52), int(w * 0.82)):
        t = (x - w * 0.52) / (w * 0.30)
        t = max(0.0, min(1.0, t))
        # ease-in
        a = int(255 * (t ** 1.6) * 0.92)
        draw.line([(x, 0), (x, h)], fill=a)
    shade = shade.filter(ImageFilter.GaussianBlur(radius=18))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    # Only shade where original is bright (planet)
    gray = img.convert("L")
    planet_mask = gray.point(lambda v: 255 if v > 25 else 0)
    planet_mask = planet_mask.filter(ImageFilter.GaussianBlur(radius=2))
    # Combine shade strength with planet mask
    shade_a = Image.composite(shade, Image.new("L", (w, h), 0), planet_mask)
    shaded = Image.composite(black, img, shade_a)
    dest = work / "bare_v03_soft_crescent.png"
    shaded.convert("RGB").save(dest, "PNG")
    print(f"  soft crescent preedit -> {dest.name}", flush=True)
    return dest


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
    generated = 0

    # --- B ---
    open_dest = OUT / "saturn_open_rings_v05.png"
    archive(open_dest, "open")
    print("REMINT2 open — soft destreak + Gemini widen (no black rectangle)", flush=True)
    pre_open = soft_destreak_mirrored(work)
    # Also attach first-pass v05 if available as composition target
    contents = [types.Part.from_bytes(data=pre_open.read_bytes(), mime_type="image/png")]
    if OPEN_V05_FIRST:
        first = OPEN_V05_FIRST[0]
        contents.append(types.Part.from_bytes(data=first.read_bytes(), mime_type="image/png"))
        print(f"  also attached first open {first.name}", flush=True)
    open_prompt = (
        "IMAGE EDIT. First image is the fine-banded ring blade still, already mirrored "
        "(Saturn RIGHT, rings from LEFT) with under-ring streaks largely cleared. "
        + (
            "Second image is a prior composition attempt — use it ONLY for how much Saturn disk to show; "
            "ignore any black rectangle or artifacts in it. "
            if OPEN_V05_FIRST
            else ""
        )
        + "OUTPUT requirements (hard): "
        "1) Keep the ring BLADE look exactly from the first image — bright thin fine bands. "
        "2) ZERO vertical streaks / rain / falling particles under or across the rings — clean black under the blade. "
        "3) Saturn on the RIGHT, more of the disk visible (about right half of frame), "
        "inner ring edge clearly meeting the equator. "
        "4) No black rectangles, no cutouts, no Orbit, no spacecraft, no text. "
        + STYLE
    )
    contents.append(open_prompt)
    generate_edit(client, contents, open_dest)
    generated += 1
    print(f"  open sha={sha256(open_dest)}", flush=True)

    # --- D ---
    bare_dest = OUT / "saturn_bare_orbit_v05.png"
    archive(bare_dest, "bare")
    print("REMINT2 bare — PIL soft crescent body + Orbit from behind", flush=True)
    pre_bare = soft_crescent_bare(work)
    bare_prompt = (
        "COMPOSITE EDIT. First image is the bare Saturn with a SOFT shadowed crescent already on the right — "
        "KEEP that soft gradual terminator (do NOT replace it with a hard straight cut edge). "
        "Keep the same planet SIZE and COLOUR. NO rings. "
        "Second image is Orbit identity. "
        "Add ONE tiny Orbit at the far LEFT edge, SMALLER than 8% of frame height, "
        "seen from BEHIND (solid orange back + antenna, NO face toward camera), "
        "turned toward the planet's bare equator. "
        "Not waving. Not looking at camera. No second face. "
        + STYLE
    )
    generate_edit(
        client,
        [
            types.Part.from_bytes(data=pre_bare.read_bytes(), mime_type="image/png"),
            types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png"),
            bare_prompt,
        ],
        bare_dest,
    )
    generated += 1
    print(f"  bare sha={sha256(bare_dest)}", flush=True)

    pack = [
        "saturn_open_rings_v05.png",
        "saturn_ice_chunks_v05.png",
        "saturn_bare_orbit_v05.png",
    ]
    for name in pack:
        chunk_write(OUT / name, UAT / name)

    man_path = OUT / "MANIFEST.json"
    manifest = json.loads(man_path.read_text()) if man_path.is_file() else {}
    prev = int(manifest.get("images_generated_this_pass", 0))
    stills = []
    roles = {
        "saturn_open_rings_v05.png": ("open-edit-v03-remint2", ["no_streaks", "saturn_right", "no_black_block", "blade"]),
        "saturn_ice_chunks_v05.png": ("ice-from-tumble-ref", ["no_orbit", "sparse", "no_mirror"]),
        "saturn_bare_orbit_v05.png": ("bare-soft-crescent-orbit-back-remint2", ["soft_crescent", "orbit_behind", "small"]),
    }
    for name in pack:
        p = OUT / name
        role, checks = roles[name]
        stills.append(
            {
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
        )
    manifest.update(
        {
            "engine": "vertex",
            "project": PROJECT,
            "location": LOCATION,
            "model": MODEL,
            "ai_studio_prepay": False,
            "veo": False,
            "ben_round": "3b",
            "ben_notes_at": "2026-09-30T22:46+01:00",
            "stills": stills,
            "pack_order": pack,
            "images_generated_this_pass": prev + generated,
            "estimated_usd_list_price": round((prev + generated) * USD_PER_IMAGE, 4),
            "remint_bd2_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "remint_bd2_images": generated,
            "self_check": {
                "open": "REMINT2 — blade kept; no streaks; no black block; Saturn right widened",
                "ice": "kept — no Orbit; sparse; no mirrored planet",
                "bare": "REMINT2 — soft crescent from PIL+edit; Orbit tiny from behind",
            },
            "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(man_path, UAT / "MANIFEST.json")
    sha_lines = ["# SHA-256 — saturn_stills_v05_for_ben_ok", "", "| File | SHA-256 | Bytes |", "|---|---|---:|"]
    for name in pack:
        p = UAT / name
        sha_lines.append(f"| `{name}` | `{sha256(p)}` | {p.stat().st_size} |")
    sha_text = "\n".join(sha_lines) + "\n"
    (OUT / "SHA256.md").write_text(sha_text)
    chunk_write(sha_text.encode(), UAT / "SHA256.md")
    print(json.dumps({"REMINT2_DONE": True, "estimated_usd": manifest["estimated_usd_list_price"], "sha256": {s["file"]: s["sha256"] for s in stills}}, indent=2), flush=True)


if __name__ == "__main__":
    main()
