# Orbit With Ben — YouTube Zero-Impressions Investigation

**Audit ID:** `youtube_zero_impressions_2026-08-07`  
**Channel:** Orbit with Ben · `@OrbitWithBen` · `UC_esArsDKd3GJvOkeO0DUog`  
**Audited (UTC):** 2026-08-06 ~22:20  
**Sources:** YouTube Data API v3 (OAuth), public watch/oEmbed/search/channel pages, Google `site:` probe, repo CDP/upload indexes, prior Studio audits  
**Evidence snapshot:** `EVIDENCE_SNAPSHOT.json`

---

## 1. Executive summary

Canonical BH assets are **public, processed, crawlable, searchable, and not kids-restricted** — yet they have **0 API views**. This is **not** a “stuck Private / still Scheduled / failed processing / not indexed” failure for those IDs.

The sharper finding is **pipeline chaos**: the channel holds **89** uploaded IDs (7 public · 30 scheduled · 52 private), including **duplicate BH Shorts**, a **public Short pointing at a private long**, and a **same-slot scheduled duplicate** of an upcoming Short. Fermi Shorts already proved the channel can get Shorts-feed distribution (**38** and **97** views). BH cluster contributed **0** of the channel’s **141** lifetime views.

| Verdict | Meaning |
|--------|---------|
| Primary for *public* BH 0-views | **Not recommended / cold-start + damaged trust signals**, not “YouTube doesn’t know the video exists” |
| Primary for many “0 impressions” IDs in Studio | Operator confusion: **Private / Scheduled / superseded** IDs |
| Critical technical defect | CDP reupload bursts + incomplete demotions left **duplicate public + broken funnel** live |

**Most likely root mix (public BH cluster):**

| Cause | Probability |
|------|-------------|
| Cold start / tiny audience / no seed watch history | **48%** |
| Technical / spam-adjacent pipeline (duplicates, reupload bursts, broken funnels, 89-ID inventory) | **32%** |
| Metadata / packaging weak vs Fermi Shorts (shorter desc, weaker hashtags, title drift) | **12%** |
| Other (analytics lag, soft review queue, synthetic-media UX, unknown Studio warning) | **8%** |

---

## 2. Live catalogue (ground truth)

### Public now (API `privacyStatus=public`)

| ID | Type | Title | Published (UTC) | Views | Notes |
|----|------|-------|-----------------|------:|-------|
| `Mo93x0fxB1Q` | Long | Fermi Paradox… | 2026-07-30 17:00 | **6** | Education · processed |
| `1HuV8o3gOss` | Short | Why Haven't We Found Aliens Yet?… | 2026-08-02 23:17 | **38** | Best early Short signal after replace |
| `KcKBixwmcV4` | Short | What If the First Alien Clue… | 2026-08-03 11:30 | **97** | Strongest Short |
| `3xrxdmaOwJI` | Long | What Happens If You Fall Into a Black Hole?… | 2026-08-05 17:00 | **0** | Canonical BH long |
| `JRfhE6yWom4` | Short | Why This Line Is a Point of No Return… | 2026-08-05 20:00 | **0** | Canonical BH launch Short |
| `L2OFjL4neOo` | Short | Falling In Wouldn't Feel Like Falling | 2026-08-06 11:30 | **0** | Supporting Short |
| `IwpO33AJaPQ` | Short | Cross This Line and You Never Come Back | 2026-08-06 22:14 | **0** | **FAIL — duplicate public; desc → private long `RCs6MMxF3ko`** |

Channel API stats: **141** views · **1** sub · **7** public videos · joined **2026-07-27** · `longUploadsStatus=allowed` · linked · not monetized.

### Intentionally not earning impressions (examples)

| ID | State | Why 0 impressions is expected |
|----|-------|-------------------------------|
| `tUAdhOnMW2g` | Private + `publishAt=2026-08-07T10:30:00Z` | Not live yet |
| `b8-X_FyJnHM` | Private + `publishAt=2026-08-12T17:00:00Z` | Alien long scheduled |
| `tfTkMdE7qqw` | Private + `publishAt=2026-08-19T17:00:00Z` | JWST long scheduled |
| `n7CbJrOCnU0`, `RCs6MMxF3ko` | Private | Superseded / mid-replace BH longs |
| ~52 other private IDs | Private | Holds, failed demotions, old takes |

