# Orbit with Ben — full technical channel audit (10 Sep 2026)

Source: live YouTube Studio (Orbit brand channel `UC_esArsDKd3GJvOkeO0DUog`) via Chrome CDP, anonymous public watch pages, and first-3s downloads of the live Shorts. Captured Thu 10 Sep 2026 19:10–19:40 BST (Neutron long had premiered at 18:00, ~75 min earlier). Raw numbers: `data/`.

## Verdict in one paragraph

**The channel is not broken.** No strikes (all three feature tiers Enabled), no copyright claims, no privacy/playability faults, Related pills and description links all point at the right Thursday long, every scheduled Short is intact through 18 Sep, and Shorts are being served from the Shorts feed (78% of Shorts views). Views are not down month-on-month either — **4,515 views in the last 28 days is +849 %**. What Ben is seeing is the shape of the curve: views arrive as one-day spikes on publish days (891 on 1 Sep, 548 on 5 Sep) and fall to ~100 → 9 within days, because YouTube stops the feed test as soon as it measures retention. The channel-wide Shorts retention is **31.7 % “stayed to watch” / 68.3 % swiped away**, and no single Short is above 46 %. Two production faults made the Europa week worse: six of the eight Europa Shorts open on the **identical Europa globe plate** (perceptual hash 0–3 bits apart — the feed saw the same video six days running), and the 9 Sep Short (`TE_HDKAnqms`) **opens on Orbit**, breaking the picture-first lock; it received **0 % Shorts-feed traffic** and 2 views. Long films are a separate problem: seven longs have **13–170 lifetime impressions each** and 0–41 views; the Shorts→long funnel delivered 2 views to the Europa film. Fix plan is at the end.

## 1. Channel health checks (all PASS)

| Check | Result | Evidence |
|---|---|---|
| Community Guidelines strikes | none | Settings → Feature eligibility: Standard / Intermediate / Advanced all **Enabled** (a strike disables tiers) |
| Copyright | none | Content detection → Copyright: “Nothing to see yet” |
| Playability of live longs | OK | anon `playabilityStatus=OK`, not private/unlisted: `Yk1tLh23rko`, `NbW5G1BpPY0`, `REXYxuLOBoI`, `TE_HDKAnqms` |
| Shorts classified as Shorts | yes | all 22–31 s uploads sit under Studio **Shorts** tab; Shorts feed = 78.4 % of Shorts views (28 d) |
| Related video (Short → that week’s long) | PASS ×10 | `fhJP6eMoU0Q` + 7 scheduled Neutron Shorts → *What Happens If You Get Near a Neutron Star*; `0j_pgYbCe5E` → Last Star; `TE_HDKAnqms` → Europa (`data/related_check.json`) |
| Description parent links | PASS ×10 | each description carries exactly the matching long id |
| Scheduled queue | intact | 11–17 Sep 11:30 UK one Neutron Short/day, 18 Sep leftover; no collisions |
| Duplicate/private hygiene | mostly OK | see §4 — three **public** copies of the same “Sky” Short |
| Made for kids / restrictions | none flagged | Studio Notices column empty on every row |
| Shorts open technically | OK | VO onset ≤0.37 s, no black frames, no fade-in on any local export (`data/shorts_open_probe.json`) |

Conclusion: nothing on the platform side is suppressing the channel. Every drop below is explained by the metrics YouTube is measuring.

## 2. What the numbers actually say (last 28 days, 13 Aug – 9 Sep)

- Views **4,515** (+849 % vs prior 28 d) · watch time **12.6 h** (+648 %) · subs **+5** (total 7) · 7,515 thumbnail impressions · 1.9 % CTR · Shorts engaged views 1.5k of 4.4k.
- Traffic (Shorts): Shorts feed 78.4 % · YouTube search 17.0 % · everything else <2 % each. External 0.8 % — Meta/Threads mirrors are not sending traffic.
- **Stayed to watch 31.7 % · swiped away 68.3 %.** This is the number that decides Shorts distribution.
- Audience: 84 % male; 42 % aged 35–44; 15.6 % 65+. Monthly audience card: “not enough viewer data”. Watch time from subscribers: nothing.
- Realtime last 48 h: **51 views** (33 of them the new Neutron Short).

Daily views (Studio series, `data/daily_views_28d.json`):

| Day | Views | What published |
|---|---|---|
| Sat 29 Aug | 421 | Remains v1 |
| Tue **1 Sep** | **891** | 3 Shorts same day (Remains 622, Sky 292, Furnace 74) |
| Wed 2 Sep | 263 | Recycling |
| Thu 3 Sep | 195 | Europa long Premiere + Ice Scars + Ocean Under Ice |
| Fri 4 Sep | 215 | Shouldn’t Exist |
| Sat **5 Sep** | **548** | 3 Shorts same day (Hiding 291, Eat 127, Sky remint 85) |
| Sun 6 Sep | 145 | Feed With No Sun (95) |
| Mon 7 Sep | 111 | Sprays (89) |
| Tue 8 Sep | 99 | Kill (92) |
| Wed 9 Sep | **9** | Under Ice (2) — first Short with **0 % Shorts-feed traffic** |

