# Research Notes & Brief Audit (`RESEARCH_NOTES.md`) — `WW2:002`

- **Film:** `WW2:002` — *How the Allies Closed the U-Boats' Safest Hunting Ground*
- **Purpose:** Documents every verification check, correction, removal, and softening applied to the draft project briefs (`TOPIC.md`, `PILOT_PLAN.md`, and `00_Brand/LAUNCH_PLAN.md`) based on live primary and official source inspection (`SOURCES.md` `S1`–`S9`).
- **Epistemic hygiene:** No quotations, archival call-number contents, or licence claims are invented. Offline UK National Archives (`TNA ADM 199/2020`, `AIR 41/47`, `ADM 234/578`) and unindexed physical files listed in `PILOT_PLAN.md` were **not** accessed first-hand in this session and are therefore **not** cited as read sources in `SOURCES.md`. All claims in `SCRIPT_v01.md` rest on published official histories and declassified US Navy operational evaluations actually read online at `ibiblio.org/hyperwar` and `history.navy.mil`.

---

## 1. Itemised Audit of Suspect Figures & Conflations in the Brief

### A. Unverified `"600-Mile"` Mid-Atlantic Air Gap Figure & Fabricated Thumbnail Concept
- **What the brief said (`TOPIC.md`, `PILOT_PLAN.md`, `LAUNCH_PLAN.md`):**
  - Described the Mid-Atlantic Air Gap ("the Black Pit") as a fixed `"600-mile"` stretch or oval south of Greenland.
  - Proposed a thumbnail with cover text `"600-MILE DEAD ZONE"` over a composite/uninspected scene (`"white-camouflaged B-24 Liberator banking low over a surfaced U-boat"`).
- **What live official sources show:**
  - `00_Brand/PLAYBOOK.md` (§3, 17 Nov 2026) already flagged that `"the '600-mile' figure could not be confirmed"`.
  - Captain S. W. Roskill, *The War at Sea 1939–1945, Vol. II*, Chapter VIII (`S2`, `UK-RN-II-8.html`), gives the actual operational radii from shore bases: `"The normal range of air cover was still only about 450 miles from the shore bases"`, while `"in exceptional circumstances temporary air cover could be given at a distance of 800 miles from our bases"` by `No. 120 Squadron` VLR Liberators.
  - US Navy OEG Report No. 51 (`S4`, `ASW-51-5.html`) states that when Convoys `HX 229` and `SC 122` lost 13 ships on the night of 16–17 March 1943, `"the convoys were about 850 miles from the nearest air bases."`
  - Because Great Circle convoy tracks shifted north and south with weather, pack ice, and evasive routing, the width of the unpatrolled gap varied continuously rather than sitting at a fixed 600-mile dimension.
- **Correction applied:**
  - Removed `"600-mile"` completely from `PACKAGING_v01.md`, `SCRIPT_v01.md` (`[P17]`–`[P18]`), and `SHOT_LIST_v01.csv`.
  - Replaced the uninspected composite thumbnail concept with two real, unmodified, inspected US federal public-domain (`NARA 80-G`) photographs (`80-G-68713` and `80-G-407707`).

---

### B. Conflation of March 1943 Worldwide Tonnage (`627,000 Tons`) with Convoys `HX 229` & `SC 122` (`141,000 Tons`)
- **What the brief said (`TOPIC.md` & `LAUNCH_PLAN.md`):**
  - *"In March 1943 (Convoys HX 229 & SC 122), U-boats sank 627,000 tons of shipping by hunting inside the 600-mile Mid-Atlantic Air Gap"*; `PILOT_PLAN.md` also cited `"22 merchantmen, 146,000 tons sunk for 1 U-boat lost"` in `HX 229` & `SC 122` and claimed the Allies came `"within four days of abandoning the North Atlantic convoy system"`.
