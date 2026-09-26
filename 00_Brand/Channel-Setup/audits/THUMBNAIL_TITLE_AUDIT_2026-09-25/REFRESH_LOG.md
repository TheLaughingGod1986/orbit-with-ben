# Thumbnail refresh log — 25 Sep 2026

**Status: prepared, not applied.** No Studio uploads. No live thumb swaps.

Override note: Ben overrode the archived UAT bible "do not mass-recut older thumbs" line **only** for the Batch A/B ids in this job. House gate still applies (yellow hook, white rest, no Orbit, centre-safe). `ORBIT_HOUSE_AND_UAT_BIBLE.md` lives under `_archive/`; live rules are `THUMBNAIL_AND_TITLE_RULES.md` + `STUDIO_PLAYBOOK.md` §8.

Plate reality this run: no masters on disk (gitignored / sparse). yt-dlp blocked (bot wall). Plates from scrubbed current public thumbs when subject fits and Orbit is absent; else **NEEDS PLATE** (Ben AI Studio still, no AI text).

Builder: `tools/build_thumb_refresh_2026_09_25.py`. Spec: `refresh/JOBS.json` · apply plan: `refresh/APPLY_PLAN.json`. Contact sheets: `refresh/contact/contact_sheet_page{1,2}.jpg` (yellow border = swap pick).

## Baseline CTR (Studio, last 28 days, 28 Aug–24 Sep 2026)

Record before any swap. Re-check the same window shape **14 days after** each swap.

| id | impressions | CTR |
|---|---:|---:|
| `DN4L1DkerMM` | 95 | 1.1% |
| `PV50PX-bE4g` | 7 | 0% |
| `l1d1ypHxLk0` | 7 | 14.3% |
| `M-VN84HCNls` | 17 | 0% |
| `68uTDP2esso` | 46 | 0% |
| `SC2WGTl_V5Q` | 13 | 0% |
| `9lLZMy8rBJo` | 90 | 4.4% |
| `CkSECfUfH2Y` | 28 | 7.1% |
| `Yk1tLh23rko` | 202 | 2.5% |
| `REXYxuLOBoI` | 142 | 2.8% |
| `NbW5G1BpPY0` | 68 | 1.5% |
| `3xrxdmaOwJI` | 6 | 0% |
| `Mo93x0fxB1Q` | 13 | 0% |
| `ojk-dfOpAmw` | 16 | 0% |

## Apply mode (T&C vs swap)

**Default: `swap`.** Studio showed **no** Test & Compare on public long `Yk1tLh23rko`. Jupiter `-jmMROGoZCM` is **Ineligible** until public. No long has a confirmed T&C option in this pass — mark every long `swap`. Shorts are always outright replace (`swap`). One long at a time; keep A (current) as the baseline above; compare 14-day CTR after the swap.

| id | apply | swap pick (strongest of B/C) | why that pick |
|---|---|---|---|
| Batch A Shorts (all 8) | **swap** | the one new hook when plate ready | Shorts have no T&C |
| `Yk1tLh23rko` | **swap** (T&C absent) | **B CRUSHED FLAT** | 2 words, body impossibility; clearer than YOU'D BE FLAT |
| `REXYxuLOBoI` | **swap** | **B LAST LIGHT** | adds to the title; wonder, not dread |
| `NbW5G1BpPY0` | **swap** | **B A HIDDEN OCEAN** | “hidden” shape matches the film |
| `3xrxdmaOwJI` | **swap** (after plate) | **B NO WAY OUT** | stronger than repeating FALLING IN? |
| `Mo93x0fxB1Q` | **swap** | **C SILENCE** | one word, phone-readable; biggest break from EVERYBODY? |
| `ojk-dfOpAmw` | **swap** | **REP WHEN THEY MEET** | current COMING FOR US? confirmed; straight replacement |
| `-jmMROGoZCM` | **swap** when public | (pick after thumb preview) | T&C Ineligible until public |

## Batch A — Shorts

