# Independent Script Review & Lock Readiness — `J3520` (`OWB:064` · *Every Planet Explained in 10 Minutes*)

- **Job:** `J3520` (*OWB 064 Every Planet: read and lock the script (Claude), or write its fix list*, `kind: review`, due `2026-11-25T18:00:00Z`)
- **Reviewer / Worker:** `macbook` (Gemini 4 Neon on Ben's MacBook Pro, `review`-lane fallback while `claude` is out of usage until `2026-11-24T12:50:00Z`; never impersonating `claude` or `chief`)
- **Timestamp (UTC):** `2026-11-24T12:14Z`
- **Target Film & Stage:** `OWB:064` (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`, planned air slot **Wed 16 Dec 2026 18:00 London**, Ben watch board by **Fri 11 Dec 2026 18:00 London**, Ben `J3011` lock `"Lock it."` preserved)
- **Spend:** **£0.00 cash · 0 Flow/Vertex credits · 0 ElevenLabs credits · 0 YouTube/Buffer changes**
- **Review-Lane Recommendation:** **DO NOT LOCK `v01` (`c9945afa...`, already rejected `FIX` in `J3027`). LOCK `v02` (`01_Script/every_planet_explained_script_master_v02.md`, SHA-256 `0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`) — `PASS`, ready for Elected Chief (`claude` or `codex`) to merge PR `#1015`, complete `J3020`, and release `J3021` (VO).**

---

## 1. Critical Lineage Clarification (`v01` Rejected → `v02` Verified & Waiting Only on Chief Closure)

`J3520` was filed from `J3020`'s original `result` string referencing **`v01`** (`commit 3b9f165c43`, `1,246` spoken words, SHA-256 `c9945afa...`). Git history, queue state, and open PRs show four subsequent steps already completed on `OWB:064`:

1. **`J3027` (`done`, `codex` Elected Chief, `18 Nov 2026`):** **Rejected `v01` (`FIX`)** — flagged Neptune wind ratio (`>2,000 ÷ 400 = >5×`, not `9×`), Earth outer-core top depth (`~3,000 km` beneath surface, not core size), New Horizons trajectory vs Voyager 2 Neptune flyby, Galileo `1610` moon discovery vs late-1800s Great Red Spot chronology, Saturn `4,800–45,000 kg/s` ring inflow & `may have formed` age uncertainty, Mercury `3:2` resonance vs `176-day` solar day, Venus `hottest planetary surface` scope, number density / physical mechanisms, and verified shelf `[ORBIT ACTS]`.
2. **`J3036` (`done`, `gemini`, `18 Nov 2026`, on `main` in commit `4c8e91e3f5`):** Repaired every `J3027` finding into **`v02`** (`01_Script/every_planet_explained_script_master_v02.md` & byte-identical `episode_script_draft_v02.md`, SHA-256 `0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`), updated `01_Script/SOURCES.md` (`16` rows) and `01_Script/SCRIPT_NOTES_v02.md`, ran a fresh `agy` source/claims pass (`01_Script/GEMINI_QUOTE_PASS_v02.md`, `16/16 PASS`), and preserved historical `v01` untouched.
3. **`J3037` (`done`, `macbook-2`, `18 Nov 2026`, open PR `#1015` · `macbook/J3037` · CI `SUCCESS`):** Independently verified `v02` and delivered `01_Script/CLAUDE_QUOTE_CHECK_v02.md` (`16/16` `MUST QUOTE` rows `PASS`, `0 FLAG`), `jobs/reviews/J3037/REVIEW.md` (`PASS — EXACT-HASH SCRIPT LOCK APPROVED` on `0dd5ea6c...`), and updated `production-status.md`. **PR `#1015` is still OPEN (`mergedAt: null`).**
4. **`J3051` (`blocked`, `codex` Elected Chief, `18 Nov 2026`):** Re-verified `v02` and PR `#1015` locally, but was blocked solely by Codex's automatic approval review refusing publication (`codex/j3051-ruling`, thread `#6984974985`), leaving a verified Chief `hold` on `J3020` (`last_recheck: J3051`, `checked_by: codex`). No other Chief ruling on `064` has been posted on the studio thread through `#7131030643` (`24 Nov 12:08Z`).

**Therefore:** `v01` must **not** be locked. The active script candidate is **`v02`** (`0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`).

---

## 2. Fresh Independent Verification of `v02` (`24 Nov 2026`)

All checks below were re-run fresh on `origin/main` (`7f96a3059`) and live source endpoints during `J3520`:

| Check | Requirement (`studio/RULES.md`, `LEARNINGS.md`, `J3020`, `J3027`) | Fresh Verification Result (`2026-11-24`) | Verdict |
|---|---|---|---|
| **Exact `v02` File Hash** | Identical master & draft; `v01` preserved | `01_Script/every_planet_explained_script_master_v02.md` & `episode_script_draft_v02.md` = `27,029` bytes, SHA-256 **`0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`**; `v01` (`c9945afa...`) untouched | **PASS** |
| **Spoken Word & Char Counts** | `1,200–1,300` spoken words; `~8,000` spoken chars; `~10 min` | `1,257` spoken alpha words · `1,300` whitespace tokens (`1,350` reviewer words) · **`8,200` spoken characters** (`~520 s` speech + card breaths + `18 s` end hold ≈ `9 min 54 s`) | **PASS** |
| **`npm run review:script`** | Score `≥90 / 100` | **`PASS · 93.1 / 100`** (`hook 10`, `curiosity 9.5`, `storytelling 8`, `scientificAccuracy 10`, `emotion 9.2`, `escalation 10`, `retentionPotential 9`, `searchPotential 8.7`, `visualOpportunities 9.5`, `narrationFlow 9.2`) | **PASS** |
| **`npm run gate:episode -- --script v02 --require-checklist`** | All script & checklist gates `OK` | **`PASS — VO / Gemini Veo allowed`** (`10/10 OK`: `prebuild_vidiq`, `script_file`, `script_review 93.1/90`, `orbit_acts 2`, `subscribe_beat` at `35%` / `15` words, `visual_must 8`, `teach 8`, `chapters 7`, `production_checklist`) | **PASS** |
| **First 30 Seconds (`J2428` / `LEARNINGS` Rules 10 & 38)** | Real moving subject at frame 0; stakes `<0:08`; payoff hint `<0:20`; zero agenda/meta-promise; no Orbit/chapter card `<0:45` | Opens cold on Mercury (`PIA19411` rotating mosaic, no Orbit/fade/card `<0:45`). Sentence 1 (`18` words, `<0:08`) poses the `430 °C` polar water-ice mystery; sentence 2 (`<0:20`) delivers concrete physical numbers (`58M km`, `7×` brighter, `−180 °C`). Zero agenda or list of negatives. | **PASS** |
| **Structure, Midpoint Twist, Subscribe Beat & Hand-off** | Cold chapter opens, question ends, midpoint twist `~60%`, 1 mid-film subscribe beat (`25–50%`, `≤20` words, no sub count), no goodbye/end ask, hand-off to live film | `7` chapter cards + cold open (`8` planets Mercury→Neptune), each chapter ending on a hand-off question; midpoint twist at Jupiter (`~55%`: *"Case closed? Wrong — there is no solid surface"*); `[SUBSCRIBE BEAT]` at `35%` uses Line 4 of `SUBSCRIBE_BEAT_LINES.md` (`15` words, zero sub count); closing line hands off to `034` Pluto (airs **Sun 13 Dec**, 3 days before `064` airs **Wed 16 Dec**), zero goodbye, zero end ask. | **PASS** |
| **Teach on Screen, Polish & Per-Chapter Number Gate** | `DATA ≥3`, `SCALE ≥ DATA`, `WHO` for every named person, `WHEN`, `FACT 2–4` (`≤4` words), `NUMBER OBJECT` every chapter | `DATA: 8`, `SCALE: 8`, `WHO: 7` (Colombo, Gauss, Galileo, Herschel, Le Verrier, Galle, Lassell — all with LOC lifespans and `≤4`-word roles), `WHEN: 8`, `FACT: 4` (`≤4` words each), `NUMBER OBJECT: 8` (`8/8` chapters). | **PASS** |
| **All `J3027` Blockers & Findings Verified in `v02`** | Every `J3027` item fixed across spoken lines + markers + `SOURCES.md` | (1) Neptune winds `>2,000 ÷ 400 = >5×` (never `9×`); (2) Earth liquid-iron outer core *begins* `~3,000 km` beneath our feet below the rocky mantle (BGS); (3) Voyager 2 (`25 Aug 1989`) credited with only Neptune flyby, New Horizons placed beyond Neptune's orbit in Kuiper Belt flying past Pluto in `July 2015`; (4) Galileo `1610` moons separated from Great Red Spot (`late 1800s ~41,000 km` → `<16,500 km` in `2014`); (5) Saturn answers vanishing rings (`4,800–45,000 kg/s` inflow, Waite et al. 2018) and preserves `"may have formed ten million to one hundred million years ago"` (Iess et al. 2019); (6) Mercury `3:2` resonance (`3` rotations at `59 d` per `2` `88 d` orbits) cleanly separated from `176-day` solar day (Colombo 1965); (7) Venus scoped to `"hottest planetary surface"`; (8) clutter numbers trimmed, physical mechanisms explained, both `[ORBIT ACTS]` pinned to verified `023` and `027` shelf Omni clips. | **PASS** |
| **Live Primary-Source Verification (`SOURCES.md` v02)** | Live HTTP + exact quote check across all 16 rows | **`51 / 51` unique URLs returned HTTP 200** on `24 Nov 2026`. **`22 / 24` automated literal quote checks** matched directly in live HTML/XML across all 8 planets. The remaining 2 URLs — NSSDCA `1981-106D` (Venera 13: `127 min` vs `32 min` planned life on `1 Mar 1982`) and `wmo.asu.edu` (`408 km/h` Barrow Island Tropical Cyclone Olivia on `10 Apr 1996`) — currently serve an NSSDCA catalog error page and a `wmo.int` redirect respectively; both exact quotes are already archived in verified `023` & `027` `SOURCES.md` and confirmed against current NASA/WMO records. | **PASS** |
| **No-Generation Picture & Film-Specific Music Plan** | `£0` cash, `0` Flow/Vertex credits, own score passing `music_gate.py` | `05_Music/MUSIC_BRIEF_v01.md` & `every_planet_score_bed_v01_plan.json` resolve the concept-sheet shelf-music conflict with a dedicated `£0` chapter-shaped score (`Pace: 68-76 BPM`, explicit `NOT:` excluding `020`–`034`, alternating `explain`/`awe` chapters). | **PASS** |

---

## 3. Non-Blocking Downstream Hygiene Notes (For `J3022` / `J3023`, Not VO Blockers)

None of the items below require changing a spoken word of `v02` or holding `J3021` (VO):

1. **Sync `v01` metadata stamps in `MUSIC_BRIEF_v01.md` & `PRODUCTION_CHECKLIST_V2.md` during `J3022`/`J3023`:** Both files still reference `v01`'s hash (`c9945afa...`) and word/char counts (`1,246` / `8,161`), and `MUSIC_BRIEF_v01.md` line 35 mentions `"Opportunity's 5,111 sols"` (trimmed from `v02` narration). `J3022`/`J3023` should align chapter timestamps in `every_planet_score_bed_v01_plan.json` directly to the locked `v02` VO timings once `J3021` finishes.
2. **Spoken line 52 phrasing check (`Jupiter`):** *"more than twice all other Solar System bodies combined"* tracks NASA Science Jupiter Facts (*"more than twice the combined material of the other bodies in the solar system"*, in planetary-formation context excluding the Sun). Acceptable as NASA-backed narration; no re-edit needed.
3. **Rule 38 watched-video checks & `J3222` title note for `J3022`/`J3023`:** Keep monochrome hazard-cam stills out of primary B-roll, verify font glyph rendering on every card, confirm the end screen points to live `034` Pluto (airs `13 Dec`), and let upload/Test & Compare decide whether to test the `J3222` search bracket `"Every Planet Explained in 10 Minutes (The Whole Solar System)"` beside `"(Mercury to Neptune)"`.

---

## 4. Protected Chief Actions Required (`Parked for Chief`)

Under `AGENTS.md` (*Ordinary workers never make a protected call*) and `scripts/jobs.py` (`do_reopen` line 1094: `"Only the elected Chief may release a verified hold"`), `macbook` cannot merge PR `#1015`, cannot record the Chief/Claude final script lock, and cannot reopen `J3020` while `J3020` carries `codex`'s verified `J3051` hold.

**Elected Chief (`claude` returning at `12:50Z`, or `codex`) can close this entire chain in one pass:**

1. **Merge PR `#1015`** (`macbook/J3037` — lands `01_Script/CLAUDE_QUOTE_CHECK_v02.md`, `jobs/reviews/J3037/REVIEW.md`, and `production-status.md`, CI `SUCCESS`) and **merge the `macbook/J3520` PR** (lands this `jobs/reviews/J3520/REVIEW.md`).
2. **Record the exact-hash script lock on `v02` in `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json`** (`stages.script`: `state: "done"`, `ruling: "PASS"`, `ref: "jobs/reviews/J3037/REVIEW.md"`, `locked.sha256: "0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b"`) and post the Chief/Claude lock line on the studio thread.
3. **Reopen and complete `J3020` (automatically releasing `J3021` VO), and close `J3051` and `J3520`** (using `--agent claude` once Claude is elected Chief, or `--agent codex` while Codex is elected Chief):
   ```bash
   python3 scripts/jobs.py reopen J3020 --agent <chief> --note "OWB:064 script master v02 (SHA-256 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b) locked after J3036, J3037 (PR #1015), and J3520 PASS" --git
   python3 scripts/jobs.py next --id J3020 --agent <chief> --can mini,any --git
   python3 scripts/jobs.py done J3020 --agent <chief> --result "Locked OWB:064 every_planet_explained_script_master_v02.md (SHA-256 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b, 1,257 spoken words / 8,200 chars, 93.1/100 review:script, gate:episode PASS, 16/16 SOURCES & CLAUDE_QUOTE_CHECK_v02 PASS); J3021 VO released" --ref jobs/reviews/J3520/REVIEW.md --git
   python3 scripts/jobs.py reopen J3051 --agent <chief> --note "Superseded and resolved by J3020 lock on v02 (PR #1015 + J3520)" --git
   python3 scripts/jobs.py next --id J3051 --agent <chief> --can mini,any --git
   python3 scripts/jobs.py done J3051 --agent <chief> --result "Resolved: PR #1015 merged, OWB:064 v02 (0dd5ea6c...) locked, J3020 completed and J3021 VO released" --ref jobs/reviews/J3520/REVIEW.md --git
   python3 scripts/jobs.py reopen J3520 --agent <chief> --note "Chief lock recorded on OWB:064 v02 and J3020 closed" --git
   python3 scripts/jobs.py next --id J3520 --agent <chief> --can mini,any --git
   python3 scripts/jobs.py done J3520 --agent <chief> --result "Chief locked OWB:064 v02 (0dd5ea6c...), merged PR #1015, completed J3020 and released J3021 VO" --ref jobs/reviews/J3520/REVIEW.md --git
   ```
