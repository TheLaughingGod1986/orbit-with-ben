# Saturn 021 — SHOT_LIST v03 (NASA pool only)

**Ben order 1 Oct 14:23 London** — supersedes CoS images-api hunt.
Pool: `07_Edit-Project/NASA_POOL_v01.md` / `nasa_pool_v01.json`.
**STOP for Ben review. No generation.**

## Summary

| Field | Value |
|---|---|
| VO (locked) | `saturn_long_vo_v03b_tightened_LOCK.m4a` · **523.62s (8:43.62)** |
| End hold | to **09:03.62** (+20s after last VO) |
| Rows | **80** |
| NASA IDs | **74** unique · 0 duplicates |
| Reuse | **0** (including second framings) |
| Goddard SVS 12672 | **once**, continuous (03:28.42–04:09.28) |
| AI approved | ice v07 · young rings · bare v05 — each once |
| Orbit | Omni ×2 (tumble · bare) — after Ben OK |
| New Veo | **none** |
| Frame | black + 5–8% push · ≤~1.5× · no stretch/slow-mo/freeze |
| Monday 9:16 | `monday_saturn_rings_streaming_v01_crop_limb_v02.png` (1080×1920, approved still, no paint) |

## Caption locks

- Aurora → **Saturn's magnetic field** (never “ring rain”).
- Hubble 1996–2000 → **seasons** (never “thinning”).
- Grand Finale drawings → **illustration**.

## Gaps flagged (not hunted)

- Row 15: FLAG: pool has no Mimas portrait — mass is VO-only.
- Row 27: FLAG: shepherd moons named in VO only; pool forbids moon-in-frame.
- Row 37: Illustration. FLAG: no NASA Keck telescope image in pool.
- Row 60: FLAG: no NASA moon-breakup image. Label: an idea.

## Sheet review (before build)

Ran `fetch_nasa_pool.py` (+ User-Agent retry). **154/154** open. Per-section sheets in `sheets/`. Eyeballed S1–S3, S5, S7–S9, S12. Skipped PIA01273 (moon dots). Did not use PIA17185 (orig 403).

## Uniqueness check (paste)

```json
{
  "vo": "saturn_long_vo_v03b_tightened_LOCK.m4a",
  "vo_duration_s": 523.62,
  "end_hold_to_s": 543.62,
  "rows": 80,
  "nasa_ids_used": [
    "PIA08247",
    "PIA20496",
    "PIA21337",
    "PIA11667",
    "PIA08248",
    "PIA08992",
    "PIA14943",
    "PIA12654",
    "PIA20498",
    "PIA03158",
    "PIA17474",
    "PIA21628",
    "PIA06193",
    "PIA05075",
    "PIA05076",
    "PIA08963",
    "PIA14629",
    "PIA01388",
    "PIA08850",
    "PIA18295",
    "PIA21058",
    "PIA21057",
    "PIA11569",
    "PIA01486",
    "PIA21618",
    "PIA12727",
    "PIA06092",
    "PIA07616",
    "PIA21621",
    "PIA12641",
    "PIA21886",
    "PIA08844",
    "PIA20502",
    "PIA16842",
    "PIA13697",
    "PIA13402",
    "PIA21439",
    "PIA22767",
    "PIA08990",
    "PIA17150",
    "PIA21892",
    "PIA21345",
    "PIA21047",
    "PIA21440",
    "PIA11396",
    "PIA03156",
    "PIA03162",
    "PIA18278",
    "PIA17176",
    "PIA11141",
    "PIA10081",
    "PIA22418",
    "PIA18274",
    "PIA18301",
    "PIA20497",
    "PIA12785",
    "PIA12786",
    "PIA18277",
    "PIA17148",
    "PIA20507",
    "PIA21052",
    "PIA21888",
    "PIA20528",
    "PIA21334",
    "PIA21327",
    "PIA11613",
    "PIA17900",
    "PIA18313",
    "PIA21046",
    "PIA08265",
    "PIA12590",
    "PIA21350",
    "PIA21351",
    "PIA17218"
  ],
  "nasa_count": 74,
  "nasa_unique": 74,
  "all_ids_in_nasa_pool_v01_json": true,
  "no_id_appears_twice": true,
  "duplicate_nasa_ids": [],
  "nasa_ids_not_in_pool": [],
  "goddard_rows": 1,
  "goddard_continuous_once": true,
  "ai_assets_once_each": true,
  "ai_duplicate_paths": [],
  "ai_assets": [
    "v07/edit_ice_chunks_v07.mp4",
    "stills_v01/saturn_young_rings_v01.png",
    "veo_v05/stills/saturn_bare_planet_only_v05.png"
  ],
  "omni_beats": 2,
  "new_veo": 0,
  "flags": [
    "Row 15: FLAG: pool has no Mimas portrait \u2014 mass is VO-only.",
    "Row 27: FLAG: shepherd moons named in VO only; pool forbids moon-in-frame.",
    "Row 37: Illustration. FLAG: no NASA Keck telescope image in pool.",
    "Row 60: FLAG: no NASA moon-breakup image. Label: an idea."
  ],
  "pool_size": 154,
  "unused_pool_count": 80,
  "pia17185_note": "Not used (~orig HTTP 403).",
  "sheet_review": "Eyeballed S1 S2 S3 S5 S7 S8 S9 S12 before build; skip PIA01273 moon dots.",
  "chapter_card_gap_s": 0.72,
  "PASS": true
}
```

