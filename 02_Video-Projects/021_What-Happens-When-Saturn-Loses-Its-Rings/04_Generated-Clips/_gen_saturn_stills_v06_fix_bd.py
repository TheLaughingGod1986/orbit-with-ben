#!/usr/bin/env python3
"""Saturn stills v06 — fix B open + D bare (CoS FAIL on v05). Vertex only. No Veo.

B OPENING: start from saturn_open_rings_v03.png
  1) mirror WHOLE image horizontally (PIL)
  2) Vertex IMAGE EDIT — inpaint/remove ALL vertical streaks into clean black space
     (NOT a rectangle fill / NOT a hard mask)
  3) outpaint right so more of Saturn shows
  Keep: fine-banded blade, Saturn RIGHT, rings from LEFT, no Orbit, no streaks
  SHIPPED: open_try_0 (sha ac085c94…) — no hard-rect; continuous blade.
  Local OpenCV rectangle/spacefill attempts rejected (cut rings or worse streaks).

D BARE: keep v04 size (~60% frame height) and colour; oblate (~10% wider);
  soft gradual shadowed crescent (not hard cut); Orbit 8–12% frame height,
  seen from BEHIND, turned toward bare equator.
  SHIPPED: bare_try_1 (sha 2fe7676a…).

Pack only B+D into OWB UAT/saturn_stills_v06_for_ben_ok/ (C ice stays v05).
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
OUT = EP / "04_Generated-Clips" / "stills_v06"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_stills_v06_for_ben_ok"
)
ORBIT_REF = (
    REPO
    / "01_Orbit-Character"
    / "05_Seedance-References"
    / "orbit-seedance-reference-16x9-v01.png"
)
OPEN_V03 = STILLS_V03 / "saturn_open_rings_v03.png"
BARE_V04 = STILLS_V04 / "saturn_bare_orbit_v04.png"

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
    chunk = 500 * 1024
    with open(tmp, "wb") as o:
        for i in range(0, len(data), chunk):
            o.write(data[i : i + chunk])
            o.flush()
    tmp.replace(dest)
    if dest.stat().st_size != len(data):
        raise RuntimeError(f"size mismatch {dest}")


def save_response(response, dest: Path) -> int:
    if not response.candidates:
        raise RuntimeError("No candidates")
    parts = response.candidates[0].content.parts or []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    raise RuntimeError(
        f"No image bytes finish={getattr(response.candidates[0], 'finish_reason', None)}"
    )


def generate_edit(client: genai.Client, contents: list, dest: Path) -> int:
    last_err: Exception | None = None
    for attempt in range(5):
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


def metric_under_ring_streaks(path: Path) -> dict:
    """Rough streak detector: bright thin pixels under mid-height left/center."""
    img = Image.open(path).convert("L")
    w, h = img.size
    # under-ring band (lower half), excluding far-right Saturn
    bright = 0
    total = 0
    for y in range(int(h * 0.52), int(h * 0.95)):
        for x in range(0, int(w * 0.62), 2):
            v = img.getpixel((x, y))
            total += 1
            if v > 28:
                bright += 1
    return {
        "bright_frac": bright / max(total, 1),
        "bright_count": bright,
        "mean_under": sum(
            img.getpixel((x, y))
            for y in range(int(h * 0.55), int(h * 0.92), 4)
            for x in range(0, int(w * 0.55), 4)
        )
        / max(1, (h // 4) * (w // 4) // 16),
    }


def metric_bare(path: Path) -> dict:
    """Planet height fraction + left/right limb brightness (crescent check)."""
    img = Image.open(path).convert("L")
    w, h = img.size
    # find vertical extent of bright planet near center-x
    cx = w // 2
    ys = [y for y in range(h) if img.getpixel((cx, y)) > 35]
    if not ys:
        # try a bit right of center
        cx = int(w * 0.55)
        ys = [y for y in range(h) if img.getpixel((cx, y)) > 35]
    if not ys:
        return {"planet_height_frac": 0.0, "left": 0, "right": 0}
    y0, y1 = min(ys), max(ys)
    ph = (y1 - y0 + 1) / h
    mid_y = (y0 + y1) // 2
    # sample left and right of planet at mid
    left_x = None
    right_x = None
    for x in range(w):
        if img.getpixel((x, mid_y)) > 35:
            left_x = x
            break
    for x in range(w - 1, -1, -1):
        if img.getpixel((x, mid_y)) > 35:
            right_x = x
            break
    left_v = img.getpixel((left_x + 20, mid_y)) if left_x is not None else 0
    # near right limb inward
    right_v = img.getpixel((right_x - 15, mid_y)) if right_x is not None else 0
    # width/height of planet bbox for oblate check
    xs = [x for x in range(w) if img.getpixel((x, mid_y)) > 35]
    pw = (max(xs) - min(xs) + 1) / w if xs else 0
    return {
        "planet_height_frac": ph,
        "planet_width_frac": pw,
        "oblate_ratio_w_over_h": (pw * w) / max(ph * h, 1),
        "left_bright": left_v,
        "right_bright": right_v,
        "crescent_delta": left_v - right_v,
    }


def metric_orbit_height(path: Path) -> float:
    """Orange blob height as fraction of frame."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    ys = []
    for y in range(h):
        for x in range(int(w * 0.45)):
            r, g, b = img.getpixel((x, y))
            if r > 150 and r > g + 35 and b < 140:
                ys.append(y)
    if not ys:
        return 0.0
    return (max(ys) - min(ys) + 1) / h


