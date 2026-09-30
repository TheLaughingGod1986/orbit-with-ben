# Full audit: channel, Buffer and workflow (30 Sep 2026)

Sources: the public channel pages today (`../weekly/2026-09-30/`, compared with 25 Sep), the Buffer record and code on main, Buffer's own stats as Cursor read them on 28–30 Sep, the Mac's 07:05 log (29 Sep), the routines on this account, and the repo. There's no new Studio read, so no stayed-to-watch numbers.

## Verdict

**The system works. Don't rebuild anything.** Everything scheduled went out on time: the 28 Sep Short, and today's Andromeda Short on all three platforms at 11:30 with its hook, question and film link. The gaps are small, and most are fixed below.

On the channel, the 24 Sep audit still holds. **Growth comes from each new Short's first day, and old videos barely move.** Like for like, the Shorts gained 486 views in five days, and no older Short gained more than 10. Subscribers went from 8 to 11.

## 1. YouTube channel

| | 25 Sep | 30 Sep |
|---|---:|---:|
| Subscribers | 8 | 11 |
| Views, newest 48 Shorts (like for like) | | +486 |
| Views, 9 longs | 133 | 136 |
| Median Short (newest 48) | | 78.5 |

- **The five new Andromeda Shorts are below the channel's median:** 31, 54, 87 and 250 views, plus today's at 38 after a few hours. The Moon Shorts had 173–347 views. Seven Shorts on one topic on consecutive days split one test seven ways, which is the 24 Sep audit's point 2c.
- **The Andromeda long was retitled** to *What Happens When Andromeda Hits the Milky Way?* (24 Sep audit, fix 1). It has 3 views after six days, which is normal for a long here.
- **Old Shorts don't grow.** The biggest gain on any older Short this week was +10. Every Short gets one day-one test, so the first two seconds are what matter.

**Needs Ben (these rename or hide videos, so each needs his OK):**

1. **Three pairs of public Shorts share a title** (weekly flag):
   - *Why Were Earth's Days Only Hours Long?*: `cmeBDZLzPHs` (103 views) and `2qTvliJQuqI` (173)
   - *Why Does the Moon Drift 3.8 cm a Year?*: `rFzqmi8RWCY` (253) and `osRFF1cBCEw` (347)
   - *What Remains After the Last Star Dies?*: `9lLZMy8rBJo` (622) and `xRxhb3vSru4` (412)

   Watch each pair. If both are the same cut, make the lower-view one private; never delete. Duplicate uploads count as reused content when the channel applies for the Partner Programme. If they're different cuts, retitle the lower one for what it shows.
2. **Titles against the house rules:**
   - `MYPIEBBs7B8` *What if the Moon just left? #space #whatif #astronomy* → *What Happens If the Moon Just Left?*
   - `68uTDP2esso` *The early universe is hiding a massive secret #space #JWST #discovery* → *The Early Universe Is Hiding a Massive Secret*
   - `eVp9a7f4rWg` *We Could Kill the Life We're Looking For*: a hedged claim. Retitle for what it shows after watching it.

   Use `retitle-videos.ts` with a dry run first.