---

## 3. Phase checks (PASS / WARNING / FAIL)

### Phase 1 — Publishing pipeline

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| Upload method (historical catalogue) | **WARNING** | Live catalogue uploaded via Studio CDP/Playwright, not `youtube:package`. API connection exists but `lastSuccessfulPublishAt=null` | CDP is flaky on visibility/schedule; ID mix-ups documented | Switch primary path to Content Ops `npm run youtube:package` per locked rule | High |
| API adapter defaults | **WARNING** | `privacyStatus` defaults **private**; `notifySubscribers` never set; scopes = `youtube.upload` + `youtube.readonly` only (no `force-ssl`) | Future API uploads can stay private if schedule omitted; incomplete Studio feature surface | Require explicit privacy; pass `notifySubscribers=true` on first public; reconnect OAuth with `force-ssl` | High |
| Canonical BH long public | **PASS** | API `3xrxdmaOwJI` → `privacy=public`, `uploadStatus=processed` | Without public, impressions impossible | None for this ID | High |
| Canonical BH Shorts public | **PASS** | `JRfhE6yWom4`, `L2OFjL4neOo` public | Same | None | High |
| Future inventory still scheduled/private | **PASS** (expected) | Alien/JWST/`tUAdhOnMW2g` have `publishAt` | 0 impressions until go-live is correct | Do not treat as “broken distribution” | High |
| Publish transition / timezone | **WARNING** | Studio UI often CEST; schedules authored UK; docs disagree Wed vs Thu long day; OPTIMAL JSON still has stale BH/JWST IDs | Easy to “fix” wrong ID or misread air time | Single source of truth = Studio + `SHORTS_UPLOAD_INDEX` + API; rewrite OPTIMAL IDs | High |
| Draft / members-only / age-restricted | **PASS** | API: no age rating object; public; not members; playability OK | Would block or shrink reach | None observed | High |
| Duplicate / mid-replace public leak | **FAIL** | `IwpO33AJaPQ` public while twin `JRfhE6yWom4` also public; funnel → private `RCs6MMxF3ko` | Duplicate + dead CTA damages trust and confuses analytics | **Privatize `IwpO33AJaPQ` now**; fix any other public dupes | High |
| Same-slot scheduled duplicate | **FAIL** | `2C-eiSMsBLc` scheduled `2026-08-07T10:30:00Z` same window as `tUAdhOnMW2g`; `IqII5mVGdrs` scheduled `2026-08-07T22:00:00Z` duplicates live `L2OFjL4neOo` theme | Two near-identical Shorts in one day looks spammy | Cancel/hold duplicates to 31 Dec or delete | High |
| Inventory hygiene | **FAIL** | **89** mine videos for an 11-day channel | Rapid reupload volume is a known Shorts suppression risk | Stop CDP replace bursts; privatize orphans; one canonical ID per asset | High |

### Phase 2 — Processing

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| HD processing complete | **PASS** | All sampled IDs `uploadStatus=processed`, `definition=hd`, `processingStatus=succeeded`, thumbnails available | Unprocessed videos get no reach | None | High |
| 4K processing | **WARNING** | Public watch adaptive max **1080** (longs) / **1920** vertical (Shorts). No 4K observed | 4K not required for impressions | Optional future masters; not causal | Medium |
| Thumbnail processed | **PASS** | `thumbnailsAvailability=available`; `maxresdefault` HTTP 200 for longs/Shorts | No thumb → weak CTR once impressed | None for processing | High |
| Captions | **WARNING** | API `contentDetails.caption=false` (no uploaded track); watch page shows **ASR EN** auto-captions | Uploaded captions help accessibility/retention; ASR exists | Upload SRT for longs + Shorts | Medium |
| Chapters | **PASS** | Timestamp lines present on Fermi + BH long descriptions | Helps browse/session | Keep; validate first chapter `0:00` | High |
| Stuck processing / rejection | **PASS** | No `failureReason` / `rejectionReason` | Would explain hard 0 | None | High |
| Transcodes complete | **PASS** | Multiple adaptive formats; Shorts ~26–30 formats | Needed for feed | None | High |

