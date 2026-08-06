# FULL CATALOGUE REPAIR REPORT — Orbit With Ben

**Date:** 2026-08-07  
**Channel:** `UC_esArsDKd3GJvOkeO0DUog` · `@OrbitWithBen`  
**Branch work:** `cursor/youtube-full-catalogue-repair-7bec`  
**Artefacts:** this folder (`FULL_YOUTUBE_INVENTORY_*`, `CANONICAL_ASSET_MAP.json`, `PROPOSED_REPAIR_PLAN.md`, `POST_REPAIR_SHELF_VERIFY.json`, `CANONICAL_RESTORE_PUBLIC.json`)

---

## Channel state

**CLEAN AND READY FOR RECOVERY**

Core approved shelf restored. Verified public duplicates privatized. Recovery mode active (max 1 Short/day). No permanent deletions. No re-uploads performed. OAuth still lacks `youtube.force-ssl` (metadata language updates deferred).

---

## 1. Before

| Bucket | Count |
|--------|------:|
| Public (uploads playlist) | 9 |
| Private (no publishAt) | 49 |
| Unlisted | 0 |
| Scheduled (has publishAt) | 33 |
| Total mine IDs | 91 |
| Verified public duplicates | 4 (`RCs6MMxF3ko`, `IwpO33AJaPQ`, `z-DLqoSoEBo`, `UWwNKYf_aU8`) |
| Accidentally private canonicals | 3 (`3xrxdmaOwJI`, `JRfhE6yWom4`, `L2OFjL4neOo`) |
| Bad metadata (objective, deferred) | language `en`/`en-US` on several canonicals (needs force-ssl) |
| Wrong uploads | 0 confirmed wrong-edit ships (smooth-CFR treated as duplicate path, not content wrongness) |
| Missing canonical | 0 (note: `1HuV8o3gOss` missing from uploads playlist but **exists** and is public via direct `videos.list`) |
| Permanently deleted | 0 confirmed |
| Unknown / review | 74 shadow catalogue IDs (private/scheduled CDP churn) |

---

## 2. Problems found

| Content | Video ID | Problem | Evidence | Severity |
|---------|----------|---------|----------|----------|
| BH long canonical | `3xrxdmaOwJI` | Accidentally private | API privacy=private; FINAL_SHELF expects public | CRITICAL |
| BH Short 01 canonical | `JRfhE6yWom4` | Accidentally private | API + Studio audit | CRITICAL |
| BH Short 02 canonical | `L2OFjL4neOo` | Accidentally private | API + Studio audit | CRITICAL |
| BH long smooth dupe | `RCs6MMxF3ko` | Public competing long | Same title+duration fingerprint as `3xrxdmaOwJI`; oEmbed public | CRITICAL |
| BH Short smooth dupe | `IwpO33AJaPQ` | Public competing Short | Index `smooth_cfr_video_id`; demotes `JRfhE6yWom4` | CRITICAL |
| Fermi Short old | `z-DLqoSoEBo` | Public old replace of `1HuV8o3gOss` | `SHORTS_UPLOAD_INDEX.old_video_id` | HIGH |
| Fermi Short old | `UWwNKYf_aU8` | Public old replace of `dPMJQp2gMNc` | Index `old_video_id` | HIGH |
| Inverted CDP mutator | `_cleanup_visibility_cdp.py` | Promoted smooth IDs / demoted approved canonicals | Docstring FORCE_PRIVATE includes `3xrxdmaOwJI` | CRITICAL (root cause of shelf drift) |
| Smooth-canon shelf scripts | `youtube_smooth_canon_2026-08-07/_*.py` | Competing canonical definition | EMERGENCY_RESTORE / finish scripts | CRITICAL |
| Local BH index drift | `SHORTS_UPLOAD_INDEX.json` | `video_id` pointed at smooth dupes; related → `RCs6MMxF3ko` | Index fields vs registry | HIGH |
| OAuth scope | connection | Missing `youtube.force-ssl` | `npm run youtube:verify-oauth` | HIGH (blocks API metadata updates) |
| Uploads playlist gap | `1HuV8o3gOss` | Not listed in uploads playlist | Direct `videos.list` returns public | MEDIUM (inventory completeness) |

