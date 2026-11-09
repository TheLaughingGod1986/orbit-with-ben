# J1958 — `OWB:060` Hyperion Topic Neighbours, Competition & Audience Evidence Report (4 November 2026)

- **Job:** `J1958` (`060 Hyperion: verify topic neighbours and audience evidence`)
- **Film / Stage:** `OWB:060` (`02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge`, stage `topic`)
- **Worker:** `gemini` (Gemini 4 Argon High, specialist review worker on Mac mini)
- **Preceding Chief Rulings Inspected:**
  - `jobs/reviews/J1803/CHIEF_TOPIC_RULING_2026-11-04.md` (`FIX / topic not locked`)
  - `jobs/reviews/J1804/CHIEF_SCRIPT_RULING_2026-11-04.md` (`FIX — script not locked`)
  - `jobs/reviews/J1805/CHIEF_SOURCES_RULING_2026-11-04.md` (`FIX / sources not approved`)
- **Dependent Elected-Chief Job:** `J1960` (`060 Hyperion: combined topic/editorial and lock decision`, linked successor to `J1804`)
- **Linked Sources Verification Jobs (`J1805`):** `J1961` (formal Gemini `facts` via `agy`) → `J1962` (direct `MUST QUOTE` verification)
- **Spend:** **£0 / 0 credits** (no paid vidIQ API, no ElevenLabs, no Vertex/Flow generation, no YouTube/Studio writes)
- **Capabilities:** No `audio_input` or `moving_video_input` required or claimed (`chief_relay.py capabilities --agent gemini --available ''`)

---

## 1. Executive Recommendation to Dependent Chief Job (`J1960` / `J1804`)

**Recommendation: `DEFER` topic lock and script advancement for `OWB:060` Hyperion (retain `060` as an unlocked candidate with `topic: review/blocked` and `script: blocked`; allow already-queued no-spend diagnostics `J1961` Gemini `facts` and `J1962` direct quote check to complete as ordered by `J1805`, but DO NOT lock the topic/script, do not queue a v02 narration rewrite now, and do not advance to VO/picture production).**

### Why `DEFER` (and Neither `LOCK NOW` Nor `REJECT`)

1. **Public Neighbour Pool & Signed-Out Competition (`4/5` Medium-Strong — Do Not Reject, But Note Single-Topic Competitor Overlap):**
   - Historic `J0773` (`IDEAS_2026-10-21_J0773.md` and the 21 Oct `PRE_BUILD_VIDIQ_AUDIT.md`) used fabricated/grouped titles and unsourced view ranges (*"Astrum — Saturn's Strangest Moons: Hyperion, Iapetus & Pan (1.4M+)"*, *"SciShow Space — Why Hyperion Looks Like a Sponge (1.1M+)"*, *"SEA / NASA JPL — Cassini's Strangest Discoveries at Saturn (1M–3M+)"* — none of which exists on YouTube).
   - Independent `yt-dlp` verification on `2026-11-04 15:02–15:04 UTC` establishes **9 real education/space videos at `1.16M–9.28M` views** across the Hyperion, Cassini, and Saturnian-moons cluster:
     - **1 standalone single-topic Hyperion long >1M views:** `4ZnN44BTTjU` (**1,765,348 views**, Astrum *You Can’t Land on Saturn's Moon Hyperion*, uploaded `2026-08-13`, 17:37 / 1,057 s — 9 chapters covering the exact same 9-beat spine as `060` `v01`).
     - **2 Cassini Saturn / astronomy education longs >1.6M views covering Saturn's icy/other moons including Hyperion:** `qaRBmeYyHoc` (**3,845,815 views**, The Secrets of the Universe *Real Images From Saturn: What Cassini Actually Saw There*, Ch. 7 *Exploring icy moons* `07:12–08:22`, naming Hyperion in description) and `E8GNde5nCSg` (**1,647,588 views**, CrashCourse *Saturn: Crash Course Astronomy #18*, Ch. 8 *Saturn's Other Moons* `09:51–11:22`).
     - **6 sibling Saturnian-moon & Cassini education longs at `1.16M–9.28M` views:** `tyMbktsAScE` (**9,275,428 views**, Astrum *NASA Cassini's Final Images of Saturn Stunned Me*), `B7497mQRn2Y` (**2,073,749 views**, Astrum *Titan*), `PaMgAJ859oY` (**2,003,195 views**, Astrum Extra *The Weirdest Moons in the Solar System*), `UPE-t_9n7w4` (**1,410,153 views**, Astrum *Iapetus Is Currently Smashing Into Saturn's Rings*), `4lJB8ynBibI` (**1,352,641 views**, Astrum *We Finally Know Why Saturn's Moon Dione Cracked Open*), and `QAj9DANPZHU` (**1,158,482 views**, Astrum *We Found New Evidence of Life on Saturn's Moon Enceladus*).
     - Other dedicated Hyperion videos sit below 1M (`syLEQgfi99Q` **257,054 views** SciShow Space Ch. 4 *HYPERION*, `OG1TarXk0QA` **213,576 views** Curioso Universo, `NnN5e4QyN6A` **72,534 views** Dr. Becky).
   - Signed-out exact-title competition check shows **0 exact-title collisions**, though Astrum's `4ZnN44BTTjU` (`2026-08-13`, **1.77M views**) is a direct recent single-topic competitor covering the identical chapter progression.