- **What live official sources show:**
  - **Worldwide March 1943 total vs convoy total:** Roskill Vol. II, Chapter XIV & Table 31 (`S1`, `UK-RN-II-14.html`) records that across **all ocean theatres** in March 1943, U-boats sank **`108` ships of `627,377` tons** (`83` ships of `487,034` tons in convoy and `25` ships of `140,343` tons independently sailed; `120` ships of `~693,000` tons from all enemy causes). US Navy OEG Report No. 51 (`S4`, `ASW-51-5.html`) similarly states: `"In March 1943 the world-wide shipping losses to U-boats mounted to 107 ships of 627,000 gross tons."`
  - **Convoys `HX 229` and `SC 122` specifically:** Roskill (`S1`, `UK-RN-II-14.html`) states: `"In fact we lost only twenty-one, but their tonnage was no less than 141,000; and only one U-boat was lost by the enemy in the course of all these attacks"` (OEG Report No. 51 `S4` counts `20` ships lost in the two convoys, with `13` sunk on the night of 16–17 March). (A 22nd ship / ~146,000-ton figure in some secondary accounts includes an independent/straggler outside the official Roskill convoy tally.)
  - **Admiralty assessment of the convoy system:** There was no `"four-day"` countdown to abandon convoys. Rather, Roskill (`S1`) quotes two specific retrospective Naval Staff statements: (1) `'the Germans never came so near to disrupting communication between the New World and the Old as in the first twenty days of March 1943'`, and (2) `'It appeared possible' wrote the Naval Staff after the crisis had passed, 'that we should not be able to continue [to regard] convoy as an effective system of defence'.`
- **Correction applied:**
  - Explicitly separated the `HX 229` / `SC 122` losses (`21` merchantmen of `141,000 tons` for `1` U-boat lost, `[P01]`) from the worldwide March 1943 U-boat total (`108` ships of `627,377 tons` across all ocean theatres, of which `83` ships of `487,034 tons` were in convoy, `[P03]`–`[P04]`).
  - Replaced the unsupported `"four days from abandoning"` phrasing with the exact Naval Staff retrospective judgements (`[P02]`, `[P05]`).

---

### C. VLR Liberator Ferry Range (`2,000–2,500 Miles`) vs Operational Patrol Radius (`~800 Miles`) & Exact Airframe Counts
- **What the brief said (`TOPIC.md`, `PILOT_PLAN.md`):**
  - Referred to `"fewer than 40 modified 2,400-mile VLR B-24 Liberators"`, treating total range as if it were patrol reach from base and blurring February/March strength with May strength.
- **What live official sources show:**
  - **Endurance range vs operational radius:** OEG Report No. 51 (`S4`, `ASW-51-5.html`) states that VLR aircraft had `"an endurance of 2000 to 2500 miles"`. Because an aircraft had to fly out against Atlantic headwinds, patrol around a convoy for two to three hours, and return with fuel reserves, Roskill (`S2`, `UK-RN-II-8.html`) states that VLR Liberators could provide temporary air cover `"at a distance of 800 miles from our bases"`, compared with `"about 450 miles"` for normal shore-based maritime aircraft.
  - **Exact airframe counts:** In **February 1943**, Roskill's **Table 29** (`S1`, `UK-RN-II-14.html`) shows that out of `820` maritime patrol aircraft across all Eastern and Western Atlantic convoy sectors, the grand total of operational **VLR aircraft was `18`** (`9` in Iceland, `9` in No. 15 Group in Northern Ireland, all in `No. 120 Squadron RAF`, and `0` in Greenland, Newfoundland/Canada, Bermuda, and the US East Coast; OEG Report 51 says `"about 20"`). At the Washington Atlantic Convoy Conference (`1 March 1943`), the Allies agreed to transfer `20` Liberators from the British allocation to the RCAF (`S1`). By **May 1943**, Roskill (`S1`) records that `"the number of V.L.R. aircraft had risen to over thirty."`
- **Correction applied:**
  - Clearly distinguished still-air endurance (`2,000 to 2,500 miles`) from operational patrol radius (`about 800 miles` vs `450 miles` normal radius) in `[P17]`–`[P21]`.
  - Gave the exact February 1943 Table 29 breakdown (`18` VLR aircraft out of `820` maritime aircraft: `9` Iceland, `9` Northern Ireland, `0` western Atlantic, `[P24]`–`[P25]`) and the growth to `"over 30"` (`fewer than 40`) by May 1943 (`[P28]`).

---

### D. Air-Cover Deterrence (Forcing Submergence) vs Direct Aircraft Sinkings, and Escort vs U-Boat Speeds
- **What the brief said (`PILOT_PLAN.md`):**
  - Mentioned U-boats surfacing in broad daylight to `"outrun 16-knot corvettes"` and treated VLR aircraft around convoys primarily as direct U-boat killers.