def main() -> None:
    for p in (OPEN_V03, BARE_V04, ORBIT_REF):
        if not p.is_file():
            raise SystemExit(f"missing {p}")

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
    rej = OUT / "_rejected"
    rej.mkdir(exist_ok=True)

    generated = 0

    # --- B: mirror then Vertex inpaint (no rect fill) ---
    mirrored = work / "open_v03_mirrored_only.png"
    Image.open(OPEN_V03).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT).save(mirrored)
    print(f"mirrored whole image -> {mirrored.name}", flush=True)

    open_dest = OUT / "saturn_open_rings_v06.png"
    open_prompt = (
        "IMAGE EDIT of the attached plate. The plate is ALREADY mirrored: "
        "Saturn is on the RIGHT, the fine-banded ring BLADE sweeps in from the LEFT "
        "and meets Saturn's equator. "
        "YOUR ONLY JOBS: "
        "1) INPAINT / REMOVE every vertical streak, rain line, falling particle trail "
        "under and across the rings. Replace those pixels with natural near-black space "
        "that matches the surrounding void. "
        "Do NOT paint a solid black rectangle. Do NOT cut the ring blade. "
        "Do NOT leave a hard mask edge. The rings must stay continuous and fine-banded. "
        "2) OUTPAINT / WIDEN the RIGHT edge so MORE of Saturn's disk is visible "
        "(about the right half of the frame), keeping the inner rings meeting the equator. "
        "KEEP the ring blade look EXACTLY (bright thin fine cream/white bands). "
        "No Orbit. No spacecraft. No text. No second planet. "
        "Premium cinematic CGI still, 16:9."
    )

    best_open = None
    best_score = 1e9
    for attempt in range(4):
        cand = work / f"open_try_{attempt}.png"
        print(f"OPEN Vertex edit try {attempt + 1}", flush=True)
        generate_edit(
            client,
            [
                types.Part.from_bytes(data=mirrored.read_bytes(), mime_type="image/png"),
                open_prompt
                + (
                    f" Attempt {attempt + 1}: be extra careful — zero streaks, "
                    "zero black rectangles, continuous blade."
                ),
            ],
            cand,
        )
        generated += 1
        m = metric_under_ring_streaks(cand)
        print(f"  metrics {m}", flush=True)
        # lower bright_frac is better; reject obvious black-rect (large uniform black block
        # is hard to detect; prefer low bright_frac)
        score = m["bright_frac"] * 1000 + m["mean_under"]
        if score < best_score:
            best_score = score
            best_open = cand
        # accept threshold
        if m["bright_frac"] < 0.015 and m["mean_under"] < 8:
            print("  ACCEPT open", flush=True)
            break
    else:
        print(f"  using best open score={best_score}", flush=True)

    assert best_open is not None
    chunk_write(best_open, open_dest)
    # archive losers
    for p in work.glob("open_try_*.png"):
        if p.resolve() != best_open.resolve():
            chunk_write(p, rej / p.name)

    # --- D: from v04 size/colour, soft crescent, Orbit behind readable ---
    bare_dest = OUT / "saturn_bare_orbit_v06.png"
    bare_prompt = (
        "EDIT the first attached image (current bare Saturn + Orbit). "
        "KEEP the planet SIZE — about 60 percent of the frame HEIGHT — and the same "
        "butterscotch/cream band COLOUR. "
        "Planet must be visibly OBLATE (about 10 percent wider than tall), NOT a perfect round ball. "
        "NO rings. "
        "LIGHTING FIX (hard): replace any hard/straight-cut right edge with a SOFT, GRADUAL "
        "shadowed crescent terminator on the right — smooth falloff into space, not a knife edge. "
        "Second image is Orbit identity. "
        "Orbit must be SMALL but READABLE — about 8 to 12 percent of the frame HEIGHT "
        "(NOT a speck, NOT huge). Place at the left edge. "
        "Seen from BEHIND / three-quarter rear: solid matte orange BACK + antenna stem with "
        "glowing tip visible; NO black visor facing the camera; NO eyes toward us. "
        "Orbit is turned toward the planet's bare equator (looking at Saturn), not at the camera. "
        "Not waving. Exactly one Orbit. "
        "Premium cinematic CGI still, 16:9, near-black space."
    )

    best_bare = None
    best_bare_score = -1e9
    for attempt in range(5):
        cand = work / f"bare_try_{attempt}.png"
        print(f"BARE Vertex edit try {attempt + 1}", flush=True)
        generate_edit(
            client,
            [
                types.Part.from_bytes(data=BARE_V04.read_bytes(), mime_type="image/png"),
                types.Part.from_bytes(data=ORBIT_REF.read_bytes(), mime_type="image/png"),
                bare_prompt
                + (
                    f" Attempt {attempt + 1}: enforce ~60% planet height, oblate, soft crescent, "
                    "Orbit 8–12% height from behind."
                ),
            ],
            cand,
        )
        generated += 1
        bm = metric_bare(cand)
        oh = metric_orbit_height(cand)
        print(f"  bare metrics {bm} orbit_h={oh:.3f}", flush=True)
        # score: planet height near 0.55–0.70, crescent_delta > 20, orbit 0.07–0.14, oblate > 1.05
        score = 0.0
        if 0.50 <= bm["planet_height_frac"] <= 0.75:
            score += 50
        else:
            score -= abs(bm["planet_height_frac"] - 0.60) * 100
        if bm["crescent_delta"] >= 20:
            score += 40
        else:
            score += bm["crescent_delta"]
        if 0.07 <= oh <= 0.15:
            score += 50
        else:
            score -= abs(oh - 0.10) * 200
        if bm["oblate_ratio_w_over_h"] >= 1.05:
            score += 20
        if score > best_bare_score:
            best_bare_score = score
            best_bare = cand
        if (
            0.50 <= bm["planet_height_frac"] <= 0.75
            and bm["crescent_delta"] >= 25
            and 0.075 <= oh <= 0.14
            and bm["oblate_ratio_w_over_h"] >= 1.04
        ):
            print("  ACCEPT bare", flush=True)
            break
    else:
        print(f"  using best bare score={best_bare_score}", flush=True)

    assert best_bare is not None
    chunk_write(best_bare, bare_dest)
    for p in work.glob("bare_try_*.png"):
        if p.resolve() != best_bare.resolve():
            chunk_write(p, rej / p.name)

    # UAT pack (B+D only)
    for old in list(UAT.glob("*")):
        if old.is_file():
            try:
                old.unlink()
            except OSError:
                pass
    for name in ("saturn_open_rings_v06.png", "saturn_bare_orbit_v06.png"):
        chunk_write(OUT / name, UAT / name)

    open_m = metric_under_ring_streaks(open_dest)
    bare_m = metric_bare(bare_dest)
    orbit_h = metric_orbit_height(bare_dest)

    manifest = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "veo": False,
        "ben_round": "3b-fix",
        "cos_notes": "v05 B+D FAIL; C ice OK kept as v05",
        "images_generated_this_pass": generated,
        "estimated_usd_list_price": round(generated * USD_PER_IMAGE, 4),
        "billing_note": (
            f"Vertex Free Trial {PROJECT}; list ${USD_PER_IMAGE}/image × {generated}."
        ),
        "stills": [
            {
                "file": "saturn_open_rings_v06.png",
                "sha256": sha256(open_dest),
                "bytes": open_dest.stat().st_size,
                "metrics": open_m,
                "method": "PIL mirror whole v03 + Vertex inpaint streaks + outpaint Saturn",
            },
            {
                "file": "saturn_bare_orbit_v06.png",
                "sha256": sha256(bare_dest),
                "bytes": bare_dest.stat().st_size,
                "metrics": {**bare_m, "orbit_height_frac": orbit_h},
                "method": "Vertex edit from bare_orbit_v04 + Orbit identity; soft crescent; Orbit behind",
            },
        ],
        "pack_order": ["saturn_open_rings_v06.png", "saturn_bare_orbit_v06.png"],
        "self_check": {
            "open": (
                f"under-ring bright_frac={open_m['bright_frac']:.4f} "
                f"mean={open_m['mean_under']:.2f} — must be near 0; no black rectangle; Saturn right"
            ),
            "bare": (
                f"planet_h={bare_m['planet_height_frac']:.2f} "
                f"oblate={bare_m['oblate_ratio_w_over_h']:.2f} "
                f"crescent_delta={bare_m['crescent_delta']} "
                f"orbit_h={orbit_h:.3f}"
            ),
        },
        "finishedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    chunk_write(OUT / "MANIFEST.json", UAT / "MANIFEST.json")

    sha_lines = [
        "# SHA-256 — saturn_stills_v06_for_ben_ok",
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

    readme = """# Saturn stills v06 — Ben OK (fix B + D)

CoS: v05 open + bare FAIL. Ice v05 OK (not in this folder).

| File | Brief |
|---|---|
| `saturn_open_rings_v06.png` | Mirror v03 → Vertex inpaint ALL streaks → outpaint Saturn RIGHT |
| `saturn_bare_orbit_v06.png` | v04 size/colour, oblate, soft crescent, Orbit 8–12% from behind |

**STOP — no Veo until Ben OK.**
"""
    (OUT / "README.md").write_text(readme)
    chunk_write(readme.encode(), UAT / "README.md")

    print(json.dumps({"STILLS_V06_DONE": True, **{k: manifest[k] for k in ("estimated_usd_list_price", "images_generated_this_pass", "self_check")}}, indent=2), flush=True)
    print("OPEN", sha256(open_dest))
    print("BARE", sha256(bare_dest))


if __name__ == "__main__":
    main()
