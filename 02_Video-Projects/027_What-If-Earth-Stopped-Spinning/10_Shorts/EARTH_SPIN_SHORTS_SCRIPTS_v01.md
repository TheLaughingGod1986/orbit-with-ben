# 027 Shorts: scripts v01 (Claude, 5 Oct 2026)

Three Shorts for the week of the 027 long (*What If Earth Stopped Spinning?*, Sun 22 Nov 18:00 London). They're written for **VO now, picture later**, under Ben's 4 Oct order. These are Claude's decisions under the 3 Oct order, and Ben can overrule them.

House rules (the same as 026), plus the Shorts feed lessons in `docs/ORBIT_PLAYBOOK_LESSONS.md` §6 and the **`J2429` First-Second Rule (9 Nov 2026)**:
- **First-second rule (`0.0–1.5 s`, `J2429`):** Frame 0 (`t = 0.00 s`) is a full-bleed `9:16` (`mode: "cover"`, `>=60%` subject, `<=30%` empty black sky, no `fit` letterbox bars, no `16:9` blur-pad bands [`J2421`], no slow fade-in from black, no Orbit at `0.0 s`) moving payoff image (`frame0_diff_0_1_5s >= 1.50`, `frame0_kick_0_0_5s >= 0.40`). The 2–4 word hook caption (white + `#FFE000` yellow highlight word) is already stamped on frame 0 (`t = 0.00 s`), VO word 1 starts at `<= 0.15 s` with `sfx_owb_whoosh_soft_v01.wav`, the spoken hook names Earth/the subject + surprise inside `0.0–1.5 s` (no unanchored pronoun opener like *"This coral..."* and no meta-promise), and Cut 1 lands at `<= 2.5–2.8 s` (`<= 3.0 s` hard gate).
- No Orbit at frame 0. Orbit may arrive from about 1 s.
- Each Short has its own open: frame 0 shows the subject the title names. `gate_shorts_open.py check … --last 10` must pass.
- 22–27 s including the loop hold.
- The exact title is on screen at 9–14 s.
- The Short loops back to its open (`< 1.2 s` tail under `OWB-2026-11-E1`, no spoken end-card CTA on newly re-cut exports).
- Related is set to the long once it's public.
- The hook caption sits on frame 0 (`t = 0.00 s`): two lines, with a yellow hook word.

