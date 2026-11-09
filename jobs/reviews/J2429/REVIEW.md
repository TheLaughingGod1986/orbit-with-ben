# J2429 Review — Orbit Shorts First-Second Swipe Audit & Rule (`9 Nov 2026`)

- **Job:** `J2429` (`macbook-2`, `£0` spend)
- **Canonical Audit Report:** [`00_Brand/Channel-Setup/audits/SHORTS_FIRST_SECOND_AUDIT_2026-11-09.md`](../../../00_Brand/Channel-Setup/audits/SHORTS_FIRST_SECOND_AUDIT_2026-11-09.md)
- **Rule & Learnings Updates:**
  - [`.cursor/rules/orbit-build-shorts.mdc`](../../../.cursor/rules/orbit-build-shorts.mdc) — added **The First Second (`0.0–1.5 s`, J2429)** rule block.
  - [`05_Analytics/LEARNINGS.md`](../../../05_Analytics/LEARNINGS.md) — updated `#2` (*The first second (`0.0–1.5 s`): frame 0 = full-bleed motion + hook text, spoken hook under 1.5 s, no slow fade-in*).
- **Ship Gate & Unit Tests:**
  - [`00_Brand/Channel-Setup/tools/gate_shorts_open.py`](../../../00_Brand/Channel-Setup/tools/gate_shorts_open.py) — added `frame0_first_second_verdict` (`frame0_kick_0_0_5s` immediate motion / no slow fade-in from black + `frame0_hook_text` on-screen hook caption presence at `t = 0.15 s`). Synced to `studio-core/LOCK.json` and HOS.
  - [`00_Brand/Channel-Setup/tools/test_gate_stayed.py`](../../../00_Brand/Channel-Setup/tools/test_gate_stayed.py) — added unit tests for slow fade-in / static first `0.5 s` and missing vs present frame-0 on-screen hook text.
- **Unlocked `026`, `027`, `032` Shorts Updated:**
  - [`02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/NEAREST_STAR_SHORTS_SCRIPTS_v01.md`](../../../02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/NEAREST_STAR_SHORTS_SCRIPTS_v01.md) + `cuts_v02_first_second_plan.json` for the 4 unlocked reserve lifts (`lift_earth_pinhead`, `lift_light_4yr`, `lift_red_dwarf`, `lift_walk_900m`).
  - [`02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/EARTH_SPIN_SHORTS_SCRIPTS_v01.md`](../../../02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/EARTH_SPIN_SHORTS_SCRIPTS_v01.md) + `cuts_v02_first_second_plan.json` for the 3 unlocked reserve lifts (`lift_40000_years`, `lift_ancient_eclipses`, `lift_day_one_year`).
  - [`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/SHORTS_PLAN_v01.md`](../../../02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/SHORTS_PLAN_v01.md) and [`README.md`](../../../02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/README.md).
- **Next-14-Day Uploaded Shorts Eligible for Opening Re-Cut / Swap Without Moving Slot (`9–23 Nov 2026`):**
  1. `iyvWYFP_ETA` (`Mon 9 Nov 11:30Z`, *Could a Robot Survive a Night on Mars?*) — fails stayed gate (`f0diff = 0.14 < 1.50`, `cut1 = 4.10 s > 3.0 s`).
  2. `gmzaCfJF1gA` (`Sat 14 Nov 11:30Z`, *Why Does Pluto's Giant Ice Heart Have Zero Craters?*) — fails stayed gate (`f0diff = 0.64 < 1.50`, `cut1 = 5.90 s > 3.0 s`, meta-promise `"stay, and i'll show you"`).
  3. `HZGTovJu_TQ` (`Mon 16 Nov 11:30Z`, *If You Can't See the Nearest Star, How Far Away Is It?*) — YouTube `v01` has `cut1 = 4.80 s > 3.0 s`; passing `v03` (`f0diff = 2.62`, `cut1 = 2.53 s`, `vo_onset = 0.03 s`) is already rendered on disk (`J0935`).
  4. `kKN8Ale42sE` (`Tue 17 Nov 11:30Z`, *How Far From Earth Is Voyager 1 Right Now?*) — fails stayed gate (`f0diff = 0.33 < 1.50`, `cut1 = 4.60 s > 3.0 s`, meta-promise `"stay, and i'll show you"`).
  5. `cwU_0WWeNZ4` (`Wed 18 Nov 11:30Z`, *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?*) — YouTube `v01` has `f0diff = 0.46 < 1.50`; passing `v04` (`f0diff = 1.74`, `cut1 = 2.63 s`, `vo_onset = 0.00 s`) is already rendered on disk (`J0935`).
