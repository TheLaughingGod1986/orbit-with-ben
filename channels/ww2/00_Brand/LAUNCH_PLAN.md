# WW2 & Military History Documentary Channel — Launch & Three-Film Pilot Plan (`J2989`)

> **17 Nov 2026, later the same day:** where this plan differs, `studio/RULES.md` (the channel's own rules, written
> fresh) and `00_Brand/PLAYBOOK.md` govern. Ben is asked only to watch finished films: the Chief locks topics after
> review, and Ben picks the name when he creates the channel. Working titles changed after scoring: see the playbook.


**Date:** `2026-11-17` · **Prepared by:** `macbook-2` (`J2989`)  
**Spend:** `£0.00` (prepared offline/read-only; zero channels created, zero sign-ins, zero ElevenLabs credits spent)  
**Board status:** Added to `studio/plan.json` (`#plan`) for Ben to pick the channel name and lock the first topics, matching the `Every Planet Explained in 10 Minutes` lock card workflow.

---

## 1. Three Channel Name Options (Free Handles Verified Live on YouTube, 17 Nov 2026)

Checked live against `https://www.youtube.com/@<Handle>` and YouTube channel search (`sp=EgIQAg%3D%3D`) on `2026-11-17`. (`@TheWarAtlas` was re-verified `HTTP 200 TAKEN`; `@CommandAndDispatch` was rejected after finding active `@command_dispatch` / `@Commanddispatch` channels; `Operations Room` variants were rejected to stay well clear of *The Operations Room*.) None of the three below resemble `WW2 Dossier`, `WW2 Combat Files`, or `Military Studio`:

| # | Channel Name | Handle | YouTube Check (`17 Nov 2026`) | Why It Works |
|---|---|---|---|---|
| **1 (Recommended)** | **Field Order History** | `@FieldOrderHistory` | **FREE (`HTTP 404`) · `0` channel-name collisions** | A *field order* is where grand strategy meets fuel, weather, terrain, and steel. Distinctly documentary rather than AI-slop ("Dossier / Files"), fits Ben's calm British narration, and leaves room to cover Korea, Cold War, or naval history later without renaming. |
| **2** | **Gridline History** | `@GridlineHistory` | **FREE (`HTTP 404`) · `0` military/history collisions** | Refers to the numbered gridlines on British War Office (`GSGS`) and US Army operational maps — directly signalling our signature combination of code-drawn campaign maps and wartime photography while replacing the taken *The War Atlas*. |
| **3** | **Iron & Compass** | `@IronAndCompass` | **FREE (`HTTP 404`) · `0` military/history collisions** | Clean, memorable two-noun documentary marque spanning naval convoys, air navigation, armour, and industrial logistics across every WW2 theatre. |

> **How it sits in the repo now:** `channels/ww2/studio/channel.json` uses slug `ww2` and film-key prefix `WW2` (`WW2:001`–`WW2:010`), with Option 1 (`Field Order History`, `@FieldOrderHistory`) as placeholder text. If Ben chooses Option 2 or Option 3, only `name`, `short`, `youtube.handle`, and `title_match` in `studio/channel.json` change.

---

## 2. Ten Sourced Topics & Titles (`≤ 70` Characters, First Three Marked)

### Why these angles win without copying competitor templates
- **What `WW2 Dossier` (`14.3k` subs, 39–56 min, archive stills, 0 Shorts) and `WW2 Combat Files` got right:** Viewers on Browse and Suggested click **concrete operational hardware and field problems** (*M1 Garand*, *grasshopper spotter plane*, *B-29 radial engines*) far harder than textbook survey titles (*The Battle of Normandy Explained*).
- **Where we beat them (and stay 100% safe under YouTube's July 2025 / July 2026 monetisation policy):** Competitors lean on repetitive, synthetic-sounding templates (*"What German Generals Admitted..."* or *"Maker Built a 42-Cylinder Monster — ..."*) and static still slideshows. Our titles state a **real historical engineering, logistics, or operational problem in one clean `How`/`Why` sentence (`61–67` chars, zero colons, zero em-dashes)**, and our films pair **per-image verified US/UK official photography** with **code-drawn animated operational maps** (`chart` lane, `£0`).
- **Demand basis:** Anchored in Claude's `17 Nov 2026` vidIQ niche pull (`"world war 2"` **564,442**/mo, `"ww2 documentary"` **261,896**/mo, `"military history"` **236,985**/mo, `"war documentary"` **137,113**/mo) plus live signed-out YouTube GB autocomplete and `30` verified `100k+`-view (`180K` to `22.18M`) neighbour videos pulled `2026-11-17`. *(Exact per-topic vidIQ keyword integers are pulled via Claude's cloud vidIQ connector when a film enters script lock — never guessed offline.)*

### Summary Table of the First Ten Films (`WW2:001` – `WW2:010`)

