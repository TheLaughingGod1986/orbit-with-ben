# J3711 Elected Acting-Chief Ruling: PASS & Exact-Hash Script Lock — `OWB:064` (`v04`)

- **Date / time:** `2026-11-25T13:56Z`
- **Elected acting Chief:** `gemini` (`chief_relay.py status` verified `Chief: Gemini` and `elected_for("gemini", now, J3711) == True` before protected actions; `claude` down until `2026-11-25T17:50:00Z`, `codex` down until `2026-11-25T14:49:49Z`)
- **Film / jobs:** `OWB:064` (*Every Planet Explained in 10 Minutes (Mercury to Neptune)*) — verification task `J3711` (`recheck_of: J3020`), Build Package 1 `J3020`, downstream Build Package 2 narration `J3021` (`after: J3020`)
- **Ben's topic/format lock:** Unchanged (`J3011`, Ben in chat 17 Nov 2026: `"Lock it."`; planned air slot **Wed 16 Dec 2026 18:00 London**, Ben watch board deadline **Fri 11 Dec 2026 18:00 London**; zero dated films moved; format test only, pause on new single-question longs unchanged).

## Verdict: **PASS — EXACT-HASH SCRIPT LOCK GRANTED ON `v04`**

`OWB:064` script master `v04` is formally **LOCKED** by the elected acting Chief on these exact bytes (now merged to `main` via PR #1269 and PR #1274):

| Artefact | Path | Exact SHA-256 |
|---|---|---|
| Locked script master (`v04`) | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v04.md` | `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8` |
| Matching script draft (`v04`, byte-identical) | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/episode_script_draft_v04.md` | `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8` |
| Verified primary-source ledger | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/SOURCES.md` | `4a7e3fa5c74a548764886a274514d2590e5951e5e8782aa8118566d252fdc415` |
| Unedited Gemini v04 facts output | `jobs/reviews/J3544/GEMINI_RAW_v04.txt` | `feb40147c55c46be958f8ff36b1eb4d1d455272e2a13fc2e638d4da9a31f3a0d` |
| Dedicated £0 music brief & plan | `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/05_Music/MUSIC_BRIEF_v04.md` & `every_planet_score_bed_v04_plan.json` | Matched to `556f3c8d...` (`606.28 s` provisional planning estimate) |

## Independent Acting-Chief Verification Summary

1. **Full script & markers audited directly on `v04` (`35,984` bytes):** `1,296` alphanumeric tokens / `1,341` whitespace tokens / `1,374` expanded words / `8,471` spoken characters; provisional estimate `606.28 s` (including `18 s` end hold; not measured audio). Markers directly verified: `DATA: 8`, `SCALE: 8`, `WHO: 7`, `WHEN: 8`, `FACT: 4`, `NUMBER OBJECT: 8`, `[CHAPTER CARD]: 7` (+ Mercury cold open = all 8 planets), `[SUBSCRIBE BEAT]: 1` (at `35.6%`, `15` words, Line 4 verbatim), `[ORBIT ACTS]: 2` (verified shelf Omni clips).
2. **All 4 `J3520` Chief Ruling fixes (`PR #1260`) confirmed intact:**
   - Jupiter mass compares planets only (`more than twice the mass of all the other planets combined`, Sun excluded).
   - Galileo probe wording matches `J3520` (`returned data for fifty-eight minutes`; far deeper hydrogen region kept separate; no crushing event or mixed depth endpoints).
   - Earth equatorial surface speed (`1,670 km/h`) compares against Cyclone Olivia's measured `408 km/h` non-tornadic gust (`4.093×`), with `43 km` equatorial bulge.
   - Neptune winds (`>2,000 km/h`) use `"roughly five times the speed of Cyclone Olivia's record gust"` (`2,000 ÷ 408 = 4.902×`, never `>5×`), and New Horizons' July 2015 Pluto flyby is cleanly separated from Voyager 2.
3. **All 7 `J3539` FIX items + optional Gauss/ESA tightening confirmed resolved:**
   - Mercury uses `"With almost no axial tilt"` (NASA general `2°` vs NSSDCA `0.034°` conflict logged; any numeric overlay restricted to `0.034°`, never `2°`), with immediate spoken ice answer in Sentence 2 (`~11.2 s`) and Sentence 1 `<8 s` (`17` expanded words, `~7.03 s` at 145 wpm).
   - Mars magnetic history states field presence `4 billion years ago` without asserting a shutdown date or unsupported cooling causal chain; Olympus Mons `21.3 km` is explicitly labelled elevation above Mars's zero-elevation datum (MOLA `21,287.4 m`), unsourced `624 km` removed, Opportunity uses `ninety-Martian-day design life`.
   - Saturn preserves uncertainty (`possibly because of seasonal haze`), keeps `282,000 km` strictly radial, and uses 2-word verbatim `FACT: Less dense` with `"Water"` as a separate comparator.
   - Uranus separates Voyager 2 (`24 January 1986`) from the `-224.2 °C` atmospheric minimum (`colder than Neptune in some places`), `nearly sixty degrees from its rotation axis`, and `at least eighty per cent of its mass`.
   - Venus replaces `"scar of a lost ocean"` with `"evidence that Venus once held much more water"`, cites verified Donahue PMID `17783310` (superseding erroneous `17782980` preserved in historical `J3538`), and cites NASA SP-4524 p. 129 (`1 March 1982`, `127 min` vs `32 min`).
   - Gauss's `1830s` method is cleanly separated from ESA's dated `2020` report of `~9%` global-average weakening over the past two centuries.
   - Single recurring building Historical Exploration Timeline (`1610–2024`) spans Chapters 1–8; first-30-s `VISUAL MUST` is strictly line-matched with real imagery between graphics and no chapter card before `0:45`.
4. **Live primary-source spot checks + independent verification (`J3545`, PR #1274):** Directly re-verified live NSSDCA Mercury (`0.034°`), PubMed efetch XML PMID `17783310` (Donahue 1982: `hundredfold`, `0.3 percent of a terrestrial ocean`), NASA Uranus Facts (`-224.2`, `in some places`, `80%`), NASA Galileo Probe (`Dec. 7, 1995`, `58 minutes`), and NASA Saturn Facts (`282,000`, `30,000`), alongside `J3545`'s 52/52 HTTP 200 verification (including PDFKit extraction of `sp-4524.pdf` pp. 124/129 and `mola.summary.pdf` Table 8 p. 21) and `J3544`'s unedited Gemini audit.
5. **Automated gates & repo checks:** `review:script` `91.6/100 PASS` (≥90), explicit-v04 `gate:episode --require-checklist` `PASS`, `core_sync.py check` OK, `studio.py status --check` OK, `test_email_ratchet.py` (8/8 OK), `test_no_private_network.py` (5/5 OK). Historical `v01`–`v03` files and raw audits preserved byte-for-byte.
6. **Concept-sheet music conflict resolved:** `MUSIC_BRIEF_v04.md` and `every_planet_score_bed_v04_plan.json` lock a dedicated £0 film-specific score bed (with `Pace:` and `NOT:` lines, never reusing shelf music).

## PR Disposition Executed

- **Merged to `main`:**
  - PR #1269 (`macbook/J3544` — `v04` master/draft, `SOURCES.md`, `MUSIC_BRIEF_v04.md`, `v03` + `J3538`/`J3539`/`J3544` records)
  - PR #1274 (`macbook/J3545` — independent exact-hash verification `ADVISORY PASS`)
  - PR #1322 (`gemini/J3711-verify-j3020` — earlier read-only condition check `jobs/reviews/J3711/REVIEW.md`)
- **Closed as superseded (preserved in git history / merged PR #1269):**
  - PR #1015 (`macbook/J3037`, rejected v02 PASS recommendation)
  - PR #1251 (`macbook/J3520`, rejected v02 PASS recommendation)
  - PR #1262 (`macbook/J3538`, v03 — preserved verbatim in PR #1269)
  - PR #1265 (`macbook/J3539`, v03 FIX review — preserved verbatim in PR #1269)

## Downstream Handoff (`J3021` Narration & `J3022` Picture/Graphics)

1. **`J3020` completed and `J3711` closed:** `OWB:064` `script` and `sources` stages are set to `done` in `status.json` with exact lock SHA-256 `556f3c8d...`. `J3021` (Build Package 2: VO narration) now releases through its existing `after: J3020` dependency.
2. **`J3021` narration requirements:** Record **exact locked bytes** of `every_planet_explained_script_master_v04.md` (`556f3c8d...`, `~8,471` spoken chars), check live ElevenLabs balance and pending ledger before spending (zero overage/top-up), dry-run first, use `vo_take.py` (`eleven_v3`, Ben Orbit Narrator) + `scribe_v2` verification.
3. **Non-blocking downstream notes for `J3022`:**
   - Chapter 1 tilt overlay: if the shot list enforces strict verbatim VO-word match on non-chart overlays (`studio/RULES.md` §6 WORDS), use `"Almost no tilt"` alongside any numeric `0.034°` DATA call-out, and never `2°`.
   - Row 3 `SOURCES.md` table label note (`Average temperature` vs `Surface temperature` on NSSDCA Venus page): non-blocking; numeric value `737 K (464 C)` is exact and tagged `[table values]`.
   - All picture, code-graphics, thumbnail, packaging-panel, music (`music_gate.py`), SFX (`sfx_kit.py level`), and polish/QA gates remain fully enforced in `J3022`–`J3023`.

## Scope & Safety

- No audio was rendered or heard; no moving video was reviewed; no media generation, ElevenLabs spend, NAS write, upload, scheduling, or YouTube privacy/metadata change occurred in this ruling (`£0`, `0` credits).
