#!/usr/bin/env python3
"""Flow Omni backup: Part 08 all 8 plates, then Part 07 remnant-first open.

Gemini Omni API quota is dead today. One Playwright session.
"""
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
P08_JSON = HERE / "parts/part-08_omni_plates_cursor_v01.json"
P07_JSON = HERE / "parts/part-07_omni_plates_cursor_v04.json"
P08_OUT = EP / "04_Generated-Clips/01_Raw/part-08"
P07_OUT = EP / "04_Generated-Clips/01_Raw/part-07"
REPORT = HERE / "parts/part-08_omni_gen_report_flow_v01.json"


def _resolve_start(plate: dict) -> Path | None:
    start = plate.get("start_frame")
    if not start:
        return None
    orbit_ref = HERE / start
    if not orbit_ref.exists():
        orbit_ref = EP / start
    return orbit_ref if orbit_ref.exists() else None


def _gen_list(page, plates: list[dict], out_dir: Path, configured: bool) -> tuple[list[dict], bool]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for plate in plates:
        dest = out_dir / plate["file"]
        if plate.get("keep") or (dest.exists() and dest.stat().st_size > 500_000):
            print(f"SKIP {dest.name}", flush=True)
            report.append({"id": plate["id"], "status": "skip", "file": dest.name})
            continue
        print(
            f"\n=== Flow Omni {out_dir.name} {plate['id']} {plate['slug']} "
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
    return report, configured


def main() -> None:
    headed = "--headed" in sys.argv
    p08 = json.loads(P08_JSON.read_text())["plates"]
    p07_open = [
        p for p in json.loads(P07_JSON.read_text())["plates"] if p["id"] == "01"
    ]
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
            chunk, configured = _gen_list(page, p08, P08_OUT, configured)
            report.extend(chunk)
            if any(r.get("status") == "fail" and "AUTH" in str(r).upper() for r in chunk):
                pass
            else:
                chunk, configured = _gen_list(page, p07_open, P07_OUT, configured)
                report.extend(chunk)
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
    os.environ.setdefault("ORBIT_PLATES_JSON", str(P08_JSON))
    os.environ.setdefault("ORBIT_OUT_DIR", str(P08_OUT))
    main()
