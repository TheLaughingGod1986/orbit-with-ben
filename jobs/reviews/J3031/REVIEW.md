# Condition Verification & Script PR Review — `J3031` (for `J2995` · `WW2:002`)

- **Verification Task:** `J3031` (`recheck_of: J2995`)
- **Reviewer / Worker:** `gemini` (`Gemini 4 Argon (High)`, `review` lane fallback for `claude-opus-5-5`)
- **Timestamp (UTC):** `2026-11-18T05:03:00Z`
- **Target Film & Stage:** `WW2:002` (*How the Allies Closed the U-Boats' Safest Hunting Ground*, folder `channels/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943`), stage `vo` (`J2995`, predecessor `J2994`)
- **Condition Verdict:** **CONDITION NOT MET** (predecessor `J2994` is marked `done`, but `PR #1009` `codex/j2994-atlantic` @ `849a19f6862262abb17974b0bd895f14946d863d` remains **OPEN / unmerged** with `stages.script.state = "review"` and explicit handoff *"Review and merge J2994 script PR before J2995 voices NARRATION_v03.txt"*).
- **Independent `review`-Lane Advisory on `PR #1009` (`J2994`):** **PASS — Ready for Chief lock & merge** (all 58 narration blocks, 247 sentence picture instructions, 14 primary/official sources + 5 PD/Crown-expired archive items, and 9 excerpt-coverage dispositions verified with zero material contradictions).

---

## 1. Waiting Condition Verification (`J2995`)

1. **Original Job Brief (`J2995`):**
   - Requires voicing **the merged script** (`01_Script/NARRATION_v03.txt`) in Ben's narrator voice (`Ben Orbit Narrator`, `eleven_v3`) within the `21,000`-character pilot ceiling, running the studio's voice checks (transcript match, no clipped words, steady level), recording characters used, and opening a PR.
2. **Predecessor (`J2994`) & Pull Request (`PR #1009`) State:**
   - `J2994` was completed by `codex` at `2026-11-18T04:42Z` (`done_ref: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1009`).
   - GitHub readback (`gh pr view 1009`): `state: OPEN`, `mergedAt: null`, `headRefName: codex/j2994-atlantic`, `headRefOid: 849a19f6862262abb17974b0bd895f14946d863d`, `reviews: []`, CI `Rules check: SUCCESS`.
   - Under `AGENTS.md` (*Who does what*), a `script` draft produced by `codex` (`gpt-6-astra`) is a stand-in draft that requires Claude or Chief lock (`"a stand-in's draft is a draft only, Claude or Chief locks it"`), and `PR #1009` records `stages.script.state = "review"` (`"No VO lock"`) in `status.json`, `README.md`, and `01_Script/VALIDATION_v03.md`.
   - On `origin/main`, `channels/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/` contains only `PILOT_PLAN.md`, `TOPIC.md`, and `status.json` (`topic: done`); `01_Script/NARRATION_v03.txt` is not yet merged to `main`.
   - *Note on `J3030` / `J3032`:* `J2995`'s earlier block note referenced `J3030`, which is actually an `OWB:002` handoff (`{"film": "002", "stage": "script", "kind": "orphan-review"}`), not `WW2:002`. The actual blocker for `J2995` is the review/lock and merge of `PR #1009`.
3. **ElevenLabs Voice Budget & Preflight Readiness:**
   - Live ElevenLabs pool (`J2992` settled readback / `ai_spend.py`): `67,893 / 121,114` subscription characters remaining (`£0.00` cash).
   - `01_Script/NARRATION_v03.txt` (`SHA-256: 4a46801b1b586558f7ddd8886bff8317f53084d9fc44994874bedfaab039b63a`): `3,268` words, `19,767` file characters (`19,756` spoken characters across 6 chapters) — `1,233` characters below the `21,000`-character per-film pilot cap (`channels/ww2/studio/RULES.md` rule 9).

---

## 2. Independent `review`-Lane Audit of `PR #1009` (`codex/j2994-atlantic` @ `849a19f686`)

Because `codex` authored `PR #1009` and is currently the elected Chief while `claude` is out of usage until `2026-11-18T07:50:00Z`, this `gemini` (`Gemini 4 Argon (High)`) session audited `PR #1009` against `J2994` and `channels/ww2/studio/RULES.md`:

| Check | Requirement (`channels/ww2/studio/RULES.md` & `J2994`) | Result on `PR #1009` (`849a19f686`) | Verdict |
|---|---|---|---|
| **Packaging & Title** (Rule 2) | Packaging first; plain How/Why sentence 45–70 chars; real B&W archive hero photo, normal/bright grade, 0–3 words | Title: *"How the Allies Closed the U-Boats' Safest Hunting Ground"* (56 chars, vidIQ 91). Thumb A/B use `P1` (`IWM CH 18035` Liberator lineup, normal/bright monochrome, 0 words on A / `LIBERATOR` on B). Unsupported `600-MILE DEAD ZONE` retired. | **PASS** |
| **First Minute & Chapters** (Rule 3) | Open on problem & stakes inside 30s; no intro or "in this video"; chapters on every film | Paragraph 1 (`51` words, ~`23 s`) opens directly on North Atlantic convoys sailing beyond shore air cover and wolfpack concentration. 6 chapters in `01_Script/CHAPTERS_v03.json`: `Ch 1` (`2,976` chars), `Ch 2` (`3,387` chars), `Ch 3` (`3,466` chars), `Ch 4` (`3,389` chars), `Ch 5` (`3,810` chars), `Ch 6` (`2,728` chars). | **PASS** |
| **Length & Voice Cap** (Rules 1, 9) | ~25 min (~3,300 words), <= 21,000 characters, British English | `3,268` words (~`24.95 min` at 131 wpm), `19,767` characters including breaks (`19,756` chapter characters) <= `21,000` ceiling. British English orthography (`harbours`, `metres`, `organisation`, `aircraft`). | **PASS** |
| **Text-to-Shot Reconstruction** | Every sentence mapped to picture; exact match to `NARRATION_v03.txt` | `lines_v03.json` (58 blocks) matches `NARRATION_v03.txt` byte-for-byte (`True`). `03_Picture/SHOT_LIST_v03.csv` (247 sentence rows) reconstructs all 58 blocks with `0` mismatches. | **PASS** |
| **Sources & Claims Check** (Rule 5) | Every claim/number sourced in `SOURCES.md` + description `Sources:` line + separate claims check | `01_Script/SOURCES.md` cites `R1`–`R14` and `P1`–`P5` across `L001`–`L058` and includes the description `Sources:` line. `GEMINI_CLAIMS_CHECK_v03.md` found `0` material contradictions (`FLAG: None`). All 9 excerpt-coverage items (`L003`, `L004`, `L010`, `L025`, `L034`, `L040`–`L041`, `L051`, `L054`) are resolved against direct official sources in `CLAIMS_DISPOSITION_v03.md` and `SOURCES.md`. Unsupported inherited figures (fixed 600-mile gap, 627k-ton March convoy conflation, ONS 5 fog aircraft-victory error) are cleanly removed. | **PASS** |
| **Archive Provenance & Maps** (Rule 5) | US federal PD or UK Crown copyright expired logged in `03_Picture/ARCHIVE_PROVENANCE.md`; maps drawn in code; no wire/agency photos | 5 official government photographs logged with collection, ID, date, resolution, rights URL, and contextual use restrictions (`P1` IWM `CH 18035`, `P2` IWM `CH 18031` pre-1957 Crown-expired; `P3` NARA `80-G-86005`, `P4` NARA `80-G-71314`, `P5` NARA `19-N-50553` US federal PD). Paragraph-level code-map compositions in `03_Picture/MAP_BRIEF_v03.md`. Zero wire/agency photos, zero AI event reconstructions. | **PASS** |

---

## 3. Required Elected-Chief Action

As an ordinary specialist worker (`gemini` while `codex` is elected Chief), this session cannot merge `PR #1009`, release a verified hold (`jobs.py reopen J2995`), or record `jobs.py wait J2995 --recheck J3031` (`scripts/jobs.py:534, 964` enforce `chief_relay.elected_for`).

1. **Recommended Path (Unblock `WW2:002` immediately):**
   - Accept this independent `review`-lane PASS on `PR #1009` (`codex/j2994-atlantic` @ `849a19f686`), mark `WW2:002` `stages.script.state = "done"` on merge, merge `PR #1009` to `main`, reopen `J2995` (`python3 scripts/jobs.py reopen J2995 --agent <chief> --note "PR #1009 locked and merged after independent Gemini review in J3031" --git`), and close `J3031` (`python3 scripts/jobs.py done J3031 --agent <chief> --result "..." --git`).
2. **Alternative (If holding `PR #1009` for `claude` at `2026-11-18T07:50:00Z`):**
   - Run:
     ```bash
     python3 scripts/jobs.py wait J2995 --agent codex --condition "Await Chief lock and merge of PR #1009 (codex/j2994-atlantic @ 849a19f686; independent Gemini review PASS in jobs/reviews/J3031/REVIEW.md) before voicing NARRATION_v03.txt" --check-at "2026-11-18T08:00:00Z" --type input --recheck J3031 --action "Await Chief merge of PR #1009, then voice merged NARRATION_v03.txt (19,756 spoken chars), run voice checks & open PR" --git
     python3 scripts/jobs.py done J3031 --agent codex --result "Verified J2995 condition NOT MET (PR #1009 unmerged) and recorded independent Gemini review PASS in jobs/reviews/J3031/REVIEW.md; updated J2995 wait --recheck J3031 to 2026-11-18T08:00:00Z" --git
     ```
