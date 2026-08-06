# YouTube Channel Audit + Cleanup — Orbit With Ben

**Date (UTC):** 2026-08-06/07  
**Channel:** `UC_esArsDKd3GJvOkeO0DUog` · `@OrbitWithBen`  
**Artifacts:** this folder (`AUDIT_AND_CLEANUP.json`, `FINAL_SHELF_VERIFY.json`, `CLEANUP_VISIBILITY_*.json`, `HOLD_SCHEDULED_DUPES.json`)

---

## 1. Executive summary

Recent BH uploads showed **0 impressions while public/processed/searchable** because they were **indexed but not recommended**, amplified by **upload-pipeline instability**: CDP replace scripts created competing public longs, duplicate Shorts, demoted canonical Shorts, and same-slot scheduled collisions.

**Cleanup completed (API-verified):**

| Goal | Result |
|------|--------|
| Canonical public shelf (6) | **PASS** — Fermi long+2 Shorts, BH long+2 Shorts |
| Public dupes removed | **PASS** — `IwpO33AJaPQ`, `RCs6MMxF3ko` → private |
| Scheduled dupes neutralized | **PASS** — 5 IDs held to **2026-12-31T11:30:00Z** |
| Canonical NF01 schedule kept | **PASS** — `tUAdhOnMW2g` still `2026-08-07T10:30:00Z` |
| Replace scripts quarantined | **PASS** — `DISABLED__*.py` with hard `SystemExit` |
| API upload path hardened | **PASS** — Education category, notifySubscribers, en-GB, post-upload assert |

**Primary root cause:** duplicate-content / pipeline instability (not processing failure).

---

## 2. Technical evidence (API)

### Channel
- Joined 2026-07-27 · GB · `longUploadsStatus=allowed` · linked · not monetized  
- Stats after cleanup: **141** views · **1** sub · **6** public videos  
- Inventory earlier in audit: **91** mine IDs (massive CDP churn)

### Final shelf (`FINAL_SHELF_VERIFY.json`)

| ID | Role | Privacy | publishAt | Views |
|----|------|---------|-----------|------:|
| `Mo93x0fxB1Q` | Fermi long | public | — | 6 |
| `1HuV8o3gOss` | Fermi Short | public | — | 38 |
| `KcKBixwmcV4` | Fermi Short | public | — | 97 |
| `3xrxdmaOwJI` | BH long **canonical** | public | — | 0 |
| `JRfhE6yWom4` | BH Short **canonical** | public | — | 0 |
| `L2OFjL4neOo` | BH Short **canonical** | public | — | 1 |
| `IwpO33AJaPQ` | dupe Short | **private** | — | 0 |
| `RCs6MMxF3ko` | competing BH long | **private** | — | 0 |
| `2C-eiSMsBLc` | dupe NF01 | private | **31 Dec** | 0 |
| `IqII5mVGdrs` | dupe Falling In | private | **31 Dec** | 0 |
| `lIHb_tyxQSM` / `wOlnj7nZWJM` / `2uT3wXJLybw` | zero-tag replace batch | private | **31 Dec** | 0 |
| `tUAdhOnMW2g` | canonical NF01 | private | **7 Aug 10:30Z** | 0 |

### Processing (sampled canonical)
All canonical IDs: `uploadStatus=processed`, `processingStatus=succeeded`, `embeddable=true`, `madeForKids=false`, no `rejectionReason`.

### Indexing
Public IDs retrievable by ID, channel tabs, and title search; not age-restricted.  
**Impressions category:** indexed but not recommended (0 views on public BH despite process+search). Analytics impressions fields require Studio/Analytics API — `statistics.viewCount` used as hard proxy.

### OAuth gap
`videos.update` returned **403 ACCESS_TOKEN_SCOPE_INSUFFICIENT** (upload+readonly only). Cleanup used Studio CDP. **Reconnect Google with `youtube.force-ssl`.**

---

## 3. Root cause

**Primary:** Duplicate content signal contamination / upload pipeline instability.