Pattern: each Short gets a feed test of roughly 80–600 impressions on day one, retention is measured, and the test is not extended. Days with three uploads look like “good days”; they are three tests stacked, not growth.

## 3. Shorts retention per video (lifetime, Studio “Stayed to watch”)

| Short | Views | Stayed | AVD | Open |
|---|---|---|---|---|
| `VE0f186WQZo` Europa Sprays Its Ocean Into Space | 89 | **46.2 %** | 0:09 | Europa globe plate |
| `wIh3armF7_k` The Last Star Will Be a Red Dwarf | 55 | 42.0 % | 0:16 | |
| `CkSECfUfH2Y` The Sky Is Already Running Out of Light | 292 | 41.2 % | 0:16 | |
| `9lLZMy8rBJo` What Remains After the Last Star Dies? | 624 | 38.8 % | 0:15 | dark moon plate |
| `jB8OAZKXdEw` Sky (3rd public copy) | 86 | 37.9 % | 0:23 | |
| `SdNXS1PD_Yk` Why the Night Sky Is Getting Darker (Sky copy) | 253 | 37.6 % | 0:17 | |
| `eVp9a7f4rWg` We Could Kill the Life We’re Looking For | 93 | 35.1 % | 0:13 | Europa globe plate |
| `IVbO9XkkDps` The Day the Last Star Goes Out | 93 | 33.3 % | 0:11 | |
| `Xza_jSHD4qw` How Life Could Feed Under Europa With No Sun | 95 | 31.8 % | 0:11 | Europa globe plate |
| `DN4L1DkerMM` The Universe Is Running Out of New Stars | 229 | 28.6 % | 0:22 | |
| `PV50PX-bE4g` Most of the Universe Gives Off No Light | 127 | 26.9 % | 0:15 | |
| `1glQuYFSaYQ` What Would Life Eat Under Europa? | 129 | 20.8 % | 0:12 | Europa globe plate |
| `KX-XU_AODoI` Last Star Furnace Goes Cold | 75 | 20.6 % | 0:25 | |
| `QNTeou-w-gY` There’s an Ocean Under That Ice | 68 | 18.6 % | 0:16 | |
| `pII09FbRYGc` Why Europa Is Hiding a Massive Ocean | 293 | **16.6 %** | 0:12 | ice-surface plate |
| `keXe1GNxWSU` Those Ice Scars Are How You Find It | 219 | 15.7 % | 0:09 | |
| `n2WbOfJhOwc` Star Recycling Isn’t Perfect | 227 | **15.3 %** | 0:10 | |
| `TE_HDKAnqms` If Life Starts Under Ice, It’s Everywhere | 2 | n/a | n/a | **Orbit in frame at 0 s** |

Reading: views do **not** track retention (Hiding had 293 views at 16.6 %; Sprays 89 at 46.2 %) — views track the size of the day-one feed test. Retention is what stops the test. Healthy Shorts on small channels sit at 65–80 % stayed; nothing here is above 46 %. The Diamond bar reference (`M-VN84HCNls`, 223 % viewed) is the only Orbit Short that ever cleared this bar and it is not in this window.

## 4. Production faults found

### 4a. Six Europa Shorts open on the same frame

First-frame perceptual hash (dHash, 64-bit) of the **live** uploads: `8Bym-yrYhGc` ↔ `VE0f186WQZo` **0 bits** apart; `8Bym` ↔ `Xza_jSHD4qw` 1; `8Bym` ↔ `eVp9a7f4rWg` 1; `1glQuYFSaYQ` within 2–3 of all of them. The only thing that changes at 0 s is the caption word. A viewer scrolling the feed on 4, 5, 6, 7, 8 Sep saw what looks like the same Short five days running, and YouTube’s repetitive-content signal sees the same thing. The house rule “first-and-last-frame off the week’s open world still” was applied as “every Short opens on the same still”, which is not what it means — the loop is per Short, the *plate* must differ.

### 4b. `TE_HDKAnqms` opens on Orbit — picture-first lock broken

Frame at 0.3 s is Orbit, full-frame, over the ice. This violates `orbit-shorts-punch-first` rule 1 (“strange picture in 1 s — not Orbit”) and the auditor gate. Result: traffic sources = 50 % search / 50 % other / **0 % Shorts feed**; 2 views in 32 h. It is the only Orbit Short ever to get zero feed seeding. The description typo was never the cause (and is already gone live). Do not remint the same cut; if the beat is wanted, it is a new Short with a world-plate open.

