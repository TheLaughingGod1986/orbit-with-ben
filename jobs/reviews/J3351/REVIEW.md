# `J3351` — Rule-E Topic Go/No-Go Review: `HOS:131` (`What Is the Theory of Relativity? (1919 Eclipse)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3351` · `macbook-2` (`review` lane) |
| **Target Proposal (`J3348`)** | **`HOS:131`** (`02_Video-Projects/131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity`) |
| **Source PRs (`J3348`)** | HOS PR [`#726`](https://github.com/TheLaughingGod1986/history-of-science/pull/726) (`macbook/J3348`, contains both `130` and `131`) · OWB PR [`#1159`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1159) (`macbook/J3348`, appends `HOS:130` & `HOS:131` to `jobs/WIP.json` `next_hos`) |
| **Rule-E Verdict — `HOS:131`** | **GO (`96.5 / 100` · `9.65 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`What Is the Theory of Relativity? (1919 Eclipse)`, `48 chars ≤ 50` Rule 15 & Rule 26; `Title B` `How a 1919 Solar Eclipse Proved Einstein Beat Isaac Newton`, `58 chars ≤ 70`; `Title C` `Theory of Relativity Explained: The 1919 Eclipse That Proved It`, `63 chars ≤ 70`; `Short S01` `How Did the 1919 Solar Eclipse Prove Einstein's Relativity?`, `59 chars`; `Short S02` replaced in `J3351` with `How Does Einstein's Relativity Keep GPS Accurate?`, `49 chars ≤ 50`; `0` exact and `0` near-exact title collisions across all 5 titles) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` holds `4 / 4` HOS slots (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes awaiting verbatim primary-source quotes in `SOURCES.md` and `facts` lane (`gemini-agy`) verification when an active HOS WIP slot opens. |
| **Merge Note** | Isolated HOS review PR (`macbook/J3351`) touches only `02_Video-Projects/131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity/` so it never conflicts with `J3350` (Rule-E review of `HOS:130`). Neither HOS PR `#726` nor OWB PR `#1159` is merged here (merges are Chief's, and both PRs include `HOS:130`). |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Summary & Audit Fixes Applied

`HOS:131` (*What Is the Theory of Relativity? (1919 Eclipse)*) from `J3348` passes all `10 / 10` `AGENTS.md` Rule-E and `STUDIO_PLAYBOOK.md` §2 gates with a **`96.5 / 100` (`9.65 / 10` Opportunity Score) GO** verdict in `jobs/WIP.json` `next_hos`, with four targeted packaging/precision improvements applied on isolated HOS branch `macbook/J3351`:

1. **Replaced Short `S02` near-exact title collision & re-verified `0` collisions (`RESOLVED`, `£0.00`):** Original Short `S02` (`Why Do GPS Satellites Need Einstein's Relativity to Work?`, `57 chars`) near-collided almost word-for-word with live video `tU2gJpkmEgs` (*"Why GPS Satellites Need Einstein's Relativity to Work"*, `The Curious Conscious`) and `hb7e6IFFFUE` (*"Why GPS Needs Einstein's Relativity to Work"*). Replaced with **`How Does Einstein's Relativity Keep GPS Accurate?`** (`49 chars ≤ 50`), verified live via `public_search.py` (`0` exact and `0` near-exact collisions; query #11 appended to `evidence_2026-11-22_public_search.json`).
2. **Fixed Thumbnail C §2.5 title-word repetition (`RESOLVED`):** Changed Thumb C cover text from `NEWTON WAS WRONG` (which repeated `NEWTON` straight from Title B, violating `THUMBNAIL_AND_TITLE_RULES.md` §2.5, and overstated General Relativity's relationship to Newtonian gravity) to **`CURVED SPACE`** (`2 words`, gold on `CURVED`, zero overlap with Titles A/B/C and distinct from Thumb A `STARLIGHT BENT` and Thumb B `TIME SLOWS`).
3. **Updated `10_Shorts/README.md` (`RESOLVED`):** Added the `19 Nov 2026` `16–19 s` Shorts house-rules header over the legacy `22–27 s` template text.
4. **Logged script-stage precision guardrails (`UNVERIFIED` pending `SOURCES.md` + `facts` lane):**
   - Distinguish Einstein's limb-extrapolated `1.75"` prediction (`vs 0.87"` Newton / Einstein 1911) from the Príncipe (`1.61" ± 0.30"`) and Sobral 4-inch (`1.98" ± 0.12"`) measured averages (`Dyson, Eddington & Davidson, 1920`), and credit Astronomer Royal Frank Dyson alongside Eddington, Crommelin, and Davidson.
   - Tighten `"230 years"` → `"over 230 years"` (`1687` *Principia* → `1919` = `232` years); avoid over-claiming Michelson–Morley (1887) as the sole trigger of Einstein's 1905 Special Relativity paper; cite Le Verrier (1859) and Newcomb (1882) for Mercury's `43"`/century; verify J. J. Thomson's 6 Nov 1919 Royal Society/RAS quote verbatim.
   - Unify GPS drift working note to `~11 km/day` (`+38 µs/day × c ≈ 11.4 km/day`; factory-offset satellite clocks keep GPS accurate, drift occurs *without* Einstein's correction) and map the 4-act sketch cleanly to HOS's 5-part (`7–9 min`) layout (`PRE_BUILD_VIDIQ_AUDIT.md` §5).

---

## 2. Rule-E Gate Verification Summary (`10 / 10 PASS`)

- **HOS data comparison (`2026-11-22` snapshot, `studio_ctr.json`, `channel_daily.json`):** **PASS** — all `7` public longs and `35` public Shorts ranked with explicit `<100`-view hypothesis caveat.
- **Signed-out YouTube autocomplete & ranking videos (`Rule 26` / `26a`):** **PASS** — `"what is the theory of relativity"` (`10`), `"theory of relativity explained"` (`10`), `"how did einstein prove relativity"` (`1`) `autocomplete = yes`, plus `"einstein 1919 solar eclipse"` → related `"1919 solar eclipse einstein"`; ranking videos `Science ABC` `yuD34tEpRFw` (`9,685,020`), `Arvin Ash` `tzQC3uYL67U` (`7,384,849`), `minutephysics` `hW7DW9NIO9M` (`6,268,836`) & `eNhJY-R3Gwg` (`1,855,197`), `StarTalk` `1BCkSYQ0NRQ` (`3,512,623`), `Vox` `HLxvq_M4218` (`2,196,555`), `SpaceRip` `g8ZO5XvHORI` (`1,881,348`), `Beeyond Ideas` `-2X8alKLJq0` (`1,647,646`).
- **Neighbour gate (`neighbours.py`, `2026-11-22`):** **PASS** — `7` raw / **`5` strictly on-topic education videos `≥1M` views**, `TED-Ed/TED: yes` (`Veritasium` `8.55M`, `TED-Ed` ★ `5.92M` & `2.73M`, `minutephysics` `1.86M`, `CrashCourse` `1.45M`; `2` raw `≥1M` rows transparently excluded as logic puzzle `1rDVz_Fb6HQ` and quantum entanglement `DbbWx2COU0E`).
- **Title collisions & non-duplication (`Rule E` item 1):** **PASS** — `0` exact and `0` near-exact title collisions across Titles A/B/C and Shorts S01/S02 (after `J3351` S02 replacement); zero overlap across `02_Video-Projects/` (`000–018`, `099–119`), open PRs (`120–130`), `ideas/011–095` (distinct from `009` Newton's gravity, `025` photoelectric effect, and `042` laser), `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
- **Visual proof-first hook & Shorts (`Rules 10, 30`, Ben 19 Nov `16–19 s` Shorts rules):** **PASS** — Príncipe brass astrographic telescope + developed glass star plate under micrometre microscope in `0:05–0:15`; `2` named-entity question Shorts (`S01` `59c`, `S02` `49c`) built to Ben's `16–19 s` 3D-cartoon frame-0 concrete-fact-line-1 loop rules.
- **Unverified claims guard & Rule G WIP cap:** **PASS** — every historical/scientific claim remains **UNVERIFIED** pending `SOURCES.md` verbatim quotes + `facts` lane when an active HOS WIP slot opens; all `12` stages in `status.json` remain `"todo"`; `£0.00` spent.

---

## 3. Opportunity Score (`9.65 / 10` · `96.5 / 100`)

| Dimension | Weight | Score | Weighted |
|---|---:|---:|---:|
| 1. Evergreen search intent | 25% | `9.9` | `2.475` |
| 2. Competition gap | 20% | `9.3` | `1.860` |
| 3. Narrative & visual arc | 20% | `9.8` | `1.960` |
| 4. Brand & guardrail fit | 20% | `9.4` | `1.880` |
| 5. Series / cluster potential | 15% | `9.8` | `1.470` |
| **Total** | **100%** | — | **`9.645 / 10` (`96.5 / 100`)** |

---

## 4. Next Steps

1. Let `J3350` (Rule-E review of `HOS:130` *How Does a Nuclear Reactor Work?*) finish on its own isolated branch.
2. Chief merges the approved `HOS:130` (`J3350`) and `HOS:131` (`macbook/J3351`) review PRs (superseding raw HOS PR `#726`), OWB PR `#1159` (`jobs/WIP.json` `next_hos` append), and this OWB review PR (`macbook/J3351`).
3. Keep `HOS:131` in `jobs/WIP.json` `next_hos` under Rule G until an active HOS WIP slot opens, then run `SOURCES.md` verbatim quotes + `facts` lane (`gemini-agy`) and live vidIQ scoring before script lock.
