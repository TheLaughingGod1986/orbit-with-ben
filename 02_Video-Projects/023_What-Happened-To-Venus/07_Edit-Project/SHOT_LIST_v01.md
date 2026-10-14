# Venus 023 — SHOT_LIST_v01 (Claude review)

**Episode:** 023 What Happened to Venus?  
**Air target:** Sun 25 Oct 2026 18:00 UK (not Studio-scheduled yet)  
**Script lock:** `01_Script/venus_script_master_v02.md`  
**VO lock:** `02_Voiceover/venus_vo_v01.mp3` — Claude VO-PASS (comment 5982369937); `vo_check` PASS  
**VO duration:** **509.58 s** (~8.49 min) · 1247 words · 6 chapters · 0.7 s gaps (cards skipped in VO)  
**Drafted:** 4 Oct 2026 ~18:05 London · Grok Bot for Claude review  
**Status:** **DRAFT — no picture generation until Claude PASS on this list**

---

## Meta / credit rules (generation NOT started)

| Rule | Value |
|---|---|
| Spend until Claude PASS on this list | **None** — no Veo / Flow / Vertex calls |
| When generation starts | Free **Vertex** credit first (Flow out until monthly reset); **never past £0** without Ben |
| Orbit / invented worlds | **Vertex Omni only** (Orbit house lock) |
| Frame 0 | **NASA plate already moving** — no fade-up, no title, no Orbit at open |
| Cut pace | Script VISUAL MUST: ~**4–6 s** per cut |
| Venera colour panoramas | **HOLD** unless reuse/license terms are clear (Soviet lander stills). Magellan “simulated colour” products that credit NASA/JPL remain OK |
| Chapter cards | VO skipped spoken cards; 0.7 s gaps only. Rows marked **CARD** below are optional Remotion inserts for Claude to keep/drop (Saturn-style ~3.5 s would need VO retime — prefer short gap cards or skip) |
| CSV sibling | Not required for Claude gate; MD path is the review artifact. Optional `shot_list_v01.csv` after PASS if checker tooling needs it |

**Preferred plate families:** NASA Magellan (radar / perspectives), Mariner 10 cloud globe, Parker Solar Probe WISPR nightside, Pioneer Venus probe/descent art, DAVINCI/VERITAS/EnVision NASA–ESA mission art. Two-Venus beat (ch.3) + Orbit beats are the only rows that likely need Omni generation.

---

## Summary counts (v01 draft)

| Source type | Rows | Est. picture time (s) | Notes |
|---|---:|---:|---|
| **NASA** (plate / SVS / mission art) | 78 | ~452 | Ken Burns push ~5–6% on stills; muted if source has music/VO |
| **GENERATE (Omni)** | 5 | ~28 | Two-Venus ×2 + Orbit between them + Orbit at Earth-line + one early-Venus spin optional spare |
| **HOLD** | 3 | ~12 | Venera surface colour; chalk cliffs if non-NASA; Pioneer still if art ID unclear |
| **CARD / SUB / BREATH** | 7 | ~8 | Chapter gaps + subscribe Remotion; no Vertex |
| **Total picture rows (excl. CARD/BREATH)** | 86 | ~492 | + gaps/cards ≈ VO **509.58 s** |
| **vs VO** | — | **509.58** | Align within ±1 s after Claude PASS; chapter walls from `credits_before_after.json` + `words.json` |

**Generate budget (post-PASS only):** ~5 Omni clips × ~6 s usable ≈ small Vertex free-credit draw. Prefer NASA everywhere else.

**Blockers for Claude:**
1. Confirm **HOLD** on Venera 13/14 colour panoramas (or clear reuse terms).
2. Confirm **CARD** policy: skip spoken cards (match VO) vs insert Remotion titles in 0.7 s gaps.
3. Confirm Omni prompts for **two-Venus** + **two Orbit** beats before any spend.
4. Parker WISPR nightside: prefer NASA press still/video (`NASA/APL/NRL`) — **no PIA number found**; credit line TBD at harvest.
5. DAVINCI descent art: NASA GSFC/CI Labs / SVS — harvest ID at pull time.
6. Earth chalk/limestone beat: use NASA ocean + Blue Marble; **omit chalk cliffs** if no clear NASA/public plate (HOLD row).

---

## Chapter wall-clock (from VO concat)