### 4c. Three public copies of the same Short

`CkSECfUfH2Y` (292), `SdNXS1PD_Yk` (253, retitled *Why the Night Sky Is Getting Darker*), `jB8OAZKXdEw` (86, 5 Sep) are the same Sky cut, all Public. Same-channel duplicate uploads split whatever feed budget the idea has and are a textbook “reused content” flag. Lower-view copies of *Remains*, *Hiding*, *Kill* are already Private (correct).

### 4d. Cluster dumping

1 Sep and 5 Sep each carried **three** public Shorts, then 4–9 Sep carried **eight Europa Shorts in seven days** (plus the long). The Neutron week is queued at one per day 11–17 Sep (acceptable cadence), but all seven titles contain “Neutron Star”, so the feed will again see a run of near-identical items. Three scheduled Neutron Shorts are over the 27 s cap: `92vmMxSNmlk` 0:31, `o7ykyTDZKiE` 0:29, `va5ATScn3rs` 0:29 (under 40 s, so not blocking).

### 4e. Neutron week opens — checked in Studio before they air

First frame (0.4 s) of each scheduled Short, captured from the Studio player:

| Airs | Short | 0.4 s frame | Verdict |
|---|---|---|---|
| Thu 11 Sep | `vCxXTYXSSqY` How Heavy Is a Teaspoon of Neutron Star? | concentric rings / spoon glow | unique — OK |
| Fri 12 Sep | `va5ATScn3rs` The Sky Would Lean | bent star trail over dark disc | unique — OK |
| Sat 13 Sep | `o7ykyTDZKiE` Your Last Clear Image | white light-line tangle | unique — OK |
| Sun 14 Sep | `Rp_8J6_6IIk` What Happens If You Touch | white lattice | unique — OK |
| Mon 15 Sep | `92vmMxSNmlk` Why You Can’t Stand on a Neutron Star | glowing cracked crust | plate A |
| **Tue 16 Sep** | `mAAMsbhm88w` Could a Probe Get Closer | **Orbit full-frame, face to camera** | **FAIL — Orbit-first, same fault as `TE_HDKAnqms`** |
| Wed 17 Sep | `BX-z1EkgANg` One Second Near a Neutron Star Is Enough | glowing cracked crust | plate A again (two days apart) |

Four of seven are distinct and world-first — better than Europa week. `mAAMsbhm88w` must not air as-is: on current evidence it will get zero feed seeding. `BX-z1EkgANg` re-uses the 15 Sep crust plate; acceptable if nothing else changes, better if its open is swapped.

### 4f. Longs get no distribution at all

| Long | Length | Lifetime impressions | CTR | Views | AVD |
|---|---|---|---|---|---|
| Neutron Star `Yk1tLh23rko` (premiered today 18:00) | 9:43 | 13 (pre-premiere) | 0 % | 0 | — |
| Europa `NbW5G1BpPY0` | 9:19 | 59 | 1.7 % | 14 | 2:08 (23 %) |
| Last Star `REXYxuLOBoI` | 8:38 | 170 | 2.4 % | 41 | 2:20 (27 %) |
| JWST `ziKBPJ6FY0U` | 16:33 | 133 | 1.5 % | 22 | 3:24 |
| Alien Worlds | 21:29 | 108 | 2.8 % | 12 | 0:54 |
| Fermi | 18:32 | 56 | 0 % | 6 | 5:10 |

Europa’s 14 views came 43 % direct, 29 % search, 14 % Browse, **14 % Related Shorts (= 2 views)** despite eight Shorts with correct Related pills pointing at it. The funnel is wired correctly and converts ~0.1 % of Shorts views. With 7 subscribers there is no Browse seed; the Premiere ran to zero attendees. Longs are living entirely on search for their title.

## 5. What is *not* the problem

- Not a strike, shadow-limit, or copyright hold (verified above).
- Not the description typo on `TE_HDKAnqms` — fixed live, irrelevant to distribution.
- Not Related/pins/links — all pass.
- Not black frames, silent opens, or wrong aspect — every export starts at 0 s with picture and VO.
- Not thumbnails on Shorts (feed ignores them); long thumbs have 1.5–2.8 % CTR on <200 impressions — too few impressions to judge.
- Not month-on-month decline — the channel is up 8×; the drop is spike decay after each feed test.

## 6. Fix plan

### P0 — this week, no generation credits

