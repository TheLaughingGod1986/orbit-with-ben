# J2875 — Chief Review & Handoff Resolution: OWB 064 Topic (`orphan-review`)

- **Job**: `J2875` — `Chief: resolve 064 topic orphan-review`
- **Handoff Signature**: `{"film": "064", "stage": "topic", "kind": "orphan-review", "signature": "88d9ced37bb93c2d3fd0"}`
- **Reviewer**: `gemini` (Elected Acting Chief under `claude -> chief (grok) -> codex -> gemini`, verified via `python3 scripts/chief_relay.py status`)
- **Date**: `2026-11-15`
- **Film**: `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/` (*Every Planet Explained in 10 Minutes (Mercury to Neptune)*)
- **Originating Jobs**: `J2863` (*064 Every Planet Explained in 10 Minutes — format-test Go/No-Go & per-planet shelf audit*, `macbook-2`, `2e3463ca43`), `J2864` (*Board & Plan: add 064 Every Planet Explained in 10 Minutes format-test candidate for Ben*, `macbook-1`, `3bc72f46a5`), `J2866` (*Chief: merge 2 review worker branches*, `gemini`, `13e51e61f6`)
- **Ruling**: **PASS / GO (`25/25`, `100%`)** — Topic & Format-Test Go/No-Go package passes Rule E (`STUDIO_PLAYBOOK.md` §1) and `LEARNINGS.md` Rules 1 & 26. `stages.topic` in `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json` is resolved to `{"state": "done", "ref": "jobs/reviews/J2875/REVIEW.md", "ruling": "PASS"}`.
- **Gate Preserved (`£0` spend)**: Per `J2863`, `J2864`, and `studio/plan.json` (`"when": ""`, `"needsBen": "Lock or decline this film on its card"`), **zero** Script, VO, or Picture build jobs are queued before Ben locks the format-test card on the board (`#plan`), and **zero** dated schedule slots (`051`–`063`) are moved.

---

## 1. Root Cause of the `orphan-review` Handoff (`88d9ced37bb93c2d3fd0`)

