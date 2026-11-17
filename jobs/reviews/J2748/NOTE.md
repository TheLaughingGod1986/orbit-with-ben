# J2748: Two New History of Science Topic Proposals on the Backlog (Corrected 13 Nov 2026 by `gemini` on Mac mini)

> **Proposal Status & Unverified Claims Notice (`jobs/reviews/J2748/RULING.md`):**
> `HOS:102` and `HOS:103` are **topic proposals only** waiting in `jobs/WIP.json` `next_hos` (Rule G) on OWB PR `#881` and HOS PR `#572`. Neither topic is approved for production yet; both require their Rule-E topic go/no-go review. All historical and scientific claims (including the remembered NASA Nimbus-7 satellite-processing story, Halley Bay Dobson spectrophotometer readings, and the solar-spectrum / ocular-cone explanation for why the sky is not violet) remain **explicitly unverified** and are **not cleared for narration or Short opens** until sourced with exact quotes in `SOURCES.md` and checked via the `facts` lane.

---

## 0. Mandatory Public-Search Preflight Probe (`2026-11-13`, Mac mini)

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "why is the sky blue"
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| why is the sky blue | yes | NASA Space Place 937,917 · Nick Cope 614,123 · SciShow Kids 530,954 · StarTalk 3,394,689 · Netflix Jr. 1,050,542 |
```

---

## 1. Summary of the Five Corrections Completed (`RULING.md` / `REVIEW.md` `d1e1e26ed0`)

1. **Complete Neighbour & Public-Search Evidence (`2026-11-13`):**
   - **`HOS:102` (*How Did We Find the Hole in the Ozone Layer?*):**
     - Saved `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_neighbours.json` (`neighbours.py`: **PASS**, `7` education videos `≥1,000,000` views, `TED-Ed/TED = yes`) and `evidence_2026-11-13_public_search.json` (`public_search.py`).
     - Verified plain search phrases: `"hole in the ozone layer"` (`autocomplete = yes`), `"ozone layer"` (`autocomplete = yes`), `"ozone hole"` (`autocomplete = yes`).
     - Verified ranking videos (`2026-11-13`): `Vox` *Why you don't hear about the ozone layer anymore* (`https://youtu.be/CaLOiGEDPJQ`, **`10,161,545` views**), `Astrum Earth` *Why Nobody Talks About the Ozone Hole Anymore* (`https://youtu.be/EmaQVbdd6Ko`, **`1,673,345` views**), and `TED-Ed` *Whatever happened to the hole in the ozone layer?* (`https://youtu.be/5wVJeq4mLL0`, **`670,049` views`, `#1` GB result for `"hole in the ozone layer"`).
     - On-topic `≥1M`-view education videos (`2026-11-13`): `Veritasium` (`https://youtu.be/IV3dnLzthDA`, **`43,564,438` views**), `Kurzgesagt` (`https://youtu.be/JGXi_9A__Vc`, **`14,084,839` views**), `Vox` (`https://youtu.be/CaLOiGEDPJQ`, **`10,161,545` views**), `Cleo Abram` (`https://youtu.be/yWgHx0HE8m8`, **`8,528,291` views**), `Peekaboo Kidz` (`https://youtu.be/ckULkfv3Hb0`, **`4,284,034` views**), `TED-Ed` (`https://youtu.be/dO2xx-aeZ4w`, **`2,795,894` views**), `Seeker` (`https://youtu.be/0ZfBgjUnXIs`, **`2,494,747` views**), `Astrum Earth` (`https://youtu.be/EmaQVbdd6Ko`, **`1,673,345` views**).
     - Exact title collisions: **`0`** on Long Title A (`How Did We Find the Hole in the Ozone Layer?`), Title B (`The Ozone Hole (Found by an Instrument From the 1950s)`), Title C (`Hole in the Ozone Layer: How a 1950s Ground Instrument Found It`), Short S01 (`Is the Hole in the Ozone Layer Still There?`), and Short S02 (`Why Did a Satellite Miss the Ozone Hole?`).
   - **`HOS:103` (*Why Is the Sky Blue? (And Why It Isn't Violet)*):**
     - Saved `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_neighbours.json` (`neighbours.py`: **PASS**, `8` education videos `≥1,000,000` views, `TED-Ed/TED = yes`) and `evidence_2026-11-13_public_search.json` (`public_search.py`).
     - Verified plain search phrases: `"why is the sky blue"` (`autocomplete = yes`), `"rayleigh scattering"` (`autocomplete = yes`), `"why are sunsets red"` (`autocomplete = yes`), `"Why Is the Sky Blue? (And Why It Isn't Violet)"` (`related autocomplete = "why is the sky blue and not violet"`).
     - Verified ranking videos (`2026-11-13`): `StarTalk` *Neil deGrasse Tyson Explains Why The Sky Is Blue* (`https://youtu.be/UvmWxm3nR6E`, **`3,394,689` views**), `Netflix Jr.` *Why is the Sky Blue | Ask the Storybots* (`https://youtu.be/Ldm_9LsKblU`, **`1,050,550` views**), and `NASA Space Place` *Why Is the Sky Blue?* (`https://youtu.be/ehUIlhKhzDA`, **`937,900` views**).
     - On-topic `≥1M`-view education videos (`2026-11-13`): `Be Smart` (`https://youtu.be/3g246c6Bv58`, **`26,613,295` views**), `Kurzgesagt` (`https://youtu.be/IXxZRZxafEQ`, **`9,990,176` views**), `StarTalk` (`https://youtu.be/UvmWxm3nR6E`, **`3,394,689` views**), `3Blue1Brown` (`https://youtu.be/aXRTczANuIs`, **`1,900,703` views**), `TED-Ed` (`https://youtu.be/J1yIApZtLos`, **`1,816,004` views**), `Veritasium` *Why the Sky ISN'T Blue* (`https://youtu.be/ro2MmmdARrs`, **`1,536,981` views**), `minutephysics` *Why Isn't The Sky Purple?* (`https://youtu.be/R5P6O0pDyMU`, **`1,382,559` views**), `minutephysics` *Why is the Sun Yellow and the Sky Blue?* (`https://youtu.be/NafbGOQBlQs`, **`1,363,672` views**), `TED-Ed` (`https://youtu.be/O0PawPSdk28`, **`1,275,823` views**).
     - Exact title collisions: **`0`** on Long Title A (`Why Is the Sky Blue? (And Why It Isn't Violet)`), Title B (`Why Is the Sky Blue? (The Glass Tube That Solved It)`), Short S01 (`Why Isn't the Sky Violet? (Rayleigh's Puzzle)`), and Short S02 (`Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)`). (Bare `"Why Is the Sky Blue?"`, bare `"Why Isn't the Sky Violet?"`, and bare `"Why Are Sunsets Red?"` collide with live videos and are documented as rejected without their disambiguating tails.)
2. **Corrected Analytics Comparison:**
   - Explicitly states snapshot timestamps (`2026-11-12T06:40:28.196Z` and `2026-11-13T06:40:29.166Z`), lifetime Studio read timestamp (`2026-11-12T07:07:54.728116+00:00`), numerator (`video.views`), and elapsed-day convention (`ageDays = max(daysBetween(publishedAt.slice(0, 10), snapshot.date), 1)`).
   - Consistently ranks all eligible public longs (`002` `2.9/d` on `12 Nov` / `2.8/d` on `13 Nov`, `004` `1.1/d`, `006` Willow `0.6/d` on `12 Nov` [`#3`] / `1.3/d` on `13 Nov` [`#2`] -> `005` Tied Arm `0.4/d` / `0.3/d`, `003` X-rays `0.1/d`, `001` Germs `0.1/d`, plus newly public `007` Vaccine `0.0/d` on `13 Nov`) and all `28` public Shorts by `views/day`, with separate rankings by impressions, CTR, avg % viewed, and stayed-to-watch.
   - Discloses the exact `PFj6172YU4Q` denominator (`215` views / **`4` elapsed days** [`2026-11-08` to `2026-11-12`] = `53.8/day` on `12 Nov`; `216` views / **`5` elapsed days** = `43.2/day` on `13 Nov`).
3. **Hypotheses & `UNKNOWN` Labels:**
   - Treats title and retention patterns as hypotheses; notes that `<10`-view long averages (`001` Germs `7` views, `006` Willow `2` Studio views) cannot establish a winning or losing retention format, that `105.30%` / `112.43%` Short avg viewed is consistent with viewer replay rather than proof of an intentional seamless loop alone, and that `003` (*How Did We Discover X-rays?*) and `001` (*How Did We Discover Germs?*) are plain questions that still sit at `41` and `44` impressions (`0.1/d`).
4. **Explicit Unverified Status of History & Science Claims:**
   - Prominent notices in both `TOPIC.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, and `production-status.md` files state that all historical and scientific claims (including the NASA satellite-processing story and the violet sky explanation) are unverified and not cleared for narration or Short opens until sourced in `SOURCES.md` and checked via the `facts` lane.
5. **Both Existing PRs Updated & Two Substantive Rule-E Review Jobs Queued:**
   - HOS PR `#572`: https://github.com/TheLaughingGod1986/history-of-science/pull/572 (`34324bee`)
   - OWB PR `#881`: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/881
   - Rule-E Review Job for `HOS:102`: **`J2775`** (`--repo hos --film 102 --stage topic --kind review --after J2748`)
   - Rule-E Review Job for `HOS:103`: **`J2776`** (`--repo hos --film 103 --stage topic --kind review --after J2748`)
