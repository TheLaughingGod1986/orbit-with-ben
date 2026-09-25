# Moon Leaving full v04 — house lock (15 Sep 2026)

**Locked:** 15 Sep 2026 · Europe/London
**Status:** Ben KEEP/LOCK after Orbit Auditor **HARD PASS**. Softs accepted; shipped.
**Scope:** Standing lessons for **every future Orbit long** (assembly · remint · end hold · chapter cards · ocean POV · join tech), plus a film-specific Shorts note that is **not** a global Shorts rule change.

Ship gate: `.cursor/rules/orbit-auditor-ship-gate.mdc`
House / UAT bible: `ORBIT_HOUSE_AND_UAT_BIBLE.md`
Open / end craft: `.cursor/rules/orbit-longform-open-end-affiliate.mdc`
Picture QA: `.cursor/rules/orbit-omni-section-qa.mdc`

Cursor follows this file as-is on future runs. **Do not ping Chief of Staff** unless Ben asks or a lock must be broken. This is a lessons/UAT doc — **do not remint or re-cut any live film from it**, and do not touch live Studio assets.

---

## Locked deliverable

| Field | Value |
|-------|-------|
| File | `OWB UAT/moon_leaving_full_rough_v04.mp4` (= `moon_leaving_full_LOCKED_v04.mp4`) |
| sha256 | `dbd3bd77f21b61afca3e60c5886c660fb6127e7c561e6c7d156aa2c0d5e4f401` |
| Duration | ~**518.81s** |
| Format | **1920×1080 stereo** |
| Listing title | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone |

The master lives on the Mac mini under `OWB UAT/`; this repo holds the lessons, not the file.

---

## Standing lessons (apply to every future long)

### Audio

1. **Remint = video only.** Never replace a mid-film remint plate with `-c copy` of the remint's own audio. Map **video from the remint, audio from the original part** — Flow/Veo ambient wipes the VO underneath.

   ```bash
   # remint plate picture + original part audio
   ffmpeg -i part04_remint_v02.mp4 -i part04_original.mp4 \
     -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy part04_joined_v03.mp4
   ```

2. **End holds carry music that fades — never silence.** A silent picture hold after the last VO line reads as a hard cut / broken file, not an ending.
3. **Bed parity across parts.** P02/P04 beds must be mixed into the same ballpark as P01/P03 (~**−20 dB mean** under VO). A sparse bed alone is not a mix — the film audibly thins at the part seam.

### Chapter cards

4. **Breath lead-in.** Give each card ~**1.5s** of lead-in (hold the last frame / let the music continue) so the VO is never chopped into the card.
5. **Soft cinematic cards.** Space gradient / starfield plate with soft type. **Not** flat black with a hard text box.
6. **Quiet music under the card.** The bed never goes dead-silent across a card.

### Picture / POV

7. **Dual-body gate.** One Earth + one Moon, or one Moon only. Extra moons or extra Earths in frame = FAIL and regen.
8. **Ocean / shore POV house rule (hard).** If the camera is **standing on Earth's ocean or shore**, there is **no Earth globe in the sky**. You are on Earth — you cannot see it above the horizon.
   - Prompt language to use: *"shore under ONE Moon, starry sky, NO Earth globe, NO planet Earth in background."*
   - The failure mode is a **water → Earth → Moon stack**: rocks/water in the foreground, an Earth globe hanging above the mist, Moon behind it. Remints invent this even when the source plate was clean.
   - **Mid-plate gate:** check a mid-plate frame (not only first/last) before locking any shore/ocean plate.
   - On Moon Leaving v04 this survived as an **accepted soft** because Ben shipped the film. It does **not** carry forward: on any future build or remint it is a hard FAIL (`orbit-auditor-ship-gate.mdc`).
9. **Outro shape.** ≥**15–20s** of slow picture after the last VO line · music fades over ~**10s** · picture fades to black over the last ~**2s**. No baked subscribe card (Studio end screens only).

### Join tech

10. **Normalize before concat.** Every input normalized to **1920×1080 stereo** before joining. Mixing 720p mono with 1080p stereo produces the hitch/pause at the seam.
11. **Verify A/V durations match after concat.** Video running past audio on the tail is a silent-ending fail — probe both streams, don't trust the container duration alone.

    ```bash
    ffprobe -v error -select_streams v:0 -show_entries stream=duration,width,height -of default=nw=1 out.mp4
    ffprobe -v error -select_streams a:0 -show_entries stream=duration,channels -of default=nw=1 out.mp4
    ```

12. **CopyFromBox truncates large MP4s.** When moving remints between the Mac mini and box, **chunk ≤500KB**, reassemble, and **verify sha256** against the source before using the file. A truncated MP4 can still play and still be the wrong file.

---

## Film-specific (Moon Leaving week only — not a rule change)

13. **Shorts seven-pack locked for this film:** 3.8 CM A YEAR · LEAVING US? · DAY WAS HOURS · THE BULGE PULLS · FOSSIL CLOCK · RINGS OF FIRE · PERFECT COVER ENDS.
14. **Ben override (this film):** Related pill **and** a pinned comment to the Premiere. The standing house rule stays **Related-only, no new Short pins** (`.cursor/rules/orbit-shorts-related-video.mdc`) — do not generalise this override to other weeks, and do not FAIL this week's Shorts for carrying the pin Ben asked for.
15. **Schedule:** Fri–Tue (or Fri–Thu) **11:30 Europe/London** with `publishAt`; Related = that Thursday Premiere.

---

## Softs accepted on this lock (not FAIL)

| Soft | Note |
|------|------|
| Orbit CU ~32s | Accepted on this cut |
| Ruler numerals | Accepted on this cut |
| Music under cards / outro | Accepted; hardened as lessons 4–6 and 9 going forward |
| Shore Earth+Moon stack | Accepted by Ben on this cut only. **Hard FAIL on future builds / remints** (lesson 8) |

Accepted softs are cut-specific. They are not precedent and they do not lower the gate for the next film.