| ID | Order | Title (`≤ 70` chars) | Chars | Primary US / UK Archive Collections (Checked Per Image) |
|---|---|---|---:|---|
| **`WW2:001`** | **★ PILOT 1 (Make 1st)** | `How Britain Towed Two Floating Ports Across the Channel for D-Day` | 65 | **UK IWM** War Office `BU` / Admiralty `A` / MoI `D` (Crown-expired pre-1976) + **US NARA** `RG 111-SC` & `RG 80-G` (Omaha Mulberry A, Phoenix caissons, Whale roadways, PLUTO drums) |
| **`WW2:002`** | **★ PILOT 2 (Make 2nd)** | `How Long-Range Bombers Closed the Atlantic Black Pit in May 1943` | 64 | **UK IWM** Coastal Command `CH` & Admiralty `A` (VLR Liberators, escort carriers, Western Approaches) + **US NARA/NHHC** `RG 80-G` (`USS Bogue`, HF/DF, convoy escorts) |
| **`WW2:003`** | **★ PILOT 3 (Make 3rd)** | `Why the B-29 Superfortress Cost More Than the Atomic Bomb Project` | 65 | **US NARA** `RG 342-FH` (USAAF 20th Air Force, Wichita/Renton assembly, Wright R-3350 tests, Tinian) + **LoC** `FSA/OWI` federal factory colour plates (`$3.0B` vs `$1.9B` Manhattan Project) |
| `WW2:004` | Film 4 | `Why America's Submarine Torpedoes Failed for 21 Months in WW2` | 61 | **US NHHC & NARA** `RG 80-G` / `RG 74` (Bureau of Ordnance Newport, Mark 14 exploder drop tests at Maui, `USS Silversides` / `USS Tunny` patrol photos & reports) |
| `WW2:005` | Film 5 | `How One Old Destroyer Rammed Germany's Only Atlantic Dry Dock` | 61 | **UK IWM** Admiralty `A` / Combined Operations `N` (`HMS Campbeltown` ex-`USS Buchanan`, Normandie dock gates at St Nazaire, Motor Launches) + **TNA** `ADM 199` / `DEFE 2` |
| `WW2:006` | Film 6 | `Why Britain Built Its Fastest WW2 Bomber Out of Plywood and Balsa` | 65 | **UK IWM** Air Ministry `CH` / `CE` / `TR` (Hatfield & High Wycombe furniture workshops, moulded birch-balsa fuselages, Pathfinder Oboe raids) + **TNA** `AIR 14` / `AVIA 15` |
| `WW2:007` | Film 7 | `How Floating Dry Docks Kept Damaged US Fleets Fighting Off Japan` | 64 | **US NHHC & NARA** `RG 80-G` (Service Squadron 10 at Ulithi Atoll, `ABSD-1`/`ABSD-2` lifting `45,000`-ton battleships, colliers, ammunition ships, concrete ice-cream barge) |
| `WW2:008` | Film 8 | `How One Planted Briefcase Pulled German Divisions Away From Sicily` | 66 | **UK TNA** `CAB 154` / `WO 208` / `ADM 223` declassified Operation Mincemeat files (Major William Martin ID card, `HMS Seraph`, Huelva dispatches) + **IWM** Sicily `NA` series |
| `WW2:009` | Film 9 | `How One Wrecked Oil Tanker Saved Starving Malta in August 1942` | 62 | **UK IWM** Admiralty `A` (`SS Ohio` riding decks-awash lashed between `HMS Penn` and `HMS Ledbury` into Grand Harbour, `HMS Eagle`/`Indomitable` convoy decks) + **US NARA** Texaco/Merchant Marine |
| `WW2:010` | Film 10 | `Why Britain Built Flame, Flail and Bridge Tanks After Dieppe Failed` | 67 | **UK IWM** War Office `H` & `BU` (Dieppe August 1942 immobilised Churchills on chert shingle; 79th Armoured Division Sherman Crab flails, AVRE petard/fascine, Crocodile) + **TNA** `WO 205` |

---

### Topic-by-Topic Demand, Sourcing & Verified `100k+` Neighbour Videos (`Pulled 2026-11-17`)

#### `WW2:001` ★ PILOT 1 — `How Britain Towed Two Floating Ports Across the Channel for D-Day` (`65 chars`)
- **Original angle:** After the August 1942 Dieppe raid proved seizing a defended French port intact was suicidal, British and US engineers secretly built two Dover-sized harbours (`Mulberry A` and `Mulberry B`) in pieces around Britain — `212` `6,000`-ton concrete Phoenix caissons, flexible steel Whale roadways that rose `24 feet` with the Normandy tide, Bombardons, Gooseberry blockships, and `PLUTO` undersea fuel pipelines — then towed `1.5 million tons` across the Channel at `4 knots` and survived the `19–22 June 1944` gale that wrecked Omaha's Mulberry A while Arromanches (`Mulberry B`) landed `2.5 million men`, `500,000 vehicles`, and `4 million tons` of supplies.
- **Demand:** Sits inside `world war 2` (`564,442`/mo vidIQ) & `ww2 documentary` (`261,896`/mo vidIQ); YouTube GB autocomplete confirms `'mulberry harbor'`, `'d day mulberry harbour'`, `'mulberry harbours ww2'`, `'mulberry b artificial harbor'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `759f-CHW-S8` — *The reason Germany failed on D-Day* (**4,879,377 views**, `23:26`)
  2. `sYXYG_F1EK0` — *Why Was Normandy Selected For D-Day?* (**1,937,565 views**, `14:54`)
  3. `zpFLLGkNm7I` — *The Floating Harbors of D-Day* (**972,554 views**, `24:55`; alongside `Nv9lBqPVuoE` *Operation PLUTO* at **1,460,569 views**, `0GgZUbGltNs` at **1,030,526 views**, and `1aGU2JQ2jDg` *Mulberry Harbours* at **180,365 views**, `35:33`)

#### `WW2:002` ★ PILOT 2 — `How Long-Range Bombers Closed the Atlantic Black Pit in May 1943` (`64 chars`)
- **Original angle:** In March 1943 (`Convoy HX 229` / `SC 122`), Admiral Dönitz's U-boats sank `627,000 tons` of Allied shipping in a single month by hunting inside the **Mid-Atlantic Air Gap** ("the Black Pit") — a `600-mile` stretch south of Greenland beyond land-based aircraft from Newfoundland, Iceland, and Northern Ireland. Just eight weeks later ("Black May" 1943), Dönitz lost `43 U-boats` (`25%` of his operational crews) and withdrew from the North Atlantic because four technologies converged simultaneously: `2,400-mile` Very Long Range (`VLR`) B-24 Liberators modified with extra bomb-bay fuel tanks, escort carriers (`HMS Biter`, `USS Bogue`), `10 cm` centimetric Type 271 / ASV Mk III radar that U-boat Metox receivers could not hear, and shipboard `HF/DF` ("Huff-Duff") radio triangulation.
- **Demand:** Core `ww2 documentary` (`261,896`/mo vidIQ) + `military history` (`236,985`/mo vidIQ); YouTube GB autocomplete confirms `'battle of the atlantic ww2'`, `'battle of atlantic ww2 footage'`, `'battle of the north atlantic world war ii'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `21qqkC1cWvE` — *Battlefield S2/E2 - The Battle of the Atlantic* (**4,127,642 views**, `1:55:11`)
  2. `JyLzA1dRc-Q` — *Why Germany Lost the Battle of the Atlantic (WW2 Documentary)* (**1,591,650 views**, `18:19`)
  3. `pEm4FK9Osjo` — *The Battle of the Atlantic: U-boats and how to sink them* (**1,299,973 views**, `54:03`; alongside `4PLS0EozSYQ` *Convoy HG76 - The Beginning of the End for the U-Boats* at **541,440 views**, `28:53`)

