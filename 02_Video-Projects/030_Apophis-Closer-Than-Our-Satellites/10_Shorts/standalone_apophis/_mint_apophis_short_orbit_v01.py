#!/usr/bin/env python3
"""030 Apophis standalone Short: the ~1 s Orbit beat (J0223, SCRIPT_v01: "Orbit drifts beside a geostationary
satellite as the rock's shadow slides over it", ORBIT ACTS: looks up, ducks, then peers after it).

  still : one Vertex gemini-2.5-flash-image plate, a geostationary satellite on a star field (no text, no planet).
          NASA's library only has dated 1990s artist concepts of TDRS/GOES, so the image rule falls to Vertex.
  start : Orbit cut from the canonical ORBIT_REF (rembg u2net matte + hand masks, as 026), scaled only, over the
          plate, with the orbit_source sidecar so orbit_gemini_omni's guard runs.
  omni  : one Omni take at location `global`, 9:16. One take, no retry loop; a miss keeps the fallback
          (the opening rock plate runs under the Orbit slot).

Vertex only, never AI Studio prepaid. Run with ~/.venvs/orbit-omni/bin/python (genai, rembg, numpy, pillow):
  python _mint_apophis_short_orbit_v01.py still|start|omni
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = HERE / "04_Generated-Clips/omni_v01"
STARTS = OUT / "starts"
PLATE = STARTS / "geo_satellite_plate_v01.png"
START = STARTS / "orbit_geo_sat_start_v01.png"
TAKE = OUT / "orbit_geo_sat_omni_v01.mp4"
REPORT = HERE / "orbit_gen_report_v01.json"
PROJECT = "gen-lang-client-0538779324"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
W, H = 720, 1280
sys.path.insert(0, str(REPO / "04_Audio/tools"))
from orbit_gemini_omni import generate_omni_clip, write_orbit_source_sidecar  # noqa: E402

PLATE_PROMPT = (
    "Photoreal space photograph, vertical 9:16. A modern geostationary communications satellite in deep space: "
    "a compact gold-foil box body with two long dark-blue solar panel wings stretched out horizontally and one "
    "white dish antenna, in the upper half of the frame, lit by hard white sunlight from the left. "
    "Black sky with faint scattered stars. Nothing else in frame: no planet, no Earth, no Moon, no horizon, "
    "no people, no robot, no text, no logos, no flags, no lettering anywhere."
)

ORBIT_LOCK = (
    " IDENTITY LOCK: Exactly one solid matte orange floating robot (Orbit), one large black curved visor as the "
    "whole face, two cream circular eyes with dark pupils, stubby orange arms with dark three-finger hands, one "
    "antenna with glowing bulb, one soft underside glow, NO LEGS. Not a toy, not a second face, not a second "
    "Orbit, no HUD, no text, no logo."
)

OMNI_PROMPT = (
    "Deep space, exactly as in the start frame: the gold satellite with its long blue solar wings across the middle, "
    "black sky with faint stars. No planet, no globe, no ground. Orbit hovers just below and to the right of the satellite. "
    "A huge dark shadow sweeps quickly across the frame from right to left, dimming the satellite and Orbit as "
    "something enormous passes just out of view above. Orbit looks up, ducks down in surprise, then turns his "
    "visor and peers after it as the light returns. The satellite stays still; the camera barely drifts."
    + ORBIT_LOCK + " Silent picture only."
)


def client(location: str):
    from google import genai

    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        os.environ.pop(k, None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    return genai.Client(vertexai=True, project=PROJECT, location=location)


def spend(amount: float, what: str) -> None:
    subprocess.run([sys.executable, str(REPO / "scripts/ai_spend.py"), "spend", "--pool", "vertex", "--amount",
                    str(amount), "--film", "OWB:030", "--what", what,
                    "--by", (os.environ.get("OWB_AGENT") or "cursor").lower()], cwd=REPO)


def report_update(key: str, entry: dict) -> None:
    rep = json.loads(REPORT.read_text()) if REPORT.exists() else {"request": "J0223 (Chief): one take each"}
    rep[key] = entry
    REPORT.write_text(json.dumps(rep, indent=2) + "\n")


def do_still() -> None:
    from google.genai import types

    if PLATE.exists():
        print("skip: plate exists", PLATE)
        return
    c = client("us-central1")
    r = c.models.generate_content(
        model="gemini-2.5-flash-image", contents=PLATE_PROMPT,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                           image_config=types.ImageConfig(aspect_ratio="9:16")))
    data = None
    for part in r.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            data = part.inline_data.data
    if not data:
        raise SystemExit("no image returned")
    STARTS.mkdir(parents=True, exist_ok=True)
    PLATE.write_bytes(data)
    spend(0.03, "J0223 geo satellite plate, 1 x gemini-2.5-flash-image")
    report_update("still", {"status": "ok", "file": PLATE.name, "model": "gemini-2.5-flash-image",
                            "prompt": PLATE_PROMPT, "size": Image.open(PLATE).size})
    print("ok", PLATE)


def orbit_rgba(px: int) -> Image.Image:
    from rembg import new_session, remove

    ref = Image.open(ORBIT_REF).convert("RGB")
    a = np.array(remove(ref, session=new_session("u2net")).split()[3]).astype(np.float32)
    m = Image.new("L", ref.size, 0)
    d = ImageDraw.Draw(m)
    d.ellipse((297, 111, 332, 146), fill=255)
    d.line([(312, 143), (310, 158), (308, 172), (306, 188), (305, 206)], fill=255, width=8)
    d.ellipse((262, 546, 390, 584), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    alpha = np.maximum(a, np.array(m).astype(np.float32))
    al = Image.fromarray(alpha.clip(0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(
        ImageFilter.GaussianBlur(0.8))
    o = ref.convert("RGBA")
    o.putalpha(al)
    o = o.crop(o.getbbox())
    return o.resize((round(o.width * px / o.height), px), Image.LANCZOS)


def do_start() -> None:
    bg = Image.open(PLATE).convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
    l, t = (bg.width - W) // 2, (bg.height - H) // 2
    c = bg.crop((l, t, l + W, t + H)).convert("RGBA")
    orb = orbit_rgba(220)
    c.alpha_composite(orb, (int(W * 0.62) - orb.width // 2, int(H * 0.80) - orb.height // 2))
    c.convert("RGB").save(START)
    write_orbit_source_sidecar(
        START, shot="030 Short ~1 s", scene="Geostationary satellite upper left on stars; Orbit ~220px lower right, clear of the satellite; no planet",
        method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over {PLATE.name} (Vertex flash-image)",
        script=str(Path(__file__).resolve().relative_to(REPO)), composited=datetime.now(timezone.utc).date().isoformat(),
        request="J0223 (Chief)")
    print("ok", START)


def do_omni() -> None:
    if TAKE.exists():
        print("skip: take exists; no second take without Chief", TAKE)
        return
    t0 = time.time()
    try:
        meta = generate_omni_clip(client("global"), OMNI_PROMPT, TAKE, orbit_ref=START, orbit_shot=True,
                                  aspect_ratio="9:16")
        sh = OUT / f"{TAKE.stem}_6frame.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(TAKE), "-vf", "fps=0.75,scale=200:-2,tile=6x1",
                        "-frames:v", "1", str(sh)], check=True)
        meta.update(status="ok", wall_seconds=round(time.time() - t0, 1), sheet=sh.name, prompt=OMNI_PROMPT,
                    sha256=subprocess.check_output(["shasum", "-a", "256", str(TAKE)], text=True).split()[0])
    except BaseException as e:  # noqa: BLE001 — no retry, record and move on
        meta = {"status": "fail", "error": f"{type(e).__name__}: {e}", "prompt": OMNI_PROMPT}
    report_update("omni", meta)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    {"still": do_still, "start": do_start, "omni": do_omni}[sys.argv[1]]()
