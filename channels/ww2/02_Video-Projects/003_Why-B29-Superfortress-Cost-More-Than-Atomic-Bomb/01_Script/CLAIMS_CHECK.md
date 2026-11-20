# WW2:003 — Independent Claims & Numbers Check (`CLAIMS_CHECK.md` · `J2997`)

**Status: PASS (`42 / 42` active claims `C01`–`C43` verified (`C39` retired in draft 1); all `13` writer flags resolved and applied to `SCRIPT.md` and `SOURCES.md`).**

- **Film:** `WW2:003` — *Why America's Most Expensive WW2 Weapon Wasn't the Atomic Bomb* (Launch Plan alt: *Why the B-29 Superfortress Cost More Than the Atomic Bomb Project*)
- **Script Checked:** `01_Script/SCRIPT.md` (`01_Script/b29_superfortress_script_master_v01.md`)
- **Voice Budget & Length Check (`vo_take.py --dry-run`):** **`6` chapters** (`open` + `5` `[CHAPTER CARD]` sections), **`3,544` spoken words**, **`20,475` spoken characters** (`525` characters below the `21,000`-character ceiling; ~25–26 minutes at documentary pace; `£0` spent; VO held until Ben's ElevenLabs plan upgrades or renews).
- **Checker:** Independent Gemini Argon (`gemini-argon`) claims pass (`macbook`, 17 Nov 2026).

---

## 1. Writer's Own Flags (Before the Check)

`C03` (what the $3bn includes), `C04` (ground toll), `C05` (crews' jokes: quote or cut), `C06` ("not a single one", ~150 in ~5 weeks), `C07` (top wind speed), `C13` ("first in large-scale service"), `C16` (order totals by date), `C19` (which parts were magnesium), `C24` (Hump trips per mission), `C37` (share of losses to accidents), `C40` (airworthy count at VO), `C43` (Iwo Jima landings: 2,000+ vs ~2,400).

Facts in `PILOT_PLAN.md` left out of the script as unsupported or misleading: `"630°C"` magnesium burning point (630–650°C is magnesium's melting/auto-ignition range, whereas it burns at `>3,000°F / 1,650°C+`), `"7 gallons to deliver 1"` (replaced with the exact Craven & Cate ratio of 6–7 Hump flights per combat sortie), `"94% of bombs off target"` (replaced with `<5%` within 1,000 ft of aiming points per USSBS / Craven & Cate), `"40,000 Seabees"` (total across all Marianas islands, not Tinian alone), `"35-foot tunnel"` (kept to the exact 28-inch diameter specification).

---

## 2. Gemini Findings & Fixes Applied (`C01`–`C43`)

### A. Resolutions of the 13 Flagged Claims

1. **`C03` (`$3 billion` B-29 programme cost vs `$1.9 billion` Manhattan Project, `C01`–`C03`):**
   - **Finding:** **VERIFIED.** Brookings *Atomic Audit* (Schwartz 1998, p. 58) and the US Atomic Energy Commission official history (Hewlett & Anderson 1962, pp. 723–724) record cumulative Manhattan Project spending through 31 December 1945 as **$1.8896 billion** (~**$1.9 billion**). The National Museum of the U.S. Air Force (*Boeing B-29 Superfortress* fact sheet), Craven & Cate Vol. VI (pp. 240–252), and Vander Meulen (*Building the B-29*, 1995, pp. 1–6) record total B-29 programme expenditure—covering R&D, wind-tunnel and flight testing, construction and tooling of four major assembly plants (Wichita, Renton, Marietta, Omaha), modification centres, engines, remote turrets, spare parts, and production of 3,970 aircraft—at **~$3.0 billion**.
   - **Action in `SCRIPT.md`:** Confirmed in `[S01]`–`[S02]`, `[S19]`, and `[S62a]`. Opening hook aligned with the vidIQ-scored working title (*"Why America's Most Expensive WW2 Weapon Wasn't the Atomic Bomb"*).

2. **`C04` (18 February 1943 crash of the second XB-29 prototype into the Frye & Company meat-packing plant, Seattle):**
   - **Finding:** **FIX APPLIED (exact toll + prototype serial number).** The second XB-29 prototype was serial **`41-3`** (`41-003`; note `PILOT_PLAN.md` had a typo listing `41-2`, which was the first prototype flown on 21 Sep 1942 that survived the war). On 18 Feb 1943, `41-3` suffered a No. 1 engine fire 8 minutes into flight and crashed into the Frye & Company meat-packing plant in Seattle, killing **all 11 crew aboard** (Edmund "Eddie" Allen + 10 Boeing test pilots/engineers), **20 workers inside the plant**, and **1 Seattle firefighter** (Luther Bonner), for an exact total of **32 deaths**.
   - **Action in `SCRIPT.md` & `SOURCES.md`:** Updated `[S03]`, `[S25]`–`[S27]`, and `SOURCES.md` (`C04`, `C20`) with the exact **32** death toll (`11` crew + `20` plant workers + `1` firefighter Luther Bonner) and serial number **`41-3`**.

3. **`C05` (`[S03]` draft 1: *"Its engines burned so often that crews joked about them"*):**
   - **Finding:** **CUT / FIX APPLIED.** Without a verbatim, primary-sourced wartime quote, saying *"crews joked about them"* in the 30-second cold open weakens the documentary authority.
   - **Action in `SCRIPT.md` & `SOURCES.md`:** Replaced in `[S03]` with the verified engineering fact from Craven & Cate Vol. VI and NACA: *"Its eighteen-cylinder engines ran so hot that magnesium fires could burn through a main wing spar in ninety seconds."*

4. **`C06` (Battle of Kansas, 9 March – 15 April 1944: *"not a single one"* ready, and `150` ready in `5 weeks`):**
   - **Finding:** **VERIFIED.** Both facts are confirmed in the National Museum of the U.S. Air Force *"Battle of Kansas"* fact sheet and Craven & Cate Vol. V, Ch. 1 (pp. 51–56): when General H. H. Arnold arrived at Smoky Hill AAF (Salina, Kansas) on **9 March 1944**, **not a single B-29** of the 58th Bombardment Wing was combat-ready. Arnold placed Maj. Gen. Bennett E. Meyers in command on **10 March 1944**; ~600 Boeing mechanics from Wichita and Seattle joined USAAF crews working outdoors in March snowstorms at Salina, Pratt, Great Bend, and Walker, modifying and clearing **150 B-29s by 15 April 1944** (5 weeks).
   - **Action in `SCRIPT.md`:** Added the exact dates (`9 March` to `15 April 1944`) and `~600` Boeing mechanics to `[S34]`–`[S37]`.

5. **`C07` (Jet stream speeds and ground speeds over Tokyo at ~30,000 feet):**
   - **Finding:** **VERIFIED.** Craven & Cate Vol. V, Ch. 17 (pp. 558–576) and USSBS (*Twentieth Air Force*) record upper-tropospheric westerlies at 27,000–33,000 feet over Honshu routinely blowing at **150 to over 200 mph** (`160–200 knots` / `185–230 mph`), pushing downwind B-29 ground speeds to **450–500 mph** (beyond Norden M-9 bombsight tracking limits).
   - **Action in `SCRIPT.md`:** Specified **150 to 200 miles an hour** and **450 to 500 miles an hour** ground speed in `[S03]` and `[S48]`–`[S49]`.

6. **`C13` (First pressurised bomber in large-scale combat service):**
   - **Finding:** **VERIFIED.** While small numbers of experimental or high-altitude reconnaissance/bomber aircraft (e.g., US XC-35, Boeing 307 Stratoliner, and limited German Ju 86P/R conversions) had pressurised cabins earlier, the Boeing B-29 was the **first heavy bomber in the world to enter large-scale combat service** with fully pressurised crew compartments (`8,000-ft` cabin altitude maintained up to `30,000 ft`, depressurised onto oxygen masks over the target).
   - **Action in `SCRIPT.md`:** Clarified in `[S10]` and `[S12]` (including the **28-inch** diameter crawl tunnel).

7. **`C16` (Order totals before first flight on 21 September 1942):**
   - **Finding:** **VERIFIED & FIXED.** Initial production order for **250** B-29s was approved in **May 1941** (16 months before first flight); by the first flight of XB-29 `41-2` on **21 September 1942**, the USAAF had placed contracts for **1,664 B-29s** (Knaack 1988, p. 481; Craven & Cate Vol. VI, pp. 241–246).
   - **Action in `SCRIPT.md`:** Added the exact figure **1,664** to `[S17]`.

8. **`C19` (Which parts of the Wright R-3350 were magnesium, and how the fires behaved):**
   - **Finding:** **VERIFIED & FIXED.** Curtiss-Wright cast the R-3350's **rear accessory drive housing and supercharger casing** in magnesium alloy. Rear-row cylinder overheating and exhaust valve failures caused backfires that ignited these magnesium castings, which burned at **over 3,000°F (`1,650°C+`)**, resisted carbon-dioxide extinguishers, and burned through the aluminium main wing spar in **60 to 90 seconds** (Craven & Cate Vol. VI, p. 247; NACA Cleveland altitude wind-tunnel reports `GRC-1944-C-05552`).
   - **Action in `SCRIPT.md`:** Named the exact magnesium parts (**rear accessory drive housing and supercharger casing**), the **>3,000°F** burning temperature, and the NACA Cleveland wind-tunnel cooling fixes in `[S23]` and `[S29]`.

9. **`C24` & `C25` (Operation Matterhorn Hump ratio and Bangkok / Yawata raid numbers):**
   - **Finding:** **VERIFIED & FIXED.** Craven & Cate Vol. V (Ch. 3–5, pp. 75–112) documents that **up to 6 to 7 Hump flights** (by stripped B-29 tankers and C-109 transports) were required to stockpile fuel and ordnance at Chengdu for each combat mission over Japan (`C24`). On **5 June 1944** (*Bangkok railway yards*), **98 B-29s** launched from India, **0** were shot down by the enemy, and **5** were lost to engine trouble and accidents (`C25`). On **15 June 1944** (*Yawata Imperial Iron and Steel Works*), **68 B-29s** launched from Chengdu, **47** bombed with slight damage, and **7** were lost, mostly to mechanical trouble (`C25`).
   - **Action in `SCRIPT.md`:** Added the exact confirmed numbers to `[S40]`, `[S41a]`, and `[S41]`.

10. **`C37` (Share of B-29 combat-mission losses due to mechanical failure/accidents vs enemy action):**
    - **Finding:** **VERIFIED & FIXED.** Official Twentieth Air Force statistical tabulations in Craven & Cate Vol. V (pp. 752–756) and the USSBS record **414 B-29s lost on combat missions against Japan**: only **147** were lost directly to Japanese fighters or anti-aircraft fire, whereas **267** (**64.5%**, nearly two-thirds) were lost to operational causes—engine fires, mechanical failures, takeoff crashes, and ditchings.
    - **Action in `SCRIPT.md`:** Added the exact breakdown (**414** lost on combat missions: **147** to enemy fire vs **267** to engine fires, mechanical failures, and accidents) in `[S62]`.

11. **`C40` (Airworthy B-29 count today):**
    - **Finding:** **VERIFIED.** Exactly **two** B-29s fly today: **FIFI** (`44-62070`, Commemorative Air Force) and **Doc** (`44-69972`, Doc's Friends, Wichita). Named both in `[S66]`.

12. **`C43` (Iwo Jima emergency landings):**
    - **Finding:** **VERIFIED & FIXED.** The first emergency landing on Iwo Jima was made on **4 March 1945** under fire by 9th Bombardment Group B-29 *Dinah Might* (`42-65286`). By the end of the war, B-29s made **2,251 recorded emergency landings** on Iwo Jima (often rounded to ~2,400 when counting repeat diversions), carrying **24,761 aircrew members** (Craven & Cate Vol. V, Ch. 18, pp. 592–597; NMUSAF).
    - **Action in `SCRIPT.md`:** Added *Dinah Might* (`4 March 1945`), **2,251 emergency landings**, and **more than 24,000 airmen** to `[S51b]`.

### B. Full Audit Table Across All Claims (`C01`–`C43`)

| Claim(s) | Paragraph(s) | Verdict | Summary |
|---|---|---|---|
| `C01`–`C03` | `S01`, `S02`, `S04`, `S19`, `S60`, `S62a`, `S65` | **PASS** | $1.89B (~$1.9B) Manhattan Project vs ~$3.0B B-29 programme verified in `[AA]`, `[HA]`, `[NMUSAF]`, `[CC6]`, `[VM]`. |
| `C04`, `C20` | `S03`, `S24`–`S27` | **PASS (FIXED)** | First XB-29 (`41-2`) flown 21 Sep 1942 by Eddie Allen (16 engine swaps in 27 hrs); second XB-29 (`41-3`) crashed 18 Feb 1943 into Frye & Co. plant in Seattle killing 11 crew + 20 plant workers + 1 firefighter (Luther Bonner) = 32 deaths. |
| `C05`, `C18`, `C19`, `C21`, `C22` | `S03`, `S20`–`S23`, `S28`–`S30` | **PASS (FIXED)** | Wright R-3350 (18-cyl, 2,200 hp, twin GE turbo-superchargers); magnesium rear accessory housing & supercharger casing fires (>3,000°F) burning through main wing spar in 60–90 s; July 1943 Truman Committee Lockland report; NACA Cleveland wind-tunnel cooling fixes. |
| `C06` | `S03`, `S32`–`S37` | **PASS** | Battle of Kansas (9 Mar – 15 Apr 1944): 0 combat-ready on Arnold's 9 Mar visit to Salina; Maj. Gen. B. E. Meyers + ~600 Boeing mechanics at Salina, Pratt, Great Bend, Walker; 150 B-29s ready by 15 Apr. |
| `C07`, `C28`, `C29` | `S03`, `S46`–`S51` | **PASS** | 24 Nov 1944 first Marianas raid on Tokyo (111 launched from Saipan, 24 bombed Nakajima Musashino); 150–200+ mph jet stream at 30,000 ft pushing downwind ground speed to 450–500 mph; <5% of bombs within 1,000 ft over first two months. |
| `C08`–`C15`, `C41` | `S05`–`S15` | **PASS** | Jan 1940 `R-40B` VLR spec (>5,000 mi with 1 ton); Boeing Model 345 vs Consolidated B-32 backup; 141 ft 3 in wingspan; >60-ton loaded weight; pressurised cabins (8,000-ft cabin at 30,000 ft) linked by 28-in tunnel; GE central analogue fire-control computer. |
| `C16`, `C17`, `C42` | `S16`–`S19b` | **PASS (FIXED)** | 250 ordered May 1941; 1,664 ordered before first flight on 21 Sep 1942; four assembly plants (Boeing Wichita & Renton, Bell Marietta, Martin Omaha); Wichita Plant II (~30,000 workers, Planeview housing for 20,000, >1/3 women). |
| `C23`–`C25` | `S31`, `S38`–`S42` | **PASS (FIXED)** | Operation Matterhorn: India bases + Chengdu staging fields (>300,000 Chinese workers); 6–7 Hump tanker flights per combat mission; 5 Jun 1944 Bangkok (98 launched, 5 lost to accidents); 15 Jun 1944 Yawata (68 launched, 47 bombed, 7 lost). |
| `C26`, `C27`, `C43` | `S43`–`S45`, `S51a`, `S51b` | **PASS (FIXED)** | Saipan, Tinian, Guam (~1,500 mi to Tokyo); Seabees built four 8,500-ft runways at North Field Tinian; Iwo Jima first landing by *Dinah Might* on 4 Mar 1945 and 2,251 emergency landings (24,761 airmen) by V-J Day. |
| `C30`–`C35` | `S52`–`S59` | **PASS** | LeMay assumed command 20 Jan 1945; 5,000–8,000-ft night incendiary shift with stripped guns; 9–10 Mar 1945 *Operation Meetinghouse* (279 bombed Tokyo, ~16 sq mi burned, 80,000–100,000 killed, 14 B-29s lost); >60 cities struck; Silverplate B-29s *Enola Gay* (6 Aug) & *Bockscar* (9 Aug); surrender 15 Aug / 2 Sep 1945. |
| `C36`–`C38`, `C40` | `S60`–`S66` | **PASS (FIXED)** | 3,970 B-29s built; 414 combat-mission losses (147 to enemy fire vs 267 to mechanical/operational causes); post-war B-50, C-97/KC-97, Boeing 377 Stratocruiser, and Soviet Tu-4; two flying today (*FIFI* and *Doc*). |
