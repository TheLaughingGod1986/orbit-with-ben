#!/bin/bash
# Start Chrome with Meta Business Suite CDP profile (port 9223) if not already running.
set -euo pipefail
PROFILE="${HOME}/.orbit-chrome-meta-dev"
PORT=9223
# Pin to Orbit with Ben portfolio + Page (not Benkay Creative).
COMPOSER="https://business.facebook.com/latest/reels_composer?asset_id=1285932871266399&business_id=1352434763139246"

if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "CDP already up on :${PORT}"
  exit 0
fi

mkdir -p "$PROFILE"
open -na "Google Chrome" --args \
  --remote-debugging-port="${PORT}" \
  --user-data-dir="$PROFILE" \
  --no-first-run \
  --no-default-browser-check \
  "$COMPOSER"

for i in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
    echo "CDP ready on :${PORT}"
    exit 0
  fi
  sleep 1
done
echo "CDP failed to start" >&2
exit 1
