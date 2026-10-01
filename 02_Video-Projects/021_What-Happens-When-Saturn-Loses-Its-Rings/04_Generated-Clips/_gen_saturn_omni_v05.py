#!/usr/bin/env python3
"""Saturn Omni Orbit shots v05 — Ben 1 Oct 11:15/11:18. Canonical still attached.

1) omni_orbit_tumble_v05 — 4–5 s: slow roll drifting through ice; one quick swipe at a
   passing chunk (never holding). Exactly two stubby arms / three-finger hands.
   Max TWO §6 attempts; then stop. Fallback: veo_orbit_tumble_v03_fallback_0-3s.mp4.
2) omni_bare_orbit_v05 — small Orbit facing bare Saturn (composition from bare v06).

Uses Gemini API interactions (gemini-omni-flash-preview) with BOTH identity + composition
images when the API accepts them; otherwise composition start + identity lock text.
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

import orbit_gemini_omni as omni  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

EP = REPO / "02_Video-Projects" / "021_What-Happens-When-Saturn-Loses-Its-Rings"
CLIPS = EP / "04_Generated-Clips"
OUT = CLIPS / "veo_v05"
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_veo_v05_for_ben_ok"
)
CONTACT = OUT / "_contact"
WORK = OUT / "_work"
IDENTITY = (
    REPO / "01_Orbit-Character" / "05_Seedance-References" / "orbit-seedance-reference-16x9-v01.png"
)
TUMBLE_STILL = CLIPS / "stills_v04" / "saturn_orbit_tumble_v04.png"
BARE_STILL = CLIPS / "stills_v06" / "saturn_bare_orbit_v06.png"
ENV = (
    REPO
    / "02_Video-Projects"
    / "019_Andromeda-Milky-Way-Collision"
    / "07_Edit-Project"
    / ".env"
)

IDENTITY_LOCK = (
    " IDENTITY LOCK — match the attached canonical Orbit still exactly: "
    "matte orange rounded floater, one large black curved visor face with two cream eyes "
    "and dark pupils, EXACTLY TWO stubby side arm pods with dark THREE-FINGER hands, "
    "one antenna with glowing tip, one soft underside glow, NO LEGS. "
    "HARD REJECT shapes: extra forearms, multi-fingered big hands growing across the body, "
    "side pods turning into full humanoid arms, four limbs, second face, legs, toy knockoff."
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
    frames: list[Image.Image] = []
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


def trim_to(mp4: Path, dest: Path, seconds: float = 4.5) -> None:
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


def generate_omni_dual(client, prompt: str, composition: Path, dest: Path) -> dict:
    """Prefer identity + composition both attached; fall back to composition-only I2V."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    ident_b64 = base64.b64encode(IDENTITY.read_bytes()).decode("ascii")
    comp_b64 = base64.b64encode(composition.read_bytes()).decode("ascii")
    full = prompt + IDENTITY_LOCK + omni.SFX_LOCK
    # Try dual-image first (Ben: canonical attached)
    try:
        print(f"  Omni dual-image (identity+composition) → {dest.name}", flush=True)
        interaction = client.interactions.create(
            model=omni.DEFAULT_MODEL,
            input=[
                {"type": "image", "data": ident_b64, "mime_type": "image/png"},
                {"type": "image", "data": comp_b64, "mime_type": "image/png"},
                {
                    "type": "text",
                    "text": (
                        "Image 1 is the CANONICAL Orbit identity. Image 2 is the composition "
                        "start frame. Animate Image 2; Orbit must match Image 1 identity lock. "
                        + full
                    ),
                },
            ],
            response_format={"type": "video", "aspect_ratio": "16:9"},
            generation_config={"video_config": {"task": "image_to_video"}},
        )
        dest.write_bytes(omni._video_bytes(interaction))
        mode = "dual_image"
    except Exception as e:
        print(f"  dual-image failed ({e}); fallback composition I2V + identity lock text", flush=True)
        meta = omni.generate_omni_clip(
            client,
            full,
            dest,
            orbit_ref=composition,
            identity_ref=IDENTITY,
        )
        return {**meta, "attach_mode": "composition_i2v_identity_text"}
    size = dest.stat().st_size
    if size < 200_000:
        raise RuntimeError(f"download too small: {dest} ({size})")
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": size,
        "model": omni.DEFAULT_MODEL,
        "engine": "gemini-api-omni",
        "attach_mode": mode,
        "identity": str(IDENTITY),
        "composition": str(composition),
        "interaction_id": getattr(interaction, "id", None),
    }


