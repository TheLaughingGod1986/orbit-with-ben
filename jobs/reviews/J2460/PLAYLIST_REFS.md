# J2460: what points at the six playlists (Orbit With Ben)

Read on 10 Nov 2026, about 03:25 UTC, by Claude Code on the Mini. **Read-only so far: nothing has been changed, repointed or removed in Studio.**

## How it was read

- Playlists, their videos, Home sections and every video description: YouTube Data API, read-only calls (`playlists.list`, `playlistItems.list`, `channelSections.list`, `videos.list`), signed in as `UC_esArsDKd3GJvOkeO0DUog` (Orbit With Ben).
- End screens and cards on public longs: the public watch page (`ytInitialPlayerResponse.endscreen` and `.cards`), the same method as `05_Analytics/live_fixes/2026-10-15.md`.
- Channel comments: `commentThreads.list` on all 91 public videos (39 threads in total), keeping any comment written by the channel that names a playlist.

## Still to read (step 1 is not finished)

- **End screens and cards on the five scheduled longs** (`c5AdqQsnnys` 15 Nov, `6bbbvfCx6zY` 22 Nov, `F-jImX5h7ws` 29 Nov, `G5uMANXHtNU` 2 Dec, `vP1BbqZ_dnM` 6 Dec). They are Private, so the public page cannot show them; they need the Studio editor (CDP 9223). Their descriptions were read and name no playlist.
- The Home tab as Studio's Customisation page shows it, to confirm the API's section list below.
- No playlist may be removed until both are read and the four references below are repointed and read back.

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
