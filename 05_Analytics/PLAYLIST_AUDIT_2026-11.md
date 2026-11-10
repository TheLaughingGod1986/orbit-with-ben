# Playlist Audit — Orbit With Ben & History of Science (9 Nov 2026)

**Scope:** Read-only audit of all playlists in YouTube Studio across **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`, CDP port `9223`) and **History of Science** (`UCXp7HkBIl1LgaznXuZHJyRg`, CDP port `9222`), read on **9 November 2026** via `Studio > Content > Playlists` and `Studio > Analytics > Playlist analytics (Lifetime)`.

> **Important:**
> - **Removing a playlist never touches its videos.** Deleting a playlist in YouTube Studio only removes the playlist container; every video inside it remains published at its same URL with its views, comments, and analytics intact.
> - **Nothing has been changed in Studio.** All removals, merges, renames, and reorders below are proposals for Ben's **Ready-for-OK**.

---

## Executive Summary

Across both channels there are **9 public playlists** (**8** on Orbit With Ben, **1** on History of Science). Every single playlist currently has **0 lifetime playlist views** (`Views` column in `Studio > Content > Playlists` = `0`; `Views from playlist` in `Playlist analytics (Lifetime)` = `—`).

Why they get 0 views and what to clean up:
1. **Six outdated August/September playlists on Orbit With Ben duplicate or fragment the catalogue:**
   - Four playlists created on **25 Aug 2026** (`Black Holes Explained`, `Alien Life & The Search for Extraterrestrials`, `Alien Worlds & Exoplanets`, `James Webb Space Telescope Discoveries`) each contain **only 1 long film** followed by vertical Shorts cut from that same film.
     - `Black Holes Explained` (`PLEs4-0r_LBVQ`) has **4 Private Shorts** inside it, leaving only **1 public long + 1 public Short**.
     - `Alien Worlds & Exoplanets` (`PLH6Vkm2g0-q0`) has **3 Fermi Paradox Shorts misfiled inside it** alongside 1 Exoplanets long + 3 Exoplanets Shorts.
     - Putting a long film's own 25-second Shorts immediately after the long film in a playlist hurts session watch time: a viewer who finishes the 16:9 film is immediately auto-played vertical 25-second clips repeating scenes they just watched.
   - Two September long-form playlists (`What Space Would Do to You`, last updated 26 Sept, and `Start Here — Biggest Mysteries of Space`, last updated 19 Sept) are **100% duplicated** inside the two active long-form playlists updated on **6 Nov 2026** (`Real Worlds` and `What Would Happen If…`), while missing the newest and highest-viewed films (`What Happened to Venus?` and `How Long Do Saturn's Rings Have Left?`).