### Phase 3 — Metadata

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| Title length | **PASS** | Public titles within limits; BH long 65 chars | Truncation hurts CTR | Optional tighten BH long (see Phase 12) | High |
| Description length | **WARNING** | Fermi Shorts 263–299 chars; BH Shorts **181–183**; dupe `IwpO33AJaPQ` **148** + **0 tags** | Thin metadata vs working Shorts | Restore full package descriptions + tags on all public Shorts | High |
| Hashtags | **WARNING** | Fermi Shorts include topic hashtags (`#FermiParadox` etc.); BH Shorts mostly `#Space #Shorts` | Discovery / clustering | Add topic hashtags (`#BlackHole #EventHorizon`) without spam | Medium |
| Tags | **PASS** on canonical · **FAIL** on dupe | Canonical BH tags 15–22; `IwpO33AJaPQ`/`RCs6MMxF3ko` tagsN=0 | Tags secondary but zero = unfinished upload | Privatize incomplete uploads | High |
| Category | **WARNING** | Longs Education (`27`); Shorts People & Blogs (`22`); private replace long also `22` | Inconsistent category on replace path | Force Education (`27`) for space docs in package manifest | Medium |
| Language | **WARNING** | BH long `defaultAudioLanguage=en-US`; Fermi `en` | Minor; British VO brand prefers `en-GB` | Set `en-GB` in package uploads | Low |
| License / embed / kids | **PASS** | `license=youtube`, `embeddable=true`, `madeForKids=false`, `selfDeclaredMadeForKids=false` | Kids mode kills ads/recs shape | Keep explicit false | High |
| Paid promotion / synthetic disclosure | **WARNING** | API field `containsSyntheticMedia` absent/null on list; not confirmed in Studio UI | Altered-content label can reduce some surfaces | Manually verify Studio → Show more options → Altered content; disclose if required, don’t fight the label | Medium |
| Recording date / location | **WARNING** | Not set in API snippets reviewed | Minor SEO | Optional; not causal | Low |
| Comments / notify | **WARNING** | Comments open (Fermi has comments); `notifySubscribers` never set in API adapter; CDP path unknown | Missed notifs on first public reduce early seed | Ensure notify on first public; don’t re-notify spam on replaces | Medium |
| Automatic chapters/places/concepts | **WARNING** | Not directly readable via this API surface | Soft ranking features | Rely on clear VO + chapters text | Low |

### Phase 4 — Searchability

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| Exact video ID | **PASS** | YT search `3xrxdmaOwJI` returns video; Google `site:youtube.com 3xrxdmaOwJI` contains ID | Proves index existence | None | High |
| Exact title | **PASS** | Title query returns `3xrxdmaOwJI`; Short titles return their IDs | Search surface works | None | High |
| Channel search | **PASS** | `Orbit with Ben` returns long + some Shorts | Channel entity indexed | None | High |
| Channel tabs | **PASS** | `/videos` shows both longs; `/shorts` shows 5 IDs including dupe | Public shelf OK | Remove dupe from shelf by privatizing | High |
| Playlist | **FAIL** | API `playlists.list mine` → **[]** | Playlists aid session watch time | Create “Orbit’s Cosmic Journey” + add longs | High |
| Scheduled/private search | **PASS** (expected fail for public) | Private IDs → LOGIN_REQUIRED / no oEmbed | Not searchable until public | Expected | High |

