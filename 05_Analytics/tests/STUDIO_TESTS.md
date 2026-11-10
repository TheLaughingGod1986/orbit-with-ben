# Studio tests: the Monday test loop (Orbit With Ben + History of Science)

Ben, 26 Oct 2026: scoreboard and keeper-score ideas are tested in the real Studio against controls. Winners are written into the studio rules; losers are reverted. Chief runs the loop every Monday at about 09:30 London (routine "Monday Studio test loop"). This file is the log.

Ben, 26 Oct 2026 (pt4241u): *"These audit and ideas can we test these in the real studio and if we get positive results roll it onto the rules going forward, our goal should be a data driven approach, test, iterate and implement winning changes … I think we should do this on Mondays."*

**The loop, every Monday:** read the week's recommended-views scoreboard (`05_Analytics/owb/recommended_scoreboard_*.json`, HOS scoreboard alongside) → turn each idea into one test here (hypothesis, metric, test and control videos, 14-day baseline, originals saved word for word, start and end date) → make the edit through the YouTube Data API (title, description and tags only; never privacy, schedule or thumbnails; nothing deleted; no spend) and read it back → on the end date, read out the metric against the controls → a **winner** is written into the rules (`00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` for Orbit; `history-of-science` `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` for HOS) with its numbers; a **loser** is reverted from the originals below.

**Never in a test:** a video in a running test of any kind (Studio Test & Compare on title or thumbnail, `THUMB_LEDGER.json` rows marked running, the J0216 standalone Shorts test and its compilation `m09jUdwC5hk`, Shorts Test A in `SHORTS_TESTS.md`), and anything that's still scheduled and not yet public.

Data source for every number here: YouTube Analytics API v2 (`YT_ANALYTICS_REFRESH_TOKEN_OWB` / `_HOS`, read-only). Analytics lags about two days, so on 26 Oct the latest complete day was **23 Oct** and every baseline is **10–23 Oct 2026 (14 days)**. Impressions and CTR aren't available from the API for these videos (`videoThumbnailImpressions` returns 400); read them from Studio's Reach tab at readout if wanted. Raw pull: `studio_tests_2026-10-26/baseline_pull.json`. Originals: `studio_tests_2026-10-26/originals.json`.

## How the loop works