2. **Generic titles and chronological (oldest-first) ordering hide the best films:**
   - Titles like `Real Worlds`, `What Would Happen If…`, and `How Did We Discover…?` are internal format labels rather than phrases viewers type into YouTube Search.
   - Every long-form playlist is currently ordered **oldest first**, which buries the channels' strongest-performing films (`What Happened to Venus?` at #6 of 6 with 230 views; `How Long Do Saturn's Rings Have Left?` at #4 of 6 with 218 views; `How Did We Discover the Periodic Table?` at #2 of 6 with 161 views) behind the earliest low-view uploads.
3. **Two newest November longs are missing from playlists:**
   - OWB's `Could a Robot Survive on Mars?` (`Js6EQJ8qDi8`, published 8 Nov 2026) is not in any playlist yet.
   - HOS's `The Willow Tree That Was Made of Air` (`VbPubYd6Fbs`, published 5 Nov 2026) is not in the HOS playlist yet (though the 10 Dec 2026 compilation `uAomPaOBrM8` is already at #6).

---

## 1. Orbit With Ben (`@OrbitWithBen`, `UC_esArsDKd3GJvOkeO0DUog`)

### Summary Table (8 Playlists)

| # | Playlist Title | Playlist ID | Visibility | Video Count | Lifetime Playlist Views | Combined Views of Videos Inside (All Sources) | Last Updated | Proposal |
|---:|---|---|---|---:|---:|---:|---|---|
| 1 | **Real Worlds** | `PLdoEpeiktw_Y` | Public | **6** (6 public longs) | **0** | 518 (4.4 h) | 6 Nov 2026 | **KEEP + RENAME + REORDER** (+ add Mars `Js6EQJ8qDi8` & Jupiter `-jmMROGoZCM`) |
| 2 | **What Would Happen If…** | `PLOw2VKzGCOWU` | Public | **9** (9 public longs) | **0** | 99 (3.1 h) | 6 Nov 2026 | **KEEP + RENAME + REORDER** (+ add Mars `Js6EQJ8qDi8`; keep 47-min compilation last) |
| 3 | **What Space Would Do to You** | `PLQLwG0axcZis` | Public | **5** (5 public longs) | **0** | 85 (1.4 h) | 26 Sept 2026 | **MERGE into `PLOw2VKzGCOWU` & REMOVE** (all 5 longs already in `#1` / `#2`) |
| 4 | **Start Here — Biggest Mysteries of Space** | `PLI1AApUz3qz8` | Public | **9** (9 public longs) | **0** | 149 | 19 Sept 2026 | **MERGE into `#1` + `#2` & REMOVE** (all 9 longs already in `#1` / `#2`; misses all Oct/Nov films) |
| 5 | **Black Holes Explained** | `PLEs4-0r_LBVQ` | Public | **6** (**2 Public**: 1 long + 1 Short; **4 Private** Shorts) | **0** | 83 (62 public; 0.9 h) | 25 Aug 2026 | **REMOVE** (near-empty: only 1 public long + 1 Short; long `3xrxdmaOwJI` is in `#2`) |
| 6 | **Alien Life & The Search for Extraterrestrials** | `PLbTzVnzsyGm4` | Public | **5** (1 long + 4 Shorts from same film) | **0** | 113 | 25 Aug 2026 | **REMOVE** (1 long + its own 4 Shorts; long `Mo93x0fxB1Q` is in `#2`) |
| 7 | **Alien Worlds & Exoplanets** | `PLH6Vkm2g0-q0` | Public | **7** (1 long + 3 Exoplanet Shorts + 3 misfiled Fermi Shorts) | **0** | 205 | 25 Aug 2026 | **REMOVE** (1 long + Shorts with 3 wrong-film Shorts; long `b8-X_FyJnHM` is in `#1`) |
| 8 | **James Webb Space Telescope Discoveries** | `PLOgdBQBnJE2o` | Public | **7** (1 long + 6 Shorts from same film) | **0** | 402 | 25 Aug 2026 | **REMOVE** (1 long + its own 6 Shorts; long `ziKBPJ6FY0U` is in `#1`) |

---

### Detailed Contents & Proposals — Orbit With Ben

#### 1. `Real Worlds` (`PLdoEpeiktw_Y`) — **KEEP + RENAME + REORDER**
- **Current description:** *"Real places and real observations, told with real imagery."*
- **Current videos (6 longs, oldest first):**
  1. `b8-X_FyJnHM` — *Alien Worlds: The Strangest Planets We've Ever Found* (21:29 · Public · 13 Aug 2026 · 13 views)
  2. `ziKBPJ6FY0U` — *JWST Found Galaxies That Shouldn't Exist Yet* (16:33 · Public · 20 Aug 2026 · 33 views)
  3. `NbW5G1BpPY0` — *Could Life Exist Under The Ice Of Europa?* (9:19 · Public · 3 Sept 2026 · 15 views)
  4. `55AEQwvs36g` — *How Long Do Saturn's Rings Have Left?* (9:20 · Public · 11 Oct 2026 · 218 views)
  5. `h8HGfyShEHI` — *Is the Sun Getting Brighter?* (8:39 · Public · 18 Oct 2026 · 9 views)
  6. `VBaYRPp85Sw` — *What Happened to Venus?* (8:34 · Public · 25 Oct 2026 · 230 views)