#### `WW2:003` ★ PILOT 3 — `Why the B-29 Superfortress Cost More Than the Atomic Bomb Project` (`65 chars`)
- **Original angle:** The Manhattan Project cost `$1.9 billion`; designing, tooling, and fielding the Boeing `B-29 Superfortress` cost **`$3.0 billion`** — the single most expensive weapons programme of World War II. Ordered off the drawing board before a prototype flew, the B-29 combined four untested leaps at once: pressurised crew compartments connected by a `35-foot` crawl tunnel, General Electric analog-computer remote gun turrets, high-aspect-ratio laminar wings with extreme wing loading, and magnesium-crankcase `Wright R-3350` `18-cylinder` engines that caught fire so often Boeing's chief test pilot Edmund Allen died in the crash of the second prototype (`18 Feb 1943`), followed by the `"Battle of Kansas"` modification blitz in freezing snow and the `30,000-foot` Japanese jet-stream crisis that forced General Curtis LeMay's radical low-altitude pivot in March 1945.
- **Demand:** Proven high-outlier subject in Claude's 17 Nov winner cohort (`WW2 Combat Files` radial/B-29 series) + `ww2 documentary` (`261,896`/mo vidIQ); YouTube GB autocomplete `#1` `'b 29 superfortress documentary'`, `'b 29 bomber documentary'`, `'boeing b 29 superfortress documentary'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `pe9o5SIDh0w` — *The WWII Flying Superfortress - B-29* (**4,022,270 views**, `12:15`)
  2. `RKgQBpP5kVs` — *B-29 Superfortress Operation Against Germany* (**1,958,234 views**, `10:55`)
  3. `Zlvjr0jqSv4` — *B-29: Frozen in Time (NOVA Classics) | Full Documentary* (**1,201,739 views**, `54:43`; alongside `KWoPUqxroT0` *Inside the B-17 Flying Fortress* at **7,379,079 views**, `24:15`)

#### `WW2:004` — `Why America's Submarine Torpedoes Failed for 21 Months in WW2` (`61 chars`)
- **Original angle:** From December 1941 until September 1943, US Pacific submarine crews risked depth-charge destruction to line up textbook shots — only to hear metallic *clangs* as `Mark 14` torpedoes ran `10 feet` deeper than set, triggered prematurely on their secret `Mark 6` magnetic exploders, or crushed their firing pins on `90-degree` hits while the Bureau of Ordnance blamed submarine skippers until Admirals Lockwood and Christie ran unauthorized live-warhead net and cliff tests in Hawaii and Western Australia.
- **Demand:** `military history` (`236,985`/mo vidIQ) + YouTube GB autocomplete `'mark 14 torpedo'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `tPug2HYrnqo` — *The Giant Torpedo Fail that Almost Changed WW2* (**1,673,011 views**, `10:20`)
  2. `eQ5Ru7Zu_1I` — *The Mark 14 Torpedo - Failure is Like Onions* (**1,431,562 views**, `33:27`)
  3. `k7LKQBdXsHk` — *The USN Pacific Submarine Campaign - Hey, the torpedoes are working!* (**1,322,956 views**, `1:03:52`)

#### `WW2:005` — `How One Old Destroyer Rammed Germany's Only Atlantic Dry Dock` (`61 chars`)
- **Original angle:** To keep the `42,000`-ton German battleship *Tirpitz* out of the Atlantic convoy lanes, Britain had to destroy the only German-held dry dock on the Atlantic coast big enough to repair her — the heavily fortified *Forme Écluse Louis Joubert* (`Normandie` dock) five miles up the Loire mudflats at St Nazaire (`Operation Chariot`, `28 March 1942`) — by disguising a `1919` flush-deck American destroyer (`HMS Campbeltown`), packing `4.25 tons` of Amatol with acid-delay pencils into her bow, and ramming the `35-foot`-thick steel caisson at `20 knots`.
- **Demand:** `war documentary` (`137,113`/mo vidIQ) + YouTube GB autocomplete `'st nazaire raid'`, `'hms campbeltown st nazaire'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `07Zd0Oy8JyQ` — *Jeremy Clarkson's the Greatest Raid of All - the FULL documentary* (**8,192,982 views**, `58:17`)
  2. `SCMCr2Kh1wI` — *The Against-All-Odds WW2 Commando Raid You've Never Heard Of* (**4,570,851 views**, `58:25`)
  3. `NB5mAG1WvvU` — *The Greatest Raid - Operation Chariot* (**1,299,056 views**, `5:36`; alongside `cqrow4nbZZg` at **988,061 views**, `22:21`)

#### `WW2:006` — `Why Britain Built Its Fastest WW2 Bomber Out of Plywood and Balsa` (`65 chars`)
- **Original angle:** In 1939–40, facing acute aluminium and gun-turret shortages, Geoffrey de Havilland proposed a twin-Merlin bomber with **zero defensive guns** made of Ecuadorian balsa sandwiched between Canadian birch plywood by High Wycombe cabinetmakers (`DH.98 Mosquito`) — flying fast and high enough (`~400 mph`) to outrun German fighters, carry a `4,000-lb` `"Cookie"` blockbuster to Berlin (the same payload as a four-engine `B-17`), and suffer the lowest loss rate (`0.7%`) in RAF Bomber Command.
- **Demand:** `ww2 documentary` (`261,896`/mo vidIQ) + YouTube GB autocomplete `'de havilland mosquito documentary'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `ww1E6ufDWzs` — *Wrecking & Trolling The Germans With A Wooden Plane - DH-98 Mosquito* (**5,392,357 views**, `20:05`)
  2. `JTsnMKzmdWs` — *De Havilland Mosquito: The wooden fighter-bomber that could do it all* (**3,111,460 views**, `13:16`)
  3. `TDZlMRVwxEY` — *Why The Mosquito Bomber Was The Unsung Hero Of WW2* (**2,386,918 views**, `46:43`)

