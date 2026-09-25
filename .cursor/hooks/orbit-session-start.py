#!/usr/bin/env python3
"""Orbit sessionStart — point new agent sessions at AGENTS.md and the docs in force."""
from __future__ import annotations

import json
import sys

CONTEXT = """
# Orbit With Ben — session start (auto-injected)

Read `AGENTS.md` at the repo root first. Docs in force, highest first:
1. `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`
2. `THUMBNAIL_AND_TITLE_RULES.md`
3. `STUDIO_PLAYBOOK.md`
4. `YOUTUBE_GROWTH_AND_POLICY.md`
5. `CHANNEL_AUTHORITY.md`
6. `YOUTUBE_FRAME_SIZES.md`
7. `IMPROVEMENTS_BACKLOG.md`
Everything in `_archive/` is superseded — ignore it unless Ben asks.

- Week: one 8–9 min long, Sunday 18:00 UK, normal publish (no Premiere); three 22–27 s Shorts, Mon/Wed/Fri 11:30 UK.
- Before VO or picture spend: pre-build vidIQ audit, `npm run review:script` ≥90, `npm run gate:episode` PASS.
- Every Short export: `gate_shorts_open.py check` PASS, then watch it once on a phone with sound on.
- Stop for Ben's OK: topic · long script · Short scripts · voice · moving picture · thumbnails · anything going public.
""".strip()


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    out = {
        "env": {
            "ORBIT_RETENTION_GATE": "1",
            "ORBIT_PREBUILD_VIDIQ_REQUIRED": "1",
            "ORBIT_SCRIPT_REVIEW_MIN": "90",
            "ORBIT_LONGFORM_MINUTES": "8-9",
            "ORBIT_STUDIO_DOCS": "AGENTS.md",
            "ORBIT_CG_ENGINE": "aistudio-veo-world-omni-orbit",
            "ORBIT_VO_ENGINE": "elevenlabs",
        },
        "additional_context": CONTEXT,
    }
    sys.stdout.write(json.dumps(out))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
