# J2460: what points at the six playlists (Orbit With Ben)

Read on 10 Nov 2026, about 03:25 UTC, by Claude Code on the Mini. Scheduled longs added about 05:25 UTC. **Applied 10 Nov 2026, 06:10 to 06:15 UTC: see "Applied" just below. The rest of this file is the state as read before any change.**

## How it was read

- Playlists, their videos, Home sections and every video description: YouTube Data API, read-only calls (`playlists.list`, `playlistItems.list`, `channelSections.list`, `videos.list`), signed in as `UC_esArsDKd3GJvOkeO0DUog` (Orbit With Ben).
- End screens and cards on public longs: the public watch page (`ytInitialPlayerResponse.endscreen` and `.cards`), the same method as `05_Analytics/live_fixes/2026-10-15.md`.
- Channel comments: `commentThreads.list` on all 91 public videos (39 threads in total), keeping any comment written by the channel that names a playlist.

## Scheduled longs: read in Studio, 10 Nov 2026 about 05:25 UTC (read-only)

Read in the Orbit Studio tab on CDP 9223 (channel checked on every page: `UC_esArsDKd3GJvOkeO0DUog`). Each video's End screen and Cards editors were opened and Studio's own answers (`get_creator_endscreens`, `list_creator_info_cards`) were read; the page was reloaded without saving. **None of the five uses a playlist anywhere, so none points at the six.**

| Scheduled long | End screen | Cards |
|---|---|---|
| `c5AdqQsnnys` (15 Nov) | subscribe · video `rVqgtkBV3jc` | one video card: `rVqgtkBV3jc` |
| `6bbbvfCx6zY` (22 Nov) | subscribe · video `VBaYRPp85Sw` | none |
| `F-jImX5h7ws` (29 Nov) | subscribe · video "best for viewer" | one video card: `c5AdqQsnnys` |
| `G5uMANXHtNU` (2 Dec) | subscribe · video "best for viewer" | none |
| `vP1BbqZ_dnM` (6 Dec) | subscribe · video "best for viewer" | one video card: `F-jImX5h7ws` |

## Applied, 10 Nov 2026 (Orbit With Ben), 06:10 to 06:15 UTC

By Claude Code on the Mini, on Ben's yes of 9 Nov (job brief). Channel checked before every write: `UC_esArsDKd3GJvOkeO0DUog`. No video was deleted; no title, thumbnail, privacy or schedule was changed.

### Step 2, the four references repointed and read back

| # | Where | Before | After (read back) | How |
|---:|---|---|---|---|
| 1 | Saturn `55AEQwvs36g` end screen | video · subscribe · playlist *Start Here* `PLI1AApUz3qz8` · playlist *Real Worlds* `PLdoEpeiktw_Y` | video · subscribe · playlist *Real Worlds* `PLdoEpeiktw_Y` | Studio end-screen editor on CDP 9223: the *Start Here* element deleted, saved. Read back in the editor after a reload, and on the public watch page (which lagged about three minutes, then showed three elements and no `PLI1AApUz3qz8`) |
| 2 | Europa `NbW5G1BpPY0` description | `Playlist: Orbit's Cosmic Journey https://www.youtube.com/playlist?list=PLI1AApUz3qz8` | `Playlist: Real Worlds https://www.youtube.com/playlist?list=PLdoEpeiktw_Y` | Data API `videos.update`, that one line only. Title, tags, category, languages and privacy read back unchanged |
| 3 | Home section, position 0 | `PLQLwG0axcZis` | `PLOw2VKzGCOWU` | Data API `channelSections.update` |
| 4 | Home section, position 8 | `PLOgdBQBnJE2o` | `PLdoEpeiktw_Y` | Data API `channelSections.update` |

### Step 3, re-check and removal

