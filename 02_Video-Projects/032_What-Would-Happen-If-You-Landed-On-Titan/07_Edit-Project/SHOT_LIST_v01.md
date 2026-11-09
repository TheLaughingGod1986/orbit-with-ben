# 032 What Would Happen If You Landed on Titan? SHOT_LIST v01 (Claude, 4 Nov 2026, J2042)

Timed to `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json`. That is the locked VO `titan_landing_vo_v02b` (582.44 s; Chief h31, J1294). Its listen check is Ben's final watch, under Ben's 4 Nov rule (J1753 done).

Times are Scribe sentence spans. Each row is a beat. Every cut sits in a VO pause.

**Chapters are inferred from the script's question bridges.** The VO lock records fades, not absolute chapter ends, so the assembler confirms them against `chapters_index.json` if one exists:
- ch0 0–50.44
- ch1 51.26–136.68
- ch2 137.56–245.10
- ch3 246.00–324.44
- ch4 325.32–388.92
- ch5 389.76–474.10
- ch6 474.94–582.38

**House rules applied (029 lessons, AGENTS "Teach on screen", LEARNINGS 10):**
- **Frame 0** is moving footage of the subject: the Huygens descent movie. There is no title card and no Orbit at frame 0.
- **Every DATA / WHO / WHEN / FACT item is our own CODE graphic,** built with `code_graphics.py`.
- **Stills:** no still more than twice, the second use reframed. Upscale ≤ 2.35×.
- **Plates:** change every 4–6 s.

**Spend: £0 in this list.**
- **Two Orbit beats are marked OMNI** (rows 26, 46). They are flagged for the Chief's price pass, with fallbacks written.
- **No Veo.**

