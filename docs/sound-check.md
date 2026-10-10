# Sound check — 24 Sep 2026

Every live and scheduled Short and long on Orbit With Ben was opened and the soundtrack measured. A fail is a voice that is missing for the whole file: mute, a near-silent track, or Flow ambience standing in for the narrator. End holds and mid-film breaths were left alone.

YouTube cannot swap the file on an existing id. Each fail was replaced with a new upload that keeps the same title, description, and thumbnail. Public fails were made public. Nothing scheduled was date-moved. The broken id was set to private and was not deleted. Related stays on the same long. These four Moon Shorts point at `2fsQcea-voM` (*Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*).

The old ids are historical duplicates.

## Replaced

### Why Won't Perfect Total Eclipses Last Forever?

- Old id: `oFTYeBFtSQ4` (public 24 Sep 2026, now private)
- New id: `_WQLVnLETYA` (public)
- What was wrong: the whole ~25s soundtrack was digital silence (about −91 dB). The upload master had been built with the audio stripped, so YouTube stored an empty voice track. Captions and picture were intact. The Ben Orbit Narrator track from the rough punch was put back on that picture, in sync from the first frame. Thumbnail still reads LAST PERFECT COVER. Related remains `2fsQcea-voM`.

### How Do Fossils Prove Earth Spun Faster?

- Old id: `Y_SQGPd4Amc` (public 22 Sep 2026, now private)
- New id: `4P9v_2jx7Yo` (public)
- What was wrong: same entire-file silence (about −90 dB). The fossil upload master had no audio stream. Narrator restored from the rough punch, in sync. Thumbnail still reads FOSSIL CLOCK. Related remains `2fsQcea-voM`.

### What's Dragging the Moon Away From Earth?

- Old id: `Roh1QI2fTjs` (now private)
- New id: `i6KGk9Z3pIE` (public)
- What was wrong: same entire-file silence. Narrator restored from the rough punch, in sync. Related remains `2fsQcea-voM`.

### Why the Moon is Slowly Leaving Us

- Old id: `c_iLsiU5qTA` (now private)
- New id: `G8DiaNjD2WE` (public)
- What was wrong: same entire-file silence on the rings-of-fire Short. Title and description were copied as they were live (description still asks what a ring of fire eclipse is). Narrator restored from the rough punch, in sync. Related remains `2fsQcea-voM`.

Checked after upload: the four new soundtracks sit at speech level (mean about −19 to −22 dB). The four old ids are private.

## Passed — not changed

### Scheduled Shorts (publish time left as it was)

| Title | Id | When | Result |
|---|---|---|---|
| What happens if you touch a neutron star? #space #science #neutronstar | `pL339HhjDwo` | Wed 7 Oct 2026 11:30 UK | Pass. Narration present (mean −21.9 dB). Date not moved. |
| What Remains After the Last Star Dies | `Ih2zhZTbIR0` | Fri 2 Oct 2026 11:30 UK | Pass. Narration present (mean −23.7 dB). Date not moved. |
| Is Andromeda Coming to Destroy Us? | `P9Jiw-MwUEU` | 25 Sep 2026 | Pass |
| Will Andromeda Fill the Entire Sky? | `U5Baf_CjhKc` | 26 Sep 2026 | Pass |
| Will Earth Survive the Galaxy Crash? | `17zpT_u7XsY` | 27 Sep 2026 | Pass |
| What Happens When Andromeda Hits The Milky Way? | `xQlV9G9lqLI` | 28 Sep 2026 | Pass |
| How Long Until Andromeda Hits Us? | `e-7hzJv4c80` | 29 Sep 2026 | Pass |
| Our Galaxy's Final Destination | `k9pXeeJvLpc` | 30 Sep 2026 | Pass |
| What Happens When Galaxies Actually Collide? | `CtllH6VOhEI` | 1 Oct 2026 | Pass |

### Scheduled long

| Title | Id | Result |
|---|---|---|
| Everything you need to know about the Andromeda crash | `ojk-dfOpAmw` | Pass. Premiere playback has narration (mean −28.1 dB on the owner preview). Not replaced. |

### Other live videos

These already had a real narrator track. They were not re-uploaded.

Moon Shorts that already had voice: `rFzqmi8RWCY` Why Does the Moon Drift 3.8 cm a Year? · `eSFhBf2rcZk` Is the Moon Leaving Us? · `cmeBDZLzPHs` Why Were Earth's Days Only Hours Long?

Live longs, all pass: `2fsQcea-voM` Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone · `Yk1tLh23rko` What Happens If You Get Near a Neutron Star · `NbW5G1BpPY0` Could Life Exist Under The Ice Of Europa? · `REXYxuLOBoI` What Happens When the Last Star Dies? · `ziKBPJ6FY0U` JWST Found Galaxies That Shouldn't Exist Yet · `b8-X_FyJnHM` Alien Worlds: The Strangest Planets We've Ever Found · `3xrxdmaOwJI` What Happens If You Fall Into a Black Hole? · `Mo93x0fxB1Q` Why Haven't We Found Aliens Yet? The Fermi Paradox Explained.

Every other live Short in the public catalogue passed the same listen (speech present, not a silent file), including the Neutron, Europa, Last Star, JWST, Fermi, Black Hole, and Alien Worlds clusters. None of those ids were replaced.

## 10 Oct follow-up: three silent Moon Shorts made Private

Chief's 10 Oct audio sweep (yt-dlp public streams + local exports) found three public Moon Shorts that are digital silence for the whole file (−70 LUFS, −91 dB max, on two YouTube audio formats). The 24 Sep listen above missed them. Ben OK'd the fix on 10 Oct 21:10 ("Any that the sound is broken can we fix"), relayed by Chief as job J0121. Each one already had an audible copy public since 21 Sep, so they were made Private with no re-upload. Nothing was deleted.

| Silent Short (now Private) | Audible copy (public) |
|---|---|
| `osRFF1cBCEw` Why Does the Moon Drift 3.8 cm a Year? (347 views) | `rFzqmi8RWCY` The Moon Gets 3.8 cm Farther Away Every Year (−16.2 LUFS) |
| `MYPIEBBs7B8` What If the Moon Just Left? (262 views) | `eSFhBf2rcZk` Is the Moon Leaving Us? (−16.8 LUFS) |
| `2qTvliJQuqI` Why Were Earth's Days Only Hours Long? (173 views) | `cmeBDZLzPHs` A Day on Young Earth Lasted Just a Few Hours (−16.5 LUFS) |

Done by Cursor on 10 Oct 2026 22:48Z with `07_Content-Ops/scripts/set-private.ts` (status-only change; title, kids flag, embed and licence kept). API before/after: `00_Brand/Channel-Setup/audits/moon_silent_private_2026-10-10.json`. Studio showed all three as Private on Orbit With Ben after a reload.
