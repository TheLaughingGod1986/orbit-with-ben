# J3378 — three rebuilt thumbnail proposals

Delivered 22 November 2026 by macbook (Codex). All three v02 JPEGs are on the specified studio-live film paths; source/destination SHA-256 values match. The three v01 candidate hashes were checked before and after delivery and remain unchanged. No Studio writes, generation or spending.

## Changes and visual inspection

- T041: Earth is the large left hemisphere; Europa's rendered limb is about 38.5% of Earth's diameter. The real PIA19048 terminator is retained. Same `2× EARTH'S WATER` hook; thin pointer to Europa; duration area clear.
- T042: `EARTH AGES 7×`; rebuilt from the original 5735-pixel NASA S84-27018 photograph. Large, feathered EVA foreground at 1.5x crop enlargement, dark Earth limb, and 64 resampled photographic star exposures for motion. No vector rays. This is a space-travel metaphor, not a claim that this EVA happened at relativistic speed.
- T043: large pale-gold solar limb and smaller crimson star, with one thin pointer. Both use real SDO texture; the red dwarf is explicitly an illustrative solar proxy, not a resolved photograph of a red dwarf. Apparent size, colour and brightness are editorial comparisons, not measured values. Earth inset removed.

Inspected all three at 168×94 and 360×202 with simulated 9:19, 8:55 and 8:38 badges. Hooks remain readable; text clears the subjects; the duration areas remain clear. The large bodies are deliberately cropped left/bottom as requested. Final creative acceptance belongs to the packaging reviewer and elected Chief.

The first experimental Hubble starfield was rejected after licence verification (ESA CC BY 4.0 is not public domain). Final art uses Mystic Mountain star pixels, with nebular low-frequency signal suppressed. STScI's explicit public-domain release is linked in the manifest. No experimental source is in the final outputs.

## Tool verification

Command (Pillow/numpy environment):

```sh
python 00_Brand/Channel-Setup/tools/thumb_preview.py long /Users/ben/_desk/j3378/final/*_B_v02.jpg --out /Users/ben/_desk/j3378/final/score_sheet.jpg --score
```

```text
PASS  NbW5G1BpPY0_B_v02.jpg  saturation=134.2  near_black=16%
PASS  REXYxuLOBoI_B_v02.jpg  saturation=130.3  near_black=13%
PASS  rVqgtkBV3jc_B_v02.jpg  saturation=129.0  near_black=16%
```

All JPEGs are 1280×720 and below 2 MB. Rebuilding into a second empty directory produced byte-identical candidates and phone sheets. Builder refuses any existing output directory. These are tool-gate results, not Chief approval.

The phone sheets, source cache and score sheet remain under `/Users/ben/_desk/j3378/` on the MacBook; their paths and hashes are in `DESIGN_MANIFEST.json`. Only the three candidate JPEGs were copied to the NAS during daytime, keeping within the handful-of-files restriction. No media is committed to git. Reproduce with the builder's `--sources` and `--out` options; filenames, source IDs, URLs and hashes are recorded in the manifest.

## Ledger and review handoff

T041–T043 were absent from main because original proposal PR #1118 is still open. This change recovers only those three owner-authored proposal rows, retains each entire v01 proposal under `history`, and changes B to the verified v02 file/hash with maker `codex`. Other ledger rows are unchanged. Resolve #1118's overlapping ledger additions by retaining these v02 rows and their history; do not restore v01 over them.

All remain `proposed`, with no start dates or results. Round 1 stays thumbnail-only against unchanged live titles. Round 2 title proposals and pairing guards follow J3306.

**Hold for packaging verification and J3307 exact-file approval plus explicit successor-test authorization before J3308–J3310.** J3307's older brief still names v01: review these manifest v02 hashes instead. J3306 decision is in open PR #1180; this job does not merge either PR or grant approval.
