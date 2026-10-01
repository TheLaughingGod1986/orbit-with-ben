# Neighbour pass — standing order (1 Oct 2026)

**Source:** Ben via Chief of Staff. Build Orbit longs so they can sit next to big education videos (HOS 002 pattern: Suggested from a TED-Ed neighbour).  
**Scope:** Orbit With Ben only. Proposals only for Saturn packaging — no Studio edits. Locked Saturn title kept. Topic picks stay Ben's call.  
**PR #99:** message thread only — never merge, close, or push that PR.

---

## 1. Saturn (021) — big neighbours + packaging proposals

**Locked title (unchanged):** What Happens When Saturn Loses Its Rings?

### Big neighbours (≥1M views · education / space · Saturn rings or Saturn losing rings)

| # | Views | Channel (internal) | id | Title |
|---|------:|--------------------|----|-------|
| 1 | 7.16M | BBC Earth Science | `6Bv8g5xBJSo` | How Saturn Got Its Rings \| The Planets |
| 2 | 3.67M | SolarBalls | `LZo9Ba8-jMI` | Why does Saturn have rings? |
| 3 | 1.98M | The Space Race | `PMFE_I6xseA` | Saturn Is The Scariest Planet In Our Solar System |
| 4 | 1.64M | Crash Course | `E8GNde5nCSg` | Saturn: Crash Course Astronomy #18 |
| 5 | 1.50M | Astrum Extra | `33yOQsptNis` | What They Didn't Teach You in School about Saturn \| 4K |
| 6 | 1.40M | Insider Tech | `9hYbrm54VkQ` | Saturn Is Officially Losing Its Rings |

**Near-miss (science lock, under 1M):** NASA Goddard `mN8o90UbpmE` — *Saturn's Rings Are Disappearing* (~724k) — source of “ring rain”; keep as subject vocabulary even though it misses the 1M bar.

Kurzgesagt / TED-Ed / Veritasium / SciShow Space / PBS Space Time did **not** return a clean 1M+ Saturn-rings hero in the probe — the pool above is still ≥3 and education-adjacent.

### Proposed description first lines (do not apply in Studio yet)

Option A (ring-rain lead):  
`Saturn's rings are made of ice particles — and they are disappearing through ring rain.`

Option B (young rings + loss):  
`Saturn did not always have its rings. Scientists now think those ice rings are younger than we thought, and they are raining onto the planet.`

Option C (question echo of locked title):  
`What happens when Saturn loses its rings? Ice particles fall as ring rain, and the solar system's crown jewel changes shape.`

Primary keyword still belongs in the first ~100 characters: **Saturn** + **loses its rings** / **ring rain**.

### Proposed subject-only tags (5–8 · no channel names)

1. `saturn rings`  
2. `saturn losing rings`  
3. `ring rain`  
4. `ice particles`  
5. `gas giant`  
6. `cassini`  
7. `solar system`  
8. `saturns rings` *(neighbour spelling variant; optional)*

---

## 2. Live Orbit longs — “Content suggesting this video” (read-only)

**API:** YouTube Analytics `insightTrafficSourceDetail`.

| Filter tried | Result |
|---|---|
| `insightTrafficSourceType==SUGGESTED` | **Invalid** (HTTP 400) — not exposed on this API surface |
| `insightTrafficSourceType==RELATED_VIDEO` | **Works** — closest read-only stand-in for Studio's “Content suggesting this video” |

Pulled for public longs (ids from channel inventory). Most rows are empty at current view counts. Non-empty **RELATED_VIDEO** referrers:

