# `J3350` — Rule-E Topic Go/No-Go Review: `HOS:130` (`How Does a Nuclear Reactor Work? (Under a Stadium)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3350` · `macbook` (`review` lane; independent Rule-E topic review) |
| **Target Proposal (`J3348`)** | **`HOS:130`** (`02_Video-Projects/130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work`) |
| **Source PRs (`J3348`)** | HOS PR [`#726`](https://github.com/TheLaughingGod1986/history-of-science/pull/726) (`macbook/J3348`, contains both `130` and `131`) · OWB PR [`#1159`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1159) (`macbook/J3348`, appends `HOS:130` & `HOS:131` to `jobs/WIP.json` `next_hos`) |
| **Rule-E Verdict — `HOS:130`** | **GO (`96.6 / 100` · `9.66 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`How Does a Nuclear Reactor Work? (Under a Stadium)`, `50 chars <= 50` Rule 15 & Rule 26; `Title B` `The First Nuclear Reactor Was Built on a Squash Court (1942)`, `60 chars <= 70`; `Title C` `Enrico Fermi: How Scientists Built the First Nuclear Reactor`, `60 chars <= 70`; `0` exact title collisions proven against live non-empty GB search rows across all 3 long titles and both `16–19 s` Short titles) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` holds `4 / 4` HOS slots (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes awaiting verbatim primary-source quotes in `SOURCES.md` and `facts` lane (`gemini-agy`) verification when an active HOS WIP slot opens. |
| **Merge Note** | Isolated HOS review PR (`macbook/J3350`) touches only `02_Video-Projects/130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work/` so it never conflicts with `J3351` (Rule-E review of `HOS:131`, currently claimed by `macbook-2`). Neither HOS PR `#726` nor OWB PR `#1159` is merged here because merges are Chief's and both source PRs also include `HOS:131`. |
| **NAS Note** | `studio-live` NAS mirror deferred (Rule G backlog text stub with zero media, outside the `01:00–06:00` NAS spin-down window). |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Summary & Audit Fixes Applied

`HOS:130` (*How Does a Nuclear Reactor Work? (Under a Stadium)*) **passes all 10 Rule-E gates** with an Opportunity Score of **`9.66 / 10` (`96.6 / 100`)** and is **GO** for pre-cleared backlog retention in `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS WIP slots full). It independently satisfies every currently in-force HOS topic gate (`neighbours.py`, `public_search.py`, Rule 15/26 titles, zero duplication, visual proof-first hook, and strict UNVERIFIED claims guard) while aligning with `J3224` Cluster 2 #2 (`hos-search-2027-01`, accurately marked `needsBen` in `studio/plan.json`).

Four concrete draft issues were caught during independent review and fixed directly on the isolated HOS branch (`macbook/J3350`):

1. **Empty `search: []` rows on Title A & Title B in `evidence_2026-11-22_public_search.json` (`RESOLVED`):**
   - PR `#726`'s `public_search.json` had `0` search rows returned for both Title A (`How Does a Nuclear Reactor Work? (Under a Stadium)`) and Title B (`The First Nuclear Reactor Was Built on a Squash Court (1942)`), leaving their `0 collisions` claims unbacked by live search results.
   - Re-ran `public_search.py` live (`2026-11-22`, £0): Title A returned `8` live GB rows (`TED-Ed` `3,332,510`, `Elearnin` `5,024,242`, `Kurzgesagt` `8,224,855`, `ENGIE Belgium` `739,189`, `AiTelly` `1,699,681` — **`0` exact collisions**); Title B with `(1942)` triggers an empty YouTube GB query page, while parentheses-stripped `"The First Nuclear Reactor Was Built on a Squash Court 1942"` returned `8` live GB rows (`Cosmic Odyssey` `366`, `Power Through Time` `74`, `Argonne National Laboratory` `81,230`, `Loren Klein` `22,699`, `IT'S HISTORY` `192,811` — **`0` exact collisions**).
   - Merged the live non-empty queries into `11_Upload-Package/evidence_2026-11-22_public_search.json` (`11` queries / `80` search rows total; copied alongside `evidence_2026-11-22_neighbours_130.json` into this OWB review folder).
2. **Thumb B cover text repeated Title A (`THUMBNAIL_AND_TITLE_RULES.md` §2.5 violation, `RESOLVED`):**
   - PR `#726` proposed Thumb B text `UNDER STAGG FIELD` (gold on `UNDER`), repeating `Under` from Title A (`How Does a Nuclear Reactor Work? (Under a Stadium)`) and relying on obscure proper-noun venue jargon.
   - Fixed in `TOPIC.md` §3 to **`HIDDEN GRAPHITE PILE`** (`3 words`, gold on `HIDDEN`, zero words repeated from Titles A, B, or C, names the concrete object, and avoids locking an unverified brick count onto the cover before `SOURCES.md`).
3. **Tightened Act IV nuclear-reactor kinetics & safety precision (`RESOLVED`):**
   - PR `#726` `TOPIC.md` §4 Act IV asked *"Why didn't Chicago Pile-1 explode in a microsecond..."* and wrote *"stretches the doubling time from microseconds to tens of seconds"*, conflating prompt neutron emission time (`~10⁻¹⁴ s`) with a graphite-moderated thermal reactor's prompt neutron generation time (`~10⁻³ s` / **milliseconds**, which Short S01 already used) and implying a nuclear-weapon explosion rather than a runaway thermal excursion/meltdown.
   - Tightened Act IV to distinguish prompt emission (`~10⁻¹⁴ s`), thermal graphite prompt generation time (`~10⁻³ s` / milliseconds), and delayed neutrons (`~0.65%`, `β ≈ 0.0065`) stretching the doubling period to tens of seconds, while explicitly noting a natural-uranium/graphite pile cannot detonate like a bomb.
4. **Aligned `10_Shorts/README.md` with Ben 19 Nov 2026 `16–19 s` Shorts house rules + added review sheets (`RESOLVED`):**
   - Added the `16–19 s` Shorts house-rules precedence header to `10_Shorts/README.md` (copied from the legacy `22–27 s` template).
   - Added `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` (`10 / 10` Rule-E gates `PASS` + `7` concrete script-stage sourcing guardrails, including delayed-neutron kinetics, exact brick/uranium masses, 2 Dec 1942 timeline & quotes, anti-"SCRAM"-backronym-myth check, 1933–1934 Szilard/Fermi prehistory, year-accurate `WHO` cards, and zero WW2 combat drift) and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`9.66 / 10` = `96.6 / 100`).

---

## 2. Rule-E Rubric Summary (`10 / 10 PASS`)

- **Neighbour demand (`neighbours.py`, `2026-11-22`):** **PASS** — `12` raw / `9` strictly on-topic education videos `>=1,000,000` views, `hasTed = true`, `failedQueries = []`: `Kurzgesagt` (`10,888,517`, `9,916,883`, `8,224,844`), `SmarterEveryDay` (`7,524,461`, `3,847,436`), `TED-Ed` ★ (`3,332,507`), `TEDx` ★ (`2,322,050`, `1,576,494`), `TED` ★ (`1,243,751`). Three raw `>=1M` rows transparently excluded (`Kurzgesagt` fusion `15.25M`, `TED-Ed` nuclear fallout `2.15M`, `TED-Ed` Three Gorges hydro `1.35M`). Even excluding policy/accident rows leaves `6 >=1M` tightly focused reactor-mechanism/build education videos (2× threshold) with `TED-Ed` ★ + `TED` ★ + `TEDx` ★ present.
- **Signed-out YouTube autocomplete & Rule 26(a) ranking proof (`public_search.py`, `2026-11-22`):** **PASS** — `4` core queries verified `autocomplete = yes` (`"how does a nuclear reactor work"` `7`, `"nuclear chain reaction"` `9`, `"chicago pile 1"` `4`, `"enrico fermi nuclear reactor"` `1`), ranking videos led by `Kurzgesagt` `rcOFV4y5z8c` (`8,224,844`), `StarTalk` `boUqlyYfUuo` (`5,655,988`), `Elearnin` `1U6Nzcv9Vws` (`5,024,242`), `SmarterEveryDay` `JVROsxtjoCw` (`3,847,425–3,847,436`), `TED-Ed` ★ `R7WPEYGr1Vs` (`3,332,507`), `Animagraffs` `PRWwXeRIvoI` (`825,335`), and `SciShow` `MLJ1ebNcNLM` (`457,251`), with **`0` exact title collisions** proven across all `3` long titles and `2` Short titles (`11` queries / `80` rows).
- **Non-duplication (`Rule E` item 1):** **PASS** — zero overlap across `02_Video-Projects/` (`000–018`, `099–119`), open PRs (`120–129`, `131`), `ideas/011–095` (`022_Meitner-Hahn-Nuclear-Fission` stops at Dec 1938 discovery & Jan 1939 Frisch test), `VIDEO_BACKLOG.json`, and `jobs/WIP.json`; zero WW2 combat overlap with Field Order History.
- **Visual proof-first hook & Shorts (`Rules 10, 30` & Ben 19 Nov `16–19 s` Shorts rules):** **PASS** — physical apparatus in `0:05–0:15` (George Weil withdrawing the cadmium control rod from the 20-ft graphite pile + climbing chart-recorder ink pen + balcony safety jugs); `2` search-titled `16–19 s` Shorts (`S01` `52c`, `S02` `53c`) with 3D-cartoon frame-0 concrete-fact line-1 captions and seamless loops.
- **Unverified claims guard & Rule G WIP cap:** **PASS** — every historical/scientific claim remains **UNVERIFIED** pending `SOURCES.md` exact quotes + `facts` lane when an active HOS WIP slot opens; all `12` stages in `status.json` remain `"todo"`; `£0.00` spent.

---

## 3. Opportunity Score (`9.66 / 10` · `96.6 / 100`)

| Dimension | Weight | Score | Weighted |
|---|---:|---:|---:|
| 1. Evergreen search intent | 25% | `9.8` | `2.450` |
| 2. Competition gap | 20% | `9.6` | `1.920` |
| 3. Narrative & visual arc | 20% | `9.8` | `1.960` |
| 4. Brand & guardrail fit | 20% | `9.3` | `1.860` |
| 5. Series / cluster potential | 15% | `9.8` | `1.470` |
| **Total** | **100%** | — | **`9.660 / 10` (`96.6 / 100`)** |

---

## 4. Next Steps

1. Complete `J3351` (Rule-E review of `HOS:131` *What Is the Theory of Relativity? (1919 Eclipse)*, currently claimed by `macbook-2`).
2. Chief merges the approved `HOS:130` (`macbook/J3350`) and `HOS:131` (`J3351`) review PRs (superseding raw HOS PR `#726`) plus OWB PR `#1159` (`jobs/WIP.json` `next_hos` append) and this OWB review PR (`macbook/J3350`).
3. Keep `HOS:130` in `jobs/WIP.json` `next_hos` under Rule G until an active HOS slot opens (or Ben approves `hos-search-2027-01` in `studio/plan.json` for Jan 2027 scheduling), at which point queue `SOURCES.md` + `facts` lane (`gemini-agy`) before script lock.
