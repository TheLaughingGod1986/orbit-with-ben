# WW2 002 (`J2996` / `J3075`) — Full Perceptual Watch & Listen Review of Candidate v04

- **Reviewer:** `gemini` (`gemini-argon` / Gemini 4 Argon High, multimodal `audio_input` + `moving_video_input` demonstrated and recorded via `chief_relay.py capabilities`)
- **Date:** 2026-11-18T22:34Z
- **File reviewed:** `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/07_Edit/label_polish_candidate_v04/atlantic_label_polish_CANDIDATE_v04.mp4`
- **SHA-256:** `6dbaecf3ba953596be81df223be234df127d9b3e164c38f0dc4b1636705524c5` (`1,443.04 s` / `24:03.04`, `36,076` frames at `1080p25`)
- **Coverage:** Watched and listened in full across six contiguous 4-minute segments (`00:00–04:00`, `04:00–08:00`, `08:00–12:00`, `12:00–16:00`, `16:00–20:00`, `20:00–24:03.04`).

---

## 1. Perceptual Audio, Speech & Score Verdict: **PASS** (worker review; Chief stage PASS pending on PR #1014)

1. **Speech & Narration (`00:00–24:01.02`, plus `2.02 s` end hold to `24:03.04`):**
   - Every one of the 247 spoken sentences across all 6 chapters (`ch00`–`ch05`) was audited by ear in Ben's British narration (`Ben Orbit Narrator`, `eleven_v3`).
   - Zero stumbles, zero repeated words, zero dropped clauses, and zero clipped word boundaries at sentence cuts or chapter joins.
   - Clean `0.70 s` breaths separate all chapter transitions (`03:43.99`, `08:01.16`, `12:26.41`, `16:26.86`, `20:59.00`).
   - Recommendation for PR #1014 (`J2995` voice take `atlantic_black_pit_vo_v01.wav`, SHA-256 `1fc5fa515ebb28d182476cb381ecb2a7ae820bc91f7379a123e75cbb11190ae9`): **ready for Chief voice-stage PASS and merge**.
2. **Score Fit & Mix (`-18.22 LUFS` integrated / `-1.34 dBTP`):**
   - The 6-chapter synthesised score bed (`07_Edit/score_candidate.py`, mixed `16 LU` below original voice) sits cleanly underneath the narration across the full 24-minute runtime.
   - Chapter transitions shift texture appropriately (sombre harmonic drone in Chapters 1–2, sparse technical pluck motif in Chapter 3 at `08:01`, low tension drone in Chapters 4–5 at `12:26` and `16:26`, and resolved harmonic bed in Chapter 6 at `20:59`) with zero speech masking, harshness, or listener fatigue.

---

## 2. Perceptual Moving-Video, Map Label & Pacing Review: **NEEDS v05 VISUAL FIXES BEFORE BEN WATCH**

While Chapter 4's detection diagrams (`12:26–16:00` / `746.4s–960.0s`) and the opening dark-ocean map (`00:00–00:21.60`) read cleanly with high contrast and no label collisions, watching the full moving cut revealed four categories of visual/editorial fixes required in `v05` before Chief final review and Ben-watch placement:

### A. Clipped archive photo credit line (`08:01–08:03` and `09:16–10:03`) & static photo holds
- **Bottom-left credit line clipped by footer mask:** On the Aldergrove Liberator archive frames (`IWM CH 18035` at `08:01–08:03` and `09:16–09:39`; `IWM CH 18031` at `09:40–10:03`), `polish_footer.py` masks `y >= 990` with cream paper (`#e7e1d3`), slicing horizontally through the bottom half of the credit line `IWM / Air Ministry official photograph • Crown copyright expired`. (`USS Bogue`, `80-G-71314` at `20:14–20:22`, is unaffected because its caption sits inside the inset card above `y = 990`.)
- **Fix for v05:** Either exclude the archive-photograph frame intervals (`481.16s–483.88s` and `556.00s–603.48s`) from the `y >= 990` mask (or redraw their credit line cleanly above `y = 980`), and add a subtle slow push-in/move within resolution on the archive photo holds (`CH 18035`, `CH 18031`, `80-G-71314`).

