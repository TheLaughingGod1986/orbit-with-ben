# Orbit With Ben — studio

Production repo for **Orbit With Ben** ([@OrbitWithBen](https://www.youtube.com/@OrbitWithBen)): animated space storytelling with Orbit, a small orange robot, and Ben's British narration. Wonder, not dread.

**Agents and new collaborators: start with [`AGENTS.md`](AGENTS.md).** It lists the docs in force, the commands, where Ben signs off, and what never to do.

| Need | Go to |
|---|---|
| What to make, the week, hooks, the four-week test | `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md` |
| How to build and ship a long or a Short | `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` |
| Titles and thumbnails | `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` |
| Latest numbers | `00_Brand/Channel-Setup/audits/weekly/<date>/REPORT.md` (every Monday) |
| Why views were low, and the fixes | `00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md` |
| Housekeeping and what's next | `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md` |
| Old docs, rules, scripts and audits | `_archive/` (history only) |

## Repo map

```
AGENTS.md                     Start here (any agent)
00_Brand/
  Brand-Guidelines/           Brand voice and look
  Channel-Setup/              Docs in force, templates, ideas, backlog
    tools/                    Shorts ship gate, thumbnail builders + preview, weekly audit
    could-orbit-survive/      Wednesday test format + test log
    audits/                   Current audits, weekly reports, gate data
    Meta/ Threads/ TikTok/ social/   Social mirror ops (TikTok paused)
01_Orbit-Character/           Canonical Orbit stills and animation masters
02_Video-Projects/NNN_Slug/   One folder per film (start from _template_NNN_Episode-Slug)
04_Audio/tools/               VO settings (orbit_voice.py), Veo helper
07_Content-Ops/               Ops app + CLIs: script review, episode gate, YouTube upload, retitle
docs/                         Tech notes (Veo CG, affiliate, analytics, playback fixes)
scripts/                      Desktop Studio helpers for Studio-only jobs
_archive/                     Superseded material, kept for history
```

## Content Ops quick start

```bash
cd 07_Content-Ops
cp .env.example .env      # fill in locally; never commit secrets
npm install
npm run dev
```

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
| **`raw`** | Straight out of the generator (AI Studio Veo/Omni), byte-for-byte as downloaded. | **Never edited. Never deleted. Never renamed after download.** Every generation is kept, including the rejects — they are the evidence behind the review scores and they cost credits to produce. |
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