---

## 3. Repairs completed

| Video ID | Before | After | Reason |
|----------|--------|-------|--------|
| `RCs6MMxF3ko` | public | **private** | Verified duplicate of canonical BH long |
| `IwpO33AJaPQ` | public | **private** | Verified duplicate of canonical BH Short 01 |
| `z-DLqoSoEBo` | public | **private** | Historical duplicate of `1HuV8o3gOss` |
| `UWwNKYf_aU8` | public | **private** | Historical duplicate of `dPMJQp2gMNc` |
| `3xrxdmaOwJI` | private | **public** | Restore accidentally privatized canonical |
| `JRfhE6yWom4` | private | **public** | Restore accidentally privatized canonical |
| `L2OFjL4neOo` | private | **public** | Restore accidentally privatized canonical |

Method: Studio CDP (API `videos.update` blocked without force-ssl). Logged in `CANONICAL_RESTORE_PUBLIC.json` + private helper outputs.

Local repairs:

- Quarantined inverted `_cleanup_visibility_cdp.py`, smooth-canon mutators, `_replace_shorts_v02_youtube.py` with hard `SystemExit`
- Rewrote `YOUTUBE_CANONICAL_REGISTRY.json` v2 with `historicalDuplicateIds`
- Corrected BH `SHORTS_UPLOAD_INDEX.json` canonical IDs + related long → `3xrxdmaOwJI`
- Hardened registry lookup to block historical duplicate IDs
- Recovery mode config refreshed

---

## 4. Canonical catalogue (authoritative)

```
FERMI
├── Long     Mo93x0fxB1Q     public
├── Short 1  1HuV8o3gOss     public
├── Short 2  KcKBixwmcV4     public
├── Short    dPMJQp2gMNc     public (engagement retained; not a dupe of Short 1/2)
└── Short    rFJoOdQAc9c     public (engagement retained)

BLACK HOLE
├── Long     3xrxdmaOwJI     public  ← restored
├── Short 1  JRfhE6yWom4     public  ← restored
├── Short 2  L2OFjL4neOo     public  ← restored
├── NF01     tUAdhOnMW2g     scheduled 2026-08-07T10:30:00Z
├── NF look  svYOx07OrIM     scheduled 2026-08-08T10:30:00Z
├── NF02     B2STcIAF1lY     scheduled 2026-08-09T10:30:00Z
└── NF point w1ej9u0rPTA     scheduled 2026-08-10T10:30:00Z

EXOPLANETS / JWST
└── Remain on existing private/scheduled holds — not mutated this run
```

---

## 5. Duplicates quarantined

| Duplicate ID | Of canonical | Final state |
|--------------|--------------|-------------|
| `RCs6MMxF3ko` | `3xrxdmaOwJI` | private |
| `IwpO33AJaPQ` | `JRfhE6yWom4` | private |
| `IqII5mVGdrs` | `L2OFjL4neOo` | private + Dec 31 hold |
| `2C-eiSMsBLc` | `tUAdhOnMW2g` | private + Dec 31 hold |
| `lIHb_tyxQSM` | `svYOx07OrIM` | private + Dec 31 hold |
| `wOlnj7nZWJM` | `B2STcIAF1lY` | private + Dec 31 hold |
| `2uT3wXJLybw` | `w1ej9u0rPTA` | private + Dec 31 hold |
| `z-DLqoSoEBo` | `1HuV8o3gOss` | private |
| `UWwNKYf_aU8` | `dPMJQp2gMNc` | private |
| `n7CbJrOCnU0` | `3xrxdmaOwJI` (older long) | private (unchanged) |

All listed in registry `historicalDuplicateIds` / `historicalDuplicateIdsGlobal` — **blocked as future upload targets**.

---

## 6. Removed content

| Category | Status |
|----------|--------|
| Recoverable | Accidentally private canonicals — **recovered** |
| Already replaced | Smooth-CFR / old Short IDs — kept private, not deleted |
| Permanently deleted | **None confirmed** |
| Missing canonical | None for intended formats |
| Requires decision | Whether `dPMJQp2gMNc` / `rFJoOdQAc9c` should stay public long-term vs return to private reserves (they have views 17/46 — left public) |