- **Proposal:**
  - **Rename to searchable phrase:** `Solar System, Moons & Alien Planets Explained`
  - **Add missing planet longs:** `Could a Robot Survive on Mars?` (`Js6EQJ8qDi8`, published 8 Nov 2026) and `Why You Can't Stand On Jupiter` (`-jmMROGoZCM`, published 4 Oct 2026).
  - **Reorder (strongest views & retention first):**
    1. `VBaYRPp85Sw` — *What Happened to Venus?* (230 views · 84% at 0:15, 51% at 0:30)
    2. `55AEQwvs36g` — *How Long Do Saturn's Rings Have Left?* (218 views)
    3. `Js6EQJ8qDi8` — *Could a Robot Survive on Mars?* (newest long, 8 Nov 2026)
    4. `ziKBPJ6FY0U` — *JWST Found Galaxies That Shouldn't Exist Yet* (33 views · 98% at 0:15, 66% at 0:30)
    5. `NbW5G1BpPY0` — *Could Life Exist Under The Ice Of Europa?* (15 views)
    6. `h8HGfyShEHI` — *Is the Sun Getting Brighter?* (9 views)
    7. `-jmMROGoZCM` — *Why You Can't Stand On Jupiter* (5 views)
    8. `b8-X_FyJnHM` — *Alien Worlds: The Strangest Planets We've Ever Found* (13 views)

#### 2. `What Would Happen If…` (`PLOw2VKzGCOWU`) — **KEEP + RENAME + REORDER**
- **Current description:** *"Scenario films: what would happen if you stood on, fell into, or travelled through these places."*
- **Current videos (9 longs, oldest first):**
  1. `Mo93x0fxB1Q` — *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* (18:32 · Public · 30 Jul 2026 · 13 views)
  2. `3xrxdmaOwJI` — *What Happens If You Fall Into a Black Hole?* (21:13 · Public · 5 Aug 2026 · 5 views)
  3. `REXYxuLOBoI` — *The Last Star: What Happens When a Red Dwarf Dies?* (8:38 · Public · 27 Aug 2026 · 46 views)
  4. `Yk1tLh23rko` — *What Happens If You Get Near a Neutron Star or Pulsar?* (9:43 · Public · 10 Sept 2026 · 15 views)
  5. `2fsQcea-voM` — *Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone* (8:39 · Public · 17 Sept 2026 · 5 views)
  6. `ojk-dfOpAmw` — *What Happens During the Milky Way Andromeda Collision?* (10:21 · Public · 24 Sept 2026 · 4 views)
  7. `-jmMROGoZCM` — *Why You Can't Stand On Jupiter* (9:54 · Public · 4 Oct 2026 · 5 views)
  8. `m09jUdwC5hk` — *How Long Will Anything in Space Last?* (47:38 compilation · Public · 21 Oct 2026 · 6 views)
  9. `rVqgtkBV3jc` — *What Happens If You Travel Near Light Speed?* (8:12 · Public · 1 Nov 2026 · 0 views)
- **Proposal:**
  - **Rename to searchable phrase:** `What Happens If You Fall Into Black Holes, Neutron Stars & Extreme Space?`
  - **Add:** `Could a Robot Survive on Mars?` (`Js6EQJ8qDi8`, published 8 Nov 2026).
  - **Reorder (lead with tight 8–10 min scenario films and best retention; keep the 47:38 compilation last):**
    1. `REXYxuLOBoI` — *The Last Star: What Happens When a Red Dwarf Dies?* (46 views · 73% at 0:15)
    2. `Yk1tLh23rko` — *What Happens If You Get Near a Neutron Star or Pulsar?* (15 views)
    3. `rVqgtkBV3jc` — *What Happens If You Travel Near Light Speed?* (8:12)
    4. `Js6EQJ8qDi8` — *Could a Robot Survive on Mars?* (8 Nov 2026)
    5. `-jmMROGoZCM` — *Why You Can't Stand On Jupiter* (5 views)
    6. `2fsQcea-voM` — *Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone* (5 views)
    7. `ojk-dfOpAmw` — *What Happens During the Milky Way Andromeda Collision?* (4 views)
    8. `Mo93x0fxB1Q` — *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* (13 views)
    9. `3xrxdmaOwJI` — *What Happens If You Fall Into a Black Hole?* (5 views)
    10. `m09jUdwC5hk` — *How Long Will Anything in Space Last?* (47:38 compilation — last slot)

