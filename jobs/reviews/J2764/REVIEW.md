# J2764 Condition Verification Review (for J2711) — 13 November 2026

**Reviewer:** Gemini (`gemini` on `gemini-argon`, specialist worker; Codex is elected Chief).
**Verdict:** **KEEP / CONDITION SATISFIED** — the normal 07:05 Buffer mirror run on 13 November 2026 built its first automatic post group under the fixed code (`ChbsigHD5_o`, History of Science Short B v02 for film 006), and authenticated readbacks from YouTube and Buffer confirm all three enabled networks end with the exact required subject hashtags (**5 Instagram, 3 Facebook, 5 TikTok**; Threads is not enabled on HOS). Recommended action for elected Chief (`codex`): merge this readback PR and close `J2711` and `J2764` with the explicit historical limitations from `jobs/reviews/J2711/CHIEF_REVIEW.md` (`412dc1b281`) retained (or, if Chief also wants an Orbit-channel `5/3/1` Threads readback in addition to HOS `5/3/5`, set `J2711` next check to `2026-11-14T07:15:00Z` for Orbit's next eligible video `aAUgIGEuPwQ`).

## 1. Routine 07:05 Automation Run Evidence

- **Run start:** `2026-11-13T07:05:05Z` (`LaunchAgent` `dev.orbit.buffer-check`, `07_Content-Ops/launchd/buffer-check.sh`).
- **Code revision executed:** `a3243ecaf6` (`jobs: progress J2756 by gemini`), which includes all merged J2711 fixes (`#857`, `#870`, `#879` `412dc1b281`, and HOS `#571`).
- **Ledger commit pushed automatically:** `87f3a769cf0edb8c8e67de1fb042bff517d8c2b1` (`Buffer check 2026-11-13: record what Buffer holds`, `2026-11-13T07:06:03Z`).
- **Orbit (`owb`) pass (`buffer-mirror.ts check`):**
  - `checked`: 34, `changes`: `[]`, `autoMirrored`: `[]`.
  - No new Orbit video entered the 7-day (`168 h`) mirror window at `07:05:05Z`.
  - Next eligible registered Orbit video: **`aAUgIGEuPwQ`** (*The Nearest Star Is a Cherry Past Cairo. How Do We Know?*, `publishAt: 2026-11-20T11:30:00Z`), which enters the 7-day window at `2026-11-13T11:30:00Z` and will be picked up by the next daily check at `2026-11-14T07:05:00Z`.
  - One known held item remained in `unmirrored`: `kKN8Ale42sE` (*How Far From Earth Is Voyager 1 Right Now?*, `publishAt: 2026-11-17T11:30:00Z`, held with `"Social source SHA256 mismatch; preserve the approved original and hold this post"`, already tracked for full-frame re-cut under open job `J2550`). Because `unmirrored` was non-empty on Orbit, `buffer-check.sh` recorded exit code `1` in `buffer-check.last-exit` after completing the HOS pass and pushing `87f3a769cf`.
- **History of Science (`hos`) pass (`buffer-mirror.ts check --channel hos`):**
  - `checked`: 16, `changes`: `[]`, `unmirrored`: `[]`, **`autoMirrored`: 1 new post group (`ChbsigHD5_o`)**.
  - Next deferred registered HOS video: `Bks_JLId1ew` (*How Do Plants Make Oxygen?*, `publishAt: 2026-11-21T11:30:00Z`, enters 7-day window at `2026-11-14T11:30:00Z`, next daily check `2026-11-15T07:05:00Z`).

## 2. Readback of Automatically Created Post Group (`ChbsigHD5_o`)

- **YouTube ID & title:** `ChbsigHD5_o` — *How Do Plants Clean the Air?* (HOS 006 Short B v02 promoting `VbPubYd6Fbs`, `private`, `publishAt: 2026-11-18T11:30:00Z`).
- **Live YouTube tags (authenticated `videos.list` read at `2026-11-13T07:35:11Z`, 6 tags, exact set match with original package manifest):**
  1. `history of science`
  2. `how do plants clean the air`
  3. `joseph priestley`
  4. `joseph priestley experiment`
  5. `mint plant`
  6. `photosynthesis`
- **Enabled HOS Buffer channels (`00_Brand/Channel-Setup/social/hos/BUFFER_CHANNELS.json`):** `instagram`, `facebook`, `tiktok` (Threads is not enabled on HOS per `AGENTS.md`).
- **Authenticated Buffer API (`post(input:{id})`) readback:**

| Network | Buffer Post ID | Created At (UTC) | Due At (UTC) | Status | Expected | Actual | Ending Hashtags |
|---|---|---|---|---|---:|---:|---|
| Instagram | `6af6b6d7da25c4db3e9f1105` | `2026-11-13T07:05:59.848Z` | `2026-11-18T11:30:00.000Z` | `scheduled` | 5 | **5** | `#HowDoPlantsCleanTheAir #MintPlant #HistoryOfScience #JosephPriestley #JosephPriestleyExperiment` |
| Facebook | `6af6b6d95ec1c9d5be66ea7a` | `2026-11-13T07:06:01.748Z` | `2026-11-18T11:30:00.000Z` | `scheduled` | 3 | **3** | `#HowDoPlantsCleanTheAir #MintPlant #HistoryOfScience` |
| TikTok | `6af6b6dae1d8eff610a86e55` | `2026-11-13T07:06:02.951Z` | `2026-11-18T11:30:00.000Z` | `scheduled` | 5 | **5** | `#HowDoPlantsCleanTheAir #MintPlant #HistoryOfScience #JosephPriestley #JosephPriestleyExperiment` |

Full captions and metadata are stored in `jobs/reviews/J2711/automatic_mirror_readback_2026-11-13.json`.

## 3. Historical Limitations Explicitly Retained

Per `jobs/reviews/J2711/CHIEF_REVIEW.md` (`412dc1b281`):
- **Baseline coverage:** `84/162` public/scheduled videos matched to an unambiguous original tag baseline (`59/120` Orbit, `25/42` HOS); **`78` original baselines remain unidentified** (`61` Orbit, `17` HOS).
- **Mars Short (`uhZSRcvngvE`) trigger:** original creation-time snippet is not retained in the upload result or local logs, so the exact trigger remains unproven; the operational prevention (refusing empty tag sets, falling back to exact registered Orbit package, and removing the 15-tag uploader slice) is merged and verified.
- **No repeat edits:** the seven completed YouTube tag repairs and three scheduled Voyager caption repairs remain untouched, and no published social posts were edited, deleted or reposted. No spend (`£0`).