| id | old text | new text | plate source | preview | apply | baseline impr/CTR | date applied | 14d CTR |
|---|---|---|---|---|---|---|---|---|
| `DN4L1DkerMM` | THIS OCEAN / SHOULDN'T EXIST (wrong Europa plate) | RUNNING OUT OF / STARS | AI Studio needed | NEEDS PLATE | swap | 95 / 1.1% |  |  |
| `PV50PX-bE4g` | (Orbit reference grid / no hook) | NO / LIGHT | AI Studio needed | NEEDS PLATE | swap | 7 / 0% |  |  |
| `l1d1ypHxLk0` | next to / 13.8 billion | TOO / EARLY | AI Studio needed | NEEDS PLATE | swap | 7 / 14.3% |  |  |
| `M-VN84HCNls` | carbon under pressure | DIAMOND / PLANETS | AI Studio needed | NEEDS PLATE | swap | 17 / 0% |  |  |
| `68uTDP2esso` | 300 million years / after big bang | A HIDDEN / SECRET | AI Studio needed | NEEDS PLATE | swap | 46 / 0% |  |  |
| `SC2WGTl_V5Q` | watch the full film (Orbit) | GLASS / RAIN | AI Studio needed | NEEDS PLATE | swap | 13 / 0% |  |  |
| `9lLZMy8rBJo` | stage is empty | WHAT / REMAINS? | current bg scrubbed from oar2_9lLZMy8rBJo.jpg | BUILT preview PASS | swap | 90 / 4.4% |  |  |
| `CkSECfUfH2Y` | what if you / were here? | SKY GOING / DARK | current bg scrubbed from oar2_CkSECfUfH2Y.jpg | BUILT preview PASS | swap | 28 / 7.1% |  |  |

## Batch B — longs (variants built; apply = swap until T&C confirmed)

| id | variant | old text | new text | plate source | preview | apply / pick | baseline impr/CTR | date applied | 14d CTR |
|---|---|---|---|---|---|---|---|---|---|
| `Yk1tLh23rko` | B ★ | YOUR BODY / NEAR A NEUTRON STAR | CRUSHED / FLAT | current bg (scrub) from old_Yk1tLh23rko.jpg | BUILT preview PASS | **swap → B** | 202 / 2.5% |  |  |
| `Yk1tLh23rko` | C | YOUR BODY / NEAR A NEUTRON STAR | YOU'D BE / FLAT | current bg (scrub) from old_Yk1tLh23rko.jpg | BUILT preview PASS | (alt) | 202 / 2.5% |  |  |
| `REXYxuLOBoI` | B ★ | WHEN THE LAST STAR DIES | LAST / LIGHT | current bg (scrub) from old_REXYxuLOBoI.jpg — asteroid field interim | BUILT preview PASS | **swap → B** | 142 / 2.8% |  |  |
| `REXYxuLOBoI` | C | WHEN THE LAST STAR DIES | THEN / DARK | current bg (scrub) from old_REXYxuLOBoI.jpg | BUILT preview PASS | (alt) | 142 / 2.8% |  |  |
| `NbW5G1BpPY0` | B ★ | LIFE UNDER THE ICE / MORE WATER THAN EARTH | A HIDDEN / OCEAN | current bg (scrub) from old_NbW5G1BpPY0.jpg | BUILT preview PASS | **swap → B** | 68 / 1.5% |  |  |
| `NbW5G1BpPY0` | C | LIFE UNDER THE ICE / MORE WATER THAN EARTH | OCEAN / BELOW | current bg (scrub) from old_NbW5G1BpPY0.jpg | BUILT preview PASS | (alt) | 68 / 1.5% |  |  |
| `3xrxdmaOwJI` | B ★ | FALLING IN? (with Orbit) | NO WAY / OUT | AI Studio needed | NEEDS PLATE | **swap → B** (after plate) | 6 / 0% |  |  |
| `3xrxdmaOwJI` | C | FALLING IN? (with Orbit) | FALLING / IN? | AI Studio needed | NEEDS PLATE | (alt) | 6 / 0% |  |  |
| `Mo93x0fxB1Q` | B | WHERE IS EVERYBODY? (with Orbit) | WHERE IS / EVERYONE? | current bg (crop_left_hard) from old_Mo93x0fxB1Q.jpg | BUILT preview PASS | (alt) | 13 / 0% |  |  |
| `Mo93x0fxB1Q` | C ★ | WHERE IS EVERYBODY? (with Orbit) | SILENCE | current bg (crop_left_hard) from old_Mo93x0fxB1Q.jpg | BUILT preview PASS | **swap → C** | 13 / 0% |  |  |
| `ojk-dfOpAmw` | REP ★ | COMING FOR US? | WHEN THEY / MEET | current bg (scrub) from old_ojk-dfOpAmw.jpg | BUILT preview PASS | **swap → REP** | 16 / 0% |  |  |

## NEEDS PLATE

- `DN4L1DkerMM`
- `PV50PX-bE4g`
- `l1d1ypHxLk0`
- `M-VN84HCNls`
- `68uTDP2esso`
- `SC2WGTl_V5Q`
- `3xrxdmaOwJI`

