#!/usr/bin/env bash
# Upload the vertical Shorts covers through Studio desktop (launchd wrapper).
#
# The Data API cannot set a Short's vertical cover — YouTube only accepts those
# in Studio on a computer — and Studio caps custom-thumbnail changes per day.
# This wrapper brings up Studio Chrome on CDP :9222 and resumes the batch,
# re-running daily until every Short has its cover.
set -uo pipefail

REPO="/Users/ben/code/Orbit-YouTube"
DIR="$REPO/00_Brand/Channel-Setup/tools"
ASSETS="$REPO/00_Brand/Channel-Setup/assets/shorts_covers_2026-08-25"
MARKER="$ASSETS/COVERS_DONE.marker"
LOG="$ASSETS/upload_run.log"
PY="$REPO/04_Audio/tools/.venv/bin/python"
PROFILE="$HOME/.orbit-chrome-youtube-studio"

exec >>"$LOG" 2>&1
echo "=== run $(date '+%F %T') ==="

if [[ -f "$MARKER" ]]; then
  echo "already complete — exiting"
  exit 0
fi

if ! curl -sf --max-time 3 http://127.0.0.1:9222/json/version >/dev/null; then
  echo "starting Studio Chrome"
  rm -f "$PROFILE"/Singleton*
  open -na "Google Chrome" --args \
    --remote-debugging-port=9222 \
    --remote-allow-origins='*' \
    --user-data-dir="$PROFILE" \
    --profile-directory=Default \
    --no-first-run --no-default-browser-check \
    "https://studio.youtube.com/"
  for _ in $(seq 1 30); do
    sleep 2
    curl -sf --max-time 3 http://127.0.0.1:9222/json/version >/dev/null && break
  done
fi

if "$PY" "$DIR/upload_shorts_covers_studio.py"; then
  date > "$MARKER"
  echo "ALL COVERS UPLOADED"
  exit 0
fi

echo "incomplete (daily limit or a failure) — will retry on the next scheduled run"
exit 1
