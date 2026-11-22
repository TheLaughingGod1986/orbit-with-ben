# `J3346` — Rule-E Topic Go/No-Go Review: `HOS:128` (`Why Do We Use AC Instead of DC? (Edison vs Tesla)`)

| Field | Value |
|---|---|
| **Job ID & Reviewer** | `J3346` · `gemini` (`review` lane; elected acting Chief for HOS under 11 Nov 2026 chain `Grok -> Claude -> Codex -> Gemini`) |
| **Target Proposal (`J3270`)** | **`HOS:128`** (`02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC`) |
| **Source PRs (`J3270`)** | HOS PR [`#724`](https://github.com/TheLaughingGod1986/history-of-science/pull/724) (`macbook/J3270`, contains both `128` and `129`) · OWB PR [`#1156`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1156) (`macbook/J3270`, appends `HOS:128` & `HOS:129` to `jobs/WIP.json` `next_hos`) |
| **Rule-E Verdict — `HOS:128`** | **GO (`97.1 / 100` · `9.71 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`Why Do We Use AC Instead of DC? (Edison vs Tesla)`, `49 chars <= 50` Rule 15 & Rule 26; `Title B` `Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents`, `61 chars <= 70`; `Title C` refined to `Why Do We Use AC Instead of DC? (The 1886 Transformer Bet)`, `58 chars <= 70`; `0` exact title collisions across all 3 long titles and both `16–19 s` Short titles) |
| **Production & Claim Guard** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** Active `WIP.json["active"]` holds `4 / 4` HOS slots (`HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes awaiting verbatim primary-source quotes in `SOURCES.md` and `facts` lane (`gemini-agy`) verification when an active HOS WIP slot opens. |
| **Merge Note** | Isolated HOS review PR (`gemini/J3346`) touches only `02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/` so it never conflicts with `J3347` (Rule-E review of `HOS:129`). Neither HOS PR `#724` nor OWB PR `#1156` is merged here because both include `HOS:129`, whose Rule-E review (`J3347`) is still open. |
| **Spend** | `£0.00` / `0` credits |

---

## 1. Executive Summary & Audit Fixes Applied

`HOS:128` (*Why Do We Use AC Instead of DC? (Edison vs Tesla)*) from `J3270` passes all `10 / 10` `AGENTS.md` Rule-E and `STUDIO_PLAYBOOK.md` §2 gates with a **`97.1 / 100` (`9.71 / 10` Opportunity Score) GO** verdict in `jobs/WIP.json` `next_hos`, with three targeted packaging/precision refinements applied on isolated HOS branch `gemini/J3346`:

1. **Fixed Thumbnail B §2.5 title-word repetition (`RESOLVED`):** Changed Thumb B cover text from `AC BEAT DC` (repeated `AC` and `DC` straight from Titles A/B/C, violating `studio/RULES.md` line 215 & `THUMBNAIL_AND_TITLE_RULES.md` §2.5 *Cover text never repeats the title*) to **`HIGH VOLTAGE`** (`2 words`, gold on `HIGH`, zero overlap with Titles A/B/C, naming the rivalry's core engineering dare). Thumb A (`1 MILE LIMIT`) and Thumb C (`26 MILES AWAY`) pass cleanly.
2. **Fixed Title C transformer year conflation & re-verified `0` collisions (`RESOLVED`, `£0.00`):** Changed Title C from `Why Do We Use AC Instead of DC? (The 1888 Transformer Bet)` to **`Why Do We Use AC Instead of DC? (The 1886 Transformer Bet)`** (`58 chars <= 70`), separating William Stanley's March 1886 Great Barrington transformer demonstration from Nikola Tesla's May 1888 polyphase induction-motor patents. Verified `0` exact YouTube title collisions via `public_search.py` and added the query into `11_Upload-Package/evidence_2026-11-22_public_search.json` (`11` queries total, `0` empty searches, `0` exact collisions across all `5` candidate titles).
3. **Improved physics precision & Shorts template alignment + added review sheets (`RESOLVED`):**
   - Updated `TOPIC.md` §4 cold open from attributing $P_{\text{loss}} = I^2 R$ solely to Ohm's law to **Joule heating combined with Ohm's law ($P_{\text{loss}} = I^2 R$, $V = IR$)** and clarified `50/60 Hz` cycles vs `100/120` direction reversals per second.
   - Added a Ben 19 Nov 2026 `16–19 s` Shorts house-rules precedence header to `10_Shorts/README.md` (which had copied the legacy `22–27 s` template).
   - Added `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` (`10 / 10` Rule-E gates `PASS` + full script-stage sourcing guardrails, including Pearl Street 110 V / three-wire verification, Gaulard/ZBD/Stanley/Westinghouse/Tesla/Ferraris attribution, anti-Topsy-myth guard, Niagara-to-Buffalo transmission mileage verification, and year-accurate `WHO` cards) and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (`9.71 / 10` = `97.1 / 100`).
   - Confirmed `hos-search-2027-01` (`J3224`) is accurately labelled `pending Ben's OK` (`needsBen` in `studio/plan.json` per `LEARNINGS.md` rule 34 item 7) and that `HOS:128` independently passes every currently in-force HOS topic gate.

---

## 2. Rule-E Rubric Summary (`10 / 10 PASS`)

- **Neighbour demand (`neighbours.py`, `2026-11-22`):** **PASS** — `8` raw / `6` strictly on-topic education videos `>=1,000,000` views, `hasTed = true`, `failedQueries = []`: `Veritasium` `28,293,671` (`bHIhgxav9LY`) & `12,838,937` (`oI_X2cMHNe0`), `TED-Ed` ★ `3,624,109` (`yc2-363MIQs`), `Thoughty2` `1,967,879` (`egCsQXuBGkQ`), `SciShow` `1,401,838` (`pPnGvjmIgZA`), `TED-Ed` ★ `1,041,472` (`0SMNYivhGsc`). `2` raw `>=1M` rows transparently excluded (`Khan Academy` Elon Musk `6.97M`, `TED-Ed` electric fish `3.64M`). Even excluding broader electricity/inventions TED-Ed rows leaves `4 >=1M` tightly focused electricity/Tesla education videos + `CrashCourse` `567k`, `TED` ★ `346k`, `FuseSchool` `100k`.
- **Signed-out YouTube autocomplete & Rule 26a ranking proof (`public_search.py`, `2026-11-22`):** **PASS** — `5` core queries verified `autocomplete = yes` (`"why do we use ac instead of dc"`, `"thomas edison vs nikola tesla"`, `"war of the currents"`, `"ac vs dc"`, `"who invented alternating current"`), ranking videos led by `ElectroBOOM` `S7C5sSde9e4` (`6,686,558`), `AddOhms` `vN9aR2wKv0U` (`3,067,900`), `Discovery UK` `pcrwTN5OEZY` (`1,603,939`), `Arvin Ash` `ag6ltdwqfms` (`1,472,705`), `Kathy Loves Physics` `NEkegQanD2I` (`1,194,597`), and `pharmacist` `Cidg4Xfpjmc` (`1,100,111`), with **`0` exact title collisions** across all `3` long titles and `2` Short titles (`11` queries).
- **Non-duplication (`Rule E` item 1):** **PASS** — zero overlap across `02_Video-Projects/` (`000–018`, `099–119`), open PRs (`120–127`, `129`), `ideas/011–095`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`008` = Franklin 1752 lightning; `ideas/019` = Galvani/Volta 1800 battery; `ideas/021` = Oersted/Faraday 1820–1831 induction).
- **Visual proof-first hook & Shorts (`Rules 10, 30` & Ben 19 Nov `16–19 s` Shorts rules):** **PASS** — physical apparatus in `0:05–0:15` (dimming 1882 Manhattan bulb / overheating copper cable → glowing brass step-up transformer); `2` named-entity question Shorts (`S01` `51c`, `S02` `43c`) planned to the `16–19 s` 3D-cartoon frame-0 concrete-fact-line-1 loop rules.
- **Unverified claims guard & Rule G WIP cap:** **PASS** — every historical/scientific claim remains **UNVERIFIED** pending `SOURCES.md` exact quotes + `facts` lane when an active HOS WIP slot opens; all `12` stages in `status.json` remain `"todo"`; `£0.00` spent.

---

## 3. Opportunity Score (`9.71 / 10` · `97.1 / 100`)

| Dimension | Weight | Score | Weighted |
|---|---:|---:|---:|
| 1. Evergreen search intent | 25% | `9.9` | `2.475` |
| 2. Competition gap | 20% | `9.6` | `1.920` |
| 3. Narrative & visual arc | 20% | `9.7` | `1.940` |
| 4. Brand & guardrail fit | 20% | `9.5` | `1.900` |
| 5. Series / cluster potential | 15% | `9.8` | `1.470` |
| **Total** | **100%** | — | **`9.705 / 10` (`97.1 / 100`)** |

---

## 4. Next Steps

1. Complete `J3347` (Rule-E review of `HOS:129` *How Was the Microwave Invented?*).
2. Chief merges the approved `HOS:128` (`gemini/J3346`) and `HOS:129` (`J3347`) review PRs (superseding raw HOS PR `#724`) plus OWB PR `#1156` (`jobs/WIP.json` `next_hos` append) and this OWB review PR (`gemini/J3346`).
3. Keep `HOS:128` in `jobs/WIP.json` `next_hos` under Rule G until an active HOS slot opens (or Ben approves `hos-search-2027-01` in `studio/plan.json` for Jan 2027 scheduling), at which point queue `SOURCES.md` + `facts` lane (`gemini-agy`) before script lock.
