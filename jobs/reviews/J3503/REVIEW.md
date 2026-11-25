# Review — `J3503`: HOS `137` *Accidental Inventions: 5 Mistakes That Worked* Rule-E Topic Go/No-Go Review

| Field | Value |
|---|---|
| **Job ID** | `J3503` (`kind: review` · `macbook` under `AGENTS.md` Rule E & Rule H) |
| **Film** | `HOS:137` · `02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World` |
| **Reviewed Source PRs (`J3495`)** | HOS PR [`#743`](https://github.com/TheLaughingGod1986/history-of-science/pull/743) (`gemini/J3495-hos-search-2027`) · OWB PR [`#1240`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1240) |
| **Isolated HOS Review PR** | [`history-of-science#747`](https://github.com/TheLaughingGod1986/history-of-science/pull/747) (`macbook/J3503`, strictly isolated to `02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/`) |
| **Date** | `2026-11-24` |
| **Verdict** | **GO (`95.8 / 100` · `9.58 / 10` Opportunity Score)** — **`10 / 10` gates PASS after `J3503` fixes** |
| **Follow-On Queued (Rule E)** | **`J3513`** (`kind: script`, `--repo hos`, `--film 137`, draft due **Mon 30 Nov 18:00 London**, lock **Tue 8 Dec**, Ben's watch by **Mon 21 Dec**, target air **Thu 24 Dec 2026 18:00 London**) |
| **Spend & Guardrails** | `£0.00` spent. All historical/scientific claims remain **UNVERIFIED** pending `SOURCES.md` verbatim primary quotes and the `facts` lane (`gemini-agy`). Enters active production at the next free HOS WIP place once `008`/`009` clear Ben's watch under Rule G; never rushed. |

---

## 1. Critical Defects Caught & Fixed in `J3503` (`history-of-science#747`)

1. **Title A Never-list collision (`FIXED`):** PR `#743`'s Title A `5 Accidental Inventions That Changed the World` (`46c`) claimed `0` collisions despite **5 exact live YouTube collisions** in saved evidence (`Arun Surya Teja` `nLbBtuydgZo` **251,692 views**, `History Files Of US` `WL0YYaFfB5g`, `The Top Five` `aVLMolVjtbI`, `CodeExiled` `R0tNklZQcwA`, `RayFlush` `XS-ul8SrcX8`), violating `studio/RULES.md` & `THUMBNAIL_AND_TITLE_RULES.md` §1.7 (*never the title of a live video*). Retired and replaced with **`Accidental Inventions: 5 Mistakes That Worked`** (`45c ≤ 50`, `0` collisions), alongside Ben-approved plan Title B (`69c`, `0` collisions), Title C (`56c`, `0` collisions), and alternate `≤50c` backup `5 Accidental Lab Mistakes That Changed the World` (`48c`, `0` collisions).
2. **Thumbnail Concept A & B (§2.2, §2.5 & §2.B.1 `FIXED`):** Replaced Concept A's title-repeating `5 MISTAKES` (repeated across Titles A/B/C, violating §2.5) and 3-object bench collage (§2.2 clutter at `168×94`) with a single giant hero object (~2/3 right frame: spiderwebbed unbroken 1903 glass flask OR glowing emerald *Penicillium* Petri dish) + **`NEARLY TRASHED`** (gold on `TRASHED`); tightened Concept B `WRONG PART` to **`WRONG RESISTOR`** (gold on `WRONG`, names exact object per §2.B.1).
3. **5-Beat Shortlist Ruling (`Safety Glass` vs `Microwave` vs `HOS:129`):** **Locked Laminated Safety Glass (Édouard Bénédictus, 1903) as Beat 3 and excluded Microwave (1945)** because `HOS:129` (*How Was the Microwave Invented? (A Radar Accident)*, PR `#724`/`#727`) already passed Rule-E GO (`96.4/100`) in `next_hos`. This keeps zero overlap between `HOS:137` (Cluster 3 anthology hub) and `HOS:129` (standalone Cluster 3 deep dive).
4. **Evidence audit & 6 extra live free `public_search.py` queries (`FIXED`):**
   - Transparently excluded `1` off-topic raw `≥1M` neighbour from `evidence_2026-11-24_neighbours.json` (`TED-Ed` `RzkD_rTEBYs` *How will AI change the world?*, `2,323,113` views), leaving **`3` strictly on-topic education videos `≥1M`** (`Thoughty2` `1.59M`, `TED-Ed` ★ `1.49M` & `1.04M`, `hasTed = true`), reinforced by `SciShow` `YYyfioO50fM` (*6 Incredible Discoveries Made on Accident*, `1,484,724` views) in `evidence_2026-11-24_public_search.json` (`4` strictly on-topic `≥1M` total).
   - Populated `inventions that changed the world` search rows (previously empty in PR `#743`), verified `inventions that shook the world` as `autocomplete = yes` (`5/5` core phrases verified), and verified `0` exact collisions across all updated Long Titles and Short Titles (`S01` `61c` & `48c` tight variant, `S02` `54c`; `13` queries total).
5. **Added durable review sheets & logged `6` script-stage guardrails (`RESOLVED`):** Added `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`, updated `status.json` (`topic = done`, `script` referencing `J3513`, all post-topic stages `todo`), `production-status.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC.md`, `10_Shorts/README.md`, and `README.md`. Verified `status_board.py --check` (`34 status files and BOARD.json are in order`) and `check_all.sh` (`ALL CHECKS PASS`).

---

## 2. Rule-E & Search-Led Rule-42 Rubric Summary (`10 / 10 PASS`)

- **Channel data first (`2026-11-24.json` + `J3223`):** Best HOS long remains `002` *Periodic Table* (`162` views, plain subject query) vs `5–15` views on story-first longs; audience is `78.8%` aged 25–54 (`70.2%` male) yet only `2.5%` US (`109` lifetime views). Targeting US/AU/UK adult accidental-inventions search directly addresses HOS's low-impression / US-starvation bottleneck.
- **Demand, Anglosphere value, gap & small-channel proof (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md`):** `inventions that changed the world` `35,881`/mo (**US 23% = 8,280 US/mo**, `10/10` gap); `accidental discoveries` `9,367`/mo comp `39` (**+93.0%**, parent `amazing discoveries` **AU 20% + US 20%**, `9/10` gap); `accidental inventions that changed the world` `8,092`/mo (**+73.9%**, `10/10` gap); `inventions that shook the world` `8,001`/mo comp `32` (`+69.5%`); US Education RPM proxy **`$3.42` mid (`$2.05–$5.47`)**; low-RPM `history of inventions` (`PK 25%`) explicitly excluded; verified `<50k` outliers `Invention Flex` (`6.2K` US → `9.6K` `8.3×`, 7:42), `Industrial Case Files` (`138` US → `4.7K` `8.6×`), `Counter Facts Lab` (`1.4K` → `1.5K` `22×`), `TheOriginLens` (`246` → `1.6K` `8×`).
- **Live free evidence (`2026-11-24`):** `neighbours.py` tie-breaker **PASS** (`4` raw / `3` strictly on-topic `≥1M`, `2` `TED-Ed` ★ `≥1M`, `hasTed = true`, plus `SciShow` `1.48M` in `public_search.json`); `public_search.py` **PASS** (`13` queries, `5/5` core phrases `autocomplete = yes`, `0` exact collisions across all updated titles & Shorts).
- **Non-duplication:** Verified zero overlap across `02_Video-Projects/` (`000–018`, `099–119`), open HOS PRs (`120–136`), `ideas/011–095`, `VIDEO_BACKLOG.json`, `WIP.json`, `ww2-channel` (`001–010`), and Orbit (`001–087`). Safety Glass locked as Beat 3 so `HOS:129` (Microwave, Rule-E GO) remains 100% separate.

---

## 3. Search-Led Opportunity Score (`9.58 / 10` · `95.8 / 100`)

| Criterion | Score (1–10) |
|---|---:|
| 1. Search demand & gap | `9.6` |
| 2. Anglosphere adult value | `9.5` |
| 3. Small-channel proof | `9.4` |
| 4. Curiosity & packaging | `9.6` |
| 5. Visual potential | `9.7` |
| 6. Storytelling | `9.5` |
| 7. Cluster & series potential | `9.8` |
| 8. Scientific credibility | `9.4` |
| 9. Shorts potential | `9.7` |
| 10. HOS lane fit | `9.6` |
| **Average** | **`9.58 / 10` (`95.8 / 100`)** |

---

## 4. Script-Stage Guardrails Handed to `J3513`

1. **Wilson Greatbatch (1956) precision:** Verify `10 kΩ` vs `1 MΩ` resistor and `1.8 ms` pulse duration/rate in primary sources; clarify he was building a heart-sound recording oscillator; credit Dr William Chardack & Andrew Gage (1958 animal / 1960 Buffalo human implant) and distinguish from Elmqvist & Senning's 1958 Swedish implant.
2. **Charles Goodyear (1839) — "prepared mind":** Verify Woburn, MA 1839 hot-stove account, 1844 patent, 1860 death in debt, and that Goodyear Tire & Rubber was named after him in 1898 (not founded by him); frame as years of obsessive trials rather than an idle fluke.
3. **Édouard Bénédictus (1903 → 1909) timeline:** Verify 1903 Paris evaporated cellulose-nitrate/collodion flask fall and keep the 1909 Triplex patent / automotive windscreen connection distinct; Microwave excluded to protect `HOS:129`.
4. **Alexander Fleming (1928) + Oxford team (1939–1941):** Verify Sept 1928 St Mary's Hospital account and explicitly credit Howard Florey, Ernst Chain, and Norman Heatley for purifying and scaling penicillin; strictly historical lab framing (zero vaccine or medical-advice claims).
5. **Spencer Silver (1968) & Art Fry (1974):** Silver accidentally created low-tack, pressure-sensitive, repositionable acrylate microspheres (never oversimplify as "glue that didn't stick at all"); Fry applied it to church choir hymnal bookmarks in 1974; national launch 1980 after 1978 Boise sample test.
6. **5-part `Teach on screen`, `Polish pass` & §2.6 typography:** `7–9 min` (~1,200–1,300 words), `≥3` animated `DATA+SCALE` graphics incl. 1839–1974 timeline, year-accurate `WHO` cards, `WHEN` stamps, `2–4 FACT` beats, Explorer 1–3 beats (never first minute), zero AI-garbled labels/oscilloscopes, and strict exclusion of low-RPM `history of inventions` (`PK 25%`).

---

## 5. Next Steps

1. Chief merges HOS PR `#743`, isolated HOS review PR `#747` (`macbook/J3503`), OWB PR `#1240`, and this OWB review PR (`macbook/J3503`).
2. `J3513` (`kind: script`, `--repo hos`, `--film 137`, queued immediately by `J3503`) runs package-first lock + 7–9 min script draft + `SOURCES.md` + 2 Short angles due **Mon 30 Nov 18:00 London** (lock **Tue 8 Dec** after `facts` lane, Ben's watch **Mon 21 Dec**, target air **Thu 24 Dec 2026 18:00 London**).
