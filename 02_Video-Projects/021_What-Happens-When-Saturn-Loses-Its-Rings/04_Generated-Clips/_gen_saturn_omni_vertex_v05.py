#!/usr/bin/env python3
"""Saturn Omni via Vertex Free Trial ONLY — CoS run#7.

Never AI Studio / never GEMINI_API_KEY.
Retry up to 3 times with backoff for:
  1) omni_orbit_tumble_v05 — Ben 11:18: 4–5s slow roll, quick swipe (never hold),
     exactly two stubby arms / three-finger hands, canonical still attached
  2) omni_bare_orbit_v05 — small Orbit facing bare Saturn

Models to try: gemini-omni-flash-preview, gemini-omni-1.1-flash-preview
Report exact error + model ID if all fail.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from orbit_gemini_veo import strip_audio  # noqa: E402

from google import genai

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
CLIPS = EP / "04_Generated-Clips"
OUT = CLIPS / "veo_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_veo_v05_for_ben_ok"
)
CONTACT = OUT / "_contact"
WORK = OUT / "_work"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/cursor_agent_stores/bc-bb6a84a0-ea11-5101-b43f-34c5b13867e0/files/artifacts"
)

IDENTITY = (
    REPO / "01_Orbit-Character" / "05_Seedance-References" / "orbit-seedance-reference-16x9-v01.png"
)
TUMBLE_STILL = CLIPS / "stills_v04" / "saturn_orbit_tumble_v04.png"
BARE_STILL = CLIPS / "stills_v06" / "saturn_bare_orbit_v06.png"

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
MODELS = [
    "gemini-omni-flash-preview",
    "gemini-omni-1.1-flash-preview",
]

IDENTITY_LOCK = (
    " IDENTITY LOCK — match Image 1 (canonical Orbit) exactly: matte orange floater, "
    "one large black curved visor with two cream eyes + dark pupils, EXACTLY TWO stubby "
    "side arm pods with dark THREE-FINGER hands, one antenna with glowing tip, one soft "
    "underside glow, NO LEGS. Forbidden: extra forearms, multi-finger growth, humanoid arms, "
    "second face, legs, toy knockoff."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunk_write(src: Path | bytes, dest: Path, retries: int = 8) -> None:
    data = src if isinstance(src, (bytes, bytearray)) else Path(src).read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries):
        try:
            tmp = dest.with_suffix(dest.suffix + ".partial")
            with open(tmp, "wb") as o:
                for i in range(0, len(data), 500 * 1024):
                    o.write(data[i : i + 500 * 1024])
                    o.flush()
            tmp.replace(dest)
            time.sleep(0.2)
            if dest.stat().st_size == len(data):
                return
        except OSError as e:
            print(f"  chunk retry {attempt}: {e}", flush=True)
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"chunk_write failed {dest}")


def contact_sheet(mp4: Path, dest: Path) -> list[float]:
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(mp4)]
    )
    dur = float(json.loads(probe)["format"]["duration"])
    times = [0.05, dur / 3, 2 * dur / 3, max(0.05, dur - 0.08)]
    frames = []
    WORK.mkdir(parents=True, exist_ok=True)
    for i, t in enumerate(times):
        p = WORK / f"_cs_{mp4.stem}_{i}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(p)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        frames.append(Image.open(p).convert("RGB"))
    h = max(im.height for im in frames) // 2
    resized = [im.resize((int(im.width * h / im.height), h)) for im in frames]
    gap = 8
    w = sum(im.width for im in resized) + gap * (len(resized) - 1)
    sheet = Image.new("RGB", (w, h + 40), (12, 12, 16))
    draw = ImageDraw.Draw(sheet)
    x = 0
    for im, t in zip(resized, times):
        sheet.paste(im, (x, 32))
        draw.text((x + 4, 4), f"{t:.2f}s", fill=(220, 220, 230))
        x += im.width + gap
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    return times


def trim_to(mp4: Path, dest: Path, seconds: float) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "0",
            "-i",
            str(mp4),
            "-t",
            str(seconds),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(dest),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def extract_video_bytes(interaction) -> bytes:
    ov = getattr(interaction, "output_video", None)
    if ov is not None and getattr(ov, "data", None):
        data = ov.data
        return data if isinstance(data, (bytes, bytearray)) else base64.b64decode(data)
    steps = getattr(interaction, "steps", None) or []
    for step in steps:
        contents = getattr(step, "content", None) or (step.get("content") if isinstance(step, dict) else None) or []
        for item in contents:
            if isinstance(item, dict) and item.get("type") == "video" and item.get("data"):
                return base64.b64decode(item["data"])
            if getattr(item, "type", None) == "video" and getattr(item, "data", None):
                data = item.data
                return data if isinstance(data, (bytes, bytearray)) else base64.b64decode(data)
    # try URI
    if ov is not None and getattr(ov, "uri", None):
        raise RuntimeError(f"URI delivery not downloaded: {ov.uri}")
    raise RuntimeError(f"no video bytes in interaction: {type(interaction)} id={getattr(interaction,'id',None)}")


def section6_heuristic(mp4: Path) -> dict:
    times = contact_sheet(mp4, WORK / f"_tmp_{mp4.stem}.png")
    widths = []
    for i, _t in enumerate(times):
        p = WORK / f"_cs_{mp4.stem}_{i}.png"
        im = Image.open(p).convert("RGB")
        w, h = im.size
        xs = []
        for y in range(int(h * 0.2), int(h * 0.85), 3):
            for x in range(w):
                r, g, b = im.getpixel((x, y))
                if r > 140 and 60 < g < 180 and b < 120 and r > g + 30:
                    xs.append(x)
        widths.append(round(((max(xs) - min(xs)) / w) if xs else 0.0, 3))
    jump = max(widths) - min(widths) if widths else 0
    return {
        "orange_width_frac_by_frame": widths,
        "width_jump": round(jump, 3),
        "heuristic_warn": jump > 0.18,
    }


def generate_vertex_omni(client, model: str, prompt: str, composition: Path, dest: Path) -> dict:
    t0 = time.time()
    ident_b64 = base64.b64encode(IDENTITY.read_bytes()).decode("ascii")
    comp_b64 = base64.b64encode(composition.read_bytes()).decode("ascii")
    full = (
        "Image 1 is the CANONICAL Orbit identity still. Image 2 is the composition start frame. "
        "Animate Image 2 as image-to-video; Orbit must match Image 1. "
        + prompt
        + IDENTITY_LOCK
        + " Silent picture. No speech, no narration, no readable text, no logo."
    )
    print(f"  submit model={model} → {dest.name}", flush=True)
    interaction = client.interactions.create(
        model=model,
        input=[
            {"type": "image", "data": ident_b64, "mime_type": "image/png"},
            {"type": "image", "data": comp_b64, "mime_type": "image/png"},
            {"type": "text", "text": full},
        ],
        response_format={"type": "video", "aspect_ratio": "16:9"},
        generation_config={"video_config": {"task": "image_to_video"}},
    )
    raw = extract_video_bytes(interaction)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    if dest.stat().st_size < 100_000:
        raise RuntimeError(f"download too small: {dest.stat().st_size}")
    try:
        strip_audio(dest)
    except Exception as e:
        print(f"  strip_audio note: {e}", flush=True)
    return {
        "model": model,
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "interaction_id": getattr(interaction, "id", None),
        "engine": "vertex-omni",
        "project": PROJECT,
        "location": LOCATION,
    }


def try_with_retries(client, name: str, prompt: str, composition: Path, raw_dest: Path) -> dict:
    errors = []
    for attempt in range(1, 4):
        for model in MODELS:
            try:
                print(f"\n=== {name} attempt {attempt}/3 model={model} ===", flush=True)
                meta = generate_vertex_omni(client, model, prompt, composition, raw_dest)
                return {"status": "ok", "attempt": attempt, "meta": meta, "errors": errors}
            except Exception as e:
                err = {
                    "attempt": attempt,
                    "model": model,
                    "error_type": type(e).__name__,
                    "error": str(e),
                }
                errors.append(err)
                print(f"  FAIL {err}", flush=True)
                # backoff: 8s, 20s, 45s
                time.sleep({1: 8, 2: 20, 3: 45}[attempt])
    return {"status": "failed", "errors": errors}


TUMBLE_PROMPT = (
    "Exactly ONE Orbit tumbles with a SLOW ROLL while drifting through sparse ring ice "
    "for about 4–5 seconds of action. One quick swipe at a passing ice chunk with one hand — "
    "never holding or keeping the chunk. Ice floats past with black space between chunks. "
    "Saturn and rings stay in the background. Exactly two stubby arms with three-finger hands, "
    "no extra limbs."
)

BARE_PROMPT = (
    "Small orange Orbit (from behind / three-quarter) on the left facing bare Saturn (no rings) "
    "on the right. Slow gentle hover / tiny tip toward the planet. Keep Orbit small and on-model. "
    "Exactly two stubby arms with three-finger hands, no extra limbs. No rings, no text."
)


def main() -> None:
    # HARD: Vertex only — strip AI Studio keys
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    assert not os.environ.get("GEMINI_API_KEY")
    assert not os.environ.get("GOOGLE_API_KEY")

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)
    CONTACT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    report = {
        "engine": "vertex_free_trial_only",
        "project": PROJECT,
        "location": LOCATION,
        "models_tried": MODELS,
        "ai_studio_prepay": False,
        "identity": str(IDENTITY),
        "identity_sha256": sha256(IDENTITY),
        "clips": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    # --- Tumble ---
    tumble_raw = WORK / "omni_orbit_tumble_vertex_raw.mp4"
    tumble_res = try_with_retries(client, "tumble", TUMBLE_PROMPT, TUMBLE_STILL, tumble_raw)
    if tumble_res["status"] == "ok":
        trimmed = OUT / "omni_orbit_tumble_v05.mp4"
        trim_to(tumble_raw, trimmed, 4.5)
        cs = CONTACT / "omni_orbit_tumble_v05_contact.png"
        times = contact_sheet(trimmed, cs)
        heur = section6_heuristic(trimmed)
        section6 = {
            "verdict": "FAIL" if heur["heuristic_warn"] else "PASS_CANDIDATE",
            "heuristic": heur,
            "contact_times": times,
            "rules": [
                "exactly one Orbit",
                "exactly two stubby arms / three-finger hands",
                "no extra limbs mid-take",
                "swipe not hold",
                "4–5s take",
            ],
            "note": "Eyeball contact sheet required",
        }
        chunk_write(trimmed, UAT / trimmed.name)
        chunk_write(cs, UAT / cs.name)
        chunk_write(cs, ART / cs.name)
        report["clips"].append(
            {
                "file": trimmed.name,
                "status": "ok",
                "sha256": sha256(trimmed),
                "bytes": trimmed.stat().st_size,
                "duration_s": 4.5,
                "meta": tumble_res["meta"],
                "section6": section6,
                "contact": cs.name,
                "prior_errors": tumble_res["errors"],
            }
        )
    else:
        report["clips"].append(
            {
                "file": "omni_orbit_tumble_v05.mp4",
                "status": "FAILED_AFTER_3",
                "errors": tumble_res["errors"],
                "fallback": "veo_orbit_tumble_v03_fallback_0-3s.mp4",
            }
        )

    # --- Bare Orbit ---
    bare_raw = WORK / "omni_bare_orbit_vertex_raw.mp4"
    bare_res = try_with_retries(client, "bare_orbit", BARE_PROMPT, BARE_STILL, bare_raw)
    if bare_res["status"] == "ok":
        final = OUT / "omni_bare_orbit_v05.mp4"
        # trim to ~5s if longer
        probe = json.loads(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(bare_raw)]
            )
        )
        dur = float(probe["format"]["duration"])
        if dur > 5.2:
            trim_to(bare_raw, final, 5.0)
        else:
            chunk_write(bare_raw, final)
        cs = CONTACT / "omni_bare_orbit_v05_contact.png"
        times = contact_sheet(final, cs)
        heur = section6_heuristic(final)
        section6 = {
            "verdict": "FAIL" if heur["heuristic_warn"] else "PASS_CANDIDATE",
            "heuristic": heur,
            "contact_times": times,
            "rules": ["exactly one Orbit", "two stubby arms", "no extra limbs", "facing bare Saturn"],
        }
        chunk_write(final, UAT / final.name)
        chunk_write(cs, UAT / cs.name)
        chunk_write(cs, ART / cs.name)
        report["clips"].append(
            {
                "file": final.name,
                "status": "ok",
                "sha256": sha256(final),
                "bytes": final.stat().st_size,
                "meta": bare_res["meta"],
                "section6": section6,
                "contact": cs.name,
                "prior_errors": bare_res["errors"],
            }
        )
    else:
        report["clips"].append(
            {
                "file": "omni_bare_orbit_v05.mp4",
                "status": "FAILED_AFTER_3",
                "errors": bare_res["errors"],
            }
        )

    report["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST_OMNI_VERTEX.json").write_text(json.dumps(report, indent=2) + "\n")
    chunk_write((OUT / "MANIFEST_OMNI_VERTEX.json").read_bytes(), UAT / "MANIFEST_OMNI_VERTEX.json")
    print(json.dumps(report, indent=2), flush=True)
    if any(c.get("status") == "FAILED_AFTER_3" for c in report["clips"]):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
