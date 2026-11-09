# J2006 — `OWB:048` Ceres Topic, Neighbour, Demand, Overlap & Short-First Evidence Report (4 November 2026)

- **Job:** `J2006` (`048 Ceres: verify neighbour, demand and Short-first evidence`)
- **Film / Stage:** `OWB:048` (`02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt`, stage `topic`)
- **Worker:** `gemini` (Gemini 4 Argon High, specialist review fallback after `J1934`)
- **Preceding Chief Ruling:** `jobs/reviews/J1934/DECISION_2026-11-04.md` (`DEFER topic lock; script FIX / blocked from lock and production`)
- **Dependent Chief Job:** `J2007` (`048 Ceres: decide capacity and advancement after topic evidence`)
- **Spend:** **£0 / 0 credits** (no paid vidIQ API, no ElevenLabs, no Vertex/Flow generation, no YouTube/Studio writes)

---

## 1. Executive Recommendation to Dependent Chief Job (`J2007`)

**Recommendation: `DEFER` `OWB:048` Ceres (retain as an unlocked candidate with `topic: blocked` and `script: blocked`; DO NOT advance to script v02 rewrite, formal Gemini `facts` pass, direct quote check, or VO/production at this time).**

### Why `DEFER` (and Neither `ADVANCE` Nor `REJECT`)

1. **Short-First Prerequisite FAILS (`1/5` — Blocking):**
   - Under `FAMILIAR_DANGER_STRATEGY.md` (*Measure*: *"A new long is only made on a topic whose Short already cleared 200 views and 40% stayed"*) and `jobs/reviews/J1934/DECISION_2026-11-04.md` (*"Demand/audit and Short-first evidence remain prerequisites either way. ... No waiver is granted. ... No new Short production is authorised"*), a matching channel Short requires **both `>=200` views AND `>=40%` stayed-to-watch** (not average % viewed).
   - Verification of `05_Analytics/owb/snapshots/2026-11-04.json` (184 videos), `05_Analytics/owb/studio_ctr.json` (`2026-11-03T07:03:36Z`), `05_Analytics/owb/REPORT.md` (`2026-11-04`), and `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md` confirms **0 channel Shorts exist (public, private, or scheduled) on Ceres, Dawn, Occator Crater, or Ahuna Mons**.
   - Even adjacent asteroid or icy-world Shorts on the channel fail the `>=200` views + `>=40%` stayed-to-watch bar:
     - `gJwNJN_yMKU` (*How Close Will Asteroid Apophis Pass Earth on Friday the 13th?*): **458 public views (457 Studio)**, **34.2% stayed-to-watch** (`MISS <40%`; 233.3% average viewed does not substitute for stayed-to-watch).
     - `pII09FbRYGc` (*Why Europa Is Hiding a Massive Ocean*): **291 views**, **16.7% stayed-to-watch** (`MISS <40%`).
     - `keXe1GNxWSU` (*Those Ice Scars Are How You Find It*, Europa): **206 views**, **15.8% stayed-to-watch** (`MISS <40%`).
     - `1glQuYFSaYQ` (*What Would Life Eat Under Europa?*): **127 views (`<200`)**, **20.9% stayed-to-watch**.
     - `VE0f186WQZo` (*Europa Sprays Its Ocean Into Space*): **91 views (`<200`)**, **45.7% stayed-to-watch**.
     - `8Bym-yrYhGc` (*Why Europa's Ocean Shouldn't Exist*): **26 views (`<200`)**, **68.0% stayed-to-watch**.
   - As J1934 ruled, `006` Europa long retention (`NbW5G1BpPY0`, 15 views, 22.9% AVD in the 18 Oct weekly audit) and `"space ice"` 28-day search terms (2 views) do **not** establish Ceres Short performance.
2. **Channel Balance & Capacity Trigger from `J1934` Is Unmet:**
   - `python3 scripts/channel_balance.py --hos "/Users/benjaminoats/YouTube/History Of Science"` on `2026-11-04T10:29Z` reports **History of Science first**: HOS has **2/4 complete for 2026-11** (`[006 007 008* 009*]`, plus `010*` for 2026-12), whereas Orbit With Ben has **5/4 complete for 2026-11** (`[024 025 026 027 028]`) and **1/4 complete for 2026-12** (`[029]`), plus `030` Apophis in AR finishing and `031`/`032` in VO listening review.
   - Furthermore, several unlocked OWB candidates ahead of `048` already have dedicated standalone Shorts in the `24 Oct – 17 Nov 2026` test cohort (`033` Uranus `ZpEA8stoSPA` at 461 day-1 views, `032` Titan `RLSJm59OSzI`, `034` Pluto `gmzaCfJF1gA`, `038` Voyager `kKN8Ale42sE`), whereas `048` Ceres has none.
