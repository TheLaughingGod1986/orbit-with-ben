# J2452 — original-source Chajnantor checkpoint

Worker: macbook. Branch macbook/J2452; PR #789. Compilation remains incomplete. No finished master/reel, UAT, NAS delivery, Studio action, sign-in, generation or spend.

The new silent picture checkpoint is `/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_chajnantor_repaired_v01/029_picture_chajnantor_repaired.mp4`.
SHA-256: `3b37262c97c2efab7110179baa65ab7b1ca30bb0bbe0bac643b672cd444684fd`.

Rebuilt the first Chajnantor sky shot (master 254.80–261.28 s; chapter 234.30–240.78 s) from the film's original ESO `chajnantor_mw.m4v`, source in 3.25 s, rather than applying another shadow lift to the compressed checkpoint. The master used a black-subtraction LUT; this replacement omits it, applies only the required 0.85 sleep darkening and Y=180 highlight cap, retains native motion and adds the small ESO credit. 1280x720 source to 1920x1080 is 1.5x. No download, crop, retiming or loop. Existing source provenance: SOURCE_POOL_v03.json, ESO, CC BY 4.0, https://www.eso.org/public/videos/chajnantormilkyway/. This is a sky establishing shot under the existing pulsation narration, not a resolved pulsation observation.

The actual frame range is [7029,7223), 194 frames / 6.4667 s, rounded from absolute endpoints on the existing 30 fps timeline. Two-second dissolves are outside that shot, using endpoint extension of the replacement in the adjacent windows. Normal component picture QA PASSes with one low-detail warning. Normal join polish PASSes with one warned row. No overrides, threshold changes or nonexistent sleep options. Five original-source replacement samples were inspected: full frame landscape/sky, no padding or black slab. The initial v01 uncredited component is superseded by v02.

Integration starts from the earlier Orion-repaired chapter, retaining that repair. Saved join and integrated chapter both match all 194 opaque component frames at 320x180: maximum RGB MAE 0.49307, unchanged threshold 2. Full decode and 14,829-frame / 494.30-second count pass. Source and saved output hashes are recorded in the JSON reports. This is not an every-frame visual watch or listening claim.

Full chapter normal polish remains **FAIL: 5 of 78 rows fail, 5 warned rows**. The Chajnantor near-black failure is removed; the remaining failures are the three sphere_dec.jpg spans and two companion_speckle.jpg spans. No gate is waived.

## Next action

Continue from this checkpoint and its cuts.json. Retain all remaining normal gate failures and warnings. Remaining work includes the other dark observation spans, 22 original graphic rows and baked labels, reuse, dissolves, quiet chapter title, inter-film breath, twelve other picture chapters and the initial darkening ramp. Then final compilation/mux, all loudness/peak/silence/CTA/picture/join checks, roughly 12-minute spot-check reel, NAS master/reel safety copies with independent hashes, then finished-film UAT. Existing thirteen narration chapters, 108:22.36 continuous audio candidate and thumbnail are unchanged. Earliest air remains 12 December.

Reproduce with the existing Pillow/numpy environment `/Users/ben/_desk/J2141-venv/bin/python`: build_chajnantor_source_repair.py --out NEW_DIR; run normal picture_qa into NEW_DIR/qa; join_chajnantor_source_repair.py --repair NEW_DIR --out NEW_JOIN; normal polish_gate into NEW_JOIN/POLISH_GATE.json; integrate_chajnantor_source_repair.py --join NEW_JOIN --out NEW_CHAPTER; normal full chapter polish_gate. Scripts refuse overwrite and pin the prior chapter hash. Media is local outside git; JSON evidence is tracked.

Seven email ratchet tests pass; the three scripts compile; diff check passes. Release at this clean checkpoint because the remaining full assembly exceeds one unattended wake. No launched process may remain at release. HOS untouched. Thread read to #6788224847.
