#!/usr/bin/env python3
"""Orbit CG helpers + optional Gemini Veo API fallback.

DEFAULT picture path for new episodes is Google Flow Ultra UI:
  04_Audio/tools/orbit_flow_veo_ui.py

Secondary UI: AI Studio (`orbit_aistudio_veo_ui.py`) — often needs a paid API key.
This module owns shared prompt locks (`build_prompt`, IDENTITY_LOCK,
NEGATIVE, strip_audio) and an optional API path when UIs are unavailable.
API billing is separate from Google One Ultra — avoid for routine clip volume.

Do NOT use ElevenLabs Image & Video for CG.

Channel VO stays on ElevenLabs TTS → Ben Orbit Narrator (see orbit_voice.py).

API fallback auth (optional):
  export GEMINI_API_KEY=...   # or GOOGLE_API_KEY

Examples (prefer Flow UI):
  python3 04_Audio/tools/orbit_flow_veo_ui.py --probe

API fallback:
  python3 04_Audio/tools/orbit_gemini_veo.py --probe
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
# TRUE identity lock — single continuous orange sphere (Seedance).
# Never prefer quarantine plates under 05_Seedance-References/_Rejected/
# (orbit-cg-canonical-* is a white-chest / two-sphere redesign — hard reject).
ORBIT_REF_SEEDANCE = (
    REPO
    / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
ORBIT_REF_SEEDANCE_PORTRAIT = (
    REPO
    / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png"
)
ORBIT_REF = (
    ORBIT_REF_SEEDANCE
    if ORBIT_REF_SEEDANCE.exists()
    else ORBIT_REF_SEEDANCE_PORTRAIT
)

# Default paid/preview model — override with ORBIT_VEO_MODEL
DEFAULT_MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-fast-generate-preview")

try:
    from orbit_voice import CG_PREFACE, CG_SILENT_AUDIO_BLOCK  # type: ignore
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from orbit_voice import CG_PREFACE, CG_SILENT_AUDIO_BLOCK

IDENTITY_LOCK = (
    "CRITICAL ORBIT IDENTITY — match the attached Seedance reference image exactly, "
    "full-CG Orbit in every frame: ONE continuous matte ORANGE sphere/egg body "
    "(head and torso are the same piece — no neck, no two stacked spheres). "
    "NO LEGS — hover only with soft orange underside glow. "
    "Large black CURVED VISOR with TWO cream/white expressive circular eyes with pupils. "
    "Integrated side nubs (NOT headphones / ear rings). "
    "Solid orange chest — tiny vents OK; NO large white chest disc. "
    "Short stubby orange arms with dark three-finger hands when arms appear. "
    "Single thin antenna with glowing bulb tip. "
    "Emotion via cream eyes and body language only."
)

NEGATIVE = (
    "Eiffel Tower, Paris, lattice iron tower, blueprint, parchment, paper schematic, "
    "architectural drawing, Explore gallery overlay, white helmet, white belly, "
    "large white chest disc, white circular chest port, mustard charcoal redesign, "
    "separate head and body spheres, neck joint split body, ear rings, headphones, "
    "side head discs, legs, feet, walking, biped, HUD text, face text, "
    "Orbit lettering, blank visor, neon outline only face, slit LED eyes, "
    "socket ring eyes, cyan crescent eyes, different robot species, photoreal human, "
    "dialogue, speech, talking, narrator, lip sync"
)

ANGLE = {
    "p0": "Camera: steady medium shot; Orbit reacts with cream-eye emotion.",
    "p1": "Camera: gentle push-in, three-quarter left; continuous hover.",
    "p2": "Camera: slow lateral drift, slightly wider; full body motion.",
    "p3": "Camera: soft arc, warm rim light, parallax; motion through final frame.",
    "p4": "Camera: intimate then ease to medium; antenna + underside glow readable.",
}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def resolve_api_key(*extra_env_files: Path) -> str:
    for p in extra_env_files:
        load_dotenv(p)
    # Common project locations
    for p in (
        Path.cwd() / ".env",
        Path.cwd() / "07_Edit-Project" / ".env",
        REPO / "04_Audio" / "tools" / ".env",
    ):
        load_dotenv(p)
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise SystemExit(
            "Missing GEMINI_API_KEY (or GOOGLE_API_KEY).\n"
            "Get a key: https://aistudio.google.com/apikey\n"
            "Then: export GEMINI_API_KEY=...  or put it in Edit-Project/.env"
        )
    return key


def make_client(*extra_env_files: Path):
    key = resolve_api_key(*extra_env_files)
    from google import genai

    return genai.Client(api_key=key)


def orbit_image(ref: Path | None = None):
    from google.genai import types

    path = ref or ORBIT_REF
    if not path.exists():
        raise SystemExit(f"Orbit ref missing: {path}")
    return types.Image.from_file(str(path))


def build_prompt(scene_action: str, *, pass_id: str = "p0") -> str:
    """Compose a silent Veo prompt with Orbit identity + CG preface."""
    body = scene_action.strip()
    for marker in ("Preserve Orbit exactly:", "CRITICAL ORBIT IDENTITY"):
        if marker in body:
            body = body.split(marker)[0].rstrip()
    parts = [
        CG_PREFACE.strip(),
        "Start on Orbit the orange robot in the scene — never on paper, blueprints, or Earth landmarks.",
        body,
        IDENTITY_LOCK,
        ANGLE.get(pass_id, ANGLE["p0"]),
        "Animate from the reference: Orbit must remain the same character throughout.",
        CG_SILENT_AUDIO_BLOCK,
    ]
    return " ".join(p for p in parts if p).strip()


def strip_audio(path: Path) -> None:
    """Always strip model audio — British VO is mixed later from ElevenLabs."""
    tmp = path.with_suffix(".nosound.mp4")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(path), "-c:v", "copy", "-an", str(tmp)],
            check=True,
            capture_output=True,
        )
        tmp.replace(path)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"WARN strip audio failed: {e}", flush=True)
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def already_done(path: Path, *, min_bytes: int = 800_000) -> bool:
    return path.exists() and path.stat().st_size > min_bytes


def generate_clip(
    client,
    prompt: str,
    dest: Path,
    *,
    model: str = DEFAULT_MODEL,
    duration_seconds: int = 8,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    seed: int | None = None,
    orbit_ref: Path | None = None,
    poll_seconds: float = 12.0,
) -> dict:
    """Generate one silent Veo clip with Orbit ASSET + start-frame lock."""
    from google.genai import types

    img = orbit_image(orbit_ref)
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=duration_seconds,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        negative_prompt=NEGATIVE,
        enhance_prompt=True,
        generate_audio=False,
        reference_images=[
            types.VideoGenerationReferenceImage(
                image=img,
                reference_type=types.VideoGenerationReferenceType.ASSET,
            )
        ],
        seed=seed,
    )
    print(f"  submit model={model} → {dest.name}", flush=True)
    t0 = time.time()
    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        image=img,  # start frame = Orbit (blocks Explore/Eiffel path)
        config=config,
    )
    while not operation.done:
        time.sleep(poll_seconds)
        operation = client.operations.get(operation)
        print(f"  poll {dest.stem} … {int(time.time() - t0)}s", flush=True)

    if operation.error:
        raise RuntimeError(f"Veo error: {operation.error}")

    response = operation.response
    if not response or not response.generated_videos:
        raise RuntimeError("Veo returned no videos")
    video = response.generated_videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    if not already_done(dest):
        raise RuntimeError(f"download too small: {dest}")
    strip_audio(dest)
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "model": model,
        "engine": "gemini-api-veo",
        "orbit_ref": str(orbit_ref or ORBIT_REF),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--probe", action="store_true", help="One short Orbit test clip")
    ap.add_argument("--prompt", default="", help="Scene action (Orbit-in-scene)")
    ap.add_argument("--out", type=Path, default=Path("/tmp/orbit_gemini_veo_probe.mp4"))
    ap.add_argument("--pass-id", default="p0")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--env-file", type=Path, action="append", default=[])
    args = ap.parse_args()

    if args.probe and not args.prompt:
        args.prompt = (
            "Orbit the orange robot floats beside the James Webb Space Telescope, "
            "cream eyes curious, soft underside glow, deep space stars behind."
        )
    if not args.prompt:
        ap.error("Provide --prompt or --probe")

    prompt = build_prompt(args.prompt, pass_id=args.pass_id)
    print(f"Orbit ref: {ORBIT_REF}", flush=True)
    print(f"model={args.model} · out={args.out}", flush=True)
    if args.dry_run:
        print(prompt[:500], "…")
        return

    client = make_client(*args.env_file)
    meta = generate_clip(client, prompt, args.out, model=args.model)
    print(json.dumps(meta, indent=2))
    print(f"SAVED {args.out}", flush=True)


if __name__ == "__main__":
    main()