**PASS = True** — every NASA ID ∈ `nasa_pool_v01.json` and no ID appears twice.

## Shot table

| # | VO in | VO out | Dur | VO line | ID / asset | NASA title | Link | Why it fits | Caption / credit |
|---:|---|---|---:|---|---|---|---|---|---|
| 1 | 00:00.00 | 00:04.32 | 4.32 | Every half hour, Saturn's rings lose enough ice to fill an Olympic swimming pool. | `AI` | edit_ice_chunks_v07.mp4 | v07/edit_ice_chunks_v07.mp4 | Approved ice crowd v07 — open falling sheet; pool has no NASA photo of ice falling. | Approved AI — not NASA |
| 2 | 00:04.32 | 00:08.95 | 4.63 | It's raining into the planet right now. So how long do the rings have left? | `PIA08247` | Opposition Surge on the A Ring | https://images.nasa.gov/details/PIA08247 | Opposition Surge on the A Ring — bright ice after AI open. | NASA/JPL-Caltech/Space Science Institute |
| 3 | 00:08.95 | 00:14.81 | 5.86 | Stay with me, and you'll see where the ice goes, what the rings looked like when they were new, | `PIA20496` | Surge in the Ring | https://images.nasa.gov/details/PIA20496 | Surge in the Ring — limb + surge while the promise lands. | NASA/JPL-Caltech/Space Science Institute |
| 4 | 00:14.81 | 00:19.67 | 4.86 | and Saturn with nothing around it at all. Look along the sheet. | `PIA21337` | Good Old Summer Time | https://images.nasa.gov/details/PIA21337 | Good Old Summer Time — rings out of frame; bare-tease from pool (bare v05 reserved for payoff). | NASA/JPL-Caltech/Space Science Institute |
| 5 | 00:19.67 | 00:23.48 | 3.81 | It is not a solid disc. It is a crowd. | `PIA11667` | The Rite of Spring | https://images.nasa.gov/details/PIA11667 | The Rite of Spring equinox mosaic — rings nearly a line; look-along hero. | NASA/JPL-Caltech/Space Science Institute |
| 6 | 00:23.48 | 00:28.64 | 5.16 | Chunks of ice, from grains to boulders, each on its own path, | `PIA08248` | Opposition Surge on the B Ring | https://images.nasa.gov/details/PIA08248 | Opposition Surge on the B Ring — soft grey crowd (S1 spare). | NASA/JPL-Caltech/Space Science Institute |
| 7 | 00:28.64 | 00:33.93 | 5.29 | packed so tightly that they read as one bright blade. | `PIA08992` | Surging Across the Rings | https://images.nasa.gov/details/PIA08992 | Surging Across the Rings — packed ice as one blade. | NASA/JPL-Caltech/Space Science Institute |
| 8 | 00:33.93 | 00:39.45 | 5.52 | The blade is enormous sideways — tens of thousands of kilometres — | `PIA14943` | Translucent Arcs | https://images.nasa.gov/details/PIA14943 | Translucent Arcs — wide colour arcs; sideways scale. | NASA/JPL-Caltech/Space Science Institute |
| 9 | 00:39.45 | 00:44.00 | 4.55 | and absurdly thin the other way. In places the main rings are only about ten metres thick. | `PIA12654` | Slender Rings | https://images.nasa.gov/details/PIA12654 | Slender Rings — crescent with rings as a thin line. | NASA/JPL-Caltech/Space Science Institute |
| 10 | 00:44.00 | 00:49.12 | 5.12 | A playing field stood on edge, stretched around a world. | `PIA20498` | Barely Bisected Rings | https://images.nasa.gov/details/PIA20498 | Barely Bisected Rings — nearly edge-on thin sheet. | NASA/JPL-Caltech/Space Science Institute |
| 11 | 00:49.12 | 00:55.80 | 6.68 | Why does something that wide look so finished, and so fragile? | `PIA03158` | A Change of Seasons on Saturn - October, 1996 | https://images.nasa.gov/details/PIA03158 | Hubble Oct 1996 — rings nearly edge-on across Saturn. | Hubble seasons/tilt — not thinning |
| 12 | 00:55.80 | 01:02.71 | 6.91 | Because you are seeing sunlight on ice, not a wall. Photons bounce off clean water ice and come back almost white. | `PIA17474` | Jewel of the Solar System | https://images.nasa.gov/details/PIA17474 | Jewel of the Solar System — soft natural colour; sunlight on ice. | NASA/JPL-Caltech/Space Science Institute |
| 13 | 01:02.71 | 01:08.17 | 5.46 | A little dust stains the older lanes a warmer colour. The mass under that shine | `PIA21628` | Colorful Structure at Fine Scales | https://images.nasa.gov/details/PIA21628 | Colorful Structure at Fine Scales — cream/tan dust lanes. | NASA/JPL-Caltech/Space Science Institute |
| 14 | 01:08.17 | 01:14.80 | 6.63 | is small for the area it covers. Cassini weighed the rings on its last orbits and found less than many maps had assumed — | `PIA06193` | The Greatest Saturn Portrait ...Yet | https://images.nasa.gov/details/PIA06193 | The Greatest Saturn Portrait — a lot of scenery for the small-mass line. | NASA/JPL-Caltech/Space Science Institute |
| 15 | 01:14.80 | 01:21.00 | 6.2 | on the order of two fifths of the little moon Mimas. | `PIA05075` | Saturn A Ring From the Inside Out | https://images.nasa.gov/details/PIA05075 | UVIS A Ring — turquoise ice / red dirtier lanes under the mass claim. | FLAG: pool has no Mimas portrait — mass is VO-only. |
| 16 | 01:21.00 | 01:26.50 | 5.5 | A lot of scenery. Not a lot of stuff. The mystery starts as a fall, not as a monument. | `PIA05076` | Saturn C and B Rings From the Inside Out | https://images.nasa.gov/details/PIA05076 | UVIS C and B Rings — composition under scenery/mass. | NASA/JPL-Caltech/Space Science Institute |
| 17 | 01:26.50 | 01:32.58 | 6.08 | But the picture that brought you here is already the danger. | `PIA08963` | Odd Ring Out | https://images.nasa.gov/details/PIA08963 | Odd Ring Out — fragile sheet danger (S1 spare). | NASA/JPL-Caltech/Space Science Institute |
| 18 | 01:32.58 | 01:38.97 | 6.39 | Does the fall ever stop? It does not stop while you are watching. Gravity keeps every chunk moving. | `PIA14629` | Ever-Changing Ring | https://images.nasa.gov/details/PIA14629 | Ever-Changing Ring — fall does not stop. | NASA/JPL-Caltech/Space Science Institute |
| 19 | 01:38.97 | 01:44.77 | 5.8 | The smallest grains are already leaking inward. What would you see if you waited? | `PIA01388` | Saturn Faint Inner D-ring | https://images.nasa.gov/details/PIA01388 | Faint Inner D-ring — inward leak. | NASA/JPL |
| 20 | 01:44.77 | 01:51.09 | 6.32 | Not a collapse in the news. A slow thinning. Then a planet that has spent the jewellery. | `PIA08850` | The Vanishing Rings | https://images.nasa.gov/details/PIA08850 | The Vanishing Rings — slow-loss mood. | NASA/JPL-Caltech/Space Science Institute |
| 21 | 01:51.09 | 01:58.16 | 7.07 | How long that takes is the question we are saving for the rain. Now the question changes. | `PIA18295` | Translucent Rings | https://images.nasa.gov/details/PIA18295 | Translucent Rings — rain question. | NASA/JPL-Caltech/Space Science Institute |
| 22 | 01:58.16 | 02:04.86 | 6.7 | What is that jewellery made of? Come in close enough that the blade breaks into pieces. | `PIA21058` | Saturn B Ring, Finer Than Ever | https://images.nasa.gov/details/PIA21058 | B Ring finer than ever — blade → pieces. | NASA/JPL-Caltech/Space Science Institute |
| 23 | 02:04.86 | 02:11.80 | 6.94 | Ice. Not rock. Water ice, the same bright mineral as a comet, | `PIA21057` | Straw in the B Ring Edge | https://images.nasa.gov/details/PIA21057 | Straw in the B Ring Edge — ice not rock. | NASA/JPL-Caltech/Space Science Institute |
| 24 | 02:11.80 | 02:18.18 | 6.38 | dirty in places and clean in others. Most of the mass sits in chunks you could hold, | `PIA11569` | Behold B Ring Clumps | https://images.nasa.gov/details/PIA11569 | B Ring Clumps — dirty/clean ice crowd. | NASA/JPL-Caltech/Space Science Institute |
| 25 | 02:18.18 | 02:27.29 | 9.11 | or in boulders the size of a house. Rocky dust rides with the ice and slowly stains it cream to tan. | `PIA01486` | Composition Differences within Saturn Rings | https://images.nasa.gov/details/PIA01486 | Composition Differences — dust stain. | NASA/JPL |
| 26 | 02:27.29 | 02:33.26 | 5.97 | Why call it a ring if it is only a crowd of snowballs? Because the crowd is flat. | `PIA21618` | Textures in the C Ring | https://images.nasa.gov/details/PIA21618 | Textures in the C Ring — flat crowd. | NASA/JPL-Caltech/Space Science Institute |
| 27 | 02:33.26 | 02:39.43 | 6.17 | Saturn's gravity, and the moons that shepherd the edges, pack the paths into a plane. | `PIA12727` | A-Ring Structures | https://images.nasa.gov/details/PIA12727 | A-Ring Structures — packed plane. | FLAG: shepherd moons named in VO only; pool forbids moon-in-frame. |
| 28 | 02:39.43 | 02:46.17 | 6.74 | The gaps are emptier roads. The ice that remains still circles. It does not sit. | `PIA06092` | Cassini Captures the Cassini Division | https://images.nasa.gov/details/PIA06092 | Cassini Division — emptier roads. | NASA/JPL-Caltech/Space Science Institute |
| 29 | 02:46.17 | 02:51.36 | 5.19 | There is no roof. | `PIA07616` | The Cassini Division Edge | https://images.nasa.gov/details/PIA07616 | The Cassini Division Edge — no roof / gap into open. | NASA/JPL-Caltech/Space Science Institute |
| 30 | 02:51.36 | 02:57.45 | 6.09 | Drop through those ten metres and you are in open space again. | `OMNI` | Orbit tumble through thin sheet — Omni + canonical still (after Ben OK) | canonical Orbit still + Omni (after Ben OK) | First Orbit beat — Omni only. | Orbit Omni — canonical still |
| 31 | 02:57.45 | 03:04.53 | 7.08 | The atmosphere sits far below the inner edge, banded and pale. | `PIA21621` | Haze on the Horizon | https://images.nasa.gov/details/PIA21621 | Haze on the Horizon — atmosphere far below. | NASA/JPL-Caltech/Space Science Institute |
| 32 | 03:04.53 | 03:08.99 | 4.46 | The unknown is not the recipe. The unknown is the leak. | `PIA12641` | Rings Through Atmosphere | https://images.nasa.gov/details/PIA12641 | Rings Through Atmosphere — the leak. | NASA/JPL-Caltech/Space Science Institute |
| 33 | 03:08.99 | 03:15.07 | 6.08 | However bright the ice looks, brightness is not a promise that it stays. | `PIA21886` | Cassini's 'Inside-Out' Rings | https://images.nasa.gov/details/PIA21886 | Inside-Out Rings — bright ice already in danger. | NASA/JPL-Caltech/Space Science Institute |
| 34 | 03:15.07 | 03:22.52 | 7.45 | That is the first answer: the famous sheet is only ice, and it is already slipping away. | `PIA08844` | Saturnian Squiggles | https://images.nasa.gov/details/PIA08844 | Saturnian Squiggles — sheet slipping. | NASA/JPL-Caltech/Space Science Institute |
| 35 | 03:22.52 | 03:27.70 | 5.18 | We make one of these every week. Subscribing is how the next one finds you. | `PIA20502` | View from Above | https://images.nasa.gov/details/PIA20502 | View from Above — subscribe cover science portrait. | NASA/JPL-Caltech/Space Science Institute |
| 36 | 03:28.42 | 04:09.28 | 40.86 | Here is one way they go — charge → magnetic field threads the plane → guided down → vapour — Ring rain. | `GODDARD` | NASA Goddard SVS 12672 — Saturn ring-rain visualisation | https://svs.gsfc.nasa.gov/12672/ | NASA Goddard SVS 12672 — ONE continuous shot (03:28.42–04:09.28). Not sliced. | Ring rain (Goddard continuous once) |
| 37 | 04:09.28 | 04:16.22 | 6.94 | We did not need a spacecraft inside that rain to know it was there. Astronomers on Earth, using the Keck telescope, watched the glow of that water in Saturn's upper air | `PIA16842` | Saturn Ring Rain Artist Concept | https://images.nasa.gov/details/PIA16842 | Saturn Ring Rain Artist Concept — NASA illustration of the rain. | Illustration. FLAG: no NASA Keck telescope image in pool. |
| 38 | 04:16.22 | 04:26.60 | 10.38 | and measured how fast the ice was leaving. At that magnetic rain rate alone, the sheet would last about three hundred million years. | `PIA13697` | Saturn Hot Plasma Explosions | https://images.nasa.gov/details/PIA13697 | Hot Plasma Explosions — magnetic field lines / lifetime. | Caption: Saturn's magnetic field |
| 39 | 04:26.60 | 04:31.80 | 5.2 | But that is only one path down. Cassini went closer. | `PIA13402` | Glowing Southern Lights | https://images.nasa.gov/details/PIA13402 | Glowing Southern Lights — magnetic field into atmosphere. | Caption: Saturn's magnetic field — never 'ring rain' |
| 40 | 04:31.80 | 04:40.57 | 8.77 | In 2017 the orbiter flew twenty-two times through the gap between the innermost ring and the cloud tops. | `PIA21439` | Cassini Grand Finale Dive Illustration | https://images.nasa.gov/details/PIA21439 | Grand Finale Dive Illustration — Cassini between rings and planet. | Label on screen: illustration |
| 41 | 04:40.57 | 04:47.54 | 6.97 | It was not sampling the magnetic rain from mid-latitudes. It was flying through something bigger: | `PIA22767` | Grand Finale: Cassini in the Gap (Illustration) | https://images.nasa.gov/details/PIA22767 | Grand Finale: Cassini in the Gap (Illustration). | Label on screen: illustration |
| 42 | 04:47.54 | 04:54.85 | 7.31 | material pouring off the innermost ring — the D ring — straight into Saturn's equator. | `PIA08990` | D-Ring Structure | https://images.nasa.gov/details/PIA08990 | D-Ring Structure — the inflow ring. | NASA/JPL-Caltech/Space Science Institute |
| 43 | 04:54.85 | 05:00.74 | 5.89 | That equatorial inflow is a heavier leak than the magnetic rain alone. | `PIA17150` | Dusty D Ring | https://images.nasa.gov/details/PIA17150 | Dusty D Ring — heavier leak path. | NASA/JPL-Caltech/Space Science Institute |
| 44 | 05:00.74 | 05:06.21 | 5.47 | Add it to the books, and the sheet's remaining life drops to around a hundred million years. | `PIA21892` | Saturn: Before the Plunge | https://images.nasa.gov/details/PIA21892 | Saturn: Before the Plunge — among Cassini's last pictures. | NASA/JPL-Caltech/Space Science Institute |
| 45 | 05:06.21 | 05:11.50 | 5.29 | So how long does the bright sheet have? Put both measurements together | `PIA21345` | So Far from Home | https://images.nasa.gov/details/PIA21345 | So Far from Home — last distant look. | NASA/JPL-Caltech/Space Science Institute |
| 46 | 05:11.50 | 05:18.55 | 7.05 | and the honest answer is a range, somewhere between about a hundred and three hundred million years. | `PIA21047` | Staring at Saturn | https://images.nasa.gov/details/PIA21047 | Staring at Saturn — full disc for the lifetime range. | NASA/JPL-Caltech/Space Science Institute |
| 47 | 05:18.55 | 05:25.25 | 6.7 | A blink next to Saturn's four and a half billion years. You would not see either leak as weather from a window. | `PIA21440` | Cassini versus Saturn Illustration | https://images.nasa.gov/details/PIA21440 | Cassini versus Saturn Illustration — orbiter over atmosphere. | Label on screen: illustration |
| 48 | 05:25.25 | 05:31.81 | 6.56 | The grains are too fine, and the fall is too spread out. What you would see, | `PIA11396` | Saturn Polar Aurora | https://images.nasa.gov/details/PIA11396 | Saturn Polar Aurora — grains too fine to see as weather. | Caption: Saturn's magnetic field — never 'ring rain' |
| 49 | 05:31.81 | 05:37.52 | 5.71 | if you could watch for an age, is the sheet growing thinner, while Saturn's bands stay put. | `PIA03156` | A Change of Seasons on Saturn | https://images.nasa.gov/details/PIA03156 | Hubble 1996–2000 seasons montage — watch for an age; NOT thinning proof. | Caption: seasons — never 'thinning' |
| 50 | 05:37.52 | 05:44.24 | 6.72 | Now look backward. The rain implies a beginning. Wind the clock back along that same scale, | `PIA03162` | A Change of Seasons on Saturn - October, 2000 | https://images.nasa.gov/details/PIA03162 | Hubble Oct 2000 — rings wide open; seasons. | Caption: seasons — never 'thinning' |
| 51 | 05:44.24 | 05:53.36 | 9.12 | and the sheet changes. More mass. Cleaner ice. A harder white, because the dust had not had time to dirty it. | `AI` | saturn_young_rings_v01.png | stills_v01/saturn_young_rings_v01.png | Approved young-rings still — whiter/wider; used once. | Approved AI — not NASA |
| 52 | 05:53.36 | 06:00.91 | 7.55 | Saturn would still have been the ringed one — only more so. A broader blade. A brighter one. | `PIA18278` | Ring King | https://images.nasa.gov/details/PIA18278 | Ring King — broader/brighter from above. | NASA/JPL-Caltech/Space Science Institute |
| 53 | 06:00.91 | 06:06.63 | 5.72 | The planet underneath was already the planet. The rings look like a late arrival. | `PIA17176` | Tis the Season | https://images.nasa.gov/details/PIA17176 | Tis the Season — planet already itself. | NASA/JPL-Caltech/Space Science Institute |
| 54 | 06:06.63 | 06:11.91 | 5.28 | Why "new", when Saturn itself is about four and a half billion years old? | `PIA11141` | Saturn … Four Years On | https://images.nasa.gov/details/PIA11141 | Saturn … Four Years On — age contrast. | NASA/JPL-Caltech/Space Science Institute |
| 55 | 06:11.91 | 06:19.15 | 7.24 | Because a heavy, ancient ring would still be heavy, unless most of its mass has already gone in. | `PIA10081` | Saturn Recycling Rings | https://images.nasa.gov/details/PIA10081 | Saturn Recycling Rings artist concept — age-debate fit. | Illustration (artist concept) |
| 56 | 06:19.15 | 06:25.74 | 6.59 | Most researchers read Cassini's low mass as young — a few hundred million years at most. | `PIA22418` | Gravity's Rainbow | https://images.nasa.gov/details/PIA22418 | Gravity's Rainbow — bright rings; mostly water ice. | NASA/JPL-Caltech/Space Science Institute |
| 57 | 06:25.74 | 06:30.87 | 5.13 | A few argue the rings could still be old, and hide their age another way. | `PIA18274` | Vortex and Rings | https://images.nasa.gov/details/PIA18274 | Vortex and Rings — debate open. | NASA/JPL-Caltech/Space Science Institute |
| 58 | 06:30.87 | 06:35.99 | 5.12 | The debate is open. The honest line is narrower than a slogan. | `PIA18301` | Study in Scarlet | https://images.nasa.gov/details/PIA18301 | Study in Scarlet — bright ring curves. | NASA/JPL-Caltech/Space Science Institute |
| 59 | 06:35.99 | 06:42.31 | 6.32 | The rings you see are ice, they are already leaving, and their birthday is not settled. | `PIA20497` | A Dark Bend | https://images.nasa.gov/details/PIA20497 | A Dark Bend — ice already leaving. | NASA/JPL-Caltech/Space Science Institute |
| 60 | 06:42.31 | 06:50.52 | 8.21 | What if a moon came too close, and came apart? That idea fits a young mass, and it is still an idea. | `PIA12785` | F Ring Bright Core Clumps | https://images.nasa.gov/details/PIA12785 | F Ring Bright Core Clumps — rubble-in-a-plane stand-in. | FLAG: no NASA moon-breakup image. Label: an idea. |
| 61 | 06:50.52 | 06:58.48 | 7.96 | Inside the Roche limit, Saturn's gravity can pull a moon into rubble, and rubble in a plane becomes a ring. | `PIA12786` | Fan in the F Ring | https://images.nasa.gov/details/PIA12786 | Fan in the F Ring — streamers as rubble in a plane. | Label: an idea |
| 62 | 06:58.48 | 07:04.04 | 5.56 | Whatever their birthday, the rings you know are ice, and they are already leaving. | `PIA18277` | Clumpy Ringlets | https://images.nasa.gov/details/PIA18277 | Clumpy Ringlets — ice already leaving. | NASA/JPL-Caltech/Space Science Institute |
| 63 | 07:04.04 | 07:09.28 | 5.24 | Then the sheet you call famous is a phase, not a permanent face. | `PIA17148` | Splitting the F Ring | https://images.nasa.gov/details/PIA17148 | Splitting the F Ring — phase, not permanent face. | NASA/JPL-Caltech/Space Science Institute |
| 64 | 07:09.28 | 07:17.15 | 7.87 | Take the ice away, and stay with the planet. Saturn is still there. Pale gold bands. | `AI` | saturn_bare_planet_only_v05.png | veo_v05/stills/saturn_bare_planet_only_v05.png | Approved bare Saturn v05 — payoff; used once. | Approved AI — not NASA |
| 65 | 07:17.15 | 07:23.81 | 6.66 | A fast day, a little over ten hours, written as soft stripes in a deep atmosphere. | `OMNI` | Orbit tiny against bare Saturn — Omni + canonical still (after Ben OK) | canonical Orbit still + Omni (after Ben OK) | Second Orbit beat — Omni only on bare plate already established. | Orbit Omni — canonical still |
| 66 | 07:23.81 | 07:30.63 | 6.82 | The curve of the planet runs clean. The shadow the rings used to cast on the clouds is gone. | `PIA20507` | Saturn Watercolor Swirls | https://images.nasa.gov/details/PIA20507 | Watercolor Swirls — pole/limb, no rings. | NASA/JPL-Caltech/Space Science Institute |
| 67 | 07:30.63 | 07:36.28 | 5.65 | The famous thing was never the body. It was the ice in orbit around the body. | `PIA21052` | Over Saturn Turbulent North | https://images.nasa.gov/details/PIA21052 | Over Saturn Turbulent North — storms, no rings. | NASA/JPL-Caltech/Space Science Institute |
| 68 | 07:36.28 | 07:41.35 | 5.07 | What would you see, standing in that later sky? A giant, | `PIA21888` | Dreamy Swirls on Saturn | https://images.nasa.gov/details/PIA21888 | Dreamy Swirls — cream bands; banded giant. | NASA/JPL-Caltech/Space Science Institute |
| 69 | 07:41.35 | 07:46.96 | 5.61 | banded and bright, ordinary once you stop using the rings as the definition. | `PIA20528` | Watercolor World | https://images.nasa.gov/details/PIA20528 | Watercolor World — limb and bands. | NASA/JPL-Caltech/Space Science Institute |
| 70 | 07:46.96 | 07:51.64 | 4.68 | You would feel the oddness in the absence. The planet does not notice. | `PIA21334` | Saturnian Dawn | https://images.nasa.gov/details/PIA21334 | Saturnian Dawn — lit limb; oddness in absence. | NASA/JPL-Caltech/Space Science Institute |
| 71 | 07:51.64 | 07:57.70 | 6.06 | The rain simply finishes, and the paths that carried it have nothing left to carry. | `PIA21327` | Hail the Hexagon | https://images.nasa.gov/details/PIA21327 | Hail the Hexagon — planet remains without the sheet. | NASA/JPL-Caltech/Space Science Institute |
| 72 | 07:57.70 | 08:03.65 | 5.95 | So the whole story fits in one breath. You would see a thin sheet of water ice, | `PIA11613` | Post-Equinox Color | https://images.nasa.gov/details/PIA11613 | Post-Equinox Color — thin dark ring band; recap. | NASA/JPL-Caltech/Space Science Institute |
| 73 | 08:03.65 | 08:07.61 | 3.96 | vast and bright, already raining into Saturn. | `PIA17900` | Dance of Saturn Auroras | https://images.nasa.gov/details/PIA17900 | Dance of Saturn Auroras — magnetic rain from Earth. | Caption: Saturn's magnetic field — never 'ring rain' |
| 74 | 08:07.61 | 08:15.29 | 7.68 | Magnetic rain measured from Earth, and a heavier equatorial leak Cassini flew through on its last dives. | `PIA18313` | Faint D Ring | https://images.nasa.gov/details/PIA18313 | Faint D Ring — equatorial leak clock. | NASA/JPL-Caltech/Space Science Institute |
| 75 | 08:15.29 | 08:23.86 | 8.57 | The mass is too small for a forever-disc, so the clock sits somewhere between about a hundred and three hundred million years. | `PIA21046` | Saturn, Approaching Northern Summer | https://images.nasa.gov/details/PIA21046 | Saturn Approaching Northern Summer — planet remains / clock. | NASA/JPL-Caltech/Space Science Institute |
| 76 | 08:23.86 | 08:30.37 | 6.51 | The rings are a phase. Saturn is the thing that remains. What else in the sky are you | `PIA08265` | Saturn Hides the Rings | https://images.nasa.gov/details/PIA08265 | Saturn Hides the Rings — brightness ≠ permanence. | NASA/JPL-Caltech/Space Science Institute |
| 77 | 08:30.37 | 08:33.35 | 2.98 | treating as permanent only because it is bright? | `PIA12590` | Shadow and Ringshine | https://images.nasa.gov/details/PIA12590 | Shadow and Ringshine — temporary ice. | NASA/JPL-Caltech/Space Science Institute |
| 78 | 08:33.35 | 08:39.44 | 6.09 | The rings are the clearest case. The mystery is how much of that sky is temporary. | `PIA21350` | Goodbye to the Dark Side | https://images.nasa.gov/details/PIA21350 | Goodbye to the Dark Side — temporary sky. | NASA/JPL-Caltech/Space Science Institute |
| 79 | 08:39.44 | 08:43.62 | 4.18 | Next: What Happens When the Last Star Dies? | `PIA21351` | The North | https://images.nasa.gov/details/PIA21351 | The North — hexagon from the last weeks; hand-off into hold. | NASA/JPL-Caltech/Space Science Institute |
| 80 | 08:43.62 | 09:03.62 | 20.0 | [END HOLD 20s — music fades ~10s; picture fades last ~2s; no subscribe card] | `PIA17218` | A Farewell to Saturn | https://images.nasa.gov/details/PIA17218 | A Farewell to Saturn — last full mosaic; slow 5–8% push. No open-callback reuse. | NASA/JPL-Caltech/Space Science Institute |

