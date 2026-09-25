# Orbit Multi-Platform Content Distribution — Audit & Plan

**Date:** 2026-07-31  
**Channel:** Orbit with Ben (`@OrbitWithBen`)  
**Timezone:** Europe/London

---

## 1. Repository audit summary

### Current framework

This is a **file-based YouTube production workspace**, not an application monorepo.

| Layer | Reality |
|-------|---------|
| Web/app framework | **None** — no Next.js/React/API server |
| Automation stack | Python scripts (ffmpeg, Playwright Studio helpers) |
| Data store | Markdown + JSON files |
| Package manager | Node only appears inside Playwright vendor trees |

### Existing routes

No HTTP routes. Ops flow is folder + JSON driven.

### Existing database / local storage

| Source | Role |
|--------|------|
| `00_Brand/Channel-Setup/OPTIMAL_PUBLISH_SCHEDULE.json` | Canonical long + Shorts calendar |
| `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` | Topic backlog |
| Per-project `10_Shorts/SHORTS_INDEX.json` | Shorts cluster metadata |
| Per-project `10_Shorts/SHORTS_UPLOAD_INDEX.json` | Uploaded Shorts IDs/URLs |
| Per-project `11_Distribution/CONTENT_FLYWHEEL.md` | Social flywheel drafts |
| Per-project `11_Upload-Package/` | Titles, descriptions, checklists |

### Video metadata structure

Schedule items already encode: `key`, `type` (`long`/`short`), `title`, `hook`, `pillar`, `date_iso`, `time`, `iso`, `status`, `youtube_id`, `folder`.

Per-video folders follow:

```
02_Video-Projects/NNN_Title/
  01_Script/  02_Voiceover/  …  09_Final-Export/
  10_Shorts/  11_Upload-Package/  11_Distribution/
```

### Script generation features

Hand-authored Markdown masters in `01_Script/` (chapters, Orbit markers, B-roll notes). No LLM pipeline in-repo for clip planning.

### Export functionality

- Long masters: `09_Final-Export/`
- Vertical Shorts: `10_Shorts/06_Final-Exports/`
- Channel archives: `05_Exports/`, `06_Published/`
- Upload packages: titles, tags, schedule JSON, Playwright finish scripts

### Analytics / audit systems

No unified analytics DB. QC/ffprobe JSON and Studio result JSON exist per video. No cross-platform performance store.

### Design system

| Token | Hex |
|-------|-----|
| Primary Orange | `#FF7A24` |
| Soft Terracotta | `#C47A4E` |
| Cream | `#F5E8D2` |
| Deep Space | `#0A0C12` |
| Muted Blue | `#5A6E82` |
| Antenna Gold | `#FFC85A` |

Voice: calm documentary · wonder over hype · soft CTAs only.

### Folder structure (canonical)

```
00_Brand/  01_Orbit-Character/  02_Video-Projects/
03_Reusable-Assets/  04_Audio/  05_Exports/  06_Published/
```

---

## 2. Reusable components

- Publishing rules in `PUBLISHING_AND_SHORTS_STRATEGY.md` + `.cursor/rules/orbit-publishing-shorts.mdc`
- Schedule machine source: `OPTIMAL_PUBLISH_SCHEDULE.json`
- Flywheel template + aliens `CONTENT_FLYWHEEL.md`
- Shorts indexes + exported vertical MP4s for V001
- Brand colours / voice / CTA language
- Upload checklists under `11_Upload-Package/`

---

## 3. Risks & missing dependencies

| Risk | Mitigation |
|------|------------|
| No existing app stack | Add isolated `07_Content-Ops/` (Next.js + Prisma + SQLite) |
| No git remote in this environment | Local app + docs; commits only if git is initialised |
| Platform APIs unreliable / restricted | Manual publishing mode + adapter stubs |
| Existing cadence differs slightly from prompt defaults | **Preserve Orbit canonical schedule** (Thu 19:00 long; Short#1 21:00; Days2–7 12:30) and add cross-platform offsets |
| Must not break video production | Do not modify Seedance/edit builders; only extend |

---

## 4. Phased implementation plan

### Phase 1 — Foundation

- Scaffold `07_Content-Ops` (Next.js, TS, Tailwind, Prisma SQLite)
- Data model: LongFormVideo, ShortClip, PlatformPost, PerformanceMetric, ContentInsight, PlatformSettings, ContentTemplate
- Platform + schedule + content-rules config
- Seed “Will We Ever Meet Aliens?” + 4 sample clips
- Overview + pipeline dashboard

### Phase 2 — Distribution pack

- Create Distribution Pack workflow (clip proposals from script)
- Platform copy generation + templates
- Caption export (SRT/VTT/plain)
- Export package + upload checklists + manifest

### Phase 3 — Calendar & ops

- Publishing calendar (week/month)
- Schedule editing + status transitions
- Duplicate protection

### Phase 4 — Analytics

- CSV import + sample templates
- Performance dashboard + insight engine (data-gated)

### Phase 5 — Automation readiness

- PublishingAdapter interface + manual adapters
- Settings page (tokens via env only)
- Tests + docs + README update

---

## 5. Architecture placement

```
Orbit-YouTube/
├── 07_Content-Ops/          ← new local ops dashboard
│   ├── prisma/
│   ├── src/app/             ← dashboard UI
│   ├── src/lib/             ← content, platforms, analytics, publishing
│   ├── src/config/
│   ├── content/             ← templates + export staging
│   └── scripts/
├── docs/                    ← strategy + workflow docs
└── (existing production tree unchanged)
```