| Factor | % | Evidence | Confidence |
|--------|--:|----------|------------|
| Duplicate / replace pipeline contamination | **45** | Competing public longs; public dupe Short→private long; demotion of canonical Shorts mid-flight; 28 fingerprint duplicate groups; 91 uploads | High |
| Cold start (1 sub, new channel) | **35** | Fermi Shorts *did* get seed (38/97); longs stay tiny; expected low but not forced 0 forever | High |
| Metadata inconsistency on replace batch | **12** | Zero-tag scheduled uploads; thinner BH Short descriptions | High |
| Recommendation delay | **5** | Possible &lt;48h lag; weaker given Fermi already seeded | Medium |
| Processing / not indexed | **3** | Rejected by API+search evidence | High |

---

## 4. Pipeline issues (severity)

| Severity | Issue | Status |
|----------|-------|--------|
| CRITICAL | CDP smooth-CFR replace scripts creating second public long + demoting canonical Shorts | **Quarantined** |
| CRITICAL | Public duplicate Short `IwpO33AJaPQ` CTA → private long | **Privatized** |
| CRITICAL | Same-slot scheduled duplicates (`2C-eiSMsBLc` vs `tUAdhOnMW2g`) | **Held 31 Dec** |
| HIGH | API cannot update visibility (missing force-ssl) | **Documented — reconnect required** |
| HIGH | Historical catalogue uploaded via CDP not API package | **Path hardened; use package CLI** |
| HIGH | 91 IDs / high upload frequency vs 1 sub | **Stabilization plan** |
| MEDIUM | category/language/notify inconsistency in adapter | **Fixed in adapter** |
| MEDIUM | No post-upload assert | **Added `assertYouTubeVideoState`** |
| LOW | Thumbnail/CTR | Deferred until impressions &gt; 0 |

---

## 5. Fix plan (done + remaining)

### Done this run
1. Privatized `IwpO33AJaPQ`, `RCs6MMxF3ko` (oEmbed + API verified).
2. Restored public `JRfhE6yWom4`, `L2OFjL4neOo`.
3. Held five replace-batch Shorts to 31 Dec 12:30 UK.
4. Quarantined four CDP replace/upload scripts with hard exit.
5. Hardened YouTube adapter: category **27**, `notifySubscribers`, `en-GB`, post-upload assert.
6. Manifest template flags: `oneVideoOneUpload`, category, language.

### Remaining (manual / next session)
1. **Reconnect YouTube OAuth** with `youtube.force-ssl` (Settings → Connections).
2. Studio finish on BH Shorts: Related → `3xrxdmaOwJI`, pin full-film comment, restore full package descriptions if thinned.
3. Confirm Studio → Channel status: phone verification, advanced features, no strikes.
4. Create playlist “Orbit’s Cosmic Journey”; add both public longs.
5. Do **not** run any `DISABLED__*` or new replace CDP jobs during the 7-day window.

---

## 6. Safe upload system (corrected design)

```
Package folder → npm run youtube:package (Data API)
  → privacy private + publishAt (if scheduled)
  → category Education (27), en-GB, tags, description, thumb
  → notifySubscribers only if immediate public
  → assertYouTubeVideoState (privacy/publishAt/tags)
  → Studio finish ONLY: ABC / pin / Related / end screen
```

**Forbidden**
- CDP as primary uploader
- Reupload to “replace” a live public ID
- Publishing a second ID with the same title+duration fingerprint while another is public/scheduled
- Private→public swap without demoting the old ID first via assert

---

## 7. Prevention rules

1. **ONE VIDEO = ONE UPLOAD** — one canonical ID per asset in `SHORTS_UPLOAD_INDEX` / package ledger.  
2. **Demote before ship** — old ID must be private (API assert) before new ID can be public/scheduled.  
3. **API primary** — `youtube:package` only; CDP only for Studio-only gaps.  
4. **Post-upload assert required** — fail the job if privacy/publishAt wrong.  
5. **No same-day multi-replace bursts** — max 1 new public Short/day in stabilization.  
6. **force-ssl connected** — required for cleanup automation.  
7. **Quarantine stickiness** — never rename `DISABLED__*` back without a written RFC.

---

## 8. 7-day stabilization plan

See `RECOVERY_7_DAY.md`.

---

## 9. Success indicators

| Checkpoint | Pass |
|------------|------|
| Public count = 6 (until next scheduled go-live) | yes now |
| No public duplicate title fingerprints | yes now |
| BH Short impressions &gt; 0 within 72h of clean shelf | monitor |
| No new uploads except scheduled canonical go-lives | required |
| After NF01 live: still only one “Time Appears…” public | required |