1. In `J2863` (`2e3463ca43`), `macbook-2` created `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/` and its format-test Go/No-Go documentation (`05_Analytics/owb/EVERY_PLANET_EXPLAINED_GO_NO_GO.md`, `TOPIC.md`, `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `TOPIC_OPPORTUNITY_SCORE.md`), setting `stages.topic` in `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json` to `{"state": "review", "ref": "J2863"}`.
2. Once `J2863` was merged to `main` in `J2866` (`13e51e61f6`) and closed (`b978ed77f5`), `064` had `stages.topic.state == "review"` with no active (`open`/`claimed`/`blocked`) `topic` job and no `WIP.json` `"next"` entry.
3. `scripts/workflow_handoffs.py` (`detect_findings`) flags any stage in `state == "review"` with no live job and no `WIP.json` `"next"` entry as `orphan-review`, generating `J2875` (`handoff: {"film": "064", "stage": "topic", "kind": "orphan-review", "signature": "88d9ced37bb93c2d3fd0"}`).
4. Meanwhile, `scripts/plan_board.py` (`_film_stand`) drives the `#plan` card state (`"stand": "Waiting for your lock"`) strictly from `studio/plan.json` (`"needsBen": "Lock or decline this film on its card"`, `"when": ""`), independent of `status.json` `stages.topic.state`. And because `064` is an unslotted format-test candidate (not in `jobs/queue.json` `"focus"`), setting `stages.topic` to `done` with `ruling: "PASS"` does not trigger `missing-next-step` in `workflow_handoffs.py`.

---

## 2. Live Mac Mini Evidence & Rule-E Verification (`2026-11-15`)

In `J2863`, `macbook-2` operated from an offline worktree without live YouTube API access and left three single-planet (`006` Saturn) neighbour rows in `TOPIC_GO_NO_GO_SHEET.md`. On `2026-11-15`, before granting a Chief `PASS`, `gemini` ran live YouTube GB verification on the Mac mini and upgraded all five `064` topic files:

### A. Signed-Out YouTube GB Autocomplete (`LEARNINGS.md` Rule 26)
- **Endpoint**: `https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&gl=gb&hl=en-GB`
- **Live results (`2026-11-15`)**:
  - `q=every+planet+explained` -> **`#1: "every planet explained"`**, **`#2: "every planet explained in 12 minutes"`**, `#3: "every dwarf planet explained"`, `#4: "every planet in the solar system explained"`, `#7: "all planets explained in 10 minutes"`
  - `q=every+planet+in+the+solar+system` -> `#1: "every planet in the solar system"`, **`#2: "every planet in the solar system explained"`**
  - `q=planets+explained+in+10+minutes` -> **`#1: "all planets explained in 10 minutes"`**

### B. Live YouTube GB Search Ranking Videos (`q="every planet explained"`, `2026-11-15`)
| Rank | Video ID | Channel | Title | Views (15 Nov 2026) | Length | Notes |
| --- | --- | --- | --- | ---: | --- | --- |
| `#1` | `lVdYYpoozZU` | Jaydone History | *Every Planet From Our Solar System Explained in 20 Minutes* | **888,006** | `20:29` | Confirms high organic search demand for the exact `"Every Planet ... Explained in N Minutes"` format; leaves the tighter 10-minute slot open |
| `#2` | `oytUCOzAYpo` | Mr. Ask | *Every Planet in the Solar System Explained in 6 Minutes* | **99,049** | `5:49` | Short overview; lacks spacecraft-instrument breakdown |
| `#3` | `iqJjTeYv5-M` | Science Channel | *Everything You Want to Know About Planets \| How the Universe Works \| Science Channel* | **3,676,506** | `58:29` | 58-minute TV compilation (`3.68M` views) |
| `#6` | `9zaruOUM_0o` | Bluntly Explained | *Every Type Of Planet Explained in 12 Minutes* | **181,027** | `12:14` | Taxonomy explainer rather than Mercury-to-Neptune tour |

### C. Five Verified `>= 1M`-View Multi-Planet Solar System Neighbours (`LEARNINGS.md` Rule 1)
Replaced the three single-planet (`006` Saturn) rows in `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` and `PRE_BUILD_VIDIQ_AUDIT.md` with five directly on-subject eight-planet / Solar System education/space neighbours verified live on `2026-11-15`:

| # | Channel | Video Title | Video ID | Views (15 Nov 2026) | Published | Core Angle |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | National Geographic | *Solar System 101 \| National Geographic* | `libKVRa01L8` | **39,831,294** | 2017-08-30 | Evergreen 8-planet order-from-the-Sun tour (`4:11`) — proves massive search & browse appetite (`39.8M` views) for a concise Mercury-to-Neptune planetary tour |
| 2 | BBC Earth Science | *Eight Wonders Of Our Solar System \| The Planets \| BBC Earth Science* | `wkQuOrsgVGY` | **10,558,560** | 2023-01-08 | All 8 planets compared end-to-end (`10.56M` views) with spacecraft imagery |
| 3 | Beyond Nature | *The Planets In Our Solar System* | `lcZTcfdZ3Ow` | **5,006,819** | 2023-07-09 | Full 8-planet documentary tour from Mercury to Neptune (`5.01M` views) |
| 4 | Science Channel | *Everything You Want to Know About Planets \| How the Universe Works \| Science Channel* | `iqJjTeYv5-M` | **3,676,506** | 2023-06-15 | Ranks `#3` on YouTube GB for `"every planet explained"` (`3.68M` views) |
| 5 | What If | *What If You Spent a Day on Every Planet, from 800 °F Mercury to Neptune?* | `WOgatB4daq8` | **2,231,803** | 2020-08-01 | Explicit Mercury-to-Neptune 8-planet structure (`2.23M` views) |

### D. Title Uniqueness & Per-Planet Shelf Audit
- **Title Uniqueness (`VIDEO_BACKLOG.json` + `studio/plan.json`, `001`–`063`)**: `0` overlaps for `"Every Planet Explained in 10 Minutes (Mercury to Neptune)"` or the two companion Shorts (`"Which Planet in Our Solar System Is the Hottest?"`, `"What Is the Coldest Planet in Our Solar System?"`).
- **Per-Planet Shelf Audit (All 8 Planets)**:
  - Single-planet deep dives on the shelf stay mechanism-specific (`012` Mercury shrinking, `021` Venus day vs year, `032` Earth rotation stop, `005` Mars ocean loss, `003` Jupiter Great Red Spot, `006` Saturn rings disappearing, `008` Uranus sideways tilt, `009` Neptune supersonic winds).
  - `064` allocates ~68 seconds (`~145–150` words) per planet and answers the comparative 8-planet architecture question (*where the rock-to-gas and gas-to-ice boundaries sit from `0.39 AU` to `30.07 AU`*), serving as an evergreen hub with an 8-planet chapter bar and end-screen handoff into the single-planet shelf.
- **Template Completeness**: Copied the 10 missing template files from `02_Video-Projects/_template_NNN_Episode-Slug/` into `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/` so `gate:episode` structure checks are satisfied.

---

## 3. Rule-E Opportunity Score Summary (`25/25`, `100%`)

| Criterion | Score | Basis |
| --- | ---: | --- |
| 1. Search Demand & Evergreen Intent | `5/5` | `#1` YouTube GB autocomplete `"every planet explained"`, `#2` `"every planet explained in 12 minutes"`; `#1` ranking video `lVdYYpoozZU` has `888,006` views |
| 2. Neighbour Ceiling (`>= 1M` views) | `5/5` | 5 verified multi-planet neighbours from `2.23M` to `39.83M` views (`libKVRa01L8`, `wkQuOrsgVGY`, `lcZTcfdZ3Ow`, `iqJjTeYv5-M`, `WOgatB4daq8`) |
| 3. Competitor Gap / 10-Minute Slot | `5/5` | No existing 10-minute NASA/ESA spacecraft-data chaptered tour between `5:49` (`oytUCOzAYpo`) and `20:29` (`lVdYYpoozZU`) |
| 4. Visual & NASA/ESA Plate Availability | `5/5` | All 8 planets have verified public-domain NASA/ESA/JPL/JHUAPL mission archives (`MESSENGER`, `Magellan`, `DSCOVR/EPIC`, `Viking/Curiosity`, `Juno/Cassini`, `Cassini`, `Voyager 2`, `Voyager 2/JWST`) |
| 5. Channel Fit & Hub-and-Spoke Value | `5/5` | Zero cannibalisation of single-planet deep dives; acts as a hub funneling viewers into `012`, `021`, `032`, `005`, `003`, `006`, `008`, `009` |
| **Total** | **`25/25` (`100%`)** | **PASS / GO (`>= 20/25` threshold)** |

---

## 4. State Transition & Next Steps

- `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json`: `stages.topic` updated from `{"state": "review", "ref": "J2863"}` to `{"state": "done", "ref": "jobs/reviews/J2875/REVIEW.md", "ruling": "PASS"}`.
- `STATUS.md`: regenerated via `python3 scripts/studio.py status` (`064` Topic shows `done`).
- `scripts/workflow_handoffs.py`: verified `count: 0`, `findings: []`.
- **Next step**: `OWB:064` remains on `#plan` (`studio/plan.json`) as an unslotted format-test candidate (`"when": ""`, `"needsBen": "Lock or decline this film on its card"`). No Script, VO, or Picture jobs will be queued until Ben locks the card on the board.
