# One-Page Topic Go/No-Go Sheet — `OWB:036` Mercury Polar Ice

- **Film:** `036_Why-Is-There-Ice-On-Mercury` (`OWB:036`, queued in `jobs/WIP.json` `next` after `OWB:035`)
- **Prepared:** 7 Nov 2026 (`J2327`, agent `macbook-2`, £0 spend; `01_Script/*` and `WIP.json` untouched)
- **Preceding Ruling:** `jobs/reviews/J1900/CHIEF_EDITORIAL_RULING_2026-11-04.md` (`DEFER` topic / `FIX` script)
- **Target Window:** Mid-to-late December 2026 Sunday/Wednesday long slot (enters `active` after `035` when a second active OWB film reaches Ben's watch)

---

## 1. Rule-E Topic Readiness Verdict: **GO ON TOPIC UNDER RULE E COMPARABLE DEMAND (OR EXPLICIT SHORT-FIRST WAIVER), WITH SPECIALIST `v02` REWRITE + `FACTS` ON ENTRY**

| Rule-E Rubric Gate | Status | Evidence Summary (`2026-11-07 01:44 UTC`) |
|---|---|---|
| **1. Neighbour check (`≥3` ed/space videos `≈1M+`) & no near-duplicate** | **PASS (Very Strong)** | **7 verified education/space longs at `1.16M–4.07M` views**, led by Astrum's *What They Didn't Teach You at School about Planet Mercury \| NASA's MESSENGER Discoveries* `B588JHKSlEE` (**4,071,155**), Astrum's 2 Sep 2026 *Why Is the Closest Planet to the Sun So Cold?* `YQ7DWNhjOpk` (**2,703,364 views in 65 days** — direct polar-cold/ice paradox!), Astrum's `1MwGXzKjFfY` (**2,621,785**), BBC Earth Science's `XhKAxwfNW_c` (**2,048,871**), CrashCourse's `P3GkZe3nRQ0` (**1,674,211**), Astrum Extra's `qBLroiXlFT0` (**1,506,397**), and Astrum's `59ZOgGBAXNU` (**1,159,298**). Zero near-duplicates on OWB (`001`–`035`) or HOS (`001`–`018`). |
| **2. Audience & Short-fit evidence** | **PASS (Rule E Comparable Views) / Short-First Gap Note** | Public OWB Mercury Short **`vlkj8RQKmH8`** (*Why Does a Day on Mercury Last Two of Its Years?*, 21 s, published `2026-10-24`) has **851 views** (2nd highest in the standalone cohort) and **76.1% avg viewed**, but **32.1% stayed-to-watch** (`< 40%` threshold, `studio_ctr.json` 4 Nov) and covers day-length resonance rather than polar ice (`0` OWB Shorts exist on Mercury polar ice). Under `AGENTS.md` Rule E rubric item (2) (*"search demand, a comparable video's views, or a Short that did well"*), audience demand is **PASS** via Astrum's **2.70M-view** recent breakout `YQ7DWNhjOpk` + **4.07M-view** `B588JHKSlEE` + `vlkj8RQKmH8`'s 851 views + `"space ice"` search demand. If applying strict `FAMILIAR_DANGER_STRATEGY.md` Short-first (`≥200 views` & `≥40% stayed` on a polar-ice Short), Chief/Rule-E reviewer must record an explicit Short-first waiver on entry. |
| **3. Script & `SOURCES.md` status (`v01` untouched)** | **REQUIRES `v02` REWRITE + `FACTS`** | `01_Script/mercury_polar_ice_script_master_v01.md` (1,233–1,278 spoken words, automated 95.8) and `SOURCES.md` (10 pre-quoted rows, all `TO VERIFY`) are preserved byte-identical. Per `J1900`, **do not lock `v01` as-is**: queue a specialist `v02` rewrite + formal Gemini `facts` pass + direct `MUST QUOTE` verification upon entry. |
| **4. Reference-channel packaging (`LEARNINGS` 15, 18, 19, 20)** | **READY** | **Series (Rule 20):** `Real Worlds`. **Collision-free Rule-15 title (≤50 chars):** `Why Mercury's Shadowed Craters Are Full of Ice` (46 chars, 0 collisions) or `Why the Planet Closest to the Sun Has Ice` (41 chars, 0 collisions; avoid 28-char `Why Is There Ice on Mercury?` which collides with `s2wXNsvNKdQ`, and 59-char draft H1 which exceeds 50 chars). **Rule-18 real-imagery variant:** `What MESSENGER Saw Inside Mercury's Polar Craters` (49 chars, 0 collisions). **Rule-19 real frame:** NASA/JHUAPL/CIW MESSENGER global enhanced-colour portrait `PIA19411` (top-band hook `ICE HERE?`, yellow `ICE`). |

---

## 2. Exact Action Plan When an OWB `active` Slot Frees

When `OWB:036` reaches the front of `jobs/WIP.json` `next` and an active OWB film reaches Ben's watch:
1. **Promote `OWB:036` in `jobs/WIP.json`** and mark `036 topic` `done` under Rule E (recording the comparable-views / Short-first waiver note for `vlkj8RQKmH8` at 851 views / 32.1% stayed + `YQ7DWNhjOpk` at 2.70M views).
2. **Queue specialist `script` job (`v02` rewrite, preserving `v00`/`v01`)** to resolve all `J1900` editorial items:
   - Claim-first opening naming Mercury + **complete causal answer before `0:30`** (Mercury's nearly upright 2° spin-axis tilt keeps deep polar craters like Prokofiev in permanent −180 °C shadow) and one central question by `~0:50` (remove 3-question agenda);
   - Make persistent shadow, how MESSENGER proved water ice, and exposed vs organic-buried ice the causal spine; subordinate flyby/mass/core catalogues;
   - Unbundle `DATA` into **one idea per animated graphic** with real moving imagery between graphics and spoken/sourced `SCALE` comparisons;
   - Shorten `FACT` labels >4 words (`A day lasts 2 years` [5w], `Core is 85% of radius` [5w]) to `≤4 words`;
   - Replace sourced yellow radar maps (`PIA16522`), orbital diagrams, and labelled reflectance montages in `[VISUAL MUST]` with compliant own `code_graphics.py` renders + unlabelled real NASA MESSENGER photography (`PIA19411`, `PIA18748`);
   - Set `15–20 s` moving end-screen hold and verify `037` Milky Way Centre hand-off title.
3. **Queue dependent formal Gemini `facts` job (`agy`)** across all 10 `SOURCES.md` rows and `J1900` verification targets (2° axial tilt & reference plane; night minimum vs permanent-shadow temp; solar-day/year wording; 10–20 cm organic blanket certainty; hollows age/process/certainty; spacecraft dates/masses/altitudes/image counts; current BepiColombo arrival date [check ESA's updated schedule vs Nov 2026]; people years & portrait rights).
4. **Queue dependent Rule-E / Chief script lock (`CLAUDE_QUOTE_CHECK_v02.md` + `review:script ≥ 90` + signed `PRE_BUILD_VIDIQ_AUDIT.md` + `gate:episode` PASS) → `vo` job.**
