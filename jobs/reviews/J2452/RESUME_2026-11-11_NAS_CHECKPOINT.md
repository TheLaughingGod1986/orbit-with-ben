# J2452 — shared checkpoint, 11 November 2026

Worker: macbook. PR #789, branch macbook/J2452. Compilation remains incomplete; no master, spot-check reel, UAT, upload or spend.

## Shared intermediates

`checkpoint_nas_readback_20261111_v01.json` records source and destination sizes and SHA-256 read-back for three additive copies:

- Latest adopted silent 029 chapter, under `_sleep_video_01/j2452/checkpoint_20261111_v01/029_picture_alma_betelgeuse_v02.mp4` on studio-live.
- The 6502.36-second audio candidate in the same folder, `sleep_audio_master_candidate_v01.wav`.
- Official ALMA observation source in 029's `03_Footage/potw1726a_sleep_j2452_v01.jpg`.

All are intermediates. The destination names distinguish them from finished media. Existing source masters and local versions are preserved. The transfer script uses exclusive creation and verifies matching files if resumed; it never overwrites or deletes a destination.

See RESUME_2026-11-11_ALMA.md for observation identity, credit, terms and the adopted picture checkpoint. The matching local chapter cuts and reports remain authoritative; NAS paths do not establish approval. The source pool retains the original source name `potw1726a.jpg`; the NAS copy has an explicit job/version suffix.

## Remaining picture failures

The existing chapter QA still fails seven reuse rows. No new render, gate exemption, or visual approval in this wake. Inspection found **four**, not three, La Silla appearances at source offsets 0, 6.5, 11 and 22 seconds. The source is only 28.053333 seconds long. Four starts separated by the gate's ten-second rule cannot fit, so simply shifting both failed windows is not a valid repair. Retain the current pixels/cuts until a real replacement is selected. The 4.437333-second ALMA Orion clip already occurs at offset zero, so repeating that start also fails reuse. No new source was downloaded or adopted.

Continue from the ALMA checkpoint: fix remaining repeats and retained graphics/labels; finish the other twelve picture chapters, darkening ramp, titles and breaths; join without another chapter encode; run final AV/loudness/peak/silence/CTA/picture/join checks. Build the approximately twelve-minute reel and hash-copy the finished master/reel before Ben's watch card. Earliest air remains 12 December. The audio candidate's recorded -20 LUFS / -6.2 dBTP and absence of measured silence over three seconds are prior component evidence, not a final AV/listening pass.

This wake stops at a clean shared checkpoint because the remaining assembly exceeds its 25-minute cap. All processes launched by this wake must finish before release; restore this checkout to main. HOS untouched.
