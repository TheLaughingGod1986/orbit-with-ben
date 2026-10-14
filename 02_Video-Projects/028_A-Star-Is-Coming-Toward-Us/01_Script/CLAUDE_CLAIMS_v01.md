# 028 script v01: claims for Gemini to check (Claude, 7 Oct 2026)

The script is `star_coming_script_master_v01.md`. It scored 91 on review:script. It was written from Gemini's `SOURCES.md` (480cc6f).

**Gemini:**
- Merge any row that `SOURCES.md` doesn't already cover into it, under the heading **"Added by Claude for script v01 (7 Oct). Gemini: verify each row and add the exact quote"**.
- Check every row below against the spoken line, and flag anything wrong.
- Spoken wording is Claude's call. Gemini flags errors and doesn't rewrite lines.
- **Three rows need an exact quote before VO.** Rows 4, 13 and 15 are marked **MUST QUOTE**.

| # | Spoken claim | Number behind it | Source to check |
|---|---|---|---|
| 1 | Gliese 710 will pass closer than any star we know of, in about 1.3 million years, almost straight at the Sun | t ≈ 1.29 Myr; closest known encounter | Bailer-Jones 2022 ApJL 935 L9; de la Fuente Marcos 2022 RNAAS 6 136 |
| 2 | About 62 light-years away now, in Serpens | 19.07 pc, 62.2 ly | Gaia DR3 via Bailer-Jones 2022 |
| 3 | An orange dwarf, a little smaller and cooler than the Sun | K7 V | Gray et al. 2006 |
| 4 | About sixty percent of the Sun's mass. **MUST QUOTE**: SOURCES gives 0.57–0.60 M☉ as a paraphrase | 0.57–0.60 M☉ | Berski & Dybczyński 2016 A&A 595 L10 (the mass they adopt), or any catalogue mass with a quote |
| 5 | Too faint to see by eye; you'd need binoculars | V = 9.69; naked-eye limit about 6 | SIMBAD |
| 6 | Coming towards us at about 14 km/s, more than 50,000 km/h, almost none of it sideways | rv −14.42 km/s = 51,900 km/h; transverse ≈ 0.04 km/s | Bailer-Jones 2022 Table 1 |
| 7 | Proxima is about four light-years away, our nearest neighbour today | 4.24 ly | Must match 026 |
| 8 | In the late 1990s Hipparcos put the pass at about a light-year, with a huge uncertainty | 0.267 pc median (90% CI 0.101–0.444); Bobylev 0.311 ± 0.167 pc | García-Sánchez et al. 1999; Bobylev 2010; Bailer-Jones 2022's summary quote |
| 9 | Gaia has measured more than a billion stars | DR3: about 1.8 billion sources | ESA Gaia DR3 |
| 10 | The latest Gaia measurements put closest approach at about a fifth of a light-year, about 10,000–13,000 times the Earth–Sun distance, five times closer than the old estimate | 0.051–0.0636 pc = 0.17–0.21 ly = 10,500–13,100 AU. Five times: about 1 ly ÷ 0.2 ly, or 0.31 pc ÷ 0.064 pc ≈ 4.9 | Bailer-Jones 2022; de la Fuente Marcos 2022 |
| 11 | Scale model: the Earth–Sun gap is 1 cm, Neptune at 30 cm, the star over 100 m away, a football pitch | 1 AU = 1 cm; 10,500–13,100 AU = 105–131 m; a pitch is about 100–110 m | Arithmetic |
| 12 | The Oort Cloud: trillions of icy bodies left over from planet formation; never seen directly; known from the comets that fall out of it | NASA: "billions, or even trillions" | NASA Oort Cloud facts; Oort 1950 |
| 13 | Inner edge a few thousand times further out than Earth; outer edge maybe 100,000. Sunlight takes eight minutes to reach us and months to reach the pass. **MUST QUOTE**: confirm "months" (about 60–75 days at 10,500–13,100 AU) | 2,000–5,000 AU; 10,000–100,000 AU; 499 s per AU | NASA Oort Cloud facts |
| 14 | Planets not affected | <40 AU region not significantly affected | de la Fuente Marcos 2018 RNAAS 2 30 |
| 15 | About ten extra comets a year falling in close enough to see, for three to four million years. "Close enough to see": check what "observable" means in the paper (perihelion < 5 AU?). **MUST QUOTE** | ~10 per year, 3–4 Myr | Berski & Dybczyński 2016 |
| 16 | The comets fall in hundreds of thousands of years later, so the shower peaks after the star has gone | Half an orbit. Claude's own numbers: a comet nudged at aphelion Q = 13,000 AU has a ≈ 6,500 AU, P ≈ 0.52 Myr, fall time ≈ 0.26 Myr; from Q = 30,000 AU, fall time ≈ 0.9 Myr. SOURCES' "0.5–1 Myr" took a = 10,000 AU (aphelion ~20,000 AU), so the script says "hundreds of thousands of years" to cover both. Gemini: confirm, or cite a paper that gives the shower's time profile | Kepler III; a paper on the time profile if there is one (Dybczyński 2002?) |
| 17 | Jupiter and Saturn throw many back out or steer them away; models find only a small rise in the chance of an impact on Earth. **No number is spoken.** Gemini: give the exact quote and figure from García-Sánchez 2001 so it can go in the description | "≤5%" (paraphrase in SOURCES) | García-Sánchez et al. 2001 A&A 379 634 |
| 18 | At closest it's the brightest star in the sky, about three times Sirius, as bright as Jupiter at its best, and orange | −2.7 vs Sirius −1.46 → 3.1×; Jupiter up to −2.9 | Berski & Dybczyński 2016 |
| 19 | Still billions of times fainter than the Sun | Δm = 24 → about 4 × 10⁹ | Sun V = −26.74 |
| 20 | It moves across the sky by about a full Moon's width every 35 years | 52.28″/yr; Moon about 1,865″ → 36 yr | Berski & Dybczyński 2016 (proper motion at closest) |
| 21 | Scholz's star, a dim red pair, passed through the outer Oort Cloud less than a light-year away, about 70,000 years ago | 52 kAU = 0.25 pc = 0.82 ly; 70 kya; 0.15 M☉ binary | Mamajek et al. 2015 |
| 22 | HD 7977, a star much like the Sun, may have passed as close as Gliese 710 will, about 2.8 Myr ago; Gaia can't yet pin it down | G3 dwarf; median 0.0641 pc, 90% CI 0.019–0.117 pc | Bailer-Jones 2022 |
| 23 | Every few million years a star brushes past | Rate of encounters within about 0.1 pc | Bailer-Jones 2022 or 2018 (encounter rate); Gemini: give the figure |
| 24 | Some astronomers think the Sun was born among sister stars, and many Oort Cloud comets were once theirs | Capture from the birth cluster, possibly most of the cloud | Levison, Duncan, Brasser & Kaufmann 2010, Science 329, 187 |

**Tone lock:**
- Wonder, not fear. No impact or disaster imagery.
- Comet effects are given as probabilities, not predictions.
- No product names and no `/go/` link.
- Use 026 (Proxima) as a one-line callback only.
