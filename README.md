# Orbit — YouTube Production Workspace

Production workspace for **Orbit with Ben** (`@OrbitWithBen`) — a faceless
animated science storytelling channel. Feel: *Pixar meets space documentary.*

Orbit is a small hovering robot: rounded orange body, black faceplate, cream
expressive eyes, a single glowing antenna, and two side arms — *a tiny robot
asking the biggest questions in the universe.*

**Creative director system:** `00_Brand/CHANNEL_BUILD_SYSTEM.md`  
**Live channel:** `00_Brand/Channel-Setup/CHANNEL_READY.md`  
**YouTube Growth System v2 (canonical):** `00_Brand/Channel-Setup/YOUTUBE_GROWTH_SYSTEM_V2.md`  
**Publishing & Shorts strategy:** `00_Brand/Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`  
**Publish schedule:** `00_Brand/Channel-Setup/OPTIMAL_PUBLISH_SCHEDULE.md` · `CHANNEL_PUBLISH_CADENCE.md`  
**Latest audit:** `00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-08-01_PM.md`  
**Flywheel / release:** `CONTENT_FLYWHEEL_TEMPLATE.md` · `RELEASE_WEEK_CHECKLIST.md`  
**Video backlog:** `00_Brand/Channel-Setup/VIDEO_BACKLOG.json`  
**Long-form quality gate (8–12 min · cold open · VO–picture):** `00_Brand/Channel-Setup/LONGFORM_STORY_AND_VO_PICTURE_GATE.md`  
**CG = Google AI Studio** — Veo world / Omni Orbit-only (`OMNI_LONGFORM_PLAYBOOK.md` · `docs/GEMINI_VEO_CG.md`) · **VO = ElevenLabs** Ben Orbit Narrator  

**Pre-build vidIQ audit (blocking before gen):** `00_Brand/Channel-Setup/PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
**Retention & growth (locked going forward):** `00_Brand/Channel-Setup/RETENTION_AND_GROWTH_LOCKED.md`  
**Script reviewer (≥90):** `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
**Episode gate:** `cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<slug>`  
**Next brief:** `cd 07_Content-Ops && npm run brief:next -- --file metrics.json`  
**Affiliate monetisation (Content Ops):** `07_Content-Ops/docs/AFFILIATE_MONETISATION_SYSTEM.md` · `/affiliate`  
**New episode scaffold:** `02_Video-Projects/_template_NNN_Episode-Slug/`  
**Cursor hooks:** `.cursor/hooks.json` (session checklist + pre-gen reminder)  
**Shorts mirrors:** TikTok `Channel-Setup/TikTok/AUTO_POST.md` · Meta (IG+FB) `Channel-Setup/Meta/AUTO_POST.md`  
**Playback lag (smooth audio, glitchy picture):** `docs/PLAYBACK_LAG_FIX.md` — remaster CFR then Studio **Replace** (keeps views)

This repository holds every asset for the channel — the character bible, the
per-video projects, reusable animation and audio libraries, and final exports.

---

## Purpose

1. Keep **one canonical visual definition of Orbit** so the character never
   drifts between videos.
2. Build a **reusable library** of Orbit animation clips (hover, talking,
   reactions, outros) that can be dropped into any future video.
3. Keep raw AI generations, chosen takes, and polished masters clearly separated
   and never confused with each other.

---

## Directory map

```
Orbit-YouTube/
├── 00_Brand/                       Channel identity
│   ├── Logos/                      Channel logo, watermark, endcards
│   ├── Fonts/                      Licensed font files
│   ├── Colour-Palette/             Swatches, hex reference
│   ├── Thumbnails/                 Reusable thumbnail templates
│   └── Brand-Guidelines/           Written brand + voice rules
│
├── 01_Orbit-Character/             THE CHARACTER BIBLE
│   ├── 01_Master-References/       PROTECTED. Canonical character sheets.
│   ├── 02_Transparent-PNGs/        Cut-outs with alpha for compositing
│   ├── 03_Expressions/             curious · amazed · concerned · playful
│   ├── 04_Poses/                   front · side · pointing · waving
│   ├── 05_Seedance-References/     Working copies fed to the video model
│   └── 06_Animation-Exports/       POLISHED REUSABLE MASTERS
│       ├── hover/                  Idle / floating / intro clips
│       ├── talking/                Explaining clips for use under narration
│       ├── reactions/              Thinking, surprised, emotional beats
│       └── outros/                 Goodbye / fly-away endings
│
├── 02_Video-Projects/              One folder per video
│   └── 001_Will-We-Ever-Meet-Aliens/
│       ├── 01_Script/              Script drafts, final read script
│       ├── 02_Voiceover/           Recorded / generated narration
│       ├── 03_Seedance-Prompts/    Scene prompt sheets for this video
│       ├── 04_Generated-Clips/     Raw → selected → polished, per clip
│       ├── 05_Music/               Licensed music for this video
│       ├── 06_Sound-Effects/       SFX for this video
│       ├── 07_Edit-Project/        CapCut / editor project files
│       ├── 08_Thumbnail/           Thumbnail working files
│       ├── 09_Final-Export/        Delivered master for this video
│       ├── 10_Shorts/              Shorts cluster (pillar-first)
│       └── 11_Distribution/        Social + Community flywheel
│
├── 03_Reusable-Assets/             Cross-video B-roll and motion graphics
│   ├── Space-Backgrounds/  Planets/  Galaxies/
│   ├── Transitions/  Titles/  Subscribe-Animations/
│
├── 04_Audio/                       Cross-video audio library
│   ├── ElevenLabs-Voice/           Generated narration masters
│   ├── Music-Library/              Licensed music
│   └── Sound-Effects/              SFX library
│
├── 05_Exports/                     Render outputs
│   ├── Long-Form/  Shorts/  Thumbnails/
│
├── 06_Published/                   Archive of what actually shipped
│   ├── YouTube-Long-Form/
│   └── YouTube-Shorts/
│
├── 07_Content-Ops/                 Multi-platform distribution dashboard
│   ├── prisma/                     SQLite data model + seed
│   ├── src/                        Next.js app (pipeline, calendar, analytics)
│   ├── content/exports/            Upload packages
│   └── scripts/                    CLI helpers
│
└── docs/                           Distribution strategy + workflow docs
```

