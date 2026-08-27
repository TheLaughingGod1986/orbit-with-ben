# Orbit with Ben — full YouTube audit

**Date:** Tuesday 25 Aug 2026, evening UK  
**Channel:** Orbit with Ben (`@OrbitWithBen` · `UC_esArsDKd3GJvOkeO0DUog`)  
**Age:** 29 days (created 27 Jul 2026)

**Night addendum (~23:00 UK):** RSS views refreshed; social ops + queue folded into **`FULL_AUDIT.md`** (same folder). Key deltas: today’s JWST Short `68uTDP2esso` **17 → 30** views; TikTok hard-paused; indexes 001–003 still stale; JWST has no Shorts index in-repo.

**Data this run**

| Source | What we got | Confidence |
|--------|-------------|------------|
| vidIQ `channel_stats` + `channel_videos` (long, recent) | Subs, lifetime views, 5 longs | **HIGH** |
| YouTube RSS (latest 15 public) | Views + likes on current shelf | **HIGH** |
| Watch-page scrape of known IDs | Older longs + a few extra Shorts | **MEDIUM** (HTML can lie on “unavailable”) |
| vidIQ Analytics reports / title scores / keywords | **Failed** — credits exhausted mid-pull | — |
| YouTube Data API catalogue | **Failed** — daily quota exceeded | — |

vidIQ leftover: **4** add-on credits. Renewable bucket empty until **30 Aug 22:23 UTC**. Do not spend on generate/score until then.

Raw: `vidiq_raw.json` · `public_views.json` · full pack: `FULL_AUDIT.md`

---

## Executive verdict

The channel is a **Shorts discovery engine with almost no long-form hold yet**. That is normal at 4 subscribers. It is **not** a reason to rewrite the brand, chase fearbait, or recut shipped films.

- **4 subscribers · 949 lifetime views · 27 videos** (vidIQ).
- Public longs we can see: **about 34 combined views** (Fermi 10 · Alien Worlds 10 · JWST 7 · Black Hole 4 · Last Star 3). Last Star is still a **premiere** (Thu 27 Aug), so 3 is not a post-launch read.
- Public Shorts we can see: **roughly 870 views**. The RSS shelf alone is ~8–9× the entire long catalogue.
- The Shorts that work are the ones that already match the locked title formula: **a drawable strange image, a named subject, the wrongness in the line**.
- The longs that are live are still the **18–21 minute** first generation, except JWST at **16:33**. The lock for everything new is **7–9 minutes**. Do not copy the live runtimes.

**What to take into the next films (Neutron Star, then Moon):** keep punch-first Shorts, scene-first packaging, VO-literal picture, Orbit in the scene, 7–9 min longs. Fix ops hygiene (indexes still name deleted IDs). Do not spend generation budget recutting old Shorts to remove Orbit.

---

## 1. What is working

### Shorts titles that look like a real shelf

Public views tonight (RSS + scrape). Age varies; treat rank as directional, not a league table.

| Views | Title | Why it fits |
|------:|-------|-------------|
| **141** | Three Suns in the Sky — Real Alien Worlds (`MDvAKtmKauw`) | Concrete image. Remake of a weak original. Diamond-bar pattern. |
| **122** | Most of the Universe Gives Off No Light (`PV50PX-bE4g`) | S1: strange fact, drawable, named subject. #2 Short on the channel. |
| **89** | These Galaxies Appeared Too Early (`l1d1ypHxLk0`) | Same shape. JWST launch Short. |
| **83** | Why JWST Pictures Don't Match the Textbook (`P-li_ZWk4lg`) | S3: named subject + contradiction. |
| **69** | Why This Alien World Looks Like a Giant Eye (`OlwENQcY-jg`) | Drawable object in the title. |
| **68** | Is the Universe Older Than We Thought? (`4-ZEpKD1yak`) | S6: the wrongness is inside the question. |
| **63** | We Found Planets Made of Diamond (`M-VN84HCNls`) | S2. House winner / 223% viewed in the earlier punch study. |
| **56** | What You Would See Falling Into a Black Hole (`B2STcIAF1lY`) | S4 experiential. Weaker than diamond — still a real title. |

The pattern is stable from 1 Aug through 25 Aug: **image words first, subject named, no series suffix, no orphan “this/it”.**

### Craft locks that earned their keep

These are already in the rules. The last three weeks confirmed them in production, not just on paper.

