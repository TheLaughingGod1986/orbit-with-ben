# J3372 HOS Studio readback — 22 November 2026

The dedicated Mini browser authorised by J3384 is authenticated as HOS `UCXp7HkBIl1LgaznXuZHJyRg`. The current evidence is **J3372_studio_readback.json**. It supersedes the earlier browser-unresponsive diagnosis in J3372_studio_read_status.json, retained as historical evidence. No login is needed for this read.

## Exact reach window

Studio Advanced mode explicitly shows **25 Oct–21 Nov 2026 / Last 28 days**. The channel Content table supplies 41 of the audit's 45 videos. The other four were opened individually in the same date window: each displays em dashes for impressions and CTR, preserved as unknown.

| Format | Available / inventory | Median impressions, available rows | Median CTR, available rows |
|---|---:|---:|---:|
| Long | 7 / 8 | 44 | 6.1% |
| Short | 34 / 37 | 76.5 | 1.9% |

These are available-row medians at Studio's displayed precision, not complete-inventory medians. The only qualifying ≥1,000-impression video is the **Short** `xzKoHg0E0_U`, “What Is Dalton's Atomic Theory?”: **2,337 impressions / 1.7% CTR**. No available long qualifies. The channel total displayed is 7,477 impressions / 2.5% CTR; that is not a median.

**Views from impressions remain unknown for every row.** The Advanced mode metric picker has no such metric. On video Reach, selecting 28 days updates key metrics, but the funnel retains its explicit “Since published” label. Those funnel values are not the requested window and are not substituted. No rounded CTR multiplication is used. The metric picker and funnel text are retained in J3372_metric_availability.txt; source table and four individual reports are retained alongside it.

## Willow finished experiment

The attached **Title and thumbnail** report for `VbPubYd6Fbs` ran **5 November 2026 18:00–19 November 2026 18:58 London**. Studio says **“Not enough impressions to declare a winner”**. Both watch-time shares are em dashes; variant CTR and impressions are not displayed. The opaque experiment ID is not shown: the recorded identity is video + exact interval + the paired titles and artwork.

- First / A: **The Willow Tree That Was Made of Air**, **WOOD FROM SKY?**; visible to all viewers.
- Second / B: **Where Does a Tree's Weight Come From?**, **DO PLANTS EAT SOIL?**.

No existing ledger row for this video was found. **T044** records the finished inconclusive test, null shares and no winner. Both makers are recorded as Gemini from the HOS J0869 THUMBS_INDEX_v01.json, with its exact existing asset hashes. The separate 28-day 70-impression / 4.3% CTR row is not an experiment outcome. The attached finished test remains intact.

## Current titles and attached tests

| Video | Current title | Attached thumbnail test |
|---|---|---|
| `_C92tIJCk8A` | How Did We Discover Germs? | Finished 5 Nov 02:21 London; insufficient impressions |
| `AL_-qlWko_g` | How Did We Discover the Periodic Table? | Finished 12 Nov 01:34 London; insufficient impressions |
| `frP_YrNShsU` | How Did We Discover X-rays? | Finished 28 Oct 21:17 London; insufficient impressions |

Each finished report was opened read-only and preserved. The ordinary title field shows no attached title test. J1130 remains closed. No replacement test is proposed or armed.

## Validation and next action

JSON inventory coverage, metric parsing, unknown preservation, screenshot hashes and ledger uniqueness were checked. `git diff --check` is clean. The ledger verdict still says **no default yet**; this result is inconclusive. Screenshots stay outside git, with paths and SHA-256 in the readback JSON.

The required HOS `npm run channel:audit` was attempted and **could not run**: missing `../../generated/prisma/client` through the existing storage/token imports. No channel audit PASS is claimed. This read-only task changed no title, thumbnail, test, visibility, schedule, end screen or other Studio setting; 004 and 007 were untouched. No spend.

J3365 / PR #1170 should use this evidence to correct its window, medians, qualifying set, Willow result and current-title recommendations before the revised audit is reviewed. This evidence collection does not itself pass the revised audit or any film stage.