#### `WW2:007` — `How Floating Dry Docks Kept Damaged US Fleets Fighting Off Japan` (`64 chars`)
- **Original angle:** Imperial Japanese planners assumed US carrier task forces operating `5,000 miles` west of Pearl Harbor would have to steam all the way back to Hawaii or California whenever a ship took a torpedo or typhoon damage. Instead, the US Navy built **Service Squadron 10** and sectional **Advance Base Sectional Docks (`ABSDs`)** capable of lifting `90,000 tons` out of the lagoon at **Ulithi Atoll** — anchoring `617 ships` at once with mobile machine shops, underway replenishment oilers, hospital ships, and even a concrete refrigerated barge (`BRL-1828`) churning `500 gallons` of ice cream per shift.
- **Demand:** `military history` (`236,985`/mo vidIQ) + YouTube GB autocomplete `'pacific war world war ii'`, `'ulithi atoll ww2'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `NYv-GC8DgMk` — *WW2 | The Resource War 1: Arsenal of Democracy* (**3,686,336 views**, `8:44`)
  2. `iIpPuJ_r8Xg` — *The US Military's Massive Global Transportation System* (**3,247,262 views**, `18:14`)
  3. `TOJQkhzpLyQ` — *WWII in the Pacific: Why Japan Lost* (**2,411,240 views**, `14:37`; alongside `Qiyo8D0nH70` *World War 2 Ice Cream of the US NAVY* at **2,023,580 views** and `OigDDVn3IaU` at **1,320,900 views**)

#### `WW2:008` — `How One Planted Briefcase Pulled German Divisions Away From Sicily` (`66 chars`)
- **Original angle:** With Allied forces poised in North Africa in spring 1943, Sicily was the obvious next landing zone. British Naval Intelligence (`Twenty Committee` — Ewen Montagu and Charles Cholmondeley) built a complete paper life for a non-existent Royal Marines courier (`"Major William Martin"` — down to theatre stubs, an overdraft letter from Lloyds Bank, and fake high-command letters pointing to Greece and Sardinia), released the canister from submarine `HMS Seraph` into the tidal current off Huelva, Spain (`Operation Mincemeat`), and tracked via `Ultra` intercepts at Bletchley Park as Berlin shifted the `1st Panzer Division` to Greece and E-boats away from Sicily.
- **Demand:** `war documentary` (`137,113`/mo vidIQ) + YouTube GB autocomplete `'operation mincemeat documentary'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `NtUSYNHmPyU` — *Operation Mincemeat: The Shadow Catalyst for CIA's Dark Age* (**3,135,398 views**, `28:21`)
  2. `8lQtdhtw5eI` — *The Grave of the Man Who Never Was: Operation Mincemeat* (**2,029,452 views**, `3:17`)
  3. `yoIjVIG94OU` — *How a Fake Soldier Defeated the Nazis* (**1,425,788 views**, `14:57`; alongside `hBk3sSUB5X4` at **1,278,357 views**, `58:48`)

#### `WW2:009` — `How One Wrecked Oil Tanker Saved Starving Malta in August 1942` (`62 chars`)
- **Original angle:** By August 1942, besieged Malta — sitting astride Rommel's North African supply lifeline — was down to weeks of aviation spirit and flour. Britain assembled `Operation Pedestal`: `14` fast merchantmen escorted by `4` aircraft carriers, `2` battleships, `7` cruisers, and `32` destroyers running a `4-day` gauntlet of Axis submarines, E-boats, and `700+` aircraft. Nine merchant ships and `HMS Eagle` were sunk; the fast American-built tanker **`SS Ohio`** (carrying `11,500 tons` of kerosene and fuel oil) took a torpedo, two crashed bombers on her deck, and near-misses that broke her spine — yet reached Valletta's Grand Harbour on `15 August 1942` held afloat only by two Royal Navy destroyers (`HMS Penn` and `HMS Ledbury`) lashed tightly to each flank.
- **Demand:** `ww2 documentary` (`261,896`/mo vidIQ) + YouTube GB autocomplete `'operation pedestal malta'`.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `0inR2jRW_P8` — *Operation Pedestal: The Convoy That Saved Malta* (**683,272 views**, `9:43`)
  2. `NeJWWPoyUPI` — *Operation Pedestal (1/4) - The Convoy Enters the Killzone* (**569,942 views**, `26:22`)
  3. `baJBXE63M1w` — *SS Ohio: The Tanker That Saved Malta in 1942* (**312,110 views**, `14:27`; alongside `zpE68ZyDj6k` at **315,739 views**, `21:56`)

#### `WW2:010` — `Why Britain Built Flame, Flail and Bridge Tanks After Dieppe Failed` (`67 chars`)
- **Original angle:** On `19 August 1942` at Dieppe, all `29` landed Canadian Churchill tanks were stopped on the beach by loose chert shingle that jammed their tracks and a `6-foot` concrete sea-wall they could not climb. Rather than send infantry naked against Rommel's Atlantic Wall on D-Day, Major-General Percy Hobart's **79th Armoured Division** engineered specialised assault vehicles (`"Hobart's Funnies"`): spinning chain mine-flails (`Sherman Crab`), `290 mm` spigot-mortar bunker-busters carrying `4-ton` brushwood fascines and canvas road carpets over soft blue clay (`Churchill AVRE`), armoured assault bridges, `DD` canvas-screen swimming Shermans, and `Crocodile` flame tanks — explaining why British/Canadian Gold, Juno, and Sword beaches broke inland cleanly on `6 June 1944` where US commanders declined most of the specialist armour other than `DD` tanks.
- **Demand:** `world war 2` (`564,442`/mo vidIQ) + `military history` (`236,985`/mo vidIQ); strong Browse crossover with tank/engineering audiences.
- **Three verified `100k+` neighbours (`2026-11-17` GB read):**
  1. `hRl0VICYS9c` — *The Real Tank Genius Of WW2 - Percy "Hobo" Hobart* (**3,332,466 views**, `20:57`)
  2. `2QI0ieR-zXM` — *Hobart's Funnies | The Strange Tanks of Operation Overlord* (**1,230,872 views**, `31:18`)
  3. `VcVroGVEaNU` — *Germans Laughed at Britain's Dustbin Gun* (**700,863 views**, `18:43`; alongside `ksc3MdjWsxc` at **645,898 views**, `12:25`)

---

## 3. Channel Packaging Style (One Title Style + One Thumbnail Style + Three Examples)

