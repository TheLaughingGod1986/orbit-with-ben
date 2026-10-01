#!/usr/bin/env python3
"""Saturn week Short opening stills v02 — 9:16 for Ben OK. Vertex only. No Veo.

Ben 1 Oct 10:19 London (supersedes earlier 10:19 re-roll brief):
  MONDAY: keep exact composition + ice curtains from
    monday_saturn_rings_streaming_v01.png. Change ONE thing: every curtain
    ends at Saturn's cloud tops in the southern half, fading into the
    atmosphere where it lands. Nothing continues below the planet into
    empty space. The ice falls INTO Saturn.
  FRIDAY: sphere ~40% of frame width. Smooth colour gradient white-hot →
    yellow → orange → dull dark grey (cooling ember). No bite, no hard
    edge, no eclipse. Starfield brighter. No Orbit.

Pack: OWB UAT/saturn_shorts_stills_v02_for_ben_ok/
STOP — wait for Ben OK before any Shorts Veo / moving cut.
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
V01 = EP / "04_Generated-Clips" / "shorts_stills_v01"
OUT = EP / "04_Generated-Clips" / "shorts_stills_v02"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_shorts_stills_v02_for_ben_ok"
)
MON_V01 = V01 / "monday_saturn_rings_streaming_v01.png"
FRI_V01 = V01 / "friday_black_dwarf_cooling_v01.png"

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
    parts = response.candidates[0].content.parts or []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            dest.write_bytes(data)
            return len(data)
    raise RuntimeError(
        f"No image bytes finish={getattr(response.candidates[0], 'finish_reason', None)}"
    )


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
            if dest.stat().st_size >= 10_000:
                im = Image.open(dest)
                w, h = im.size
                if h > w:
                    return n
                print(f"  warn not portrait {w}x{h}, retry", flush=True)
        except Exception as e:
            last_err = e
            print(f"  retry {attempt + 1}: {e}", flush=True)
            time.sleep(8 * (attempt + 1))
    raise RuntimeError(f"FAILED {dest}: {last_err}")


def score_monday_below_planet(path: Path) -> dict:
    """Bright curtain pixels in empty space BELOW Saturn's southern limb = FAIL.

    Saturn in v01 sits roughly in the upper ~65% of frame; the void under the
    planet is y > ~0.72. Curtains that continue into that void are the bug.
    """
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # Band under the planet (bottom ~28% of frame), centre where curtains fall
    y0 = int(h * 0.72)
    x0, x1 = int(w * 0.18), int(w * 0.82)
    bright = 0
    total = 0
    for y in range(y0, h, 2):
        for x in range(x0, x1, 2):
            r, g, b = img.getpixel((x, y))
            # pale ice curtains are bright + cool/neutral
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            total += 1
            if luma > 55:
                bright += 1
    ratio = bright / max(total, 1)
    return {
        "below_planet_bright_ratio": round(ratio, 5),
        "below_planet_bright": bright,
        "below_planet_total": total,
        "pass": ratio < 0.012,
    }


def score_friday_sphere(path: Path) -> dict:
    """Sphere should be ~40% of frame width; reject tiny dots."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # find bright/coloured non-black pixels near centre
    xs: list[int] = []
    for y in range(int(h * 0.25), int(h * 0.75), 2):
        for x in range(int(w * 0.15), int(w * 0.85), 2):
            r, g, b = img.getpixel((x, y))
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            if luma > 40:
                xs.append(x)
    if not xs:
        return {"sphere_width_frac": 0.0, "pass": False, "reason": "no_sphere"}
    span = (max(xs) - min(xs)) / w
    # accept 0.28–0.55 (target ~0.40)
    return {
        "sphere_width_frac": round(span, 3),
        "pass": 0.28 <= span <= 0.55,
    }