2. **Strategy Short-First Prerequisite Is UNMET (`1/5` — Blocking Topic Lock):**
   - Under `FAMILIAR_DANGER_STRATEGY.md` (*Measure*: *"A new long is only made on a topic whose Short already cleared 200 views and 40% stayed"*) and `J1803` (*"Verify the strategy prerequisite of a Hyperion topic Short with at least 200 views and 40% stayed using actual id/date/analytics evidence. If absent, state unmet; do not create a Short. Saturn rings results and continuity promises in unlocked 059/061 drafts are not Hyperion topic approval."*), `OWB:060` requires a matching channel Short with **both `>=200` views AND `>=40%` stayed-to-watch**.
   - Verification of `05_Analytics/owb/snapshots/2026-11-04.json` (184 videos), `05_Analytics/owb/studio_ctr.json` (`2026-11-04T14:56:50Z`), `05_Analytics/owb/REPORT.md` (`2026-11-04`), `00_Brand/Channel-Setup/social/UPLOADS.json`, and `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md` confirms **0 OWB Shorts exist (public, private, or scheduled) on Hyperion, chaotic rotation, or porous moons**.
   - Furthermore, all 4 public Saturn Rings Shorts (`Cka7_TVVOUQ` **53 views / 33.3% stayed**, `lbW2iQ9YvqA` **12 views / 25.0% stayed**, `82Ao0v5XiQI` **91 views / 14.0% stayed**, `6dcL5rBmHPM` **45 views / 21.7% stayed**) missed both thresholds, and Titan Short `RLSJm59OSzI` is Private until `2026-11-10` with `0` views (and tests `032` Titan, not `060` Hyperion).
3. **Channel Balance, Pipeline Priority & Saturn/Moon Crowding:**
   - `python3 scripts/channel_balance.py --hos "/Users/benjaminoats/YouTube/History Of Science"` on `2026-11-04T15:05Z` reports **History of Science first**: HOS has **2/4 complete for 2026-11** (`[006 007 008* 009*]`, plus `010*` for 2026-12), whereas Orbit With Ben has **5/4 complete for 2026-11** (`[024 025 026 027 028]`) and **1/4 complete for 2026-12** (`[029]`), plus `030` Apophis in AR finishing (`J1471`/`J1356`) and `031`/`032` in VO listening review (`J1752`/`J1753`).
   - Within OWB, `060` is the **5th Saturn-system film** (`021` Rings, `032` Titan, `046` Enceladus, `050` Iapetus, `060` Hyperion) and **11th moon candidate**, and its Chapter 4 mechanism (`Phoebe` dark dust + thermal sublimation on crater floors) directly overlaps `050` Iapetus (`J1936`).