3. **Why Retain as Unlocked Candidate (`DEFER`) Rather Than `REJECT`:**
   - Public YouTube demand is real and current: Astrum's *Dawn* Ceres/Vesta supercut (`0w6KRajHMlo`) has **2,957,410 views**, NASA JPL's *Flight Over Dwarf Planet Ceres* (`nJiw2NxqoBU`) has **1,383,924 views**, CrashCourse's *Asteroids #20* covering Ceres (`auxpcdQimCs`) has **1,337,561 views**, Free School's and SciShow Kids' dwarf-planet explainers naming/covering Ceres (`OGiEkHZZrIs`, `evIsmxM5c7o`) have **1,923,830** and **1,591,061 views**, SEA's *Dwarf Planets: The Lesser Worlds* (`SOxAkOOqpKU`, Ch. 3 *Ceres*) has **942,301 views**, Astrum's dedicated 10-minute Ceres *Dawn* long (`13eztn3RxQw`) has **824,012 views**, and V101 SPACE's recent 17 Oct 2025 Ceres long (`7glhGmoneQo`) reached **543,061 views in 18 days**.
   - Signed-out exact-title competition check shows **0 collisions** on YouTube.
   - Deferring preserves `01_Script/ceres_salt_domes_script_master_v00.md`, `v01.md`, `SCRIPT_NOTES_v01.md`, and `SOURCES.md` intact until HOS November reaches 4 completed films and Chief either tests a Ceres Short or records a specific capacity rationale.

---

## 2. Verified Education / Space Neighbours (`yt-dlp`, `2026-11-04 10:23–10:25 UTC`)

Channel names are internal notes only and never appear in public listings (`STUDIO_PLAYBOOK.md` §2).

### A. Direct Ceres / Dawn & Dwarf-Planet / Asteroid-Belt Education Videos at ≈1M+ Views

| # | Views (`2026-11-04`) | Video ID & URL | Title | Uploaded · Length | Channel (internal) | Coverage & Shared Subject Words |
|---|---------------------:|----------------|-------|-------------------|--------------------|---------------------------------|
| 1 | **2,957,410** | `0w6KRajHMlo` (`https://www.youtube.com/watch?v=0w6KRajHMlo`) | *What NASA's Dawn Saw on Ceres and Vesta Stunned Me \| Supercut* | 2022-04-01 · 20:17 (1,217 s) | Astrum (2.90M subs) | **Direct Ceres + Dawn mission long.** Full recap of NASA's *Dawn* probe at 4 Vesta and dwarf planet Ceres, Occator Crater bright spots, and Ahuna Mons. Words: `Ceres`, `Dawn`, `NASA Dawn mission`, `Vesta`, `what did Dawn discover`, `dwarf planet`, `protoplanet`, `mission to Ceres`. |
| 2 | **1,383,924** | `nJiw2NxqoBU` (`https://www.youtube.com/watch?v=nJiw2NxqoBU`) | *Flight Over Dwarf Planet Ceres* | 2016-01-29 · 3:44 (224 s) | NASA Jet Propulsion Laboratory (1.25M subs) | **Direct Ceres + Occator + Ahuna Mons official visual piece.** DLR/JPL simulated flyover built from *Dawn* images over Occator Crater bright spots and Ahuna Mons. Words: `dwarf planet Ceres`, `Ceres`, `NASA`, `Dawn spacecraft`, `Occator Crater`, `bright spots`. |
| 3 | **1,337,561** | `auxpcdQimCs` (`https://www.youtube.com/watch?v=auxpcdQimCs`) | *Asteroids: Crash Course Astronomy #20* | 2015-06-04 · 11:33 (693 s) | CrashCourse (17.3M subs) | **Direct Asteroid Belt + Ceres education long.** Covers Piazzi's 1801 discovery of Ceres, asteroid-belt mass share, Vesta, and *Dawn*. Words: `asteroid belt`, `Ceres`, `asteroids`, `Vesta`, `dwarf planet`. |
| 4 | **1,923,830** | `OGiEkHZZrIs` (`https://www.youtube.com/watch?v=OGiEkHZZrIs`) | *Guide to Dwarf Planets: Ceres, Pluto, Eris, Haumea and Makemake for Kids - FreeSchool* | 2017-02-15 · 8:53 (533 s) | Free School (906k subs) | **Dwarf planets explainer naming Ceres in title.** Covers 2006 IAU classification, Ceres in the asteroid belt, and *Dawn*. Words: `dwarf planet`, `dwarf planets`, `Ceres`, `Ceres facts`, `Pluto`, `Eris`. |
| 5 | **1,591,061** | `evIsmxM5c7o` (`https://www.youtube.com/watch?v=evIsmxM5c7o`) | *Meet the 5 Dwarf Planets!* | 2015-07-01 · 4:33 (273 s) | SciShow Kids (1.73M subs) | **Dwarf planets education explainer.** Covers Ceres in the asteroid belt alongside Pluto, Eris, Haumea, and Makemake. Words: `dwarf planets`, `Ceres`, `solar system`. |
| 6 | **942,301** *(≈0.94M)* | `SOxAkOOqpKU` (`https://www.youtube.com/watch?v=SOxAkOOqpKU`) | *Dwarf Planets: The Lesser Worlds* | 2020-12-19 · 27:59 (1,679 s) | SEA (782k subs) | **Space-documentary long (~1M views) with dedicated Chapter 3 (`05:34–09:15`, *Ceres*).** Words: `dwarf planets`, `minor planets`, `Ceres`, `icy worlds`, `solar system`. |

