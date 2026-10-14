# Sun 022 Shorts: scripts v01 (Claude, 4 Oct 2026)

**Retitled 6 Oct 2026 (Claude):** the statement titles below became "specific contradiction" questions (THUMBNAIL_AND_TITLE_RULES.md §1 shape 6, rule 9). Andromeda week tested it: *Why Stars Don't Crash When Galaxies Meet* got 249 views and a 3.6% like rate, the channel's best, while *Is Andromeda Coming to Destroy Us?* got 89. The VO is unchanged; it already opens on the contradiction. The on-screen title at 9–14 s and the listing use the new title.

Three Shorts for the week of the Sun long (*Is the Sun Getting Brighter?*, Sun 18 Oct 18:00 London). Written under Ben's 4 Oct "VO first" order: these are for **VO now, picture later**. Decisions are Claude's under Ben's 3 Oct order; Ben can overrule.

House rules for all three:
- No Orbit at frame 0. `gate_shorts_open.py` must pass.
- 22–27 s with the loop hold.
- The on-screen title is exact at 9–14 s.
- The spoken end line names the long.
- The last seconds return to the open picture so the Short loops.
- Related is set to the Sun long once it is public.
- The hook caption sits on frame 0: 8–10% of the height, at most 80% of the width, two lines, in the upper third.

The numbers are locked to `../01_Script/SOURCES.md` and the long's script v02. New facts are listed under each Short for Gemini's fact-check.

**VO:**
- `orbit_voice.py` LOCK settings (Ben Orbit Narrator, `eleven_v3`, speed 1.04).
- One take per Short; retake only a clipped line.
- Whisper `words.json` is diffed against the spoken lines below.
- Speak only the lines outside the brackets.

| Day (11:30 London) | Title (on screen at 9–14 s) | Hook caption, frame 0 | Spoken words |
|---|---|---|---:|
| Mon 19 Oct | Why Is the Sun Getting Brighter as It Runs Out of Fuel? | IT'S **BRIGHTER** | 55 |
| Wed 21 Oct | Could a Robot Survive Touching the Sun? | TOO **CLOSE** | 58 |
| Fri 23 Oct | Why Didn't Earth Freeze Under a Dimmer Young Sun? | **30%** DIMMER | 51 |

At the house pace (Saturn Short: 53 words in about 23 s), each voice runs about 23–25 s. If a take runs past 25 s, Ben's speed stays at 1.04; the Chief trims pauses to about 0.4 s instead.

---

## 1. Mon 19 Oct: Why Is the Sun Getting Brighter as It Runs Out of Fuel?

| | |
|---|---|
| Promotes | Sun long 022 |
| Frame 0 | SDO disc filling the frame, a prominence already lifting off the limb. Caption IT'S BRIGHTER (yellow BRIGHTER). No Orbit. |
| Cover | SDO disc with a prominence. White **IT BURNS**, yellow **HARDER**. It adds to the title and does not repeat it. No Orbit. |

