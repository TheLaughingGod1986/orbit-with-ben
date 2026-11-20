#!/bin/bash
# Proposed detached-engine entrypoint. Never install before migration acceptance.
# Exec preserves launchd exit status; Python bounds the entire process group.
main() {
  local engine safe
  engine="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || return 1
  safe="${ANALYTICS_SAFE_DIR:-$HOME/Library/Application Support/owb-analytics}"
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
  if [[ -z ${ANALYTICS_CREDENTIAL_FILE:-} ]]; then
    echo 'Analytics requires a local credential-file path; nothing run' >&2
    return 1
  fi
  local options=()
  [[ ${BOARD_PUBLISH:-1} == 0 ]] && options+=(--no-board)
  exec "${STUDIO_PYTHON:-python3}" "$engine/scripts/analytics_timer.py" \
    --records "${ANALYTICS_RECORDS_DIR:-$safe/records}" \
    --credentials "$ANALYTICS_CREDENTIAL_FILE" \
    --cache "${ANALYTICS_GATE_CACHE:-$HOME/_desk/cache/gate-media}" \
    --safe-cache "$safe/gate-media" --gate-timeout "${GATE_LIMIT_S:-600}" "${options[@]}"
}
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
  main "$@"
fi
