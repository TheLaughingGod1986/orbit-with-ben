#!/usr/bin/env python3
"""Orbit sessionStart — inject Growth System v2 checklist into new agent sessions."""
from __future__ import annotations

import json
import sys

CONTEXT = """
# Orbit session checklist — Growth System v2 (auto-injected)

Follow these standing rules for this channel:

1. **Pre-build vidIQ audit (blocking)** before script lock / VO / Flow Veo gen → `00_Brand/Channel-Setup/PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
2. **Script reviewer ≥ 90** before VO/picture → `cd 07_Content-Ops && npm run review:script -- --file <script.md>`
2b. **Episode gate PASS** → `npm run gate:episode -- --project ../02_Video-Projects/<slug>`
3. **Longs:** 8–12 min trust window · cold open 5s/15s/30s · Question→Danger→Story→explain-in-story · Orbit experiences science · 4–6 acts · `[VISUAL MUST]` + `[ORBIT ACTS]` + `[TEACH]`
4. **Titles:** one promise · prefer ≤~60 chars · no series suffix · thumb = one question
5. **Shorts:** 3–5 · 22–30s · strongest-fact open · curiosity-gap end · Related→long
6. **CG = Google Flow Veo UI / Ultra** (`04_Audio/tools/orbit_flow_veo_ui.py`) · **VO = ElevenLabs** Ben Orbit Narrator only — never EL Image & Video for CG; AI Studio / API key are fallbacks only
7. **No dead ends:** end screen · cards · pin · description → another Orbit documentary
8. **Success:** impressions · CTR · AVD · APV · session time · returning viewers · Browse/Suggested/Search
9. Canonical: `00_Brand/Channel-Setup/YOUTUBE_GROWTH_SYSTEM_V2.md` · `RETENTION_AND_GROWTH_LOCKED.md`

Do not redesign the brand. Do not spend Ultra / Veo credits or lock VO until pre-build audit + script ≥90 are signed off for new episodes.
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
            "ORBIT_LONGFORM_MINUTES": "8-12",
            "ORBIT_GROWTH_SYSTEM": "v2",
            "ORBIT_CG_ENGINE": "flow-veo-ui",
            "ORBIT_VO_ENGINE": "elevenlabs",
        },
        "additional_context": CONTEXT,
    }
    sys.stdout.write(json.dumps(out))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
