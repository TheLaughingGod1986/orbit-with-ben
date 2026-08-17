#!/bin/bash
# Start Chrome with Meta Business Suite CDP profile (port 9223) if not already running.
set -euo pipefail
PROFILE="${HOME}/.orbit-chrome-meta-dev"
PORT=9223
# Do not open reels_composer here. Crash-restore + Leave Page? stacked
# composer tabs and froze the Mac. Playwright navigates to composer per post.
if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "CDP already up on :${PORT}"
  exit 0
fi

mkdir -p "$PROFILE"
# Launch the binary directly so --user-data-dir is honoured (open -na often
# ignores flags when another Chrome is already running).
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port="${PORT}" \
  --user-data-dir="$PROFILE" \
  --no-first-run \
  --no-default-browser-check \
  --hide-crash-restore-bubble \
  --disable-session-crashed-bubble \
  about:blank \
  >/dev/null 2>&1 &

for i in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
    echo "CDP ready on :${PORT}"
    exit 0
  fi
  sleep 1
done
echo "CDP failed to start" >&2
exit 1
