# J2452 — Moon from its finished public picture

Worker `macbook`, 11 November 2026. Compilation incomplete. **No chapter completion, final master, reel, UAT, upload, or spend is claimed.**

The 09:29Z Chief ruling is now the build approach. Start with Moon, then Saturn in running order. Earlier Betelgeuse/Earth/Venus reconstructions remain evidence and do not enter version 1. Public-film charts and labels remain; dissolves are only at this job's new cuts. Carry both limitations onto the eventual watch card.

## Saved candidate — do not render it again

`/Users/ben/_desk/J2452-sleep-scratch/public_moon_v04/013_moon_undarkened_v01.mp4`

`public_moon_build_v04.json` records its actual SHA-256, source master, narration hash, planned versus used cuts, expected 13,209 frames and 440.3-second picture clock. The narration is the existing 440.29-second clean Moon chapter. All six picture spans use exactly its corrected master coordinates; short raw-audio tails hold the last clean frame before the source breath/card/outro. Five 0.4-second dissolves use endpoint handles without overlapping the narration clock. Corrected cuts remove the actual Orbit/agenda/act cards; the old plan's approximate Moon cover windows are not used blindly.

The quiet `I · The Drifting Moon` name fades in for 1.5 seconds, holds three, and fades out for 1.5, in 42-pixel Georgia at 65% warm-white opacity, over the opening picture. Only the 17.9-second first interior was re-encoded for this title; all remaining saved interiors and dissolves were stream copied. `finish_public_moon.py` documents that finishing step. Do not rerun it over its existing output directory.

Moon ends before the 19:30 darkening ramp, so this chapter's darkening operation is identity. Its four-second inter-film breath remains for the final join, outside the narration chapter. It contains clean narration only; the continuous bed, final levels and silence check are still assembly work.

## Next action: finish the current saved-file checks

Run, using the existing environment with numpy and Pillow:

```sh
/Users/ben/_desk/J2141-venv/bin/python jobs/reviews/J2452/check_public_moon.py
```

It runs the normal `polish_gate` across the full saved chapter at two-second intervals including the final partial interval; normal `picture_qa` over half-second samples within two seconds of every new edit/title/hold; actual full decode and frame count before brightness-scan sampling; audio level measurement; and the five brightest two-second windows with a JPEG each. No gate overrides, changed thresholds or nonexistent sleep flags. Gate outputs and `READBACK.json` live beside the candidate. A stopped verifier leaves partial gate reports, not a completed read-back.

Fix any finding at a new edit. List only findings in an untouched public-master stretch more than two seconds from a new edit as “in the public film”, with original master times, under the Chief's ruling. Do not describe a failing overall pixel report as PASS.

After checks, save the chapter and hash/read-back into this film's own NAS working folder, verify the destination hash, and record progress **1 of 15**. Then move to Saturn. No NAS copy or chapter completion was claimed in this checkpoint; see the run's gate checkpoint JSON for exactly which checks finished.

## Preserved local work

- `public_moon_v02/`: six complete source picture slices; first join failed on ffmpeg's `.2` duration syntax, corrected to `0.2` in the committed builder.
- `public_moon_v03/`: complete six interiors, five dissolves, concat list and complete silent joined picture. A redundant whole-chapter title encode was stopped deliberately; its partial AV output is **not** the candidate.
- `public_moon_v04/`: the finished candidate above, efficient title interior, build record and gate outputs.
- `public_moon_v01/`: failed hardware-encoder attempt; never a valid candidate.

No existing media was overwritten or deleted. No source search, generation, login, Studio operation or NAS write. All processes launched by this run are stopped before release. OWB is returned to main; HOS is untouched.
