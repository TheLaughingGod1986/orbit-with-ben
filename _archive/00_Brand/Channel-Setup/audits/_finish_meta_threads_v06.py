#!/usr/bin/env python3
"""Retry Meta reel shares + Threads video posts for the 3 live aliens Shorts."""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube")
EXPORTS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/live_funnel_four_2026-08-03"
SOFT = "Full film on YouTube."

TARGETS = [
    {"id": "1HuV8o3gOss", "title": "Where Is Everybody?", "file": "aliens_short-02_fermi-paradox_v02.mp4"},
    {"id": "dPMJQp2gMNc", "title": "Space Is Rude About Distance", "file": "aliens_short-01_distance_v02.mp4"},
    {"id": "rFJoOdQAc9c", "title": "What If Aliens Are Watching Us?", "file": "aliens_short-03_zoo-hypothesis_v02.mp4"},
]


def cdp_up(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def main() -> None:
    out = {"started_at": datetime.now(timezone.utc).isoformat(), "meta": {}, "threads": {}}
    assert cdp_up(9222), "9222 down"
    assert cdp_up(9223), "9223 down"

    # --- META ---
    sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/Meta"))
    from auto import caption as meta_cap  # type: ignore
    from auto import studio_upload as meta_up  # type: ignore

    creds_path = ROOT / "00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json"
    creds = json.loads(creds_path.read_text())
    orig = dict(creds)
    creds["business_id"] = "1203116147241086"
    creds["business_suite_asset_id"] = "1251385088056874"
    creds_path.write_text(json.dumps(creds, indent=2) + "\n")
    try:
        # Only retry unconfirmed ones from v05; still do all 3 for safety if needed
        prev = json.loads((AUDIT / "FINISH_v05.json").read_text())
        for t in TARGETS:
            prev_status = (prev.get("meta") or {}).get(t["id"], {}).get("status")
            if prev_status == "ok":
                out["meta"][t["id"]] = {"status": "skipped_already_ok"}
                print("meta skip", t["id"], flush=True)
                continue
            path = EXPORTS / t["file"]
            short = {"title": t["title"], "description": "", "video_id": t["id"]}
            cap = meta_cap.meta_caption(short)
            if SOFT not in cap:
                cap = f"{cap} {SOFT}".strip()
            print("meta post", t["id"], flush=True)
            r = meta_up.post_short(
                video_path=path,
                caption=cap,
                confirm_needle=meta_cap.confirm_needle(short, cap),
                audit_dir=AUDIT / "meta_v06",
                port=9223,
            )
            out["meta"][t["id"]] = r
            print(" meta", t["id"], r.get("status"), flush=True)
            time.sleep(2)
    finally:
        creds_path.write_text(json.dumps(orig, indent=2) + "\n")

    # --- THREADS ---
    import importlib.util as ilu

    def load_th(name: str):
        path = ROOT / "00_Brand/Channel-Setup/Threads/auto" / f"{name}.py"
        key = f"orbit_threads_auto_{name}_v06"
        if key in sys.modules:
            return sys.modules[key]
        spec = ilu.spec_from_file_location(key, path)
        mod = ilu.module_from_spec(spec)
        sys.modules[key] = mod
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        return mod

    th_up = load_th("studio_upload")
    th_cap = load_th("caption")
    th_ledger = load_th("ledger")

    ledger_path = ROOT / "00_Brand/Channel-Setup/Threads/THREADS_POSTED.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"posted": {}}
    for t in TARGETS:
        ledger.get("posted", {}).pop(f"yt:{t['id']}", None)
        ledger.get("posted", {}).pop(t["id"], None)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

    for t in TARGETS:
        if not cdp_up(9222):
            out["threads"]["cdp_died"] = True
            break
        path = EXPORTS / t["file"]
        short = {"title": t["title"], "description": "", "video_id": t["id"]}
        cap = th_cap.threads_caption(short)
        if SOFT not in cap:
            cap = f"{cap}\n\n{SOFT}".strip()
        print("threads post", t["id"], flush=True)
        try:
            r = th_up.post_short(
                video_path=path,
                caption=cap,
                confirm_needle=th_cap.confirm_needle(short, cap),
                audit_dir=AUDIT / "threads_v06",
                port=9222,
            )
            out["threads"][t["id"]] = r
            print(" threads", t["id"], r.get("status"), flush=True)
            if r.get("status") in ("ok", "unconfirmed"):
                try:
                    th_ledger.mark_posted(
                        {"video_id": t["id"], "title": t["title"], "file": str(path)},
                        result=r,
                    )
                except Exception:
                    pass
        except Exception as e:
            out["threads"][t["id"]] = {"status": "failed", "error": str(e)[:400]}
            print(" threads fail", t["id"], e, flush=True)
            time.sleep(2)

    out["finished_at"] = datetime.now(timezone.utc).isoformat()
    (AUDIT / "FINISH_v06_meta_threads.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "meta": {k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["meta"].items()},
        "threads": {k: (v.get("status") if isinstance(v, dict) else v) for k, v in out["threads"].items()},
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
