# Scheduled Shorts cover fixes — 28 October 2026

J1111 · Codex specialist worker · GBP0 · **Orbit evidence from J1111; HOS completion recorded below**.

## Orbit: 22 scheduled Shorts read back; 12 cover fixes

All 12 changed covers were saved, reloaded in video details, then independently fetched from the refreshed Studio Shorts list. Ten existing hook covers were retained. The live list revealed replacement IDs absent from the morning snapshot: `aAUgIGEuPwQ`, `xvarZP2aYyE`, `v6euXX2omz4`. No title, visibility, schedule, video file, related link or audience controls were changed. Chief owns the review/PASS.

| Air date (Studio) | Video | Old → new cover | Outcome | Saved UTC |
|---|---|---|---|---|
| 29 Oct 2026 | `_a66uhRDips` — Why Is Venus Hot Enough to Melt Lead? | NEARLY 1 KM DEEP → VENUS MELTS LEAD | Saved; list image read back | 16:38:53 |
| 30 Oct 2026 | `6dcL5rBmHPM` — How Thin Are Saturn's Rings? | small long-title banner / SIT → SATURN’S RINGS / 10 METRES THICK | Saved; list image read back | 16:38:53 |
| 31 Oct 2026 | `VfDm3E2bUgU` — Why Do Astronauts See 16 Sunrises a Day? | EVERY 90 MINUTES, small caption → DAWN EACH / 90 MINUTES | Saved; list image read back | 16:35:47 |
| 2 Nov 2026 | `hZH0C7fpCk4` — How Big Is Venus Compared to Earth? | small long-title banner / TIME → 95% AS WIDE | Saved; list image read back | 16:36:09 |
| 3 Nov 2026 | `ZpEA8stoSPA` — Why Does Uranus Have 21-Year Winters? | Existing complete hook retained | Unchanged; list image read back | — |
| 7 Nov 2026 | `T9fVlG3CCzU` — What Are Shooting Stars Really Made Of? | Existing complete hook retained | Unchanged; list image read back | — |
| 9 Nov 2026 | `iyvWYFP_ETA` — Could a Robot Survive a Night on Mars? | Existing complete hook retained | Unchanged; list image read back | — |
| 10 Nov 2026 | `RLSJm59OSzI` — What Would Standing on Saturn's Moon Titan Feel Like? | Existing complete hook retained | Unchanged; list image read back | — |
| 11 Nov 2026 | `TtgHNLXfDSs` — Why Did a 90-Day Mars Rover Last 14 Years? | Existing complete hook retained | Unchanged; list image read back | — |
| 12 Nov 2026 | `N42gKBbD7tE` — How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years? | small rover caption → SAVED BY WIND | Saved; list image read back | 16:39:05 |
| 13 Nov 2026 | `bSjWiCbB7pY` — How Did a Helicopter Fly 72 Times on Mars? | Existing complete hook retained | Unchanged; list image read back | — |
| 14 Nov 2026 | `gmzaCfJF1gA` — Why Does Pluto's Giant Ice Heart Have Zero Craters? | Existing complete hook retained | Unchanged; list image read back | — |
| 16 Nov 2026 | `HZGTovJu_TQ` — If You Can't See the Nearest Star, How Far Away Is It? | small long-title banner → TOO FAINT | Saved; list image read back | 16:36:30 |
| 17 Nov 2026 | `kKN8Ale42sE` — How Far From Earth Is Voyager 1 Right Now? | Existing complete hook retained | Unchanged; list image read back | — |
| 18 Nov 2026 | `cwU_0WWeNZ4` — If Voyager Needs 75,000 Years, How Far Is the Nearest Star? | small long-title banner → 75,000 YEARS | Saved; list image read back | 16:36:51 |
| 20 Nov 2026 | `aAUgIGEuPwQ` — The Nearest Star Is a Cherry Past Cairo. How Do We Know? | small long-title banner → SUN TO A GRAPEFRUIT? | Saved; list image read back | 16:37:13 |
| 23 Nov 2026 | `emwQsPxnRGM` — Why Do You Weigh Less at Earth's Equator? | small long-title banner → 0.5% LIGHTER AT EQUATOR | Saved; list image read back | 16:37:35 |
| 30 Nov 2026 | `xvarZP2aYyE` — Why Will Gliese 710's Comets Arrive After It Has Gone? | Existing complete hook retained | Unchanged; list image read back | — |
| 2 Dec 2026 | `v6euXX2omz4` — Is a Star Really Coming Towards Us? | Existing complete hook retained | Unchanged; list image read back | — |
| 4 Dec 2026 | `jJ5LkFGyzLI` — How Close Will Gliese 710 Come to the Sun? | small long-title banner → HOW CLOSE TO THE SUN? | Saved; list image read back | 16:37:56 |
| 7 Dec 2026 | `X768qs8sNQs` — What Will the Night Sky Look Like When Gliese 710 Arrives? | small long-title banner → 3X BRIGHTER THAN SIRIUS | Saved; list image read back | 16:38:18 |
| 16 Dec 2026 | `f17XCtUmN-g` — What Happens When Gliese 710 Passes Through the Oort Cloud? | small long-title banner → MONTHS OF SUNLIGHT | Saved; list image read back | 16:38:39 |