### Phase 5 — Indexing

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| YouTube knows video exists | **PASS** | oEmbed + watch playability OK + API item present | Rules out “failed upload” | None | High |
| Indexed but not recommended | **PASS** (diagnosis) | Searchable + crawlable + **0 views** on BH | Separates index from feed | Fix trust/dupe; keep publishing cadence | High |
| Still processing internally | **FAIL as cause** | `processingStatus=succeeded` | Would delay | None | High |
| Failed indexing | **FAIL as cause** | Google + YT search find ID/title | Would block search | None | High |

### Phase 6 — Channel health

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| Long uploads allowed | **PASS** | `longUploadsStatus=allowed` | Feature limit would block longs | None | High |
| Channel linked / public | **PASS** | `isLinked=true`, privacy public | Required | None | High |
| Strikes / copyright / limited features | **WARNING** | Not exposed on this API; Fermi Shorts still distributed → hard ban unlikely | Strikes would explain hard 0 | Manually open Studio → Channel status / Copyright | Medium |
| Phone / ID verification | **WARNING** | Cannot confirm via API | Common 0-impression cause on brand-new channels | Confirm phone verification + Advanced features in Studio | Medium |
| Upload frequency | **FAIL** | 89 uploads in ~11 days; multi-ID replaces same day | Spam-adjacent | One ship per asset; demote old before publishing new | High |
| Channel age / subs | **WARNING** | Joined 2026-07-27; **1** sub; 141 views | Cold start real | Continue Shorts→long funnel; community posts | High |
| Brand account | **PASS** (assumed) | Channel custom URL `@orbitwithben`, linked | — | Confirm no Brand Account permission split | Low |

### Phase 7 — API audit

| Check | Result | Evidence | Why it matters | Exact fix | Confidence |
|-------|--------|----------|----------------|-----------|------------|
| Historical uploads via API | **FAIL** (not used) | Connection connected; no successful API publish recorded; CDP results own the IDs | Diverges from locked YouTube API upload rule | Use package CLI for next episode | High |
| `privacyStatus` / `publishAt` design | **PASS** (design) | Adapter forces private/unlisted + publishAt when ≥15m | Correct native schedule pattern | Keep | High |
| Default private without schedule | **WARNING** | CLI/manifest default private | Easy to ship forever-private | Dry-run + post-upload `videos.list` assert | High |
| `notifySubscribers` | **FAIL** | Repo grep: not set on insert | First public may skip subscriber ping | Add query param / status field where supported | Medium |
| Category ID | **WARNING** | Adapter hardcodes `categoryId: "28"` (Science & Technology) while live longs are `27` Education | Inconsistency across paths | Align package to Education `27` | Medium |
| Thumbnail set path | **PASS** (code) | Adapter can set thumb after upload | Needed for CTR | Ensure package always passes thumb | High |
| Captions upload | **FAIL** | Not in adapter publish path | No human captions | Add captions.insert step | Medium |
| Processing polling | **WARNING** | `getExternalStatus` checks uploadStatus; no HD/SD detail polling in publish | Can mark done before feed-ready | Poll processingDetails until succeeded (already mostly OK) | Medium |
| Retry / error handling | **PASS** | Classified HTTP errors + retryable flags in adapter | Prevents silent fail | Keep | High |
| OAuth scopes | **WARNING** | Missing `youtube.force-ssl` called out in connection docs | Limits some manage operations | Re-auth with broader scope | High |

### Phase 8 — Compare successful vs latest

| Dimension | Fermi Short winner `KcKBixwmcV4` | BH Short `JRfhE6yWom4` | BH Long `3xrxdmaOwJI` |
|-----------|----------------------------------|------------------------|------------------------|
| Views | **97** | **0** | **0** |
| Privacy | public | public | public |
| Duration | 49s | 45s | 21m13s |
| Category | 22 | 22 | 27 |
| Tags | 20 | 16 | 22 |
| Desc length | 299 | **183** | 1739 |
| Hashtags | topic-rich | generic `#Space #Shorts` | n/a (long) |
| Related/CTA | → public Fermi long | → public BH long | n/a |
| Captions | ASR | ASR | ASR |
| Playlist | none | none | none |
| Processing | succeeded | succeeded | succeeded |
| Thumbnail | abstract signal visual | Orbit face close-up | Orbit + black hole + “FALLING IN?” |
| Publish lag at audit | ~3.5 days | ~26h | ~29h |
| Reupload neighborhood | quieter | inside heavy BH replace storm | 3 long IDs exist (`n7…`, `3xr…`, `RCs…`) |