- **What live official sources show:**
  - **Speeds:** Roskill Vol. I (`S3`, `UK-RN-I-8.html`) confirms that `865-ton` Flower-class corvettes had a `"Maximum speed 16 knots"` and `"insufficient speed to overtake a U-boat retiring on the surface"`. A Type VIIC U-boat made `~17 knots` (`17–17.7 knots`) surfaced on diesels, but only `~7.5 knots` (`7.4–7.6 knots`) maximum submerged for under an hour and `2 to 4 knots` economical underwater speed (`S2` Appendix K), slower than a `7 to 10 knot` merchant convoy (`S5`).
  - **Deterrence vs sinkings:** OEG Report No. 51, Chapter 10 (`S5`, `ASW-51-10.html`), establishes that `"the primary effect of aircraft flying is to reduce the speed of convoy for which the submarine can carry out Method B tracking and approach, because it is forced to submerge at least part of the time."` Even when an aircraft did not sink a U-boat (as in `NARA 80-G-68710` / `80-G-68713`, where a *Bogue* Avenger forced `U-603` to dive on 4 June 1943 and saved a nearby convoy), forcing the boat underwater neutralized its ability to overtake the convoy. Roskill (`S1`, `UK-RN-II-14.html`) confirms that across the entire January–May 1943 phase, `"only two ships were sunk in convoy in the Atlantic while an air anti-submarine escort was present; and not one of the ships lost from the convoys shown in Table 32 (pp. 380–382) fell victim to a U-boat while her convoy was receiving air protection."`
- **Correction applied:**
  - Made the distinction between air-cover deterrence (forcing submergence to defeat wolfpack surface mobility) and lethal attacks a central analytical theme in `[P09]`–`[P15]` and `[P59]`.

---

### E. Convoy `ONS 5` (`29 April – 6 May 1943`) Command, Aircraft Role, and Submarine Losses
- **What the brief said (`PILOT_PLAN.md`):**
  - *"radar-guided escorts (HMS Duncan, HMS Vidette, Hedgehog forward-throwing mortars) plus VLR Liberators destroy 7 U-boats in zero-visibility fog."*