3. **Jupiter long `-jmMROGoZCM` (Sun 4 Oct 18:00): the end screen and pinned comment are still not done** (backlog #1; its upload record says `end_screen: false`). Set the end screen in Studio before Sunday: Last Star `REXYxuLOBoI` plus Subscribe. Post the pinned comment right after 18:00 with `update-pinned-comment.ts --create --video -jmMROGoZCM`, then pin it in Studio. Its question in `PINNED_COMMENTS.json` no longer says "58 minutes", because the 14 Oct Robot Short asks "Guess how long it lasted?" and that would give the answer away.
4. **Record stayed-to-watch at 48 h for the Andromeda Shorts** from Studio. The 24 Sep audit set today as the re-measure, and `TEST_LOG.md` has no rows before 12 Oct.

## 2. Buffer

**Working:**
- Posts go out at the YouTube go-public time.
- The daily check ran cleanly on 29 Sep.
- Every queued media file answered 200.
- After today, 5 posts are queued per channel. The free plan allows 10.

**Baseline to beat** (Buffer stats, 151 posts, 2 Aug–28 Sep): Facebook Reels 72 impressions, Instagram Reels 12.5 reach, Threads 5–15 views, **0 comments on every post.** The hooks, questions and film links started today. **Judge them on 14 Oct:** comments, and reach against this baseline.

**Found and fixed in this audit:**

| Problem | Fix |
|---|---|
| A video that goes public without a schedule, or after the 07:05 check has already run, was never mirrored. The check only looked at scheduled uploads. | The check now also looks at uploads that went public in the last 24 h. Any that `UPLOADS.json` knows are shared now. Anything else is listed for a person, so an old video made public again never reaches social. |
| Facebook first comments are refused on the free plan. | Fixed on 29 Sep (`b4d945b`): the link goes in the text. |
| The daily check was using up Buffer's request limit. | Fixed on 29 Sep: it only asks about posts that are already due. |

**Not worth changing yet:**
- Buffer's paid plan. It would only add first comments and a bigger queue, and neither is needed.
- Threads Shorts as images instead of video. Only 5 image posts so far, which is too few to go on.

## 3. Workflow (GitHub and the Mac)

| Problem | Fix |
|---|---|
| **No CI.** Cursor and cloud sessions merge to main many times a day, and nothing ran the tests. | Added `.github/workflows/content-ops.yml`, which runs typecheck, lint and tests on every push and PR that touches `07_Content-Ops/`. |
| **The Mac ran whatever code it last pulled.** Every fix this week needed a "pull on the Mac" prompt. | Added `launchd/buffer-check.sh`. It pulls main before the 07:05 check, but only when that checkout is on main with no local code changes. |
| **The Buffer record drifted.** The Mac changed `BUFFER_POSTS.json`, and nobody committed it. | The same script commits and pushes `social/` to main after each check. |
| **Failures were silent.** A failed 07:05 run only wrote to a log. | The script shows a Mac notification when the check fails. |
| **The weekly report counted older Shorts as new.** Shorts coming back into the newest-48 list counted as growth: +1,449 instead of the real +486. | `weekly_public_audit.py` now counts a Short as new only if it's above last week's newest, and compares views like for like. |
| **The 28 Sep weekly routine ran but left no report on main,** and no `weekly-audit-*` branch. | This audit's run is on main as `weekly/2026-09-30/`. Open the routine's 28 Sep session ("Orbit weekly public audit") in the Claude app to see why it didn't push. Google also blocked some watch-page reads from cloud IPs today, so a blocked fetch is the likely cause. |
| **46 September branches** are still on GitHub; 11 have work that isn't on main, and all 11 are superseded. | Not changed. List them with `git branch -r`. Delete them once Ben says so, the same way as the August ones. |

**Recommended next (not built):**
- **Add the YouTube Analytics read scope (`yt-analytics.readonly`)** so the weekly report can pull each Short's average % viewed and average view duration at 48 h, instead of relying on someone reading Studio. Stayed-to-watch itself is Studio-only, so this is a supplement. It needs one re-run of `youtube:auth`.
- **Thumbnails through the API** are refused on the new Cloud project (`thumbnails.set` forbidden). Studio is the fallback, and the step is in the playbook. The likely fix is Google's app verification for the project. Leave it unless it becomes a burden.

## 4. After this merges (Mac, once)

Reinstall the LaunchAgent so it uses the new script:

```bash
cd ~/YouTube/orbit-with-ben && git pull origin main
launchctl bootout gui/$(id -u)/dev.orbit.buffer-check 2>/dev/null
cp 07_Content-Ops/launchd/dev.orbit.buffer-check.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/dev.orbit.buffer-check.plist
launchctl kickstart gui/$(id -u)/dev.orbit.buffer-check; sleep 60; tail -n 30 ~/Library/Logs/orbit-buffer-check.log
```

The log should start with `--- <date>`, then `code: <commit>`, then the check's JSON.
