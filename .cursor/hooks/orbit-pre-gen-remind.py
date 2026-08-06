#!/usr/bin/env python3
"""Remind agents before shell commands that look like VO/picture generation spend."""
from __future__ import annotations

import json
import re
import sys

GEN_RE = re.compile(
    r"(veo|omni|_generate_|elevenlabs|orbit_voice|orbit_gemini_veo|orbit_aistudio_veo|"
    r"text_to_speech|seedance|generate_vo|vidiq_score|ultra.?credit|generate_videos|"
    r"aistudio)",
    re.I,
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    command = str(data.get("command") or data.get("tool_input", {}).get("command") or "")
    if not command and isinstance(data.get("arguments"), dict):
        command = str(data["arguments"].get("command") or "")

    if GEN_RE.search(command):
        msg = (
            "Orbit Growth System v2 gate: before ElevenLabs VO or AI Studio Veo CG spend, "
            "confirm (1) pre-build vidIQ audit signed off, (2) script reviewer ≥90, "
            "(3) cold open 5/15/30s + Orbit agency. "
            "CG = AI Studio Ultra UI (orbit_aistudio_veo_ui.py) — not EL Image & Video; "
            "API key is fallback only. "
            "VO = ElevenLabs Ben Orbit Narrator. "
            "See YOUTUBE_GROWTH_SYSTEM_V2.md · orbit-gemini-veo-cg.mdc."
        )
        sys.stdout.write(
            json.dumps(
                {
                    "permission": "allow",
                    "agent_message": msg,
                }
            )
        )
    else:
        sys.stdout.write(json.dumps({"permission": "allow"}))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
