# 029 script v01: claims for Gemini to check (Claude, 8 Oct 2026)

The script is `betelgeuse_script_master_v01.md` (review:script 92.2). It was written before SOURCES existed, like 027.

**Gemini:**
- Create `SOURCES.md` from these rows, in the 028 layout: claim, source, **exact quote**.
- Flag anything that's wrong or outdated.
- **No spoken number goes to VO without an exact quote.**
- Spoken wording is Claude's call. Gemini flags errors and doesn't rewrite lines.
- The **MUST QUOTE** rows carry the film.

| # | Spoken claim | Number behind it | Source to check |
|---|---|---|---|
| 1 | Betelgeuse is a red supergiant in Orion's shoulder and will end as a supernova | M1–M2 Iab; core-collapse (type II) expected | Joyce et al. 2020, ApJ 902, 63 |
| 2 | At the Sun's place its surface would reach past Mars into the asteroid belt. **MUST QUOTE** (radius) | about 764 R☉ (Joyce 2020) = 3.55 AU; Mars at 1.52 AU, belt at 2.2–3.3 AU. Is "into the asteroid belt" right at 3.5 AU, or "past the asteroid belt"? | Joyce et al. 2020 |
| 3 | 500–700 light-years away; hard to measure | 168 (+27/−15) pc ≈ 548 ly (Joyce 2020) vs 222 pc ≈ 724 ly (Harper et al. 2017) | Joyce 2020; Harper et al. 2017, AJ 154, 11 |
| 4 | About ten million years old; the Sun is 4.5 billion and halfway | about 8–10.5 Myr | Joyce 2020 (or Dolan et al. 2016) |
| 5 | About 15–20 times the Sun's mass. **MUST QUOTE** | Joyce 2020: present-day 16.5–19 M☉ | Joyce 2020 |
| 6 | Around a hundred thousand times as bright as the Sun | log L ≈ 5.0 | Joyce 2020 or Levesque & Massey 2020 |
| 7 | Find it: up and to the left of Orion's belt; its surface is cooler than the Sun's, so it glows orange | Teff ≈ 3,500–3,600 K vs 5,772 K | Levesque & Massey 2020, ApJL 891, L37 |
| 8 | Great Dimming: from late 2019 to Feb 2020, down to about a third of its usual brightness, the dimmest in more than a century of careful measurements. **MUST QUOTE** | V ≈ 0.5 → 1.61 (Feb 2020) ≈ 36% | AAVSO; Guinan et al. ATel 13512; Montargès et al. 2021 |
| 9 | Cause: a bubble of gas burst from the surface, cooled into dust and blocked part of the star; a cool patch made it deeper; back by spring 2020. **MUST QUOTE** | surface mass ejection + dust (Dupree 2022 calls it an SME) | Montargès et al. 2021, Nature 594, 365; Dupree et al. 2022, ApJ 936, 18 |
| 10 | Now fusing helium into carbon; later stages get faster; the last take years, then days | core He burning (Joyce 2020); Si burning about 1 day | Joyce 2020; Woosley, Heger & Weaver 2002, Rev. Mod. Phys. |
| 11 | Iron fusion costs energy; when the core fills with iron, gravity wins | binding-energy peak at Fe/Ni | Any textbook; Woosley 2002 |
| 12 | In under a second a core heavier than the Sun collapses to the size of a city; layers bounce and blast out | collapse ≈ 0.1–1 s; NS radius about 10–12 km | Woosley 2002; Janka 2012 |
| 13 | A neutron-star teaspoon weighs as much as a mountain | about 10⁹ t per 5 mL. Check whether "mountain" is a fair comparison | NASA Goddard (neutron star explainer) |
| 14 | Neutrinos first, a burst in underground detectors, alert hours before the light | SN 1987A: neutrinos about 3 h before the optical rise. SNEWS | Hirata et al. 1987; Bionta et al. 1987; SNEWS 2.0 (Al Kharusi et al. 2021) |
| 15 | Within days it blazes as bright as the half Moon, visible in daylight, casting shadows at night. **MUST QUOTE** | peak about −10 to −12. Half Moon about −10, full −12.7 | Joyce 2020 or a NASA explainer; Goldberg et al. on the light curve |
| 16 | Bright for weeks, fading over months and years | type II-P plateau about 100 days | standard SN II-P light curves |
| 17 | Only harmful within a few dozen light-years; Betelgeuse is far beyond. **MUST QUOTE** | about 8 pc (≈ 26 ly) for ozone damage (Gehrels 2003); 25–50 ly | Gehrels et al. 2003, ApJ 585, 1169; Melott & Thomas 2011 |
| 18 | If it had exploded around 1500 we'd only be finding out about now | 548–724 ly → light leaving about 1300–1480 arrives now. **Check:** "the year fifteen hundred" fits 548 ly (arriving about 2048), so fine as "about now"? Flag if not | Arithmetic |
| 19 | Best estimate about 100,000 years left. **MUST QUOTE** | Joyce 2020 | Joyce et al. 2020 |
| 20 | A few researchers argue it could go within centuries; most disagree | Saio et al. 2023 (MNRAS) late carbon burning; rebuttals (e.g. Molnár et al. 2023/24, or Joyce's response) | Saio, Nandal et al. 2023; give the rebuttal ref |
| 21 | In 2025 astronomers found a faint companion orbiting about every six years, hidden in the glare, explaining a slow pulse. **MUST QUOTE** | Howell et al. 2025 (Gemini North 'Alopeke), name Siwarha; LSP about 2,100 d (Goldberg 2024; MacLeod 2024) | NASA / NOIRLab press release July 2025; ApJL paper |
| 22 | 1054: Chinese astronomers recorded a new star visible in daylight for more than three weeks; now the Crab Nebula | 23 days in daylight; 653 nights at night | Song Huiyao records; NASA Crab explainer |
| 23 | Much of the oxygen you breathe and the calcium in your bones were made in giant stars and scattered by their explosions | massive-star nucleosynthesis | Woosley & Weaver 1995; a NASA explainer |
| 24 | Long ago a giant star exploded near the cloud that became the Sun | short-lived radionuclides (²⁶Al, ⁶⁰Fe) in meteorites. Keep the claim as "the evidence suggests". **Gemini: is "exploded" too strong (a Wolf-Rayet wind is the alternative)?** | Ouellette et al.; Dwarkadas 2017; a review |

**Tone lock:**
- **The answer to "will it explode soon?" is "probably not for a very long time".** No doom.
- The minority "soon" view gets one fair line.
- No made-up dates.
