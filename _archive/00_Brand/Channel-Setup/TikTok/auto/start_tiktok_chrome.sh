#!/usr/bin/env bash
set -euo pipefail
PROFILE="${HOME}/.orbit-chrome-tiktok-dev"
PORT=9222
if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null; then
  echo "Chrome CDP already on :${PORT}"
  curl -s "http://127.0.0.1:${PORT}/json/version" | head -c 200; echo
  exit 0
fi
rm -f "$PROFILE/SingletonLock" "$PROFILE/SingletonSocket" "$PROFILE/SingletonCookie" 2>/dev/null || true
nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$PROFILE" \
  --no-first-run \
  --no-default-browser-check \
  --disable-extensions \
  --disable-gpu \
  --disable-software-rasterizer \
  --disable-dev-shm-usage \
  "https://www.tiktok.com/tiktokstudio/content" \
  >>/tmp/orbit-tiktok-chrome.log 2>&1 &
for i in $(seq 1 20); do
  if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null; then
    echo "Chrome CDP ready on :${PORT}"
    exit 0
  fi
  sleep 0.5
done
echo "Chrome CDP failed to start" >&2
exit 1