| Ch | Title | vo_in | vo_out | Dur (s) |
|---:|---|---:|---:|---:|
| 0 | Open | 0.00 | 42.88 | 42.88 |
| — | gap | 42.88 | 43.58 | 0.70 |
| 1 | The Twin Next Door | 43.58 | 142.22 | 98.64 |
| — | gap | 142.22 | 142.92 | 0.70 |
| 2 | A Blanket With No Way Out | 142.92 | 223.80 | 80.88 |
| — | gap | 223.80 | 224.50 | 0.70 |
| 3 | Where Did the Water Go? | 224.50 | 347.54 | 123.04 |
| — | gap | 347.54 | 348.24 | 0.70 |
| 4 | The Line Earth Hasn't Crossed | 348.24 | 416.88 | 68.64 |
| — | gap | 416.88 | 417.58 | 0.70 |
| 5 | Going Back | 417.58 | 509.58 | 92.00 |
| | **Total** | | | **509.58** |

Timings below are approx from `words.json` (ElevenLabs Scribe); refine with `align_shot_list.py`-style pass after Claude PASS.

---

## Shot table

Columns: **#** · **vo_in–out** · **source** · **id / asset** · **move** · **VO / beat** · **notes**

### Ch 0 — Open (0.00–42.88) · VISUAL MUST: Magellan Maat Mons already pushing; cut 4–6 s; no Orbit

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 1 | 0.00 | 5.44 | NASA | **PIA00254** Magellan Maat Mons 3-D perspective | push 6% from frame 0 | “Venus is the planet most like Earth. So what happened to it?” | **Frame 0 lock.** Already moving. Alt twin: PIA00106 (same subject, 10× exag). No fade, no title, no Orbit. |
| 2 | 5.44 | 10.80 | NASA | PIA00254 (continue) or PIA00106 tighter crop | push 6% | “This is the ground on Venus, seen through the clouds by radar. Why radar?” | Same volcano/plains; cut on “radar”. |
| 3 | 10.80 | 15.50 | NASA | **PIA00240** Lakshmi Planum (radar plains) | push 5% | “Because ordinary light cannot get through. It is hot enough to melt lead.” | Plains under heat line. |
| 4 | 15.50 | 20.80 | NASA | **PIA00241** Lakshmi + Maxwell / tessera edge | push 5% | “The air presses down like the sea nearly a kilometre deep.” | Pressure beat — dense terrain. |
| 5 | 20.80 | 24.54 | NASA | PIA00087 Lavinia plains / lava | push 5% | “No machine we have landed there could survive it for much more than two hours.” | **No Venera still** here (HOLD elsewhere). |
| 6 | 24.54 | 30.20 | NASA | **PIA23791** Mariner 10 Venus globe | push 5% | “And this world is almost the size of yours. It is made of the same rock.” | Cloud-wrapped globe enters. |
| 7 | 30.20 | 36.32 | NASA | PIA23791 (continue) + subtle Ken Burns | push 5% | “It even takes in less sunlight than Earth does, and it is still the hottest planet in the solar system.” | Stay on globe; Sun out of frame. |
| 8 | 36.32 | 42.88 | NASA | Magellan global mosaic / cloud-wrapped Venus (e.g. Magellan hemispheric — harvest PIA at pull) | push 5% | “In this film I will show you how that can be true, where its water went, and why the answer is still open.” | Promise beat; end open on Venus disk. |
| 9 | 42.88 | 43.58 | BREATH/CARD | optional Remotion “The Twin Next Door” | — | (gap) | Claude: keep short title in gap **or** skip to match VO. |