4. **Scientific (`J1805` → `J1961`/`J1962`) & Editorial (`J1804`) Prerequisites Remain Outstanding:**
   - Before any v02 rewrite or lock, `J1961` and `J1962` must verify the 16 `SOURCES.md` rows and resolve `J1805`'s 7 scientific flags (`410 × 260 × 220 km` diameters vs `180 × 133 × 103 km` radii mismatch in Row 1; Lyapunov instability timescale vs repeating `"30-day chaotic spin wobble"` in Rows 4–5; hypothetical proto-moon breakup & sublimation qualifiers vs `"proves"` in Rows 8 & 13; Wikipedia-only crater rows 10–11; albedo vs dust provenance & `−200 V` potential vs charge in Rows 12–14; exact identities of `PMID 39100574` and `PMID 42390330` in Row 15; missing `Nordheim` `WHO:` years in Row 7), alongside `J1804`'s editorial fixes (`<0:30` causal opening, trimmed spoken date/orbital inventories, single-idea `DATA:` graphics with `≤4`-word labels, `15–20 s` end-screen hold, and `v00` vs `v01` gate selection).

---

## 2. Individually Verified Education / Space Neighbours (`yt-dlp`, `2026-11-04 15:02–15:04 UTC`)

Channel names are internal notes only and must never appear in public listings (`STUDIO_PLAYBOOK.md` §2).

### A. Verified Education / Space Videos at ≥1M Views

