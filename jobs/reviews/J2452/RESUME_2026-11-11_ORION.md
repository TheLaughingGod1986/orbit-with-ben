# J2452 — original-source Orion repair checkpoint

Worker macbook; branch macbook/J2452; PR #789. Compilation incomplete. Released for continuation because the remaining full assembly exceeds the unattended 25-minute run. No finished master/reel, NAS delivery, UAT, upload, generation, sign-in or spend. Earlier thirteen narration chapters, 108:22.36 audio candidate and thumbnail are preserved.

## Saved result

Local silent picture:
`/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chapter_orion_repaired_v01/029_picture_orion_repaired.mp4`

SHA-256 `8f4e2bde4a3143e09c3b0597eed6bd0f74bc52668716ba610268b557ef4e14e1`.

The source is the original unapproved picture checkpoint, not any rejected shadow grade. Row 36 (master 453.00–459.59 s, chapter 432.50–439.09 s) now uses the film's existing real Orion-rising timelapse, ESO `vlttimelapseorion`, credit ESO/B. Tafreshi (twanight.org), CC BY 4.0 per SOURCE_POOL_v03.json. It is an Orion-sky establishing shot under the closing Betelgeuse question, not a claimed resolved picture of Betelgeuse or its companion.

Uses 6.6 seconds of native 6.8-second 1920×1080 footage, no crop/upscale, retiming or loop. Source exposure ×1.2 precedes the plan's ×0.85 sleep darkening; Y highlight cap stays 180. Small corner credit is retained. Two-second dissolves lie outside the nominal replacement: the saved join is chapter 430.50–441.10 s, with full opacity across all 198 replacement frames. Discrete used frame span is [12975,13173), equivalent to 432.50–439.10 s. This rounds the plan/map's 439.09 s to the 30 fps clock without changing chapter length.

Prefix and suffix are encoded once into separate components; components plus the repaired join are concatenated by stream copy. Exactly 14,829 frames / 494.30 seconds remain. Full decode passes. Independent saved-file read-back checks every timestamp/geometry and all 198 opaque frames against the checked component: maximum RGB MAE 0.62553 at 320×180, below unchanged threshold 2. No watch/listen claim.

The saved join's normal picture_qa **PASSes**, with two retained low-detail warnings; its still sheet and the full chapter repair sheet were inspected. The full chapter's normal polish gate remains **FAIL: six near-black rows, three warnings**. The old telescope gutter finding is removed, and no new failed rows appeared. Exact failure coordinates remain in `betelgeuse_chapter_orion_repaired_v01/FAILURES.json`. No thresholds, reviewed-ok exceptions or nonexistent sleep-darken flags were used.

## Rejected alternatives and metadata correction

The old source's cropped sky was tried first. A midpoint gate PASS was insufficient: the five-point sheet shows the moving telescope/rail entering the crop and clipping/obscuring M42. Those candidates remain local and are not used. The alternate native timelapse at plain 0.85 brightness failed low detail/near-black; modest source exposure was applied before sleep darkening. The accepted alternate's endpoint/midpoint sheet shows full framing without padding.

The first join QA map omitted `framing.offset`, causing polish_gate to classify actual timelapse footage as a still and run its still-push jitter test. That failed result is preserved. Corrected metadata records the real video offset 0 (the tool uses this field, not `kind`, to identify footage); normal QA then passes. No jitter switch or override was used. Reproduction scripts now write correct footage metadata directly.

The existing original observation assets were also inspected: sphere_dec.jpg is 816×816 and companion_speckle.jpg 1080×1080. ESO's official eso2003a page confirms its native 816×816 size, so a larger wallpaper is not additional detail. Do not assume a higher-resolution download will solve those dark spans or crop beyond the upscale limit. No new source was downloaded and no NAS file changed.

## Resume directly from here

Use this new picture checkpoint for continued 029 work. Preserve all previous candidates and source masters. Resolve the remaining six dark spans honestly from original sources, without repeating rejected compressed-picture grades. Resolve 22 original graphic rows, baked labels, reuse, original scene dissolves, quiet chapter name and inter-film breath. Twelve other picture chapters and the initial darkening ramp still need work. Then assemble/mux, run every final loudness/peak/silence/CTA/picture/join check, create the roughly 12-minute spot-check reel, copy master/reel to NAS with independent hashes and send only the finished cut to Ben's watch. Earliest air remains 12 December.

Reproduction (all outputs must be NEW local directories):

1. Existing Pillow/numpy environment: `/Users/ben/_desk/J2141-venv/bin/python jobs/reviews/J2452/build_orion_source_repair.py --out <repair>`.
2. Run normal polish_gate on `<repair>/orion_source_repair.mp4` with `<repair>/cuts.json`.
3. `python3 jobs/reviews/J2452/join_orion_source_repair.py --repair <repair> --out <join>`.
4. Run normal polish_gate on `<join>/orion_repaired_join.mp4` with `<join>/cuts.json`, writing `<join>/POLISH_GATE_CORRECTED.json`. Run picture_qa with the saved actual source map/pool as in `orion_repaired_join_v01/qa_source_cuts.json`.
5. `python3 jobs/reviews/J2452/integrate_orion_source_repair.py --join <join> --out <chapter>`.
6. Run `check_orion_source_repair.py --out <join-or-chapter>` in the Pillow/numpy environment, then normal polish_gate on the chapter with its saved cuts.json. Six existing dark failures are expected until repaired; that is not a PASS.

All builds/checks from this continuation exited before release. Thread read to #6787909578.