**Sources (licence checked at harvest, logged in `HARVEST_POOL_v01.json`):**
- **NASA/JPL/Caltech:** Cassini ISS, VIMS and radar. Public domain; credit the instrument team where asked.
- **ESA/NASA/JPL/University of Arizona:** the Huygens DISR descent images and the descent movie (NASA-released, PD). The ESA versions are CC BY-SA 3.0 IGO.
- **NASA/Johns Hopkins APL:** the Dragonfly mission animations (NASA, PD; credit "NASA/Johns Hopkins APL").
- **NASA:** the Voyager 1 Titan image (PD).
- **Commons:** the Christiaan Huygens portrait (PD). The Gerard Kuiper photo only if Commons marks it PD; otherwise a CODE name card.
- **The existing Short `RLSJm59OSzI`** ("What Would Standing on Saturn's Moon Titan Feel Like?", scheduled 10 Nov): no frames are reused from it in the long, to keep the two distinct.
- **No fire, explosion or disaster stock** (the film's answer is "it would not explode").

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.16–5.24 | 5.1 | ESA/NASA | Huygens DISR descent movie, mid-descent, the ground rising through orange haze, already moving | 1 | **Frame 0 lock.** |
| 2 | 0 Open | 6.38–9.36 | 3.0 | CODE | A body outline with ticks: "won't explode ✓", "blood won't boil ✓" | 1 | Calm, quick. |
| 3 | 0 Open | 10.06–22.50 | 12.4 | NASA/JPL / CODE | Cassini in orbit (JPL animation) → Titan's orange limb haze (Cassini ISS) → CODE `pressure --seconds 5`: a gauge with Earth 1.0 vs Titan ≈ 1.5 | 3 | **DATA:** "one and a half times". |
| 4 | 0 Open | 23.34–31.58 | 8.2 | CODE | `pressure` hold, then a thermometer dropping to "−179 °C" and an O₂ bar near zero | 2 | **DATA.** "The cold and almost no oxygen." |
| 5 | 0 Open | 32.76–44.56 | 11.8 | ESA/NASA / CODE / NASA APL | Promise beat: the Huygens surface image (pebbles) → CODE raindrop falling slowly → Dragonfly flying (APL animation) | 3 | One cut per question. |
| 6 | 0 Open | 45.62–50.44 | 4.8 | NASA/JPL | Titan + Saturn true-colour (Cassini), slow push | 1 | Bridge into ch1. |
| 7 | 1 A Moon With a Sky | 51.26–60.10 | 8.8 | CODE / Commons | Card "25 MARCH 1655 · CHRISTIAAN HUYGENS" (CODE), then the Huygens portrait (PD), slow push | 2 | **WHO/WHEN.** |
| 8 | 1 A Moon With a Sky | 60.10–68.06 | 8.0 | CODE | `orbit16`: Saturn with rings; a dot circles once on a "16 days" counter | 1 | **DATA.** |
| 9 | 1 A Moon With a Sky | 68.98–79.82 | 10.8 | CODE | `sizes`: Moon, Mercury and Titan discs side by side to scale; Titan's label shows "bigger than our Moon, wider than Mercury" | 2 | **VISUAL MUST, DATA.** |
| 10 | 1 A Moon With a Sky | 81.02–93.80 | 12.8 | CODE / Commons | Card "1944 · GERARD KUIPER" (portrait only if PD), then CODE `spectrum`: light through a prism, with a methane absorption line lighting up | 2 | **WHO/WHEN + VISUAL MUST.** |
| 11 | 1 A Moon With a Sky | 94.80–99.82 | 5.0 | NASA/JPL | Titan's haze layers at the limb (Cassini, the detached-haze image) | 1 | "A moon has an atmosphere of its own." |
| 12 | 1 A Moon With a Sky | 101.22–111.94 | 10.7 | NASA | The Voyager 1 spacecraft (NASA/JPL animation) → card "NOVEMBER 1980 · VOYAGER 1" | 2 | **WHEN.** |
| 13 | 1 A Moon With a Sky | 112.78–124.76 | 12.0 | NASA | The Voyager 1 Titan image (featureless orange), slow push; then CODE: a sunlight arrow splitting N₂ + CH₄ into haze particles | 2 | **VISUAL MUST.** |
| 14 | 1 A Moon With a Sky | 126.02–136.68 | 10.7 | CODE / NASA/JPL | `methane`: a CH₄ gauge draining from sunlight and refilling from below (a "?" source); then a Cassini cloud image | 2 | The question bridge into ch2. |
| 15 | 2 The Huygens Landing | 137.56–151.98 | 14.4 | NASA/JPL / ESA | Cassini–Huygens launch → Huygens separation (ESA animation) → card "14 JANUARY 2005"; parachute opens | 3 | **WHEN.** |
| 16 | 2 The Huygens Landing | 153.08–158.64 | 5.6 | ESA/NASA | DISR descent movie, the high part (murky orange) | 1 | "Two hours and twenty-seven minutes" as a CODE lower-third. |
| 17 | 2 The Huygens Landing | 159.48–171.18 | 11.7 | ESA/NASA | DISR mosaic: bright hills with dark branching channels, the panorama at about 8 km altitude; a slow pan along the channels | 2 | **VISUAL MUST.** "Dark branching channels." |
| 18 | 2 The Huygens Landing | 172.16–183.54 | 11.4 | ESA/NASA / CODE | The Huygens surface image (rounded pebbles, colour), slow push; a CODE ruler marks "≈ 15 cm" | 2 | **VISUAL MUST, DATA.** |
| 19 | 2 The Huygens Landing | 184.60–197.20 | 12.6 | CODE | `distance`: Sun–Earth–Saturn line with "9.5×", then a thermometer at "−179 °C" | 2 | **DATA.** |
| 20 | 2 The Huygens Landing | 198.02–205.82 | 7.8 | ESA/NASA / CODE | The pebble image (second use, tight on one pebble) with the overlay "WATER ICE" | 2 | "Water ice plays the role of rock." |
| 21 | 2 The Huygens Landing | 206.64–219.36 | 12.7 | CODE | `cycle --seconds 12`: Earth's water cycle beside Titan's methane–ethane cycle (cloud → rain → river → lake), labels swapping H₂O ↔ CH₄/C₂H₆ | 3 | **VISUAL MUST.** |
| 22 | 2 The Huygens Landing | 220.54–228.72 | 8.2 | CODE / NASA/JPL | Huygens on the ground; a "72 MIN" counter; Cassini sinking below the horizon (CODE geometry) | 2 | **DATA.** |
| 23 | 2 The Huygens Landing | 229.78–239.50 | 9.7 | CODE / NASA | A distance chart of landings (Moon, Mars, Venus, Titan furthest), then Titan from orbit | 2 | **FACT:** "most distant landing". |
| 24 | 2 The Huygens Landing | 240.84–245.10 | 4.3 | — | House mid-roll subscribe card (existing asset, short version) | 1 | |
| 25 | 3 Standing on Titan | 246.00–258.48 | 12.5 | NASA/JPL / CODE | The Huygens surface view (third look, wide, with a CODE suit outline at the horizon), then `pressure` reuse (tight: 1.5) | 2 | Third look: the reframed "standing there" version. |
| 26 | 3 Standing on Titan | 259.18–268.10 | 8.9 | OMNI (flag) | Orbit standing on an orange plain under a hazy sky, taking a slow breath-like look around, calm | 1 | **ORBIT ACTS.** Fallback: CODE `airmix` pie (95% N₂ / 5% CH₄). |
| 27 | 3 Standing on Titan | 269.04–286.96 | 17.9 | CODE | `airmix` pie (95 / 5) → `densegrav`: two bars, air density "≈ 4×" vs gravity "≈ 1/7" → O₂ bar near zero | 4 | **VISUAL MUST, DATA.** |
| 28 | 3 Standing on Titan | 288.12–298.28 | 10.2 | CODE | `rain --seconds 10`: Earth raindrop 6.5 mm at 9 m/s (fast) | 2 | **DATA.** |
| 29 | 3 Standing on Titan | 298.94–313.92 | 15.0 | CODE | `rain` continued: Titan drop 9.5 mm ("marble") at 1.6 m/s beside a snowflake, side by side with the Earth drop | 3 | **VISUAL MUST, DATA.** |
| 30 | 3 Standing on Titan | 314.86–324.44 | 9.6 | NASA/JPL | Titan dunes (Cassini radar, the Belet dunes strip), slow pan; CODE "centuries between showers" | 2 | "Case closed? Just a dry desert?" |
| 31 | 4 Seas of Natural Gas | 325.32–337.84 | 12.5 | NASA/JPL | The Cassini radar mosaic of the north polar lakes (false colour), a slow push to the coastline | 2 | **VISUAL MUST.** "Bays and islands." |
| 32 | 4 Seas of Natural Gas | 338.92–354.22 | 15.3 | NASA/JPL / CODE | The lakes mosaic (second use, Kraken framing) → CODE `scalemap`: the Kraken Mare outline over North America with "≈ 400,000 km²" and Lake Superior ×5 | 3 | **VISUAL MUST, DATA.** |
| 33 | 4 Seas of Natural Gas | 355.14–366.88 | 11.7 | NASA/JPL / CODE | Ligeia Mare radar image (Cassini), then CODE: a radar beam passing through the liquid to the seabed "≈ 160 m"; card "2013" | 2 | **DATA.** |
| 34 | 4 Seas of Natural Gas | 367.92–372.42 | 4.5 | CODE | A depth bar: Kraken "≥ 300 m" next to Ligeia 160 m | 1 | **DATA.** |
| 35 | 4 Seas of Natural Gas | 373.10–385.06 | 12.0 | NASA/JPL / CODE | A Titan interior cutaway (NASA/JPL illustration of the subsurface ocean), then a CODE label "tens of km · water + salts + ammonia" | 2 | **VISUAL MUST.** It is an illustration; label it so. |
| 36 | 4 Seas of Natural Gas | 386.06–388.92 | 2.9 | NASA/JPL | Sunglint off Kraken Mare (Cassini VIMS) | 1 | "Wait..." |
| 37 | 5 Would It Explode? | 389.76–401.44 | 11.7 | NASA APL / CODE | Dragonfly landing animation near a shoreline (APL), then CODE: a thruster plume icon + a "?" spark | 2 | No real fire footage. |
| 38 | 5 Would It Explode? | 402.02–411.64 | 9.6 | CODE | `reserves`: Titan's hydrocarbon bar towering over Earth's oil + gas reserves, "hundreds of times" | 1 | **DATA.** |
| 39 | 5 Would It Explode? | 412.62–424.92 | 12.3 | CODE | `fire`: the fire triangle (fuel, oxygen, heat); Earth's air "21% O₂" lights it | 2 | **VISUAL MUST, DATA.** |
| 40 | 5 Would It Explode? | 425.66–432.96 | 7.3 | CODE | `fire` (second use): Titan with lots of fuel, the O₂ side greyed out | 1 | |
| 41 | 5 Would It Explode? | 433.82–446.86 | 13.0 | CODE | A match and a thruster in Titan air: no flame; a methane lake beside a water pond, both labelled "not explosive" | 2 | **VISUAL MUST.** |
| 42 | 5 Would It Explode? | 447.74–455.56 | 7.8 | CODE | `flipfire`: Earth (gas tank → burn in O₂ air) | 1 | |
| 43 | 5 Would It Explode? | 456.16–463.26 | 7.1 | CODE | `flipfire` reversed: an O₂ tank on the back sprays into the methane sky, with a small flame at the nozzle | 1 | **VISUAL MUST.** |
| 44 | 5 Would It Explode? | 464.44–474.10 | 9.7 | NASA/JPL | Titan haze from orbit, then the north lakes (third look, wide) | 2 | Bridge into ch6. |
| 45 | 6 Wings for Titan | 474.94–494.52 | 19.6 | CODE | `densegrav` (second use) → `lift`: air "4×" and weight "1/7" feeding a wing icon | 4 | **VISUAL MUST, DATA.** Split by reframing. |
| 46 | 6 Wings for Titan | 495.24–501.70 | 6.5 | OMNI (flag) | Orbit hovering effortlessly over orange dunes with small fins out, delighted | 1 | **ORBIT ACTS.** Fallback: CODE "≈ 28× easier" counter over a Dragonfly icon. The "28×" is our own rough sum and is labelled "our estimate". |
| 47 | 6 Wings for Titan | 503.20–516.86 | 13.7 | NASA APL | Dragonfly flight animation over dunes (APL) | 2 | **FACT:** the Dragonfly team quote as an on-screen pull-quote only if SOURCES.md has the exact wording. |
| 48 | 6 Wings for Titan | 517.68–527.30 | 9.6 | NASA APL / CODE | Dragonfly rotorcraft close-up (eight rotors) + card "NO EARLIER THAN JULY 2028"; "car-sized, nuclear-powered" labels | 2 | **WHEN/DATA.** |
| 49 | 6 Wings for Titan | 528.38–540.56 | 12.2 | NASA APL / CODE | Dragonfly landing and charging at dusk (APL); CODE: "arrives 2034", a day/night bar "≈ 8 Earth days" | 2 | **DATA.** |
| 50 | 6 Wings for Titan | 541.82–556.06 | 14.2 | NASA/JPL / CODE | Selk Crater (Cassini radar/VIMS), then CODE "water + organics → primordial soup" | 2 | **VISUAL MUST.** |
| 51 | 6 Wings for Titan | 557.32–566.50 | 9.2 | ESA/NASA | The Huygens descent movie (second use, the last frames down to the surface), ending on the pebble field | 1 | "A time capsule of early Earth." |
| 52 | 6 Wings for Titan | 567.66–582.38 | 14.7 | NASA/JPL | The existing hand-off to 033: Uranus (Voyager 2 / JWST image, PD), tipped on its side, slow rotation | 2 | The house hand-off line. No subscribe ask; no goodbye. |

## Tally

- **Stills or clips used twice or more:**
  - Huygens pebble image: rows 18, 20, 25 (3 looks; row 25 is a composite with the suit outline).
  - Lakes mosaic: rows 31, 32, 44 (three framings).
  - Huygens descent movie: rows 1, 16, 51 (different segments).
  - All others are used once or twice.
- **Code graphics to build:** `pressure`, `orbit16`, `sizes`, `spectrum`, `methane`, `distance`, `cycle`, `airmix`, `densegrav`, `rain`, `scalemap`, `reserves`, `fire`, `flipfire`, `lift`, plus cards, rulers, counters and icon plates.
- **Harvest list:**
  - ESA/NASA: the DISR descent movie, the surface pebbles image, the DISR channel mosaic, the separation animation.
  - Cassini ISS/VIMS/radar: limb haze, detached haze, true-colour Titan + Saturn, Belet dunes, north lakes mosaic, Ligeia Mare, Kraken sunglint, Selk Crater, clouds.
  - NASA/JPL: Cassini animation, the Voyager 1 animation and Titan image, the Titan interior illustration.
  - Dragonfly (APL): the flight, landing and close-up animations.
  - Uranus for the hand-off.
  - Commons: the Huygens portrait, the Kuiper photo (if PD).
- **Flags for the Chief:**
  1. Two OMNI Orbit beats (rows 26, 46), price pass, with fallbacks written.
  2. Kuiper photo licence.
  3. Row 47's quote only if exact in SOURCES.md.
  4. The row 46 "28×" stays labelled as our own estimate (it is "by our own rough sum" in the VO).
  5. Confirm the inferred chapter breaks against the assembler's chapter index.
