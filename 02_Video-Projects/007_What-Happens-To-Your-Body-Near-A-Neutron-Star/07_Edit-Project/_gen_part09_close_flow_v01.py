#!/usr/bin/env python3
"""Flow Omni backup: Part 09 close plates. Gemini API spend cap is dead."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import _gen_part01_omni_cursor_v01 as gen  # noqa: E402
import orbit_flow_veo_ui as flow  # noqa: E402

EP = gen.EP
JSON = HERE / "parts/part-09_close_omni_plates_v01.json"
OUT = EP / "04_Generated-Clips/01_Raw/part-09-close"
REPORT = HERE / "parts/part-09_close_omni_gen_report_flow_v01.json"


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
    plates = json.loads(JSON.read_text())["plates"]
    only = {a for a in sys.argv[1:] if not a.startswith("--")}
    if only:
        plates = [p for p in plates if p["id"] in only or p["slug"] in only]
    OUT.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright

    report: list[dict] = []
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
            for plate in plates:
                dest = OUT / plate["file"]
                if plate.get("keep") or (dest.exists() and dest.stat().st_size > 500_000):
                    print(f"SKIP {dest.name}", flush=True)
                    report.append({"id": plate["id"], "status": "skip", "file": dest.name})
                    continue
                print(
                    f"\n=== Flow Omni close {plate['id']} {plate['slug']} "
                    f"orbit={plate.get('orbit')} ===",
                    flush=True,
                )
                try:
                    meta = gen.generate_omni(
                        page,
                        plate["prompt"],
                        dest,
                        configure=not configured,
                        attach_orbit=bool(plate.get("orbit")),
                        orbit_ref=_resolve_start(plate),
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
    print(f"ALL DONE ok+skip={ok} fail={fail}", flush=True)
    missing = [r["id"] for r in report if r["status"] == "fail"]
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    os.environ["ORBIT_PLATES_JSON"] = str(JSON)
    os.environ["ORBIT_OUT_DIR"] = str(OUT)
    main()
