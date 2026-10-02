# Title and thumbnail audit: every OWB long and Short (2 Oct 2026)

Ben's order (2 Oct, 14:27): *"do a full audit of titles, and thumbnails to check they are all correct"*.

**How this was built:** titles come from the 30 Sep public snapshot plus the Chief's 2 Oct Studio schedule, and the older Shorts from the 25 Sep audit. Thumbnail text comes from the 26 Sep swap log, the Short-cover manifests (`yellow_white_v04`, `melodysheep_v01` A), the 25 Sep refresh and the Saturn package.

**Chief:** fill the *Studio says* column from Studio (title + thumbnail text) and mark ✅ or ❌. Where it says **read from Studio**, the repo has no record, so note what Studio shows. Fixes are agreed on the thread. **Title changes on public videos are renames, so they need Ben's OK** (`AGENTS.md`). Thumbnail swaps on the back catalogue go in one batch for Ben's OK.

## Already known problems (fix list for Ben)

| Video | Problem | Proposed fix |
|---|---|---|
| `9lLZMy8rBJo` / `xRxhb3vSru4` | Same title: *What Remains After the Last Star Dies?* | Retitle the lower-view copy (`xRxhb3vSru4`, 412) to *What's Left When the Last Star Goes Out?* |
| `rFzqmi8RWCY` / `osRFF1cBCEw` | Same title: *Why Does the Moon Drift 3.8 cm a Year?* | Retitle `rFzqmi8RWCY` (253) to *The Moon Moves 3.8 cm Further Every Year* |
| `cmeBDZLzPHs` / `2qTvliJQuqI` | Same title: *Why Were Earth's Days Only Hours Long?* | Retitle `cmeBDZLzPHs` (103) to *Earth Once Had 5-Hour Days* (check the figure against its script first) |
| `MYPIEBBs7B8` | Hashtags + hedge: *What if the Moon just left? #space #whatif #astronomy* | *What Happens If the Moon Leaves?* |
| `68uTDP2esso` | Hashtags: *…hiding a massive secret #space #JWST #discovery* | *The Early Universe Is Hiding a Massive Secret* |
| `pII09FbRYGc` | Trailing full stop: *Why Europa Is Hiding a Massive Ocean.* | Drop the full stop |
| `ykmoxRJ6BOI` | Hedged: *We May Have Already Recorded Alien Life* | Check it against its script; if the claim is about the Wow! signal, *The Signal We Never Heard Again* |
| `-jmMROGoZCM` (Jupiter long) | Title conflict between the records; description says "if you fall" | **Resolved:** Studio title is *Why You Can't Stand On Jupiter*; the pin matches. Still to do: "fall" → "fell" in the description (not a rename) |
| `DN4L1DkerMM`, `l1d1ypHxLk0` | Thumbnails flagged NEEDS PLATE on 25 Sep (burned-in captions) | Build plates from the NASA pools or the masters, then batch them for Ben |
| `55AEQwvs36g` (Saturn long) | Title ABC includes the Monday Short's title | Remove it from the test |

## Applied (3 Oct 00:07 London)

10 titles are live (5 clean-ups on 2 Oct, then 3 duplicate retitles, the Alien Life rename and the Monday Moon Short on 3 Oct). Ben OK'd the two NEEDS PLATE covers on 2 Oct; the Mini rebuilds them in Arial Black and swaps them. `rFzqmi8RWCY` still shows Orbit on its cover: try a clean Studio frame first, else the NASA plate job in `tools/build_nasa_plate_short_covers.py` (needs Ben's OK).

## Every video