### Ch 1 — The Twin Next Door (43.58–142.22) · VISUAL MUST: Mariner 10 + Earth same size; Sun out; no Orbit; no text on plate

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 10 | 43.58 | 46.98 | NASA | PIA23791 Mariner 10 | push 5% | “Start with what the two planets share.” | |
| 11 | 46.98 | 55.00 | NASA | PIA23791 | push 5% | Size/mass twin lines | Hold Venus disk. |
| 12 | 55.00 | 66.86 | NASA | **AS17-148-22727** Blue Marble (or PIA00114 Earth family) | push 5% | “From a distance, it is the closest thing to a second Earth…” | Side-by-side edit intent: Venus then Earth same scale (split or match-cut). |
| 13 | 66.86 | 83.84 | NASA | PIA23791 | push 5% | Closer to Sun / twice the sunlight / “nearer the fire” | Sun **out of frame**. |
| 14 | 83.84 | 96.00 | NASA | PIA23791 contrast-enhanced cloud bands | push 6% | Bright cloud / three-quarters reflected / soaks up less | Albedo paradox setup. |
| 15 | 96.00 | 109.66 | NASA | Magellan Maat Mons PIA00106 | push 6% | “Less light in… four hundred and sixty-five degrees… paradox” | Surface under paradox. |
| 16 | 109.66 | 119.96 | NASA | Magellan plains PIA00240 | push 5% | “Heat is not about how much light arrives… cannot get out.” | |
| 17 | 119.96 | 130.00 | NASA | Magellan perspective plains (Sedna Planitia / lava) | push 5% | “What would you see if you stood there? Not darkness… dim orange daylight…” | Orange grade on Magellan sim-colour OK (NASA/JPL product). |
| 18 | 130.00 | 142.22 | NASA | Magellan low plains / haze grade | push 5% | Never see the Sun / slow wind / pushes like a river | End chapter on surface stillness. |
| 19 | 142.22 | 142.92 | BREATH/CARD | optional “A Blanket With No Way Out” | — | (gap) | Claude keep/skip. |

### Ch 2 — A Blanket With No Way Out (142.92–223.80) · VISUAL MUST: Magellan plains → Earth chalk/ocean; carbon in sky vs rock; no Orbit in the heat

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 20 | 142.92 | 149.02 | NASA | Magellan CO₂ world — global Venus + haze | push 5% | “The air of Venus is ninety-six percent carbon dioxide…” | |
| 21 | 149.02 | 165.00 | NASA | Magellan radar plains sequence (PIA00240 / PIA00087) | push 5% | CO₂ greenhouse / ninety times thicker / heat in not out | Cut ~5 s. |
| 22 | 165.00 | 177.56 | NASA | Magellan pole-to-equator mosaic family | push 5% | Day/night same temperature | Uniform heat. |
| 23 | 177.56 | 184.64 | NASA | Magellan → cut to Earth | push 5% | “Here is the turn. Earth has roughly as much carbon dioxide…” | |
| 24 | 184.64 | 195.00 | NASA | Blue Marble / ocean still (NASA Earth) | push 5% | “It is in rock. Limestone, chalk and seabed…” | **Chalk cliffs:** HOLD if no clear NASA plate — prefer ocean + carbonate teaching via ocean still. |
| 25 | 195.00 | 202.34 | NASA | NASA ocean / Earth water cycle still | push 5% | Rain, rivers, sea lock carbon into floor | |
| 26 | 202.34 | 212.74 | NASA | Magellan plains return | push 5% | Question changes: why no water to put CO₂ away | |
| 27 | 212.74 | 218.76 | CARD/SUB | Remotion subscribe card (house) | — | “We make one of these every week…” | No Vertex. No Orbit required. |
| 28 | 218.76 | 223.80 | NASA | Magellan / Mariner 10 | push 5% | “The water is the mystery… clue in the air” | Bridge into ch.3. |
| 29 | 223.80 | 224.50 | BREATH/CARD | optional “Where Did the Water Go?” | — | (gap) | Claude keep/skip. |

