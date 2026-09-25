# Improvements backlog

Written 25 Sep 2026. None of this changes the four-week test in `FAMILIAR_DANGER_STRATEGY.md` (12 Oct – 6 Nov). Part 1 is channel housekeeping to do now. Part 2 waits until the test ends. Part 3 runs every week.

## 1. Do now (under an hour, no new videos)

| # | Job | Why | Done when |
|---|---|---|---|
| 1 | **Add an end screen and a pinned comment to the Jupiter long `-jmMROGoZCM` before it goes public on Sun 4 Oct 18:00.** End screen: the Last Star long `REXYxuLOBoI` plus Subscribe. Pinned comment: one question the film leaves open. | Its upload record (`020_…/11_Upload-Package/Schedule/jupiter_longform_upload_result.json`) says `end_screen: false` and `pinned_comment: false`. A viewer who finishes it gets sent nowhere. | Both visible in Studio |
| 2 | **Check every live long has an end screen,** and add one where it's missing. Point it at the best-performing long (Last Star) or the matching topic long. | Same gap as #1. Longs are the only place a viewer can be sent on from the channel. | A row per long in the fix log |
| 3 | **Rebuild the playlists around the topics that work.** Make one playlist, *What Space Would Do to You*, with Moon `2fsQcea-voM`, Last Star `REXYxuLOBoI`, Neutron Star `Yk1tLh23rko`, Europa `NbW5G1BpPY0`, Jupiter `-jmMROGoZCM` (from 4 Oct) and Andromeda `ojk-dfOpAmw`. Put it first on the channel home page. Keep the old playlists, but move them below it. | The five current playlists (Alien Life, JWST, Alien Worlds, Black Holes, Start Here) lead with the weakest topics. The home page is where a viewer lands from a Short. | Playlist live and first on the home page |
| 4 | **Upload the script as captions (SRT) on every long,** starting with Jupiter and Andromeda. | The exact words already exist. Auto-captions get science terms wrong, and clean captions help search. | Captions show as "English" (not auto-generated) in Studio |
| 5 | **Subscribe ask, every long from Sun 11 Oct.** One mid-film `[SUBSCRIBE BEAT]` (gate-checked), a 4-second lower-right cue, a hand-off last line, and the subscriber thank-you in the pinned comment, refreshed every Monday by `update-pinned-comment.ts`. | An end-of-film ask makes people leave before the end screen, and a small count in the film goes stale. The comment can be edited; the film can't. | Beat in the 11 Oct script; `PINNED_COMMENTS.json` has the Jupiter comment id |

## 2. After the test (from 9 Nov)

| # | Change | How to judge it |
|---|---|---|
| 6 | **Competition check before any long.** Search the exact planned title on YouTube, signed out. If all top five results are from channels with millions of subscribers, narrow the angle (for example *What Would You See on Io?* rather than *What's Inside Jupiter?*). Only make a long whose Short already cleared 200 views and 40% stayed. | Long impressions and search share after 28 days, against the current 13–170 lifetime impressions |
| 7 | **Test shorter Shorts, 13–18 seconds.** One fact, one clean loop. On today's 25-second Shorts, the average viewer leaves at 9–16 seconds. | Average % viewed and whether the graph ends above 100%, against that week's 22–27 s Shorts. Loop is scored as in the test plan. |
| 8 | **Keep the human visible.** Sources under every long (already a house rule), Ben's own voice (if the week-4 test holds), and original writing. | YouTube's Partner Programme needs 1,000 subscribers plus 4,000 watch hours or 10 million Shorts views in 90 days, and its reviewers look harder at mass-produced AI channels. |

## 3. Every week: public audit (automated)

A routine runs **every Monday at 07:47 UTC** (08:47 UK until the clocks go back on 25 Oct, 07:47 after) and does:

```
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py
```

It writes `audits/weekly/<date>/PUBLIC_SNAPSHOT.json` and `REPORT.md`, and puts them on main. The report covers:

- subscribers, Short views and long views, and the change since last week;
- every upload that is new since last week;
- frame 0 of each new Short, flagged for Orbit at frame 0 or a mostly dark frame 0;
- hashtags in titles, hedged claims, and duplicate titles across the whole channel.

It cannot see stayed-to-watch, CTR or a silent soundtrack; those stay Studio jobs. After each report, add stayed-to-watch at 48 h for each new Short to `could-orbit-survive/TEST_LOG.md`.

The first baseline is `audits/weekly/2026-09-25/`.
