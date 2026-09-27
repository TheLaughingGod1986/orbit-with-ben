#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok"
PY="/Users/ben/code/youtube/Video 004 - Decorative vs Meaningful ALT/.venv/bin/python3"
bash "$ROOT/auto/start_tiktok_chrome.sh"
sleep 3
cd "$ROOT"
"$PY" _upload_missing_v02_cdp.py | tee -a audit/tt_v02_replace/missing_upload_launchd.log
# unload self after one run
launchctl bootout "gui/$(id -u)/dev.orbit.tiktok-upload-missing-v02" 2>/dev/null || true
