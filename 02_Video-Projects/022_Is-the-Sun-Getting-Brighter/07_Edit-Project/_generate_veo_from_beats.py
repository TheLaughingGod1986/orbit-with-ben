#!/usr/bin/env python3
"""Generate silent Orbit CG clips via Gemini Veo from a beats JSON file.

Copy this into a new episode's 07_Edit-Project/ (or run from template).

Requires:
  export GEMINI_API_KEY=...
  pip install google-genai

beats.json example:
  [
    {"id": "01A", "pass": "p0", "slug": "orbit-crosses-horizon",
     "prompt": "Orbit falls toward a black hole event horizon, cream eyes wide"}
  ]

Usage:
  python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --dry-run
  python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --limit 1
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Prefer repo tools path (works from template copy under 02_Video-Projects/…)
HERE = Path(__file__).resolve().parent
REPO = HERE
for _ in range(6):
    if (REPO / "04_Audio" / "tools" / "orbit_gemini_veo.py").exists():
        break
    REPO = REPO.parent
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

import orbit_gemini_veo as veo  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--beats", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--env-file", type=Path, default=HERE / ".env")
    args = ap.parse_args()

    beats = json.loads(args.beats.read_text())
    if args.limit > 0:
        beats = beats[: args.limit]

    queue = []
    for row in beats:
        pass_id = row.get("pass", "p0")
        slug = row["slug"]
        beat_id = row.get("id", slug)
        dest = args.out_dir / f"{pass_id}_{beat_id}_{slug}_gemini-veo_v01_raw.mp4"
        prompt = veo.build_prompt(row["prompt"], pass_id=pass_id)
        queue.append((pass_id, beat_id, slug, prompt, dest))

    print(f"queue {len(queue)} · model={veo.DEFAULT_MODEL} · ref={veo.ORBIT_REF.name}")
    if args.dry_run:
        for pass_id, beat_id, slug, prompt, dest in queue:
            print(f"  {pass_id} {beat_id} → {dest.name} ({len(prompt)} chars)")
        return

    client = veo.make_client(args.env_file)
    ok = fail = 0
    for i, (pass_id, beat_id, slug, prompt, dest) in enumerate(queue, 1):
        print(f"\n=== [{i}/{len(queue)}] {pass_id} {beat_id} {slug} ===", flush=True)
        if args.skip_existing and veo.already_done(dest):
            print("SKIP existing")
            ok += 1
            continue
        try:
            meta = veo.generate_clip(client, prompt, dest)
            print(f"SAVED {dest} ({meta['bytes']}) in {meta['seconds']}s")
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL: {e}")
            if fail >= 3:
                break
    print(f"done ok={ok} fail={fail}")
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
