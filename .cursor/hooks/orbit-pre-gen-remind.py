#!/usr/bin/env python3
"""Remind agents before shell commands that look like VO/picture generation spend."""
from __future__ import annotations

import json
import re
import sys

GEN_RE = re.compile(
    r"(veo|omni|_generate_|elevenlabs|orbit_voice|orbit_gemini_veo|text_to_speech|"
    r"seedance|kling|generate_vo|vidiq_score|ultra.?credit|generate_videos|aistudio)",
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
            "Orbit Growth System v2 gate: before ElevenLabs VO or AI Studio Veo/Omni spend, "
            "confirm (1) pre-build vidIQ audit signed off, (2) script reviewer ≥90, "
            "(3) cold open 5/15/30s. "
            "CG = Google AI Studio — Veo for world, Omni ONLY when Orbit must move "
            "(stills first · 2–3 Veo Fast money shots · never Omni the whole film · no Kling). "
            "Mute Veo baked audio. VO = ElevenLabs Ben Orbit Narrator. "
            "See OMNI_LONGFORM_PLAYBOOK.md · orbit-omni-longform-playbook.mdc · orbit-gemini-veo-cg.mdc."
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
