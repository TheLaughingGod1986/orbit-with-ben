#!/usr/bin/env python3
"""Generate silent Orbit CG clips via Google Flow Veo UI (Ultra) from beats JSON.

Default CG path for new episodes. Uses Google Flow in a Playwright browser
with your Google One → AI Ultra session — not GEMINI_API_KEY.

Copy this into a new episode's 07_Edit-Project/ (or run from template).

Requires (one-time):
  python3 04_Audio/tools/orbit_flow_veo_ui.py --login
  pip install playwright && playwright install chromium

beats.json example:
  [
    {"id": "01A", "pass": "p0", "slug": "orbit-crosses-horizon",
     "prompt": "Orbit falls toward a black hole event horizon, cream eyes wide"}
  ]

Usage:
  python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --dry-run
  python3 _generate_veo_from_beats.py --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --limit 1

Fallbacks (only if Flow UI broken):
  python3 _generate_veo_from_beats.py --engine aistudio --beats … --out-dir …
  python3 _generate_veo_from_beats.py --engine api --beats … --out-dir …
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE
for _ in range(6):
    if (REPO / "04_Audio" / "tools" / "orbit_flow_veo_ui.py").exists():
        break
    REPO = REPO.parent
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

ENGINE_TAG = {
    "flow": "flow-veo",
    "aistudio": "aistudio-veo",
    "api": "gemini-api-veo",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--beats", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--profile", type=Path, default=None)
    ap.add_argument(
        "--engine",
        choices=("flow", "aistudio", "api"),
        default="flow",
        help="flow = Google Flow Ultra (default); aistudio = AI Studio UI; api = Gemini API key",
    )
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
        tag = ENGINE_TAG[args.engine]
        dest = args.out_dir / f"{pass_id}_{beat_id}_{slug}_{tag}_v01_raw.mp4"
        prompt = veo.build_prompt(row["prompt"], pass_id=pass_id)
        queue.append((pass_id, beat_id, slug, prompt, dest))

    model = {
        "flow": flow.DEFAULT_MODEL,
        "aistudio": "veo-3.1-fast-generate-preview",
        "api": veo.DEFAULT_MODEL,
    }[args.engine]
    print(
        f"queue {len(queue)} · engine={args.engine} · "
        f"model={model} · ref={veo.ORBIT_REF.name}"
    )
    if args.dry_run:
        for pass_id, beat_id, slug, prompt, dest in queue:
            print(f"  {pass_id} {beat_id} → {dest.name} ({len(prompt)} chars)")
        return

    ok = fail = 0

    if args.engine == "api":
        client = veo.make_client(args.env_file)
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
    elif args.engine == "aistudio":
        import orbit_aistudio_veo_ui as studio
        from playwright.sync_api import sync_playwright

        profile = studio.profile_path(args.profile)
        with sync_playwright() as p:
            ctx, page = studio.launch_context(
                p, headed=args.headed, profile=profile
            )
            try:
                for i, (pass_id, beat_id, slug, prompt, dest) in enumerate(queue, 1):
                    print(
                        f"\n=== [{i}/{len(queue)}] {pass_id} {beat_id} {slug} ===",
                        flush=True,
                    )
                    if args.skip_existing and veo.already_done(dest):
                        print("SKIP existing")
                        ok += 1
                        continue
                    try:
                        meta = studio.generate_clip(page, prompt, dest)
                        print(
                            f"SAVED {dest} ({meta['bytes']}) in {meta['seconds']}s"
                        )
                        ok += 1
                    except Exception as e:
                        fail += 1
                        print(f"FAIL: {e}")
                        if fail >= 3:
                            break
            finally:
                ctx.close()
    else:
        from playwright.sync_api import sync_playwright

        profile = flow.profile_path(args.profile)
        with sync_playwright() as p:
            ctx, page = flow.launch_context(
                p, headed=args.headed, profile=profile
            )
            try:
                for i, (pass_id, beat_id, slug, prompt, dest) in enumerate(queue, 1):
                    print(
                        f"\n=== [{i}/{len(queue)}] {pass_id} {beat_id} {slug} ===",
                        flush=True,
                    )
                    if args.skip_existing and veo.already_done(dest):
                        print("SKIP existing")
                        ok += 1
                        continue
                    try:
                        meta = flow.generate_clip(
                            page,
                            prompt,
                            dest,
                            reuse_project=(i > 1),
                        )
                        print(
                            f"SAVED {dest} ({meta['bytes']}) in {meta['seconds']}s"
                        )
                        ok += 1
                    except Exception as e:
                        fail += 1
                        print(f"FAIL: {e}")
                        if fail >= 3:
                            break
            finally:
                ctx.close()

    print(f"done ok={ok} fail={fail}")
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
