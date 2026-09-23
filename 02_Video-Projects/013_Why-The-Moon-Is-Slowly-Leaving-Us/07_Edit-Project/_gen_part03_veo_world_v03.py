#!/usr/bin/env python3
"""Part 03 variety WORLD plates via Gemini API Veo (Fast) — no Orbit, no reference image, silent.

Fallback for when Google Flow credits are exhausted. Same prompt list as the Flow variety run;
mints only ids that have no `{id}_*.mp4` in the part03 plate folder. Audio is never generated.

  python3 _gen_part03_veo_world_v03.py --dry-run
  python3 _gen_part03_veo_world_v03.py --only p03_18 p03_19
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
PROMPTS = HERE / "parts/part-03_flow_prompts_v03_variety.json"
OUT = PROJ / "04_Generated-Clips/part03/flow_world_v01"
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-fast-generate-preview")
WORLD_PREFIX = (
    "Silent cinematic CGI only. No people. No readable text. No logos. "
    "No mascot. No cartoon. Premium documentary look. "
)
NEGATIVE = (
    "people, faces, text, captions, subtitles, logos, watermark, cartoon, mascot, robot, "
    "flat water plane in space, ocean sheet cutting through a planet, cross-section table, "
    "duplicate Earth, twin planet, rings around the Moon, speech, narration, music"
)


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def strip_audio(path: Path) -> None:
    tmp = path.with_suffix(".noaudio.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(path), "-an", "-c:v", "copy", str(tmp)],
        check=True,
    )
    tmp.replace(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--env-file", type=Path, default=HERE / ".env")
    args = ap.parse_args()
    load_env(args.env_file)

    rows = json.loads(PROMPTS.read_text())
    todo = [r for r in rows if not list(OUT.glob(f"{r['id']}_*.mp4"))]
    if args.only:
        todo = [r for r in todo if r["id"] in set(args.only)]
    print(f"model={MODEL} todo={[r['id'] for r in todo]}", flush=True)
    if args.dry_run or not todo:
        for r in todo:
            print(f"  {r['id']}: {WORLD_PREFIX + r['prompt']}")
        return

    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY / GOOGLE_API_KEY missing")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    report = []
    for r in todo:
        stem = r["id"]
        print(f"\n=== {stem} (bed {r.get('bed')}) ===", flush=True)
        t0 = time.time()
        try:
            # Developer API mode has no generate_audio switch; any baked audio is stripped below.
            op = client.models.generate_videos(
                model=MODEL,
                source=types.GenerateVideosSource(prompt=WORLD_PREFIX + r["prompt"]),
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    duration_seconds=8,
                    aspect_ratio="16:9",
                    resolution="720p",
                    negative_prompt=NEGATIVE,
                    enhance_prompt=True,
                ),
            )
            while not op.done:
                time.sleep(10)
                op = client.operations.get(op)
                print(f"  poll … {int(time.time() - t0)}s", flush=True)
            if op.error:
                raise RuntimeError(str(op.error))
            vids = op.response.generated_videos if op.response else None
            if not vids:
                raise RuntimeError("no videos returned")
            video = vids[0]
            short = f"veo{int(time.time()) % 100000:05d}"
            dest = OUT / f"{stem}_{short}.mp4"
            client.files.download(file=video.video)
            video.video.save(str(dest))
            strip_audio(dest)
            print(f"  ok {dest.name} {dest.stat().st_size} bytes {int(time.time() - t0)}s", flush=True)
            report.append({"id": stem, "status": "ok", "file": dest.name, "model": MODEL, "seconds": round(time.time() - t0, 1)})
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {e}", flush=True)
            report.append({"id": stem, "status": "fail", "error": str(e)[:300]})

    (OUT / "_gen_report_v03_veo.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