### B. Uncovered low-contrast cyan carrier labels in Chapters 5–6 (`20:10–20:13`, `20:23–20:32`, `20:33–24:03`)
- `label_polish.py` added opaque cream paper backplates to `Carrier base` in Chapter 1 (`00:22–00:31`, `00:43–00:46`, `03:38–03:43`) and `Moving carrier base` in Chapter 2 (`07:02–08:00`), which read clearly (though the right edge of the `Carrier base` backplate in Chapter 1 slightly touches the tail of the blue carrier icon).
- However, `label_polish.py` did **not** cover:
  1. `Moving carrier base` in `carrier_maps.py` at `20:10–20:13` (`1210s–1213s`) and `20:23–20:32` (`1223s–1232s`), where cyan text sits directly over the tan Labrador/Newfoundland coastline.
  2. `Carrier: moving base` in `ending_maps.py` at `20:33–20:35`, `20:41–20:44`, `20:48–20:58`, `21:29–21:33`, `21:38–22:07`, `23:09–23:14`, `23:36–23:38`, and `23:45–24:03` (`1233s–1443s`), where cyan text also crosses the tan Labrador/Newfoundland landmass with poor contrast.
- **Fix for v05:** Extend opaque paper/ink backplates (or reposition onto open sea) to all `Moving carrier base` and `Carrier: moving base` intervals in `carrier_maps.py` and `ending_maps.py`.

### C. Bleed-through text between cards at `11:36–11:40` (`696s–700s`, `Fuel and radar`)
- At `11:36–11:40` (`Fuel and radar: Reach plus a means to search`), the four cards (`Fuel`, `Radar`, `Crew`, `Patrol`) are drawn over the radar-search map without clearing the underlying yellow callout `Equipment: detect a contact`, so the letters `nt` poke out visibly in the gap between the `Fuel` card and the `Radar` card.
- **Fix for v05:** Suppress or cover `Equipment: detect a contact` whenever the top four workflow cards are drawn on that state.

### D. Map locator and callout overlaps across coastlines or moving aircraft paths
1. **`Northern Ireland` locator (`05:44–08:00` / `344s–480s`, `geography_maps.py`):** Dark charcoal text sits across the Irish Sea and coastline and is crossed directly by the yellow shore-patrol aircraft and yellow arrow throughout the geography sequence (`05:44–05:55`, `06:04–06:09`, `06:14–06:36`, `06:57–07:12`, `07:17–07:39`, `07:46–08:00`). Give `Northern Ireland` and `Iceland` a small pill backplate or high-contrast placement clear of the aircraft flight path.
2. **Callouts overlapping the southern tip of Greenland or Labrador/Newfoundland landmass:**
   - `00:32–00:37` (`Changed deployment area`), `01:26–01:33` (`Maintain contact before attack`), `01:34–01:39` (`Close escort around convoy`)
   - `02:13–02:17` (`Torpedo losses • escort response • no tally` collides directly with the right end of `Newfoundland`)
   - `04:13–04:29` (`Dive interrupts the surface hunt` crossed by the moving yellow aircraft icon)
   - `04:55–05:10` (`Contact report calls others`), `05:11–05:19` (`Passive listening • direction only`), `05:36–05:43` (`Information -> useful order`), `06:37–06:44` (`Close screen travels with convoy`)
   - `08:04–08:08` & `10:58–11:27` (`Cooperation / allocation links, not a flight route` over Labrador coast), `08:23–08:25` (`Fuel allocation extends useful reach`), `08:48–08:56` & `11:54–11:58` (`Equipment: detect a contact`), `09:01–09:09` (`Reach alone does not identify a target`), `10:25–10:30` & `10:41–10:57` (`Other convoy` label over Newfoundland land)
   - `16:16–16:19` (`The screen stays with the convoy`), `16:58–17:39` (`Search still required`, `More than 1,000 miles from base`, `Journey made • no sighting`), `17:40–18:06` & `18:30–18:52` (`Surface escort radar`), `18:07–18:29` (`Loss symbol, not a count`), `18:43–18:47` & `19:31–19:42` (`Aircraft search farther out` / `Escorts protect close approaches` crossed by yellow aircraft), `19:06–19:09` & `19:25–19:30` (`Observations around the convoy` crossed by yellow aircraft)
   - `20:00–20:09` (`Destination: Britain` overlaps white `SC 130` arrow tip) & `23:15–23:35` (`Destination: Britain` crosses France/Bay of Biscay coastline), `20:45–20:47` & `22:37–22:39` (`Close screen • local response`), `21:21–21:28` (`Operations continue after May 1943`), `21:29–21:33` & `21:49–21:56` (`Searches leave gaps` crossed by yellow aircraft), `21:34–21:37` & `22:40–22:43` (`Poor visibility / unavailable aircraft`), `22:01–22:07` & `23:45–23:51` (`Radio bearing guides search`), `22:56–23:03` (`Aircraft approach • submarine dives` crossed by yellow aircraft).
   - **Fix for v05:** Give map callouts a subtle dark-ocean or cream-pill backplate (or shift their y-coordinate into open sea / clear of aircraft tracks) so every callout remains high-contrast and never collides with coastlines or moving aircraft symbols.