**Highlight differences that can matter:** thinner BH Short descriptions; weaker hashtags; BH cluster surrounded by duplicate/replace uploads; long-form cold start already visible on Fermi (only 6 views).

### Phase 9 — Impression investigation

| Hypothesis | Fit | Notes |
|------------|-----|-------|
| Not indexed | **Rejected** for public IDs | Search + Google + crawlable |
| Not processed | **Rejected** | API processing succeeded |
| Still Scheduled / Private | **Accepted for many Studio rows** | 30 scheduled + 52 private — check the right ID |
| Delayed recommendation | **Partial** | Possible for <48h assets; weaker once Fermi already got seed |
| Not recommended / seed failed | **Best fit for public BH** | Public + indexed + 0 views |
| Technical trust damage | **Strong contributor** | Dupes, broken funnel, 89-ID churn |

**Most likely for “Studio says 0 impressions” on BH public IDs:** indexed but **not entering / not expanding Shorts or Browse seed**, with cold start amplified by reupload noise.

### Phase 10 — Competitor benchmark

Direct scrape of 20 *brand-new* educational space channels was **not reliable** (search ranks survivors, not true zero-impression newborns). Using industry cold-start bands + Orbit’s own control group:

| Window | Typical new-channel Short (industry band) | Orbit Fermi Shorts | Orbit BH Shorts |
|--------|--------------------------------------------|--------------------|-----------------|
| 1 hour | 0–30 (often analytics lag) | Had distribution later | 0 |
| 6 hours | 0–50 | — | 0 |
| 24 hours | **10–100** common seed | Achieved tens–low hundreds | **0** after ≥24h |
| 72 hours | 30–500 highly variable | `KcKBixwmcV4` ~97 | still 0 |
| 1 week | wide variance | Fermi long still ~6 | BH long 0 |

**Orbit-specific control:** same channel, same niche, earlier Shorts **did** get the seed pool. Therefore BH 0 is **not** “all new space channels get nothing.”

### Phase 11 — Thumbnail audit

| Asset | Res | Compression | CTR potential | Safe zones | Mobile | Clutter | Brand | Emotion | Subject |
|-------|-----|-------------|---------------|------------|--------|---------|-------|---------|---------|
| BH long | 1280×720 maxres OK | OK (~185KB) | **Strong** — Orbit + hole + “FALLING IN?” | OK | Good | Low | Strong orange Orbit | Worry/curiosity | Clear |
| Fermi long | 1280×720 | OK | Strong — “WHERE IS EVERYBODY?” | Robot bottom-right may kiss duration badge | Good | Low | Strong | Lonely/sad | Clear |
| BH Short `JRfh…` | vertical frame in maxres | darker (meanL≈36) | Medium — face clear, **no text hook** | OK | Good | Low | Strong | Curious eyes | Clear |
| Fermi best Short | abstract waveforms | Medium | Medium-low subject clarity but **worked anyway** | OK | OK | Medium | Weak Orbit presence | Mystery | Abstract |

**Verdict:** Thumbnails are **not** the reason impressions are zero. They matter only after impressions exist (CTR). BH long thumb is shippable; BH Short could add a 2–3 word curiosity label.

### Phase 12 — Title audit

| Title | Score (clarity+curiosity, no fearbait) | Notes | Improved options |
|-------|----------------------------------------|-------|------------------|
| What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey | **88** | Clear; brand suffix OK | `What Happens If You Fall Into a Black Hole?` · `Falling Into a Black Hole — What You'd Actually Experience` |
| Why This Line Is a Point of No Return #Space #Shorts | **80** | Curiosity OK; “This Line” vague without visual | `Why the Event Horizon Is a Point of No Return #Shorts` |
| Falling In Wouldn't Feel Like Falling | **90** | Excellent paradox hook | Keep |
| Cross This Line… (dupe public) | **70** | Fine title, **wrong to be public duplicate** | Privatize; don’t compete with retitled twin |
| What If the First Alien Clue Is Already Here? | **93** | Best performer pattern | Use as template |
| Fermi long | **92** | Keep | Keep |