### Ch 3 — Where Did the Water Go? (224.50–347.54) · VISUAL MUST: two young Venuses 4–6 s each; **Orbit between them**; Pioneer for 1978

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 30 | 224.50 | 236.66 | NASA | **Pioneer Venus** probe / descent art (NASA) | push 5% | 1978 NASA probe tasted the air / trace of water | Harvest official NASA Pioneer Venus Large Probe art ID at pull. If only unclear third-party art → HOLD swap to Magellan + caption-free probe silhouette Remotion. |
| 31 | 236.66 | 247.48 | NASA | Pioneer / Magellan upper-atmosphere haze | push 5% | Deuterium / heavy hydrogen ~100× Earth | |
| 32 | 247.48 | 268.82 | NASA | Magellan + schematic-free escape beat (plate only) | push 5% | Fingerprint / light H escapes / Venus lost water | No baked-in captions. |
| 33 | 268.82 | 275.70 | NASA | Magellan global | push 5% | “How much… Was it ever an ocean?” | Open question hold. |
| 34 | 275.70 | 291.78 | NASA | Magellan / Mariner 10 slow-spin feel (slow push) | push 4% | Spin 243 days retrograde / day longer than year | |
| 35 | 291.78 | 305.00 | **GENERATE** | Omni · **early Venus A — shallow sea under bright dayside cloud** | — | Way et al. 2016 model beat | **GENERATE.** 4–6 s. Label nothing on plate. Mild weather, shining cloud, shore. |
| 36 | 305.00 | 312.96 | **GENERATE** | Omni · early Venus A continue / gentle push | — | “…shallow oceans and mild weather for billions of years.” | Same world continuity. |
| 37 | 312.96 | 325.00 | **GENERATE** | Omni · **early Venus B — hot steaming sky, no shore** | — | Turbet et al. 2021 nightside-cloud / no ocean | **GENERATE.** 4–6 s. Steam lid, no shoreline. |
| 38 | 325.00 | 331.34 | **GENERATE** | Omni · early Venus B continue | — | “…oceans may never have formed.” | |
| 39 | 331.34 | 338.98 | **GENERATE** | Omni · **Orbit small between the two Venuses** | — | “Both are careful models, and they disagree.” | **ORBIT ACT.** Visor tilted; turns from A to B; no words on plate. Vertex Omni only. **Not at frame 0.** |
| 40 | 338.98 | 347.54 | NASA | Magellan Maat Mons / plains | push 5% | “Either way… Water gone. Carbon in the sky. Heat with nowhere to go.” | Land back on real Venus. |
| 41 | 347.54 | 348.24 | BREATH/CARD | optional “The Line Earth Hasn't Crossed” | — | (gap) | Claude keep/skip. |

### Ch 4 — The Line Earth Hasn't Crossed (348.24–416.88) · VISUAL MUST: Earth → Sun (022 plate reuse) → Venus; Orbit looks back at Earth; no disaster imagery

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 42 | 348.24 | 350.92 | NASA | Blue Marble | push 5% | “So why Venus and not Earth?” | |
| 43 | 350.92 | 373.58 | NASA | Magellan + Earth alternate | push 5% | Distance / water vapour / line / Venus wrong side | Calm science cuts; no red city skies. |
| 44 | 373.58 | 389.88 | NASA | Earth ocean/cloud + **reuse Sun plate from 022** (NASA solar disk) | push 5% | Earth safe for now / Sun brightening 1%/110 Myr / line reaches Earth ~1 Gyr | Pull Sun still from `022_Is-the-Sun-Getting-Brighter` NASA pool if present; else NASA SDO/AIA still. |
| 45 | 389.88 | 409.60 | NASA | Blue Marble calm | push 5% | Not next-century warning / fossil-fuel runaway unlikely / Venus is deep time | **No disaster imagery.** |
| 46 | 409.60 | 416.88 | **GENERATE** | Omni · **Orbit small near Venus looking back at Earth’s blue edge** | — | “What it shows is how thin the difference is…” | **ORBIT ACT.** Quiet, noticing; brighter Venus behind. Vertex Omni only. |
| 47 | 416.88 | 417.58 | BREATH/CARD | optional “Going Back” | — | (gap) | Claude keep/skip. |

### Ch 5 — Going Back (417.58–509.58) · VISUAL MUST: Parker WISPR → DAVINCI art; return Maat Mons; no Orbit on last shot

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 48 | 417.58 | 420.88 | NASA | Magellan tessera / Maxwell (PIA00241) | push 5% | “The answer is waiting on the ground.” | |
| 49 | 420.88 | 435.48 | NASA | Magellan lava plains + tessera blocks | push 5% | Repainted with lava / tesserae older / rocks may remember water | |
| 50 | 435.48 | 445.00 | **HOLD** | Venera 13 surface colour panorama | — | “People have landed… 1982 Soviet lander… two hours” | **HOLD.** Reuse/license terms unclear for colour panoramas. Fallback: Magellan surface + VO only; or NASA NSSDCA diagram without Venera photo. |
| 51 | 445.00 | 454.82 | NASA | **Parker Solar Probe WISPR** Venus nightside glow (NASA/APL/NRL press still or video, muted) | push 5% / slow | 2021 night-side surface through clouds | No PIA found at draft time — credit `NASA/Johns Hopkins APL/Naval Research Laboratory`. Mute if video has audio. |
| 52 | 454.82 | 465.00 | NASA | **DAVINCI** probe-toward-Alpha-Regio mission art (NASA GSFC / CI Labs / SVS) | push 5% | “NASA chose two missions… DAVINCI… Alpha Regio” | No launch-date promise on plate text. |
| 53 | 465.00 | 475.72 | NASA | **VERITAS** orbiter art + **EnVision** ESA art (harvest) | push 5% | VERITAS map / Europe EnVision | Credit NASA + ESA correctly; no VenSAR promise. |
| 54 | 475.72 | 488.40 | NASA | Magellan Maat Mons PIA00254 | push 6% | Clearest record / keeping heat / losing water | Return toward open picture. |
| 55 | 488.40 | 495.12 | NASA | Mariner 10 + Magellan match-cut | push 5% | “What if Venus was never the monster, but a twin…” | Wonder, not fearbait. |
| 56 | 495.12 | 505.82 | NASA | Venus as morning/evening star context — Magellan globe / Mariner 10 | push 5% | Bigger question in your sky / how close did Earth come | No Orbit on closing beats. |
| 57 | 505.82 | 509.58 | NASA | **PIA00254** Maat Mons — same as open, still moving | push 6% | “Next week: what happens to your clock near the speed of light.” | **VISUAL MUST return.** Music may fade. **No Orbit, no goodbye card, no subscribe graphic.** End screen later in Studio. |

