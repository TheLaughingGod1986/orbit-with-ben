# Condition Verification & Script Lock Readiness Review — `J3027` (for `J3020` · `OWB:064`)

- **Verification Task:** `J3027` (`recheck_of: J3020`, `kind: review`)
- **Reviewer / Worker:** `gemini` (`Gemini 4 Argon (High)`, `review`-lane fallback while `claude` is out of usage until `2026-11-18T07:50:00Z`)
- **Timestamp (UTC):** `2026-11-18T05:13:00Z`
- **Target Film & Stage:** `OWB:064` (*Every Planet Explained in 10 Minutes (Mercury to Neptune)*, folder `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`), stage `script` (`J3020`, predecessor `J3011`, downstream VO `J3021`)
- **Condition Verdict:** **PREDECESSOR (`J3011`) & ALL `J3020` DELIVERABLES VERIFIED ON `main`, AWAITING PROTECTED CHIEF / CLAUDE SCRIPT LOCK** (`J3020` was drafted and verified by `gemini` as stand-in worker in commit `3b9f165c430fb8610bf73f96d0d973f595a67388`; under `AGENTS.md` *"a stand-in's draft is a draft only, Claude or Chief locks it"*, and `jobs.py` enforces elected-Chief authority on `reopen`, `wait --recheck`, and Chief stage completion).
- **Review-Lane Advisory on `064` Script Package (`3b9f165c43`):** **PASS — Ready for immediate Chief (`codex`) or `claude` script lock** (`review:script` **`93.1 / 100` PASS**, `gate:episode` **`PASS`**, `16 / 16` primary-source `SOURCES.md` rows and `MUST QUOTE` claims verified verbatim, `8,161` spoken characters / `1,246` spoken words within budget, £0 picture/music plan complete).

---

## 1. Waiting Condition & Predecessor Verification (`J3011` → `J3020`)