A fresh survey after the repoints (all 195 upload rows' descriptions, the nine Home sections, end screens and cards of the 16 public longs, channel comments on 91 public videos) found no reference to five of the six; those were removed first. Saturn's public page still showed *Start Here* for about three minutes, so that playlist was held until the public page was clear, then removed. Each title was matched against the audit immediately before removal. Contents of all six are under "Contents of the six, for rebuilding" below and were unchanged since the first read.

| Playlist id | Title | Videos | Removed (UTC) |
|---|---|---:|---|
| `PLQLwG0axcZis` | What Space Would Do to You | 5 | 06:13 |
| `PLbTzVnzsyGm4` | Alien Life & The Search for Extraterrestrials | 5 | 06:13 |
| `PLOgdBQBnJE2o` | James Webb Space Telescope Discoveries | 7 | 06:13 |
| `PLH6Vkm2g0-q0` | Alien Worlds & Exoplanets | 7 | 06:13 |
| `PLEs4-0r_LBVQ` | Black Holes Explained | 6 | 06:13 |
| `PLI1AApUz3qz8` | Start Here — Biggest Mysteries of Space | 9 | 06:15 |

### Step 4, the two kept Orbit playlists (read back)

`PLdoEpeiktw_Y`, now **Real Worlds: Solar System, Moons and Alien Planets Explained** (public, description unchanged). Added Mars `Js6EQJ8qDi8` and Jupiter `-jmMROGoZCM`. Order: `VBaYRPp85Sw`, `55AEQwvs36g`, `Js6EQJ8qDi8`, `ziKBPJ6FY0U`, `NbW5G1BpPY0`, `h8HGfyShEHI`, `-jmMROGoZCM`, `b8-X_FyJnHM`.

`PLOw2VKzGCOWU`, now **What Would Happen If…: Black Holes, Neutron Stars and Extreme Space** (public, description unchanged). Added Mars `Js6EQJ8qDi8`. Order: `REXYxuLOBoI`, `Yk1tLh23rko`, `rVqgtkBV3jc`, `Js6EQJ8qDi8`, `-jmMROGoZCM`, `2fsQcea-voM`, `ojk-dfOpAmw`, `Mo93x0fxB1Q`, `3xrxdmaOwJI`, `m09jUdwC5hk`.

### Read-back after everything (06:15 UTC)

- Playlists on the channel: the two above, nothing else.
- Videos: 179 distinct ids before, 179 after, none missing. Title, privacy and go-public time identical on every one. Descriptions differ from the 03:26 read on two: Europa `NbW5G1BpPY0` (row 2 above) and `6bbbvfCx6zY`, which this job never wrote to (changed by other work between 03:26 and 06:15).
- Home sections: position 0 `PLOw2VKzGCOWU`, position 8 `PLdoEpeiktw_Y`, the other seven untouched.

### History of Science playlist `PLEbpfUzWzcXU`, 10 Nov 2026 about 08:35 UTC

Done in Studio on CDP 9222 (`?authuser=1`; the content list showed channel `UCXp7HkBIl1LgaznXuZHJyRg`, History of Science, one playlist).

- **Renamed and read back:** *How Did We Discover…? | History of Science* is now **How Did We Discover…? Atoms, the Periodic Table, Germs and X-Rays | History of Science**. Studio Details tab, Save (`edit_playlist` 200), page reloaded: new title shown, still Public, description unchanged.

### Not done yet

- **Add `VbPubYd6Fbs` (Willow Tree) and reorder `PLEbpfUzWzcXU`.** Still 6 videos in date order (Germs, Periodic Table, X-rays, Atom, Tied Arm, compilation `uAomPaOBrM8`). Studio's Videos tab only lists them; adding and ordering go through "Edit in YouTube" (`youtube.com/playlist?list=PLEbpfUzWzcXU`), and there this browser's sign-in is a viewer, not the channel (it shows Subscribe and Save playlist, no edit controls, with or without `authuser=1`). Two things to try next, in this order: (1) Studio Content > Videos, tick `VbPubYd6Fbs`, "Add to playlist" (a playlist action, the video itself is not edited); (2) Studio Details > Default video order > Manual, then see whether the Videos tab allows moving rows. If the order cannot be set from this sign-in it needs the History of Science identity on youtube.com or a History of Science Data API login, neither of which is on the Mini today.

## Playlist ids

The API returns the same 13-character ids the audit uses; these are the full ids.

| Playlist id | Title (live) | Videos | Six or kept |
|---|---|---:|---|
| `PLdoEpeiktw_Y` | Real Worlds | 6 | kept |
| `PLOw2VKzGCOWU` | What Would Happen If… | 9 | kept |
| `PLQLwG0axcZis` | What Space Would Do to You | 5 | one of the six |
| `PLbTzVnzsyGm4` | Alien Life & The Search for Extraterrestrials | 5 | one of the six |
| `PLOgdBQBnJE2o` | James Webb Space Telescope Discoveries | 7 | one of the six |
| `PLH6Vkm2g0-q0` | Alien Worlds & Exoplanets | 7 | one of the six |
| `PLEs4-0r_LBVQ` | Black Holes Explained | 6 | one of the six |
| `PLI1AApUz3qz8` | Start Here — Biggest Mysteries of Space | 9 | one of the six |

All six titles match the audit.

## References found: four

Two Home sections, one end-screen element and one description link. The job brief knew only of row 1.

| # | Where | Points at | Swap to (step 2) |
|---:|---|---|---|
| 1 | End screen of Saturn `55AEQwvs36g` (*How Long Do Saturn's Rings Have Left?*): playlist element *Start Here — Biggest Mysteries of Space* | `PLI1AApUz3qz8` | Remove the element: the same end screen already carries *Real Worlds* `PLdoEpeiktw_Y`, the kept playlist that holds Saturn |
| 2 | Description of Europa `NbW5G1BpPY0` (*Could Life Exist Under The Ice Of Europa?*): link with `list=PLI1AApUz3qz8` | `PLI1AApUz3qz8` | `PLdoEpeiktw_Y` (*Real Worlds* holds Europa) |
| 3 | Home tab, section at position 0: single playlist | `PLQLwG0axcZis` (*What Space Would Do to You*) | `PLOw2VKzGCOWU` (*What Would Happen If…*) |
| 4 | Home tab, section at position 8: single playlist | `PLOgdBQBnJE2o` (*James Webb Space Telescope Discoveries*) | `PLdoEpeiktw_Y` (*Real Worlds* holds the JWST long) |

Note for the Chief on row 2: swapping it means editing a video description. The brief's step 2 covers links, and its last line protects only title, thumbnail, privacy and schedule, so I read it as allowed; say if not.

## Checked and clear

- **End screens, 16 public longs.** Only Saturn uses one of the six. Every other playlist element is `PLdoEpeiktw_Y` or `PLOw2VKzGCOWU`.
- **Cards, 16 public longs.** Each has one card entry with no video or playlist link in it. On Saturn, the one opened in full, it is YouTube's own "View corrections" teaser; the other 15 were checked only for links, not for what the card is.
- **Descriptions, all 195 uploads (public, scheduled and private).** Only Europa names a playlist.
- **Channel comments, 91 public videos.** No comment by the channel names a playlist, so no pinned comment does.
- **Home sections.** Nine sections; the two above are the only ones tied to a playlist. One section is "all playlists", which lists whatever exists and needs no change.

## End screens as read (public longs)

| Video | Elements |
|---|---|
| `Js6EQJ8qDi8` Could a Robot Survive on Mars? (One Lasted 14 Years) | channel `UC_esArsDKd3GJvOkeO0DUog` · video `-jmMROGoZCM` |
| `rVqgtkBV3jc` What Happens If You Travel Near Light Speed? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `Mo93x0fxB1Q` · playlist `PLOw2VKzGCOWU` |
| `VBaYRPp85Sw` What Happened to Venus? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `b8-X_FyJnHM` · playlist `PLdoEpeiktw_Y` |
| `m09jUdwC5hk` How Long Will Anything in Space Last? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `rVqgtkBV3jc` · playlist `PLOw2VKzGCOWU` |
| `h8HGfyShEHI` Is the Sun Getting Brighter? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `VBaYRPp85Sw` · playlist `PLdoEpeiktw_Y` |
| `55AEQwvs36g` How Long Do Saturn's Rings Have Left? | video `y-SPHQ0-VjQ` · channel `UC_esArsDKd3GJvOkeO0DUog` · playlist `PLI1AApUz3qz8` · playlist `PLdoEpeiktw_Y` |
| `-jmMROGoZCM` Why You Can't Stand On Jupiter | channel `UC_esArsDKd3GJvOkeO0DUog` · video `m09jUdwC5hk` · playlist `PLOw2VKzGCOWU` |
| `ojk-dfOpAmw` What Happens During the Milky Way Andromeda Collision? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `-jmMROGoZCM` · playlist `PLOw2VKzGCOWU` |
| `2fsQcea-voM` Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone | channel `UC_esArsDKd3GJvOkeO0DUog` · video `ojk-dfOpAmw` · playlist `PLOw2VKzGCOWU` |
| `Yk1tLh23rko` What Happens If You Get Near a Neutron Star or Pulsar? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `2fsQcea-voM` · playlist `PLOw2VKzGCOWU` |
| `NbW5G1BpPY0` Could Life Exist Under The Ice Of Europa? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `55AEQwvs36g` · playlist `PLdoEpeiktw_Y` |
| `REXYxuLOBoI` The Last Star: What Happens When a Red Dwarf Dies? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `Yk1tLh23rko` · playlist `PLOw2VKzGCOWU` |
| `ziKBPJ6FY0U` JWST Found Galaxies That Shouldn't Exist Yet | channel `UC_esArsDKd3GJvOkeO0DUog` · video `NbW5G1BpPY0` · playlist `PLdoEpeiktw_Y` |
| `b8-X_FyJnHM` Alien Worlds: The Strangest Planets We've Ever Found | channel `UC_esArsDKd3GJvOkeO0DUog` · video `ziKBPJ6FY0U` · playlist `PLdoEpeiktw_Y` |
| `3xrxdmaOwJI` What Happens If You Fall Into a Black Hole? | channel `UC_esArsDKd3GJvOkeO0DUog` · video `REXYxuLOBoI` · playlist `PLOw2VKzGCOWU` |
| `Mo93x0fxB1Q` Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | channel `UC_esArsDKd3GJvOkeO0DUog` · video `3xrxdmaOwJI` · playlist `PLOw2VKzGCOWU` |

## Contents of the six, for rebuilding

Order is the playlist's own order. Privacy is each video's, as the API reports it.

### `PLQLwG0axcZis` What Space Would Do to You

Description: What would really happen to you out there? Neutron stars, black holes, the last star and alien oceans, explained with Orbit.

1. `2fsQcea-voM` Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone (public)
2. `REXYxuLOBoI` The Last Star: What Happens When a Red Dwarf Dies? (public)
3. `Yk1tLh23rko` What Happens If You Get Near a Neutron Star or Pulsar? (public)
4. `NbW5G1BpPY0` Could Life Exist Under The Ice Of Europa? (public)
5. `ojk-dfOpAmw` What Happens During the Milky Way Andromeda Collision? (public)

### `PLbTzVnzsyGm4` Alien Life & The Search for Extraterrestrials

Description: Why haven't we found aliens yet? The Fermi Paradox, quiet skies, and the possibility that the first clue is already in an archive — Orbit's alien-life cluster.

1. `Mo93x0fxB1Q` Why Haven't We Found Aliens Yet? The Fermi Paradox Explained (public)
2. `f8V6wCjWwHA` Billions of Planets, Zero Signals (public)
3. `ykmoxRJ6BOI` Is Alien Life Already Hiding in Our Data? (public)
4. `03v4f1hlvtQ` What If They're Leaving Us Alone On Purpose (public)
5. `iQUbmlaj4vk` A Reply From the Stars Takes Generations (public)

### `PLOgdBQBnJE2o` James Webb Space Telescope Discoveries

Description: Galaxies that appeared too early, black holes that grew too fast, and infrared eyes on cosmic dawn — what JWST actually found, told with Orbit's careful curiosity.

1. `ziKBPJ6FY0U` JWST Found Galaxies That Shouldn't Exist Yet (public)
2. `68uTDP2esso` The Early Universe Is Hiding a Massive Secret (public)
3. `4-ZEpKD1yak` Is the Universe Older Than We Thought? (public)
4. `P32uaiserG0` What JWST's Infrared Eyes Can See (public)
5. `P-li_ZWk4lg` Why JWST Pictures Don't Match the Textbook (public)
6. `ZnsJTCcrTlA` Black Holes Grew Too Big, Too Fast (public)
7. `l1d1ypHxLk0` These Galaxies Appeared Too Early (public)

### `PLH6Vkm2g0-q0` Alien Worlds & Exoplanets

Description: Diamond crusts, glass rain sideways, three suns, and glowing hot nights — Orbit explores the strangest exoplanets we've ever found. Full Alien Worlds film plus Shorts.

1. `b8-X_FyJnHM` Alien Worlds: The Strangest Planets We've Ever Found (public)
2. `SC2WGTl_V5Q` This Planet's Rain Is Molten Glass (public)
3. `tEOHYQbcgOw` This Planet's Night Never Cools Down (public)
4. `M-VN84HCNls` We Found Planets Made of Diamond (public)
5. `03v4f1hlvtQ` What If They're Leaving Us Alone On Purpose (public)
6. `f8V6wCjWwHA` Billions of Planets, Zero Signals (public)
7. `ykmoxRJ6BOI` Is Alien Life Already Hiding in Our Data? (public)

### `PLEs4-0r_LBVQ` Black Holes Explained

Description: What happens if you fall into a black hole? Event horizons, time dilation, and the strangest moments from Orbit's black hole journey — full film plus supporting Shorts.

1. `3xrxdmaOwJI` What Happens If You Fall Into a Black Hole? (public)
2. `tUAdhOnMW2g` Time Appears to Stop at a Black Hole (private)
3. `B2STcIAF1lY` What You Would See Falling Into a Black Hole (public)
4. `9ez9BeqGBtE` The Event Horizon Is a One-Way Line (private)
5. `kBkWtBMKPqE` Falling Into a Black Hole Feels Like Nothing (private)
6. `5-sofIhR0lI` What You'd See Looking Back From a Black Hole (private)

### `PLI1AApUz3qz8` Start Here — Biggest Mysteries of Space

Description: Begin with Orbit's Cosmic Journey: the Fermi Paradox, falling into a black hole, strange alien worlds, and what the James Webb Space Telescope found at cosmic dawn. Cinematic space storytelling — wonder over clickbait.

1. `Mo93x0fxB1Q` Why Haven't We Found Aliens Yet? The Fermi Paradox Explained (public)
2. `3xrxdmaOwJI` What Happens If You Fall Into a Black Hole? (public)
3. `b8-X_FyJnHM` Alien Worlds: The Strangest Planets We've Ever Found (public)
4. `ziKBPJ6FY0U` JWST Found Galaxies That Shouldn't Exist Yet (public)
5. `2fsQcea-voM` Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone (public)
6. `Yk1tLh23rko` What Happens If You Get Near a Neutron Star or Pulsar? (public)
7. `NbW5G1BpPY0` Could Life Exist Under The Ice Of Europa? (public)
8. `REXYxuLOBoI` The Last Star: What Happens When a Red Dwarf Dies? (public)
9. `ojk-dfOpAmw` What Happens During the Milky Way Andromeda Collision? (public)

## Claude Code run, 10 Nov 2026 about 10:25 to 10:45 UTC (no playlist changed)

- **Orbit re-read by Data API (read-only):** the channel has two playlists and nothing else. `PLdoEpeiktw_Y` *Real Worlds: Solar System, Moons and Alien Planets Explained* (8 films) and `PLOw2VKzGCOWU` *What Would Happen If…: Black Holes, Neutron Stars and Extreme Space* (10 films) are both in the audit's order. Home sections 0 and 8 point at `PLOw2VKzGCOWU` and `PLdoEpeiktw_Y`. The only playlist link in any of 195 upload descriptions is Europa `NbW5G1BpPY0` to `PLdoEpeiktw_Y`.
- **History of Science add and reorder: still not done.** Studio's playlist Videos tab (9222) has "Add to playlist" and "Edit in YouTube" but no way to move rows. On `youtube.com` in that browser the account switcher lists four identities: Benjamin Oats, OpptiAI, Orbit With Ben and History of Science. I switched the active one to History of Science through the switcher's own sign-in link (`/signin?action_handle_signin=true&authuser=1&pageid=<History of Science page id>`); the switcher then reported History of Science as selected, but the playlist page, reloaded once, still rendered as a viewer (Subscribe and Save playlist, no edit controls, no rows read).
- **State left behind:** the 9222 browser's youtube.com identity is now History of Science (it was Benjamin Oats). Nothing else was changed. Studio there is unaffected (it reached History of Science by `authuser=1` before).
- **Next, in order:** (1) reload `youtube.com/playlist?list=PLEbpfUzWzcXU` after the identity switch has settled and check `ytcfg DELEGATED_SESSION_ID` and the page's edit controls; (2) if it is editable, add `VbPubYd6Fbs`, then use each row's menu "Move to top" on X-rays, Atom, Periodic Table in that order and "Move to bottom" on the compilation `uAomPaOBrM8`, which gives the audit's order; (3) otherwise Studio Content, tick `VbPubYd6Fbs`, "Add to playlist", and set Details > Default video order.