### Phase 13 — Cold start analysis

| Bucket | Probability | Rationale |
|--------|-------------|-----------|
| Cold start (new channel, 1 sub, weak watch history) | **48%** | Channel 11 days old; long-form already weak (Fermi 6); industry expects small seeds |
| Technical issue (dupes, reuploads, broken funnel, CDP) | **32%** | 89 IDs; public dupe→private long; same-slot schedules; Fermi proves channel *can* get views |
| Metadata issue | **12%** | BH Shorts thinner than Fermi Shorts; not enough alone to force literal 0 |
| Other | **8%** | Unverified phone/advanced features, altered-content UI, analytics lag |

---

## 4. Root cause analysis

1. **For scheduled/private rows in Studio:** zero impressions are **correct**. Many recent uploads are not public yet (`publishAt` future) or are held private after replaces. Always verify the **canonical public ID**.

2. **For public BH long + Shorts at 0 views:** YouTube **has indexed** them. They are **not earning recommendation impressions**. This matches “indexed but not recommended,” not “failed publish.”

3. **Why Fermi Shorts got distribution but BH did not:** same channel trust floor exists; BH cluster is entangled in **replace/reupload storms** (multiple longs with identical titles, duplicate Shorts, unfinished metadata uploads, one public Short CTA to a private long). That is the main *technical amplifier* on top of ordinary cold start.

4. **Content quality is not required to explain current evidence.** Processing, privacy, kids flags, embed, and search all clear for canonical public IDs.

---

## 5. Risk assessment

| Risk | Severity | Likelihood | Impact |
|------|----------|------------|--------|
| Leaving `IwpO33AJaPQ` public with dead CTA | High | Certain now | Duplicate shelf + trust damage |
| `2C-eiSMsBLc` / `IqII5mVGdrs` auto-publishing as dupes | High | Certain if not cancelled | Same-day near-duplicates |
| Continuing CDP multi-upload replaces | High | High if unchanged | Ongoing 0-view loops |
| Misreading OPTIMAL stale IDs as live | Medium | High | Wasted optimisation on private assets |
| API default private without assert | Medium | Medium | Silent private ships |
| No playlists / thin Short descriptions | Medium | Certain | Weaker session + discovery |

---

## 6. Immediate fixes (do today)

1. **Privatize** public duplicate Short `IwpO33AJaPQ`.
2. **Cancel/hold** scheduled duplicates `2C-eiSMsBLc` (same slot as `tUAdhOnMW2g`) and `IqII5mVGdrs` (dup of Falling In) → 31 Dec hold or delete.
3. **Confirm Studio → Channel → Status** for strikes, limited features, phone verification, advanced features.
4. On canonical public Shorts `JRfhE6yWom4` + `L2OFjL4neOo`: restore **full descriptions**, topic **hashtags**, **Related** → `3xrxdmaOwJI`, **pin** full-film comment.
5. Stop all BH reupload/replace CDP jobs until inventory is clean.
6. Create playlist **Orbit’s Cosmic Journey** and add `Mo93x0fxB1Q` + `3xrxdmaOwJI`.
7. Re-check BH Short impressions after **48h** of clean public shelf (no new dupes).

---

## 7. Long-term improvements

1. Make **YouTube Data API package upload** the only primary path; CDP only for Related/ABC/pin gaps.
2. Post-upload **assert job**: `videos.list` must show expected `privacyStatus`, `publishAt`, tags≥10, desc length floor, category, no duplicate title+duration public pairs.
3. **Canonical ID ledger** per episode (one long ID, N short IDs); auto-fail if a second public ID shares title fingerprint.
4. Add `notifySubscribers` policy (true on first public only).
5. Upload **caption tracks**; set `defaultAudioLanguage=en-GB`.
6. Align category to **Education (27)** for space documentary.
7. Reconnect OAuth with `youtube.force-ssl`.
8. Rewrite `OPTIMAL_PUBLISH_SCHEDULE.json` IDs to match Studio/API.
9. Keep Fermi-like Short packaging: paradox title + specific hashtags + full CTA block.