1. **Inputs.** That Monday's *Weekly recommended-views scoreboard (Orbit + HOS)* (~08:47 London; `05_Analytics/owb/recommended_scoreboard_<date>.*`, HOS `02_Video-Projects/_analytics/evidence_<date>_scoreboard/SCOREBOARD.json` in history-of-science) and the *Orbit weekly keeper score* (~08:12 London). Each "suggested change to try" becomes a proposal row below.
2. **Read out** every test whose end date is today or earlier: compare test videos against controls on the named metric, from real YouTube Analytics. Verdict: **winner** (write the rule into the docs workers read, per AGENTS.md > Changing the rules), **loser** (revert the listing to the logged original, verbatim), or **no clear result** (revert; note why).
3. **Start at most 1–2 new tests**, only when worth testing (the metric must be able to move in 14 days at the channel's current volume).
4. Commit this file by PR to `main`.

## Hard rules for every test

- Listing edits only, all reversible: title, description, tags, Shorts Related video. Through the channel's own Content Ops access (`07_Content-Ops/scripts/retitle-videos.ts`, `redescribe-videos.ts`, `update-shorts-listings.ts`). Confirm the channel name before any write.
- Never delete; never change privacy, publishAt or schedule; £0.
- Never use a video that is in another running test: thumbnail Test & Compare (`THUMB_LEDGER.json`), Shorts Tests A/B (`SHORTS_TESTS.md`), the J0216 standalone Shorts test (`00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md`), or anything else live on the board.
- Never touch anything Ben has OK'd that is scheduled and not yet public.
- **Log the original title and description verbatim here before the edit.**
- Baseline numbers come from real YouTube Analytics (API or Studio) with the date range stated. No real baseline, or no safe edit, means the row stays **proposed, not started** with the reason.
- Default length 14 days.

## Test register

| ID | Channel | Hypothesis | Metric | Test videos | Control videos | Baseline (source, range) | Start | End | Status / verdict |
|---|---|---|---|---|---|---|---|---|---|
| A | OWB | The exact search words viewers already type, in a long's title and description line 1, raise its YouTube-search views vs similar untouched longs | YT_SEARCH views per video, 27 Oct – 9 Nov vs baseline, test vs control (diff in diffs) | `ojk-dfOpAmw`, `Yk1tLh23rko`, `REXYxuLOBoI` | `b8-X_FyJnHM`, `2fsQcea-voM`, `55AEQwvs36g` | YouTube Analytics API v2, 10–23 Oct 2026 | 26 Oct 2026 | 9 Nov 2026 | **Running** (pass rule under *Test A*) |
| B | HOS | Using the subject phrases of the videos that already suggest the Atom film raises its suggested (RELATED_VIDEO) views vs the other HOS longs | RELATED_VIDEO views on `GHZDsiH7L7A`, window vs baseline, vs controls | `GHZDsiH7L7A` | `AL_-qlWko_g`, `_C92tIJCk8A`, `frP_YrNShsU` | YouTube Analytics API v2, 10–23 Oct 2026 | **Blocked on Fri 30 Oct 2026** (J0280 Title Test & Compare finished 29 Oct 17:54 inconclusive; Data API still returns `400 Precondition check failed` / `UPDATE_TITLE_NOT_ALLOWED_DURING_TEST_AND_COMPARE`; job J0978) | 9 Nov 2026 | **Blocked, not started** (pass rule under *Test B*) |

Original listings (verbatim, before edit) go under each test's *Originals (to revert)* block below.

## Originals

Test A: under *Test A > Originals (to revert)*, and `studio_tests_2026-10-26/originals.json`. Test B: under *Test B > Originals (to revert)* (nothing has been changed on it yet).

---

## Test A — Orbit long films: the exact search words in the title and line 1

| | |
|---|---|
| **Status** | **Running.** Edits made 26 Oct 2026 09:32 GMT, read back 09:34 GMT (`studio_tests_2026-10-26/test_a_apply_readback.json`). |
| **Source idea** | Scoreboard 17–23 Oct: Orbit longs got 15 views, 10 from search, 1 from suggested (6.7%). Proposal: put the exact words people search in long-film titles and the first description line. |
| **Hypothesis** | Putting the exact phrases viewers already type (from our own YT_SEARCH traffic-source detail) into a long's title and description line 1 raises that long's YouTube-search views, compared with similar longs left alone. |
| **Primary metric** | YT_SEARCH views per video, 27 Oct – 9 Nov (14 days) vs the 10–23 Oct baseline, test group against control group (difference in differences). |
| **Secondary** | Whether the inserted phrases appear in each test video's YT_SEARCH `insightTrafficSourceDetail`; total views; suggested (RELATED_VIDEO) views; avg % viewed (a search viewer who leaves fast is not a win). |
| **Pass** | The three test videos together gain **at least 5 more YT_SEARCH views than the three controls gain**, **and** at least two of the three test videos get search views on a phrase that was added. Anything less is **no result** (keep for another 14 days or revert); a drop in avg % viewed of more than 5 points on the test group is a **fail**. |
| **Start / end** | Start **26 Oct 2026** (edit day; first full day 27 Oct). End **9 Nov 2026**. Readout on the first Monday the Analytics API has data through 9 Nov (expected **Mon 16 Nov**; a provisional look on Mon 9 Nov with data to ~7 Nov). |
| **What changed** | Title and description line 1 only. Tags, the rest of the description, privacy, schedule and thumbnails untouched (verified by read-back). |

**Why these words (real YouTube search data).** Per-video search terms on these longs are very thin (most have none), so the phrases come from the channel's own YT_SEARCH terms, 1 Jul – 26 Oct 2026, which are mostly searches that found our Shorts on the same subjects:

| Search term (YT_SEARCH, channel) | Views |
|---|---:|
| andromeda | 16 |
| neutron star | 16 |
| orbital skybender | 11 |
| jwst latest update | 10 |
| last star | 9 |
| alien worlds | 7 |
| the last orbit | 7 |
| extraterrestrial life | 6 |
| sun | 6 |
| are they engineering the apocalypse | 5 |
| barnard's star | 5 |
| the last star | 5 |
| behind the scenes of movies | 4 |
| black dwarf | 4 |
| jwst | 4 |
| red dwarf | 4 |
| alien planets | 3 |
| andromeda galaxy | 3 |
| eclipse | 3 |
| exoplanets | 3 |
| final orbit 2026 trailer | 3 |
| how old is the universe | 3 |
| james webb space telescope live | 3 |
| milky way andromeda collision | 3 |
| milky way galaxy and andromeda collision | 3 |

**Test videos (edited)**

| Id | Old title | New title | Search evidence for the added words |
|---|---|---|---|
| `ojk-dfOpAmw` | What Happens When Andromeda Hits the Milky Way? | What Happens During the Milky Way Andromeda Collision? | "milky way andromeda collision" 3, "milky way galaxy and andromeda collision" 3, "andromeda galaxy" 3, "andromeda" 16 (channel, mostly via its Shorts) |
| `Yk1tLh23rko` | What Happens If You Get Near a Neutron Star | What Happens If You Get Near a Neutron Star or Pulsar? | "space pulsar" 2 (this video, its only search terms), "neutron star" 16 (channel) |
| `REXYxuLOBoI` | What Happens When the Last Star Dies? | The Last Star: What Happens When a Red Dwarf Dies? | "last star" 9, "the last star" 5, "red dwarf" 4, "black dwarf" 4 (channel) |

| Id | Old description line 1 | New description line 1 |
|---|---|---|
| `ojk-dfOpAmw` | In about 4 billion years, Andromeda fills our sky — and the galaxies don't smash into fireworks. | The Milky Way Andromeda collision: in about 4 billion years, the Andromeda galaxy fills our sky — and the galaxies don't smash into fireworks. |
| `Yk1tLh23rko` | What happens to your body near a neutron star — and what would you actually see as you got close? | What happens to your body near a neutron star or pulsar — and what would you actually see as you got close? |
| `REXYxuLOBoI` | What Happens When the Last Star Dies? | Orbit's Cosmic Journey | The last star in the universe will be a red dwarf. This is what happens when it dies — and why black dwarfs are what remains. |

**Controls (not edited):** `b8-X_FyJnHM` Alien Worlds, `2fsQcea-voM` Moon, `55AEQwvs36g` Saturn. Chosen as the nearest public longs not in any running or queued test. Note: Saturn's baseline is inflated by its launch push (192 subscriber views), which is why the metric is search views, not total views. Saturn and Moon are also in the compilation `m09jUdwC5hk` with all three test films, so compilation traffic hits both groups; Alien Worlds is not.

**Baselines, 10–23 Oct 2026 (14 days)**

| Role | Id | Title at baseline | Published | Lifetime views (26 Oct) | Views | YT_SEARCH views (share) | Suggested (RELATED_VIDEO) views (share) | Watch min | Avg % viewed | YT_SEARCH terms, publish→23 Oct |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Test | `ojk-dfOpAmw` | What Happens When Andromeda Hits the Milky Way? | 2026-09-24 | 4 | 0 | 0 (–) | 0 (–) | 0 | 0 | none |
| Test | `Yk1tLh23rko` | What Happens If You Get Near a Neutron Star | 2026-09-10 | 15 | 0 | 0 (–) | 0 (–) | 0 | 0 | "space pulsar" 2, "vicineko" 1 |
| Test | `REXYxuLOBoI` | What Happens When the Last Star Dies? | 2026-08-27 | 44 | 2 | 0 (0%) | 0 (0%) | 0 | 1.13 | "katie mack" 1, "red dwarf episode 1" 1, "wszechświat" 1 |
| Control | `b8-X_FyJnHM` | Alien Worlds: The Strangest Planets We've Ever Found | 2026-08-13 | 13 | 0 | 0 (–) | 0 (–) | 0 | 0 | "alien planets" 1 |
| Control | `2fsQcea-voM` | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone | 2026-09-17 | 5 | 0 | 0 (–) | 0 (–) | 0 | 0 | none |
| Control | `55AEQwvs36g` | How Long Do Saturn's Rings Have Left? | 2026-10-11 | 212 | 205 | 1 (0%) | 6 (3%) | 33 | 9.89 | none |

The baselines are close to zero (test group: 2 views, 0 from search; controls: 205 views, 1 from search). That makes this a low-power test: read it as "did search start finding these films at all", not as a precise lift.

**Not used (and why):** `h8HGfyShEHI` Sun (thumbnail test T012 until 1 Nov ~16:30), `VBaYRPp85Sw` Venus (T011 running), `vP1BbqZ_dnM` Betelgeuse (T010 running), `Mo93x0fxB1Q` Fermi, `NbW5G1BpPY0` Europa, `ziKBPJ6FY0U` JWST (T005–T007 running), `rVqgtkBV3jc` Light Speed (T004 running), `m09jUdwC5hk` the J0216 compilation (running), `3xrxdmaOwJI` Black Hole and `-jmMROGoZCM` Jupiter (thumbnail tests T002/T003 queued).

**Knock-ons to know about:** Shorts that show or say the film's exact live title (STUDIO_PLAYBOOK §6) now show the old title for these three films; the compilation's chapter cards also use the old titles. Neither was changed (the compilation is in a running test). J0216's "Orbit longs" comparison group includes these films; only their titles and line 1 changed.

**Originals (to revert):**

<details><summary><code>ojk-dfOpAmw</code> original title, description and tags (word for word)</summary>

Title:

```text
What Happens When Andromeda Hits the Milky Way?
```

Description:

````text
In about 4 billion years, Andromeda fills our sky — and the galaxies don't smash into fireworks.

Andromeda is already inbound. This film walks the honest clock, the night sky rewriting, why stars almost never hit, whether Earth survives the crash, and what one merged galaxy looks like after.

0:00 Andromeda is already coming
0:47 The Second Spiral
2:03 The Honest Clock
4:17 When the Night Sky Rewrites
5:44 Stars Almost Never Hit
7:11 Would We Survive?
8:50 What Else Is Coming

If you want more Thursday films like this, subscribe to Orbit With Ben.

#andromeda #milkyway #spacedocumentary
````

Tags: `["andromeda galaxy", "andromeda milky way collision", "astronomy", "documentary", "galactic merger", "galaxy collision", "milkomeda", "milky way", "nasa", "orbit with ben", "space documentary", "space facts"]`

</details>

<details><summary><code>Yk1tLh23rko</code> original title, description and tags (word for word)</summary>

Title:

```text
What Happens If You Get Near a Neutron Star
```

Description:

````text
What happens to your body near a neutron star — and what would you actually see as you got close?

A teaspoon of this leftover star outweighs mountains. Light leans. The last clear image in your eyes may not be the star at all. Orbit flies the approach, second by second: density, tides, a crust that is not a floor, and the line where “you” stops being a useful word.

This is not a black hole. It is worse in a different way.

Subscribe for the next film from Orbit with Ben.

Chapters
0:00 Orbit hangs in the dark
1:13 The Corpse of a Star
2:16 Density You Can't Imagine
3:36 What You Would See
5:45 What You Would Feel
7:39 The Surface That Isn't a Floor

Watch next
Could Life Exist Under The Ice Of Europa? — https://www.youtube.com/watch?v=NbW5G1BpPY0
````

Tags: `["astronomy shorts", "cosmic mysteries", "could you stand on a neutron star", "densest object in the universe", "extreme gravity", "gravitational lensing", "magnetar", "neutron star", "neutron star density", "neutron star explained", "neutron star vs black hole", "orbit with ben", "orbit's cosmic journey", "pulsar", "space documentary", "space shorts", "spaghettification", "teaspoon of a neutron star", "what happens if you fall into a neutron star", "what happens to your body near a neutron star"]`

</details>

<details><summary><code>REXYxuLOBoI</code> original title, description and tags (word for word)</summary>

Title:

```text
What Happens When the Last Star Dies?
```

Description:

````text
What Happens When the Last Star Dies? | Orbit's Cosmic Journey

Orbit rides deep time to the last star in the universe — and asks what remains when even that light fails.

Heat death explained without dreadbait: why stars stop being born, why red dwarfs outlive the Sun, and what "the end" actually means in physics. Real observations, honest uncertainty, and wonder without fearbait.

Chapters
0:00 — The Last Light
1:08 — When Stars Stop Being Born
2:34 — The Age of Red Dwarfs
4:17 — When the Last Star Dies
6:47 — What Remains
8:15 — Keep Looking

If you enjoy calm investigations into the biggest mysteries in the universe, subscribe to Orbit With Ben.

If you want to go further

A film can open a question. A good book sits with the uncertainty longer. The End of Everything, Katie Mack's look at how the universe might close, is the one I'd keep on the desk after this episode.

Playlist: Orbit's Cosmic Journey

Next film: Could Life Exist Under the Ice of Europa

#LastStar #HeatDeath #OrbitWithBen
````

Tags: `["astronomy", "astrophysics", "black dwarf", "cosmology", "cosmos", "deep time", "degenerate era", "dying stars", "end of the universe", "far future of the universe", "fate of the universe", "heat death explained", "heat death of the universe", "last light in the universe", "orbit with ben", "orbit's cosmic journey", "red dwarf stars", "red dwarfs", "science documentary", "space documentary", "star death explained", "stellar evolution", "the last star in the universe", "what happens when the last star dies"]`

</details>


---

## Test B — HOS Atom film: match the videos that suggest it

| | |
|---|---|
| **Status** | **Blocked, not started (30 Oct 2026, J0978).** On 26 Oct 09:32 GMT the Data API refused the title change (`400 Precondition check failed`). Title and description did not change; the tags did change in that call and were put back to the originals at 09:34 GMT (read back 09:35: title, line 1, tags, privacy all original). On **Fri 30 Oct 2026 07:21 UTC** (`J0978`), HOS Studio (`GHZDsiH7L7A` > `View test report`) showed the J0280 **Title and thumbnail** test had finished (`Test finished. Ran from 15 October 2026 at 18:00 to 29 October 2026 at 17:54. · Not enough impressions to declare a winner`), leaving Variant A (*What's Really Inside an Atom?*) `Now visible to all viewers` with watch-time share `—` on all three variants. However, because the edit page still holds the `A/B testing titles · Results ready` widget on the title field, the YouTube Data API (`07_Content-Ops/scripts/retitle-videos.ts`) again refused `PUT /youtube/v3/videos?part=snippet` with `400 Precondition check failed` (`reason: "UPDATE_TITLE_NOT_ALLOWED_DURING_TEST_AND_COMPARE"`). Because `retitle-videos.ts` ran first, no field was modified; API read-back (`studio_tests_2026-10-30/test_b_apply_readback.json`) confirmed title, line 1, full description, tags, privacy (`public`) and `publishAt` (`null`) all match `originals.json` verbatim. |
| **J0280 Title Test & Compare result (read 30 Oct 2026)** | **Mode:** `Title and thumbnail` (`15 October 2026 at 18:00 to 29 October 2026 at 17:54`). **Verdict:** `Not enough impressions to declare a winner`. **Variant A:** *What's Really Inside an Atom?* — `Now visible to all viewers`, watch-time share `—`. **Variant B:** *Why Is the Periodic Table in This Order?* — watch-time share `—`. **Variant C:** *How Small Can You Cut Gold?* — watch-time share `—`. Live title remains *What's Really Inside an Atom?*. |
| **Source idea** | HOS scoreboard 17–23 Oct: longs got 68% of views from suggested (up from 40%); most went to the Atom film, suggested from atom-history videos such as Science Retold's *How The True Size Of An Atom Was Discovered*. Proposal: match its title and description to those videos ("true size", "mostly empty space"). |
| **Hypothesis** | Using the subject phrases of the videos that already suggest the Atom film ("mostly empty space", "true size of an atom", "history of the atom") in its title, description line 1 and tags makes YouTube pair it with them more often, raising its suggested views compared with the other HOS longs. |
| **Primary metric** | RELATED_VIDEO views on `GHZDsiH7L7A`, test window vs the 10–23 Oct baseline, against the controls. |
| **Secondary** | Suggested views coming from `-a-EgwRmuQw` (*How The True Size Of An Atom Was Discovered*) and `Ul232hsiLbk` (*How Scientists Discovered Atoms Are Mostly Empty Space*) in `insightTrafficSourceDetail`; YT_SEARCH views and terms; avg % viewed. |
| **Pass** | Atom's suggested views in the window are **at least 1.5× its baseline (≥14)** and its share of views from suggested holds or rises, while the controls' suggested views don't rise by the same factor. Avg % viewed down more than 5 points = fail. Otherwise no result. |
| **Start / end** | Start: day after J0280 ends (about 29–30 Oct). End **9 Nov 2026** as briefed; that gives about 10 days, so the readout also checks 14 days from start. |
| **Planned change** | Title, description line 1 and tags (below). Rest of the description, privacy, schedule, thumbnails untouched. The J0280 winning title should be recorded first; if J0280 picks a different title, re-check that the new title still beats it before applying. |

| Id | Current title | Planned title |
|---|---|---|
| `GHZDsiH7L7A` | What's Really Inside an Atom? | What's Inside an Atom? Mostly Empty Space |

Planned description line 1 (replaces the current line 1 only):

> What's inside an atom? Mostly empty space. This is the history of the atom in four discoveries, from cutting a gold coin to find the true size of an atom, to Rutherford's tiny centre and the number that fixed the periodic table.

Planned tags: `["atom", "history of the atom", "inside an atom", "atoms are mostly empty space", "true size of an atom", "atomic number", "history of chemistry", "history of science", "moseley", "periodic table", "rutherford", "thomson", "dalton"]` (current: `["atom", "history of chemistry", "history of science", "moseley", "periodic table", "rutherford"]`).

Evidence: Atom's suggested views publish→23 Oct came from `-a-EgwRmuQw` Science Retold *How The True Size Of An Atom Was Discovered* (3), `Ul232hsiLbk` Science Retold *How Scientists Discovered Atoms Are Mostly Empty Space* (1) and five single views; its only search term is "history of the atom" (2). HOS rule §1.3 (the subject noun "atom" in title, line 1–2 and tags) still holds; channel names are not used.

**Controls (not edited):** `AL_-qlWko_g` Periodic Table, `_C92tIJCk8A` Germs, `frP_YrNShsU` X-rays (the other public HOS longs). Germs (T009, to ~5 Nov) and X-rays (T001, to ~28 Oct) have thumbnail tests running; they are controls only and aren't touched.

**Baselines, 10–23 Oct 2026 (14 days)**

| Role | Id | Title at baseline | Published | Lifetime views (26 Oct) | Views | YT_SEARCH views (share) | Suggested (RELATED_VIDEO) views (share) | Watch min | Avg % viewed | YT_SEARCH terms, publish→23 Oct |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Test | `GHZDsiH7L7A` | What's Really Inside an Atom? | 2026-10-15 | 26 | 19 | 4 (21%) | 9 (47%) | 16 | 12.18 | "history of the atom" 2 |
| Control | `AL_-qlWko_g` | How Did We Discover the Periodic Table? | 2026-09-17 | 150 | 14 | 3 (21%) | 10 (71%) | 17 | 16.09 | "history of the periodic table" 3, "history of periodic table" 1, "mendeleev" 1 |
| Control | `_C92tIJCk8A` | How Did We Discover Germs? | 2026-09-03 | 7 | 1 | 0 (0%) | 0 (0%) | 11 | 192.76 | none |
| Control | `frP_YrNShsU` | How Did We Discover X-rays? | 2026-09-24 | 3 | 0 | 0 (–) | 0 (–) | 0 | 0 | none |

**Originals (to revert):**

<details><summary><code>GHZDsiH7L7A</code> original title, description and tags (word for word)</summary>

Title:

```text
What's Really Inside an Atom?
```

Description:

````text
What's really inside an atom, and why is the periodic table in this order? Four discoveries, one century — from a knife and a gold coin to the number that fixed the table.

Cut gold in half, then again. How small can you go before it stops being gold? Dalton weighed atoms. Thomson found a piece inside them. Rutherford found their tiny centre. Moseley counted what was inside every element — and tellurium 52 finally sat before iodine 53 for a reason that wasn't weight.

A 3D cartoon film about the moment chemistry got a ruler that worked.

History of Science · Discovery. Wonder. Proof. · @HistoryOfScienceYT

#HistoryOfScience #Atom #PeriodicTable #AtomicNumber #Moseley #Rutherford #Thomson #Dalton

0:00 How small can you cut gold?
1:09 The table that broke its own rule
2:41 The crumb inside the atom
4:05 The shell that bounced back
5:55 Counting with X-rays

Sources: J. Dalton, A New System of Chemical Philosophy (1808); D. Mendeleev, Zeitschrift für Chemie 12 (1869); J. J. Thomson, "Cathode Rays", Philosophical Magazine 44 (1897); H. Geiger & E. Marsden, "On a Diffuse Reflection of the α-Particles", Proc. R. Soc. A 82 (1909); E. Rutherford, "The Scattering of α and β Particles by Matter and the Structure of the Atom", Philosophical Magazine 21 (1911); H. G. J. Moseley, "The High-Frequency Spectra of the Elements", Philosophical Magazine 26 (1913).
````

Tags: `["atom", "history of chemistry", "history of science", "moseley", "periodic table", "rutherford"]`

</details>


HOS keeps no general Studio-tests log in `history-of-science` (its tests sit per film, e.g. `02_Video-Projects/002_…/11_Upload-Package/AB_TEST_2026-09-27.md`), so Test B is logged here.

---

## Week of Mon 26 Oct 2026 (first run)

### Inputs found

- **OWB recommended-views scoreboard:** `05_Analytics/owb/recommended_scoreboard_2026-10-26.{json,txt}` (pulled 08:51 London). Analytics settled through 23 Oct, so the window is 17–23 Oct, not 19–25 Oct. 15 views on 14 longs: search 10, direct 3, browse 1, suggested 1 (6.7%). Prior window 12–18 Oct: 201 views, 189 of them browse (94%), suggested 2 (1%). No long had a view on all 7 days. Note: the two windows overlap on 17–18 Oct, so the "prior" total is not fully independent; the scoreboard script should use 10–16 Oct for the prior week (HOS already does).
- **HOS recommended-views scoreboard:** history-of-science `02_Video-Projects/_analytics/evidence_2026-10-26_scoreboard/SCOREBOARD.json` (08:51 London). Window 17–23 Oct: 19 views; Related video 13 (68.4%), up from 6 of 15 (40%) in 10–16 Oct. `GHZDsiH7L7A` (What's Really Inside an Atom?) took 15 views, 9 from Related video (Science Retold atom videos and others). `AL_-qlWko_g` got 4 from TED-Ed's Mendeleev video (3.69M views; also in the prior week).
- **Orbit keeper score (Mon 19–Sat 24 Oct):** no standalone output file found; its findings were turned straight into rules by PR #286 (Ben's rulings) and #287 (grandfather line), both merged 26 Oct. *Could a Robot Survive Touching the Sun?* 883 views, *Why Does a Day on Mercury Last Two of Its Years?* 849, *Saturn's Rings Are on a Clock* 12. Rules: one question per Short in the title and line 1, no statement/teaser titles, 22 s floor, Related video + description link to the matching long, Sun Shorts held until the `h8HGfyShEHI` thumbnail test ends 1 Nov.
- Neither routine wrote a "suggested change to try" list to disk; the proposals below are taken from the numbers above and from #286.

### Tests started or queued this week

- **Test A** (OWB search words on 3 longs): started 26 Oct 09:32 GMT, ends 9 Nov.
- **Test B** (HOS Atom `GHZDsiH7L7A`): queued; starts Fri 30 Oct 2026 (J0978), the day after J0280 ends.

### Read-outs due

None. No listing test with controls had an end date on or before 26 Oct. Running tests elsewhere (not read out here): thumbnail Test & Compare T001, T004–T007, T009–T012 (Studio estimates T001 ends ~28 Oct, T005–T007 ~29 Oct, T012 1 Nov); Shorts Test A (first readout Wed 18 Nov) and Test B (~10 Dec); J0216 standalone Shorts test (ends 20 Nov).

### Proposals

| ID | Channel | Proposal | Status | Why |
|---|---|---|---|---|
| P-2026-10-26-1 | OWB | Retitle older statement-titled public Shorts as one question (keeper score rule 1), against untouched statement-titled controls; metric 14-day views and search views. | proposed, not started | Volume. Public-view snapshots (Data API, 12 Oct 05:40 → 26 Oct 06:40 UTC): the 53 public OWB Shorts published before 5 Oct gained **10 views in total** over 14 days (max 3 on one Short). Test and control would both read ~0, so no verdict is possible. The rule is already in force for new cuts (#286), which is where it can be measured (the keeper score each week). The Saturn statement Short `6dcL5rBmHPM` (Fri 30 Oct) is OK'd and scheduled, so it's off limits anyway. |
| P-2026-10-26-2 | OWB | Add the description link to the matching long on public Shorts that lack it (keeper score rule: Related video + description link), metric the long's views from Shorts. | proposed, not started | The recent Shorts with real traffic overlap running tests: `n_4XskX0yZk` and `y-SPHQ0-VjQ` promote `h8HGfyShEHI` (thumbnail test T012, to 1 Nov); `vlkj8RQKmH8` is a J0216 test Short (unlinked until 20 Nov). Older Shorts get ~0 new views (above). Revisit on Mon 2 Nov once T012 has ended: Sun Shorts → `h8HGfyShEHI`, with a baseline of its Shorts-sourced views from Analytics. |
| P-2026-10-26-3 | OWB | Lift Suggested-video share on longs (6.7% of 15 views, 17–23 Oct) with listing changes. | proposed, not started | No concrete listing change came from the scoreboard, and 15 views a week across 14 longs is too few for a 14-day test (the 10 public longs published before 5 Oct gained 9 views in total, 12→26 Oct). Re-check when weekly long views are much higher. |
| P-2026-10-26-4 | HOS | Align `GHZDsiH7L7A`'s description/tags with the atom-history videos that suggest it (Related video is 68% of HOS long views). | proposed, not started | 15 views a week on the video. A 14-day test can't separate an edit effect from noise, and there's no comparable control long (the other public HOS longs had 0–4 views in the window; `frP_YrNShsU` and `_C92tIJCk8A` are in thumbnail tests T001/T009). Revisit if its weekly views pass ~100. Note: the same idea is now set up as **Test B** (above, from PR #289) with a 14-day baseline and a pass rule; it is queued behind J0280 and the low-volume caveat here applies to its readout. |

### Rules changed this week

None from this loop (no test ended). The keeper-score rules (#286, #287) were Ben's rulings, not a result from this loop.

---

## Readout log

| Date | Test | Result | Rule change |
|---|---|---|---|
| Fri 30 Oct 2026 | B | **blocked** (job J0978): J0280 title test finished 29 Oct 17:54 (`Not enough impressions to declare a winner`; Variant A *What's Really Inside an Atom?* visible to all, watch-time share `—` on A/B/C), but Data API still returned `400 Precondition check failed` (`UPDATE_TITLE_NOT_ALLOWED_DURING_TEST_AND_COMPARE`) while `A/B testing titles · Results ready` stays attached on Studio edit page; read-back (`studio_tests_2026-10-30/test_b_apply_readback.json`) verified all fields original | — |
| Mon 2 Nov 2026 | A | provisional look (data to ~31 Oct) | — |
| Mon 9 Nov 2026 | A, B | end date | — |
| Mon 16 Nov 2026 | A, B | final readout (data through 9 Nov) | — |