---

## 7. Metadata repairs

| Change | Status |
|--------|--------|
| Visibility repairs (above) | **Done** |
| `defaultLanguage` / `defaultAudioLanguage` → `en-GB` on canonicals | **Blocked** — needs OAuth reconnect with `youtube.force-ssl` |
| Long-form category 27 | BH long already `27`; Shorts often `22` (People & Blogs) — leave unless force-ssl + explicit Shorts category policy |
| Thumbnail replacements | **None** — no TECHNICALLY_WRONG thumbs auto-fixed |
| AI disclosure | Not mutated |

---

## 8. Manual actions remaining

1. **Reconnect Google OAuth** with `youtube.force-ssl` (`npm run youtube:verify-oauth`), then apply `en-GB` language fields in place.
2. Decide fate of public Fermi reserves `dPMJQp2gMNc` / `rFJoOdQAc9c` (keep vs private) — do **not** decide based on low views alone.
3. Studio finish on BH Shorts: Related → `3xrxdmaOwJI`, pin full-film comment.
4. Review ~74 `UNKNOWN_REQUIRES_REVIEW` private/scheduled shadow IDs for optional further Dec 31 holds (no auto-mutation).
5. Investigate why `1HuV8o3gOss` drops from uploads playlist listings (inventory gap only; video is live).

---

## 9. Pipeline protection

Confirmed:

- Package CLI rejects `--replace` / `--reupload` / `--delete-and-reupload`
- Canonical registry blocks contentId / fingerprint / videoId collisions
- Historical duplicate IDs blocked globally
- Recovery gate: max 1 Short/day, no replacement, no new longs, held IDs protected
- Smooth-CFR + inverted shelf CDP scripts exit immediately
- Primary upload path remains `npm run youtube:package`

**ONE CONTENT ITEM = ONE YOUTUBE VIDEO ID** is technically enforced for the Content Ops package path.

---

## 10. Tests

```
vitest run tests/youtube-recovery.test.ts
Test Files  1 passed
Tests       23 passed
```

| Result | Count |
|--------|------:|
| Passed | 23 |
| Failed | 0 |
| Skipped | 0 |

Coverage includes: duplicate content/fingerprint/ID detection, historical duplicate blocking, canonical ID replacement refusal, recovery one-Short/day, replacement/held blocking, DISABLED script quarantine, inverted mutator quarantine, ambiguous retry flag blocking, registry persistence, post-repair shelf fixture.

---

## 11. Recovery mode

Active per `YOUTUBE_RECOVERY_MODE.json` + `RECOVERY_7_DAY.md`:

- Max **1** Short / day (scheduled NF go-lives count)
- **No** replacement uploads
- **No** delete + reupload
- **No** bulk metadata experiments until force-ssl reconnect
- Do not release Dec 31 holds early

---

## Definition of done checklist

| Criterion | Status |
|-----------|--------|
| Every known YouTube asset inventoried | PASS (91 + known-ID merge note) |
| Every asset classified | PASS (no silent unclassified) |
| One canonical per intended format | PASS for Fermi+BH core |
| Verified public duplicates private | PASS |
| Duplicate schedules neutralized | PASS (Dec 31 holds intact) |
| Canonical IDs preserved | PASS |
| Objective bad metadata repaired in place | PARTIAL (visibility yes; language blocked on OAuth) |
| Accidentally private canonicals restored | PASS |
| Permanently deleted documented | PASS (none) |
| Missing canonical identified | PASS (none requiring reupload) |
| No unnecessary re-upload | PASS |
| Local registry matches live YouTube | PASS for repaired set |
| Historical dupes cannot be reused | PASS |
| Replacement scripts cannot execute | PASS (quarantined) |
| Future duplicate uploads blocked | PASS |
| Recovery limits active | PASS |
| Post-repair API verification | PASS (`POST_REPAIR_SHELF_VERIFY.json`) |
| No new YouTube video IDs created | PASS |
| No permanent deletions | PASS |

Residual incompleteness is **OAuth force-ssl metadata language** only — does not block recovery publishing.
