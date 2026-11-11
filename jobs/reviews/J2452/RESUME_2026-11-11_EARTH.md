# J2452 — closing Earth replacement checkpoint

Worker macbook. Continue macbook/J2452, PR #789. Full compilation remains incomplete; no final master, reel, NAS delivery or UAT card. No upload, Studio change, generation, sign-in or spend. HOS untouched.

## Current picture candidate

`/Users/ben/_desk/J2452-sleep-scratch/home_earth_v04/029_picture_home_earth.mp4`

Preserves the latest remote Crab repair and earlier observatory/closing repairs. Replaces Betelgeuse chapter 472.6667–476.4000 seconds (source master 493.16–496.90) with the existing cleared Apollo 17 Blue Marble under “The bigger question is closer to home.” This is the second appearance of that Earth photograph. No new asset downloaded; source identity, public-domain record, credit and hashes are inherited from the film's SOURCE_POOL_v03 and retained in REPORT.json. The whole globe is fitted into real dark space with a 1.2% slow push, 15% sleep darkening and inherited luma cap. NASA / Apollo 17 credit is visible. No sourced labels or panels.

The 112-frame replacement has 0.5-second endpoint dissolves using neighbouring shot frames, without changing narration time. Source masters and the previously measured 108:22.36 audio candidate remain untouched. The source/fit was visually inspected as a still; no moving-picture or listening approval is claimed.

`home_earth_v01` is explicitly rejected locally: it started from the stale local branch and omitted the later remote Crab repair. The branch was then fetched and fast-forwarded to the latest published checkpoint before building v02. v02 also failed its fade-background/pixel checks; v03 stopped on a quoted-filter expression error. Only checked v04 may be continued.

## Reproduce

Use the existing `_desk/J2141-venv` with Pillow/numpy:

- `python jobs/reviews/J2452/repair_home_earth.py --out NEW_LOCAL_DIRECTORY`
- `python jobs/reviews/J2452/check_home_earth.py NEW_LOCAL_DIRECTORY`

Builders refuse overwrites. Run normal picture_qa with the saved cuts and the original SOURCE_POOL_v03, betelgeuse_covers_pool_v01 and crab_reuse_v02/pool.json. Do not waive failures or use a nonexistent sleep-darken option.

## Remaining work

Continue from the adopted checked chapter and cuts. Other repeated sources and retained graphics/baked labels remain. Twelve other picture chapters, ramp/quiet names/inter-film breaths, final AV assembly, picture/CTA/loudness/peak/silence/join checks, ~12-minute reel and delivery remain before Ben's watch card. The latest acting-Chief ruling (#6790308575, 07:50Z) explicitly keeps finished files and sources under _desk with report hashes; Chief-owned J2568 handles the NAS transfer. Do not attempt NAS writes from this MacBook. Earliest air is 12 December. This is a resumable production checkpoint, not a finished cut.

## Saved-file checks

Output SHA-256: `759c3d853b0a5d87fae4ac1471091cf87cb899f41197b6c1f91be2de3682b9cd`. Full decode and exact 14,829-frame clock pass, duration 494.30 seconds. All 112 replacement frames compared at 320×180 against the separately encoded dissolved patch: maximum mean frame error 0.801, threshold 2. Seven sparse unchanged samples pass (maximum 0.714). The boundary strip and final seven-sample transition sheet were inspected as stills: M42 dissolves into Earth and then the following ALMA observation, with no old dish picture in the replacement. No listening or moving-picture approval claimed.

Normal full saved-chapter picture QA still FAILs: nine remaining reuse rows, seven warnings; no sampled pixel hard failure. The Earth replacement row passes. No override, renamed identity or relaxed threshold. The standalone patch polish check has zero failures/warnings. Full QA samples cut midpoints; it is not every-frame perceptual review. Reports and cuts are committed, media/sheets remain under _desk.

Scripts compile; seven email-ratchet tests and git diff check pass. All launched processes finished. Release because full remaining assembly exceeds this unattended run. Thread read to #6790308575 (trusted message displayed; home marker persistence is restricted).