## Jupiter `-jmMROGoZCM` (scheduled/private)

Primary / ABC paths from `020_…/11_Upload-Package/PACKAGE_MANIFEST.json`:

- `08_Thumbnail/Selected/jupiter_thumb_primary_cloud-deck.jpg`
- `08_Thumbnail/jupiter_thumb_A_no-floor.jpg`
- `08_Thumbnail/jupiter_thumb_B_cloud-deck.jpg`
- `08_Thumbnail/jupiter_thumb_C_the-fall.jpg`

**None of these files are in this sparse checkout.** Public i.ytimg returns 404 (private). Could not run `thumb_preview.py` on them. Ben: pull the four JPGs from the mini checkout and run previews locally.

## Andromeda Short title proposals (PROPOSE ONLY — Ben approves before anything is saved)

`019_Andromeda-Milky-Way-Collision` is absent from this checkout. Evidence used: live Short description for `P9Jiw-MwUEU` (*Andromeda is already coming for the Milky Way* / full film link), sound-check schedule titles, and the 21 Sep cluster plan (Fri = already getting bigger; Mon = stars almost never hit). Style matched to the fixed titles (*What Happens When Andromeda Hits the Milky Way?*, *The Last Stars Will Shine for 10 Trillion Years*, *This Star Is 20 km Wide and Heavier Than the Sun*): familiar noun early, no fear words, no hashtags, not a live duplicate.

### `P9Jiw-MwUEU` — live, *Is Andromeda Coming to Destroy Us?* (64 views)

Fails lane rule (“Destroy”). Film beat: Andromeda is already inbound / already in our sky.

| # | proposed | reason |
|---|---|---|
| 1 | **Is Andromeda Already in Our Sky?** | Yes/no about a familiar thing (Moon-winner shape); drops fear; matches the Short’s “already coming” promise. |
| 2 | **Andromeda Is Already Getting Bigger** | Statement shape like *The Last Stars Will Shine…*; names the visual beat (Andromeda growing in the sky) without threat. |

### `xQlV9G9lqLI` — scheduled 28 Sep, *What Happens When Andromeda Hits The Milky Way? #space…*

Will collide with the long’s retitle. Cluster beat: stars almost never hit in a galaxy merger.