### B. Dedicated Ceres / Dawn / Occator Crater / Ahuna Mons Videos Below 1M (115k–824k)

- **`13eztn3RxQw` (`https://www.youtube.com/watch?v=13eztn3RxQw`)** — *The Discoveries On Ceres That Shocked NASA Scientists \| Dawn Mission* · **824,012 views** (2019-12-14, 10:00, Astrum). Closest single-topic 10-min Ceres/Dawn peer (`ceres`, `dawn`, `nasa dawn`, `nasa ceres`, `what did dawn discover`).
- **`R1OICuZtypk` (`https://www.youtube.com/watch?v=R1OICuZtypk`)** — *The Great Secret of the Smallest Worlds in Our Solar System* · **824,008 views** (2025-04-24, 1:09:10, Astrum Extra). Planetesimals compilation featuring *Dawn* at Ceres and Vesta.
- **`7glhGmoneQo` (`https://www.youtube.com/watch?v=7glhGmoneQo`)** — *The "Forgotten" Dwarf Planet Between Mars and Jupiter: What NASA Found on Ceres* · **543,061 views** (2025-10-17, 10:48, V101 SPACE). Recent 18-day breakout (`ceres dwarf planet`, `nasa ceres mission`, `dawn spacecraft`, `asteroid belt`, `dwarf planet between mars and jupiter`, `ceres water`).
- **`8er_0yY1S1o` (`https://www.youtube.com/watch?v=8er_0yY1S1o`)** — *Ceres Rotation and Occator Crater* · **315,459 views** (2015-12-09, 1:13, NASA JPL).
- **`6V3WehjinAc` (`https://www.youtube.com/watch?v=6V3WehjinAc`)** — *Could Ceres be Home to Life? [OOTW]* · **284,508 views** (2018-12-31, 11:53, SEA).
- **`KyHG3IQZQMM` (`https://www.youtube.com/watch?v=KyHG3IQZQMM`)** — *The Forgotten Dwarf Planet Ceres* · **257,616 views** (2023-01-02, 8:50, Insane Curiosity).
- **`Fs3fODU9P0w` (`https://www.youtube.com/watch?v=Fs3fODU9P0w`)** — *Neil deGrasse Tyson: What Is The Bright Spot on Ceres?* · **124,751 views** (2016-06-10, 2:08, StarTalk).
- **`ZVBHclVvJ7s` (`https://www.youtube.com/watch?v=ZVBHclVvJ7s`)** — *Surprising New Findings Inside a Crater on Ceres* · **114,912 views** (2020-08-26, 12:46, Anton Petrov — covers the Aug 10, 2020 *Nature* Occator brine reservoir papers).
- **Off-lane / kids exclusions noted:** `8VB-jfqrtM4` (Ridddle, 5.70M, *What If The Largest Asteroid Hit Earth?*, Ch. 6 *The dwarf planet Ceres*) and `7_sVAcX-ueE` (What If, 1.93M, *What If the Largest Asteroid Hit Earth? It's Nearly 600 Miles Wide*, Ch. 7 *Ceres*) use off-lane Earth-impact disaster hooks; kids songs (`4tw_RiQp6H8` 95.8M, `ws3kWuMi0Y8` 60.2M, `PCJO5DREJKo` 4.95M) and cartoons (`fxpnvoR1w3g` 4.67M) are excluded.

**Neighbour Verdict:** **Medium / Borderline (`3/5`).** Two direct Ceres/Dawn videos exceed 1M (`2.96M`, `1.38M`) and four multi-object education peers covering Ceres sit at `0.94M–1.92M` (plus `824k` and `543k` dedicated Ceres longs), but no standalone video solely about Occator Crater's bright spots or Ahuna Mons has crossed 1M views.

---

## 3. Overlap Assessment (`006`, `030`, `034`, `046`, `049` & Channel Inventory `001`–`061`)

- **`006` Europa (`NbW5G1BpPY0`, public live 2026-09-03, 15 views):** Shares subsurface salty ocean + astrobiology themes. `048` differentiates via Ceres's **lack of giant-planet tidal heating**, focusing on **freezing-point-depressed relict brine (`~25 mi` deep)**, sodium carbonate evaporite domes in `Occator Crater`, and `2.5–4 Ga` radiogenic core heating.
- **`030` Apophis (locked, AR cohort `J1471`/`J1356`):** Low mechanism overlap (2029 near-Earth planetary-defence flyby vs main-belt dwarf planet cryovolcanism/brine), though both touch the broad "asteroid" search cluster.
- **`034` Pluto (unlocked candidate, blocked `J1971`/`J1972`):** Moderate structural overlap — both are **2015 NASA dwarf-planet encounters** (`Dawn` at Ceres in Mar 2015 vs `New Horizons` at Pluto in Jul 2015) explaining young, crater-erasing surface geology (`Occator`/`Ahuna Mons` vs `Sputnik Planitia`). Pluto already has a scheduled standalone Short (`gmzaCfJF1gA`, airing 14 Nov 2026), whereas Ceres has none.
- **`046` Enceladus (unlocked candidate, blocked `J1930`/`J2001`/`J2002`):** Moderate-to-high chemical overlap (subsurface brine, carbonate/chloride salts, hydrothermal chemistry, and water vapour plumes).
- **`049` Bennu (unlocked candidate, script in review `J1935`):** Moderate overlap on carbonaceous main-belt asteroid chemistry and ancient hydrothermal brine alteration (`OSIRIS-REx` magnesium-sodium phosphate & serpentine clay). Incoming `047` (*Great Red Spot Shrinking*, blocked `J2003`/`J2004`) promises `048` Ceres, and `048` v01 promises `049` Bennu in both its `[SUBSCRIBE BEAT]` (line 40) and closing hand-off (line 90). **Per J1934, both `047` and `049` are unlocked draft promises, not schedule commitments.**
- **Broader `001`–`061` pipeline:** Heavy concentration of icy-world/asteroid candidates (`006`, `030`, `032`, `034`, `035`, `036`, `040`, `044`, `046`, `048`, `049`, `050`, `051`, `052`, `057`, `060`), reinforcing the recommendation to defer `048` until candidates with scheduled Shorts are read out.

---

## 4. Updated Artifacts & Preserved Draft Integrity

### Updated in `J2006`
1. `02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (created with full 30-point J0590 verification, 10-point breakdown, Tiers A/B/C dated neighbour tables, Short-first verification, overlap matrix, and `DEFER` recommendation).
2. `02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (completed with dated evidence, unavailable paid vidIQ fields explicitly marked `UNKNOWN`, Section `2b` neighbour pass added, exact-title competition check, J1934's 5 mandatory v02 fixes mapped into Section 5, refreshed current studio rules, and Section 7 left UNSIGNED so `gate:episode` continues to block VO/Veo until Chief lock).
3. `02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/11_Upload-Package/PRODUCTION_CHECKLIST_V2.md` (refreshed obsolete AI Studio / burned-in subscribe / `/go/` affiliate template instructions to current `AGENTS.md` locks).

### Preserved Untouched (Verified SHA-256 Matching `jobs/reviews/J1934/INPUT_SHA256SUMS.txt`)
- `cfe5d5329c2fa39fb9d98c6d62d023228a63c2a51ef5358d070ad1a0a89604ed  02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/01_Script/ceres_salt_domes_script_master_v01.md`
- `d07969fe209c87407c9d48d45496c7b8892fdca2dc9cca3dd5df11aeeb5e41d3  02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/01_Script/SOURCES.md`
- `5854d028689bfab278e815e548a6bccbda01abe43ab82ab4ab5404f33629d03f  02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/01_Script/SCRIPT_NOTES_v01.md`
- `14bf3aec63d44e9762c5bfd9caaa7d5f01019f967178ab6e1113966b8cd3a619  02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/01_Script/ceres_salt_domes_script_master_v00.md`
