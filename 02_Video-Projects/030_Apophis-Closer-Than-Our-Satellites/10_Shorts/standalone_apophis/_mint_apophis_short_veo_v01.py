#!/usr/bin/env python3
"""030 Apophis standalone Short: one Veo Fast rock take (J0223, SCRIPT_v01 frame 0 and the last ~3 s).

Text-to-video, no Orbit, no planet. The rock tumbles on pure black so the assembler can lay it over a
graded NASA Earth-limb plate (never a whole planet as a Veo start frame).
Vertex only (never AI Studio prepaid, never an API key). One take, no retry loop.
Veo 3.1 Fast on Vertex, audio off: ~£0.075/s, so ~£0.60 for 8 s, recorded in ai_spend.

  ~/.venvs/hos-vertex/bin/python _mint_apophis_short_veo_v01.py
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
REPO = HERE.parents[3]
OUT = HERE / "04_Generated-Clips/veo_v01"
REPORT = HERE / "veo_gen_report_v01.json"
PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
MODELS = ("veo-3.1-fast-generate-001", "veo-3.1-fast-generate-preview")
GBP_PER_S = 0.075

NEG = ("text, captions, subtitles, logos, watermark, numbers, robot, cartoon, mascot, planet, Earth, moon, "
       "globe, horizon, stars, nebula, lens flare text, speech, narration, fire trail, explosion")

ROWS = [
    {
        "id": "apophis_rock_tumble_veo_v01", "seconds": 8, "aspect": "9:16",
        "prompt": ("Photoreal space footage. A single elongated, peanut-shaped rocky asteroid, grey-brown, rough "
                   "and cratered with scattered boulders, fills most of the vertical frame and is already tumbling "
                   "slowly end over end as it sweeps from upper right towards lower left. Hard white sunlight from "
                   "the left gives a sharp terminator and deep shadows; the dark side falls to black. The background "
                   "is pure, empty black with no stars and nothing else in frame. The rock has clearly turned by "
                   "the first second and keeps rotating steadily. Smooth, steady camera, slight drift. Silent."),
    },
]


def record_spend(r: dict, model: str) -> None:
    amt = round(r["seconds"] * GBP_PER_S, 2)
    subprocess.run([sys.executable, str(REPO / "scripts/ai_spend.py"), "spend", "--pool", "vertex", "--amount",
                    str(amt), "--film", "OWB:030", "--what", f"J0223 Veo Fast {r['id']} {r['seconds']}s ({model}; est.)",
                    "--by", (os.environ.get("OWB_AGENT") or "cursor").lower()], cwd=REPO)


def gen(client, types, r: dict, dest: Path) -> str:
    last = None
    for model in MODELS:
        try:
            op = client.models.generate_videos(
                model=model, prompt=r["prompt"],
                config=types.GenerateVideosConfig(number_of_videos=1, duration_seconds=r["seconds"],
                                                  aspect_ratio=r["aspect"], resolution="1080p",
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


def sheet(mp4: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-vf",
                    "fps=6/8,scale=240:-2,tile=6x1", "-frames:v", "1", str(dest)], check=True)


def main() -> int:
    from google import genai
    from google.genai import types

    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        os.environ.pop(k, None)
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    report = {"startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "engine": "vertex_veo_fast",
              "project": PROJECT, "location": LOCATION, "request": "J0223 (Chief): one take, no retry", "rows": []}
    for r in ROWS:
        dest = OUT / f"{r['id']}.mp4"
        entry = {k: r[k] for k in ("id", "seconds", "aspect", "prompt")}
        if dest.exists():
            entry.update(status="skip", note="take already exists; no second take without Chief")
        else:
            t0 = time.time()
            try:
                model = gen(client, types, r, dest)
                record_spend(r, model)
                sh = OUT / f"{r['id']}_6frame.jpg"
                sheet(dest, sh)
                entry.update(status="ok", model=model, wall_seconds=round(time.time() - t0, 1),
                             bytes=dest.stat().st_size, sheet=sh.name,
                             sha256=subprocess.check_output(["shasum", "-a", "256", str(dest)], text=True).split()[0])
            except BaseException as e:  # noqa: BLE001 — no retry, record and move on
                entry.update(status="fail", error=f"{type(e).__name__}: {e}")
                if any(s in str(e).lower() for s in ("prepayment", "billing", "402", "resource_exhausted", "quota")):
                    report["stop"] = "billing"
        report["rows"].append(entry)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if all(x["status"] in ("ok", "skip") for x in report["rows"]) else 1


if __name__ == "__main__":
    sys.exit(main())
