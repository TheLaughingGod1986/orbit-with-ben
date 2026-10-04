# Sources — Could a Robot Survive on Mars?

Spoken claims for the description and script draft. Not narration. Neighbour packaging lives in `NEIGHBOURS_2026-10-04.md` (subject words only in public listing — never channel names).

| Claim in the film | Source |
|---|---|
| Mars surface pressure averages ~6.36 mbar (~0.6% of Earth's ~1013 mbar), varying ~4.0–8.7 mbar by season | NASA NSSDCA Mars Fact Sheet: "Surface pressure: 6.36 mb at mean radius (variable from 4.0 to 8.7 mb depending on season)." Ratio vs Earth ≈ 0.006. https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html |
| Average surface temperature about −59 °C (~214 K); Viking 1 diurnal range about −89 to −31 °C | Same NASA Mars Fact Sheet: "Average temperature: ~214 K (−59 C)"; "Diurnal temperature range: 184 K to 242 K (−89 to −31 C) (Viking 1 Lander site)." https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html |
| Curiosity's RAD measured surface GCR dose equivalent ≈ 0.64 ± 0.12 mSv/day (~230 mSv/year near solar maximum) | Hassler, D. M. et al. (2014). "Mars' Surface Radiation Environment Measured with the Mars Science Laboratory's Curiosity Rover." *Science*, 343(6169), 1244797. DOI [10.1126/science.1244797](https://doi.org/10.1126/science.1244797). Reported average GCR dose-equivalent rate on the surface: $0.64 \pm 0.12\,\mathrm{mSv/day}$ (absorbed dose $0.210 \pm 0.040\,\mathrm{mGy/day}$). |
| Dust storms range from local dust devils to planet-encircling events that can blanket the globe for weeks | NASA Opportunity end-of-mission release describes the 2018 Mars-wide dust storm that stopped solar-powered ops. Broader context: planet-encircling dust activity is a recurring Mars climate feature (Zurek & Martin 1993, *JGR* 98, 3247; DOI [10.1029/92JE02936](https://doi.org/10.1029/92JE02936)). |
| Spirit became stuck in soft sand at "Troy" (May 2009) with a failed wheel; last contact 22 March 2010 as winter cut solar power | NASA/JPL: Spirit embedded in soft soil at Troy; last communication 22 March 2010; recovery ended May 2011. https://www.jpl.nasa.gov/news/nasas-spirit-rover-completes-mission-on-mars/ · End-of-mission report: [NTRS 20160001767](https://ntrs.nasa.gov/citations/20160001767) · Mission summary: https://science.nasa.gov/mission/mer-spirit/ |
| Opportunity's last contact was 10 June 2018 when a planet-wide dust storm blocked sunlight; mission ended 13 Feb 2019 after 1,000+ recovery commands | NASA: "The Opportunity rover stopped communicating with Earth when a severe Mars-wide dust storm blanketed its location in June 2018… The solar-powered rover's final communication was received June 10." https://www.nasa.gov/news-release/nasas-record-setting-opportunity-rover-mission-on-mars-comes-to-end/ |
| Curiosity's thin aluminium wheels (~0.75 mm skin) developed punctures, tears, and broken grousers from sharp embedded rocks | NASA LLIS lesson 22401 (MSL wheel damage): puncture first noted sol 411 (2 Oct 2013); progressive tears from ventifacts / metal fatigue. https://llis.nasa.gov/lesson/22401 · Grouser breaks / monitoring: https://science.nasa.gov/resource/break-in-raised-tread-on-curiosity-wheel/ · Assessment paper: Rankin et al., [NTRS 20230005728](https://ntrs.nasa.gov/citations/20230005728) |
| Ingenuity completed 72 flights over almost three years; Flight 72 (18 Jan 2024) damaged rotor blade(s) on landing and ended flight ops | NASA: "Originally designed… up to five experimental test flights over 30 days… performed 72 flights… Imagery… indicates one or more of its rotor blades sustained damage during landing and it is no longer capable of flight." https://www.nasa.gov/news-release/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ · Accident investigation follow-up: https://www.nasa.gov/missions/mars-2020-perseverance/ingenuity-helicopter/nasa-performs-first-aircraft-accident-investigation-on-another-world/ |
| The 2018 global dust storm (MY 34) darkened Opportunity's skies and dropped solar power until contact was lost | Same NASA Opportunity release (above). MSL/Curiosity also observed the storm from Gale: Guzewich, S. D. et al. (2019). "Mars Science Laboratory Observations of the 2018/Mars Year 34 Global Dust Storm." *Geophys. Res. Lett.*, 46, 71–79. DOI [10.1029/2018GL080839](https://doi.org/10.1029/2018GL080839). |
| Radioisotope-powered Curiosity kept working through the 2018 dust storm; solar-powered Opportunity could not | Contrast implied by Opportunity solar failure (NASA release above) vs Curiosity MMRTG continuous power (~110 W electric at launch class). Curiosity power system overview: https://mars.nasa.gov/msl/spacecraft/rover/power/ |

No product is named. No `/go/` link.

**Science lock reminder:** Robots have survived years on Mars despite dust, cold, and radiation; failures are usually power/dust or mechanical wear, not instant "death." Keep wonder, not fearbait.

## Notes for Claude (Gemini draft, 4 Oct 2026)

- Core five topic bullets covered with NASA / peer-reviewed links. Prefer nasa.gov over jpl.nasa.gov mirrors when bots get 403s.
- Pressure "≈0.6% of Earth" is the fact-sheet ratio (6.36/1013 ≈ 0.63%); film may say "less than one percent."
- **UNVERIFIED / soft:** Exact Opportunity Wh numbers (e.g. 645 → 22 Wh) and tau = 10.8 were in an earlier draft but not re-confirmed from a primary status log in this pass — do not speak them until Claude locks a status page quote.
- Ingenuity: NASA wording is "one or more" blades; later investigation covers tip damage — safe spoken forms: "blade damage" / "damaged rotor blades."
- PARKED FOR CLAUDE: script/VO lock for 025; any spoken Wh/tau figures.


## Added by Claude for script v01 (4 Oct). Gemini: verify each row and add the exact quote

| Claim in the film | Source to check |
|---|---|
| Spirit and Opportunity were each designed for a 90-sol mission; Opportunity operated from January 2004 to June 2018 ("more than fourteen years") | NASA Opportunity end-of-mission release (above); NASA MER mission pages |
| Wind and dust devils repeatedly cleaned the rovers' solar panels ("cleaning events") | NASA/JPL MER news releases on cleaning events (e.g. Spirit 2005, Opportunity 2014) |
| One-way radio time between Earth and Mars is about 3 to 22 minutes | NASA Mars mission pages ("communications delay"); compute from 0.37–2.67 AU |
| Phoenix landed May 2008, went silent Nov 2008; MRO HiRISE imaging in 2010 showed solar-panel damage, likely from CO₂ ice | NASA/JPL release, 24 May 2010 ("Phoenix Mars Lander Is Silent, New Image Shows Damage") |
| InSight detected more than 1,300 marsquakes; dust on its panels ended the mission in December 2022 | NASA release, 21 Dec 2022 (InSight mission ends) |
| Earth natural background dose about 2.4 mSv/year, so 0.64 mSv/day on Mars ≈ three months on Earth | UNSCEAR 2008 report (worldwide average natural exposure 2.4 mSv/yr) |
| Ingenuity flew in air about 1% as dense as Earth's at sea level; its rotors spun at about 2,400–2,700 rpm | NASA Ingenuity fact sheet / JPL Ingenuity pages |
| Curiosity (landed August 2012) is still operating in Oct 2026 | NASA Curiosity mission status page. **Check before VO.** The film only says it kept working through 2018 |
| Landers are slowed from thousands of km/h before touchdown | NASA Mars 2020 EDL facts (entry at about 20,000 km/h) |
