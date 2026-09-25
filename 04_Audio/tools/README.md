# Orbit audio + packaging tools

Shared CLIs for ElevenLabs production audio and vidIQ title gates.

Auth: `ELEVENLABS_API_KEY` **or** Firebase bearer (same caches as VO generators —
`/tmp/elevenlabs_bearer.txt`, project `.elevenlabs_bearer`, Playwright profile).

| Endpoint | Bearer OK? | API key (`~/.config/elevenlabs/api_key`) |
|----------|------------|------------------------------------------|
| TTS / Music / STT | yes | yes |
| Sound generation (SFX) | **no** | **required** (same key as ElevenLabs MCP) |

The Cursor ElevenLabs MCP wrapper reads `~/.config/elevenlabs/api_key`. Our CLIs
use that file automatically (or `ELEVENLABS_API_KEY` / `ELEVENLABS_API_KEY_FILE`).

## Commands

### 1. SFX from script cues

Requires `ELEVENLABS_API_KEY` for `--generate` (Firebase bearer is not accepted on
`/v1/sound-generation`).

```bash
cd 04_Audio/tools

# Parse [SFX: …] tags → manifest
python3 generate_sfx_from_script.py \
  --script ../../02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/01_Script/exoplanets_script_master_v01.md \
  --out-dir ../../02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/06_Sound-Effects/generated_v01

# Generate (costs credits; needs API key)
export ELEVENLABS_API_KEY=…   # https://elevenlabs.io/app/settings/api-keys
python3 generate_sfx_from_script.py --script … --out-dir … --generate --duration 3
```

### 2. Music bed

```bash
python3 generate_music_bed.py \
  --project exoplanets \
  --script ../../02_Video-Projects/003_…/01_Script/exoplanets_script_master_v01.md \
  --out-dir ../../02_Video-Projects/003_…/05_Music \
  --length-ms 180000

python3 generate_music_bed.py … --generate   # costs credits
```

### 3. VO → captions (Scribe)

```bash
python3 transcribe_vo.py \
  --audio ../../02_Video-Projects/003_…/02_Voiceover/05_Master/<master>.mp3 \
  --out-dir ../../02_Video-Projects/003_…/02_Voiceover/06_Captions
```

Writes `.srt`, plain transcript, and raw JSON word timestamps.

### 4. vidIQ title score sheet

```bash
python3 vidiq_title_score_sheet.py \
  --project-dir ../../02_Video-Projects/004_JWST-Discoveries-That-Change-Everything
```

Opens/creates `11_Upload-Package/Titles/VIDIQ_TITLE_SCORE_SHEET.md`. Fill scores
in the vidIQ web app / extension (automation profile must be logged in).

### 5. Fix playback lag (VFR / VideoToolbox)

Smooth audio + stuttery picture on YouTube/Shorts/social is almost always a
variable-frame-rate delivery file (Shorts used `h264_videotoolbox`). Remaster
in place, then **Studio Replace** so view counts stay on the original video id.

```bash
python3 04_Audio/tools/test_orbit_cfr_delivery.py
python3 04_Audio/tools/fix_published_playback_lag.py --apply
python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py --dry-run
```

See `docs/PLAYBACK_LAG_FIX.md`.

## Pipeline slot

| Step | When | Tool |
|------|------|------|
| Title gate | Before VO lock | `vidiq_title_score_sheet.py` + live vidIQ |
| VO | After title lock | existing `_generate_vo_v01.py` |
| Captions | After VO master | `transcribe_vo.py` |
| SFX | During / before edit | `generate_sfx_from_script.py --generate` |
| Music bed | During / before edit | `generate_music_bed.py --generate` |

Package checklist: `00_Brand/Channel-Setup/templates/PRODUCTION_CHECKLIST_V2.md`

## Voice lock (British)

All long-form VO uses **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`) — Ben’s
British Instant Voice Clone. Constants: `orbit_voice.py`. Do not substitute
another ElevenLabs voice unless the channel voice is explicitly redesigned.

