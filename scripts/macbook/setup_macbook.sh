#!/bin/zsh
# One-time setup of the MacBook worker lane (Ben, 28 Oct 2026: "yes" to the MacBook worker and Ollama install).
# Run it yourself on the MacBook Pro, in Terminal:
#
#   curl -fsSL https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/main/scripts/macbook/setup_macbook.sh | zsh
#   (or, from a checkout:  zsh scripts/macbook/setup_macbook.sh)
#
# What it does, and what it never does:
#   1. uses your ~/YouTube checkouts only if they are clean and on main; otherwise clones its own into ~/_desk/worker
#      and leaves yours exactly as they are (your GitHub sign-in);
#   2. installs Ollama with Homebrew and starts it ON THIS MAC ONLY (127.0.0.1:11434). It checks nothing else on the
#      network or Tailscale can reach it, and stops it if something can;
#   3. downloads the local text model (default qwen3:14b, about 9 GB; OLLAMA_MODEL=... to change, SKIP_MODEL=1 to skip);
#   4. installs the launchd worker (every 15 min; only on mains power, only when you've been away 10 min).
#   It never changes sleep, firewall, Tailscale or security settings, never signs in to anything for you, never
#   prints keys, and spends nothing. Re-running it is safe.
set -euo pipefail

# Everything runs inside main(): with `curl | zsh` the script arrives on stdin, and a command that reads stdin
# (brew install did, 28 Oct) would otherwise swallow the rest of it. main() is parsed whole before it runs.
main() {

say() { print -P "%F{cyan}==>%f $*"; }
stop() { print -P "%F{red}STOP:%f $*"; exit 1; }

[[ "$(uname -s)" == "Darwin" ]] || stop "run this on the MacBook (macOS)."
[[ "$(uname -m)" == "arm64" ]] || say "not Apple Silicon: the local model will be slow."
command -v brew >/dev/null || stop "Homebrew isn't installed. Install it from https://brew.sh, then run this again."
command -v git >/dev/null || stop "git isn't installed (xcode-select --install), then run this again."

YT="$HOME/YouTube"
WORK="$HOME/_desk/worker"
MODEL="${OLLAMA_MODEL:-qwen3:14b}"
mkdir -p "$YT" "$WORK" "$HOME/_desk/state" "$HOME/_desk/logs" "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

# The worker needs a checkout on main with no local changes. Ben's own checkout is used only if it is exactly that;
# otherwise (another branch, local edits) it is left alone and the worker gets its own clone in ~/_desk/worker.
pick_repo() {  # pick_repo <preferred dir> <worker dir> <url>
  local pref="$1" own="$2" url="$3"
  if [[ -d "$pref/.git" && "$(git -C "$pref" branch --show-current)" == "main" && -z "$(git -C "$pref" status --porcelain)" ]] \
     && git -C "$pref" pull -q --ff-only </dev/null; then
    REPLY="$pref"; return
  fi
  if [[ -d "$pref/.git" ]]; then
    say "   $pref isn't a clean main checkout ($(git -C "$pref" branch --show-current || echo detached)); leaving it as it is." >&2
  fi
  if [[ ! -d "$own/.git" ]]; then
    GIT_LFS_SKIP_SMUDGE=1 git clone -q "$url" "$own" </dev/null || stop "couldn't clone $url (sign in to GitHub, then re-run)."
  fi
  git -C "$own" checkout -q main </dev/null && git -C "$own" pull -q --ff-only </dev/null || stop "$own didn't pull cleanly."
  REPLY="$own"
}

say "1/4 studio checkouts"
pick_repo "${OWB_REPO:-$YT/orbit-with-ben}" "$WORK/orbit-with-ben" https://github.com/TheLaughingGod1986/orbit-with-ben.git
OWB="$REPLY"
pick_repo "${HOS_REPO:-$YT/History Of Science}" "$WORK/history-of-science" https://github.com/TheLaughingGod1986/history-of-science.git
HOS="$REPLY"
say "   worker uses: $OWB"
say "                $HOS"

say "2/4 Ollama, local only"
command -v ollama >/dev/null || brew install ollama </dev/null
host="$(launchctl getenv OLLAMA_HOST 2>/dev/null || true)"
if [[ -n "$host" && "$host" != 127.0.0.1* && "$host" != localhost* ]]; then
  stop "OLLAMA_HOST is set to '$host', which can expose Ollama beyond this Mac. Run: launchctl unsetenv OLLAMA_HOST, then re-run."
fi
brew services start ollama </dev/null >/dev/null 2>&1 || brew services restart ollama </dev/null >/dev/null
for i in {1..20}; do curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1 && break; sleep 1; done
curl -fsS http://127.0.0.1:11434/api/version >/dev/null || stop "Ollama didn't start (brew services list)."
listen="$(lsof -nP -iTCP:11434 -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $9}' | sort -u)"
if [[ -z "$listen" ]]; then
  say "   (lsof found no listener to check; Ollama binds 127.0.0.1 by default)"
elif print -r -- "$listen" | grep -qvE '^(127\.0\.0\.1|\[::1\]|localhost):11434$'; then
  brew services stop ollama >/dev/null
  stop "Ollama was listening on: $listen (not only this Mac), so it's stopped. Check OLLAMA_HOST, then re-run."
fi
say "   Ollama is up on 127.0.0.1:11434 only."

say "3/4 local text model ($MODEL)"
if [[ "${SKIP_MODEL:-}" == "1" ]]; then
  say "   skipped (SKIP_MODEL=1)."
else
  ollama pull "$MODEL" </dev/null
  reply="$(curl -fsS http://127.0.0.1:11434/api/generate -d "{\"model\":\"$MODEL\",\"prompt\":\"Reply with the single word OK.\",\"stream\":false,\"think\":false}" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("response","").strip()[:40])' || true)"
  say "   test reply: ${reply:-<none>}"
fi

say "4/4 launchd worker"
CLI_OK=1
command -v codex >/dev/null || [[ -x "$HOME/.npm-global/bin/codex" ]] || CLI_OK=0
PLIST="$HOME/Library/LaunchAgents/com.owb.macbook-worker.plist"
sed -e "s#__HOME__#$HOME#g" -e "s#__OWB__#$OWB#g" -e "s#__HOS__#$HOS#g" -e "s#__MODEL__#$MODEL#g" \
  "$OWB/scripts/macbook/com.owb.macbook-worker.plist" > "$PLIST"
launchctl bootout "gui/$(id -u)/com.owb.macbook-worker" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
python3 "$OWB/scripts/macbook_worker.py" check || true

print
say "Done. The worker checks every 15 min and only takes 'macbook' jobs."
[[ $CLI_OK == 1 ]] || say "One thing for you: install and sign in to the Codex CLI on this Mac (npm i -g @openai/codex, then codex login). Until then the worker releases any job it claims."
say "Pause:  touch ~/_desk/state/macbook-worker.pause    Log: ~/Library/Logs/owb-macbook-worker.log"
}

main "$@" </dev/null
