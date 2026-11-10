# Nearest-star 026 Shorts: scripts v01 (Claude, 4 Oct 2026)

**Retitled 6 Oct 2026 (Claude):** the statement titles below became "specific contradiction" questions (THUMBNAIL_AND_TITLE_RULES.md §1 shape 6, rule 9). Andromeda week tested it: *Why Stars Don't Crash When Galaxies Meet* got 249 views and a 3.6% like rate, the channel's best, while *Is Andromeda Coming to Destroy Us?* got 89. The VO is unchanged; it already opens on the contradiction. The on-screen title at 9–14 s and the listing use the new title.

Three Shorts for the week of the 026 long (*How Far Is the Nearest Star?*, Sun 15 Nov 18:00 London). Written for **VO now, picture later**, under Ben's 4 Oct order. These are Claude's decisions under the 3 Oct order, and Ben can overrule.

House rules, the same as `022/10_Shorts/SUN_SHORTS_SCRIPTS_v01.md`, updated for the **`J2429` First-Second Rule (9 Nov 2026)**:
- **First-second rule (`0.0–1.5 s`, `J2429`):** Frame 0 (`t = 0.00 s`) is a full-bleed `9:16` (`mode: "cover"`, `>=60%` subject, `<=30%` empty black sky, no `fit` letterbox bars, no `16:9` blur-pad bands [`J2421`], no slow fade-in from black, no Orbit at `0.0 s`) moving payoff image (`frame0_diff_0_1_5s >= 1.50`, `frame0_kick_0_0_5s >= 0.40`). The 2–4 word hook caption (white + `#FFE000` yellow highlight word) is already stamped on frame 0 (`t = 0.00 s`), VO word 1 starts at `<= 0.15 s` with `sfx_owb_whoosh_soft_v01.wav`, the spoken hook names the star/subject + surprise inside `0.0–1.5 s` with zero meta-promise, and Cut 1 lands at `<= 2.5–2.8 s` (`<= 3.0 s` hard gate).
- No Orbit at frame 0. `gate_shorts_open.py` must pass.
- 22–27 s.
- The exact title is on screen at 9–14 s.
- The Short loops back to its open (`< 1.2 s` tail under `OWB-2026-11-E1`, no spoken end-card CTA on newly re-cut exports).
- Related is set to the long once it is public.
- The hook caption sits on frame 0 (`t = 0.00 s`), two lines, with a yellow hook word.

> **Status of `026` Shorts under `J2429` (9 Nov 2026):**
> - **Scheduled weekday Shorts:** `mon16_cant_see_nearest_star` (`HZGTovJu_TQ`, `v03` staged on disk with `f0diff=2.62, cut1=2.53s, vo_onset=0.03s`), `wed18_robot_reach_nearest_star` (`cwU_0WWeNZ4`, `v04` staged on disk with `f0diff=1.74, cut1=2.63s, vo_onset=0.00s`), and `fri20_grapefruit_cherry` (`aAUgIGEuPwQ`, `v04` live/scheduled on YouTube, `f0diff=3.58, cut1=2.37s`).
> - **Unlocked reserve lifts (`lift_earth_pinhead`, `lift_light_4yr`, `lift_red_dwarf`, `lift_walk_900m`):** Each unlocked lift folder carries `cuts_v02_first_second_plan.json` splitting Shot 1 at `2.20–2.50 s <= 2.8 s` over full-bleed `9:16` moving footage with stamped `0.0 s` hook text and `<= 0.15 s` VO onset.

The facts come from `../01_Script/SOURCES.md`. VO waits for Gemini's check and Claude's `Locked: VO`.

| Day (11:30 London) | Title (on screen at 9–14 s) | Hook caption, frame 0 | Cover (adds to the title, no Orbit) | Spoken words |
|---|---|---|---|---:|
| Mon 16 Nov | Why Can't You See the Nearest Star? | TOO **FAINT** | Yellow **4.24**, white **LIGHT-YEARS** | 53 |
| Wed 18 Nov | Could a Robot Reach the Nearest Star? | 75,000 **YEARS** | Yellow **17 KM/S**, white **NOT ENOUGH** | 52 |
| Fri 20 Nov | If the Sun Were a Grapefruit, Where's the Nearest Star? | A **CHERRY** | Yellow **4,000 KM**, white **AWAY** | 50 |

---

## 1. Mon 16 Nov: Why Can't You See the Nearest Star?

[VISUAL MUST: 0:00. A real night-sky time-lapse already turning. Whoosh. Caption: TOO FAINT. No Orbit.]

The nearest star to the Sun is out there tonight. You can't see it.

[VISUAL MUST: About 1.5 s. Push into a dense southern star field. Orbit (Omni on Vertex only) may peer through a tiny telescope. If Omni is unavailable, stay on the sky.]

It's called Proxima Centauri, a small red dwarf.

[VISUAL MUST: A telescope image of Proxima, small and red. The exact title is on screen from 9 to 14 s.]

It gives out less than one percent of the Sun's light.
Its light still takes more than four years to reach you.

[VISUAL MUST: The last 3 s return to the opening sky.]

The full film: How Far Is the Nearest Star?

[TEACH: Proxima V ≈ 11 (naked-eye limit about 6); L ≈ 0.0017 L☉; 4.24 ly (Gaia).]

---

## 2. Wed 18 Nov: Could a Robot Reach the Nearest Star?

Uses the "Could a Robot…" slot. Voyager 1 is the robot. **No Orbit is needed.**

[VISUAL MUST: 0:00. NASA Voyager art, the craft already moving against the stars. Whoosh. Caption: 75,000 YEARS. No Orbit.]

Our fastest robot leaving the solar system is Voyager 1.

[VISUAL MUST: About 1.5 s. The 1977 Voyager launch (NASA archive footage, muted).]

Could a robot like it reach the nearest star?

[VISUAL MUST: Voyager against a deep star field. The exact title is on screen from 9 to 14 s.]

Voyager moves seventeen kilometres every second.
At that speed, the trip would take about seventy-five thousand years.
And Voyager isn't even heading that way.

[VISUAL MUST: The last 3 s return to the opening Voyager pass.]

The full film: How Far Is the Nearest Star?

[TEACH: Voyager 1 is at about 16.9 km/s; 4.018 × 10¹³ km / 16.9 km/s ≈ 75,000 yr. It is headed towards Ophiuchus/Camelopardalis, not Proxima (NASA JPL).]

---

## 3. Fri 20 Nov: If the Sun Were a Grapefruit, Where's the Nearest Star?

[VISUAL MUST: 0:00. A real grapefruit on a table, the camera already sliding past it. Whoosh. Caption: A CHERRY. No Orbit.]

Shrink the Sun to the size of a grapefruit.

[VISUAL MUST: About 1.5 s. A pin far across a long room.]

Earth is a pinhead fifteen metres away.
The nearest star becomes a cherry.

[VISUAL MUST: A cherry on a plain surface. The exact title is on screen from 9 to 14 s.]

Where is it?
About four thousand kilometres away. Put the grapefruit in London, and the cherry is past Cairo.

[VISUAL MUST: A satellite-map pull-back from London to Cairo (NASA imagery), no text. The last 3 s return to the grapefruit.]

The full film: How Far Is the Nearest Star?

[TEACH: Scale 1 : 10¹⁰: Sun 13.9 cm, Earth at 15 m, Proxima (0.154 R☉) 2.1 cm at about 4,018 km; London–Cairo is about 3,500 km.]