- **What live official sources show (`S1` `UK-RN-II-14.html`, `S4` `ASW-51-5.html`, `S7` `UK-RAF-III-2.html`):**
  1. **`HMS Duncan` was not present during the night fog battle of 5–6 May 1943:** Although Commander P. W. Gretton in `HMS Duncan` led Escort Group B7 when U-boats contacted `ONS 5` on 29 April (`500 miles east of Cape Farewell`), heavy gales exhausted fuel reserves. On `3 May`, `"the Duncan had to make for St. John's, and command of the escort devolved on the frigate Tay (Lieutenant-Commander R. E. Sherwood, R.N.R.)"` (`S1`).
  2. **VLR Liberators did NOT sink any of the 7 U-boats around `ONS 5`, nor did aircraft sink U-boats in the fog:**
     - The `7` U-boats destroyed across the `ONS 5` passage in Roskill (`S1`) were:
       - `U-710` early in the passage south of Iceland by an RAF Coastal Command **Flying Fortress** (not a VLR Liberator);
       - `U-630` on `4 May` by a Royal Canadian Air Force **Canso** (amphibious Catalina) of **No. 5 Squadron RCAF** from Newfoundland (not a VLR Liberator);
       - `U-192` in daylight on `5 May` by the Flower-class corvette **`HMS Pink`** guarding stragglers;
       - `U-638` on the night of `5–6 May` by the corvette **`HMS Loosestrife`** with depth charges;
       - `U-125` in the small hours of `6 May` by the destroyer **`HMS Vidette`** with her **`Hedgehog`** ahead-throwing mortar;
       - `U-531` in the fog on `6 May`, rammed and sunk by the destroyer **`HMS Oribi`**;
       - `U-438` at about `4 a.m. on 6 May` by the sloop **`HMS Pelican`** (leading the reinforcing 1st Escort Group) with depth charges after running down a radar echo.
     - *(Note on postwar hull-number cross-reassessments: While Roskill 1956 records the wartime/1956 Admiralty hull attributions above—`Pink`/`U-192`, `Loosestrife`/`U-638`, `Vidette`/`U-125`, `Oribi`/`U-531`, `Pelican`/`U-438`—later postwar German-British wreck cross-checks swapped several hull numbers among those exact same five escort attacks on 5–6 May, e.g. crediting `Loosestrife` with `U-192`, `Pink` with `U-638` or `U-531`, `Vidette`'s Hedgehog with `U-531` or `U-638`, and `Oribi` & `Snowflake` with `U-125`. In both the 1956 official history and modern reassessments, the five surface-escort kills on 5–6 May plus the 4 May RCAF Canso kill and the earlier RAF Fortress kill total seven U-boats across the operation, and zero were sunk by VLR Liberators in fog.)*
  3. **Where `No. 120 Squadron` VLR Liberators and Gretton's `HMS Duncan` scored their joint victory:** Days later around **`Convoy SC 130` (`11–25 May 1943`)**, where Gretton was back in `HMS Duncan`, `No. 120 Squadron` VLR Liberators (`"P for Peter"` sighting `8` U-boats in one sortie) sank `U-954` and `U-258`, a `No. 269 Squadron` Hudson sank `U-273`, escorts `Jed`, `Sennen`, and `Duncan` disposed of `U-209` and `U-381`, and all `38` merchant ships arrived without loss (`S1`, `S7`).
- **Correction applied:**
  - Accurately narrated both `ONS 5` (`[P41]`–`[P50]`, crediting Sherwood in `HMS Tay`, the RCAF No. 5 Squadron Canso, and the five surface escorts `Pink`, `Loosestrife`, `Vidette`, `Oribi`, and `Pelican`) and `SC 130` (`[P51]`–`[P52]`, crediting Gretton back in `HMS Duncan` and `No. 120 Squadron` VLR Liberators).

---

### F. May 1943 U-Boat Loss Totals (`41` vs `43` vs `44`), Percentages, and "Permanent" Closure
- **What the brief said (`TOPIC.md`, `PILOT_PLAN.md`):**
  - Stated that Dönitz lost `"43 U-boats (25% of his operational crews)"` in May 1943 and that escort carriers and Support Groups closed the gap `"permanently"`.
- **What live official sources show:**
  - **Monthly U-boat loss count:** British official histories (`S1` Roskill Vol. II Ch. XIV & Table 31; `S7` Saunders RAF Vol. III Ch. II) record **`41` U-boats sunk** in May 1943 (`33` lost by 22 May when the decision to withdraw was made, and `28` lost around mid-Atlantic convoys). The 1946 US Navy OEG Report No. 51 (`S4`, `ASW-51-5.html`) recorded a wartime assessment of **`44` U-boats sunk worldwide** in May 1943, with **`38` in the Atlantic** (`15` in the Northwest Atlantic Area and `11` in the Bay of Biscay), noting that `"Shore-based aircraft accounted for over half the U-boats sunk during the month"`.
  - **Percentage / force proportion:** OEG Report No. 51 (`S4`) states that `"The number of U-boats at sea in the Atlantic reached a peak of about 120"` and dropped to `"about 85"` by the end of May. Thus the May losses (`38–41` boats in the Atlantic/overall) represented **roughly one-third of the ~120 U-boats at sea in the Atlantic** (rather than an unqualified `"25%"`).
  - **Temporary withdrawal vs permanent strategic effect:** Dönitz ordered the withdrawal on 23–24 May 1943 as a temporary measure while awaiting `Naxos` 10-cm radar detectors, heavier anti-aircraft guns, and acoustic torpedoes (`S4`, `S5`, `S7`). However, because VLR aircraft and escort carriers maintained continuous patrols from June 1943 onward (`S7`) and Allied aircraft began operating from the Azores in October 1943, the autumn 1943 U-boat comeback failed (`S4`, `S8`).
- **Correction applied:**
  - Stated both the postwar British official figure (`41` U-boats sunk in May, `28` around mid-Atlantic convoys, `33` by 22 May) and the wartime US Navy OEG assessment (`38` in the Atlantic, `44` worldwide), related that toll to the verified `~120` U-boats at sea in the Atlantic (`[P54]`–`[P55]`), and explained why a withdrawal intended by Dönitz to be temporary became permanent in strategic outcome (`[P57]`–`[P58]`).