| # | Views (`2026-11-04`) | Video ID & URL | Exact Title | Uploaded · Length | Channel (internal) | Coverage & Shared Subject Words |
|---|---------------------:|----------------|-------------|-------------------|--------------------|---------------------------------|
| 1 | **1,765,348** | `4ZnN44BTTjU` (`https://www.youtube.com/watch?v=4ZnN44BTTjU`) | *You Can’t Land on Saturn's Moon Hyperion* | 2026-08-13 · 17:37 (1,057 s) | Astrum (2.90M subs) | **Direct single-topic Hyperion long.** 9 chapters (*Hyperion*, *Discovery of Hyperion*, *It’s Empty*, *How Did It Form?*, *Spongy Surface*, *Irregular Orbit*, *Unpredictable Spin*, *Complex Chemistry*, *Hyperion Zapped Cassini*). Words: `Saturn's moon Hyperion`, `weirdest object in the solar system`, `spongy surface`, `mostly empty interior`, `chaotic motion`, `electric shocks`, `Cassini`. |
| 2 | **3,845,815** | `qaRBmeYyHoc` (`https://www.youtube.com/watch?v=qaRBmeYyHoc`) | *Real Images From Saturn: What Cassini Actually Saw There* | 2021-11-09 · 11:28 (688 s) | The Secrets of the Universe (1.79M subs) | **Direct Cassini Saturn & icy moons education long.** Chapter 7 *Exploring icy moons* (`07:12–08:22`) and description explicitly highlight Cassini's discoveries at **Hyperion** alongside Titan, Dione, Enceladus, Rhea, Iapetus, and Phoebe. Words: `real images from Saturn`, `Cassini`, `Saturn and its moons`, `exploring icy moons`, `Hyperion`. |
| 3 | **1,647,588** | `E8GNde5nCSg` (`https://www.youtube.com/watch?v=E8GNde5nCSg`) | *Saturn: Crash Course Astronomy #18* | 2015-05-21 · 12:16 (736 s) | CrashCourse (17.3M subs) | **Direct Saturn & Saturnian moons education long.** Chapter 6 *Titan* (`06:31–08:34`), Chapter 7 *Enceladus* (`08:34–09:51`), Chapter 8 *Saturn's Other Moons* (`09:51–11:22`). Words: `Saturn`, `Saturn's moons`, `Saturn's other moons`, `Titan`, `Enceladus`, `ice particles`. |
| 4 | **2,003,195** | `PaMgAJ859oY` (`https://www.youtube.com/watch?v=PaMgAJ859oY`) | *The Weirdest Moons in the Solar System* | 2025-03-13 · 1:51:29 (6,689 s) | Astrum Extra (329k subs) | **Direct strange-moons education compilation** covering Saturn's moons (`Rhea`, `Titan`, `Enceladus`) alongside Jupiter, Uranus, and Neptune moons. Words: `weirdest moons in the solar system`, `Saturn's moons`, `solar system`, `moons`. |
| 5 | **2,073,749** | `B7497mQRn2Y` (`https://www.youtube.com/watch?v=B7497mQRn2Y`) | *The Bizarre Characteristics of Titan \| Our Solar System's Moons: Titan* | 2019-01-11 · 18:49 (1,129 s) | Astrum (2.90M subs) | **Direct Saturnian moon long (Titan)**, whose gravity locks Hyperion into its 3:4 orbital resonance. Words: `Saturn's moons`, `Titan`, `our solar system's moons`. |
| 6 | **1,410,153** | `UPE-t_9n7w4` (`https://www.youtube.com/watch?v=UPE-t_9n7w4`) | *Iapetus Is Currently Smashing Into Saturn's Rings* | 2025-05-08 · 22:50 (1,370 s) | Astrum (2.90M subs) | **Direct sibling Saturnian moon long (Iapetus)** covering Cassini's discovery, physical characteristics, and dark/bright albedo contrast. Words: `Saturn's moon`, `Iapetus`, `Cassini's discovery`, `physical characteristics`. |
| 7 | **1,352,641** | `4lJB8ynBibI` (`https://www.youtube.com/watch?v=4lJB8ynBibI`) | *We Finally Know Why Saturn's Moon Dione Cracked Open* | 2025-04-10 · 17:21 (1,041 s) | Astrum (2.90M subs) | **Direct sibling Saturnian icy-moon long (Dione).** Words: `Saturn's moon`, `Voyager era`, `Cassini revolution`, `icy crust`, `craters`. |
| 8 | **1,158,482** | `QAj9DANPZHU` (`https://www.youtube.com/watch?v=QAj9DANPZHU`) | *We Found New Evidence of Life on Saturn's Moon Enceladus* | 2026-04-08 · 21:29 (1,289 s) | Astrum (2.90M subs) | **Direct sibling Saturnian icy-moon long (Enceladus).** Words: `Saturn's moon`, `Enceladus`, `Cassini`, `first images`. |
| 9 | **9,275,428** | `tyMbktsAScE` (`https://www.youtube.com/watch?v=tyMbktsAScE`) | *NASA Cassini's Final Images of Saturn Stunned Me* | 2020-06-16 · 10:23 (623 s) | Astrum (2.90M subs) | **Direct Cassini mission flagship** (`hxgdjbi2MTU` supercut at **2,498,801 views**; NASA JPL `SY-hQJ5pMd4` at **1,916,654 views**). Words: `Cassini`, `NASA Cassini`, `Saturn`, `final images of Saturn`. |

### B. Dedicated Sub-1M Hyperion & Saturnian Moons Education Videos (`64k–933k` views)

