# J3136 — muon Short bed repair (£0)

Candidate only. YouTube was not touched. The scheduled Private film is `gc1hWQQJOq4` (v05, Sat 21 Nov 2026 11:30Z). `rvug71d7Dqk` is the earlier id, already Private and unscheduled after J2881. Neither id was changed.

## What failed

`fri06_muons_ground_v05` uses `light-speed_score_bed_v01_full.mp3` (`7859c2294b05`). J3128 scored it **0.830** against archived `moon-leaving-part02_score_bed_v01.mp3` (`5093a4c23253`).

## Replacement bed

Own synthesis, no paid generator, no samples: `05_Music/fri06_muons_ground_score_bed_v01.mp3` (`9c67eb4593e3800459af44b914a9344d07e8c1f569194bfe20b12312e7ba242a`), 36.0 s, Pace 72–88 BPM. Confirmed max similarity against the 31 Orbit comparison beds, decoded by `music_gate.py`, is **0.099**.

`music_gate.py` PASS with `--others` set to those 31 beds, including the archived Moon Leaving part 2 file. No fails, no warns. Measured tempo about 133 BPM (double the 80 BPM clock; inside the brief's octave).

## Candidate cut

`fri06_muons_ground_v06.mp4` (`5c85e4430ccd035adb35532291cf5626a5b1d6a8684d8acda213b24c4c378eee`)

- Picture: v05 video stream copied. Frame CRC matches v05 (`1232cb5041f9`). 666 frames, 1080×1920, 22.200 s.
- Voice: locked `_work_v02/stem_vo.wav` (`35826bf888c6`).
- SFX: locked `stem_sfx.wav` (`3315116f10d7`). Bed dropped 27.9 dB so the plucks stay under the voice.
- Mix: −14.4 LUFS, true peak −1.9 dBFS.

Gates: `picture_qa` PASS (0 of 6 fail, 2 to look at, same notes as v05), `polish_gate` PASS (0 of 6 fail, 1 to look at), `sfx_kit.py level` PASS, `gate_shorts_open.py` PASS (`--id gc1hWQQJOq4`, so it does not call the scheduled cut a reused open). Duration warn 22.20 s outside 16–19 s is the same length as v05.

Copies on the shared working-film store, SHA-256 matched: the new bed in `05_Music`, and `v06` in the Short's export folder. v05 was not overwritten.

## Chief decision still open

Swap or leave `gc1hWQQJOq4` on v05. This job does not upload, unschedule, or edit the Private video.
