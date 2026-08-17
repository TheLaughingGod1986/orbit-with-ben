#!/usr/bin/env python3
"""Ensure Chrome CDP for Meta Business Suite (default port 9223)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from _sib import load

config = load("config")
suite_ids = load("suite_ids")

PROFILE = Path.home() / ".orbit-chrome-meta-dev"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
COMPOSER = suite_ids.COMPOSER_PATH


def composer_url(creds: dict) -> str:
    return suite_ids.composer_url(creds)


def mark_exited_cleanly() -> None:
    """Stop Chrome restoring crashed Reels composer tabs on the next launch."""
    prefs_path = PROFILE / "Default" / "Preferences"
    if not prefs_path.exists():
        return
    try:
        data = json.loads(prefs_path.read_text())
        profile = data.setdefault("profile", {})
        profile["exit_type"] = "Normal"
        profile["exited_cleanly"] = True
        data.setdefault("session", {})["restore_on_startup"] = 5
        prefs_path.write_text(json.dumps(data))
    except Exception:
        pass
    sessions = PROFILE / "Default" / "Sessions"
    if sessions.is_dir():
        import shutil

        try:
            shutil.rmtree(sessions)
        except Exception:
            pass


def cdp_up(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
            json.loads(r.read().decode())
        return True
    except Exception:
        return False


def ensure_chrome(*, port: int | None = None) -> dict:
    creds = config.load_credentials()
    port = int(port or creds.get("cdp_port") or 9223)
    if cdp_up(port):
        return {"ok": True, "started": False, "port": port}
    if not CHROME.exists():
        return {"ok": False, "started": False, "error": "Chrome not found", "port": port}
    PROFILE.mkdir(parents=True, exist_ok=True)
    mark_exited_cleanly()
    # about:blank — never launch straight into reels_composer. That URL
    # plus Chrome's crash-restore bubble is what stacked tabs and froze the Mac.
    args = [
        str(CHROME),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-crash-restore-bubble",
        "--disable-session-crashed-bubble",
        "about:blank",
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
