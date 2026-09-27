#!/bin/bash
# Ensure Chrome CDP, re-upload missing scheduled shorts, then unload this one-shot agent.
set -euo pipefail
ROOT="/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok"
cd "$ROOT"
bash "$ROOT/auto/start_tiktok_chrome.sh" || true
sleep 3
/usr/bin/python3 -u "$ROOT/_reupload_missing_scheduled_cdp.py" \
  2>&1 | tee -a "$ROOT/audit/tt_reschedule/reupload_missing_retry.log"
# Self-unload so it does not fire again next year
launchctl unload "$ROOT/auto/dev.orbit.tiktok-reupload-missing.plist" 2>/dev/null || true
launchctl unload "$HOME/Library/LaunchAgents/dev.orbit.tiktok-reupload-missing.plist" 2>/dev/null || true