| # | proposed | reason |
|---|---|---|
| 1 | **Stars Almost Never Hit When Galaxies Collide** | Body/impossibility shape (*Why You Can't Stand…*); says what the Short teaches; no hashtags; not a live duplicate. |
| 2 | **Why Stars Don't Crash When Galaxies Meet** | *Why…* search shape like the fixed Neutron/JWST lines; familiar “stars” in the first four words; softens “collide” without hedging. |

## Jupiter pinned comment (prepared)

Ben draft: *Galileo lasted 58 minutes and never found a floor. How far down do you think Orbit would get before turning back?*

Accuracy: matches upload description (`NASA’s Galileo probe… lasted about 58 minutes… never found a surface`). Film promise is cloud deck → light gone → metal dark / no floor. Draft is accurate.

**Proposed final (pin when public):**

> Galileo lasted about 58 minutes and never found a floor. How far down do you think Orbit would get before turning back?

(Adds "about" to match the description’s wording. Keep Orbit in the question — pinned comments are allowed to name him; thumbs are not.)

Already stored in `PINNED_COMMENTS.json` / `jupiter_long_pinned_v01.txt` is an older line; replace with the draft above when creating the pin.

## Captions

- Jupiter (`-jmMROGoZCM`): **no final locked VO script** in this checkout (sparse `020_…` has upload package + gen script only). Caption txt not produced.
- Andromeda (`ojk-dfOpAmw`): **project folder `019_Andromeda-Milky-Way-Collision` absent**. Caption txt not produced.

## Shorts sweep (grade only — not built)

Swept 46 public Shorts excluding Batch A. Failures: 34. Passes (heuristic): 12.

Full rows: `refresh/sweep/SWEEP_GRADE.json`.

| id | title | fail | proposed fix |
|---|---|---|---|
| `cmeBDZLzPHs` | Why Were Earth's Days Only Hours Long? | Orbit on thumb (score=0.260) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `rFzqmi8RWCY` | Why Does the Moon Drift 3.8 cm a Year? | Orbit on thumb (score=0.227) | Custom thumb: 3.8 CM A YEAR. Plate: strongest frame from that Short's master, no Orbit. |
| `osRFF1cBCEw` | (unknown — not in 25 Sep audit) | Orbit on thumb (score=0.227) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `BX-z1EkgANg` | One Second Near a Neutron Star Is Enough | Orbit on thumb (score=0.143) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `_8L9jYbDVmQ` | Why You Can't Stand on a Neutron Star | Orbit on thumb (score=0.122) | Custom thumb: CAN'T STAND. Plate: strongest frame from that Short's master, no Orbit. |
| `to-b2baeoWQ` | Could a Probe Get Closer to a Neutron Star? | Orbit on thumb (score=0.053) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `Rp_8J6_6IIk` | What Happens If You Touch a Neutron Star? | Orbit on thumb (score=0.208) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `o7ykyTDZKiE` | Your Last Clear Image Near a Neutron Star | Orbit on thumb (score=0.190) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `fhJP6eMoU0Q` | Your Atoms Near a Neutron Star Do Not Survive | Orbit on thumb (score=0.392) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `TE_HDKAnqms` | If Life Starts Under Ice, It's Everywhere | Orbit on thumb (score=0.123) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `eVp9a7f4rWg` | We Could Kill the Life We're Looking For | Orbit on thumb (score=0.060) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `VE0f186WQZo` | Europa Sprays Its Ocean Into Space | Orbit on thumb (score=0.062) | Custom thumb: HIDDEN OCEAN. Plate: strongest frame from that Short's master, no Orbit. |
| `Xza_jSHD4qw` | How Life Could Feed Under Europa With No Sun | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `pII09FbRYGc` | Why Europa Is Hiding a Massive Ocean. | Orbit on thumb (score=0.348) | Custom thumb: HIDDEN OCEAN. Plate: strongest frame from that Short's master, no Orbit. |
| `1glQuYFSaYQ` | What Would Life Eat Under Europa? | Orbit on thumb (score=0.144) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `8Bym-yrYhGc` | Why Europa's Ocean Shouldn't Exist | Orbit on thumb (score=0.060) | Custom thumb: HIDDEN OCEAN. Plate: strongest frame from that Short's master, no Orbit. |
| `keXe1GNxWSU` | Those Ice Scars Are How You Find It | Orbit on thumb (score=0.155) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `n2WbOfJhOwc` | Star Recycling Isn't Perfect | Orbit on thumb (score=0.411) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `KX-XU_AODoI` | What Happens When the Last Star Furnace Goes Cold | Orbit on thumb (score=0.120) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `GjcZB8826J8` | It Rains Glass Sideways on This Alien World | Orbit on thumb (score=0.042) | Custom thumb: GLASS RAIN. Plate: strongest frame from that Short's master, no Orbit. |
| `xRxhb3vSru4` | (unknown — not in 25 Sep audit) | Orbit on thumb (score=0.420) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `IVbO9XkkDps` | (unknown — not in 25 Sep audit) | Orbit on thumb (score=0.264) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `wIh3armF7_k` | The Last Star Will Be a Red Dwarf | Orbit on thumb (score=0.213) | Custom thumb: LAST RED DWARF. Plate: strongest frame from that Short's master, no Orbit. |
| `4-ZEpKD1yak` | Is the Universe Older Than We Thought? | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `P32uaiserG0` | What JWST's Infrared Eyes Can See | Orbit on thumb (score=0.176) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `P-li_ZWk4lg` | Why JWST Pictures Don't Match the Textbook | little/no readable hook type at centre | Custom thumb: DON'T MATCH. Plate: strongest frame from that Short's master, no Orbit. |
| `ZnsJTCcrTlA` | Black Holes Grew Too Big, Too Fast | Orbit on thumb (score=0.153) | Custom thumb: TOO BIG TOO FAST. Plate: strongest frame from that Short's master, no Orbit. |
| `03v4f1hlvtQ` | What If They're Leaving Us Alone On Purpose | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `QRi6Dxq0hz0` | We Could Smell Alien Life in a Spectrum | Orbit on thumb (score=0.120) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `tEOHYQbcgOw` | This Planet's Night Never Cools Down | Orbit on thumb (score=0.254) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `MDvAKtmKauw` | Three Suns in the Sky — Real Alien Worlds | Orbit on thumb (score=0.046) | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `iQUbmlaj4vk` | A Reply From the Stars Takes Generations | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `f8V6wCjWwHA` | Billions of Planets, Zero Signals | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |
| `ykmoxRJ6BOI` | We May Have Already Recorded Alien Life | little/no readable hook type at centre | Custom thumb: 2–4 word house hook from title promise (yellow on one word). Plate: strongest frame from that Short's master, no Orbit. |

