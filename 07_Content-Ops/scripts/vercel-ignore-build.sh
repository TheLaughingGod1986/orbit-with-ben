#!/usr/bin/env bash
# Vercel Ignored Build Step for Orbit Content Ops (/go affiliate door).
# Exit 0 = skip build; exit 1 = proceed with build.
#
# Vercel Root Directory is 07_Content-Ops. Studio/jobs/board commits
# elsewhere in the monorepo must not burn the team's free deploy quota.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
APP_DIR="07_Content-Ops"

PREV="${VERCEL_GIT_PREVIOUS_SHA:-}"
if [[ -z "$PREV" ]]; then
  if git -C "$ROOT" rev-parse --verify --quiet HEAD^ >/dev/null; then
    PREV="$(git -C "$ROOT" rev-parse HEAD^)"
  else
    echo "[vercel-ignore-build] No previous commit — proceeding with build"
    exit 1
  fi
fi

if git -C "$ROOT" diff --quiet "$PREV" HEAD -- "$APP_DIR"; then
  echo "[vercel-ignore-build] No changes under ${APP_DIR} vs ${PREV} — skipping build"
  exit 0
fi

echo "[vercel-ignore-build] ${APP_DIR} changed vs ${PREV} — proceeding with build"
exit 1