### A. One Fixed Title Style
- **Formula:** `How [Specific Hardware, Ship, or Operation] [Concrete Action Verb] [Hard Operational Stakes or Timeframe]` or `Why [Specific Hardware or Programme] [Concrete Cost, Material, or Failure]`.
- **Hard constraints:**
  - `55–70` characters (never truncated on mobile Browse or Suggested rail);
  - Plain Title Case sentence — **zero colons (`:`), zero em-dashes (`—`), zero pipes (`|`), zero all-caps shouting**;
  - Names the real historical system or place up front (`Two Floating Ports`, `Atlantic Black Pit`, `B-29 Superfortress`, `Mark 14` / `Submarine Torpedoes`, `Plywood and Balsa`) plus one tangible number or operational constraint;
  - Never copies competitor AI-slop templates (*"What German Generals Admitted..."*, *"Shocked Enemy Commanders..."*).

### B. One Fixed Thumbnail Style
- **Visual foundation:** One authentic, high-resolution US federal (`NARA`/`NHHC`/`LoC`) or UK Crown-expired (`IWM`) wartime photograph occupying `85–100%` of the `1280×720` frame, cleaned of dust scratches and graded for **high-contrast tonal separation** (deep blacks lifted above crushing so near-black stays `<= 30%`, crisp mid-tone steel/concrete detail, subtle warm sepia-silver tone or authentic wartime Kodachrome colour where real colour exists, plus **one crisp `#FF3B30` crimson-orange tactical map arc or callout arrow** only when pointing to the key structure).
- **Cover text (`2–4` words max):**
  - Set in a clean upper-left or top-band dark gradient zone, never overlapping the focal machine/ship and never touching the bottom-right duration badge;
  - Heavy condensed sans-serif (house bold grotesque), **1–2 key words/numbers in `#FFD600` signal yellow**, rest in `#FFFFFF` pure white, `6 px` `#0B0E14` keyline + soft drop shadow so every letter reads instantly at `168×94 px` mobile preview;
  - **Complements the title** rather than repeating its words.

### C. Three Concrete Example Thumbnails (Pilot Films `001`–`003`)

1. **Pilot 1 (`WW2:001` Mulberry Harbours) — Text: `BUILT IN 12 DAYS` (`12 DAYS` in `#FFD600`, `BUILT IN` in `#FFFFFF`):**
   - **Archive photo:** High-angle Royal Navy / War Office aerial photograph (`IWM BU` / `US NARA RG 80-G`, June 1944, Crown-copyright-expired / US PD) looking straight down the curved line of sunken `6,000`-ton concrete `Phoenix` breakwaters and floating steel `Whale` pierheads packed with trucks streaming ashore at Arromanches (`Mulberry B`).
   - **Contrast & callout:** Crisp silver-white surf breaking against the outer concrete wall vs calm dark harbour water inside; one clean `#FF3B30` bracket callout pointing to the floating roadway (`1.5M TONS TOWED` omitted — keep strictly to 4 words `BUILT IN 12 DAYS`).
2. **Pilot 2 (`WW2:002` Mid-Atlantic Air Gap) — Text: `600-MILE DEAD ZONE` (`DEAD ZONE` in `#FFD600`, `600-MILE` in `#FFFFFF`):**
   - **Archive photo:** Dramatic low-altitude RAF Coastal Command / US Navy photograph (`IWM CH` / `NARA RG 80-G`, 1943, Crown-expired / US PD) of a white-camouflaged `B-24 Liberator` banking low over a surfaced Atlantic U-boat churning white foam in dark grey North Atlantic swells.
   - **Contrast & callout:** High-contrast white fuselage and ocean spray against dark slate sea; subtle translucent arc overlay in top-right corner hinting at the Greenland–Iceland–Newfoundland air-cover gap closing over the U-boat.
3. **Pilot 3 (`WW2:003` B-29 Superfortress Cost) — Text: `$3 BILLION GAMBLE` (`$3 BILLION` in `#FFD600`, `GAMBLE` in `#FFFFFF`):**
   - **Archive photo:** Authentic wartime US Office of War Information / USAAF wide-angle factory photograph (`LoC FSA/OWI` / `NARA RG 342-FH`, US federal public domain) of gleaming unpainted aluminium `B-29 Superfortress` greenhouse noses stretching down the Boeing Wichita assembly bay, paired with high-contrast cockpit glass and `Wright R-3350` nacelles.
   - **Contrast & callout:** Bright specular highlights on polished duralumin skin against deep factory rafters; `$3 BILLION` in `#FFD600` top-left (`3 words` total, instant mobile legibility).

---

## 4. Three-Film Pilot Plan & Shared ElevenLabs Voice Budget

### Voice Budget Arithmetic (Strict Guardrail — £0 Extra Spend)
- **Current shared ElevenLabs pool (17 Nov 2026):** `~79,000` characters remaining in this billing cycle, shared across **Orbit With Ben**, **History of Science**, and this pilot (`AGENTS.md` `channel_balance.py` priority applies; never top up, upgrade, or alter the plan).
- **Character rate:** A `10-minute` narrated script uses `~8,000` characters (`~800` characters/minute at `~132 wpm`).
- **Pilot runtime cap:** **~25 minutes per pilot film** = **`~20,000` spoken characters** (`3,250–3,350` words; budgeted at **`21,000` characters** per film with a `5%` Scribe pickup margin).
- **Hard two-film cap before upgrade/renewal:**
  - **Pilot 1 (`WW2:001`, `25 min`):** `~20,000` spoken chars (`21,000` max with pickups) — **Voiced in current cycle** once Ben locks topic & creates channel.
  - **Pilot 2 (`WW2:002`, `25 min`):** `~20,000` spoken chars (`21,000` max with pickups) — **Voiced in current cycle** (only after confirming OWB & HOS scheduled voice takes remain covered).
  - **Subtotal voiced in current cycle (2 films max):** **`~40,000` spoken chars (`42,000` max)** — leaving **`~37,000–39,000` characters (`~48%` of remaining pool)** untouched for Orbit With Ben and History of Science!
  - **Pilot 3 (`WW2:003`, `26 min`):** `~20,800` spoken chars (`21,800` max with pickups) — **Script, `SOURCES.md`, USAAF archive harvest, and code-drawn maps built at `£0` now; VO HELD until Ben upgrades ElevenLabs or the monthly cycle renews.**
  - **Post-upgrade steady state (`WW2:004` onward):** Expand runtime to **`32–42 minutes`** (`~25,600–33,600` characters/film) at **2 films/week** so `~35,000–40,000` total channel views clear the `1 Feb 2027` **8,000 watch-hour** YPP threshold.

