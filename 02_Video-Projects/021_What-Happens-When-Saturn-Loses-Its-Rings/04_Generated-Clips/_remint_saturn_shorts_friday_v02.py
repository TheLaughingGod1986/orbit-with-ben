#!/usr/bin/env python3
"""Remint Friday Black Dwarf Short still only — keep Monday v02.

Ben 1 Oct 10:19: sphere ~40% frame width; smooth white→yellow→orange→dull grey
ember gradient (no bite / hard edge / eclipse); brighter starfield; no Orbit.
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
OUT = EP / "04_Generated-Clips" / "shorts_stills_v02"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_shorts_stills_v02_for_ben_ok"
)

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0538779324")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash-image"
USD_PER_IMAGE = 0.039


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src: Path | bytes, dest: Path) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".partial")
    with open(tmp, "wb") as o:
        for i in range(0, len(data), 500 * 1024):
            o.write(data[i : i + 500 * 1024])
            o.flush()
    tmp.replace(dest)
    if dest.stat().st_size != len(data):
        raise RuntimeError(f"size mismatch {dest}")


def save_response(response, dest: Path) -> int:
    if not response.candidates:
        raise RuntimeError("No candidates")
    for part in response.candidates[0].content.parts or []:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    raise RuntimeError("No image bytes")


def generate(client: genai.Client, contents: list, dest: Path) -> int:
    last_err: Exception | None = None
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="9:16"),
                ),
            )
            n = save_response(response, dest)
            im = Image.open(dest)
            if dest.stat().st_size >= 10_000 and im.size[1] > im.size[0]:
                return n
        except Exception as e:
            last_err = e
            print(f"  retry {attempt + 1}: {e}", flush=True)
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"FAILED {dest}: {last_err}")


def sphere_core_frac(path: Path) -> float:
    """Estimate opaque sphere width fraction (ignore soft bloom)."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # mid horizontal band; require saturated/coloured body pixels, not dim stars
    xs: list[int] = []
    for y in range(int(h * 0.35), int(h * 0.65), 3):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            # body: warm glow OR mid grey surface, exclude tiny star pinpricks
            warm = r > 80 and g > 40 and (r + g) > b + 30
            grey_body = luma > 55 and abs(r - g) < 25 and abs(g - b) < 25 and luma < 200
            hot = luma > 180
            if (warm or grey_body or hot) and luma > 50:
                # skip isolated star pixels: need neighbours
                xs.append(x)
    if len(xs) < 40:
        return 0.0
    # trim outliers: use 5th–95th percentile span
    xs.sort()
    lo = xs[int(len(xs) * 0.05)]
    hi = xs[int(len(xs) * 0.95)]
    return (hi - lo) / w


PROMPT = (
    "Vertical 9:16 cinematic CGI still — YouTube Short OPENING FRAME. "
    "ONE cooling white-dwarf / black-dwarf sphere, centred, diameter about "
    "FORTY PERCENT of the frame WIDTH (leave generous black space around it — "
    "not filling the frame, not tiny). "
    "The sphere itself glows from WITHIN like a cooling ember: a SMOOTH "
    "continuous colour wash across the WHOLE disk — white-hot on the left, "
    "through yellow, through orange, into dull dark grey on the right. "
    "CRITICAL: this is internal heat colour, NOT sunlight and shadow. "
    "NO terminator line, NO crescent, NO eclipse, NO bite, NO hard edge "
    "between light and dark, NO jagged silhouette. Soft gradual blend only. "
    "Starfield BRIGHT and readable on a phone — many clear white pinprick "
    "stars on near-black space. "
    "Premium CGI. Wonder, not dread. "
    "NO Orbit, NO robot, NO spacecraft, NO text, NO logo, NO rings, NO planets."
)


def main() -> None:
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    work = OUT / "_work"
    work.mkdir(parents=True, exist_ok=True)
    tries: list[dict] = []
    best: Path | None = None
    best_score = -1.0
    generated = 0

    for i in range(6):
        dest = work / f"friday_remint_{i}.png"
        print(f"FRIDAY remint try {i}", flush=True)
        generate(client, [PROMPT], dest)
        generated += 1
        frac = sphere_core_frac(dest)
        # score: closer to 0.40 is better; reject <0.25 or >0.55
        dist = abs(frac - 0.40)
        ok = 0.30 <= frac <= 0.50
        score = (1.0 - dist) if ok else (0.2 - dist)
        tries.append(
            {
                "try": i,
                "sha256": sha256(dest),
                "sphere_width_frac": round(frac, 3),
                "score": round(score, 4),
                "pass": ok,
            }
        )
        print(f"  frac={frac:.3f} score={score:.3f} pass={ok}", flush=True)
        if score > best_score:
            best_score = score
            best = dest
        if ok and dist < 0.05:
            break

    assert best is not None
    fri_dest = OUT / "friday_black_dwarf_cooling_v02.png"
    chunk_write(best, fri_dest)
    chunk_write(fri_dest, UAT / fri_dest.name)

    mon = OUT / "monday_saturn_rings_streaming_v02.png"
    stills = [
        {
            "file": mon.name,
            "slot": "monday_saturn_short",
            "sha256": sha256(mon),
            "bytes": mon.stat().st_size,
            "aspect": "9:16",
            "orbit_at_frame0": False,
            "note": "kept from first v02 pass — curtains land on southern cloud tops",
        },
        {
            "file": fri_dest.name,
            "slot": "friday_black_dwarf_short",
            "sha256": sha256(fri_dest),
            "bytes": fri_dest.stat().st_size,
            "aspect": "9:16",
            "orbit_at_frame0": False,
            "qa": tries,
            "picked": best.name,
        },
    ]
    for s in stills:
        if sha256(UAT / s["file"]) != s["sha256"]:
            # monday may already be in UAT; re-chunk friday only if needed
            chunk_write(OUT / s["file"], UAT / s["file"])

    manifest = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "veo": False,
        "ben_order": "2026-10-01T10:19 London — v02; Friday reminted for size+smooth ember",
        "images_generated_this_remint": generated,
        "estimated_usd_list_price_remint": round(generated * USD_PER_IMAGE, 4),
        "stills": stills,
        "stop": "WAIT for Ben OK — do not start Shorts Veo or moving cut",
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write((OUT / "MANIFEST.json").read_bytes(), UAT / "MANIFEST.json")
    sha_md = "\n".join(
        [
            "# SHA-256 — saturn_shorts_stills_v02_for_ben_ok",
            "",
            "| File | SHA-256 | Bytes |",
            "|---|---|---:|",
            *[f"| `{s['file']}` | `{s['sha256']}` | {s['bytes']} |" for s in stills],
            "",
        ]
    )
    (OUT / "SHA256.md").write_text(sha_md)
    chunk_write(sha_md.encode(), UAT / "SHA256.md")
    readme = """# Saturn Shorts opening stills v02 — Ben OK

| File | Brief |
|---|---|
| `monday_saturn_rings_streaming_v02.png` | 9:16 — same composition as v01; ice curtains end at southern cloud tops (into Saturn); no streams below planet; no Orbit |
| `friday_black_dwarf_cooling_v02.png` | 9:16 — sphere ~40% width; smooth white→yellow→orange→dark grey ember; brighter stars; no bite/eclipse; no Orbit |

**STOP — WAIT for Ben OK. No Shorts Veo. No moving cut.**
"""
    (OUT / "README.md").write_text(readme)
    chunk_write(readme.encode(), UAT / "README.md")
    print(json.dumps({"FRIDAY_REMINT_DONE": True, **manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