## Description credit block

Image credits (NASA media guidelines; NASA does not endorse this film):

- PIA08247 — Opposition Surge on the A Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08247
- PIA20496 — Surge in the Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20496
- PIA21337 — Good Old Summer Time — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21337
- PIA11667 — The Rite of Spring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA11667
- PIA08248 — Opposition Surge on the B Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08248
- PIA08992 — Surging Across the Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08992
- PIA14943 — Translucent Arcs — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA14943
- PIA12654 — Slender Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12654
- PIA20498 — Barely Bisected Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20498
- PIA03158 — A Change of Seasons on Saturn - October, 1996 — NASA/ESA/STScI (Hubble) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA03158
- PIA17474 — Jewel of the Solar System — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA17474
- PIA21628 — Colorful Structure at Fine Scales — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21628
- PIA06193 — The Greatest Saturn Portrait ...Yet — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA06193
- PIA05075 — Saturn A Ring From the Inside Out — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA05075
- PIA05076 — Saturn C and B Rings From the Inside Out — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA05076
- PIA08963 — Odd Ring Out — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08963
- PIA14629 — Ever-Changing Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA14629
- PIA01388 — Saturn Faint Inner D-ring — NASA/JPL — https://images.nasa.gov/details/PIA01388
- PIA08850 — The Vanishing Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08850
- PIA18295 — Translucent Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18295
- PIA21058 — Saturn B Ring, Finer Than Ever — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21058
- PIA21057 — Straw in the B Ring Edge — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21057
- PIA11569 — Behold B Ring Clumps — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA11569
- PIA01486 — Composition Differences within Saturn Rings — NASA/JPL — https://images.nasa.gov/details/PIA01486
- PIA21618 — Textures in the C Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21618
- PIA12727 — A-Ring Structures — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12727
- PIA06092 — Cassini Captures the Cassini Division — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA06092
- PIA07616 — The Cassini Division Edge — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA07616
- PIA21621 — Haze on the Horizon — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21621
- PIA12641 — Rings Through Atmosphere — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12641
- PIA21886 — Cassini's 'Inside-Out' Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21886
- PIA08844 — Saturnian Squiggles — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08844
- PIA20502 — View from Above — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20502
- PIA16842 — Saturn Ring Rain Artist Concept — NASA/JPL-Caltech (illustration) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA16842
- PIA13697 — Saturn Hot Plasma Explosions — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA13697
- PIA13402 — Glowing Southern Lights — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA13402
- PIA21439 — Cassini Grand Finale Dive Illustration — NASA/JPL-Caltech (illustration) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA21439
- PIA22767 — Grand Finale: Cassini in the Gap (Illustration) — NASA/JPL-Caltech (illustration) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA22767
- PIA08990 — D-Ring Structure — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08990
- PIA17150 — Dusty D Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA17150
- PIA21892 — Saturn: Before the Plunge — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21892
- PIA21345 — So Far from Home — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21345
- PIA21047 — Staring at Saturn — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21047
- PIA21440 — Cassini versus Saturn Illustration — NASA/JPL-Caltech (illustration) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA21440
- PIA11396 — Saturn Polar Aurora — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA11396
- PIA03156 — A Change of Seasons on Saturn — NASA/ESA/STScI (Hubble) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA03156
- PIA03162 — A Change of Seasons on Saturn - October, 2000 — NASA/ESA/STScI (Hubble) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA03162
- PIA18278 — Ring King — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18278
- PIA17176 — Tis the Season — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA17176
- PIA11141 — Saturn … Four Years On — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA11141
- PIA10081 — Saturn Recycling Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA10081
- PIA22418 — Gravity's Rainbow — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA22418
- PIA18274 — Vortex and Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18274
- PIA18301 — Study in Scarlet — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18301
- PIA20497 — A Dark Bend — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20497
- PIA12785 — F Ring Bright Core Clumps — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12785
- PIA12786 — Fan in the F Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12786
- PIA18277 — Clumpy Ringlets — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18277
- PIA17148 — Splitting the F Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA17148
- PIA20507 — Saturn Watercolor Swirls — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20507
- PIA21052 — Over Saturn Turbulent North — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21052
- PIA21888 — Dreamy Swirls on Saturn — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21888
- PIA20528 — Watercolor World — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA20528
- PIA21334 — Saturnian Dawn — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21334
- PIA21327 — Hail the Hexagon — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21327
- PIA11613 — Post-Equinox Color — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA11613
- PIA17900 — Dance of Saturn Auroras — NASA/ESA/STScI (Hubble) — copy exact line from photojournal page — https://images.nasa.gov/details/PIA17900
- PIA18313 — Faint D Ring — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA18313
- PIA21046 — Saturn, Approaching Northern Summer — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21046
- PIA08265 — Saturn Hides the Rings — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA08265
- PIA12590 — Shadow and Ringshine — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA12590
- PIA21350 — Goodbye to the Dark Side — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21350
- PIA21351 — The North — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA21351
- PIA17218 — A Farewell to Saturn — NASA/JPL-Caltech/Space Science Institute — https://images.nasa.gov/details/PIA17218
- SVS 12672 — Saturn ring-rain visualisation — NASA's Goddard Space Flight Center / SVS — https://svs.gsfc.nasa.gov/12672/

_STOP — Ben OK before Omni / assemble._