---

### Pilot Film 1 (`WW2:001`): *How Britain Towed Two Floating Ports Across the Channel for D-Day*
- **Target length & voice:** **`25:00`** (`~3,300` spoken words · **`~20,000` characters**, `21,000` max with pickups · **Voice Slot 1 of 2** in current cycle).
- **Six-Chapter Outline:**
  1. **`0:00–3:30` Cold Open — The Lesson Written in Shingle at Dieppe (`Aug 1942`):** Proof-first aerial shot of Arromanches artificial port (`0:00`); why attacking Cherbourg or Le Havre head-on meant catastrophe, and the radical calculation: `2` Allied armies needed `12,000 tons` of fuel, ammunition, and rations ashore *every single day* across open beaches with a `24-foot` Channel tidal range.
  2. **`3:30–8:00` Chapter 1 — Churchill's "Piers Must Float Up and Down with the Tide" (`1942–1943`):** Churchill's famous `30 May 1942` minute (`WHO: Winston Churchill`, `WHO: Hugh Iorys Hughes`, `WHO: Allan Beckett`); competing designs tested in Scottish sea lochs at Garlieston (`DATA` tidal range & wave-tank forces).
  3. **`8:00–13:00` Chapter 2 — Secret Concrete Giants in the Thames (`Winter 1943–Spring 1944`):** `45,000` British workers pouring `212` six-storey hollow `Phoenix` concrete caissons (`6,044 tons` each), `Bombardon` floating cruciform breakwaters, `Spud` jack-up pierheads, and `10 miles` of flexible `Whale` steel bridge spans — then sinking them in shallow English estuaries (`Selsey`, `Dungeness`) to hide them from Luftwaffe reconnaissance.
  4. **`13:00–17:30` Chapter 3 — The 4-Knot Armada (`6–18 June 1944`):** Refloating the caissons on D-Day, `150+` ocean tugs towing `1.5 million tons` across `100 miles` of English Channel; sinking `55` elderly `Corncob` blockships (`Gooseberries`) in `48 hours` and positioning `Mulberry A` (Omaha) and `Mulberry B` (Gold Beach, Arromanches).
  5. **`17:30–21:30` Chapter 4 — Midpoint Twist: The Worst June Gale in 40 Years (`19–22 June 1944`):** Force 6–8 northeasterly storm slams Normandy; why US `Mulberry A` broke apart on `20 June` (unprotected deep-water exposure, loose `Bombardons` battering `Phoenix` walls, rushed seabed surveying) while British `Mulberry B` behind the Calvados Reef held firm and salvaged `Mulberry A`'s surviving spans.
  6. **`21:30–25:00` Chapter 5 — Fuel Under the Sea (`PLUTO`) & the Tonnage Verdict (`July–Nov 1944`):** `Conundrum` floating steel bobbins laying `Operation PLUTO` pipelines from the Isle of Wight to Cherbourg and Dungeness to Boulogne; how Arromanches + open-beach `LST`/`DUKW` logistics moved `2.5M` troops and `4M` tons before Antwerp opened.
- **Primary Sources List (for `01_Script/SOURCES.md` & Description `Sources:` line):**
  1. Hartcup, Guy (2011 / orig. 1977), *Code Name Mulberry: The Planning, Building & Operation of the Normandy Harbours* (official War Office / Admiralty file synthesis).
  2. UK The National Archives `CAB 106/999` & `WO 219/2522` — *SHAEF Chief Engineers' Report on Artificial Harbours (Mulberry A & B), 1944–1945*.
  3. Ruppenthal, Roland G. (1953), *Logistical Support of the Armies, Vol. I: May 1941 – September 1944*, US Army Center of Military History (*United States Army in World War II*, public domain federal history — exact daily tonnage tables for Omaha vs Mulberry B during and after the `19–22 June` gale).
  4. Morison, Samuel Eliot (1957), *History of United States Naval Operations in World War II, Vol. XI: The Invasion of France and Germany, 1944–1945* (Naval Task Force 128 Mulberry A tow and storm damage logs).
  5. Institution of Civil Engineers (1948), *The Civil Engineer in War, Vol. 2: Docks and Harbours* (Jory, Pavry, Beckett, and Wood papers on `Phoenix` caissons and `Whale` flexible roadways).
- **Picture Plan (`~260` cuts across `25:00`):**
  - **Archive stills & public-domain newsreels (`~70%`, `~180` cuts):** `IWM` War Office `BU` / Admiralty `A` / MoI `D` Crown-expired series (Garlieston prototypes, Thames dry-dock `Phoenix` builds, `Conundrum` drum towing, Arromanches aerials) + `US NARA RG 111-SC` & `RG 80-G` (Omaha `Mulberry A` storm wreckage, `DUKW` amphibians, `LST` beaching). Smooth `1.00 -> 1.045` sub-pixel pan/zoom per cut.
  - **Code-drawn maps & engineering graphics (`~30%`, `~80` cuts, `£0`):** (1) Channel map showing `Selsey`/`Portsmouth` staging zones and `4-knot` tow lanes to Omaha and Arromanches; (2) Animated `24-foot` tide diagram showing `Spud` pierhead legs + `Whale` torsion bridge flexing without snapping; (3) Calvados Reef bathymetry comparison (`Mulberry B` sheltered vs `Mulberry A` exposed); (4) Animated daily tonnage bar chart (`Omaha DUKW/LST` vs `Mulberry B` June–Oct 1944); (5) `PLUTO` pipeline routes (`Bambi` & `Dumbo`).
  - **Flow Veo (`0%` needed):** 100% covered by rich US/UK engineering photography, US Signal Corps public-domain `16 mm`/`35 mm` storm footage, and code-drawn maps (`£0`).

---