Evidence outside git (images are not committed):
- Before/after Studio images, full screenshots and contact sheets: `/Users/benjaminoats/_desk/J1111/evidence`.
- Final contact sheet: `/Users/benjaminoats/_desk/J1111/evidence/owb-list-after-sheet.jpg`.
- Machine-readable before/after URLs and timestamps accompany this report as JSON.

The first quick three-image batch returned Save but did not persist. Those attempts are not counted; slower retries waited for the upload before Save and passed the subsequent persistence read-back. The Venus fix ran first. All three Orbit Shorts airing before Sunday 1 November now show their hook covers.

The missing approved Mars length-test cover was restored by running its unchanged `_build_cover_thu12_v01.py` with output redirected to the desk and its original NAS `025_MarsRobot_full_rough_v03f.mp4` master. No new design or film render was made.

## HOS: earlier J1111 access attempt (superseded by J1113 below)

Port 9222 refused connection. The existing `~/.hos-chrome-youtube-studio` profile opened in its existing browser session and exposed no requested CDP 9224 endpoint. The Orbit account explicitly returned “Oops, you don’t have permission to view this page” for the exact HOS channel ID `UCXp7HkBIl1LgaznXuZHJyRg`. No HOS metadata or cover was changed. Screenshot: `/Users/benjaminoats/_desk/J1111/evidence/hos-session.png`.

**Chief next:** provide/restore the logged-in HOS Studio session for the worker, then inventory its scheduled Shorts live and fix/read back their hook covers. The tracker candidates below are from the 28 October snapshot, not a live Studio verification. The 30/31 October deadlines are urgent.

| Snapshot air time UTC | Candidate | Title |
|---|---|---|
| 2026-10-30T11:30:00Z | `Rl2uZ-KOTl8` | Your Heart Pumps More Blood Than You Have |
| 2026-10-31T11:30:00Z | `BW_CFAX-mxc` | Is the Heart a Pump? |
| 2026-11-01T11:30:00Z | `pWySvZsneZg` | Why Gold Foil Bounced Rutherford's Particles Back |
| 2026-11-03T11:30:00Z | `qW2OsD4mujc` | The Four Elements Were Wrong |
| 2026-11-05T11:30:00Z | `xHnIi9GqOsM` | Why Do Veins Have Valves? |
| 2026-11-08T11:30:00Z | `PFj6172YU4Q` | One Tight Band Proved Your Blood Goes Round |
| 2026-11-13T11:30:00Z | `-I_GHK-GcFs` | What Was the Edward Jenner Experiment? |
| 2026-11-15T11:30:00Z | `x_3L_IdYgEc` | The Blood Vessels Finer Than a Hair |
| 2026-11-16T11:30:00Z | `-sa2t7dAtCk` | What Is Dalton's Atomic Theory? |
| 2026-11-17T11:30:00Z | `4WUs0beKn0A` | Why Is It Called a Vaccine? |