def section6_heuristic(mp4: Path) -> dict:
    """Cheap orange-blob width check across 4 frames — flag sudden limb growth.

    Not a substitute for eyeballing the contact sheet; flags gross morphs.
    """
    times = contact_sheet(mp4, WORK / f"_tmp_{mp4.stem}_cs.png")
    widths = []
    for i, t in enumerate(times):
        p = WORK / f"_cs_{mp4.stem}_{i}.png"
        im = Image.open(p).convert("RGB")
        w, h = im.size
        xs = []
        for y in range(int(h * 0.2), int(h * 0.85), 3):
            for x in range(w):
                r, g, b = im.getpixel((x, y))
                if r > 140 and g > 60 and g < 180 and b < 120 and r > g + 30:
                    xs.append(x)
        span = (max(xs) - min(xs)) / w if xs else 0.0
        widths.append(round(span, 3))
    # FAIL if orange span jumps a lot (extra limbs widening blob) late vs early
    jump = max(widths) - min(widths)
    return {
        "orange_width_frac_by_frame": widths,
        "width_jump": round(jump, 3),
        "heuristic_warn": jump > 0.18,
        "note": "Eyeball contact sheet required — heuristic only flags gross morph width jumps",
    }


TUMBLE_PROMPT = (
    "Animate the composition start frame: exactly ONE Orbit (orange robot) tumbles with a "
    "SLOW ROLL while drifting through sparse ring ice chunks for about 4–5 seconds of action. "
    "One quick swipe at a passing ice chunk with one hand — never holding or grabbing and "
    "keeping the chunk. Ice floats past at different depths with black space between chunks. "
    "Saturn and rings stay in the background. Continuous motion, no freeze. "
    "Exactly two stubby arms with three-finger hands, no extra limbs. "
    "No second Orbit, no text, no spacecraft."
)