1. **Stop the duplicate-plate run.** Before any further Short ships, the auditor must reject a new Short whose 0.3 s frame is within 10 dHash bits of any Short published in the previous 14 days. Add this to the ship gate (`orbit-auditor-ship-gate`) as a hard FAIL alongside the ≥40 s probe. Reference script: `data/shorts_open_probe.json` shows the check is a one-line ffmpeg + hash.
2. **Fix `mAAMsbhm88w` before Tue 16 Sep 11:30.** It opens on Orbit (§4e). Re-export with a world-plate open (the crust or the probe itself at 0 s, Orbit later if at all), upload the new file private, copy title/description/thumb, set Related → `Yk1tLh23rko`, schedule it for 16 Sep 11:30, then unschedule the old id (Private, no publishAt — do not delete), per the replace rule. If a re-export cannot be done in time, pull it (Private) rather than let an Orbit-first Short air. Optional: swap the open on `BX-z1EkgANg` so 15 and 17 Sep do not share plate A.
3. **Dedupe Sky.** Keep the highest-view public copy (`CkSECfUfH2Y`, 292) public; set `jB8OAZKXdEw` (86) Private. `SdNXS1PD_Yk` (253, retitled) is Ben’s call — it is the same cut under a different title; house rule says one public per cut. Do not delete anything.
4. **`TE_HDKAnqms`:** leave it public, do nothing else. Log it in the auditor as the Orbit-first FAIL example (the first Orbit Short with 0 % feed traffic) next to `FbRFvSApfOQ`.
5. **One Short per day, maximum.** Never three in one day again; the “big” 1 Sep / 5 Sep totals were three separate tests, not one good Short.
6. **Stop Premieres for longs** until subscribers are in the hundreds. 13 impressions and zero attendees is a wasted first hour; schedule as a normal publish at 18:00 Thursday with Studio end screens.

### P1 — next production week (the lever that moves views)

7. **Target ≥60 % stayed-to-watch, measured per Short after 48 h.** This becomes the single Shorts KPI in the UAT bible; views are an output. Any Short under 35 % at 48 h is a study case (write down what the 0–1 s frame was), not a remint.
8. **Open on the object the line names, at 0 s, moving.** The 46 % top scorer (*Sprays*) opens on a plume verb; the 15–17 % floor (*Recycling*, *Ice Scars*, *Hiding*) open on a static globe with a caption. First frame must already be in motion (Veo Fast plate, not a still with Ken Burns), never a static globe with text, never Orbit.
9. **Distinct plate per Short, distinct subject per Short.** Each of the 4–8 cluster Shorts gets its own Veo Fast world money shot as its open/loop. Cost: one extra Veo Fast (~8 s) per Short, no Omni. If budget allows only three unique plates, ship three Shorts, not eight.
10. **Vary the title stem.** Seven consecutive “…Near a Neutron Star” titles read as one video in the feed and in search. Keep the concrete question form but rotate the noun: “a teaspoon of this star”, “this crust”, “the last thing your eyes see”.
11. **Trim the three 28–31 s Neutron Shorts to ≤27 s** when re-exporting under item 2; otherwise leave (they are under 40 s).

### P2 — long-form distribution (structural)

12. **Accept that longs are search-only for now** and package them for search: primary keyword in the first 100 characters (Neutron and Europa already do this), full chapter list, and a pinned comment that asks one question (the house already allows long pins). Do not spend Veo/Omni credits on long-form thumbnails A/B beyond the three-variant test — with <200 impressions the test cannot resolve.
13. **Shorts→long funnel is 0.1 %.** The Related pill is correct and stays, but the only funnel that will move longs at 7 subscribers is the Short itself finishing on the *exact* unanswered question the long answers (curiosity gap), not “watch the full film”. Re-check the last 4 s copy on the Neutron Shorts against this before 11 Sep.
14. **Subscribers are the long-form gate.** 7 subs → Browse gives nothing. Every Short’s last 4 s and every long’s end screen is a next-film hook, not a subscribe ask (house rule), so subs will come from stayed-to-watch, which loops back to item 7.

### Measurement

- Re-run this audit on Thu 17 Sep 19:00 after the Neutron cluster has aired: channel stayed-to-watch (target >45 % as a first step, 60 % by October), views on days 2–4 after each Short (target: >30 % of day-1 views instead of the current ~10 %), and Europa/Neutron long impressions (target: >300 lifetime by 24 Sep).
- Do not read a 500-view day as growth unless the following two days hold above 150.

## Files

- `data/daily_views_28d.json` — Studio daily views / watch minutes / net subs, 13 Aug–9 Sep
- `data/per_video_28d.json` — Studio Advanced mode: views, watch hours, AVD, impressions, CTR, subs per video (48 rows)
- `data/stayed.json`, `data/vid_analytics.json` — per-video stayed-to-watch, AVD, traffic sources
- `data/related_check.json` — Related pill + description link per Neutron-week Short
- `data/shorts_rows.json` — Studio Shorts list (id, title, visibility, date, views) 50 most recent
- `data/shorts_open_probe.json` — local export probe: duration, VO onset, first-frame luma, black-frame detect

Screenshots (Studio overview, content, audience, reach, advanced table, first-frame contact sheets) are in the agent artifacts for this run; PNGs are gitignored in this repo.