1. **Punch-first 22–27s Shorts.** Early 44s cuts sat ~20% stayed-to-watch (4 Aug). Do not go back to 40s+.
2. **Picture tells the story.** Neutron Part 02 (17 Aug): teaspoon vs mountains. Mute the VO and you still follow the beat. At most one Orbit + distant-object hang per minute.
3. **Orbit in the video is fine.** 25 Aug measure on 20 public Shorts: Orbit-led median **47** views vs scenery-led **20.5**, Pearson **r = +0.09**. The #2 Short is ~85% Orbit-dominated. **Scene-first is a cover/thumb rule, not a recut rule.**
4. **≥2 pure-scenery plates per minute** so Shorts have a native cover frame. Orbit-only minutes force parent-film rescues.
5. **Shorts covers: Studio desktop only.** Data API `thumbnails.set` returns ok, letterboxes 9:16 into 16:9, never fills the vertical slot. Daily Studio cap is real.
6. **Never grab a fixed-% frame** for a cover. That landed on Orbit faces and burned-in captions.
7. **Open/end craft:** first 3s strange picture only; Orbit after ~8s; last 10s real picture for Studio end screens. No brand sting, no baked subscribe.
8. **One-minute Omni path + Ben UAT.** Europa 01–08 and Neutron parts. Do not gen a whole episode in one pass.

### Ops that is now healthier

- Playlists (JWST, Start Here, Alien Life, Alien Worlds, Black Holes) cleaned of deleted items on 25 Aug.
- JWST Shorts index has live IDs + files, so today’s Short can mirror.
- Social LaunchAgents reloaded; Threads posted today’s JWST Short.

---

## 2. What is not working (or not working yet)

### Longs are cold — and still too long

| Film | Runtime | Views tonight | Notes |
|------|--------:|--------------:|-------|
| Fermi `Mo93x0fxB1Q` | 18:32 | **10** | First pillar. Series-suffix era. |
| Alien Worlds `b8-X_FyJnHM` | 21:29 | **10** | Same generation. |
| JWST `ziKBPJ6FY0U` | 16:33 | **7** | Shorter, still no Browse hold. Live 5 days. |
| Black Hole `3xrxdmaOwJI` | 21:13 | **4** | Weakest public long. |
| Last Star `REXYxuLOBoI` | premiere | **3** | **Do not judge.** Goes live Thu 27 Aug 18:00. Title still has `\| Orbit's Cosmic Journey`. |
| Europa `NbW5G1BpPY0` | scheduled | — | Thu 3 Sept. |
| Neutron `Yk1tLh23rko` | scheduled | — | Next to *make*, not next to air. Broadcast v02 **8.89 min**. Do not mint until Ben watches. |

Channel-level APV / CTR / traffic mix **could not be pulled tonight**. Last honest long note (4–6 Aug, LOW_DATA): ~3–5 views, search-ish, openings not proven. Do not invent a CTR story.

**Implication:** the 21-minute Alien Worlds / Black Hole / Fermi films are a **catalogue**, not a template. Neutron already sits in the 7–9 lock. Keep it there.

### The Shorts → long funnel is not converting yet

JWST is the cleanest current test: six public cluster Shorts at **17–89 views**, parent long at **7**. Related + pin are required; they are not yet a watch-time machine. At 4 subs that is **expected**. The job is still: Short earns the click, listing + first 15s of the long earn the stay.

Do not add `/go/` or shop voice to “help” the funnel.

### Weak or orphan Shorts

| Views | Title | Lesson |
|------:|-------|--------|
| 19 | Black Holes Grew Too Big, Too Fast | Abstract process, not a picture. |
| 17 | JWST Keeps Finding Galaxies Too Big, Too Soon | Same idea as better JWST titles; too soon to call (posted today). |
| 16 | This Planet's Night Never Cools Down | Superlative / weather, weak picture words (matches the formula’s proven miss). |
| **9** | Time Appears to Stop at a Black Hole (`tUAdhOnMW2g`) | Public, **not in the uploads playlist**. Every audit that only walks Uploads misses it. |

Deleted / superseded IDs from the first generations scrape as unavailable (Fermi v02 cluster, old exo IDs, old BH cluster). That is correct — do not resurrect them.

### Indexes 001–003 are stale again

The live shelf is **not** what `SHORTS_UPLOAD_INDEX.json` says for Fermi / Black Hole / Alien Worlds:

- 001 still points at `1HuV8o3gOss` etc. (unavailable).
- 002 still lists the deleted BH cluster as `scheduled`.
- 003 still lists `ho9VJxp7f3A` / `aoR-dA_g7eI` as scheduled while the **live** diamond / three-suns IDs are `M-VN84HCNls` and `MDvAKtmKauw`.

Social mirrors and the full-film comment watcher read these files. Seeding saved us from dumping corpses today; the files still need a **true** live-ID rewrite.

