# 030: Claude's quote check before lock (J0227, 14 Oct 2026)

I checked every MUST QUOTE row of `SOURCES.md` against the live pages themselves, fetched today, not against Gemini's quotes. Script: `apophis_script_master_v02.md`. It has the three line fixes below. `review:script` gives PASS 94.5, the same as v01.

| Row | Claim | Result | Source checked |
|---|---|---|---|
| 1 | about 340 m, about the height of the Eiffel Tower | ✓ "mean diameter of 1,115 feet (340 meters)… about the height of the Eiffel Tower". ESA now says "Roughly 375 m across"; the film follows NASA | NASA Apophis Facts; ESA Apophis |
| 2 | Fri 13 Apr 2029, about 32,000 km from the surface | ✓ "less than 20,000 miles (32,000 kilometers) from our planet's surface" | JPL 25 Mar 2021 release; JPL radar page |
| 3 | geostationary ring at about 36,000 km | ✓ "an altitude of 35 786 km" | ESA *Types of orbits* |
| 4 | roughly a tenth of the way to the Moon | ✓ "384,400 kilometers"; "within 0.1 lunar distances" | NASA Moon facts; JPL radar page |
| 5 | June 2004, Kitt Peak, Tucker, Tholen, Bernardi, two nights | ✓ "discovered on 19 June 2004 by Roy Tucker, David Tholen and Fabrizio Bernardi… from Kitt Peak, Arizona, and observed over two nights" | CNEOS news 146 |
| 6 | found again in December from Australia | ✓ "On 18 December, the object was rediscovered from Australia" | CNEOS news 146 |
| 7 | 1 in 37 **"by Christmas"** | ✗ **The date is wrong.** On 24 Dec CNEOS gave "about 1.6%" (about 1 in 60). The 2.7% sources (CNEOS 164: "Initially… 2.7 percent"; ESA: "rose as high as 2.7%") give no date. **Line 18 is now "At its peak it reaches about one in thirty-seven."** | CNEOS 146, 164; ESA Apophis |
| 8 | Torino 4, highest ever; ≥1% chance of regional devastation | ✓ The claim holds. ✗ **Gemini's quote merged levels 4 and 5:** "posing a serious, but still uncertain threat" is level 5's text. Level 4 on the page reads "A close encounter, meriting attention by astronomers. Current calculations give a 1% or greater chance of collision capable of regional devastation." Quote fixed in SOURCES | CNEOS Torino scale page; ESA ("highest ever rating") |
| 10 | March 2004 precovery images; 2029 ruled out within days | ✓ "archival images dating to 15 March 2004… an Earth impact on 13 April 2029 can now be ruled out" (27 Dec 2004) | CNEOS news 148 |
| 11 | March 2021 radar, Goldstone + Green Bank, nothing for 100 years | ✓ "don't show any impact risk for at least the next 100 years"; the flyby was "around March 5" | JPL 25 Mar 2021 release |
| 13 | naked eye from Britain, Europe, Africa; as bright as Megrez | ✓ on the real quote. ✗ **"visual magnitude 3.1" is not on the page** (Cursor was right). The page says "visible in the night sky to the naked eye at about 3rd-4th magnitude for several hours at closest approach for observers in western Europe and Africa". Megrez is V 3.32, which falls in that range, so line 56 stays. **No card may say 3.1.** TEACH note fixed | JPL radar page; ESA Apophis; SIMBAD |
| 14 | every few thousand years on average | ✓ "only every few thousand years on average" | NASA Apophis Facts |
| 15 | orbit a little under a year → a little over | ✓ "about 0.9 years" → "about 1.2 years" | NASA Apophis Facts |
| 17 | Bennu sample 24 Sept 2023; OSIRIS-APEX ~18 months; thrusters | ✓ "Sunday, Sept. 24, 2023"; "for about the next 18 months"; "firing its thrusters downward" | NASA release 23-109; NASA OSIRIS-APEX article |
| 20 | Chelyabinsk 2013, about 20 m, **"around fifteen hundred" hurt** | ✗ **The number is wrong.** NASA: "injured over 1,600 people – mostly due to broken glass". **Line 87 is now "more than sixteen hundred people were hurt".** 20 m ✓ (Popova et al. 2013). Not seen coming ✓ ("not detected prior to impact") | NASA Planetary Defense blog, 15 Feb 2023 |
| 21 | DART, 26 Sept 2022, 32 minutes shorter | ✓ "altered Dimorphos' orbit around Didymos by 32 minutes, shortening the 11 hour and 55-minute orbit to 11 hours and 23 minutes" | NASA release 22-105 (11 Oct 2022) |
| 22 | Rubin has begun; NEO Surveyor due in 2027 | ✓ "has begun the revolutionary Legacy Survey of Space and Time"; "scheduled for launch no earlier than September 2027" | Rubin release; NASA NEO Surveyor page |
| 24 | WHO years on cards | Tucker (1951–2021) ✓ on NASA Apophis Facts. Tholen 1955: the Library of Congress page refused my fetch (403), so it rests on Gemini's quote. Check it again before the card is made. Bernardi 1972: MPC citation (Gemini) | NASA Apophis Facts |
| 25 | 1 in 37 ≈ a double six (1 in 36) | ✓ arithmetic: 2.70% vs 2.78% | — |
| 26 | about 7 km/s | ✓ JPL close-approach API: v_rel 7.4225, v_inf 5.8414 km/s (2029-Apr-13 21:46). The Wikipedia line in the row is secondary and isn't needed | ssd-api.jpl.nasa.gov `cad.api?des=99942` |
| 27 | crosses Britain in about two minutes | ✓ great circle Land's End–John o' Groats 968 km; 968 / 7.42 = 130 s | arithmetic (haversine) |
| 28 | closest pass of an asteroid this big anyone has known about | ✓ with a wording fix. NASA: "the closest approach to Earth by an asteroid of this size that scientists have known about **in advance**". Line 58 now ends "…that anyone has ever known about in advance." | NASA Apophis Facts; JPL radar page |

## Spoken numbers not covered by a row

- **"Billions of people will have the chance to see it"** (v01 line 58): no page gives a number of people, so the sentence is **cut**. Gemini said row 13 covered it, but row 13 only names regions.
- "No asteroid had ever scored that high before. None has since." ESA's current page says "the highest ever rating", so this holds.
- Everything else in Gemini's list holds: "twenty years ago", "three astronomers", "fifteen times wider" (340 / 20 = 17), "millions of years", "twenty-five years early" and "Friday night in April".

## Lock

Script **v02 is locked for Chief** (J0227). No spend. Chief: the VO can be cast from v02 once you PASS it.