def main() -> None:
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    if not MON_V01.is_file():
        raise SystemExit(f"missing base still {MON_V01}")

    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)
    work = OUT / "_work"
    work.mkdir(exist_ok=True)

    generated = 0
    stills: list[dict] = []
    tries_log: list[dict] = []

    # --- Monday: EDIT v01 — keep composition; curtains land on Saturn ---
    mon_prompt = (
        "IMAGE EDIT of the attached vertical 9:16 Saturn Short opening still. "
        "KEEP this EXACT composition: Saturn position and size, rings cutting "
        "diagonally across the frame, the same ice curtains falling from the "
        "underside of the rings, camera angle, lighting, colour, starfield. "
        "CHANGE ONLY ONE THING: every ice curtain must END at Saturn's cloud "
        "tops in the southern half of the planet, fading softly into the "
        "butterscotch atmosphere where it lands. The ice falls INTO Saturn. "
        "Nothing continues below the planet into empty black space — the void "
        "under Saturn's southern limb must be clean near-black with no falling "
        "ice streams, no curtains, no grain trails. "
        "Do NOT redesign the shot. Do NOT move Saturn. Do NOT remove the "
        "curtains above the southern hemisphere. Do NOT add Orbit, robots, "
        "spacecraft, text, logos, or Earth. Premium CGI still, 9:16."
    )
    mon_dest = OUT / "monday_saturn_rings_streaming_v02.png"
    best_mon: Path | None = None
    best_mon_score: dict | None = None
    for try_i in range(4):
        try_path = work / f"monday_try_{try_i}.png"
        print(f"MONDAY edit try {try_i}", flush=True)
        contents = [
            "Base image to edit (keep this composition):",
            types.Part.from_bytes(data=MON_V01.read_bytes(), mime_type="image/png"),
            mon_prompt,
        ]
        generate(client, contents, try_path)
        generated += 1
        sc = score_monday_below_planet(try_path)
        tries_log.append({"slot": "monday", "try": try_i, "sha256": sha256(try_path), **sc})
        print(f"  score {sc}", flush=True)
        if best_mon_score is None or sc["below_planet_bright_ratio"] < best_mon_score[
            "below_planet_bright_ratio"
        ]:
            best_mon = try_path
            best_mon_score = sc
        if sc["pass"]:
            break
    assert best_mon is not None and best_mon_score is not None
    chunk_write(best_mon, mon_dest)
    chunk_write(mon_dest, UAT / mon_dest.name)
    stills.append(
        {
            "file": mon_dest.name,
            "slot": "monday_saturn_short",
            "sha256": sha256(mon_dest),
            "bytes": mon_dest.stat().st_size,
            "aspect": "9:16",
            "orbit_at_frame0": False,
            "base": MON_V01.name,
            "qa": best_mon_score,
        }
    )

    # --- Friday: larger sphere, smooth cooling gradient, brighter stars ---
    fri_prompt = (
        "Vertical 9:16 cinematic CGI still for a YouTube Short OPENING FRAME. "
        "A cooling white dwarf becoming a black dwarf: ONE sphere about 40% of "
        "the frame width (much larger than a tiny distant star), centred. "
        "SMOOTH colour gradient across the sphere like a cooling ember: "
        "white-hot on one side, through yellow and orange, into dull dark grey "
        "on the other side. NO bite, NO hard terminator edge, NO eclipse look, "
        "NO jagged silhouette — the fade must be continuous and soft. "
        "Starfield visibly BRIGHT enough to read on a phone — many clear "
        "pinprick stars on near-black space (not a nearly empty void). "
        "Premium CGI. Wonder, not dread. "
        "NO Orbit, NO robot, NO spacecraft, NO text, NO logo, NO planet rings. "
        "Strange picture only — frame 0 of a Short."
    )
    fri_dest = OUT / "friday_black_dwarf_cooling_v02.png"
    best_fri: Path | None = None
    best_fri_score: dict | None = None
    for try_i in range(4):
        try_path = work / f"friday_try_{try_i}.png"
        print(f"FRIDAY gen try {try_i}", flush=True)
        contents_f: list = [fri_prompt]
        if FRI_V01.is_file() and try_i == 0:
            # first try: edit v01 toward the new brief (same subject, fix bite/size)
            contents_f = [
                "Reference (same subject — enlarge sphere, replace bite with smooth ember gradient, brighten stars):",
                types.Part.from_bytes(data=FRI_V01.read_bytes(), mime_type="image/png"),
                fri_prompt
                + " Edit the attached still: make the sphere ~40% frame width; "
                "replace the hard dark bite/eclipse edge with a smooth white-hot "
                "→ yellow → orange → dull dark grey gradient; brighten the starfield.",
            ]
        generate(client, contents_f, try_path)
        generated += 1
        sc = score_friday_sphere(try_path)
        tries_log.append({"slot": "friday", "try": try_i, "sha256": sha256(try_path), **sc})
        print(f"  score {sc}", flush=True)
        if best_fri_score is None or (
            sc.get("sphere_width_frac", 0) > best_fri_score.get("sphere_width_frac", 0)
            and sc.get("sphere_width_frac", 0) <= 0.55
        ):
            best_fri = try_path
            best_fri_score = sc
        if sc["pass"]:
            best_fri = try_path
            best_fri_score = sc
            break
    assert best_fri is not None and best_fri_score is not None
    chunk_write(best_fri, fri_dest)
    chunk_write(fri_dest, UAT / fri_dest.name)
    stills.append(
        {
            "file": fri_dest.name,
            "slot": "friday_black_dwarf_short",
            "sha256": sha256(fri_dest),
            "bytes": fri_dest.stat().st_size,
            "aspect": "9:16",
            "orbit_at_frame0": False,
            "qa": best_fri_score,
        }
    )

    for s in stills:
        u = UAT / s["file"]
        if sha256(u) != s["sha256"]:
            raise SystemExit(f"UAT sha mismatch {s['file']}")

    manifest = {
        "engine": "vertex",
        "project": PROJECT,
        "location": LOCATION,
        "model": MODEL,
        "ai_studio_prepay": False,
        "veo": False,
        "ben_order": (
            "2026-10-01T10:19 London — v02 re-roll: Mon curtains land on Saturn "
            "(edit v01 composition); Fri larger sphere + smooth ember gradient + brighter stars"
        ),
        "images_generated": generated,
        "estimated_usd_list_price": round(generated * USD_PER_IMAGE, 4),
        "billing_note": (
            f"Vertex Free Trial {PROJECT}; ${USD_PER_IMAGE}/image × {generated}. "
            "No Veo on Shorts until Ben OK."
        ),
        "stills": stills,
        "tries": tries_log,
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
    print(json.dumps({"SHORTS_STILLS_V02_DONE": True, **manifest}, indent=2), flush=True)


if __name__ == "__main__":
    main()
