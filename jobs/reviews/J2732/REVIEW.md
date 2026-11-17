# J2732 — Next-Morning Snapshot Readout After `J2716`: OWB 025 Mars Wind Short `uhZSRcvngvE` (*How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?*)

- **Job:** `J2732` (`Mars wind Short: read next-morning snapshot after J2716`, `ref: 6831935790`, `after: J2716`, `films: ["OWB:025"]`)
- **Agent:** `macbook-2` (`gemini-argon`)
- **Date:** `2026-11-17`
- **Mode:** Read-only (`£0` spend, zero Studio or YouTube changes)

---

## 1. Next-Morning Snapshot Read (`05_Analytics/owb/snapshots/2026-11-13.json`) & Baseline Comparison

- **Published:** `2026-11-12T11:30:13Z` (Thu 12 Nov 11:30 London), `55 s` (`54.63 s` meta, Chief-approved one-off 50–60 s length test per `studio/RULES.md` → *Packaging* §5).
- **Next-morning snapshot (`05_Analytics/owb/snapshots/2026-11-13.json`, `takenAt: 2026-11-13T06:40:09.513Z`, age `19.17 h`):**
  - **Views:** **`30`** (up from `19` at the `6 h 30 m` Studio check in `J2716`).
  - **Likes / Comments:** **`2` likes**, **`0` comments** (`privacy: "public"`, `format: "short"`, `seconds: 55`).
- **Comparison with channel first-day baselines at comparable ages (`firstMorning`, `0 <= age <= 36 h` in `scripts/launch_check.py`):**
  1. **Recent 10-Short `firstMorning` baseline (`LOOK_BACK = 10`):** Across the 10 earlier Shorts before `uhZSRcvngvE` (`gJwNJN_yMKU` `386`, `_a66uhRDips` `244`, `6dcL5rBmHPM` `44`, `VfDm3E2bUgU` `1,082`, `hZH0C7fpCk4` `513`, `ZpEA8stoSPA` `461`, `T9fVlG3CCzU` `1,234`, `iyvWYFP_ETA` `1,025`, `ffYKoNVPoqg` `32`, `B1z2dv7m7Vk` `59`), the median next-morning views is **`423.5`** (`424` rounded in `launch_check.py judge`).
     - At **`30` views (`30 / 423.5 = 7.08%`)**, `uhZSRcvngvE` is **under one tenth (`< 10%`, i.e. `< 42.35` views)** of the recent 10-Short first-day baseline.
  2. **All-history 24-Short `firstMorning` baseline:** Across all `24` earlier Shorts with a `firstMorning` snapshot, the median is **`77.5` views** (`30 / 77.5 = 38.7%`).
  3. **Studio 6-hour baseline (`J2716`):** At `6 h` (`19` views), Studio reported the channel's usual range at that age as `240–810` (`19 / 240 = 7.92%`, also under one tenth of Studio's usual floor `240`).
- **48-hour+ progression (`2026-11-14.json` through `2026-11-17.json` & `05_Analytics/owb/studio_ctr.json`):**
  - `2026-11-14.json` (`43.17 h`): `51` views, `2` likes, `0` comments.
  - `2026-11-15.json` (`67.17 h`, first snapshot after the `48 h` mark `Sat 14 Nov 11:30Z`), `2026-11-16.json`, and `2026-11-17.json`: **`57` views**, **`2` likes**, **`0` comments**.
  - `05_Analytics/owb/studio_ctr.json`: `57` views, **`41.86%` stayed to watch**, **`0:29` AVD (`52.35%` average viewed)**; YTA through `13 Nov` (`J2827`): `35` views (`22` `YT_SEARCH` [`62.9%`], `13` `SHORTS` [`37.1%`]), `0:41` AVD (`74.75%` YTA average viewed). All `<100` views = descriptive only.

---

## 2. Methodological Guards (`6831935790` / `J2732`)

1. **Shown-in-feed was not observed in the 6-hour Studio check (`J2716`):** Studio showed no separate `Shown in feed` card on `12 Nov`. The `~19` figure printed by `launch_check.py` (`10` feed views `/ 53.3%` stayed) is a calculated estimate, **not** a Studio measurement.
2. **Small samples and the different duration do not establish causality:** With `<100` views (`19` at 6 h, `30` next morning, `57` at 48 h+) and multiple simultaneous confounders (`55 s` length vs `18–27 s`, a static pushed frame-0 still `PIA22909.jpg` + `4.33 s` static Shot 2 `PIA17759.jpg`, Thursday slot, second upload replacing `N42gKBbD7tE`, and airing 24 hours after `B1z2dv7m7Vk` on the same `"90-Day Rover / 14 Years"` angle), this single Short does not establish that a `50–60 s` duration caused the low feed reach.
3. **Full-week length experiment preserved:** No changes to title, edit, upload, test, privacy, or schedule. The 48-hour figures are logged in `00_Brand/Channel-Setup/audits/SHORT_LENGTH_TEST_2026-11/TEST_LOG.md`, and the 7-day readouts remain scheduled for `2026-11-20` (after `Thu 19 Nov 11:30Z` for `uhZSRcvngvE`) and `2026-11-22` (after `Sat 21 Nov 11:30Z` for `RT-ec4_GcOk`).

---

## 3. Subject/Title Hypothesis Carried Into Topic Review (`6831935790`)

- **Evidence across the `025` Mars Short cluster:**
  - Mon 9 Nov `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?*, `26 s`): **`1,025`** next-morning views, **`1,065`** at 48 h, **`1,074`** at 7 d (`96%` Shorts feed).
  - Wed 11 Nov `B1z2dv7m7Vk` (*Why Did a 90-Day Mars Rover Last 14 Years?*, `27 s`): **`59`** next-morning views, **`103`** at 48 h (`52.69%` stayed, `72.67%` Studio avg viewed).
  - Thu 12 Nov `uhZSRcvngvE` (*How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?*, `55 s`): **`30`** next-morning views (`7.08%` of recent 10-Short median `423.5`), **`57`** at 48 h+.
  - Sat 14 Nov `RT-ec4_GcOk` (*How Did a Helicopter Fly 72 Times on Mars?*, `27 s` / `18.00 s` cut): **`1,033`** views at 6 h (`92.7%` feed), **`1,118`** next-morning views, **`1,249`** at 67 h (`50.70%` stayed, `100.07%` Studio avg viewed).
- **Takeaway carried into topic review:** Because `iyvWYFP_ETA` (`1,025` next morning) and `RT-ec4_GcOk` (`1,118` next morning, 5 days after `iyvWYFP_ETA` on a distinct machine, `Ingenuity Helicopter`) were both strongly fed, the Shorts feed did **not** suppress Mars as a planet subject. Rather, airing two Shorts on consecutive days (`11 Nov` and `12 Nov`) with the near-identical `"90-Day Rover / 14 Years"` Opportunity title/sub-angle coincided with small feed trials.
- **Recorded in:**
  1. `05_Analytics/owb/launch/uhZSRcvngvE.json` (via `launch_check.py note uhZSRcvngvE`).
  2. `00_Brand/Channel-Setup/audits/SHORT_LENGTH_TEST_2026-11/TEST_LOG.md` (table + morning/48 h readout section).
  3. `02_Video-Projects/070_Every-Mars-Rover-Explained-In-10-Minutes/TOPIC.md` (§2.7) and `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` (Gate 5), alongside `05_Analytics/LEARNINGS.md` Learning 33.