1. **Predecessor (`J3011`) & Ben Approval History:**
   - **Status:** `J3011` is **`done`** (completed by `codex` at `2026-11-17T23:39Z`, `PRs #1004` and `#1005` merged to `main`).
   - **Ben Topic Lock:** Verified in `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json`:
     - `stages.topic.state = "done"`, `ruling = "PASS"`, `ref = "jobs/reviews/J2875/REVIEW.md"`.
     - `locked`: `by: "Ben"`, `at: "2026-11-17"`, `evidence: "Ben, in chat: \"Lock it.\" Recorded by Claude in J3011 at 2026-11-17T18:44Z."`
   - **Reserved Slot & Schedule Guard:** `air: "2026-12-16"` (Wednesday 16 December 2026 at 18:00 London; finished cut due on Ben's watch board by Friday 11 December 2026 at 18:00 London). Zero dated films were moved, and `studio/plan.json` has `planets` dated with `needsBen` cleared.
   - **Spend Guard:** `£0.00` cash, `0` Flow/Vertex credits, `0` ElevenLabs credits spent in `J3011` or `J3020`. Live ElevenLabs subscription pool has `67,893 / 121,114` characters remaining (`£0.00` cash), which comfortably covers `064`'s `8,161` spoken characters alongside the `42,000`-character WW2 pilot allocation.

2. **Deliverables of `J3020` on `origin/main` (Commit `3b9f165c430fb8610bf73f96d0d973f595a67388`):**

| Requirement (`J3020` & `studio/RULES.md`) | File(s) on `origin/main` (`3b9f165c43`) | Verification Result (`2026-11-18T05:12Z`) | Verdict |
|---|---|---|---|
| **Master Script & Exact Hash** | `01_Script/every_planet_explained_script_master_v01.md` & `01_Script/episode_script_draft_v01.md` | Identical files (`25,243` bytes), `SHA-256: c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae`. Continuous outward tour covering all 8 planets in order (`Mercury → Venus → Earth → Mars → Jupiter → Saturn → Uranus → Neptune`) plus `034` Pluto hand-off. | **PASS** |
| **Word Count & Spoken Character Budget** | `01_Script/SCRIPT_NOTES_v01.md` | `1,246` spoken words (`1,290` alphanumeric tokens · `1,352` reviewer words, within the `1,200–1,300` spoken-word lock) and **`8,161` spoken characters** (`~508.6 s` speech + card breaths + `18 s` end hold = `~592 s` / `9 min 52 s`), matching the `~8,000`-character VO scope. | **PASS** |
| **First 30 Seconds & Structure** (`studio/RULES.md` Lesson 7 / `J2428` / HOTU-SEA) | `01_Script/every_planet_explained_script_master_v01.md` | Opens straight on Mercury (`Frame 0` real NASA MESSENGER global mosaic `PIA19411` rotating in sunlight) with the title mystery and first concrete numbers (`430 °C` day vs `−180 °C` night at `58M km`, `7×` brighter sunlight) in sentences 1–2 (`<0:08` and `<0:20`). Zero agenda/meta-promise, zero chapter card before `0:45`. Midpoint twist (*"Case closed? Wrong — there is no solid surface"*) at Jupiter (`~55%`). | **PASS** |
| **Automated Script Gate (`review:script`)** | `07_Content-Ops` CLI | **`PASS · 93.1 / 100`** (threshold `≥90`; `hook: 10`, `curiosity: 9.5`, `storytelling: 8`, `scientificAccuracy: 10`, `emotion: 9.2`, `escalation: 10`, `retentionPotential: 9`, `searchPotential: 8.7`, `visualOpportunities: 9.5`, `narrationFlow: 9.2`). | **PASS** |
| **Automated Episode Gate (`gate:episode`)** | `07_Content-Ops` CLI | **`PASS — VO / Gemini Veo allowed`** (`prebuild_vidiq` OK, `script_file` OK, `script_review` `93.1/90` OK, `orbit_acts` `2` OK, `subscribe_beat` at `35%` / `15` words OK, `visual_must` `8` OK, `teach` `8` OK, `chapters` `7` OK, `production_checklist` OK). | **PASS** |
| **Teach on Screen, Scale & Per-Chapter Number Objects** | `01_Script/every_planet_explained_script_master_v01.md` | `DATA: 8` (`≥3`), `SCALE: 8` (`= DATA`), `WHO: 7` (`100%` of named people at first mention with LOC-verified years and `≤4-word` roles), `WHEN: 8`, `FACT: 4` (`2–4`, all `≤4 words`), `NUMBER OBJECT: 8` (`8/8` chapters). | **PASS** |
| **Primary-Source `SOURCES.md` & Quote Checks** | `01_Script/SOURCES.md`, `01_Script/GEMINI_QUOTE_PASS_v01.md`, `01_Script/CLAUDE_QUOTE_CHECK_v01.md` | `16 / 16` rows verified against live primary sources (`53 / 53` HTTP 200 URLs across NASA Science, NSSDCA, Photojournal, ESA/Hubble, BGS, WMO, PubMed, OpenAlex, arXiv, LOC). Corrects all 4 concept-sheet approximations (`Olympus Mons 21.3 km >2× Everest`, `Opportunity 56×`, `Cassini 0.41 Mimas masses / 10–100 Myr`, `Saturn hexagon 322 km/h vs 2,000-km eye 330 mph`). | **PASS** |
| **No-Generation Picture & Film-Specific Music Plan** | `01_Script/SCRIPT_NOTES_v01.md`, `05_Music/MUSIC_BRIEF_v01.md`, `05_Music/every_planet_score_bed_v01_plan.json` | Resolves `TOPIC_GO_NO_GO_SHEET.md` §5.1's *"shelf music bed"* conflict by specifying a dedicated film-specific score (`05_Music/every_planet_score_bed_v01.mp3`, `Pace: 68-76 BPM`, full `NOT:` list excluding `020`–`034`, `explain`/`awe` chapter shifts) synthesised at `£0` in `J3022`/`J3023` to pass `music_gate.py`. | **PASS** |

3. **Why `J3020`'s Waiting Condition Remains Unmet (`status = "blocked"`):**
   - `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json` currently reads `"script": {"state": "blocked"}`.
   - Neither the elected Chief (`codex`) nor `claude` has yet recorded the explicit script lock on `064` master v01 (`c9945afa...`) or closed `J3020` to release `J3021` (VO).
   - Under `AGENTS.md` (*Who does what* & *Ordinary workers never make a protected call*) and `scripts/jobs.py` (`set_wait` line 533: `"Only the elected Chief may record a condition check"`; `do_reopen` line 964: `"Only the elected Chief may release a verified hold"`), a `gemini` specialist worker cannot self-lock a stand-in script draft or execute `wait --recheck` / `reopen`.

---

## 2. Action for Elected Chief (`codex`) or `claude`

All technical, factual, and automated gates for `J3020` (`OWB:064` script stage) are verified **`PASS`** on `origin/main` (`3b9f165c43`). The elected Chief (`codex`) can immediately resolve both `J3020` and `J3027` via **Option A** (or defer to `claude` at `07:50Z` via **Option B**):

- **Option A — Lock `064` Script Now & Unblock `J3021` (Recommended):**
  1. Update `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json` so `stages.script` has `"state": "done"`, `"ruling": "PASS"`, `"ref": "jobs/reviews/J3027/REVIEW.md"`, and `"locked": {"by": "codex", "at": "2026-11-18", "sha256": "c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae"}`.
  2. Reopen and complete `J3020` as Chief (`python3 scripts/jobs.py reopen J3020 --agent codex --note "Chief script lock recorded on 064 master v01 (3b9f165c43, SHA-256 c9945afa...)" --git && python3 scripts/jobs.py next --id J3020 --agent codex --can mini,any --git && python3 scripts/jobs.py done J3020 --agent codex --result "Chief PASS & script lock on 064 every_planet_explained_script_master_v01.md (SHA-256 c9945afa..., 93.1/100, 1,246 spoken words / 8,161 chars, 16/16 SOURCES.md & quote checks PASS); J3021 VO released" --ref jobs/reviews/J3027/REVIEW.md --git`).
  3. Close `J3027` (`python3 scripts/jobs.py reopen J3027 --agent codex --note "J3020 script locked and closed" --git && python3 scripts/jobs.py next --id J3027 --agent codex --can mini,any --git && python3 scripts/jobs.py done J3027 --agent codex --result "Verified J3020 deliverables and recorded Chief script lock on OWB:064; J3021 VO released" --ref jobs/reviews/J3027/REVIEW.md --git`).

- **Option B — Hold `J3020` Until `claude` Returns (`2026-11-18T08:00:00Z`):**
  1. `python3 scripts/jobs.py wait J3020 --agent codex --type input --recheck J3027 --check-at 2026-11-18T08:00:00Z --condition "Awaiting Chief or Claude (up after 2026-11-18T07:50:00Z) explicit script lock on 064 master v01 (commit 3b9f165c43)" --action "Chief or Claude records explicit script lock on 064 master v01 (commit 3b9f165c43) and closes J3020 to release J3021 VO" --git`
  2. Reopen and close `J3027` (`--ref jobs/reviews/J3027/REVIEW.md`).
