# J2452 — Crab reuse repair checkpoint

Worker macbook-2. Continue macbook/J2452, PR #789. Job incomplete: no finished master/reel, NAS master delivery, UAT, upload, Studio action, generation, sign-in or spend. HOS untouched.

## Adopted silent chapter

`/Users/ben/_desk/J2452-sleep-scratch/crab_reuse_v02/029_picture_crab_repaired.mp4`

SHA-256 `78dc108fc34a242733b8ba65bfe331c110ce9275c2bb3ba51d9bf1d8531bde39`.

Preserves the previous framefixed observatory repair and all earlier repairs. Replaces chapter 421.40–432.50 seconds (source master 441.90–453.00) with a different real Crab Nebula observation, ESA/Webb weic2326a. This is not a renamed or recropped copy of the original Hubble photograph. The locked narration names the Crab Nebula in this window; it does not specify a telescope or wavelength. The still illustrates the named nebula, not a measurement of expansion over time.

Official image and terms checked live: https://esawebb.org/images/weic2326a/ and https://esawebb.org/copyright/. The unannotated Large JPEG has the full 10509×9151 dimensions. Full required credit is visible, unaltered, plus a small “Webb infrared observation” identification. CC BY 4.0 permits this use with credit. REPORT.json records the source URL, identity, dimensions, modifications and hashes. The original source and a saved-output midpoint were inspected as stills: real filaments, no sourced labels or panels, credit clear. No moving-picture or listening approval is claimed.

The initial v01 integration is rejected: its chosen fade-in frame already contained the old Hubble image. The transition-sheet review caught this; matching a flawed patch did not establish removal. v02 moves the replacement start three frames into the preceding graphic (421.40 s), extracts the preceding frame by exact index and preserves the full narration clock. Only the checked v02 output is adopted.

The patch uses a central 16:9 crop and slow push, 15% sleep darkening and inherited luma cap. Two-second endpoint dissolves use neighbouring shot frames, fully removing the third original Crab appearance and its baked overlay. Neighbouring retained graphics remain for later repair. Source master and narration are unchanged.

## Evidence

- Full decode and exact frame clock: 14,829 frames, 494.30 seconds.
- Independent checker: all 333 replacement frames compared at 320×180 to the separately encoded dissolved patch; maximum frame mean error 1.731, threshold 2. Seven sparse unchanged samples and three opaque-patch samples pass. Source/output hashes match.
- Normal combined picture QA: FAIL, **10 remaining reuse rows** (down from 11), seven warnings, no sampled pixel hard failure. No override or relaxed threshold. The replacement row passes source/pixel checks. QA samples midpoints, not every chapter frame.
- Scripts compile; seven email-ratchet tests and diff check pass.

Reports, cut list and new source pool entry are tracked in crab_reuse_v02/ and crab_reuse_qa_v02/. Full QA and transition review sheets remain local. REMAINING_REUSE_CONTEXT.json now lists the ten remaining failed source/master windows.

## NAS copy restriction

Source retained at `/Users/ben/_desk/J2452-sleep-scratch/crab_reuse_v01/weic2326a.jpg`, SHA-256 `40b9ad0c8ece2c1948e274c9e5a38bcf60c5018fb95ab1d92fd918bc8aa1aa05`. Automatic approval review rejected the proposed copy to the film's NAS 03_Footage directory: the user restricts this unattended run to the checkouts and _desk. Nothing was written to NAS and no workaround attempted. A separately authorized run must deliver the source and verify its hash; do not record this as delivered.

## Resume

1. Work from the adopted output and its cuts.json. Repair the ten remaining source reuse failures with actual changed pixels. Original retained graphics/labels still need the sleep-plan review.
2. Twelve other picture chapters, the initial darkening ramp, quiet titles and breaths remain. Preserve thirteen narration chapters and the measured 108:22.36 audio candidate from RESUME_2026-11-11_0415.md.
3. Final assembly, actual AV/CTA/picture/join gates, ~12-minute reel, authorized same-run hash-verified NAS delivery, then Ben's finished-film watch card. Earliest air: 12 December. Do not mark done or UAT.

Reproduce with repair_crab_reuse.py --out NEW_DIRECTORY --photo SOURCE_JPEG in the existing _desk/J2141-venv; builders refuse overwrites. Run check_crab_reuse.py NEW_DIRECTORY. Normal picture QA uses the original SOURCE_POOL_v03.json assets list flattened to a list (saved locally as crab_reuse_v01/source_pool.json), betelgeuse_covers_pool_v01.json and the new pool.json. Passing the original assets wrapper directly to the current loader omits its titles. No gate code changed.

Released at this clean point because full remaining assembly exceeds the unattended 25-minute run limit. All processes launched in this run finished. Checkout restored to main. Thread read to #6789410890; trusted messages displayed, home-directory marker write remains restricted.