> **Status of `027` Shorts under `J2429` (9 Nov 2026):**
> - **Scheduled Short:** `lift_equator_weight` (`Dm4xsF1Ateg`, *Why Do You Weigh Less at Earth's Equator?*, `earth_equator_weight_v07.mp4`, scheduled `Mon 23 Nov 11:30Z`) already passes all first-second gates (`J1100` swap).
> - **Unlocked `lift_sudden_air`:** `earth_sudden_air_v03.mp4` (`23.27 s`, `f0diff=6.60`, `cut1=2.50s`, `vo_onset=0.00s`, `visor=0.0`) already passes the `22–27 s` band and all `J2429` first-second checks.
> - **Unlocked reserve lifts (`lift_40000_years`, `lift_ancient_eclipses`, `lift_day_one_year`):** Each unlocked lift folder carries `cuts_v02_first_second_plan.json` enforcing positive question titles, full-bleed `9:16` moving Frame 0, stamped `0.0 s` hook caption, named subject in `<= 1.5 s`, and Cut 1 at `2.20–2.50 s <= 2.8 s`.

All facts come from `../01_Script/SOURCES.md` (`dd053ee`, all rows verified).

| Day (11:30 London) | Title (on screen at 9–14 s, positive question per Keeper + `J2429`) | Hook caption, frame 0 (`t = 0.00 s`) | Cover (adds to the title, no Orbit) | Spoken words |
|---|---|---|---|---:|
| Mon 23 Nov (`Dm4xsF1Ateg` live slot uses *Why Do You Weigh Less at Earth's Equator?*) | Why Are You Moving at 1,000 km/h Right Now? | 1,000 **KM/H** | Yellow **YOU**, white **RIGHT NOW** | 55 |
| Wed 25 Nov | Could a Robot Survive If Earth Stopped Spinning? | THE AIR **KEEPS GOING** | Yellow **1,670 KM/H**, white **WIND** | 58 |
| Fri 27 Nov | Why Did a Day on Earth Last Only 22 Hours? | 22 **HOURS** | Yellow **400**, white **DAYS A YEAR** | 55 |

---

## 1. Mon 23 Nov: You're Moving at 1,000 km/h Right Now

[VISUAL MUST: 0:00. Real NASA ISS time-lapse of Earth already turning, with the day-night line sweeping across Europe. Whoosh. Caption: 1,000 KM/H. No Orbit.]

Right now, you're moving at about a thousand kilometres an hour.

[VISUAL MUST: About 1.5 s. Real footage of a British city at dusk, then an airliner at cruise.]

If you're in Britain, the ground is carrying you east. At the equator, it's faster than a jet airliner.

[VISUAL MUST: A real sunrise time-lapse. The exact title is on screen from 9 to 14 s.]

You don't feel it, because the speed never changes. The Sun doesn't rise. You turn towards it.

[VISUAL MUST: The last 3 s return to the turning Earth.]

The full film: What If Earth Stopped Spinning?

[TEACH: 465.1 m/s at the equator (≈1,674 km/h); × cos 51.5° ≈ 290 m/s ≈ 1,040 km/h in London; airliner cruise ≈ 900 km/h (SOURCES rows 1, 5).]

---

## 2. Wed 25 Nov: Could a Robot Survive If Earth Stopped Spinning?

This Short uses the "Could a Robot…" Wednesday slot, and Orbit is the robot. Orbit's beat reuses the long's North Pole Omni take, because it's the same action ("turning on the spot"). No new Omni is needed.

[VISUAL MUST: 0:00. The real turning Earth from orbit, with a text-free code overlay of air arrows streaming east, longest at the equator. Whoosh. Caption: THE AIR KEEPS GOING. No Orbit.]

Could a robot survive if Earth suddenly stopped spinning?

[VISUAL MUST: About 1.5 s. Real wind-driven spray on a coast. No disaster imagery.]

The rock stops. The air doesn't. At the equator, the wind keeps going at more than fifteen hundred kilometres an hour, faster than sound.

[VISUAL MUST: The exact title is on screen from 9 to 14 s. Then Orbit at the North Pole, turning slowly on the spot (the long's Omni take).]

No robot on the ground there survives that. But at the North Pole, it would barely notice.

[VISUAL MUST: The last 3 s return to the opening Earth with the arrows.]

The full film: What If Earth Stopped Spinning?

[TEACH: Equator ≈ 1,674 km/h vs sound ≈ 1,235 km/h vs the record gust of 408 km/h; surface speed falls to zero at the pole (SOURCES rows 6, 7). A thought experiment: Earth can't stop suddenly.]

---

## 3. Fri 27 Nov: Why Did a Day on Earth Last Only 22 Hours?

[VISUAL MUST: 0:00. Full-bleed `9:16` (`cover` mode, no blur-pad bars) moving close-up of a fossil Devonian coral under a lens with daily growth bands translating across frame (`f0diff >= 1.50`). Whoosh at `0.00 s`. Hook caption stamped at `t = 0.00 s`: 22 **HOURS**. No Orbit.]

On young Earth, a day lasted twenty-two hours — and this 380-million-year-old coral proves it.

[VISUAL MUST: About 1.5 s. A macro of the fine growth lines.]

It grew a fine line every day, and a thicker band every year. Count them, and a year had about four hundred days.

[VISUAL MUST: A text-free code clock dial sweeping a shorter day. The exact title is on screen from 9 to 14 s.]

So a day lasted about twenty-two hours. And Earth is still slowing down.

[VISUAL MUST: The last 3 s return to the opening coral.]

The full film: What If Earth Stopped Spinning?

[TEACH: Wells (1963): Middle Devonian corals show about 400 daily increments per year, so 8,766 h / 400 ≈ 21.9 h; today the day lengthens by about 1.78 ms per century (SOURCES rows 14, 15). Don't mix this up with the 620 Ma Elatina tidalites.]