#### 3. `What Space Would Do to You` (`PLQLwG0axcZis`) — **MERGE into `PLOw2VKzGCOWU` & REMOVE**
- **Current videos (5 longs):** `2fsQcea-voM` (Moon, 5 views), `REXYxuLOBoI` (Last Star, 46 views), `Yk1tLh23rko` (Neutron Star, 15 views), `NbW5G1BpPY0` (Europa, 15 views), `ojk-dfOpAmw` (Andromeda, 4 views).
- **Why remove:** 0 playlist views; last updated 26 Sept 2026; superseded by `PLOw2VKzGCOWU` (*What Would Happen If…*) and `PLdoEpeiktw_Y` (*Real Worlds*), which already contain all 5 of these videos.

#### 4. `Start Here — Biggest Mysteries of Space` (`PLI1AApUz3qz8`) — **MERGE into `PLdoEpeiktw_Y` + `PLOw2VKzGCOWU` & REMOVE**
- **Current videos (9 longs):** `Mo93x0fxB1Q` (Fermi, 13 views), `3xrxdmaOwJI` (Black Hole, 5 views), `b8-X_FyJnHM` (Alien Worlds, 13 views), `ziKBPJ6FY0U` (JWST, 33 views), `2fsQcea-voM` (Moon, 5 views), `Yk1tLh23rko` (Neutron Star, 15 views), `NbW5G1BpPY0` (Europa, 15 views), `REXYxuLOBoI` (Last Star, 46 views), `ojk-dfOpAmw` (Andromeda, 4 views).
- **Why remove:** 0 playlist views; last updated 19 Sept 2026; all 9 films are already in `PLdoEpeiktw_Y` (3 films) and `PLOw2VKzGCOWU` (6 films), while the 7 newer October/November longs (including the channel's top two longs, Venus and Saturn's Rings) are missing.

#### 5. `Black Holes Explained` (`PLEs4-0r_LBVQ`) — **REMOVE**
- **Current videos (6 in Studio, only 2 Public):**
  1. `3xrxdmaOwJI` — *What Happens If You Fall Into a Black Hole?* (21:13 · **Public** · 5 views)
  2. `tUAdhOnMW2g` — *Time Appears to Stop at a Black Hole* (0:28 · **Private** · 9 views)
  3. `B2STcIAF1lY` — *What You Would See Falling Into a Black Hole* (0:28 · **Public** · 57 views)
  4. `9ez9BeqGBtE` — *The Event Horizon Is a One-Way Line* (0:27 · **Private** · 4 views)
  5. `kBkWtBMKPqE` — *Falling Into a Black Hole Feels Like Nothing* (0:27 · **Private** · 5 views)
  6. `5-sofIhR0lI` — *What You'd See Looking Back From a Black Hole* (0:25 · **Private** · 3 views)
- **Why remove:** 0 playlist views; last updated 25 Aug 2026; 4 of its 6 videos are Private, leaving only 1 public long + 1 public Short. The long (`3xrxdmaOwJI`) is already in `PLOw2VKzGCOWU`.

#### 6. `Alien Life & The Search for Extraterrestrials` (`PLbTzVnzsyGm4`) — **REMOVE**
- **Current videos (5 videos: 1 long + 4 Shorts from the same film):**
  1. `Mo93x0fxB1Q` — *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* (18:32 · Public · 13 views)
  2. `f8V6wCjWwHA` — *Billions of Planets, Zero Signals* (0:27 · Public · 16 views)
  3. `ykmoxRJ6BOI` — *Is Alien Life Already Hiding in Our Data?* (0:27 · Public · 10 views)
  4. `03v4f1hlvtQ` — *What If They're Leaving Us Alone On Purpose* (0:25 · Public · 57 views)
  5. `iQUbmlaj4vk` — *A Reply From the Stars Takes Generations* (0:25 · Public · 17 views)