---

## Generate queue (post Claude PASS only)

| Priority | Asset | Est. | Model | Prompt intent (short) |
|---:|---|---:|---|---|
| 1 | `venus_early_ocean_cloud_omni_v01` | ~6–8 s | Vertex Omni | Young Venus, shallow sea, bright dayside cloud shade, mild; no text; Orbit house grade |
| 2 | `venus_early_steam_lid_omni_v01` | ~6–8 s | Vertex Omni | Young Venus, no shore, hot steaming sky, nightside cloud lid feel; no text |
| 3 | `orbit_between_two_venus_omni_v01` | ~5–6 s | Vertex Omni | Orbit small between two Venuses; turns A→B; visor tilt; ask without words |
| 4 | `orbit_looks_back_earth_omni_v01` | ~5–6 s | Vertex Omni | Orbit near Venus looking at Earth’s blue edge; quiet; Venus brighter behind |
| — | Spare early-Venus spin | optional | Omni | Only if Claude wants a spin-model insert without dual worlds |

**Do not generate** until Claude PASS. Flow first is N/A while Flow is out — use free Vertex credit; stop at £0.

---

## HOLD / resolve before picture pull

| Item | Reason | Fallback |
|---|---|---|
| Venera 13/14 colour panoramas | Soviet lander stills — reuse terms not verified for OWB | Magellan NASA plates only under lander VO |
| Earth chalk cliffs | May not be NASA | NASA ocean / Blue Marble only |
| Pioneer Venus art exact PIA | Confirm at harvest | Magellan + Remotion probe glyph |
| Parker WISPR PIA | Press package, no PIA in draft | NASA/APL/NRL URL + credit line |
| Chapter CARD length | VO has 0.7 s gaps only | Prefer skip or ultra-short Remotion; do not retime VO without Claude |

---

## Claude review checklist

- [ ] Frame 0 = Magellan Maat Mons moving (PIA00254/PIA00106) — PASS/FAIL  
- [ ] No Orbit in open / heat chapter / final shot — PASS/FAIL  
- [ ] Two-Venus GENERATE + Orbit-between GENERATE — PASS/FAIL prompts  
- [ ] Orbit Earth-line GENERATE — PASS/FAIL  
- [ ] Venera HOLD — confirm omit or clear terms  
- [ ] CARD gaps — skip vs Remotion  
- [ ] NASA-vs-generate balance OK for free Vertex remaining  
- [ ] **PASS → picture may start** (Vertex free credit; Omni for Orbit/invented; never past £0)

---

## Paths

| Artifact | Path |
|---|---|
| This list | `02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/SHOT_LIST_v01.md` |
| Script | `02_Video-Projects/023_What-Happened-To-Venus/01_Script/venus_script_master_v02.md` |
| Sources | `02_Video-Projects/023_What-Happened-To-Venus/01_Script/SOURCES.md` |
| VO | `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.mp3` |
| Words | `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/words.json` |
| Template ref | Saturn `021_.../07_Edit-Project/shot_list_v03i.csv` + `SHOT_LIST_v03b_REVIEW.md` |

*v01 — draft for Claude. No generation. No Studio/Buffer touch.*
