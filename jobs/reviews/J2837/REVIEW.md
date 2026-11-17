# `J2837` — Rule-E Topic Go/No-Go Review: `HOS:107` (Autumn Leaves / Chromatography) & `HOS:106` (Eels)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J2837` · `macbook` (`gemini-argon` / `gemini-agy`, `review` lane; companion to `J2836`) |
| **Target Proposals (`J2835`)** | **`HOS:107`** (`02_Video-Projects/107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll`, primary board target of `J2837`) & **`HOS:106`** (`02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso`, primary board target of `J2836`) |
| **Source PRs (`J2835`)** | HOS PR [`#588`](https://github.com/TheLaughingGod1986/history-of-science/pull/588) (`claudecode/J2835-hos-topics-106-107`) · OWB PR [`#930`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/930) (`claudecode/J2835-wip`) |
| **Review Deliverables (`J2837` & `J2836`)** | HOS PR [`#591`](https://github.com/TheLaughingGod1986/history-of-science/pull/591) (`macbook/J2837`, isolated to `107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll`) · HOS PR [`#589`](https://github.com/TheLaughingGod1986/history-of-science/pull/589) (`macbook/J2836`, isolated to `106_Aristotle-Freud-Schmidt-Eels-Sargasso`) · OWB PR [`#931`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/931) (`macbook/J2836`) · `jobs/reviews/J2837/REVIEW.md` (this file) · `jobs/reviews/J2837/evidence_2026-11-14_public_search_107.json` · `jobs/reviews/J2837/evidence_2026-11-14_public_search_106.json` |
| **Rule-E Verdict — `HOS:107` (Autumn Leaves)** | **GO (`90 / 100` · `9.00 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` behind `HOS:106` (`Why Do Leaves Change Colour? (A Chalk Tube Showed Why)`, `54` chars, `0` collisions; recommended late-August / September seasonal release window) |
| **Rule-E Verdict — `HOS:106` (Eels)** | **GO (`94 / 100` · `9.40 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` ahead of `HOS:107` under Rule G (`Where Do Eels Come From? (The Sargasso Sea Hunt)`, `48` chars, `0` collisions) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` has `4 / 4` HOS slots full (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). Every name, date, and number in `TOPIC.md` §2 for both `107` and `106` is **UNVERIFIED** (`written from memory`) and requires an exact primary-source quote in `SOURCES.md` verified by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens. |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Summary & Rulings on Open Points

Both History of Science topic proposals from `J2835` (HOS PR [`#588`](https://github.com/TheLaughingGod1986/history-of-science/pull/588), OWB PR [`#930`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/930)) pass the `AGENTS.md` Rule-E rubric after gathering the missing signed-out YouTube GB `public_search.py` autocomplete and title-collision evidence (`13` queries for `107`, `11` queries for `106`) and disambiguating title collisions caught in the raw search pulls.

- **Clean branch split across `J2836` and `J2837`:** Because `J2835` queued two companion review jobs (`J2836` for `HOS:106` and `J2837` for `HOS:107`) with the same two-film brief, `J2836` delivered the HOS review package for `106_Aristotle-Freud-Schmidt-Eels-Sargasso` on HOS PR [`#589`](https://github.com/TheLaughingGod1986/history-of-science/pull/589), and this job (`J2837`) delivers the complete HOS review package for `107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll` on HOS PR [`#591`](https://github.com/TheLaughingGod1986/history-of-science/pull/591) (`TOPIC.md`, `status.json`, `production-status.md`, `README.md`, `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, and `11_Upload-Package/evidence_2026-11-14_public_search.json`) so `#589` and `#591` can merge in either order with zero file conflicts.

### Why `public_search.py` Failed in `J2835` and How the Evidence Was Gathered
- **Root cause:** `00_Brand/Channel-Setup/tools/neighbours.py` wraps `public_search.search()` in `search_retry(q, top, tries=3)` with `2–4 s` backoff, whereas `public_search.py` calls `search()` once with no retry. When `J2835` ran `public_search.py` immediately after two 12-query `neighbours.py` runs from the same IP, YouTube served a transient response without `var ytInitialData =` and `public_search.py` exited on the first miss.
- **Resolution (`£0.00`):** Running `00_Brand/Channel-Setup/tools/public_search.py` on the MacBook retrieved full signed-out YouTube GB `suggest` and `search` arrays (`8` top results per query) for all `13` queries on `HOS:107` and all `11` queries on `HOS:106`. Both raw JSON files are committed in `jobs/reviews/J2837/`, in `02_Video-Projects/107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll/11_Upload-Package/evidence_2026-11-14_public_search.json` on HOS PR [`#591`](https://github.com/TheLaughingGod1986/history-of-science/pull/591), and in `02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso/11_Upload-Package/evidence_2026-11-14_public_search.json` on HOS PR [`#589`](https://github.com/TheLaughingGod1986/history-of-science/pull/589).

### Ruling on Open Point 1 (`HOS:107`): Seasonal Search Peak & Lack of an On-Subject `TED-Ed` Film Over `1M`
- **Ruling: `GO` (`90 / 100`), placed behind `HOS:106` in `next_hos` (target late-August / September release window) and bridged with year-round GCSE/AP Chemistry chromatography search.**
  1. **Lack of an on-subject `TED-Ed` film over `1M` (`PASS` under `studio/RULES.md` line 45):**
     - `history-of-science/studio/RULES.md` line 45 and `neighbours.py` lines 21–22 specify: **`≥ 3` education videos with `1M+` views on the topic (`TED-Ed`, `Kurzgesagt`, `Khan Academy`, `SciShow`, `Veritasium`, `Crash Course`, etc.; `TED-Ed`/`TED` preferred).**
     - In `107`'s `evidence_2026-11-14_neighbours.json`, the two `TED-Ed` hits (`gKfjHTk8KrY` *History's deadliest colors* `8.46M` and `UZ5UGnU7oOI` *What is color?* `1.11M`) matched on general colour, while `006_Trees-Are-Made-Of-Air` already holds the adjacent `TED-Ed` plant/chlorophyll neighbour `eo5XndJaz-Y` (*The simple story of photosynthesis and food*, **`2,218,164` views**).
     - Across the two halves of `HOS:107` (autumn leaf colour + Mikhail Tswett's 1903 chromatography discovery), `neighbours.py` and `public_search.py` confirm **5 directly on-subject education videos over `1,000,000` views**:
       1. **SciShow Kids** [`xB2DiiAOpCg`](https://youtu.be/xB2DiiAOpCg) — *The Science of Fall | Compilation | SciShow Kids* (**`1,916,547` views**, Tier 2)
       2. **SciShow Kids** [`Xk4-6II8l5Q`](https://youtu.be/Xk4-6II8l5Q) — *Why Do Leaves Change Colors in the Fall? | Biology for Kids* (**`1,850,237` views**, Tier 2)
       3. **MinuteEarth** [`JWva5AaDkXw`](https://youtu.be/JWva5AaDkXw) — *The Real Reason Leaves Change Color In the Fall* (**`1,558,957` views**, Tier 2)
       4. **Cognito** [`TdJ57SQ6GAQ`](https://youtu.be/TdJ57SQ6GAQ) — *GCSE Chemistry - Paper Chromatography* (**`1,532,859` views**, Tier 2 in `neighbours.py` line 43)
       5. **Khan Academy (`khanacademymedicine`)** [`SnbXQTTHGs4`](https://youtu.be/SnbXQTTHGs4) — *Basics of chromatography | Chemical processes | MCAT | Khan Academy* (**`1,328,589` views**, Tier 2)
       *(Plus `It's AumSum Time` `PvHvx7k7UPU` *Chromatography* at `2,116,418` views, `Free School` `UuTrDnzmMxY` at `388,111` views, `Chemistorian` `nVy5jC0-xYk` at `319,708` views, `Mystery Science` `Vi1EGjqocbY` at `308,037` views, `FuseSchool` `ByJ6lzD2Vbg` at `300,327` views, and `SciShow` `rwA1QVsbD6g` at `269,611` views.)*
  2. **Seasonal search peak (`September–November`):**
     - While `"why do leaves change colour"` / `"why do leaves change color in the fall"` peaks in September–November (and top leaf-colour results skew toward younger school audiences like `SciShow Kids` and `Super Simple Songs`), the second half of `107`'s hook — **chromatography** (`"what is chromatography"`, `"chlorophyll"`, `Cognito` `1.53M`, `Khan Academy` `1.33M`) — is a **year-round GCSE / AP Chemistry / MCAT curriculum staple** that serves adult and secondary-school viewers (`LEARNINGS.md` Rule 28).
     - Furthermore, under Rule G (`jobs/WIP.json`), `HOS` has `4` active films (`008, 009, 010, 013`) and `12` films ahead of `107` in `next_hos` / open PRs (`011, 012, 014, 015, 018, 100, 101, 102, 103, 104, 105, 106`) — `16` weeks of Thursday slots (`~4 months`), plus `80+` ideas in `00_Brand/Channel-Setup/ideas/`. Keeping `107` behind `106` in `next_hos` (or holding its Thursday publish slot for late August / September 2027) avoids mid-winter release while keeping the backlog full.

### Ruling on Open Point 2 (`HOS:106`): Does `Thoughty2` Count as the Third Education Neighbour?
- **Ruling: YES (`PASS`).**
  1. **Explicit tool contract (`neighbours.py` line 49):** `Thoughty2` is explicitly listed in `TIER2` of `00_Brand/Channel-Setup/tools/neighbours.py` (`"Physics Girl", "Thoughty2", "Kings and Generals", "Oversimplified", "Extra History", "Simple History"`). `neighbours.py` returns `gate: "PASS"`, `bigCount: 3`, `hasTed: true` on `k61Bk63EvTM` (*Why Nobody Knows How Eels Reproduce*, **`3,317,475` views**).
  2. **Strong Tier-1 `TED-Ed` anchor:** `HOS:106` already has **two direct Tier-1 `TED-Ed` lessons over `1,000,000` views** on the exact subject:
     - **TED-Ed ★** [`RFi6ISTjkR4`](https://youtu.be/RFi6ISTjkR4) — *No one can figure out how eels have sex - Lucy Cooke* (**`2,751,342` views**)
     - **TED-Ed ★** [`BR1enXROmgA`](https://youtu.be/BR1enXROmgA) — *Eli the eel: A mysterious migration - James Prosek* (**`1,157,611` views**)
  3. **Fourth `≥ 1M` science-education video in `public_search.py`:** Signed-out YouTube GB search on `"where do eels come from"` and `"how do eels reproduce"` (`evidence_2026-11-14_public_search_106.json`) also ranks **Bizarre Beasts** [`acEIGorImGs`](https://youtu.be/acEIGorImGs) (*We Finally Know Where Eels Come From*, **`1,594,707` views** — Complexly / Hank Green & Sarah Suta's natural-history education series alongside `SciShow` and `CrashCourse`) at `#1`/`#2`, plus **Auralis** [`LxNq8zOEbM8`](https://youtu.be/LxNq8zOEbM8) (*Eels Shouldn't Be Able To Exist...*, **`1,629,143` views**) and **MinuteEarth** [`DQVUuBQtb7w`](https://youtu.be/DQVUuBQtb7w) (*Why We Haven't Learned More In 101 Years Of Trying*, **`569,775` views**, directly about Johannes Schmidt's Sargasso Sea hunt).

---

## 2. Film 1 Review (Primary Target of `J2837`): `HOS:107` (`02_Video-Projects/107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll`)

- **Verdict:** **GO (`90 / 100` · `9.00 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` behind `HOS:106` (recommended late-August / September seasonal release window).
- **Companion HOS PR (`J2837`):** [`#591`](https://github.com/TheLaughingGod1986/history-of-science/pull/591) (`macbook/J2837`, `status_board.py --check` and `check_all.sh` PASS).

### (1) Non-Duplication Check (`001–106`, `ideas/`, `VIDEO_BACKLOG.json`, `WIP.json`)
- **Result: `PASS` (`0` duplicates or near-duplicates).**
- Checked across all `02_Video-Projects/000–106`, `00_Brand/Channel-Setup/ideas/011–095` & `IDEAS_*.md`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
- **Distinction from `HOS:006` (*The Willow Tree That Was Made of Air*):** `006` covers where tree mass comes from (van Helmont's 1648 willow tree, Priestley's mint, Ingenhousz's 1779 sunlit leaf bubbles, and Calvin's `14C` carbon fixation). `107` covers **why leaves change colour in autumn and how Mikhail Tswett invented chromatography in 1903 by pouring leaf extract through a tube of powdered chalk (`CaCO3`)** to reveal that yellow/orange carotenoids were hidden behind green chlorophyll all summer, followed by Richard Willstätter's 1915 Nobel work on plant pigments.
- **Distinction from `ideas/070` (*Enzymes*):** `070` mentions Richard Willstätter only in his 1926 dispute with James Sumner over whether urease crystals are pure protein, not his 1906–1915 chlorophyll/carotenoid chemistry.

### (2) Audience Evidence: Neighbour Gate, Rule-26 Search Phrase & `public_search.py` Collision Audit

| Phrase / Candidate Title | Autocomplete (`suggest()`) | Top Results in YouTube GB (`public_search.py`, `2026-11-14`) | Verdict |
|---|---|---|---|
| `"why do leaves change colour"` | **yes** (`10` suggestions: `why do leaves change colour in autumn`, `why do leaves change colour`, `why do leaves change color in the fall`, etc.) | 1) **Super Simple Songs** [`Sa_zH0RXfvk`](https://youtu.be/Sa_zH0RXfvk) **`1,991,366` views** · 2) **SciShow Kids** [`Xk4-6II8l5Q`](https://youtu.be/Xk4-6II8l5Q) **`1,850,236` views** · 3) **MinuteEarth** [`JWva5AaDkXw`](https://youtu.be/JWva5AaDkXw) **`1,558,957` views** · 4) **Peekaboo Kidz** [`ubLe26x_2pI`](https://youtu.be/ubLe26x_2pI) **`346,918` views** · 5) **SciShow** [`rwA1QVsbD6g`](https://youtu.be/rwA1QVsbD6g) **`269,611` views** | **PASS (Rule 26a UK phrase)** |
| `"why do leaves change color in the fall"` | **yes** (`6` suggestions) | 1) **SciShow Kids** [`Xk4-6II8l5Q`](https://youtu.be/Xk4-6II8l5Q) **`1,850,236` views** · 2) **Peekaboo Kidz** [`ubLe26x_2pI`](https://youtu.be/ubLe26x_2pI) **`346,918` views** · 3) **Super Simple Songs** [`Sa_zH0RXfvk`](https://youtu.be/Sa_zH0RXfvk) **`1,991,366` views** · 4) **MinuteEarth** [`JWva5AaDkXw`](https://youtu.be/JWva5AaDkXw) **`1,558,957` views** · 5) **Free School** [`UuTrDnzmMxY`](https://youtu.be/UuTrDnzmMxY) **`388,111` views** | **PASS (Rule 26a US phrase)** |
| `"what is chromatography"` | **yes** (`10` suggestions: `what is chromatography`, `what is chromatography in chemistry`, etc.) | 1) **It's AumSum Time** [`PvHvx7k7UPU`](https://youtu.be/PvHvx7k7UPU) **`2,116,418` views** · 2) **Cognito** [`TdJ57SQ6GAQ`](https://youtu.be/TdJ57SQ6GAQ) **`1,532,858` views** · 3) **Khan Academy** [`SnbXQTTHGs4`](https://youtu.be/SnbXQTTHGs4) **`1,328,589` views** · 4) **Chemistorian** [`nVy5jC0-xYk`](https://youtu.be/nVy5jC0-xYk) **`319,708` views** · 5) **Freesciencelessons** [`dsKz9eF1Sc0`](https://youtu.be/dsKz9eF1Sc0) **`242,321` views** | **PASS (Year-round curriculum phrase)** |
| `"chlorophyll"` | **yes** (`10` suggestions incl. `chlorophyll`, `chlorophyll is necessary for photosynthesis`, `chlorophyll structure`) | `Dr. Eric Berg DC` `567,457` · `thedailyECO` `198,943` · `Guess Who's Vegan` `58,203` | **PASS** |
| `Why Do Leaves Change Colour in Autumn? (The Yellow Was Always There)` (`J2835` draft, `68` chars) | no | Result #4: `In A Few Lines` (`tlhm2c7bhic`, `10`v) *#7 – Why Do Leaves Change Colour in Autumn? (The Yellow Was There All Along)* · Result #5: `Kawavu.` (`PfgRu-0WTts`, `2`v) *Why Do Leaves Change Color? (The Yellow Was Always There)* | **Near-collision caught → disambiguated below** |
| **`Why Do Leaves Change Colour? (A Chalk Tube Showed Why)`** (`J2835` alt / Primary Title A, `54` chars) | related (`3` suggestions) | `SciShow Kids` `1,850,236` · `Peekaboo Kidz` `346,918` · `MinuteEarth` `1,558,957` · `Mister Kipley` `25,600` · `SciShow` `269,611` | **`0` collisions — Locked Primary Title A (`54` chars)** |
| **`Why Do Leaves Change Colour? (The 1903 Chalk Tube)`** (`50` chars, Rule 15 `≤50` chars) | related (`4` suggestions) | `SciShow Kids` `1,850,237` · `MinuteEarth` `1,558,952` · `LoveofLearning` `309` · `Curious Kids Lab` `351` · `Infinite Insights` `165` | **`0` collisions — Locked Title C (`≤50`-char variant)** |
| **`Why Do Leaves Change Colour in Autumn? (Tswett's 1903 Chalk Tube)`** (`65` chars) | no | `Tiny Thinkers Lab` `27` · `Timm's Tiny Wonders` `12` | **`0` collisions — Locked Title B (T&C)** |
| `The Hidden Colours Inside Every Green Leaf` (`J2835` draft, `42` chars) | no | Result #2: `Ordinary Runs Deep` (`hthQp2wvPJY`, `4`v) *The Hidden Colors Inside Every Leaf* · Result #8: `sciexplorer_x` (`DrcdawG3cAs`, `70,498`v) *The Hidden Colours Inside a Green Leaf* | **Near-collision + no Rule-26 search phrase → dropped** |
| **`Why Do Leaves Turn Yellow in Autumn?`** (Short `S01`, `36` chars) | related (`3` suggestions: `why do leaves turn yellow in autumn`, `why do leaves turn yellow`, `why do leaves change colour in autumn`) | `MinuteEarth` `1,558,962` · `SciShow Kids` `1,850,236` · `Peekaboo Kidz` `346,918` · `Sheffield Made Plants` `106,876` · `Curiously Kids` `1,808` | **`0` collisions — Locked Short `S01`** |
| `What Is Chromatography?` (`J2835` Short `S02` draft, `23` chars) | **yes** (`10` suggestions) | Result #1: `Chemistry Student` (`rTFlBVcwewI`, `131,452` views) *What is Chromatography?* | **EXACT VERBATIM COLLISION (`rTFlBVcwewI`) → disambiguated below** |
| **`What Is Chromatography? (Tswett's 1903 Leaf-Chalk Tube)`** (Disambiguated Short `S02`, `55` chars) | related | `Cognito` `1,532,866` · `StudyIB` `23` · `NC State S.M.A.R.T. Lab` `324,857` · `Chemistorian` `319,712` · `STEM Spark Zone` `359` | **`0` collisions — Locked Disambiguated Short `S02`** |

### (3) Unverified Claims Guard (`HOS:107` `TOPIC.md` §2)
Every name, date, and number in `107/TOPIC.md` §2 is unverified working memory and **must be verified with exact quotes in `SOURCES.md` by the `facts` lane (`gemini-agy`) before any script lock**:
1. **Pierre-Joseph Pelletier & Joseph Bienaimé Caventou (`1817`, *Journal de Pharmacie* / *Annales de Chimie et de Physique*):** Claim that in `1817` they isolated and named *chlorophylle* (chlorophyll) from green leaves.
2. **Mikhail Semyonovich Tswett (`21 March 1903` Warsaw lecture, *Trudy Varshavskogo Obshchestva Estestvoispytatelei* / `1906` *Berichte der Deutschen Botanischen Gesellschaft* vol. 24, pp. 316–323 & 384–393):** Claim that in `1903` Tswett separated leaf pigments (chlorophylls $a/b$, carotenes, xanthophylls) by washing leaf extract through a glass column packed with powdered calcium carbonate (`chalk`), and in `1906` coined the term *chromatography* ("colour writing").
3. **Richard Willstätter (`1906–1914` *Untersuchungen über Chlorophyll*, `1915` Nobel Prize in Chemistry):** Claim that Willstätter won the `1915` Nobel Prize in Chemistry for his investigations on plant pigments, especially chlorophyll (establishing magnesium at the core of chlorophyll $a$ and $b$), and that Tswett's column chromatography was largely overlooked for ~25 years (until Kuhn, Winterstein & Lederer `1931`) after Tswett died in `1919`.
4. **Plant physiology claim (carotenoids vs anthocyanins):** Claim that yellow/orange carotenoids (xanthophylls and carotenes) are present in the chloroplast all summer and unmasked when chlorophyll breaks down in autumn, whereas red/purple anthocyanins are newly synthesised in autumn.

---

## 3. Film 2 Review (Companion Target of `J2836`): `HOS:106` (`02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso`)

- **Verdict:** **GO (`94 / 100` · `9.40 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` ahead of `HOS:107` under Rule G.
- **Companion HOS PR (`J2836`):** [`#589`](https://github.com/TheLaughingGod1986/history-of-science/pull/589) (`macbook/J2836`, `check_all.sh` PASS).

### (1) Non-Duplication Check (`001–105`, `ideas/`, `VIDEO_BACKLOG.json`, `WIP.json`)
- **Result: `PASS` (`0` duplicates or near-duplicates).**
- Checked across all `02_Video-Projects/000–105` (including open PRs `102` Ozone Hole, `103` Blue Sky, `104` Speed of Light, `105` Venus Flytrap), `00_Brand/Channel-Setup/ideas/011–095` & `IDEAS_*.md`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
- Only tangential mentions exist: `005` Harvey mentions frog and eel hearts in one sentence as cold-blooded examples; `019` Galvani mentions electric eels in passing; `100` Bird Magnetic Compass lists `TED-Ed`'s *Eli the eel* (`BR1enXROmgA`) as a migration neighbour. None covers the 2,000-year mystery of eel reproduction, Freud's 1876 Trieste dissections, Grassi's 1896 *Leptocephalus* metamorphosis, or Schmidt's 1904–1922 Sargasso Sea expeditions.

### (2) Audience Evidence: Neighbour Gate, Rule-26 Search Phrase & `public_search.py` Collision Audit

| Phrase / Candidate Title | Autocomplete (`suggest()`) | Top Results in YouTube GB (`public_search.py`, `2026-11-14`) | Verdict |
|---|---|---|---|
| `"where do eels come from"` | **yes** (`5` suggestions: `where do eels come from`, `where does eels come from`, `where did eels come from`, `where do electric eels come from`, `eels where do they come from`) | 1) **Bizarre Beasts** [`acEIGorImGs`](https://youtu.be/acEIGorImGs) **`1,594,707` views** · 2) **Atomic Frontier** [`y0UIJekwyPY`](https://youtu.be/y0UIJekwyPY) **`365,534` views** · 3) **TED-Ed** [`BR1enXROmgA`](https://youtu.be/BR1enXROmgA) **`1,157,605` views** · 4) **Auralis** [`LxNq8zOEbM8`](https://youtu.be/LxNq8zOEbM8) **`1,629,143` views** · 5) **MinuteEarth** [`DQVUuBQtb7w`](https://youtu.be/DQVUuBQtb7w) **`569,775` views** | **PASS (Rule 26a primary phrase)** |
| `"how do eels reproduce"` | **yes** (`7` suggestions: `how do eels reproduce`, `how do eels reproduce ted ed`, `how do eels reproduce mystery`, etc.) | 1) **TED-Ed** [`RFi6ISTjkR4`](https://youtu.be/RFi6ISTjkR4) **`2,751,342` views** · 2) **Bizarre Beasts** [`acEIGorImGs`](https://youtu.be/acEIGorImGs) **`1,594,707` views** · 3) **Thoughty2** [`k61Bk63EvTM`](https://youtu.be/k61Bk63EvTM) **`3,317,475` views** | **PASS (Rule 26a secondary phrase)** |
| `"eel migration"` | **yes** (`9` suggestions incl. `eel migration`, `eel migration sargasso sea`, `european eel migration`) | 1) **TED-Ed** [`BR1enXROmgA`](https://youtu.be/BR1enXROmgA) **`1,157,608` views** · 2) **Auralis** [`LxNq8zOEbM8`](https://youtu.be/LxNq8zOEbM8) **`1,629,141` views** · 3) **Bizarre Beasts** [`acEIGorImGs`](https://youtu.be/acEIGorImGs) **`1,594,707` views** | **PASS** |
| `"sargasso sea eels"` | **yes** (`1` suggestion: `sargasso sea eels`) | `acapellascience` `175,206` · `Discovery UK` `114,189` · `Auralis` `1,629,143` · `Bizarre Beasts` `1,594,707` | **PASS** |
| `Where Do Eels Come From? (The 2,000-Year Mystery)` (`J2835` draft, `49` chars) | related | Result #1: `Creature Code` (`mgRlVeTSSMA`, `8` views) *Where Do Eels Come From? The 2,000-Year Mystery* | **Punctuation collision caught → disambiguated below** |
| **`Where Do Eels Come From? (The Sargasso Sea Hunt)`** (`48` chars, Rule 15 & Rule 26) | related | `Bizarre Beasts` `1,594,709` · `WowScience` `66` · `Untamed Animal Facts` `1,209` · `MinuteEarth` `569,777` · `TED-Ed` `1,157,611` | **`0` collisions — Locked Primary Title A** |
| `How Do Eels Reproduce? (Nobody Has Ever Seen It)` (`J2835` draft, `48` chars) | related | Result #6: `CuriosityFact` (`_BWQLJJ3GcM`, `2` views) *How Do Eels Reproduce? No One Has Ever Seen It* | **Near-collision caught → disambiguated below** |
| **`How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)`** (`51` chars, Rule 26 + Rule 23) | related | `Bizarre Beasts` `1,594,709` · `Thoughty2` `3,317,476` · `The Earth and Alien` `1` · `OctoLab` `1,365` · `Deep Sea Lab` `668` | **`0` collisions — Locked Title B (T&C)** |
| **`The Fish That Freud Dissected 400 Times`** (`39` chars) | no | `calvintheninja` `47,374` · `VILEMasterShake` `13,938` · `Animal Oddballs` `81` · `The Origin Vault` `66,928` · `Fish Journeys` `255` | **`0` collisions — Title C (Story variant)** |
| **`Why Did Sigmund Freud Dissect 400 Eels?`** (Short `S01`, `39` chars) | related | `calvintheninja` `47,374` · `VILEMasterShake` `13,938` · `Animal Oddballs` `80` · `showselectordog` `3,451,018` · `Sketchy Details` `31` | **`0` collisions — Locked Short `S01`** |
| **`Has Anyone Ever Seen an Eel Lay Eggs?`** (Short `S02`, `37` chars) | no | `Bizarre Beasts` `1,594,707` · `Never Filmed` `57` · `Pokato_1` `9` · `TED-Ed` `2,751,342` · `Nescium` `382` | **`0` collisions — Locked Short `S02`** |

### (3) Unverified Claims Guard (`HOS:106` `TOPIC.md` §2)
Every name, date, and number in `106/TOPIC.md` §2 is unverified working memory and **must be verified with exact quotes in `SOURCES.md` by the `facts` lane (`gemini-agy`) before any script lock**:
1. **Aristotle (4th century BC, *Historia Animalium* VI.16):** Claim that Aristotle concluded eels have no eggs or milt and grow from mud / "earth's guts" (*gēs enteron*).
2. **Sigmund Freud (`1876` Trieste / `1877` publication, *Sitzungsber. Kaiserl. Akad. Wiss. Wien* Bd. 75, pp. 419–431):** Claim that a 19-year-old Freud at Carl Claus's zoological station in Trieste dissected `~400` eels searching for the male organs (Syrski's lobed organ) and found no mature sperm.
3. **Giovanni Battista Grassi & Salvatore Calandruccio (`1896` / `1897`, *Proc. R. Soc. Lond.* vol. 60, pp. 260–271):** Claim that they proved the transparent willow-leaf fish *Leptocephalus brevirostris* transforms into the European glass eel (*Anguilla anguilla*).
4. **Johannes Schmidt (`1904–1922`, *Phil. Trans. R. Soc. B* vol. 211, pp. 179–208, `1922`):** Claim that Schmidt towed nets across the Atlantic for nearly twenty years, tracing progressively smaller larvae (`<10 mm`) to the Sargasso Sea in `1922` without ever observing adult spawning.
5. **Wright et al. (`13 October 2022`, *Scientific Reports* 12, 15362):** Claim that the first direct satellite-tag tracks of adult European eels reaching the Sargasso Sea were published in `2022`, and that wild eel spawning/eggs in the Sargasso remain unseen.

---

## 4. Opportunity Score Comparison (`HOS:107` vs `HOS:106`)

| Dimension | Weight | `HOS:107` Autumn Leaves (`Score` / `Weighted`) | `HOS:106` Eels (`Score` / `Weighted`) |
|---|---:|---|---|
| 1. Evergreen search intent | 25% | `8.5` / `2.125` (Strong autumn peak on leaf colour `1.85M` / `1.56M` + year-round GCSE/MCAT chromatography search `1.53M` / `1.33M`) | `9.5` / `2.375` (Year-round search + `TED-Ed` `2.75M` & `1.16M`, `Thoughty2` `3.32M`, `Bizarre Beasts` `1.59M`) |
| 2. Competition gap | 20% | `9.0` / `1.800` (Leaf-colour videos are 2–3 min kids explainers; chromatography videos are dry GCSE whiteboard lessons — none connects Tswett's 1903 chalk tube to autumn leaves) | `9.0` / `1.800` (No painted-3D 4-act detective film from Freud's 1876 Trieste lab to Schmidt's *Dana* nets) |
| 3. Narrative & visual arc | 20% | `9.5` / `1.900` (`0:05–0:15` green leaf extract separating into emerald, gold, and orange rings inside Tswett's 1903 glass chalk column) | `9.5` / `1.900` (Freud's 400 eels → transparent willow-leaf larva → Atlantic larval contour map → 2022 satellite tags) |
| 4. Brand & guardrail fit | 20% | `9.5` / `1.900` (Pure HOS discovery story; distinct from `006` mass/photosynthesis; must avoid `Made for Kids` tone) | `10.0` / `2.000` (Pure HOS discovery story; `0` duplicates) |
| 5. Series / cluster potential | 15% | `8.5` / `1.275` (Botany & Analytical Chemistry cluster with `006`, `105`, `081`) | `8.8` / `1.320` (Animal Navigation & Ocean Mysteries cluster with `100`, `101`, `089`) |
| **Total Opportunity Score** | **100%** | **`9.00 / 10` (`90 / 100`) — `GO` (behind `106`)** | **`9.40 / 10` (`94 / 100`) — `GO` (ahead of `107`)** |

---

## 5. Verification & Checks Run

- `00_Brand/Channel-Setup/tools/public_search.py` (in HOS): **PASS** (`13` queries for `107` saved in `jobs/reviews/J2837/evidence_2026-11-14_public_search_107.json` and HOS PR [`#591`](https://github.com/TheLaughingGod1986/history-of-science/pull/591); `11` queries for `106` saved in `jobs/reviews/J2837/evidence_2026-11-14_public_search_106.json` and HOS PR [`#589`](https://github.com/TheLaughingGod1986/history-of-science/pull/589)).
- `python3 00_Brand/Channel-Setup/tools/status_board.py --check` (in HOS on `macbook/J2837`): **`16 status files and BOARD.json are in order` (`PASS`)**.
- `00_Brand/Channel-Setup/tools/check_all.sh` (in HOS on `macbook/J2837`): **`ALL CHECKS PASS`**.