- **Why remove:** 0 playlist views; last updated 25 Aug 2026; contains only 1 long film plus 4 vertical Shorts cut from that exact same film. The long (`Mo93x0fxB1Q`) is already in `PLOw2VKzGCOWU`.

#### 7. `Alien Worlds & Exoplanets` (`PLH6Vkm2g0-q0`) — **REMOVE**
- **Current videos (7 videos: 1 long + 3 Exoplanet Shorts + 3 misfiled Fermi Paradox Shorts):**
  1. `b8-X_FyJnHM` — *Alien Worlds: The Strangest Planets We've Ever Found* (21:29 · Public · 13 views)
  2. `SC2WGTl_V5Q` — *This Planet's Rain Is Molten Glass* (0:23 · Public · 25 views)
  3. `tEOHYQbcgOw` — *This Planet's Night Never Cools Down* (0:23 · Public · 18 views)
  4. `M-VN84HCNls` — *We Found Planets Made of Diamond* (0:23 · Public · 66 views)
  5. `03v4f1hlvtQ` — *What If They're Leaving Us Alone On Purpose* (0:25 · Public · 57 views — *Fermi Paradox Short*)
  6. `f8V6wCjWwHA` — *Billions of Planets, Zero Signals* (0:27 · Public · 16 views — *Fermi Paradox Short*)
  7. `ykmoxRJ6BOI` — *Is Alien Life Already Hiding in Our Data?* (0:27 · Public · 10 views — *Fermi Paradox Short*)
- **Why remove:** 0 playlist views; last updated 25 Aug 2026; contains only 1 long film (already in `PLdoEpeiktw_Y`), 3 Shorts cut from it, and 3 Fermi Paradox Shorts added by mistake.

#### 8. `James Webb Space Telescope Discoveries` (`PLOgdBQBnJE2o`) — **REMOVE**
- **Current videos (7 videos: 1 long + 6 Shorts from the same film):**
  1. `ziKBPJ6FY0U` — *JWST Found Galaxies That Shouldn't Exist Yet* (16:33 · Public · 33 views)
  2. `68uTDP2esso` — *The Early Universe Is Hiding a Massive Secret* (0:27 · Public · 54 views)
  3. `4-ZEpKD1yak` — *Is the Universe Older Than We Thought?* (0:29 · Public · 75 views)
  4. `P32uaiserG0` — *What JWST's Infrared Eyes Can See* (0:27 · Public · 39 views)
  5. `P-li_ZWk4lg` — *Why JWST Pictures Don't Match the Textbook* (0:25 · Public · 83 views)
  6. `ZnsJTCcrTlA` — *Black Holes Grew Too Big, Too Fast* (0:27 · Public · 22 views)
  7. `l1d1ypHxLk0` — *These Galaxies Appeared Too Early* (0:25 · Public · 96 views)
- **Why remove:** 0 playlist views; last updated 25 Aug 2026; contains only 1 long film (already in `PLdoEpeiktw_Y`) plus 6 vertical Shorts cut from that same film.

---

## 2. History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`)

### Summary Table (1 Playlist)

| # | Playlist Title | Playlist ID | Visibility | Video Count | Lifetime Playlist Views | Combined Views of Videos Inside (All Sources) | Last Updated | Proposal |
|---:|---|---|---|---:|---:|---:|---|---|
| 1 | **How Did We Discover…? \| History of Science** | `PLEbpfUzWzcXU` | Public | **6** (5 public longs + 1 scheduled compilation) | **0** | 209 (3.1 h) | 29 Oct 2026 | **KEEP + RENAME + REORDER** (+ add missing 5 Nov long `VbPubYd6Fbs`) |

