#!/usr/bin/env bash
# Start the two Chrome windows the studio agents drive on the MacBook (Ben, 9 Nov 2026: signed into YouTube Studio
# for both channels on the MacBook). Same ports and profile folders as the Mac mini:
#   9223  Orbit With Ben Studio   ~/.orbit-chrome-youtube-studio
#   9222  History of Science      ~/.hos-chrome-cdp
# Chrome refuses remote debugging on your everyday profile, so each port gets its own profile folder. The first run
# copies your everyday Chrome profile into each, so your Google sign-in comes with it (switch each window to the right
# channel once: Studio > your avatar > Switch account). If macOS refuses the copy, the window starts on a fresh profile
# and you sign in to Google there once. Later runs just start them if they aren't running.
#
#   bash scripts/macbook/start_cdp_browsers.sh            # start both (copy the profile first time)
#   bash scripts/macbook/start_cdp_browsers.sh --install  # also start them at every login (LaunchAgent)
#
# The MacBook worker offers itself Studio jobs only while the channel's port answers. Never quit these windows mid-job.
set -euo pipefail
SRC="${HOME}/Library/Application Support/Google/Chrome"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

start() {  # port profile-dir url
  local port="$1" dst="$2" url="$3"
  if curl -sf "http://127.0.0.1:${port}/json/version" >/dev/null 2>&1; then
    echo "CDP :${port} already up (${dst})"
    return 0
  fi
  if [[ ! -d "$dst/Default" ]]; then
    echo "First run: copying your Chrome profile to $dst (sign-ins come with it)"
    mkdir -p "$dst"
    if ! rsync -a --exclude 'Singleton*' --exclude 'BrowserMetrics*' --exclude 'Crashpad' \
      --exclude 'ShaderCache' --exclude 'GrShaderCache' --exclude 'GraphiteDawnCache' \
      --exclude 'component_crx_cache' --exclude 'extensions_crx_cache' --exclude 'Safe Browsing' \
      "$SRC/" "$dst/" 2>"/tmp/owb-cdp-rsync-${port}.log"; then
      # macOS can refuse the copy ("Operation not permitted", 9 Nov 2026). Keep what was copied to one side and
      # start a fresh profile instead: the window opens signed out, so sign in to Google there once.
      echo "Couldn't copy your Chrome profile (macOS blocked it). Starting a fresh one: sign in to Google in the new window."
      mv "$dst" "${dst}.partial.$(date +%s)"
      mkdir -p "$dst"
    fi
  fi
  rm -f "$dst/SingletonLock" "$dst/SingletonSocket" "$dst/SingletonCookie"
  nohup "$CHROME" --remote-debugging-port="${port}" --remote-allow-origins='*' --user-data-dir="$dst" \
    --profile-directory=Default --no-first-run --no-default-browser-check "$url" \
    >"/tmp/owb-cdp-${port}.log" 2>&1 &
  echo "Started Chrome on :${port} (pid $!)"
}

start 9223 "${HOME}/.orbit-chrome-youtube-studio" "https://studio.youtube.com/"
start 9222 "${HOME}/.hos-chrome-cdp" "https://studio.youtube.com/"

if [[ "${1:-}" == "--install" ]]; then
  plist="${HOME}/Library/LaunchAgents/com.owb.macbook-cdp.plist"
  script="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  cat >"$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.owb.macbook-cdp</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>${script}</string></array>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>/tmp/owb-cdp-launchd.log</string>
  <key>StandardErrorPath</key><string>/tmp/owb-cdp-launchd.log</string>
</dict></plist>
PLIST
  launchctl bootout "gui/$(id -u)/com.owb.macbook-cdp" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$plist"
  echo "Installed: both Studio windows start at every login"
fi
echo "In each new window: check Studio shows the right channel (9223 = Orbit With Ben, 9222 = History of Science)."
