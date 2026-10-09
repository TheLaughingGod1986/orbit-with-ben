#!/usr/bin/env python3
"""027 Veo Fast props, SHOT_LIST rows 5 and 31 (J0077, Claude #99 6086047504). Text-to-video, no Orbit.

Vertex only, on the free-trial credit (never AI Studio prepaid, never an API key). One take each, no retry loop.
Row 5 runs 10.3 s with 2 pictures, so 8 s is enough; row 31 runs 3.8 s, so 4 s.
Veo 3.1 Fast on Vertex is about $0.10/s with audio off: ~$1.20 for both, recorded per take in ai_spend.
A take that misses keeps the row's listed fallback; no second take without Claude.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE.parent / "04_Generated-Clips/01_Raw/veo_v01"
REPORT = HERE / "veo_gen_report_5_31_v01.json"
PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
MODELS = ("veo-3.1-fast-generate-001", "veo-3.1-fast-generate-preview")
GBP_PER_S = 0.075

NEG = ("text, captions, subtitles, logos, brand names, watermark, readable digits, numbers on screen, robot, "
       "cartoon, mascot, people's faces, speech, narration")

ROWS = [
    {
        "row": 5, "id": "cabin_pour_veo_v01", "seconds": 8,
        "prompt": ("Photoreal, steady close shot inside a calm airliner cabin in smooth flight: a hand pours sparkling "
                   "water from a small plain bottle into a clear plastic cup on a seat-back tray table. The surface of "
                   "the water stays perfectly level, not a drop spills. Soft daylight from the oval window beside it, "
                   "white clouds far below. No logos, no text, no brand marks. Silent."),
    },
    {
        "row": 31, "id": "phone_midnight_veo_v01", "seconds": 4,
        "prompt": ("Photoreal, still close shot of a plain black smartphone lying face-up on a wooden bedside table "
                   "in a dark bedroom at night. The screen lights up softly with a plain blurred glow, nothing "
                   "readable on it, lighting the edge of the table and a glass of water. No digits, no logos, "
                   "no text. Silent."),
    },
]


def record_spend(r: dict, model: str) -> None:
    amt = round(r["seconds"] * GBP_PER_S, 2)
    subprocess.run([sys.executable, str(REPO / "scripts/ai_spend.py"), "spend", "--pool", "vertex", "--amount",
                    str(amt), "--film", "OWB:027", "--what", f"Veo Fast prop {r['id']} {r['seconds']}s ({model}; est.)",
                    "--by", (os.environ.get("OWB_AGENT") or "cursor").lower()], cwd=REPO)


def gen(client, types, r: dict, dest: Path) -> str:
    last = None
    for model in MODELS:
        try:
            op = client.models.generate_videos(
                model=model, prompt=r["prompt"],
                config=types.GenerateVideosConfig(number_of_videos=1, duration_seconds=r["seconds"],
                                                  aspect_ratio="16:9", resolution="1080p",
                                                  generate_audio=False, negative_prompt=NEG))
        except Exception as e:  # noqa: BLE001 — model name not served here: try the other one
            if "404" in str(e) or "not found" in str(e).lower():
                last = e
                continue
            raise
        t0 = time.time()
        while not op.done:
            time.sleep(12)
            op = client.operations.get(op)
            print(f"  poll {r['id']} {int(time.time() - t0)}s", flush=True)
        if op.error:
            raise RuntimeError(f"Veo error: {op.error}")
        vids = (op.response.generated_videos if op.response else None) or []
        if not vids or not vids[0].video.video_bytes:
            raise RuntimeError("Veo returned no video bytes")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(vids[0].video.video_bytes)
        tmp = dest.with_suffix(".noaudio.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(dest), "-c:v", "copy", "-an", str(tmp)], check=True)
        tmp.replace(dest)
        return model
    raise RuntimeError(f"no Veo Fast model served on Vertex {LOCATION}: {last}")


def main() -> int:
    from google import genai
    from google.genai import types

    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        os.environ.pop(k, None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    report = {"startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "engine": "vertex_veo_fast",
              "project": PROJECT, "location": LOCATION, "request": "Claude #99 6086047504 (J0077): one take each",
              "rows": []}
    for r in ROWS:
        dest = OUT / f"{r['id']}.mp4"
        entry = {k: r[k] for k in ("row", "id", "seconds", "prompt")}
        if dest.exists():
            entry.update(status="skip", note="take already exists; no second take without Claude")
        else:
            t0 = time.time()
            try:
                model = gen(client, types, r, dest)
                record_spend(r, model)
                entry.update(status="ok", model=model, wall_seconds=round(time.time() - t0, 1),
                             bytes=dest.stat().st_size,
                             sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0])
            except BaseException as e:  # noqa: BLE001 — no retry, record and move on
                entry.update(status="fail", error=f"{type(e).__name__}: {e}")
                if any(s in str(e).lower() for s in ("prepayment", "billing", "402", "resource_exhausted", "quota")):
                    report["rows"].append(entry)
                    report["stop"] = "billing"
                    break
        report["rows"].append(entry)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if all(x["status"] in ("ok", "skip") for x in report["rows"]) else 1


if __name__ == "__main__":
    sys.exit(main())