---

### Detailed Contents & Proposal — History of Science

#### 1. `How Did We Discover…? | History of Science` (`PLEbpfUzWzcXU`) — **KEEP + RENAME + REORDER**
- **Current description:** *"Animated stories of how we discovered the things science now takes for granted, told in the order they happened: germs, the periodic table, X-rays, and more to come."*
- **Current videos (6 in Studio: 5 public longs + 1 scheduled compilation):**
  1. `_C92tIJCk8A` — *How Did We Discover Germs?* (6:05 · Public · 3 Sept 2026 · 7 views)
  2. `AL_-qlWko_g` — *How Did We Discover the Periodic Table?* (9:01 · Public · 17 Sept 2026 · 161 views)
  3. `frP_YrNShsU` — *How Did We Discover X-rays?* (7:06 · Public · 24 Sept 2026 · 5 views)
  4. `GHZDsiH7L7A` — *What's Really Inside an Atom?* (8:45 · Public · 15 Oct 2026 · 31 views)
  5. `wwcjcFfC-5M` — *The Tied Arm That Proved Your Blood Circulates* (8:49 · Public · 29 Oct 2026 · 5 views)
  6. `uAomPaOBrM8` — *How Did Experiments Explain Blood, Germs and Atoms?* (49:19 compilation · **Scheduled 10 Dec 2026** · 0 views)
- **Missing public long:** `VbPubYd6Fbs` — *The Willow Tree That Was Made of Air* (published 5 Nov 2026 · 2 views).
- **Proposal:**
  - **Rename to searchable subject phrase:** `How We Discovered Atoms, the Periodic Table, Germs & X-Rays | History of Science` (replaces the generic *"How Did We Discover…?"* with the actual searched discovery subjects).
  - **Add missing public long:** Add `VbPubYd6Fbs` (*The Willow Tree That Was Made of Air*) before the 49-minute compilation.
  - **Reorder (lead with the breakout 161-view Periodic Table film and its 31-view Atom sequel, with the 49-minute compilation last):**
    1. `AL_-qlWko_g` — *How Did We Discover the Periodic Table?* (161 views · 71% at 0:15, 51% at 0:30)
    2. `GHZDsiH7L7A` — *What's Really Inside an Atom?* (31 views · natural continuation from Mendeleev to Rutherford & Moseley)
    3. `frP_YrNShsU` — *How Did We Discover X-rays?* (5 views)
    4. `_C92tIJCk8A` — *How Did We Discover Germs?* (7 views)
    5. `wwcjcFfC-5M` — *The Tied Arm That Proved Your Blood Circulates* (5 views)
    6. `VbPubYd6Fbs` — *The Willow Tree That Was Made of Air* (2 views — add)
    7. `uAomPaOBrM8` — *How Did Experiments Explain Blood, Germs and Atoms?* (49:19 compilation, scheduled 10 Dec 2026 — keep last)

---

## 3. Ready-for-OK Checklist (Waiting on Ben's OK)

Nothing has been modified in YouTube Studio. Once Ben OKs:

1. **Orbit With Ben — Remove 6 zero-view duplicate / single-episode playlists** *(deleting a playlist never touches its videos)*:
   - [ ] Remove `PLEs4-0r_LBVQ` (*Black Holes Explained* — 0 views, 4 of 6 videos are Private, long is in `PLOw2VKzGCOWU`)
   - [ ] Remove `PLbTzVnzsyGm4` (*Alien Life & The Search for Extraterrestrials* — 0 views, 1 long + 4 repeat Shorts, long is in `PLOw2VKzGCOWU`)
   - [ ] Remove `PLH6Vkm2g0-q0` (*Alien Worlds & Exoplanets* — 0 views, 1 long + 3 Exoplanet Shorts + 3 misfiled Fermi Shorts, long is in `PLdoEpeiktw_Y`)
   - [ ] Remove `PLOgdBQBnJE2o` (*James Webb Space Telescope Discoveries* — 0 views, 1 long + 6 repeat Shorts, long is in `PLdoEpeiktw_Y`)
   - [ ] Remove `PLQLwG0axcZis` (*What Space Would Do to You* — 0 views, all 5 longs already in `PLOw2VKzGCOWU` / `PLdoEpeiktw_Y`)
   - [ ] Remove `PLI1AApUz3qz8` (*Start Here — Biggest Mysteries of Space* — 0 views, all 9 longs already in `PLdoEpeiktw_Y` / `PLOw2VKzGCOWU`)