BARE_PROMPT = (
    "Animate the composition start frame: small orange Orbit (seen from behind / three-quarter) "
    "on the left facing bare Saturn (no rings) on the right. Slow gentle hover / tiny tip toward "
    "the planet. Keep Orbit the same size and on-model. No rings, no extra objects, no text. "
    "Exactly two stubby arms with three-finger hands, no extra limbs."
)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    UAT.mkdir(parents=True, exist_ok=True)
    CONTACT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    if not IDENTITY.is_file():
        raise SystemExit(f"missing identity {IDENTITY}")
    client = veo.make_client(ENV)

    report: dict = {
        "ben_order": "2026-10-01T11:18 London — Omni tumble 4–5s swipe; max 2 §6 fails",
        "identity": str(IDENTITY),
        "identity_sha256": sha256(IDENTITY),
        "clips": [],
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    # --- Tumble: max 2 attempts ---
    tumble_ok = False
    for attempt in range(1, 3):
        raw = WORK / f"omni_orbit_tumble_try{attempt}_raw.mp4"
        print(f"\n=== Omni tumble attempt {attempt}/2 ===", flush=True)
        try:
            meta = generate_omni_dual(client, TUMBLE_PROMPT, TUMBLE_STILL, raw)
        except Exception as e:
            print(f"FAIL generate: {e}", flush=True)
            report["clips"].append(
                {"file": "omni_orbit_tumble_v05.mp4", "attempt": attempt, "status": "gen_fail", "error": str(e)}
            )
            continue
        # trim to 4.5s
        trimmed = WORK / f"omni_orbit_tumble_try{attempt}_4p5s.mp4"
        trim_to(raw, trimmed, 4.5)
        cs = CONTACT / f"omni_orbit_tumble_try{attempt}_contact.png"
        times = contact_sheet(trimmed, cs)
        heur = section6_heuristic(trimmed)
        # Agent §6 check notes (heuristic + forced eyeball fields)
        section6 = {
            "attempt": attempt,
            "verdict": "PENDING_EYEBALL",
            "heuristic": heur,
            "contact_times": times,
            "rules_checked": [
                "exactly one Orbit",
                "exactly two stubby arms / three-finger hands",
                "no extra forearms / multi-finger growth",
                "no legs",
                "no second face",
                "swipe not hold",
            ],
        }
        # Auto-fail obvious width jump (extra limbs)
        if heur["heuristic_warn"]:
            section6["verdict"] = "FAIL"
            section6["reason"] = "orange blob width jump suggests extra limbs mid-take"
            chunk_write(trimmed, OUT / f"_rejected_omni_orbit_tumble_try{attempt}.mp4")
            chunk_write(cs, UAT / cs.name)
            report["clips"].append(
                {
                    "file": "omni_orbit_tumble_v05.mp4",
                    "attempt": attempt,
                    "status": "fail_section6",
                    "sha256": sha256(trimmed),
                    "meta": meta,
                    "section6": section6,
                }
            )
            print(f"  §6 FAIL attempt {attempt}: {section6['reason']}", flush=True)
            continue

        # Ship candidate for Ben eyeball (agent marks PASS_CANDIDATE if heuristic clean)
        section6["verdict"] = "PASS_CANDIDATE"
        section6["reason"] = "no gross orange-width jump; Ben confirms via contact sheet"
        final = OUT / "omni_orbit_tumble_v05.mp4"
        chunk_write(trimmed, final)
        chunk_write(final, UAT / final.name)
        chunk_write(cs, UAT / "omni_orbit_tumble_v05_contact.png")
        chunk_write(cs, CONTACT / "omni_orbit_tumble_v05_contact.png")
        report["clips"].append(
            {
                "file": final.name,
                "attempt": attempt,
                "status": "ok_candidate",
                "sha256": sha256(final),
                "bytes": final.stat().st_size,
                "duration_s": 4.5,
                "meta": meta,
                "section6": section6,
                "contact": "omni_orbit_tumble_v05_contact.png",
            }
        )
        tumble_ok = True
        print(f"  §6 PASS_CANDIDATE attempt {attempt} → {final.name}", flush=True)
        break

    if not tumble_ok:
        report["tumble"] = {
            "status": "STOPPED_AFTER_TWO_FAILS",
            "fallback": "veo_orbit_tumble_v03_fallback_0-3s.mp4",
            "fallback_sha256": sha256(OUT / "veo_orbit_tumble_v03_fallback_0-3s.mp4")
            if (OUT / "veo_orbit_tumble_v03_fallback_0-3s.mp4").is_file()
            else None,
            "note": "Do not attempt a third Omni tumble without Ben.",
        }
        print("STOPPED: Omni tumble failed §6 twice — use fallback 0–3s", flush=True)

    # --- Bare Orbit facing Saturn ---
    bare_raw = WORK / "omni_bare_orbit_raw.mp4"
    print("\n=== Omni bare Orbit facing Saturn ===", flush=True)
    try:
        meta = generate_omni_dual(client, BARE_PROMPT, BARE_STILL, bare_raw)
        bare_final = OUT / "omni_bare_orbit_v05.mp4"
        # keep ~5s if longer
        probe = json.loads(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(bare_raw)]
            )
        )
        dur = float(probe["format"]["duration"])
        if dur > 5.2:
            trim_to(bare_raw, bare_final, 5.0)
        else:
            chunk_write(bare_raw, bare_final)
        cs = CONTACT / "omni_bare_orbit_v05_contact.png"
        times = contact_sheet(bare_final, cs)
        heur = section6_heuristic(bare_final)
        section6 = {
            "verdict": "FAIL" if heur["heuristic_warn"] else "PASS_CANDIDATE",
            "heuristic": heur,
            "contact_times": times,
            "rules_checked": [
                "exactly one Orbit",
                "exactly two stubby arms",
                "no extra limbs",
                "no legs",
                "facing bare Saturn",
            ],
        }
        chunk_write(bare_final, UAT / bare_final.name)
        chunk_write(cs, UAT / cs.name)
        report["clips"].append(
            {
                "file": bare_final.name,
                "status": "ok_candidate" if section6["verdict"] == "PASS_CANDIDATE" else "fail_section6",
                "sha256": sha256(bare_final),
                "bytes": bare_final.stat().st_size,
                "meta": meta,
                "section6": section6,
                "contact": cs.name,
            }
        )
    except Exception as e:
        report["clips"].append({"file": "omni_bare_orbit_v05.mp4", "status": "gen_fail", "error": str(e)})
        print(f"FAIL bare Omni: {e}", flush=True)

    report["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "MANIFEST_OMNI.json").write_text(json.dumps(report, indent=2) + "\n")
    chunk_write((OUT / "MANIFEST_OMNI.json").read_bytes(), UAT / "MANIFEST_OMNI.json")
    print(json.dumps({"OMNI_V05_DONE": True, "tumble_ok": tumble_ok}, indent=2), flush=True)
    if not tumble_ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
