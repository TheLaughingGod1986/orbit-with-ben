# J2452 — Moon chapter, finished-public-master approach

Worker `macbook`, 11 November 2026. One chapter this run, as ruled by Chief at 09:29Z. The compilation is still incomplete; no final OK, full master, reel, thumbnail or UAT is claimed.

## Saved chapter

Local candidate: `/Users/ben/_desk/J2452-sleep-scratch/public_moon_v06/013_moon_undarkened_v03.mp4`.

NAS destination and matching hashes are recorded in `public_moon_v03/NAS_COPY.json`. The film's `CHAPTER.json` includes the build, full read-back and copied-file hashes. Nothing existing was replaced or deleted.

440.3 seconds, 13,209 frames, SHA-256 `cb7edd7482e8d2b8c2980d6521ace15033c96d844aa596acd32331a46b76d994`. Full decode succeeded with the expected frame count. The chapter precedes the 19:30 darkening ramp, so the delivered undarkened file is also its final chapter picture: identity darkening, unchanged frame count and brightness. Five brightest two-second windows (318–320, 340–342, 364–366, 320–322, 56–58 seconds) have individual local stills and a NAS contact sheet.

Clean narration measures −20.33 LUFS integrated, −8.98 dBTP. These are the measured **input** values, not the loudnorm filter's hypothetical output values. There is no bed in this chapter; the four-second inter-film breath, continuous soft bed and full-film loudness/peak/silence/CTA checks belong to final assembly.

## Gates and the one repair

New-edit picture QA: **PASS**, with six low-detail warnings retained in its report for Chief review. The warning sheet was inspected as stills: the Moon's opening plate/title and the Moon-over-sea plate remain visible. This is not a claim of moving-video or audio perception, nor Chief approval.

Full-chapter polish gate: **FAIL**, with five findings **in the public film**, all more than two seconds from compilation edits. Under the explicit Chief ruling these are recorded and retained, not waived or called PASS:

| Chapter second | Public master second | Finding |
|---|---|---|
| 37 | 65.62625 | horizontal seam |
| 41 | 69.62625 | horizontal seam |
| 165 | 199.57875 | near-black |
| 167 | 201.57875 | near-black |
| 215 | 255.573 | near-black |

The earlier candidate failed new-edit QA at **17.65 seconds**, within two seconds of the first trim: the outgoing public picture was already fading. The repair holds its neighbouring clean frame from 17.0 seconds through the short cover and dissolves into the next kept shot. It changes only the opening interior and first dissolve, without altering the narration clock. An earlier dissolve-only brightness attempt did not fix the actual pre-dissolve frame; it remains local evidence and is excluded. All other interiors and transitions were copied from the saved candidate.

The original checker used ffmpeg's showinfo maximum counter; filter reinitialization at stream-copied segment boundaries reset that counter (7,218 instead of 13,209). Independent ffprobe full decode confirmed 13,209. The checker now disables filter reinitialization for this constant-size stream, fails on decoding errors, and saves its decode log. The repaired file then decoded and counted 13,209 frames in the same pass as its brightness scan. No gate thresholds or overrides changed.

## Resume at Saturn

Record Moon as step **1 of 15**, then process **021 Saturn** from its finished public master and existing corrected narration/cut list. Use the same Chief scope: finished-master picture, only named covers, quiet chapter names, joins and darkening. Do not reuse earlier reconstructed Betelgeuse/Earth/Venus picture in version 1.

The eventual watch card must say: public-film charts/labels remain, and dissolves are only at compilation cuts. Thirteen chapters, join with one bed and final sound/join checks, then reel/copies/watch card are the fifteen steps. No upload or Studio operation; earliest air date remains 12 December. All launched processes finish before release; OWB returns to main, HOS untouched. No source searches, generation, login or spend.
