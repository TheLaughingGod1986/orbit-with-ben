#!/usr/bin/env python3
"""Ensure Chrome CDP for TikTok (port 9222) is available."""
from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from pathlib import Path

CDP = "http://127.0.0.1:9222/json/version"
PROFILE = Path.home() / ".orbit-chrome-tiktok-dev"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def cdp_up() -> bool:
    try:
        with urllib.request.urlopen(CDP, timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def ensure_chrome(*, headless_ok: bool = False) -> dict:
    """Return {ok, started} — launches headed Chrome with remote debugging if needed."""
    if cdp_up():
        return {"ok": True, "started": False}
    if not CHROME.exists():
        return {"ok": False, "started": False, "error": "Chrome not found"}
    PROFILE.mkdir(parents=True, exist_ok=True)
    args = [
        str(CHROME),
        f"--remote-debugging-port=9222",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://www.tiktok.com/tiktokstudio/content",
    ]
    subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(30):
        time.sleep(1)
        if cdp_up():
            return {"ok": True, "started": True}
    return {"ok": False, "started": True, "error": "CDP did not come up"}
