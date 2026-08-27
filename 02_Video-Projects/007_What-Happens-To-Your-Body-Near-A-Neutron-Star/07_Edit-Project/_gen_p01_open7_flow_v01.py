#!/usr/bin/env python3
"""Flow Omni: Part 01 first-7s plates. Unique clips. Picture only. No mint."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _gen_part01_omni_cursor_v01 as gen  # noqa: E402
import orbit_flow_veo_ui as flow  # noqa: E402

EP = gen.EP
PLATES = HERE / "parts/p01_open7_omni_plates_v01.json"
OUT = EP / "04_Generated-Clips/01_Raw/part-01"
REPORT = HERE / "parts/p01_open7_omni_gen_report_v01.json"


def probe(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float((r.stdout or "").strip())
    except ValueError:
        return 0.0


def _resolve_start(plate: dict) -> Path | None:
    start = plate.get("start_frame")
    if not start:
        return None
    orbit_ref = HERE / start
    if not orbit_ref.exists():
        orbit_ref = EP / start
    return orbit_ref if orbit_ref.exists() else None


def main() -> None:
    headed = "--headed" in sys.argv
    data = json.loads(PLATES.read_text())
    from playwright.sync_api import sync_playwright

    report: list[dict] = []
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=headed, profile=flow.profile_path(None))
        configured = False
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=1500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("FLOW AUTH DEAD — Ben must sign in. Stop. No more gens.")
            print(f"logged_in url={page.url}", flush=True)
            for plate in data["plates"]:
                dest = OUT / plate["file"]
                if dest.exists() and dest.stat().st_size > 500_000 and probe(dest) >= 7.2:
                    print(f"SKIP {dest.name}", flush=True)
                    report.append({"id": plate["id"], "status": "skip", "file": dest.name})
                    continue
                start = _resolve_start(plate)
                if start is None:
                    raise SystemExit(f"missing start_frame for {plate['id']}")
                print(
                    f"\n=== Flow Omni open7 {plate['id']} {plate['slug']} "
                    f"orbit={plate.get('orbit')} start={start.name} ===",
                    flush=True,
                )
                try:
                    meta = gen.generate_omni(
                        page,
                        plate["prompt"],
                        dest,
                        configure=not configured,
                        attach_orbit=bool(plate.get("orbit")),
                        orbit_ref=start,
                    )
                    configured = True
                    print(f"SAVED {dest.name} {meta}", flush=True)
                    report.append({"id": plate["id"], "status": "ok", "file": dest.name, **meta})
                except Exception as e:
                    print(f"FAIL {plate['id']}: {e}", flush=True)
                    report.append({"id": plate["id"], "status": "fail", "error": str(e)})
                    configured = False
                    try:
                        flow.recover_flow_home(page)
                    except Exception:
                        pass
                    if "sign in" in str(e).lower() or "auth" in str(e).lower():
                        print("AUTH DEAD — stopping remaining plates", flush=True)
                        break
        finally:
            ctx.close()
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    ok = sum(1 for r in report if r["status"] in ("ok", "skip"))
    fail = sum(1 for r in report if r["status"] == "fail")
    print(f"OPEN7 FLOW DONE ok+skip={ok} fail={fail}", flush=True)
    if fail:
        raise SystemExit(1)


if __name__ == "__main__":
    os.environ.setdefault("ORBIT_PLATES_JSON", str(PLATES))
    os.environ.setdefault("ORBIT_OUT_DIR", str(OUT))
    main()