### Packaging still mixed on longs

- Last Star public title still has the **series suffix**.
- JWST’s live long title is *JWST Found Galaxies That Shouldn't Exist Yet* (fine) while several Shorts reuse adjacent wording — cluster is OK, just don’t clone the weakest line.
- Scene-first **punch-text 9:16 covers** are staged, not live. Desktop grid was fixed with Select-from-video (0 broken tiles). Studio custom-cover job is **13:15 daily**. Mobile cache can lag.

### Tooling limits (ops, not creative)

- YouTube Data API **quota blown** — no inventory pull until reset.
- vidIQ **4 credits** — no scoring / keyword refresh until 30 Aug.
- TikTok mirror failed on today’s Short (`upload_error`). Threads succeeded. Meta was in-flight at 15:30.

---

## 3. Lessons to take into the next videos

Apply these on Neutron Star Shorts, Europa’s remaining packaging, and anything after. Do not silently regress.

### Picture and story

1. **One VO idea → one literal image.** If they disagree, the picture is wrong.
2. **Mute test** every minute. If you could swap the plate with the last Orbit-hang, rewrite it.
3. **Character in the world:** bank / skim / push-off / one bottom glow. No sticker Orbit. No second face.
4. **≥2 no-Orbit scenery plates per ~60s** — covers and Shorts depend on them.
5. **7–9 minutes now.** Expand only after an 8-min film gets real impressions **and** hold stays past ~5 min.
6. **You-beats** (Kurzgesagt steal, Marcus Jones lock): talk to one viewer, more than once, then a next-film end screen. Not a shop close. Not a 10s logo void.

### Titles and thumbs

7. Write Short titles from **S1–S6 only**. Kill test: drawable · named subject · no hashtag · no series suffix · wrongness in the line.
8. Thumbs / covers: **the object is the poster**. Orbit off by default. ≤4 words on the thumb.
9. Score titles in vidIQ after **30 Aug** (`type=long` / `type=short`, ≥90). Brand overrides a higher fearbait score.
10. Upload Shorts covers in **Studio on a computer**. Never bulk `thumbnails.set`.

### Shorts cluster

11. **4–8 punch Shorts**, 22–27s, captions the whole way, Thursday film title on screen, loop the open into the last 4s.
12. Related + pinned `Full film — {title}: https://www.youtube.com/watch?v={ID}`. Zero `/go/` on Shorts.
13. Prefer a **native scenery cover** from that minute. If the Short is Orbit-only, crop the parent film.
14. Recut = **new ID**. Leave the old live until the remake is public, then unpublish. Three Suns is the proof.

### Production path

15. **One minute at a time.** Write → VO → plates → assemble → Ben UAT → next minute.
16. Script ≥90 and the episode gate before VO / Flow.
17. Affiliate only if **this** cut names the product. Neutron: no book unless the locked VO names one.

### Ops (so the next cluster does not lie to the robots)

18. After every upload, write the **live** ID + `file` + `visibility` into the index. Confirm with `search.list forMine`, not Uploads alone.
19. Seed social ledgers before any index rewrite.
20. Keep `tUAdhOnMW2g` in the mental inventory (or add it to 002’s live index).

---

## 4. What to do next (priority)

| # | Action | Why |
|---|--------|-----|
| 1 | Ben watches Neutron **broadcast v02** (~8:53). Do not mint. Finish the close jewel if you still want it. | Next long is already the right length. |
| 2 | Leave Last Star premiere **27 Aug 18:00** alone. After it airs, strip the series suffix if Studio still shows it, then start the A/B that is waiting. | 3 views is not a verdict. |
| 3 | Tomorrow: confirm `dev.orbit.shorts-covers` (13:15). If Studio says Verify, Ben must click it. Re-check the desktop Shorts grid. | Punch-text covers are the unfinished packaging job. |
| 4 | Rebuild 001–003 indexes to the **live** IDs (and add `tUAdhOnMW2g`). | Mirrors and comment watchers still read corpses. |
| 5 | After 30 Aug: vidIQ title scores on the live shelf + Neutron title ABC; keyword refresh for neutron star / Europa. | Credits are gone tonight. |
| 6 | Do **not** start 013 Moon or 015 Simulation. Do **not** recut old Shorts to remove Orbit. | Queue lock + 25 Aug evidence. |

---

## 5. What we are *not* changing

- Orbit character and British VO.
- Wonder over dread. No conspiracy, no fearbait titles.
- One long / week, Shorts as the discovery layer.
- Named-in-film affiliate gate.
- “Algorithm = audience.” Browse will come when strangers come back. Four subs is not a sample for a niche pivot.
