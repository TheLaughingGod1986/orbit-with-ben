#!/usr/bin/env python3
"""Orbit sessionStart — inject Growth System v2 checklist into new agent sessions."""
from __future__ import annotations

import json
import sys

CONTEXT = """
# Orbit session checklist — Growth System v2 (auto-injected)

Follow these standing rules for this channel:

1. **Pre-build vidIQ audit (blocking)** before script lock / VO / picture gen → `00_Brand/Channel-Setup/PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
2. **Script reviewer ≥ 90** before VO/picture → `cd 07_Content-Ops && npm run review:script -- --file <script.md>`
2b. **Episode gate PASS** → `npm run gate:episode -- --project ../02_Video-Projects/<slug>`
3. **Longs:** 7–9 min NOW · cold open 5s/15s/30s · Question→Danger→Story→explain-in-story · **world does the science** · Orbit in **1–2** inquisitive beats · 4–6 acts · `[VISUAL MUST]` + `[ORBIT ACTS]` (Orbit beats only) + `[TEACH]`
4. **Titles:** one promise · prefer ≤~60 chars · no series suffix · long thumb = picture + SEA hook (**no Orbit**)
5. **Shorts:** 4–8 · 22–27s · picture in 1s · picture thumb no Orbit · exact listing title on screen · CTA that week’s Thursday id · Related→long · zero `/go/`
6. **CG = Google AI Studio** — **Veo** for world · **Omni only** when Orbit must move · stills first · 2–3 Veo Fast money shots · mute Veo audio · **never Omni the whole film** · no Kling / EL Image & Video / Seedance · **VO = ElevenLabs** Ben Orbit Narrator
7. **No dead ends:** end screen · cards · pin · description → another Orbit documentary
8. **Success:** impressions · CTR · AVD · APV · session time · returning viewers · Browse/Suggested/Search
9. Canonical: `00_Brand/Channel-Setup/YOUTUBE_GROWTH_SYSTEM_V2.md` · `OMNI_LONGFORM_PLAYBOOK.md` · `RETENTION_AND_GROWTH_LOCKED.md`

Do not redesign the brand. Do not spend Veo/Omni credits or lock VO until pre-build audit + script ≥90 are signed off for new episodes.
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
            "ORBIT_LONGFORM_MINUTES": "7-9",
            "ORBIT_GROWTH_SYSTEM": "v2",
            "ORBIT_CG_ENGINE": "aistudio-veo-world-omni-orbit",
            "ORBIT_VO_ENGINE": "elevenlabs",
        },
        "additional_context": CONTEXT,
    }
    sys.stdout.write(json.dumps(out))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