## Relay to weekly audits J1106 / J1107

Every new Short upload must explicitly set the frame-0 hook cover, wait for thumbnail upload completion before Save, reload the details, and read back the Studio list image. Successful upload/Save alone is not proof. This is an operational reminder for the existing rule, not a rule change.

## Resource note

Disk headroom check was below 20 GB. `nas_offload.py --apply --json` found no eligible scratch folders and moved/deleted nothing (NAS mounted; about 16.9 GB free). No subscriptions or credits were spent.

## HOS completion — J1113, 28 October 2026

All **10 scheduled HOS Shorts** now show their pack hook or archived frame-zero hook. Changes ran earliest air first; the 30/31 October covers were fixed first. Every cover was saved, reloaded in video details, then fetched again from the refreshed Studio Shorts list. The list row text is identical before/after for all 10 (titles, dates and Scheduled status retained). All 10 details pages read back not Made for Kids after saving. Chief review/PASS remains outstanding.

The existing authenticated `~/.hos-chrome-youtube-studio` Chrome process already exposed **CDP 9460**, with the exact HOS channel `UCXp7HkBIl1LgaznXuZHJyRg`. Direct CDP worked; Playwright connection stalled and its probe was stopped. Used the existing endpoint rather than restarting its live Studio/Flow tabs to change the port to 9222. No password or 2FA was required. Orbit 9223 was untouched.

| Air date | Video | Previous cover | New hook | Saved UTC |
|---|---|---|---|---|
| 30 Oct 2026 | `Rl2uZ-KOTl8` | small title/caption on anatomical figure | MORE THAN YOU HAVE | 2026-10-28T17:04:35.691658+00:00 |
| 31 Oct 2026 | `BW_CFAX-mxc` | small title/caption on anatomical figure | IS THE HEART A PUMP? | 2026-10-28T17:04:55.559539+00:00 |
| 1 Nov 2026 | `pWySvZsneZg` | mid-film white foil | GOLD THREW IT BACK | 2026-10-28T17:05:15.443919+00:00 |
| 3 Nov 2026 | `qW2OsD4mujc` | small title on laboratory scene | FOUR ELEMENTS WERE WRONG | 2026-10-28T17:07:12.136014+00:00 |
| 5 Nov 2026 | `xHnIi9GqOsM` | small title/caption on vein scene | DOORS IN VEINS | 2026-10-28T17:05:38.552047+00:00 |
| 8 Nov 2026 | `PFj6172YU4Q` | small title/caption on arm | ONE TIGHT BAND | 2026-10-28T17:05:58.830020+00:00 |
| 13 Nov 2026 | `-I_GHK-GcFs` | small title/caption on bed scene | THE FIRST TEST | 2026-10-28T17:06:18.550509+00:00 |
| 15 Nov 2026 | `x_3L_IdYgEc` | older FINER THAN A HAIR hook | HE NEVER SAW THIS | 2026-10-28T17:07:35.055764+00:00 |
| 16 Nov 2026 | `-sa2t7dAtCk` | older WEIGH ATOM hook | EACH ATOM | 2026-10-28T17:07:57.856888+00:00 |
| 17 Nov 2026 | `4WUs0beKn0A` | cow plate without hook | NOT THE FIRST | 2026-10-28T17:06:38.270016+00:00 |

Only the image-only thumbnail input and Save were used. No title, privacy, schedule, video file, Related, or audience control was changed. GBP0; no credit spent. One slow page was retried; only successful reloaded saves are counted.

Evidence outside git: `/Users/benjaminoats/_desk/J1113/evidence` (before/after images, `before-sheet.jpg`, `after-sheet.jpg`, and archived frame-zero comparisons). JSON read-back, change record and sha256 manifest accompany this report.

Disk: 14.6 GB free; required `nas_offload.py --apply` found no eligible old scratch and moved nothing.

**Chief next:** review the 10-cover after sheet and recorded read-back, then decide PASS. Worker gives no final OK.
