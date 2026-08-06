#!/usr/bin/env python3
"""Locked Orbit channel voice — British Ben Orbit Narrator (IVC).

Import these constants in every VO generator. Do not swap voice_id without an
explicit channel-voice change request.
"""
from __future__ import annotations

VOICE_NAME = "Ben Orbit Narrator"
VOICE_ID = "kDch6ACCIpqgQ0NsU9kk"
VOICE_ACCENT = "British (Ben IVC)"
MODEL_ID = "eleven_v3"

# Production lock (V003 / V004)
VOICE_SETTINGS = {
    "stability": 0.34,
    "similarity_boost": 0.78,
    "style": 0.42,
    "speed": 1.04,
    "use_speaker_boost": True,
}

DESCRIPTION = (
    "Warm, articulate British educational narrator with calm authority, "
    "cinematic curiosity and restrained mystery. Quietly dramatic — never "
    "theatrical, never trailer-like."
)

# Append to every Flow / AI Studio Veo / Seedance prompt (never EL Image & Video for new CG).
# Video models often invent American narration — never use that audio.
# Channel VO = ElevenLabs Ben Orbit Narrator only (VOICE_ID above).
# Default CG engine: orbit_flow_veo_ui.py (Ultra Flow). API = last-resort only.
CG_SILENT_AUDIO_BLOCK = (
    "SILENT PICTURE ONLY: no dialogue, no narration, no voiceover, no spoken "
    "words, no lip sync speech, no American or any-language talking. No announcer. "
    "Mute or ambient space soundscape only if the model requires an audio track. "
    "Channel voiceover is added later in edit (British Ben Orbit Narrator)."
)

CG_PREFACE = (
    "Premium cinematic 3D animation, educational space documentary. Soft warm "
    "key light on Orbit, cool scientific accents, shallow depth of field, "
    "continuous subtle hover. Full character motion — not a still with light "
    "wiggle. " + CG_SILENT_AUDIO_BLOCK + " "
)
