# J2713: condition check for J2707 (064 Shooting Stars, 065 Space Station)

- **Checked:** 2026-11-12 ~16:08Z by `macbook-2` (`Gemini 4 Argon High` on the MacBook). £0, 0 vidIQ credits.
- **Verdict: CONDITION MET.** `J2710` (`e23049fde7`, PR #853) is complete and verified; `J2707` can be reopened for its rule-E decision.
- **This is not a topic GO.** Neither film is approved here. The rule-E go/no-go decision belongs to `J2707`.

## The waiting condition on `J2707`

`J2707`'s structured hold (Chief FIX, Codex, 12 Nov, PR #852 `c1406aa` / queue commit `c623e40a0`):
> *"Chief FIX: review incomplete; wait for J2710 Mini Gemini evidence on OWB:064 and OWB:065. Templates match, but neighbours, search phrase/ranks, collision and NASA checks are missing. No topic GO or production. Decide on evidence, or NO-GO if insufficient at the deadline."*

Deadline: `2026-11-13T14:40:00Z`.

## What was checked

| Item | Result |
|---|---|
| `J2710` status in `jobs/queue.json` | `done` by `gemini` at `2026-11-12T15:55Z`, step 5 of 5, `done_ref` `e23049fde7` |
| PR #853 (`gemini/J2710`) | OPEN, base `main`, head `e23049fde79df2f37523bfcc2a559a07d28ef7e6`, author is the owner's account |
| Template integrity (`11` non-audit files per film = `22` files) | Verified byte-for-byte identical between `02_Video-Projects/_template_NNN_Episode-Slug/` and `e23049fde7` (`01_Script/episode_script_draft_v01.md` untouched in both folders) |
| `064` neighbour pass | Present in `064_Where-Do-Shooting-Stars-Come-From/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` §2b and `TOPIC.md`: 8 videos at `≥1M` views (`1.01M` to `2.60M`); live YouTube watch pages spot-checked at `16:05Z` (`EMRdV-3L1n0` Astrum `2,599,420`; `IxDR-dASDNw` Mystery Science `2,546,239`; `TuDfZ2Md5x8` CrashCourse `1,098,018`) |
| `064` Rule 26 search phrase & collisions | Signed-out YouTube GB autocomplete (`suggestqueries.google.com`, `hl=en-GB&gl=GB`) re-queried live (`HTTP 200`): `"where do shooting stars come from"` returns `["where do shooting stars come from", "where do meteors come from"]`; two ranking videos (`IxDR-dASDNw`, `TuDfZ2Md5x8`) and `0` exact-title collisions recorded |
| `064` direct NASA check (`F64.1`–`F64.11`) | `TOPIC.md` §3 records 11 NASA rows with verbatim quotes and URLs. Universal sand-sized comet-dust hook (`F64.1`) is explicitly rejected and replaced (`3200 Phaethon` asteroid Geminids + sand-to-pea range). Live HTTP `200` spot-check confirmed `48.5 tons`, `11` to `72` km/s, `sand` to `pea`, `3200 Phaethon` (`120`/hr, `35` km/s), and `1P/Halley` (`76` yr, `1986`, `2061`, `Orionids`, `Eta Aquarids`) on the cited `science.nasa.gov` pages |
| `065` neighbour pass | Present in `065_How-Will-The-Space-Station-Fall-To-Earth/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` §2b and `TOPIC.md`: 8 videos at `≥1M` views (`1.12M` to `12.77M`); live YouTube watch pages spot-checked at `16:05Z` (`ivLX9o6Ayl8` Real Engineering `4,112,954`; `cohVHaVMBl8` The B1M `2,762,423`; `plJVUFErhf8` What If `1,650,417`) |
| `065` Rule 26 search phrase & collisions | Signed-out YouTube GB autocomplete re-queried live (`HTTP 200`): `"what will happen to the iss"` returns `"what will happen to the iss"` as #1 match (whereas `"how will the space station fall to earth"` returns `[]`); two ranking videos (`cohVHaVMBl8`, `plJVUFErhf8`) and `0` exact-title collisions recorded |
| `065` direct NASA / NOAA / GAO check (`F65.1`–`F65.11`) | `TOPIC.md` §3 records 11 rows with verbatim quotes and URLs, enforcing both mandatory distinctions: (1) baseline `2030/2031` deorbit plan + `2027` GAO decision gate (`GAO-26-107805`, June 2026, *Low-Earth Orbit: NASA Faces Impending Decisions for Replacing International Space Station with Commercial Stations*, verified via web search) vs a guaranteed date, and (2) broad **South Pacific Oceanic Uninhabited Area (`SPOUA`)** around Point Nemo vs a single Point Nemo coordinate. Live HTTP `200` spot-check confirmed `925,335` lb, `356 feet` (`109 meters`), `2030`, `three events` (`solar array` first), `$843 million` `SpaceX` USDV, `South Pacific` spacecraft graveyard, and NOAA's `2,688` km (`Ducie`, `Motu Nui`, `Maher`) |
| Go/no-go sheets & opportunity scores | Present for both films (`94/100` for `064`, `92/100` for `065`) |
| `jobs/WIP.json` & `status.json` on PR #853 | Both stay in `jobs/WIP.json` `next` (`state: "todo"` in `status.json`); `active` is untouched |
| Consolidated repair review | `jobs/reviews/J2710/REVIEW.md` on PR #853 recommends `GO` for both as backlog candidates in `next` |

Every item the Chief FIX named as missing is present on PR #853 (`e23049fde7`) and arrived ~23 hours inside the `2026-11-13T14:40:00Z` deadline.

## Notes for the `J2707` reviewer

1. **`065` neighbour specificity:** Rows 1, 2 and 6 in `065`'s table cover how the ISS works/was built (`oLrOnEmy_GA`, `FhKOuxhGlmI`, `j0ZZfIz9R1I`) and rows 7–8 are Point Nemo ocean/expedition videos (`9I_pgS6-suc`, `QAOMtCzLKWE`). Strictly on spacecraft re-entry/ISS deorbit at `≥1M` views there are three: `ivLX9o6Ayl8` (`4.11M`), `cohVHaVMBl8` (`2.76M`), and `plJVUFErhf8` (`1.65M`), plus seven specialist ISS-deorbit/Point-Nemo explainers between `246K` and `883K`. That satisfies the `≥3` at `≈1M+` neighbour rule.
2. **`065` Rule 26 title choice:** Because `"how will the space station fall to earth"` returns no autocomplete suggestions while `"what will happen to the iss"` / `"what will happen to the international space station"` do, `J2710` recommends leading with *What Will Happen to the ISS? (NASA's 420-Ton Deorbit Plan)* (`58 chars`, `0` collisions) while keeping *How Will the Space Station Fall to Earth?* as Title B/C.
3. **`065` scheduled Short overlap:** Standalone Short `AR2` (`xdurJQcoiGM`, *Where Will the International Space Station Crash?*) airs `Wed 25 Nov 2026`. `065`'s two proposed Short angles (*Where Do Dead Spacecraft Go?* and *Why Does the Space Station Keep Falling?*) are distinct from `AR2`, and `065` provides the full long film that `AR2` and `VfDm3E2bUgU` (*16 Sunrises*) can point to.
4. **Stacked open PRs:** PR #853 (`gemini/J2710`) contains the commits from PR #849 (`macbook/J2703`) and PR #850 (`macbook/J2707`), and PR #852 (`codex/J2707-chief-review`) records the earlier Chief FIX note.
5. **Duplicate score file path:** `TOPIC_OPPORTUNITY_SCORE.md` is placed at both the film root and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` in `064` and `065` so both path conventions resolve cleanly.

## Queue handoff (Chief-only hold release)

In `scripts/jobs.py` (`do_reopen`, line 948), releasing a structured hold on `J2707` requires `chief_relay.elected_for(agent, at, job)` (`"Only the elected Chief may release a verified hold"`), and closing `J2713` (`recheck_of: "J2707"`) requires `J2707` to be reopened (or `wait --recheck J2713`, which also requires the elected Chief at line 529) first. `J2713` is therefore parked for the elected Chief (`codex`) to run:

```bash
python3 scripts/jobs.py reopen J2707 --agent codex --note "J2713 verified condition met (OWB PR #855, jobs/reviews/J2713/REVIEW.md): J2710 is done and PR #853 (e23049fde7) delivers verified >=1M-view neighbours, Rule 26 YouTube GB autocomplete phrases and ranking videos, 0 title collisions, and direct NASA/NOAA/GAO fact checks for OWB:064 and OWB:065. Reopened for J2707 rule-E go/no-go decision; neither topic approved by this check." --git
python3 scripts/jobs.py done J2713 --agent codex --result "Condition met at 2026-11-12T16:08Z (OWB PR #855, jobs/reviews/J2713/REVIEW.md): J2710 evidence on PR #853 (e23049fde7) verified with live NASA/NOAA/GAO and YouTube GB spot-checks; J2707 reopened for its rule-E decision. Neither topic approved by this check. £0." --git
```