### Pilot Film 2 (`WW2:002`): *How Long-Range Bombers Closed the Atlantic Black Pit in May 1943*
- **Target length & voice:** **`25:00`** (`~3,300` spoken words · **`~20,000` characters**, `21,000` max with pickups · **Voice Slot 2 of 2** in current cycle).
- **Six-Chapter Outline:**
  1. **`0:00–3:30` Cold Open — March 1943: Four Days from Losing the Atlantic Lifeline:** `Convoy HX 229` & `SC 122` (`22 ships`, `146,000 tons` sunk against `1` U-boat lost); the British Admiralty's written admission that Germans *"never came so near to disrupting communications between the New World and the Old."*
  2. **`3:30–8:00` Chapter 1 — Geometry of the "Black Pit":** Why aircraft flying from Northern Ireland, Iceland, and Newfoundland left a `600-mile` unpatrolled oval south of Greenland where wolfpacks (`40+` Type VIIc boats) surfaced in broad daylight to recharge batteries and outrun `16-knot` corvettes.
  3. **`8:00–13:00` Chapter 2 — Eight Handfuls of VLR Liberators (`No. 120 Squadron RAF` & USAAF Controversy):** Why Bomber Command and US Pacific theatres hoarded `B-24 Liberators` while fewer than **40 Very Long Range (`VLR`) B-24s** — stripped of belly turrets and armour to reach `2,400 miles` — could cover the entire gap (`WHO: Max Horton`, `WHO: John Slessor`).
  4. **`13:00–17:30` Chapter 3 — Invisible Beams (`10 cm` Cavity Magnetron Radar, Leigh Light & `HF/DF`):** How British `Type 271` / `ASV Mk III` centimetric radar spotted a submarine conning tower through Atlantic fog without triggering German `Metox` receivers, paired with shipboard `HF/DF` triangulating every U-boat wolfpack radio report within seconds.
  5. **`17:30–21:30` Chapter 4 — Midpoint Climax: Convoy `ONS 5` (`29 April – 6 May 1943`):** Gales scatter a slow westbound convoy off Greenland right into `43` waiting U-boats (`Group Fink`) — and instead of a massacre, radar-equipped escorts (`HMS Duncan` / `HMS Vidette` with Hedgehog forward-throwing mortars) and VLR Liberators sink **7 U-boats** in blind fog.
  6. **`21:30–25:00` Chapter 5 — "Black May" & Dönitz's Retreat (`24 May 1943`):** Escort carriers (`USS Bogue`, `HMS Biter`) + Support Groups seal the gap permanently; `43 U-boats` lost in `31 days`; Dönitz orders temporary withdrawal from the North Atlantic on `24 May 1943`, clearing the sea lane for `Operation Overlord`.
- **Primary Sources List:**
  1. Roskill, Capt. S.W. (1956), *The War at Sea 1939–1945, Vol. II: The Period of Balance*, HMSO (*History of the Second World War, UK Military Series* — Crown copyright expired, exact monthly merchant sinkings vs U-boat losses and `ONS 5` track charts).
  2. UK The National Archives `ADM 199/2020` & `AIR 41/47` — *RAF Coastal Command Narrative: The Anti-U-Boat War, 1942–1943* (exact VLR Liberator squadron counts and sortie hours in the Greenland Air Gap).
  3. Morison, Samuel Eliot (1947 / 1956), *History of United States Naval Operations in World War II, Vol. I & Vol. X: The Atlantic Battle Won, May 1943 – May 1945* (`USS Bogue` TG 21.12 action reports).
  4. US Navy Tenth Fleet / Chief of Naval Operations (1946, declassified NARA), *German Submarine Activities on the Atlantic Coast and U-Boat Loss Assessment, 1943*.
  5. Dönitz, Karl (war diary extracts via UK Admiralty Naval Staff History *The Defeat of the Enemy Attack on Shipping, 1939–1945*, `BR 1736(51)`, TNA `ADM 234/578` — exact `24 May 1943` withdrawal signal).
- **Picture Plan (`~255` cuts across `25:00`):**
  - **Archive stills & official film (`~65%`, `~165` cuts):** `IWM` Coastal Command `CH` & Admiralty `A` series (Reykjavik & Ballykelly `B-24` bases, `Flower`-class corvettes pitching in green Atlantic seas, `Type 271` lantern radar domes, Western Approaches `Wrens` plotting table in Liverpool) + `US NARA/NHHC RG 80-G` (`USS Bogue` `CVE-9` flight deck in heavy swell, `Grumman Avenger` depth-charge runs, `Hedgehog` spigot launchers).
  - **Code-drawn maps & operational graphics (`~35%`, `~90` cuts, `£0`):** (1) North Atlantic orthographic map with animated `800-mile` vs `1,100-mile` aircraft range circles from Newfoundland, Iceland, and Ulster shrinking the "Black Pit" to zero; (2) `HF/DF` two-escort bearing intersection diagram; (3) `1.5 m` Metox-detectable wave vs `10 cm` centimetric radar beam; (4) `Convoy ONS 5` day-by-day encounter plot (`29 Apr – 6 May 1943`); (5) Dual line chart: Allied merchant tonnage sunk vs German U-boats sunk (`Jan 1942 – Aug 1943`, highlighting the May 1943 crossover).
  - **Flow Veo (`0%` required; optional `1–2` empty grey North Atlantic storm-swell transition plates max, `flow_only` `0` £, labelled `AI illustration` if used).**

---

