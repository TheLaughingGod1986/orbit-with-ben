#!/usr/bin/env python3
"""Standalone Shorts S1-S4: the ~1 s Orbit beat (J0200, Chief #99 6125827198 item 4), the ORBIT ACTS line of
SCRIPTS_v01.md for each.

  start : a 9:16 crop of a NASA plate from ASSEMBLY_STATUS.md (never a whole planet), with Orbit cut from the
          canonical ORBIT_REF (rembg u2net matte + hand masks, as 030), scaled only, plus the orbit_source sidecar
          so orbit_gemini_omni's guard runs.
  omni  : one Omni take each at location `global`, 9:16. One take, no retry loop; a miss keeps the opening plate
          under the Orbit slot.

Vertex only (promo credit pool), never AI Studio prepaid. Outputs to /private/tmp/owb_sa_shorts/orbit/ (media,
not in git). Run with ~/.venvs/orbit-omni/bin/python:
  python _mint_sa_orbit_s1-s4_v01.py start|omni [s1 s2 ...]
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
PLATES = Path("/private/tmp/owb_sa_shorts/plates")
OUT = Path("/private/tmp/owb_sa_shorts/orbit")
STARTS = OUT / "starts"
REPORT = HERE / "orbit_gen_report_s1-s4_v01.json"
PROJECT = "gen-lang-client-0538779324"
ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
W, H = 720, 1280
sys.path.insert(0, str(REPO / "04_Audio/tools"))
import orbit_gemini_omni  # noqa: E402
from orbit_gemini_omni import generate_omni_clip, write_orbit_source_sidecar  # noqa: E402

ORBIT_LOCK = (
    " IDENTITY LOCK: Exactly one solid matte orange floating robot (Orbit), one large black curved visor as the "
    "whole face, two cream circular eyes with dark pupils, stubby orange arms with dark three-finger hands, one "
    "antenna with glowing bulb, one soft underside glow, NO LEGS. Not a toy, not a second face, not a second "
    "Orbit, no HUD, no text, no logo."
)

# crop: (cx, cy, h) as fractions of the plate; the 9:16 box is h tall and centred on (cx, cy).
# orbit: (x, y, px) on the 720x1280 start frame.
SHOTS = {
    "s1": {
        "id": "orbit_sa_s1_mercury_omni_v01", "plate": "s1_mercury/PIA11351.jpg",
        "crop": (0.62, 0.50, 1.0), "orbit": (0.50, 0.40, 220),
        "scene": "Mercury cratered horizon in hard light (MESSENGER PIA11351, part limb, no whole planet); "
                 "Orbit ~220px above the rock",
        "prompt": (
            "A grey cratered horizon under a black sky, exactly as in the start frame, in bright sunlight with long "
            "shadows. Orbit floats gently down and settles on the rocky ridge, looks up towards the bright light "
            "off frame, taps his wrist with one hand as if checking the time, waits, then sinks a little lower. "
            "The camera barely drifts."
            + ORBIT_LOCK + " Silent picture only."
        ),
    },
    "s2": {
        "id": "orbit_sa_s2_neptune_omni_v01", "plate": "s2_neptune/PIA00058.jpg",
        "crop": (0.40, 0.50, 1.0), "orbit": (0.42, 0.52, 220),
        "scene": "Neptune's white cloud streaks over deep blue (Voyager 2 PIA00058, close cloud view, no limb disc); "
                 "Orbit ~220px mid-frame",
        "prompt": (
            "Deep blue Neptune cloud tops with long bright white cloud streaks, exactly as in the start frame. "
            "No globe, no whole planet. A violent supersonic wind hits: the white streaks race past and Orbit is "
            "blown sideways across the frame, tumbling slightly, gripping his antenna with one hand to hold on, "
            "his visor eyes wide. The camera shakes very slightly with the wind."
            + ORBIT_LOCK + " Silent picture only."
        ),
    },
    "s3": {
        "id": "orbit_sa_s3_iss_omni_v01", "plate": "s3_iss/iss054e002538.jpg",
        "crop": (0.30, 0.50, 1.0), "orbit": (0.62, 0.58, 220),
        "scene": "ISS robotic arm and truss against Earth's thin blue limb and black space (iss054e002538); "
                 "Orbit ~220px holding on beside the truss",
        "prompt": (
            "White spacecraft modules and a robotic arm against black space above a thin blue horizon line, exactly "
            "as in the start frame. Orbit holds on to the white module with one hand as warm golden sunrise light "
            "spreads slowly across the scene from the horizon. Orbit lifts his other hand above his visor, then "
            "his eyes curve into a happy smile. The camera barely drifts."
            + ORBIT_LOCK + " Silent picture only."
        ),
    },
    "s4": {
        "id": "orbit_sa_s4_uranus_omni_v01", "plate": "s4_uranus/PIA01391.jpg",
        "crop": (0.42, 0.62, 0.70), "orbit": (0.66, 0.42, 220),
        "scene": "Part of Uranus's thin pale crescent edge and its dark night side (Voyager 2 PIA01391, tight crop, "
                 "no whole planet); Orbit ~220px over the dark side",
        "prompt": (
            "A thin pale blue-green crescent edge curving through a dark frame, exactly as in the start frame. Orbit "
            "floats over the dark side; a light white frost slowly forms on his orange shell and his underside glow "
            "softens. He turns and looks over his shoulder at a tiny faraway point of light in the black sky. The "
            "camera barely drifts."
            + ORBIT_LOCK + " Silent picture only."
        ),
    },
}


def client(location: str):
    from google import genai

    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        os.environ.pop(k, None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    return genai.Client(vertexai=True, project=PROJECT, location=location)


def spend(stem: str) -> None:
    subprocess.run([sys.executable, str(REPO / "scripts/ai_spend.py"), "spend", "--pool", "vertex", "--amount", "0",
                    "--film", "OWB:SA", "--what", f"J0200 Omni clip {stem} (gemini-omni-flash-preview; unpriced, billed late)",
                    "--by", (os.environ.get("OWB_AGENT") or "cursor").lower()], cwd=REPO)


def report_update(key: str, entry: dict) -> None:
    rep = json.loads(REPORT.read_text()) if REPORT.exists() else {
        "request": "J0200 (Chief #99 6125827198 item 4): one take each", "project": PROJECT, "location": "global",
        "model": "gemini-omni-flash-preview", "out_dir": str(OUT)}
    rep[key] = entry
    REPORT.write_text(json.dumps(rep, indent=2) + "\n")


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


def crop916(path: Path, cx: float, cy: float, hf: float) -> tuple[Image.Image, float]:
    im = Image.open(path).convert("RGB")
    h = hf * im.height
    w = h * W / H
    l = min(max(cx * im.width - w / 2, 0), im.width - w)
    t = min(max(cy * im.height - h / 2, 0), im.height - h)
    box = im.crop((round(l), round(t), round(l + w), round(t + h)))
    return box.resize((W, H), Image.LANCZOS), W / w


def do_start(keys: list[str]) -> None:
    STARTS.mkdir(parents=True, exist_ok=True)
    cache: dict[int, Image.Image] = {}
    for k in keys:
        s = SHOTS[k]
        bg, up = crop916(PLATES / s["plate"], *s["crop"])
        x, y, px = s["orbit"]
        orb = cache.setdefault(px, orbit_rgba(px))
        c = bg.convert("RGBA")
        c.alpha_composite(orb, (int(W * x) - orb.width // 2, int(H * y) - orb.height // 2))
        out = STARTS / f"{s['id'].replace('_omni_', '_start_')}.png"
        c.convert("RGB").save(out)
        write_orbit_source_sidecar(
            out, shot=f"standalone {k.upper()} ~1 s", scene=s["scene"],
            method=f"Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over a 9:16 crop of "
                   f"{s['plate']} (upscale {up:.2f}x)",
            script=str(Path(__file__).resolve().relative_to(REPO)),
            composited=datetime.now(timezone.utc).date().isoformat(), request="J0200 (Chief #99 6125827198)")
        print(f"ok {out} (plate upscale {up:.2f}x)")


def do_omni(keys: list[str]) -> int:
    orbit_gemini_omni._record_spend = lambda dest, model: None  # logged below with --film OWB:SA
    bad = 0
    for k in keys:
        s = SHOTS[k]
        take = OUT / f"{s['id']}.mp4"
        start = STARTS / f"{s['id'].replace('_omni_', '_start_')}.png"
        if take.exists():
            print("skip: take exists; no second take without Chief", take)
            continue
        t0 = time.time()
        try:
            meta = generate_omni_clip(client("global"), s["prompt"], take, orbit_ref=start, orbit_shot=True,
                                      aspect_ratio="9:16")
            spend(take.stem)
            sh = OUT / f"{take.stem}_6frame.jpg"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(take), "-vf",
                            "fps=0.75,scale=200:-2,tile=6x1", "-frames:v", "1", str(sh)], check=True)
            meta.update(status="ok", wall_seconds=round(time.time() - t0, 1), sheet=sh.name, start=start.name,
                        plate=s["plate"], prompt=s["prompt"],
                        sha256=subprocess.check_output(["shasum", "-a", "256", str(take)], text=True).split()[0])
        except BaseException as e:  # noqa: BLE001 — no retry, record and move on
            bad += 1
            meta = {"status": "fail", "error": f"{type(e).__name__}: {e}", "start": start.name, "prompt": s["prompt"]}
            if any(x in str(e).lower() for x in ("prepayment", "billing", "402", "resource_exhausted", "quota")):
                report_update(k, meta)
                print("STOP: billing/quota", e)
                return 2
        report_update(k, meta)
        print(k, json.dumps({x: meta.get(x) for x in ("status", "seconds", "bytes", "error")}))
    return 1 if bad else 0


if __name__ == "__main__":
    keys = [a for a in sys.argv[2:] if a in SHOTS] or list(SHOTS)
    if sys.argv[1] == "start":
        do_start(keys)
    else:
        sys.exit(do_omni(keys))
