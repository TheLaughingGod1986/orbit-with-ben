# Sun 022: SHOT_LIST v01 (Claude, 7 Oct 2026)

**Film:** 022 *Is the Sun Getting Brighter?* · airs **Sun 18 Oct 18:00 London** · cut review **Sat 10 Oct** · final OK **Tue 13 Oct**  
**VO lock:** `02_Voiceover/words.json` (502.64 s, 1270 words) · **Script:** `01_Script/sun_brighter_script_master_v02.md`  
**Built by:** `_build_shot_list_v01.py` (re-run it after any change; it checks every rule below and writes nothing on a FAIL). The machine-readable list is `shot_list_v01.csv` (Saturn's columns, plus chapter, grade and fallback).

Written by Claude because no shot list existed and Grok is out of credit. **Claude PASSes it as written**; the assembler (Cursor while Grok is out) builds the first cut from the CSV, Thu 8-Fri 9 Oct.

## Rules this list keeps

| Rule | How |
|---|---|
| Frame 0 | Real SDO motion, **SVS 10925**, eruption already rising. No fade, no title, no Orbit. |
| Pace | A new picture every 4-6 s, cut on the gap before a word (never mid-word). Preview cuts from 1.5 s inside the first 20 s. |
| Chapter cards | Lower third, ~2.5 s, over the chapter's first shot, with the 0.7 s breath before it. No full-screen card. |
| Stills | 16:9 fill with feathered blur, upscale at most about 2.35x, Ken Burns move as listed. Crop the SDO corner timestamp with the push. |
| SVS motion | Muted, clean stretches with no on-screen text, credit 'NASA's Goddard Space Flight Center' + instrument. Max 2 stretches per clip. |
| Sunspots | Only over the 0.1% wobble lines, never the 1% climb. |
| Young / future Sun | One SDO disc **graded** (young -30% and cooler; future +10%, scale 1.04). **No red giant.** |
| Orbit | Two Omni beats only (ch.3 and ch.4), small in frame, Vertex free credit only. **If Omni is down, use each row's fallback** and stay on the world pictures (plan, 3 Oct). |
| Code graphics | `code_graphics.py` outputs: `zoom_nolabels.mp4` (ch.1), `core_nolabels.mp4` (ch.2, two passes), `clocks.mp4` (ch.5). |
| End | Back to the opening Sun in motion (SVS 10925, a different stretch), held 16 s past the last word; end screen added in Studio. |
| Mix | -14 LUFS, music the full runtime, fade under the last line. |

## Shots

| # | VO in-out (s) | Source | Picture | Move / stretch | Over the words | Card | Grade / fallback |
|---:|---|---|---|---|---|---|---|
| 1 | 0.00-5.46 | GODDARD | SVS 10925 | stretch 1: eruption already rising off the limb at frame 0 | The sun is getting brighter. Why does it brighten while it runs down? |  | fallback: SVS 11517 |
| 2 | 5.46-7.56 | NASA | iss074e0494675 | push 4% | You are looking at the light on your face |  |  |
| 3 | 7.56-11.12 | GODDARD | SVS 11517 | stretch 1: graceful eruption mid-rise | and a prominence is already lifting off the limb. |  |  |
| 4 | 11.12-16.56 | NASA | GSFC_20171208_Archive_e002168 | push 5% | The danger is not that ribbon. The danger is a slow climb that is already true. |  |  |
| 5 | 16.56-18.20 | NASA | PIA21783 | pull 4% | It is not the spots. |  |  |
| 6 | 18.20-21.50 | NASA | s85e5052 | pan L-R 4% | It is not the warming of a human century. |  |  |
| 7 | 21.50-25.18 | NASA | GSFC_20171208_Archive_e002035 | push 4% | In this film, I will show you why the light rises, |  |  |
| 8 | 25.18-30.82 | NASA | PIA22123 | pull 5% | what the sky was like under a fainter sun and what happens as it keeps climbing. |  |  |
| 9 | 30.82-34.74 | GODDARD | SVS 13778 | stretch 1: prominence eruption (mute: licensed music) | The motion is real and it is the wrong clock. | The Climb You Cannot See | fallback: SVS 11517 stretch 2 |
| 10 | 34.74-38.56 | NASA | PIA22123 | drift up 4% | A prominence is plasma held in the sun's magnetic field. |  |  |
| 11 | 38.56-43.88 | NASA | GSFC_20171208_Archive_e001052 | push 5% | It can hang, fall back or break away. In a day, it is over. |  |  |
| 12 | 43.88-49.28 | NASA | GSFC_20171208_Archive_e000970 | pan L-R 4% | Your eyes are built for that. They are not built for the change in the title. |  |  |
| 13 | 49.28-55.42 | NASA | GSFC_20171208_Archive_e002035 | push 5% | So is the sun getting brighter? Yes. Not by a ribbon you could watch from the garden, |  |  |
| 14 | 55.42-59.12 | CODE | zoom_nolabels.mp4 | 0-12 s (no baked captions: VISUAL MUST) | by a slow rise in the light of the whole star, |  |  |
| 15 | 59.12-63.36 | NASA | PIA20881 | drift up 4% | about 1 % brighter in every 110 million years, |  |  |
| 16 | 63.36-68.44 | NASA | s85e5052 | push 5% | as it uses its hydrogen. Schroeder and Conn and Smith published that |  |  |
| 17 | 68.44-73.48 | NASA | GSFC_20171208_Archive_e001363 | pan L-R 4% | pace in 2008 in a model of the sun's long life. |  |  |
| 18 | 73.48-78.42 | GODDARD | SVS 3548 | solar minimum, then cut to SVS 3549 maximum | What if the spots were the whole story? They are not. Across a cycle |  |  |
| 19 | 78.42-84.72 | NASA | PIA22662 | pan R-L 4% | of about 11 years, the total light wobbles by about a 10th of 1%. |  |  |
| 20 | 84.72-91.10 | GODDARD | SVS 3549 | solar maximum | Spots darken a patch, brighter faculae make up the rest and a little more. |  |  |
| 21 | 91.10-97.20 | NASA | PIA22123 | push 5% | The wobble rises, falls and comes back. It is not a climb. |  |  |
| 22 | 97.20-102.18 | NASA | iss017e011603 | pan R-L 4% | The warming measured on earth is a different ledger written in the air over decades. |  |  |
| 23 | 102.18-106.96 | NASA | GSFC_20171208_Archive_e001052 | pull 5% | This film does not say the sun has brightened enough in your lifetime |  |  |
| 24 | 106.96-111.04 | NASA | GSFC_20171208_Archive_e000970 | pan R-L 4% | to be that warming. Across a human life, |  |  |
| 25 | 111.04-115.06 | NASA | PIA20881 | drift up 4% | the 1 % climb is far smaller than the sunspot wobble. |  |  |
| 26 | 115.06-118.68 | NASA | s85e5052 | push 5% | You will not see it and you will not feel it. |  |  |
| 27 | 118.68-124.92 | NASA | GSFC_20171208_Archive_e002035 | pull 5% | Now the strange question. Why would a star brighten while its fuel is running down? |  |  |
| 28 | 124.92-128.58 | GODDARD | SVS 31400 | stretch 1: churning interior flows | The fuel is hydrogen. The ash is helium. | Brighter While It Runs Down |  |
| 29 | 128.58-133.84 | NASA | PIA20881 | pan R-L 4% | The change sits in the core where the disc you see cannot show it. |  |  |
| 30 | 133.84-138.56 | CODE | core_nolabels.mp4 | 0-12 s: H to He, core tightening (no text) | Deep inside, the sun is fusing hydrogen into helium. |  |  |
| 31 | 138.56-143.90 | NASA | PIA22662 | push 5% | The net of the proton -proton chain is simple enough to say aloud. |  |  |
| 32 | 143.90-148.40 | NASA | PIA22645 | pan L-R 4% | Four hydrogen nuclei become one helium nucleus. |  |  |
| 33 | 148.40-153.18 | NASA | PIA21764 | pull 5% | A little mass becomes energy and that energy is the light. |  |  |
| 34 | 153.18-157.30 | NASA | iss074e0494675 | pan L-R 4% | The radiation that leaves the surface takes eight minutes to reach you. |  |  |
| 35 | 157.30-161.08 | NASA | GSFC_20171208_Archive_e001978 | drift up 4% | The energy was made long before that. |  |  |
| 36 | 161.08-166.22 | GODDARD | SVS 31400 | stretch 2 | Here is the turn. Helium is not a second sort of hydrogen. |  |  |
| 37 | 166.22-171.32 | NASA | PIA22360 | pan L-R 4% | Each helium nucleus locks up more mass in fewer particles. |  |  |
| 38 | 171.32-176.36 | NASA | PIA15377 | pull 5% | As the core fills with ash, fewer particles remain to hold the star up against |  |  |
| 39 | 176.36-181.54 | NASA | PIA22724 | pan R-L 4% | gravity. Pressure would fall unless something else rose. |  |  |
| 40 | 181.54-185.46 | CODE | core_nolabels.mp4 | second pass from 6 s: the core tightens and the light floods out | So the core contracts a little. It heats. |  |  |
| 41 | 185.46-190.32 | NASA | GSFC_20171208_Archive_e000808 | push 5% | Hotter hydrogen fuses faster. Faster fusion releases more |  |  |
| 42 | 190.32-195.40 | NASA | GSFC_20171208_Archive_e000393 | pan L-R 4% | energy and the star brightens. The sun brightens because it is |  |  |
| 43 | 195.40-201.94 | NASA | PIA22662 | pull 5% | running down. The waste in the middle leaves the fire no choice but to burn harder. |  |  |
| 44 | 201.94-207.12 | GODDARD | SVS 11112 | gradient Sun | That is the first payoff. The tank is not dimming as it empties. |  |  |
| 45 | 207.12-211.76 | NASA | PIA22645 | drift up 4% | About 1 % more light in every 110 million years. |  |  |
| 46 | 211.76-218.14 | NASA | PIA21764 | push 5% | For as long as this remains the star you know. The spectrum drifts only a little hotter. |  |  |
| 47 | 218.14-223.30 | NASA | GSFC_20171208_Archive_e001978 | pan L-R 4% | What changes is the amount of light, not a new color on a walk. |  |  |
| 48 | 223.30-226.82 | NASA | GSFC_20171208_Archive_e002035 | push 6% | What would you see across a hundred million years? |  |  |
| 49 | 226.82-232.12 | NASA | PIA22360 | pan R-L 4% | Almost nothing at first, then a sun about 1 % more severe. |  |  |
| 50 | 232.12-236.90 | NASA | PIA15377 | drift up 4% | No mystery in it, just mass, gravity and ash. |  |  |
| 51 | 236.90-242.38 | GODDARD | SVS 5649 | stretch 1: restless disc (no on-screen text) | We make one of these every week. Subscribing is how the next one finds you. |  |  |
| 52 | 242.38-248.44 | NASA | s09-11-675 | push 4% | But the sun over your street is not the sun that a young earth knew. |  |  |
| 53 | 248.44-254.44 | NASA | GSFC_20171208_Archive_e002035 | pull 5% | Wind the clock back. When earth was young, this same star was fainter. | When the Light Was Less | young Sun: -30% brightness, slightly cooler (orange-ward) |
| 54 | 254.44-259.32 | GODDARD | SVS 11853 | faint young Sun stretch, picture only (mute, no text frames) | Solar models put the early sun near 70 % of today's light. |  | fallback: NASA GSFC_20171208_Archive_e000888 |
| 55 | 259.32-264.02 | NASA | as4-01-750 | drift up 4% | Roughly 30 % dimmer than the disk in your sky. |  |  |
| 56 | 264.02-267.98 | NASA | s04-41-1206 | push 5% | The 1 % rule is today's pace. It is not a flat rate. |  |  |
| 57 | 267.98-274.48 | NASA | sl4-142-4577 | pan L-R 4% | You can run backwards across the whole life of the star. The young sun was the dimmer one. |  |  |
| 58 | 274.48-279.36 | NASA | GSFC_20171208_Archive_e000888 | push 5% | Then the paradox arrives. A star that faint should have left the |  |  |
| 59 | 279.36-283.38 | NASA | S66-25771 | pan R-L 4% | early earth frozen. The rocks say otherwise. |  |  |
| 60 | 283.38-287.24 | NASA | GSFC_20171208_Archive_e000888 | drift up 4% | There was liquid water. There was an ocean. How does |  |  |
| 61 | 287.24-290.82 | NASA | ast-27-2339 | push 5% | a dimmer sun sit over a wet world? |  |  |
| 62 | 290.82-295.30 | NASA | s36-07-012 | pan L-R 4% | The usual repair is the air. More greenhouse gas, |  |  |
| 63 | 295.30-301.52 | NASA | as4-01-750 | pull 5% | carbon dioxide and early methane held heat. The weaker sunlight did not supply. |  |  |
| 64 | 301.52-307.30 | NASA | s04-41-1206 | pan R-L 4% | The faint young sun is a paradox with an answer, not a hole in the model. |  |  |
| 65 | 307.30-311.30 | NASA | sl4-142-4577 | drift up 4% | The sunlight was less. The atmosphere did more. |  |  |
| 66 | 311.30-315.84 | NASA | S66-25771 | push 5% | How warm that early air was is still partly unknown. |  |  |
| 67 | 315.84-320.64 | OMNI | Orbit young-Sun shore | Orbit hangs small against the dimmer disc, visor tilted up, one hand lifted (ORBIT ACTS); 5-6 s, one take | What would you have seen from that shore? A sun that gave less heat, |  | dim young disc in plate · fallback: NASA s04-41-1206 push 4% (Omni down: stay on the world) |
| 68 | 320.64-326.32 | NASA | GSFC_20171208_Archive_e000888 | pull 5% | a sky that may not have been this blue and a day that was not yet yours. |  |  |
| 69 | 326.32-329.92 | NASA | ast-27-2339 | pan R-L 4% | The light was enough for water once the air had taken its share. |  |  |
| 70 | 329.92-334.00 | NASA | as4-01-750 | drift up 4% | It was not the daylight you were standing in. |  |  |
| 71 | 334.00-342.58 | EDIT | two-disc compare | GSFC_20171208_Archive_e002035 twice, same framing: left graded young, right today | Until the two suns sit side by side, the daylight you trust feels finished. It is the m… |  | left -30% and cooler; right as shot |
| 72 | 342.58-347.70 | NASA | GSFC_20171208_Archive_e002035 | push 5% | Now run today's pace forward. 1 % in 110 million years. | Ten Percent More |  |
| 73 | 347.70-352.76 | NASA | S06-46-617 | pull 5% | 10 % takes about 10 of those steps, a bit over a billion years. |  |  |
| 74 | 352.76-358.58 | NASA | iss071e364425 | pan R-L 4% | Schroeder and Collins -Smith follow the rise and place a harder limit for earth near a … |  |  |
| 75 | 358.58-362.08 | NASA | iss072e617674 | drift up 4% | when the sun is on the order of 10 % brighter. |  |  |
| 76 | 362.08-366.74 | NASA | iss072e769023 | push 4% | More light warms the surface, warmer air holds more water. |  |  |
| 77 | 366.74-373.14 | NASA | sts064-83-099 | pan R-L 4% | Water vapor is itself a greenhouse gas. Why the oceans would feel it is that water in t… |  |  |
| 78 | 373.14-376.72 | NASA | s44-94-051 | pull 5% | Past the limit, they can begin to lose water to space. |  |  |
| 79 | 376.72-380.28 | NASA | GSFC_20171208_Archive_e002131 | pan R-L 4% | The name for that threshold is a moist greenhouse. |  |  |
| 80 | 380.28-385.64 | NASA | STS067-709-007 | drift up 4% | It is not next century. It is the far side of the same climb. |  |  |
| 81 | 385.64-390.72 | OMNI | Orbit brighter-Sun cloud | Orbit tips towards the brighter disc, then towards a thin bright skin of cloud; small, low in frame; 5-6 s | Could a shoreline survive it? Not one that still needs an ocean, |  | future Sun: +10% brightness, scale 1.04 · fallback: NASA iss071e364425 push 4% (Omni down: stay on the world) |
| 82 | 390.72-395.10 | NASA | as08-16-2588 | pan L-R 4% | but life under this star has a very long while yet. |  |  |
| 83 | 395.10-399.84 | NASA | sts065-86-095 | pull 5% | The number matters because of its direction. The sun does not sit still and then fail all |  |  |
| 84 | 399.84-403.50 | NASA | GSFC_20171208_Archive_e002130 | pan R-L 4% | at once. It leans brighter the whole way. |  |  |
| 85 | 403.50-408.68 | NASA | GSFC_20171208_Archive_e002035 | push 4% | The disk swells only slowly through this stretch, a little larger. |  | future Sun: +10% brightness, scale 1.04 (no red giant) |
| 86 | 408.68-413.84 | NASA | S06-46-617 | push 5% | The thing that changes the shore is the light. The great red swelling comes later |  |  |
| 87 | 413.84-418.82 | NASA | iss071e364425 | pan L-R 4% | and it belongs to another film. This one stops at the brightening. |  |  |
| 88 | 418.82-423.82 | NASA | iss071e439624 | pan L-R 4% | The blue can last a very long time. It cannot last forever under a star that |  |  |
| 89 | 423.82-427.58 | NASA | iss072e617674 | pan R-L 4% | only turns one way. |  |  |
| 90 | 427.58-431.84 | NASA | s39-610-037 | push 4% | However bright that future disk is, you are not standing under it. |  |  |
| 91 | 431.84-436.54 | GODDARD | SVS 5649 | stretch 2 | You are standing in the middle of the climb. The fainter sun is behind you. | The Sun You Already Have |  |
| 92 | 436.54-442.08 | NASA | GSFC_20171208_Archive_e000414 | pan L-R 4% | The 10 % sun is further off than any civilization you can picture. |  |  |
| 93 | 442.08-446.80 | NASA | GSFC_20171208_Archive_e001517 | pull 5% | Overhead is the star that learned to be this bright and it is still learning. |  |  |
| 94 | 446.80-450.44 | NASA | PIA17669 | pan R-L 4% | About 1 % every 110 million years. |  |  |
| 95 | 450.44-456.80 | NASA | GSFC_20171208_Archive_e000759 | drift up 4% | A 10th of 1 % up and down with the spots. A prominence when the cameras want motion. |  |  |
| 96 | 456.80-461.30 | CODE | clocks.mp4 | 0-10 s: three clocks lit in turn | Free clocks. Only one of them answers the title. |  |  |
| 97 | 461.30-466.22 | NASA | GSFC_20171208_Archive_e002035 | push 5% | The sun is getting brighter because the helium in its core leaves the fire no choice. |  |  |
| 98 | 466.22-472.50 | NASA | GSFC_20171208_Archive_e000991 | pull 5% | Earth has lived the dimmer half. The oceans are still here because the climb has not go… |  |  |
| 99 | 472.50-478.70 | NASA | s09-11-675 | pan R-L 4% | That is timing and it is also just the physics running in ordinary daylight. |  |  |
| 100 | 478.70-482.40 | NASA | iss071e439624 | pull 4% | What if the real question was never whether the sun is changing, |  |  |
| 101 | 482.40-487.34 | NASA | GSFC_20171208_Archive_e000414 | push 5% | but whether you arrived while the light is still gentle enough for a blue sky. |  |  |
| 102 | 487.34-492.44 | NASA | as08-16-2588 | push 4% | The bigger question sits in that blue. How long can it last under a |  |  |
| 103 | 492.44-496.14 | NASA | GSFC_20171208_Archive_e002131 | pull 5% | star that brightens while it burns? |  |  |
| 104 | 496.14-518.64 | GODDARD | SVS 10925 | stretch 2: a different stretch from the open, prominence in motion; hold to the end | Next door, there is a planet that may already have taken that path. Next week, what hap… |  |  |

## Credits

Stills: from `nasa_pool_v01.json` (one line per picture used). SVS: NASA's Goddard Space Flight Center (Scientific Visualization Studio), per clip page.

- GSFC_20171208_Archive_e000393: Picturing the Sun’s Magnetic Field · NASA/SDO/AIA/LMSAL
- GSFC_20171208_Archive_e000414: SDO: Year 6 · NASA's Goddard Space Flight Center/SDO/S. Wiessinger
- GSFC_20171208_Archive_e000759: Two Coronal Holes on the Sun Viewed by SDO · NASA/Goddard/SDO
- GSFC_20171208_Archive_e000808: Magnetic Field Lines on the Sun · NASA/Solar Dynamics Observatory
- GSFC_20171208_Archive_e000888: BENNU’S JOURNEY - Early Earth · NASA's Goddard Space Flight Center Conceptual Image Lab
- GSFC_20171208_Archive_e000970: Twisting Blob of Plasma · NASA/SDO
- GSFC_20171208_Archive_e000991: A Significant Flare Surges Off the Sun · NASA/Goddard/SDO
- GSFC_20171208_Archive_e001052: Spurting Plasma · NASA/Goddard/Solar Dynamics Observatory
- GSFC_20171208_Archive_e001363: Filament Eruption Creates 'Canyon of Fire' on the Sun · NASA/SDO
- GSFC_20171208_Archive_e001517: The Sun: One Year in One Image · NASA/GSFC/SDO
- GSFC_20171208_Archive_e001978: C3-class Solar Flare Erupts on Sept. 8, 2010 [Full Disk] · NASA/SDO
- GSFC_20171208_Archive_e002035: Full disk view of the sun June 21, 2010 · NASA/SDO
- GSFC_20171208_Archive_e002130: NASA Blue Marble 2007 East · NASA/Goddard Space Flight Center/Reto Stöckli
- GSFC_20171208_Archive_e002131: NASA Blue Marble 2007 West · NASA/Goddard Space Flight Center/Reto Stöckli
- GSFC_20171208_Archive_e002168: Erupting Prominence Observed by SDO on March 30, 2010 · NASA/GSFC/SDO
- PIA15377: Wavelength Comparison · NASA/GSFC/Solar Dynamics Observatory
- PIA17669: Pulses from the Sun · NASA/SDO/AIA
- PIA20881: Magnetic Field Illuminated · NASA/GSFC/Solar Dynamics Observatory
- PIA21764: Coils of Magnetic Field Lines · NASA/GSFC/Solar Dynamics Observatory
- PIA21783: New Lone Sunspot Group · NASA/GSFC/Solar Dynamics Observatory
- PIA22123: Slithering Prominence · NASA/GSFC/Solar Dynamics Observatory
- PIA22360: Wavelength Comparisons · NASA/GSFC/Solar Dynamics Observatory
- PIA22645: Detailed Loops Above an Active Region · NASA/GSFC/Solar Dynamics Observatory
- PIA22662: Magnetic Field Portrayed · NASA/GSFC/Solar Dynamics Observatory
- PIA22724: Two Wavelengths, Two Different Images · NASA/GSFC/Solar Dynamics Observatory
- S06-46-617: Earth limb at sunset · NASA
- S66-25771: GEMINI-TITAN (GT)-8 - (EARTH SKY)(EARTH'S LIMB) - OUTER SPACE · NASA
- STS067-709-007: STS-67 sunset and earth limb view · NASA
- as08-16-2588: Both sides of the Atlantic Ocean are visible from Apollo 8 spacecraft · NASA
- as4-01-750: Atlantic Ocean, Antarctica as seen from the Apollo 4 unmanned spacecraft · NASA
- ast-27-2339: Earth's limb and cloud silhouette in Southern Hemisphere · NASA
- iss017e011603: Earth Limb taken by the Expedition 17 Crew · NASA
- iss071e364425: Noctilucent clouds illuminated when the sun is below Earth's horizon · NASA
- iss071e439624: An orbital sunrise colorfully illuminates the Earth's atmosphere · NASA
- iss072e617674: Storm clouds rise above the South Pacific Ocean northwest of New Zealand · NASA
- iss072e769023: A cloudy Indian Ocean southwest of Perth, Australia · NASA
- iss074e0494675: The Sun begins illuminating Earth’s surface just after an orbital sunrise · NASA
- s04-41-1206: Clouds and Open Ocean near the Bahamas · NASA
- s09-11-675: Earth limb at sunrise · NASA
- s36-07-012: STS-36 Earth observation of sun beaming off cloud-covered ocean waters · NASA
- s39-610-037: STS-39 Earth observation of Earth's limb at sunset shows atmospheric layers · NASA
- s44-94-051: Supertyphoon Yuri, Western Pacific Ocean · NASA
- s85e5052: The Earth limb glows shortly after an orbital sunrise · NASA
- sl4-142-4577: South Georgia Island in the South Atlantic Ocean · NASA
- sts064-83-099: Thunderstorms over the Pacific Ocean as seen from STS-64 · NASA
- sts065-86-095: STS-65 Earth observation of Hurricane Emilia in Eastern Pacific Ocean · NASA