### Pilot Film 3 (`WW2:003`): *Why the B-29 Superfortress Cost More Than the Atomic Bomb Project*
- **Target length & voice:** **`26:00`** (`~3,450` spoken words · **`~20,800` characters**, `21,800` max with pickups · **Scripted & harvested at `£0` now; VO HELD until Ben upgrades ElevenLabs or the cycle renews**).
- **Six-Chapter Outline:**
  1. **`0:00–3:30` Cold Open — `$3.0 Billion` vs `$1.9 Billion`:** Cold open on rows of silver `B-29` noses at Wichita (`0:00`); why building an intercontinental pressurised bomber from scratch cost `58%` more than inventing nuclear weapons — and why Boeing's second prototype burned out of the sky over Seattle on `18 February 1943`.
  2. **`3:30–8:00` Chapter 1 — Ordering `1,600` Bombers Before One Had Flown (`1940–1942`):** Hap Arnold's Pacific range problem (`3,200+ miles` round trip, zero European bases if Britain fell); pressurised forward/aft cabins joined by a `28-inch` tunnel over unpressurised bomb bays (`WHO: Henry "Hap" Arnold`, `WHO: Edmund "Eddie" Allen`).
  3. **`8:00–13:00` Chapter 2 — Magnesium Fires & General Electric's Analog Fire-Control Computer:** Why `Wright R-3350` `2,200-hp` twin-row radials overheated (`magnesium` accessory housings igniting at `630°C` so water/CO2 extinguishers couldn't put them out), alongside the revolutionary `GE` central station computer compensating for lead, windage, gravity drop, and parallax at `30,000 feet`.
  4. **`13:00–17:30` Chapter 3 — The "Battle of Kansas" (`March–April 1944`) & Flying Over the Himalayas (`Operation Matterhorn`):** Production B-29s rolling off Wichita lines straight onto snow-swept Kansas ramps unable to fly; `600` engineers working outdoors in sub-zero winds; why staging from China (`Chengdu`) burned `7 gallons` of aviation fuel just to carry `1 gallon` to the bomber bases.
  5. **`17:30–22:00` Chapter 4 — Midpoint Crisis: Discovering the `200-mph` Jet Stream Over Tokyo (`Nov 1944 – Feb 1945`):** Moving to captured Saipan, Tinian, and Guam (`40,000` Seabees carving `8,500-foot` coral runways); high-altitude daylight precision raids hit an uncharted `180–230 mph` river of wind at `30,000 feet`, scattering `94%` of bombs off target while engine failures ditch crews in the Pacific.
  6. **`22:00–26:00` Chapter 5 — LeMay's Low-Altitude Gamble & Industrial Verdict (`March–Aug 1945`):** Stripping tail/turret guns and flying at `5,000–8,000 feet` at night to cut engine strain and fuel burn (`WHO: Curtis LeMay`), kept strictly factual and sober on civilian human cost without shock framing; how `3,970` B-29s ushered in modern pressurised aviation.
- **Primary Sources List:**
  1. Craven, Wesley Frank & Cate, James Lea, eds. (1953), *The Army Air Forces in World War II, Vol. V: The Pacific: Matterhorn to Nagasaki, June 1944 to August 1945*, Office of Air Force History (US federal public domain — exact `$3B` programme cost, engine loss rates, and Matterhorn fuel ratios).
  2. United States Strategic Bombing Survey (`USSBS`, 1946, NARA public domain), *Summary Report (Pacific War)* & *The Strategic Air Operation of Very Heavy Bombardment in the War Against Japan (Twentieth Air Force)*.
  3. Correll, John T. (Air Force Historical Foundation / USAF official records), & Knaack, Marcelle Size (1988), *Encyclopedia of U.S. Air Force Aircraft and Missile Systems, Vol. II: Post-World War II Bombers* (`B-29` `R-3350` modification directives and Wichita "Battle of Kansas" figures).
  4. Boeing Historical Archives / NARA `RG 342-FH` — *XB-29 Flight Test Accident Investigation Report (`41-2`, Seattle, 18 Feb 1943)*.
  5. Air Force Historical Research Agency (`AFHRA`) — *XXI Bomber Command Tactical Mission Reports (`Nov 1944 – Mar 1945`: jet-stream groundspeed & hit-percentage tables)*.
- **Picture Plan (`~265` cuts across `26:00`):**
  - **Archive stills & USAAF film (`~70%`, `~185` cuts):** `US NARA RG 342-FH` & `LoC FSA/OWI` (colour and B&W Boeing Wichita/Renton assembly lines, `XB-29` prototypes, `Wright R-3350` engine test cells, pressurised tunnel cutaways, Seabees building North Field Tinian, `20th Air Force` crews).
  - **Code-drawn maps & engineering graphics (`~30%`, `~80` cuts, `£0`):** (1) Cost comparison bar (`$3.0B` B-29 vs `$1.9B` Manhattan Project vs `$1.8B` US Navy Essex-class carriers); (2) Cross-section of B-29 pressurised cabins + `35-foot` crawl tunnel + remote gun sight lines; (3) `Operation Matterhorn` India-to-Chengdu-to-Kyushu `7:1` fuel pyramid vs Marianas (`Tinian` -> `Honshu` `1,500-mile` direct track); (4) `30,000-ft` `200-mph` jet-stream drift diagram showing `500-mph` groundspeed error; (5) Engine-overheat climb stress comparison (`30,000 ft` vs `7,000 ft`).
  - **Flow Veo (`0%` required):** 100% public-domain USAAF colour/B&W archive + code-drawn engineering diagrams (`£0`).

---

## 5. Studio Registration Steps (Listed Without Executing Yet)

Per `05_Analytics/kanban/board_site/studio_app.js` (`Channels → Add a channel`) and `scripts/channel_new.py` (`scripts/channel_ratchet.json` already reads `total: 0`, `home_total: 0`):

1. **You (Ben):** Pick one of the three verified channel names (`Field Order History @FieldOrderHistory`, `Gridline History @GridlineHistory`, or `Iron & Compass @IronAndCompass`) and lock your first pilot topics on the Studio board (`#plan`).
2. **Claude / Studio (done in `J2989`):** Channel folder (`channels/ww2/`), `studio/channel.json`, `studio/RULES.md`, and film folders `001`–`010` are built from `channels/_template/` and pass `python3 scripts/channel_check.py channels/ww2` (`0` must-fix).
3. **You (Ben):** Create the new YouTube **Brand Account** channel (separate from your personal channel), create its GitHub repository (`TheLaughingGod1986/<chosen-slug>`), sign in to its YouTube Studio on the Mac mini (dedicated CDP browser port, e.g. `9224`), and confirm `Ben Orbit Narrator` on the existing ElevenLabs plan.
4. **Claude / Studio (after Step 3):** Update `name`/`youtube.handle`/`repo.url`/`cadence` in `channels/ww2/studio/channel.json`, push `channels/ww2/` as `main` of the new GitHub repository, add `{"slug": "ww2", "env": "WW2_REPO", "checkouts": ["ww2"]}` to `channels/channels.json`, and run `python3 scripts/channels.py sync` + `python3 scripts/channel_check.py --all`.
5. **Claude / Studio (after Step 4):** Queue `WW2:001` script + US/UK archive provenance harvest (`£0`), then voice **at most two** `~25-min` pilot films (`WW2:001` and `WW2:002`, `~40k` chars total) before the ElevenLabs plan is upgraded or renews.
