#!/usr/bin/env bash
# Post-premiere Last Star thumbnail A/B test (launchd wrapper).
# Ensures Studio Chrome CDP :9222 (detached via `open`), waits, runs the
# python setter, retries once, and stops for good after success.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
MARKER="$DIR/AB_TEST_DONE.marker"
LOG="$DIR/ab_test_run.log"
PY="/Users/ben/code/Orbit-YouTube/04_Audio/tools/.venv/bin/python"
PROFILE="$HOME/.orbit-chrome-youtube-studio"

exec >>"$LOG" 2>&1
echo "=== run $(date '+%F %T') ==="

if [[ -f "$MARKER" ]]; then
  echo "already done — exiting"
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

for attempt in 1 2; do
  echo "--- attempt $attempt"
  if "$PY" "$DIR/_set_ab_test_post_premiere.py"; then
    date > "$MARKER"
    echo "SUCCESS"
    exit 0
  fi
  sleep 60
done
echo "FAILED after 2 attempts — see AB_TEST_RESULT.json"
exit 1