[VISUAL MUST: 0:00. The SDO disc is already mid-action, with a prominence lifting off the limb. Whoosh on frame 0. Caption: IT'S BRIGHTER. No Orbit.]

The Sun is getting brighter.

[VISUAL MUST: About 1.5 s. Push in towards the disc centre. Orbit (Omni only) may enter small in the lower third, visor tilted up. If Omni is down, stay on the disc.]

And it's running out of fuel.

[VISUAL MUST: The core graphic (`code_graphics.py core`, text-free): four H into one He, the centre tightening. The exact title is on screen from 9 to 14 s.]

Deep in the core, hydrogen fuses into helium.
The helium ash leaves fewer particles holding the core up.
So the core squeezes, heats, and burns faster.

[VISUAL MUST: The three-clocks graph, climb line only (`code_graphics.py clocks`).]

About one percent brighter every hundred and ten million years.

[VISUAL MUST: The last 3 s return to the opening disc and prominence so the Short loops.]

The full film: Is the Sun Getting Brighter?

[TEACH: Core fusion raises the mean mass per particle, so the core contracts and heats, and luminosity rises: about 1% per 110 million years (Schröder & Connon Smith 2008).]

---

## 2. Wed 21 Oct: Could a Robot Survive Touching the Sun?

| | |
|---|---|
| Promotes | Sun long 022 |
| Frame 0 | NASA's Parker Solar Probe artwork (or the WISPR corona pass) already moving against the corona. Caption TOO CLOSE (yellow CLOSE). No Orbit. |
| Orbit | **None (Claude, 4 Oct, PR #99 5982450383).** Omni was unavailable, and the probe is the robot in the title. VO passed and is kept. |
| Cover | The Parker Solar Probe shield against the glare. Yellow **1,400°C**, white **SHIELD**. No Orbit. |

[VISUAL MUST: 0:00. The probe is already in motion, the corona streaming past. Whoosh. Caption: TOO CLOSE. No Orbit.]

Nothing we've built has flown this close to the Sun.

[VISUAL MUST: About 1.5 s. NASA Parker Solar Probe art: the probe turning its heat shield to the Sun. No Orbit.]

Could a robot survive touching it?

[VISUAL MUST: The probe's heat shield faces the Sun. The exact title is on screen from 9 to 14 s.]

Parker Solar Probe passes six million kilometres from the surface.
Its shield takes nearly fourteen hundred degrees.
Behind it, room temperature.

[VISUAL MUST: SDO close-up of granulation, boiling plasma, with no hard edge anywhere.]

But there is no ground to touch. Only gas, hotter than any shield.

[VISUAL MUST: The last 3 s return to the opening probe pass.]

The full film: Is the Sun Getting Brighter?

New facts for Gemini to check:
- Parker's closest pass, 24 Dec 2024: about 6.1 million km (3.8 million miles) from the surface.
- Shield face: up to about 1,377 °C (2,500 °F).
- Instruments: near room temperature (about 29 °C).
- Visible surface: about 5,500 °C, above the melting point of any known shield material.

Source: NASA's Parker Solar Probe pages. Gemini adds the rows to `../01_Script/SOURCES.md`.

---

## 3. Fri 23 Oct: Why Didn't Earth Freeze Under a Dimmer Young Sun?

| | |
|---|---|
| Promotes | Sun long 022 |
| Frame 0 | A dim, graded SDO disc over a dark early sea (a NASA ocean or Earth-limb still, graded cold). Caption 30% DIMMER (yellow 30%). No Orbit. |
| Cover | The dim disc over water. Yellow **FROZEN?**, white **IT WASN'T**. No Orbit. |

[VISUAL MUST: 0:00. The young-Sun grade is already in place over moving water. Whoosh. Caption: 30% DIMMER.]

Four billion years ago, the Sun was about thirty percent dimmer.

[VISUAL MUST: About 1.5 s. Orbit (Omni) small against the dim disc, visor tilted up, asking. If Omni is down, stay on the world.]

Earth should have frozen. It didn't.

[VISUAL MUST: Wet rock and early shoreline stills. The exact title is on screen from 9 to 14 s.]

Rocks nearly that old formed under water.
The usual answer: thicker greenhouse air, holding the heat the weaker sunlight couldn't give.

[VISUAL MUST: The same framing cuts from the dim young disc to today's brighter disc.]

It's been brightening ever since.

[VISUAL MUST: The last 3 s return to the opening dim Sun over water.]

The full film: Is the Sun Getting Brighter?

[TEACH: Standard solar models put the early Sun near 70% of today's light. The faint young Sun paradox is that liquid water existed anyway. Greenhouse gases (CO₂, methane) are the usual answer, and how warm that early air was is still debated.]

New facts for Gemini to check:
- About 3.8 billion years ago, the Isua greenstone belt in Greenland formed sediments and pillow lavas under water. That is "nearly that old" against "four billion years ago".
- Jack Hills zircons, about 4.4 billion years old, hint at liquid water earlier still. Not spoken.
