# J3114 — Pluto packaging rebuild v02

19 November 2026. Codex. £0 spend; existing verified New Horizons plates only.

Built three candidates under the controlling J3112 FIX ruling (jobs/reviews/J3112/REVIEW.md). These are delivered for exact-file Chief review **J3115**, not approved or armed. J3112 supersedes the optional STILL ALIVE/glacier-caliper/two-arm suggestions in J3111; none were built.

## Changes and visual inspection

- A: removed the rectangular paste halo with a feathered circular limb; globe is 560 px across, with whole limb below the hook and away from the duration badge. The previous 550 px source tile contained black margins, leaving a smaller actual disc. A 640–660 px globe cannot fit beneath the top-band hook in 720 px without clipping; J3112 expressly prioritises an uncovered whole globe. PLUTO / 2,377 km uses 52/48 px Arial Black, replacing the unreadable 19 px qualifier. No projected glacier caliper.
- B: cropped the source width from 3420 to 2804 px (18% tighter), retaining the haze and mountain/plain boundary. Cold blue/silver editorial grade, 8 px bar and 48 px label. Approximate 250 km bar = round(250 / (1250 × 2804/3420) × 1280) = 312 px; this is a scene-width reference, not a measurement of foreshortened terrain.
- C: full 2736 px source width; crop y=520..2059, warm cream/rust/charcoal editorial grade, smooth navy top vignette, dark lower-left scale pad. Approximate 100 km bar = 100/400 × 1280 = 320 px. No invented terrain, horizon or hard teal header.
- Viewed all three full-size images and the final 168×94 / 360×202 sheet with the image input tool. Hooks and scale labels are legible; A has no rectangular seam, B retains haze and mountain relief, C retains real cells and the rugged shoreline. Colours on B/C are editorial, not scientific temperature or natural-colour claims. This is still-image inspection only.

## Exact-file colour checks

| Candidate | Saturation | Near-black | thumb_preview --score |
|---|---:|---:|---|
| A | 159.6 | 4% | PASS |
| B | 176.5 | 1% | PASS |
| C | 104.2 | 1% | PASS |

C clears the 100 floor but remains below the 120 target. Colour metrics alone are not creative approval. Source SHA-256 matches the previously verified harvest for all three. The manifest records source URLs, source hashes, crops, scales and output hashes. Phone sheet and individual preview sheets live beside the NAS JPEGs.

## Package verification

Lead title is the panel's 58-character “Why Does Pluto Have a Heart? (And Why It Has Zero Craters)”. The four proposed titles are consistent across manifest, title file and metadata. Thumbnail paths/hashes now name v02 drafts; final arms remain unlocked.

Description: **4,602 Unicode characters / 4,626 UTF-8 bytes**. Extracted the panel text and applied J3112's qualification: “a giant moon fixed in the sky as seen from Pluto”. The complete Image credits line is byte-for-byte identical to the previous description; the complete URL set, all six Sources URLs, all seven chapter timestamps, Real Worlds series line and Pictures disclosure are preserved. Chapters file untouched.

- `gate:episode --script ...pluto_frozen_heart_script_master_v03.md`: **PASS**, script score 95.8/100. Output: `11_Upload-Package/GATE_EPISODE_J3114.md`. Explicit locked v03 selected because the automatic selector initially chose v00.
- `youtube:package --dry-run`: **ok=true, dryRun=true**, “Dry-run complete. Would upload now with publishAt=2026-12-13T18:00:00.000Z.” Saved result in the package. Its scheduledOnPlatform field is simulated; no platform write occurred. Existing channel adapter resolves category 28 although the package legacy categoryId field says 27; no category/tool change was made in this packaging job.
- Long master SHA-256 recomputed: `e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62` unchanged.
- Trailer SHA-256 recomputed: `01701660d2fcc3a1340fa8d6ffef2f8d1a96b87e049facf1d28905c4a05392fd` unchanged.
- NAS copy verification: `NAS_VERIFY_J3114.json`; revised artifacts and four package text files copied and read back. v01 untouched.
- Proposed ledger **T044** (built as T041 on 19 Nov; renumbered when published on 25 Nov under J3530, because T041-T043 were taken on main in the meantime), started=null, video=null. Main ends at T040; open PR #1031 revises existing rows/history without adding live row IDs. Only the new row is added here; no historical ledger data rewritten.

## Handoff

J3115 reviews these exact files and locks three distinct arms before delivery. Both thumbnail and upload stages stay in review. Preserve the existing J2868.1 long watch (8 December 18:00 London watch-by; 13 December 18:00 planned air slot), and J3066/J3065 public-parent holds. No new watch card, assumed Ben approval, YouTube write, Buffer change or media rewrite.

## Output hashes

- 034_pluto_A_j3105_v02.jpg: `8f5673606c0070eda94f90b7fee7960975fe41a49415812fcd841d20a9195a42`
- 034_pluto_B_j3105_v02.jpg: `3b17f4c7f131bc275d4cd7109f591ef65535db0d63bc4286e3d7a584f7b4c4f7`
- 034_pluto_C_j3105_v02.jpg: `c23a742058756337b7ee56e3e2aafe526763e5cccc3369f439cefd2f6a501aa3`