---

## 8. Priority action table

| Priority | Issue | Expected impact | Difficulty | Time required | Steps |
|----------|-------|-----------------|------------|---------------|-------|
| Critical | Privatize `IwpO33AJaPQ` | Removes duplicate public Short + dead funnel | Easy | ~5 min | Studio → Short → Visibility → Private → Save |
| Critical | Kill scheduled dupes `2C-eiSMsBLc`, `IqII5mVGdrs` | Prevents tomorrow’s duplicate publish | Easy | ~10 min | Studio schedule → 31 Dec hold or delete |
| Critical | Studio channel status / phone / advanced features check | Rules in/out account-level block | Easy | ~10 min | Studio Settings → Channel → Feature eligibility |
| High | Restore BH Short metadata + Related + pin | Improves seed CTR/session if impressions appear | Easy | ~20 min | Paste package desc/tags; set Related `3xrxdmaOwJI`; pin comment |
| High | Freeze CDP replace bursts | Stops further trust damage | Easy | immediate | Do not run smooth-CFR replace scripts |
| High | Playlist + end screen on BH long | Session watch pathways | Easy | ~15 min | Create playlist; add end screen to Fermi + next |
| Medium | Switch next episode to API package upload | Deterministic privacy/publishAt | Medium | one episode ops change | `youtube:package` dry-run → upload → assert |
| Medium | OAuth scope + notifySubscribers + category lock | Cleaner API surface | Medium | 1–2 hrs eng | Re-auth; patch adapter; tests |
| Medium | Captions upload automation | Retention/accessibility | Medium | eng task | captions.insert in package pipeline |
| Low | Title/thumb micro-optimisations | CTR after impressions exist | Easy | ~30 min | Only after impressions >0 |
| Low | OPTIMAL JSON ID rewrite | Ops clarity | Easy | ~20 min | Sync to API public/scheduled IDs |

---

## 9. Checklist for every future upload

- [ ] Canonical ledger row created (episode → long ID → short IDs)
- [ ] Dry-run package manifest: privacy, publishAt (≥15m), madeForKids=false, category Education, language en-GB
- [ ] Upload via API package CLI (not CDP primary)
- [ ] Assert via `videos.list`: privacy/publishAt/tags/desc/thumb/processing succeeded
- [ ] No other public video with same title fingerprint
- [ ] Old takes privatized **before** new public go-live
- [ ] Short description includes full-film URL to **public** long
- [ ] Related + pinned comment set (Studio finish)
- [ ] Captions uploaded (or ASR verified)
- [ ] Playlist add for longs
- [ ] Notify subscribers only on first public of that asset
- [ ] Post-publish 1h / 6h / 24h impression check on the **canonical** ID only

---

## 10. Technical findings (compact)

- Channel can distribute Shorts (Fermi evidence).
- BH public IDs are healthy at the file/status layer and dead at the recommendation layer.
- Ops system currently optimizes and reuploads faster than it demotes, producing a large private/scheduled shadow catalogue and at least one leaked public duplicate.
- API path is ready but unused; CDP path is the source of ID confusion (`normal_speed_upload_result.json` historically mapped wrong IDs; smooth-CFR scripts treat `RCs6MMxF3ko` as new long while `3xrxdmaOwJI` remains the public canonical).

---

## 11. Deliverable map

1. Executive summary — §1  
2. Technical findings — §2–3, §10  
3. Root cause analysis — §4  
4. Risk assessment — §5  
5. Immediate fixes — §6  
6. Long-term improvements — §7  
7. Future upload checklist — §9  
8. Priority table — §8  

Raw machine snapshot: `EVIDENCE_SNAPSHOT.json`.
