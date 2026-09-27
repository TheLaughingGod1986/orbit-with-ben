#!/usr/bin/env python3
"""Ensure Chrome CDP for Threads (default port 9222 — shared IG session)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

AUTO = Path(__file__).resolve().parent

import importlib.util as _ilu
from pathlib import Path as _P
def _threads_load(name: str):
    auto = _P(__file__).resolve().parent
    key = f"orbit_threads_auto_{name}"
    import sys as _sys
    if key in _sys.modules:
        return _sys.modules[key]
    path = auto / f"{name}.py"
    spec = _ilu.spec_from_file_location(key, path)
    mod = _ilu.module_from_spec(spec)
    _sys.modules[key] = mod
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

load = _threads_load

config = load("config")

PROFILE = Path.home() / ".orbit-chrome-tiktok-dev"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
HOME = "https://www.threads.com/"


def cdp_up(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def ensure_chrome(*, port: int | None = None) -> dict:
    creds = config.load_credentials()
    port = int(port or creds.get("cdp_port") or 9222)
    if cdp_up(port):
        return {"ok": True, "started": False, "port": port}
    if not CHROME.exists():
        return {"ok": False, "started": False, "error": "Chrome not found", "port": port}
    PROFILE.mkdir(parents=True, exist_ok=True)
    args = [
        str(CHROME),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={str(PROFILE)}",
        "--no-first-run",
        "--no-default-browser-check",
        HOME,
    ]
    subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(30):
        time.sleep(1)
        if cdp_up(port):
            return {"ok": True, "started": True, "port": port}
    return {"ok": False, "started": True, "error": "CDP did not come up", "port": port}
