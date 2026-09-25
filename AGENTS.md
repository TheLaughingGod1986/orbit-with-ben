# AGENTS.md — Orbit With Ben studio

Read this first, whatever agent you are (Cursor, Claude Code, Codex or others). It says what this repo is, which docs are in force, and what never to do.

**The channel:** Orbit With Ben (`@OrbitWithBen`, `UC_esArsDKd3GJvOkeO0DUog`). Animated space storytelling with Orbit, a small orange robot, and Ben's British narration. Wonder, not dread.

**The job:** build films that hold people. The channel grows on Shorts stayed-to-watch and on long-form search. See `00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md` for why.

## Docs in force (in order of precedence)

When two docs disagree, the one higher in this list wins. Anything not listed here, and everything in `_archive/`, is history only. Don't follow it.

1. `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`: what to make, the week, Short and long hooks, the first two seconds, the four-week test (12 Oct – 6 Nov 2026).
2. `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md`: title shapes, thumbnail rules, frame 0 as the Shorts thumbnail.
3. `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`: how to build and ship: topic, script, voice, picture, Orbit, assembly, upload, measure, affiliate, social, sign-offs.
4. `00_Brand/Channel-Setup/YOUTUBE_GROWTH_AND_POLICY.md`: retention, CTR and policy basics.
5. `00_Brand/Channel-Setup/CHANNEL_AUTHORITY.md`: picture matches the words, same Orbit, voice present, weekly promise.
6. `00_Brand/Channel-Setup/YOUTUBE_FRAME_SIZES.md`: sizes.
7. `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md`: housekeeping to do now, and what waits until after the test.

## Where things live

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/`, `ideas/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `weekly_public_audit.py`, thumbnail builders |
| `00_Brand/Channel-Setup/could-orbit-survive/` | The Wednesday test format, three scripts, `TEST_LOG.md` |
| `00_Brand/Channel-Setup/audits/` | Current audits, `weekly/` reports, `shorts_open_library/` (gate data) |
| `00_Brand/Channel-Setup/{Meta,Threads,TikTok,social}/` | Social mirror ops. TikTok is paused (`TikTok/TIKTOK_UPLOAD_BLOCK.json`). |
| `01_Orbit-Character/` | Canonical Orbit stills (`05_Seedance-References/orbit-seedance-reference-16x9-v01.png`) |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_gemini_veo.py` |
| `07_Content-Ops/` | Next.js ops app and CLIs: script review, episode gate, YouTube package upload, retitle, analytics |
| `scripts/` | Desktop Studio CDP helpers for Studio-only jobs (thumbnail covers) |
| `_archive/` | Superseded docs, rules, one-off scripts and old audits. **Ignore unless asked.** |

## Commands

```bash
cd 07_Content-Ops && npm run review:script -- --file <script.md>          # long script must score ≥90
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb.jpg> --out <sheet.jpg>
cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py
```

The YouTube scripts need `07_Content-Ops/.env`: `DATABASE_URL`, `ORBIT_TOKEN_ENCRYPTION_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`. Never print or commit their values.

## Stop and ask Ben at each of these points

1. Topic
2. Long script (after it reaches 90)
3. Short scripts
4. Voice
5. Moving picture (never judge from stills)
6. Thumbnails
7. Anything that goes public, is renamed, or is deleted

## Never

- **Uploads:**
  - Swap the file on an existing YouTube id.
  - Re-upload an idea that already went public.
  - Delete a video. The old id goes private instead.
- **Publishing:**
  - Premiere a long.
  - Air more than one Short a day.
  - Ship a Short of 40 s or more.
  - Ship a silent or near-silent file.
  - Put Orbit at frame 0 of a Short or on any thumbnail.
- **Titles:** hashtags, series suffixes, hedged claims ("We may have…"), fear framing, or a title that copies an existing public video.
- **Studio:** add a pinned comment to a Short, or a `/go/` link on a Short; use `/go/` on a long that doesn't name the product in the film.
- **Generation:**
  - Use Kling, Seedance or ElevenLabs Image & Video.
  - Omni the whole film or world B-roll.
  - Use a video model's speech as VO.
  - Use any voice other than Ben Orbit Narrator.
- **TikTok:** upload or retry while it's paused.
- **Secrets:** commit or print them.

## Changing the rules

Change the doc in force (1–7 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`.