- **`ce-AkRewzdo` (`https://www.youtube.com/watch?v=ce-AkRewzdo`)** — *Something Is Wrong With Saturn's Moon Rhea* · **933,051 views** (2024-12-29, 15:38, Astrum).
- **`_yaX8HqYSI8` (`https://www.youtube.com/watch?v=_yaX8HqYSI8`)** — *The Moon That Should Have Been a Planet \| Phoebe* · **727,174 views** (2026-02-18, 16:46, Astrum — outer irregular moon Phoebe).
- **`CYxdXkB3BKY` (`https://www.youtube.com/watch?v=CYxdXkB3BKY`)** — *What We Found on the Icy Moons of Saturn* · **719,992 views** (2025-12-03, 1:45:26, Astrum Extra).
- **`FHtd05wfNRQ` (`https://www.youtube.com/watch?v=FHtd05wfNRQ`)** — *Saturn's Death Star Moon Has a Surprising Secret* · **683,022 views** (2026-05-06, 21:08, Astrum — Mimas).
- **`4JU4417x2p8` (`https://www.youtube.com/watch?v=4JU4417x2p8`)** — *Zooming Into Strangest Moons in Our Solar System* · **467,154 views** (2026-10-17, 8:53, cjushal).
- **`J8eZTDVOEWk` (`https://www.youtube.com/watch?v=J8eZTDVOEWk`)** — *10 Strange Moons of the Solar System* · **265,001 views** (2019-09-30, 16:55, John Michael Godier).
- **`syLEQgfi99Q` (`https://www.youtube.com/watch?v=syLEQgfi99Q`)** — *3 of the Strangest Moons in the Solar System* · **257,054 views** (2017-04-25, 4:21, SciShow Space, Chapter 4 `02:40–03:44` *HYPERION* — refutes `J0773`'s unsupported `1.1M+` *Why Hyperion Looks Like a Sponge* claim).
- **`OG1TarXk0QA` (`https://www.youtube.com/watch?v=OG1TarXk0QA`)** — *Hyperion attacked the Cassini probe — and we caught it on tape!* (`Hipérion atacou a sonda Cassini — e nós registramos isso!`) · **213,576 views** (2026-09-13, 10:36, Curioso Universo — dedicated single-topic Hyperion long).
- **`NnN5e4QyN6A` (`https://www.youtube.com/watch?v=NnN5e4QyN6A`)** — *Saturn's spongey moon Hyperion \| Space is Weird* · **72,534 views** (2020-07-08, 13:13, Dr. Becky — dedicated single-topic Hyperion astrophysicist explainer citing Thomas et al. 2007 *Nature*).
- **`U5VfYDYL3rA` (`https://www.youtube.com/watch?v=U5VfYDYL3rA`)** — *Hyperion Flyby (moon of Saturn) 2010 - Colorized* · **64,574 views** (2010-12-01, 0:25, Ian Regan).

---

## 3. Updated Artifacts & Preserved Draft Integrity

### Updated / Created in `J1958`
1. `02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (created from `00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md` with verified `2026-11-04` Tier A/B neighbour tables, refutation of unsupported `J0773` claims, Short-first analytics check, Saturn/moon overlap matrix, and explicit `DEFER` recommendation to `J1960`).
2. `02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (repaired: unsupported historic `J0773` vidIQ scores `96`/`95`/`93` and `High`/`Med`/`Low` labels marked `UNKNOWN`; grouped/fabricated placeholder neighbours replaced with individually verified URLs/views; signed-out exact-title competition table and `4ZnN44BTTjU` single-topic overlap added; `J1803`, `J1804` & `J1805` fixes mapped into Section 5; Section 7 left UNSIGNED).
3. `02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/11_Upload-Package/PRODUCTION_CHECKLIST_V2.md` (refreshed obsolete AI Studio / `8–9 min` template lines to current Vertex-only, `7–9 min`, `15–20 s` end-hold, and `J1803`/`J1804`/`J1805` gate requirements).

### Preserved Untouched (Verified SHA-256 Hashes)
- `8e7da06fdb792c2cbae88b054fe20cd7db192e2a20fbd844e84699f44ab760fd  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/SCRIPT_NOTES_v00.md`
- `1513042ce8a10f4e8aea7df4d893b50d4fd70cde9e101e641159070b233f5288  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/SCRIPT_NOTES_v01.md`
- `c8e304bca5962bfbb4d81a4931286ed5882842063d3796984598843eafdb1294  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/SOURCES.md`
- `d6ddbf1b9ed0dbfbee6556e1c9f6537dba7ad883a425435ac133965528ad55c2  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/episode_script_draft_v01.md`
- `b8faab0602c50ce129aca8ad1dd896d8d38fa5ef92a630cdc052431471f9666b  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/hyperion_sponge_script_master_v00.md`
- `d6ddbf1b9ed0dbfbee6556e1c9f6537dba7ad883a425435ac133965528ad55c2  02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/hyperion_sponge_script_master_v01.md`