| Kind | State | ID | Title (record) | Views 30 Sep | Intended thumbnail text | Flags | Studio says |
|---|---|---|---|---:|---|---|---|
| long | scheduled Sun 11 Oct 18:00 | `55AEQwvs36g` | How Long Do Saturn's Rings Have Left? | — | ALREADY FALLING |  · title ABC still lists the Monday Short's title, to remove (comment 5948133381) | |
| long | scheduled Sun 4 Oct 18:00 | `-jmMROGoZCM` | Why You Can't Stand On Jupiter | — | NO FLOOR (swapped 26 Sep) |  · title conflict: REFRESH_LOG 28 Sep set **Why You Can't Stand On Jupiter** (vidIQ); Chief reports **Why You Can't Stand On Jupiter**. PINNED_COMMENTS uses the first. Description line 1 says "if you **fall**" (should be "fell"). | ✅ Studio title *Why You Can't Stand On Jupiter* (Chief, 2 Oct 15:50); pin fits it. Description "fall"→"fell" to do |
| long | public | `b8-X_FyJnHM` | Alien Worlds: The Strangest Planets We've Ever Found | 13 | A GIANT EYE? (25 Sep audit) |  | |
| long | public | `NbW5G1BpPY0` | Could Life Exist Under The Ice Of Europa? | 15 | A HIDDEN OCEAN (swapped 26 Sep) |  | |
| long | public | `ziKBPJ6FY0U` | JWST Found Galaxies That Shouldn't Exist Yet | 29 | TOO EARLY? (25 Sep audit) |  | |
| long | public | `3xrxdmaOwJI` | What Happens If You Fall Into a Black Hole? | 4 | NO WAY OUT (swapped 26 Sep) |  | |
| long | public | `Yk1tLh23rko` | What Happens If You Get Near a Neutron Star | 15 | CRUSHED FLAT (swapped 26 Sep) |  | |
| long | public | `ojk-dfOpAmw` | What Happens When Andromeda Hits the Milky Way? | 3 | WHEN THEY MEET (swapped 26 Sep) |  · 25 Sep record said 'retitle pending'; check the live title | |
| long | public | `REXYxuLOBoI` | What Happens When the Last Star Dies? | 41 | LAST LIGHT (swapped 26 Sep) |  | |
| long | public | `Mo93x0fxB1Q` | Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | 12 | SILENCE (swapped 26 Sep) |  | |
| long | public | `2fsQcea-voM` | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone | 4 | LEAVING US? (25 Sep audit) |  | |
| short | scheduled Wed 14 Oct | `buaOI3QGm7U` | Could a Robot Survive Falling Into Jupiter? | — | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | scheduled Wed 7 Oct | `pL339HhjDwo` | This Star Is 20 km Wide and Heavier Than the Sun | — | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | scheduled Mon 5 Oct | `dQlOgsDGmtA` | Did You Know the Moon Is Leaving? | — | **read from Studio** |  | ✅ retitled 3 Oct 00:07 London (was *Why the Moon Is Leaving Us*) |
| short | public (older) | `iQUbmlaj4vk` | A Reply From the Stars Takes Generations | 17 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `f8V6wCjWwHA` | Billions of Planets, Zero Signals | 16 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `ZnsJTCcrTlA` | Black Holes Grew Too Big, Too Fast | 22 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `to-b2baeoWQ` | Could a Probe Get Closer to a Neutron Star? | 67 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `VE0f186WQZo` | Europa Sprays Its Ocean Into Space | 91 | AN OCEAN / IN SPACE |  | |
| short | public | `4P9v_2jx7Yo` | How Do Fossils Prove Earth Spun Faster? | 3 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `vCxXTYXSSqY` | How Heavy Is a Teaspoon of Neutron Star? | 30 | A TEASPOON / OF MOUNTAINS |  | |
| short | public | `Xza_jSHD4qw` | How Life Could Feed Under Europa With No Sun | 95 | LIFE WITHOUT / SUNLIGHT |  | |
| short | public | `e-7hzJv4c80` | How Long Until Andromeda Hits Us? | 38 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `TE_HDKAnqms` | If Life Starts Under Ice, It's Everywhere | 2 | LIFE UNDER / ICE |  | |
| short | public | `P9Jiw-MwUEU` | Is Andromeda Coming to Destroy Us? | 87 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `eSFhBf2rcZk` | Is the Moon Leaving Us? | 291 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `4-ZEpKD1yak` | Is the Universe Older Than We Thought? | 75 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `GjcZB8826J8` | It Rains Glass Sideways on This Alien World | 9 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `PV50PX-bE4g` | Most of the Universe Gives Off No Light | 127 | NO LIGHT (swapped 26 Sep) |  | |
| short | public | `BX-z1EkgANg` | One Second Near a Neutron Star Is Enough | 20 | ONE SECOND / IS ENOUGH |  | |
| short | public 2 Oct | `k9pXeeJvLpc` | Our Galaxy's Final Destination | — | **read from Studio** |  | ✅ retitled 2 Oct 16:57 London (was *Our Galaxy's Final Destination #cosmos #astronomy #space*) |
| short | public | `n2WbOfJhOwc` | Star Recycling Isn't Perfect | 213 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `IVbO9XkkDps` | The Day the Last Star Goes Out | 93 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `68uTDP2esso` | The Early Universe Is Hiding a Massive Secret | 53 | A HIDDEN SECRET (swapped 26 Sep) | hashtag in title | ✅ retitled 2 Oct 16:57 London (was *The Early Universe Is Hiding a Massive Secret*) |
| short | public | `wIh3armF7_k` | The Last Star Will Be a Red Dwarf | 55 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public 2 Oct | `Ih2zhZTbIR0` | The Last Stars Will Shine for 10 Trillion Years | — | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `CkSECfUfH2Y` | The Sky Is Already Running Out of Light | 292 | SKY GOING DARK (swapped 26 Sep) |  | |
| short | public | `va5ATScn3rs` | The Sky Would Lean Near a Neutron Star | 19 | THE SKY / WOULD LEAN |  | |
| short | public | `DN4L1DkerMM` | The Universe Is Running Out of New Stars | 229 | RUNNING OUT OF / STARS | thumbnail NEEDS PLATE | |
| short | public | `QNTeou-w-gY` | There's an Ocean Under That Ice | 65 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `l1d1ypHxLk0` | These Galaxies Appeared Too Early | 95 | TOO / EARLY | thumbnail NEEDS PLATE | |
| short | public (older) | `tEOHYQbcgOw` | This Planet's Night Never Cools Down | 16 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `SC2WGTl_V5Q` | This Planet's Rain Is Molten Glass | 25 | GLASS RAIN (swapped 26 Sep) |  | |
| short | public | `keXe1GNxWSU` | Those Ice Scars Are How You Find It | 206 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `MDvAKtmKauw` | Three Suns in the Sky — Real Alien Worlds | 147 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `eVp9a7f4rWg` | We Could Kill the Life We're Looking For | 93 | COULD WE / KILL IT? |  | |
| short | public (older) | `QRi6Dxq0hz0` | We Could Smell Alien Life in a Spectrum | 32 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `M-VN84HCNls` | We Found Planets Made of Diamond | 64 | DIAMOND PLANETS (swapped 26 Sep) |  | |
| short | public (older) | `ykmoxRJ6BOI` | Is Alien Life Already Hiding in Our Data? | 10 | **read from Studio** | hedged | ✅ retitled 3 Oct 00:07 London (was *We May Have Already Recorded Alien Life*) |
| short | public | `Rp_8J6_6IIk` | What Happens If You Touch a Neutron Star? | 62 | CRUSHES YOU / TOO FAST |  | |
| short | public | `KX-XU_AODoI` | What Happens When the Last Star Furnace Goes Cold | 75 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `MYPIEBBs7B8` | What If the Moon Just Left? | 262 | **read from Studio** | hashtag in title; hedged | ✅ retitled 2 Oct 16:57 London (was *What if the Moon just left? #space #whatif #astronomy*) |
| short | public (older) | `03v4f1hlvtQ` | What If They're Leaving Us Alone On Purpose | 55 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `P32uaiserG0` | What JWST's Infrared Eyes Can See | 39 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `9lLZMy8rBJo` | What Remains After the Last Star Dies? | 622 | WHAT REMAINS? (swapped 26 Sep) | DUPLICATE TITLE | |
| short | public | `xRxhb3vSru4` | What's Left When the Last Star Goes Out? | 412 | **read from Studio** | DUPLICATE TITLE | ✅ retitled 3 Oct 00:07 London (was *What Remains After the Last Star Dies?*); cover clean (no Orbit) |
| short | public | `1glQuYFSaYQ` | What Would Life Eat Under Europa? | 127 | WHAT WOULD / LIFE EAT? |  | |
| short | public | `i6KGk9Z3pIE` | What's Dragging the Moon Away From Earth? | 15 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `rFzqmi8RWCY` | The Moon Gets 3.8 cm Farther Away Every Year | 253 | **read from Studio** | DUPLICATE TITLE | ✅ retitled 3 Oct 00:07 London (was *Why Does the Moon Drift 3.8 cm a Year?*); cover **still shows Orbit**: new cover pending |
| short | public | `osRFF1cBCEw` | Why Does the Moon Drift 3.8 cm a Year? | 347 | **read from Studio** | DUPLICATE TITLE | ✅ title unchanged (higher-view copy kept); cover clean (no Orbit) |
| short | public | `pII09FbRYGc` | Why Europa Is Hiding a Massive Ocean | 291 | **read from Studio** | trailing full stop | ✅ retitled 2 Oct 16:57 London (was *Why Europa Is Hiding a Massive Ocean.*) |
| short | public | `8Bym-yrYhGc` | Why Europa's Ocean Shouldn't Exist | 26 | THIS OCEAN / SHOULDN'T EXIST |  | |
| short | public | `P-li_ZWk4lg` | Why JWST Pictures Don't Match the Textbook | 82 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `xQlV9G9lqLI` | Why Stars Don't Crash When Galaxies Meet | 250 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `G8DiaNjD2WE` | Why the Moon Is Slowly Leaving Us | 6 | **read from Studio** |  | ✅ retitled 2 Oct 16:57 London (was *Why the Moon is Slowly Leaving Us*) |
| short | public | `SdNXS1PD_Yk` | Why the Night Sky Is Getting Darker | 254 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public (older) | `OlwENQcY-jg` | Why This Alien World Looks Like a Giant Eye | 69 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `cmeBDZLzPHs` | A Day on Young Earth Lasted Just a Few Hours | 103 | **read from Studio** | DUPLICATE TITLE | ✅ retitled 3 Oct 00:07 London (was *Why Were Earth's Days Only Hours Long?*); cover clean (no Orbit) |
| short | public | `2qTvliJQuqI` | Why Were Earth's Days Only Hours Long? | 173 | **read from Studio** | DUPLICATE TITLE | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `_WQLVnLETYA` | Why Won't Perfect Total Eclipses Last Forever? | 23 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `_8L9jYbDVmQ` | Why You Can't Stand on a Neutron Star | 419 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `U5Baf_CjhKc` | Will Andromeda Fill the Entire Sky? | 54 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `17zpT_u7XsY` | Will Earth Survive the Galaxy Crash? | 31 | **read from Studio** |  | ✅ thumbnail matches topic (Chief, 2 Oct 15:50) |
| short | public | `fhJP6eMoU0Q` | Your Atoms Near a Neutron Star Do Not Survive | 51 | TEARS YOU / INTO ATOMS |  | |
| short | public | `o7ykyTDZKiE` | Your Last Clear Image Near a Neutron Star | 47 | LAST CLEAR / IMAGE |  | |

Rules checked: no duplicate titles; no hashtags or hedges in titles; no Orbit on any thumbnail; thumbnail text never repeats the title; a Short never shares its long's title.