2. **Orbit With Ben — Keep, rename, add Mars (`Js6EQJ8qDi8`), and reorder the 2 active long-form playlists:**
   - [ ] `PLdoEpeiktw_Y`: Rename `Real Worlds` → `Solar System, Moons & Alien Planets Explained`, add `Js6EQJ8qDi8` (*Mars*) and `-jmMROGoZCM` (*Jupiter*), and reorder with `VBaYRPp85Sw` (*Venus*, 230 views) and `55AEQwvs36g` (*Saturn's Rings*, 218 views) at #1 and #2.
   - [ ] `PLOw2VKzGCOWU`: Rename `What Would Happen If…` → `What Happens If You Fall Into Black Holes, Neutron Stars & Extreme Space?`, add `Js6EQJ8qDi8` (*Mars*), and reorder with `REXYxuLOBoI` (*The Last Star*, 46 views) and `Yk1tLh23rko` (*Neutron Star*, 15 views) at #1 and #2, keeping the 47-min compilation `m09jUdwC5hk` last.
3. **History of Science — Keep, rename, add Willow Tree (`VbPubYd6Fbs`), and reorder the 1 long-form playlist:**
   - [ ] `PLEbpfUzWzcXU`: Rename `How Did We Discover…? | History of Science` → `How We Discovered Atoms, the Periodic Table, Germs & X-Rays | History of Science`, add `VbPubYd6Fbs` (*The Willow Tree That Was Made of Air*), and reorder with `AL_-qlWko_g` (*Periodic Table*, 161 views) at #1 and `GHZDsiH7L7A` (*Inside an Atom*, 31 views) at #2, keeping the 49-min compilation `uAomPaOBrM8` last.

---

## 4. Applied (10 Nov 2026, J2460)

Ben's yes, 9 Nov 2026. Full record, with every read-back and the contents of the six removed playlists for rebuilding: `jobs/reviews/J2460/PLAYLIST_REFS.md`.

**Orbit With Ben, done 06:10 to 06:15 UTC:**

- Four things pointed at the six and were repointed first: Saturn `55AEQwvs36g` end screen (the *Start Here* element removed; it already carried *Real Worlds*), the Europa `NbW5G1BpPY0` description link (now *Real Worlds*), and Home sections 0 and 8 (now *What Would Happen If…* and *Real Worlds*).
- All six removed: `PLQLwG0axcZis`, `PLbTzVnzsyGm4`, `PLOgdBQBnJE2o`, `PLH6Vkm2g0-q0`, `PLEs4-0r_LBVQ`, `PLI1AApUz3qz8`. No video was touched: 179 before, 179 after, same titles, privacy and schedule.
- `PLdoEpeiktw_Y` is now **Real Worlds: Solar System, Moons and Alien Planets Explained**, 8 films, in the order of section 1 above (Mars and Jupiter added).
- `PLOw2VKzGCOWU` is now **What Would Happen If…: Black Holes, Neutron Stars and Extreme Space**, 10 films, in the order of section 1 above (Mars added, compilation last).
- The names are the Chief's (series name kept, search phrase after it, LEARNINGS rule 20), not the renames proposed in sections 1 and 3.
- Playlist list read back: those two and nothing else.

**History of Science: not applied yet.** `PLEbpfUzWzcXU` still needs its rename to "How Did We Discover…? Atoms, the Periodic Table, Germs and X-Rays | History of Science", `VbPubYd6Fbs` added and the reorder of section 2.

