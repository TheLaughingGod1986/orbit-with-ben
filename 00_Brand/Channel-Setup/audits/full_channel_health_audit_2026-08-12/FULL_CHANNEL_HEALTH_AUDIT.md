# Full channel health audit — 2026-08-12

**Mode:** read-only discovery (no visibility/schedule mutations in this pass)  
**Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`)  
**Captured:** live YouTube Data API uploads playlist + Studio Shorts draft filter  
**Branch:** `cursor/full-channel-health-audit-555c`

---

## Executive verdict

```text
CHANNEL NEEDS TARGETED REPAIRS — NOT CATALOGUE-HEALTHY
```

Canonical “public by now” Shorts are present. The serious problems are:

1. **Two accidental-early Shorts are public again** (should stay private)
2. **Four hold/obsolete/duplicate IDs are scheduled** (should not air)
3. **Exoplanets Shorts were re-uploaded** — Aug 7 calendar IDs are stale (replacements are correctly scheduled)
4. **Two “reserve” exo Shorts are live-scheduled** despite `reserve: true` in production index

Blank-thumb crisis from earlier looks **mostly resolved** for the two fixed IDs; no additional public/scheduled Shorts failed the visual blankish test.

---

## Live inventory (API)

| Bucket | Count |
|--------|------:|
| Uploads playlist items | 36 |
| Shorts | 32 |
| Longs | 4 |
| Public Shorts | **9** |
| Scheduled Shorts | 14 |
| Private Shorts | 9 |
| Public longs | 2 |
| Scheduled longs | 2 |
| Studio Draft filter (Shorts) | **empty** |

### Public Shorts (9)

| ID | Title | Expected? |
|----|-------|-----------|
| `1HuV8o3gOss` | Why Haven't We Found Aliens Yet? | ✅ canonical |
| `KcKBixwmcV4` | Why the First Alien Clue Might Be a Pattern… | ✅ canonical |
| `JRfhE6yWom4` | Why This Line Is a Point of No Return | ✅ canonical |
| `L2OFjL4neOo` | Falling In Wouldn't Feel Like Falling | ✅ canonical |
| `tUAdhOnMW2g` | Time Appears to Stop at a Black Hole | ✅ canonical |
| `svYOx07OrIM` | Would You Look Back? | ✅ canonical (fired) |
| `B2STcIAF1lY` | What You Would See Falling Into a Black Hole | ✅ canonical (fired) |
| `dPMJQp2gMNc` | Space Is Rude About Distance | ❌ **UNEXPECTED PUBLIC** |
| `rFJoOdQAc9c` | Don't Look Up: The Zoo Hypothesis | ❌ **UNEXPECTED PUBLIC** |

Previous unexpected superseded publics `z-DLqoSoEBo` / `UWwNKYf_aU8` are **gone** from the API (deleted) — good.

### Public / scheduled longs

| ID | State | Notes |
|----|-------|-------|
| `Mo93x0fxB1Q` | public | Fermi ✅ |
| `3xrxdmaOwJI` | public | BH ✅ — live title now *Time Dilation Near Black Holes: Observer vs. Reality* (title drift vs older package name) |
| `b8-X_FyJnHM` | scheduled `2026-08-13T17:00:00Z` | Exo long ✅ |
| `tfTkMdE7qqw` | scheduled `2026-08-20T17:00:00Z` | JWST long ✅ |

---

## P0 — fix with explicit approval

### A. Unexpected public (privatize candidates)

| ID | Title | Why |
|----|-------|-----|
| `dPMJQp2gMNc` | Space Is Rude About Distance | Accidental-early KEEP_PRIVATE hold — public again |
| `rFJoOdQAc9c` | Don't Look Up: The Zoo Hypothesis | Accidental-early KEEP_PRIVATE hold — public again |

**Recommended action:** `public → private` one-at-a-time after you confirm. Do **not** bulk-change.

### B. Should not be scheduled (clear `publishAt` → private)

| ID | Title | Scheduled | Why |
|----|-------|-----------|-----|
| `icedH_gK8JE` | What Your Eyes Would See | 19 Aug 2026 10:30Z | BH **reserve** / legacy hold |
| `gPCpMsB0w2E` | Is the Universe Older Than We Thought? | 28 Aug 2026 11:30Z | **16→13 obsolete** |
| `YsyPMhNmHMk` | The Discovery That Doesn't Add Up | 1 Sep 2026 11:30Z | **16→13 obsolete** |
| `8DxCTXUlw74` | Where Is Everybody? | 3 Sep 2026 10:30Z | 20s **historical duplicate** of Fermi short |

If these fire, they will compete with the canonical calendar and re-open the duplicate problem.

---

## P1 — registry / calendar / decision

### Exoplanets retention reuploads (healthy live schedule, stale Aug 7 calendar)

| Slot | Old approved ID | Live scheduled ID | Live `publishAt` |
|------|-----------------|-------------------|------------------|
| Glass rain | `ho9VJxp7f3A` (private) | `SC2WGTl_V5Q` | 2026-08-13T19:00:00Z |
| Diamond | `aoR-dA_g7eI` (private) | `M-VN84HCNls` | 2026-08-14T10:30:00Z |
| Three suns | `6QFGAFZk264` (private) | `nAZRIBm5wJw` | 2026-08-15T10:30:00Z |
| Hottest nights | `eOOFVrJ2Ojc` (private) | `tEOHYQbcgOw` | 2026-08-16T10:30:00Z |

Production `SHORTS_UPLOAD_INDEX.json` already points at the new IDs.  
**Fix:** update `YOUTUBE_CANONICAL_REGISTRY` + approved calendar references — not a publish emergency.

### Reserve shorts that are live-scheduled (decision needed)

| ID | Title | Live schedule | Index |
|----|-------|---------------|-------|
| `OlwENQcY-jg` | Eyeball / Giant Eye | 17 Aug 10:30Z | `reserve: true` but `status: scheduled` |
| `QRi6Dxq0hz0` | Could Any of These Alien Worlds Host Life? | 18 Aug 10:30Z | `reserve: true` but `status: scheduled` |

Either **accept** as an expanded exo week, or **unschedule** back to private hold. Index is internally inconsistent.

---

## Thumbnails

| Check | Result |
|-------|--------|
| `nAZRIBm5wJw` / `KcKBixwmcV4` custom covers (earlier fix) | Present / OK |
| Visual blankish scan of all Short `hqdefault` probes | **No public/scheduled blankish hits** |
| Byte-size “WEAK” heuristic | **Noisy** for letterboxed Shorts — ignore as primary signal |
| Private superseded `6QFGAFZk264` | Tiny auto-thumb only (OK to ignore) |

Studio mobile may still cache old greys — pull-to-refresh after CDN settles.

---

## What looks healthy

- All 7 expected canonical publics are public (BH/Alien cluster through today’s slot)
- Exo long + JWST long remain correctly scheduled
- Draft filter empty
- No overdue canonical private for the current expected-public set
- Prior unexpected public superseded IDs removed from catalogue

---

## Recommended next actions (approval gate)

1. **Privatize** `dPMJQp2gMNc`, `rFJoOdQAc9c`
2. **Unschedule** `icedH_gK8JE`, `gPCpMsB0w2E`, `YsyPMhNmHMk`, `8DxCTXUlw74`
3. **Decide** on `OlwENQcY-jg` + `QRi6Dxq0hz0` (keep schedule vs reserve)
4. **Refresh registry/calendar** to retention exo IDs (`SC2WGTl_V5Q`, `M-VN84HCNls`, `nAZRIBm5wJw`, `tEOHYQbcgOw`)
5. Optional: confirm BH long title change is intentional

---

## Evidence

- `AUDIT_SUMMARY.json` — raw API audit
- `TRIAGED_FINDINGS.json` — P0/P1 triage
- `api/LIVE_CATALOGUE.json` — full row dump
- `thumbs/` — hq probes
- `screenshots/` — Studio pages
- Script: `07_Content-Ops/scripts/youtube-full-channel-health-audit.ts`
