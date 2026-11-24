# Review — `J3502`: HOS `136` *Trinity Test Explained* Rule-E Topic Go/No-Go Review

| Field | Value |
|---|---|
| **Job ID** | `J3502` (`kind: review` · `macbook-2` under `AGENTS.md` Rule E & Rule H) |
| **Film** | `HOS:136` · `02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` |
| **Reviewed Source PRs (`J3495`)** | HOS PR [`#743`](https://github.com/TheLaughingGod1986/history-of-science/pull/743) (`gemini/J3495-hos-search-2027`) · OWB PR [`#1240`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1240) |
| **Isolated HOS Review PR** | [`history-of-science#746`](https://github.com/TheLaughingGod1986/history-of-science/pull/746) (`macbook/J3502`, strictly isolated to `02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/`) |
| **Date** | `2026-11-24` |
| **Verdict** | **GO (`96.3 / 100` · `9.63 / 10` Opportunity Score)** — **`10 / 10` gates PASS** |
| **Follow-On Queued (Rule E)** | **`J3507`** (`kind: script`, `--repo hos`, `--film 136`, draft due **Sat 28 Nov 18:00 London**, lock **Fri 4 Dec**, Ben's watch by **Mon 14 Dec**, target air **Thu 17 Dec 2026 18:00 London**) |
| **Spend & Guardrails** | `£0.00` spent. All historical/scientific claims remain **UNVERIFIED** pending `SOURCES.md` verbatim primary quotes and the `facts` lane (`gemini-agy`). Enters active production at the next free HOS WIP place once `008`/`009` clear Ben's watch under Rule G; never rushed. |

---

## 1. Corrections Applied in `J3502` (`history-of-science#746`)

1. **Thumbnail Concept A §2.5 & §2.B violation (`FIXED`):** Replaced `IGNITE THE SKY?` (which repeated Title A *Trinity Test Explained: Could It Ignite the Sky?* verbatim, violating `THUMBNAIL_AND_TITLE_RULES.md` §2.5) with **`AIR ON FIRE?`** (3 words, gold on `FIRE?`, names the subject per §2.B, zero overlap across Long Titles A, B, and C).
2. **Thumbnail Concept B §2.5 & physics-accuracy mismatch (`FIXED`):** Replaced `ZERO MARGIN` (which contradicted `LA-602`'s large radiative-cooling safety margin and did not match the Fermi paper-scrap visual) with **`MEASURED BY PAPER`** (3 words, gold on `PAPER`, concrete and accurate to the visual).
3. **Evidence audit & 4 extra free `public_search.py` queries (`FIXED`):**
   - Removed the unbacked parenthetical citation to `SciShow` (`1,671,802`) and `CrashCourse` (`944,463`) from `TOPIC.md` and `production-status.md` because neither row was present in saved `11_Upload-Package/evidence_2026-11-24_neighbours.json`.
   - Filtered the saved `8` raw `≥1M` rows transparently to **`5` strictly relevant `≥1M`** nuclear-fission / Oppenheimer / atomic-blast education videos (`Veritasium` `19.96M`, `TEDx` ★ `9.22M`, `Kurzgesagt` `8.23M`, `TED-Ed` ★ `3.33M`, `TED-Ed` ★ `2.15M`), explicitly excluding `3` broader/adjacent rows (`Real Engineering` `4.98M` nuclear fusion, `TEDx` `2.32M` nuclear power policy, `TED` ★ `1.24M` small fission reactors) as not required for PASS.
   - Merged `4` extra live free `2026-11-24` queries into `evidence_2026-11-24_public_search.json` (`10` queries total): verified `"trinity test explained"` and `"enrico fermi"` as **`autocomplete = yes`** (`4/4` core phrases verified) and verified **`0` exact collisions** on Short S01 (`63c`, corrected from `64c`) and Short S02 (`58c`).
4. **Added durable review sheets & logged `7` script-stage guardrails (`RESOLVED`):** Added `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`, updated `status.json` (`topic = done`, `script` referencing `J3507`, all post-topic stages still `todo`), `production-status.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC.md`, `10_Shorts/README.md`, and `README.md`. Verified `status_board.py --check` (`34 status files and BOARD.json are in order`) and `check_all.sh` (`ALL CHECKS PASS`).

---

## 2. Rule-E & Search-Led Rule-42 Rubric Summary (`10 / 10 PASS`)

- **Channel data first (`2026-11-24.json` + `J3223`):** Best HOS long remains `002` *Periodic Table* (`162` views, plain subject query) vs `5–15` views on story-first longs; audience is `78.8%` aged 25–54 (`70.2%` male) yet only `2.5%` US (`109` lifetime views). Targeting US/UK adult physics search directly addresses HOS's primary bottleneck.
- **Demand, Anglosphere value, gap & small-channel proof (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md`):** `trinity test` `21,494`/mo, competition `38`, steady; parent `manhattan project` `35,203`/mo (**US 18%, GB 9%** = `27%` US+GB); US Education RPM proxy **`$3.42` mid (`$2.05–$5.47`)**; low-RPM `nuclear bomb` (`IN 26%, BD 17%`) explicitly excluded; **`9/10` signed-out US top-10 gap**; verified `<50k` US outliers `Unifying Lens` (`1.5K` → `1.7K`, `15×`, 9:55), `Untold WWII` (`84` → `5.8K`, `172×`), Cluster 2 `Science Retold` (`3.4K` → `61.9K` `13×` & `28.5K` `6.1×`), `Math Everywhere` (`10.3K` → `36.5K`, `10×`).
- **Live free evidence (`2026-11-24`):** `neighbours.py` tie-breaker **PASS** (`8` raw / `5` strictly relevant `≥1M`, `2` `TED-Ed` ★ `≥1M`, `hasTed = true`, `failedQueries = []`); `public_search.py` **PASS** (`10` queries, `4/4` core phrases `autocomplete = yes`, `0` exact title collisions across 3 long titles and 2 Short titles; ranking videos `CBS Sunday Morning` `3.96M`, `The Film Gate` `2.45M`, `Kyle Hill` `2.24M`, `Because Science` `2.24M`, `UCTV` `7.03M`, `Iron Minds` `359k`).
- **Non-duplication:** Verified zero overlap across `02_Video-Projects/` (`000–018`, `099–119`), open HOS PRs (`120–135`, `137`), `ideas/011–095`, `VIDEO_BACKLOG.json`, `WIP.json`, `ww2-channel` (`001–010`), and Orbit (`001–087`). Explicitly distinct from `HOS:130` (Chicago Pile-1 1942 reactor) and `ideas/022` (1938 fission).

---

## 3. Search-Led Opportunity Score (`9.63 / 10` · `96.3 / 100`)

| Criterion | Score (1–10) |
|---|---:|
| 1. Search demand & gap | `9.8` |
| 2. Anglosphere adult value | `9.6` |
| 3. Small-channel proof | `9.8` |
| 4. Curiosity & packaging | `9.5` |
| 5. Visual potential | `9.6` |
| 6. Storytelling | `9.7` |
| 7. Cluster & series potential | `9.8` |
| 8. Scientific credibility | `9.4` |
| 9. Shorts potential | `9.6` |
| 10. HOS lane fit | `9.5` |
| **Average** | **`9.63 / 10` (`96.3 / 100`)** |

---

## 4. Script-Stage Guardrails Handed to `J3507`

1. **`LA-602` date vs pre-test timeline:** `LA-602` (Konopinski, Marvin & Teller) is dated **August 1946** (post-war documentation of the July 1942 Berkeley & pre-Trinity Los Alamos checks — never claim it was written in 1942 or handed to Groves before July 1945).
2. **Atmospheric-ignition physics & no movie-myth conflation:** `¹⁴N + ¹⁴N` fusion was ruled out with a large safety margin by radiative cooling (Bremsstrahlung / inverse Compton losses); never present Arthur Compton's 1959 *"three chances in a million"* recollection as settled 1945 math without primary attribution and Bethe's rebuttal in `SOURCES.md`.
3. **Separate Fermi's side bet from his paper-scrap yield estimate:** Keep the pre-shot Base Camp side bet strictly separate from his ~40 s post-flash torn-paper shockwave measurement (~2.5 m displacement → ~10 kt estimate vs ~20–21 kt official yield).
4. **Plutonium-240 implosion physics:** Conceptual physics only (Segrè 1944 Pu-240 spontaneous fission → gun-type pre-detonation → spherical explosive lenses); zero actionable weapon blueprints.
5. **Strict HOS 3D cartoon lane & Advertiser-Friendly policy:** Zero combat footage, zero Hiroshima/Nagasaki bombing or casualty imagery, zero fear framing (*Wonder, not fear*; zero overlap with Field Order History).
6. **5-part `Teach on screen` & `Polish pass` targets:** `7–9 min`, ~1,200–1,300 words, `≥3` animated `DATA+SCALE` graphics incl. timeline, year-accurate `WHO` cards, `WHEN` stamps, `2–4 FACT` beats, Explorer 1–3 beats (never first minute).
7. **Typography (§2.6):** Chalkboard/teach equations inked cleanly in edit or hand-verified; no AI-garbled math.

---

## 5. Next Steps

1. Chief merges HOS PR `#743`, isolated HOS review PR `#746` (`macbook/J3502`), OWB PR `#1240`, and this OWB review PR (`macbook/J3502`).
2. `J3507` (`kind: script`, `--repo hos`, `--film 136`, queued immediately by `J3502`) runs package-first lock + 7–9 min script draft + `SOURCES.md` + 2 Short angles due **Sat 28 Nov 18:00 London** (lock **Fri 4 Dec** after `facts` lane, Ben's watch **Mon 14 Dec**, target air **Thu 17 Dec 18:00 London**).