### Multi-platform Content Ops

Local dashboard that turns one completed Orbit long-form into reusable short-form
distribution packs (YouTube Shorts, TikTok, Instagram Reels, Facebook Reels, X,
Threads) with platform-specific copy, calendars, CSV analytics, and manual
upload checklists.

```bash
cd 07_Content-Ops
cp .env.example .env
npm install
npx prisma migrate dev
npm run db:seed
npm run dev
```

Docs: `docs/MULTI_PLATFORM_STRATEGY.md` · `docs/CONTENT_WORKFLOW.md` ·
`docs/PLATFORM_SETUP.md` · `docs/ANALYTICS_IMPORT.md` ·
`docs/PUBLISHING_ADAPTERS.md` · `docs/TROUBLESHOOTING.md`

---

## Naming convention

```
project_scene_asset_version_status.extension
```

| Part | Meaning | Example |
|---|---|---|
| `project` | Video or character prefix | `orbit`, `aliens` |
| `scene` | Scene or clip identifier | `intro`, `scene-001` |
| `asset` | What the file actually is | `wave`, `earth-wide` |
| `version` | Zero-padded, always increments | `v01`, `v02` |
| `status` | `raw` · `selected` · `polished` | `raw` |

**Good:**

```
orbit_intro_wave_v01_raw.mp4
orbit_intro_wave_v02_raw.mp4
orbit_intro_wave_v02_selected.mp4
orbit_intro_wave_v02_polished.mp4
aliens_scene-001_earth-wide_v01_raw.mp4
aliens_voiceover-master_v01.wav
```

**Never use:**

```
final.mp4
final-final.mp4
new-final-2.mp4
```

Versions only ever go **up**. If v02 is bad, the next attempt is v03 — v02 is
never reused or overwritten.

---

## Raw · Selected · Polished

These three words are the backbone of the whole workspace. Every video file
carries exactly one of them.

| Status | What it is | Rules |
|---|---|---|
| **`raw`** | Straight out of Seedance, byte-for-byte as downloaded. | **Never edited. Never deleted. Never renamed after download.** Every generation is kept, including the rejects — they are the evidence behind the review scores and they cost credits to produce. |
| **`selected`** | A byte-identical copy of the one raw take that passed review. | Created by copying, never by moving. It marks the decision; it does not change the pixels. |
| **`polished`** | The selected take after trimming and cleanup in the editor. | This is the only file that gets used in an edit. Exported fresh — never overwritten in place. |

A polished master is then **copied** (not moved) into the matching
`01_Orbit-Character/06_Animation-Exports/` sub-folder so it becomes part of the
reusable library.

---

## Master assets — never overwrite

Files in these locations are **protected masters**:

- `01_Orbit-Character/01_Master-References/`
- `01_Orbit-Character/06_Animation-Exports/`
- every `*_raw.*` file in any `04_Generated-Clips/` folder

Rules:

1. **Never overwrite a master.** Write a new version number instead.
2. **Never resize, recompress or re-encode the master character sheet.** If a
   smaller file is needed, derive an optimised copy into
   `05_Seedance-References/` and leave the master untouched.
3. **Never delete a raw generation**, even an obviously failed one. Mark it
   rejected in `notes.md` and leave the file in place.
4. If a master genuinely must change, bump the version:
   `...-master-v01.png` → `...-master-v02.png`, keeping both.

---

## Generation workflow (Seedance)

1. Open Seedance and upload
   `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png`.
