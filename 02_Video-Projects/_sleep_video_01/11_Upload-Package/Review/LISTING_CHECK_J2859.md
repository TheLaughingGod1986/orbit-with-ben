# J2859 — Search-Led Listing Verification (`J01_Journey-To-Every-World` v02 & `_sleep_video_01` v01)

## 1. Sleep Film (`_sleep_video_01`) — Verification of Opening Claims Against Build Reports (`J2452`)

The opening two lines of `Descriptions/sleep_video_01_description_v01.txt` are:
> `A slow space documentary for sleep: 108 minutes drifting from the Moon, out through the planets and the nearby stars, to the Andromeda galaxy. Quiet narration over one soft bed of music, a picture that dims after twenty minutes, and no sudden sounds.`

Every claim was verified against the finished build reports in `J2452` (`WATCH_CARD_V01.md`, `RESUME_2026-11-11_PUBLIC_EARTH_SAVED.md`, `FINAL_JOIN_CHECKPOINT_V01.json`, `FINAL_AUDIO_PCM_READBACK_V02.json`, and `final_join_v04/AAC_V05_READBACK.json`):
1. **Runtime & running order (`108 minutes drifting from the Moon ... to the Andromeda galaxy`):**
   - Verified duration: `6,502.333 s` (`108 min 22.333 s`, `195,070` frames at `30 fps`), spanning 13 chapters starting with `013` Moon (`0:00 I · The Drifting Moon`) and ending with `019` Andromeda (`1:37:58 XIII · When Two Galaxies Meet`) plus a `20.0 s` closing fade to black.
2. **Quiet narration over one soft bed of music:**
   - Assembled exclusively from the 13 films' clean discrete narration stems (`013, 021, 027, 025, 023, 031, 020, 022, 028, 029, 024, 026, 019`) over a single continuous low-passed ambient drone bed (`-34` to `-36 LUFS`), with all cold-open stings, agenda lines, subscribe beats, and end-screen CTAs excised (`FINAL_CTA_AUDIT_V01.json`).
3. **A picture that dims after twenty minutes:**
   - Verified in `RESUME_2026-11-11_PUBLIC_EARTH_SAVED.md` and `public_earth_dark_v04/DARKEN_READBACK.json`: Chapter 1 (`013` Moon, `0:00–7:20`) and Chapter 2 (`021` Saturn, `7:24–16:03`) run at 100% source brightness; Chapter 3 (`027` Earth, starting at `16:07.2` / `967.2 s`) applies a 60-second linear 10-bit legal-luma ramp from compilation `19:30` to `20:30` (`1,170.0–1,230.0 s`) reducing brightness to `85%` (`85.16%` measured mean post-`20:30`), and Chapters 4–13 (`23:29–1:48:02`) hold that `85%` darkened grade through the final 20-second fade to black.
4. **No sudden sounds:**
   - Verified in `FINAL_AUDIO_PCM_READBACK_V02.json` and `final_join_v04/AAC_V05_READBACK.json`: zero SFX stems (`stem_sfx = None`), integrated loudness `-20.1 LUFS`, narrow loudness range `2.9 LU LRA`, oversampled true-peak ceiling `-6.4 dBTP` (strictly below `-6.0 dBTP`), and zero silence gaps over 3 seconds (`silence_over_3s: []`).

## 2. Title, Tag & Guard Checks (`J01` v02 and `_sleep_video_01` v01)

| Film | Variant | Title | Length | Plain Phrase First? | Hashtags? | Public Exact Matches (YouTube GB) |
|---|---|---|---:|---|---|---:|
| `J01` Journey (58m) | **Side A (Set First)** | `Space Documentary: A Calm 600-Light-Year Journey From Earth` | `59` (<= 70) | Yes (`Space Documentary`) | None | `0` |
| `J01` Journey (58m) | Held B (Later Test) | `Relaxing Space Documentary: From Earth to Betelgeuse in 58 Minutes` | `66` (<= 70) | Yes (`Relaxing Space Documentary`) | None | `0` |
| `J01` Journey (58m) | Held C (Present A) | `A Calm Journey From Venus to a Dying Star` | `41` (<= 70) | Yes | None | `0` |
| `_sleep_video_01` (108m) | **Side A (Set First)** | `Space Documentary for Sleep: A Slow Journey From the Moon to Andromeda` | `70` (<= 70) | Yes (`Space Documentary for Sleep`) | None | `0` |
| `_sleep_video_01` (108m) | Held B (Later Test) | `Fall Asleep to Space: 13 Calm Stories From the Moon to Andromeda` | `64` (<= 70) | Yes (`Fall Asleep to Space`) | None | `0` |
| `_sleep_video_01` (108m) | Held C (Later Test) | `Space Facts to Fall Asleep To: From the Moon to Andromeda` | `57` (<= 70) | Yes (`Space Facts to Fall Asleep To`) | None | `0` |

- **Journey v02 tags (`Tags/j01_tags_v02.txt`):** `17` tags, `296` characters (`< 500` chars), zero channel names.
- **Sleep v01 tags (`Tags/sleep_video_01_tags_v01.txt`):** `18` tags, `373` characters (`< 500` chars), zero channel names.
- **No "no ads" and no "no AI" claims:** Verified absent across all titles, descriptions, and tags.
- **Note for `J2860` / upload handoff:** Once `J2860` writes `sleep_video_01_master_v02.mp4` (repairing the `97:38` picture window), point `_sleep_video_01/11_Upload-Package/PACKAGE_MANIFEST.json` `video` and `masterSha256` at `sleep_video_01_master_v02.mp4`.