| Orbit long | id | Suggesting video (related) | Views on referrer | Views attributed |
|---|---|---|---:|---:|
| What Happens If You Get Near a Neutron Star | `Yk1tLh23rko` | Alan Becker — *Animation vs. Physics* (`ErMSHiQRnc8`) | 49.2M | 3 |
| same | | Alan Becker — *Animation vs. Geometry* (`VEJWE6cpqw0`) | 30.3M | 1 |
| same | | T. Folse Nuclear — nuclear engineer reacts to Animation vs. Physics (`H7OW_nSCcl0`) | 2.2M | 1 |
| same | | The Chill Zone — nerding out react (`BPlcUh_hkT0`) | 0.37M | 1 |
| JWST Found Galaxies That Shouldn't Exist Yet | `ziKBPJ6FY0U` | ParkerZen sleep / Brian Cox remix (`AcNTQaeXxFs`) | 90k | 1 |
| Why Haven't We Found Aliens Yet? (Fermi) | `Mo93x0fxB1Q` | Orbit Short *This Planet's Night Never Cools Down* (`tEOHYQbcgOw`) | 16 | 1 |

**Andromeda, Moon Leaving, Europa, Last Star, Alien Worlds, Black Hole:** RELATED_VIDEO rows empty in this pull.

**Read:** No classic TED-Ed / Kurzgesagt / Veritasium education long is yet suggesting Orbit at measurable volume. The only large external pool touching us is **Alan Becker animation-education** → Neutron Star (tiny absolute counts). Packaging for big education neighbours is forward-looking; it is not yet showing up in Analytics.

Raw dump: `/tmp/orbit_suggesting.json` (machine-local; not committed).

---

## 3. Playbook change

Neighbour pass added as a **blocking** step before topic lock:

- `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §2  
- `AGENTS.md` (topic pick section)  
- `.cursor/rules/orbit-studio.mdc` · `orbit-build-long.mdc`  
- `templates/TOPIC_OPPORTUNITY_SCORE.md`  
- `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` §2b  

Rule: ≥3 big neighbours ≈1M+ views; subject-only tags and description words; Ben still picks the topic.

---

## 4. Ranked future Orbit topics (strongest big-neighbour pools)

Not already a live Orbit long. **Ben decides.** Evidence only.

| Rank | Topic angle (working) | Pool strength | Example neighbours (internal) |
|---:|---|---|---|
| 1 | Could We Build a Dyson Sphere? | Very strong | Kurzgesagt *How to Build a Dyson Sphere* ~24.5M (`pP44EPBMb8A`); stellar engines / megastructure cluster |
| 2 | What Happened to Venus? / Why Venus Became Hell | Very strong | Kurzgesagt *How To Terraform Venus* ~22.7M (`G-WO-z-QuWI`); Cool Worlds *What the Hell Happened to Venus?* ~1.3M |
| 3 | Are We Living in a Simulation? | Strong (brand caution) | Kurzgesagt *Is Reality Real? The Simulation Argument* ~21.7M (`tlTKTTt47WE`) — wonder framing only; reject conspiracy packaging |
| 4 | What If You Traveled Near Light Speed? (twin paradox / time dilation) | Strong · TED-Ed-shaped | TED-Ed twin paradox ~5.9M (`h8GqaAp3cGs`); Kurzgesagt time paradox ~15.0M; ScienceClic / minutephysics cluster |
| 5 | What Is a Quasar? / The Light That Kills Galaxies | Strong single-hero | Kurzgesagt *The Black Hole That Kills Galaxies – Quasars* ~11.2M (`V4Z8EdiJxgk`) — thinner second/third tier; needs one more 1M+ before lock |

**Already live (do not re-pick):** Black Hole fall, Neutron Star, Fermi, Europa, Last Star / heat-death adjacent, Moon Leaving, JWST, Andromeda, Alien Worlds.  
**In flight:** Saturn 021 (this report). Jupiter 020 and Sun 022 keep their own neighbour passes before any re-lock.

---

## 5. Ask for Ben / Claude

1. OK to keep Saturn locked title and only change **description + tags** after Ben signs packaging?  
2. Which of the five ranked future topics (if any) should enter the next topic-score round?  
3. No Studio writes from this report.