2. Use that uploaded image as the **only** canonical character reference.
3. Paste the clip prompt from the clip's `prompt.txt`.
4. Append the **mandatory consistency block** to every single generation:

   > Preserve Orbit exactly as shown in the uploaded reference image. Maintain
   > the same rounded orange body, black faceplate, cream expressive eyes,
   > single glowing antenna, side arms, proportions, materials and warm
   > animated-film visual style. Do not redesign the character. Do not add
   > limbs, fingers, facial features, clothing, text, logos or accessories.

5. Generate in **16:9 landscape**. Prefer subtle, controlled movement over
   exaggerated animation.
6. Generate **at least two versions** of each scene when credits permit.
7. Download every version. Save into the clip folder as
   `..._vNN_raw.mp4`, incrementing `NN`.
8. Record each version in the clip's `notes.md`.

### Review criteria

Check every generation for: character consistency · eye consistency · antenna
consistency · correct arm count · body shape and colour · unwanted morphing ·
camera stability · motion smoothness · background artefacts · accidental text or
logos · clean first and final frames · suitability for looping or editing.

**Reject outright** any clip with: extra limbs · faceplate distortion · eye
deformation · missing antenna · colour changes · body redesign · sudden camera
jumps · melting or morphing · unreadable generated text · clipped body parts.

---

## Editing workflow (polishing)

Editor: **CapCut Desktop** (installed). `ffmpeg` is also available for lossless
trims and format checks.

For each selected clip:

1. Import the selected raw generation.
2. Trim unstable opening or ending frames.
3. Remove frozen or malformed frames where practical.
4. Apply light stabilisation **only if required**.
5. Correct framing to 16:9.
6. Keep Orbit inside safe margins.
7. Avoid aggressive sharpening or filters.
8. **Do not add music or narration** at this stage — these are reusable clips.
9. Export **constant 30 fps** (`libx264`). Do not preserve AI-clip VFR and do not use VideoToolbox for delivery files — that is the social-playback stutter (smooth audio, glitchy picture). See `docs/PLAYBACK_LAG_FIX.md`.
10. Export a high-quality reusable master.

### Export format

| Setting | Value |
|---|---|
| Container | MP4 |
| Codec | H.264 |
| Resolution | 1920 × 1080 minimum |
| Frame rate | **30 fps constant (CFR)** — never “original” / VFR |
| Bitrate | High |
| Watermark | None |
| Audio | None, unless useful source audio is deliberately retained |

### Where polished masters go

| Clip | Destination |
|---|---|
| Introduction | `01_Orbit-Character/06_Animation-Exports/hover/` |
| Thinking | `01_Orbit-Character/06_Animation-Exports/reactions/` |
| Surprised | `01_Orbit-Character/06_Animation-Exports/reactions/` |
| Explaining | `01_Orbit-Character/06_Animation-Exports/talking/` |
| Ending | `01_Orbit-Character/06_Animation-Exports/outros/` |

Copy, don't move — the polished file stays in the clip folder too.

---

## Reference files

| File | Role | Notes |
|---|---|---|
| `01_Master-References/orbit-character-sheet-master-v01.png` | **Protected master** | 1448 × 1086 PNG. The full character bible: hero pose, four expressions, turnaround, side pose, palette. Set read-only (`chmod 444`). Never resize, recompress or overwrite. |
| `05_Seedance-References/orbit-seedance-reference-v01.png` | **Primary Seedance reference** | 896 × 1296. Derived crop of the hero figure only, upscaled 2×. Text-free. |
| `05_Seedance-References/orbit-seedance-reference-16x9-v01.png` | Landscape variant | 1920 × 1080, character centred on a flat `#111419` plate. Use if the tool wants the reference in the output aspect. |

### Why the Seedance reference is a crop, not the full sheet

The master sheet is deliberately dense with text and branding — the ORBIT
wordmark, the tagline, four expression labels, PALETTE / TURNAROUND / SIDE POSE
headings, the "brand in use" panel and the footer strip. That is correct for a
character bible and wrong for a video-model reference.

Every clip prompt ends *"No redesign, extra limbs, text, logos or watermark."*
Feeding a text-heavy, multi-panel sheet to an image-to-video model works
directly against that instruction: models tend to carry layout elements from the
reference into the output, and the two likely failure modes are garbled
pseudo-text bleeding into frames and the model rendering a *grid of several
Orbits* instead of one hovering character.

The derived crop isolates a single, complete, text-free Orbit — antenna, both
side arms, hover glow — which is exactly what the prompts describe.

**Known limitation:** the hero figure occupies only ~450 px of the source sheet,
so the crop is upscaled and detail-limited. If character fidelity proves weak in
generation, the fix is a high-resolution render of the hero pose alone, saved as
`orbit-seedance-reference-v02.png`.

## Current status

Folder structure, prompt sheets, review scaffolding and both reference files are
in place. Next step is Seedance generation — see
`02_Video-Projects/001_Will-We-Ever-Meet-Aliens/04_Generated-Clips/animation-review.md`.
