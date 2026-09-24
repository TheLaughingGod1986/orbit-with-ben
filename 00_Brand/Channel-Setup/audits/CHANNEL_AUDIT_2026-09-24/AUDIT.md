# Orbit with Ben — full channel audit (24 Sep 2026)

Why views are low, and what to do about it.

Sources: anonymous public channel pages for `@OrbitWithBen` (`UC_esArsDKd3GJvOkeO0DUog`) captured Thu 24 Sep 2026, about 22:00 BST, four hours after the Andromeda long went live. Raw rows are in `PUBLIC_SNAPSHOT.json`. This pass also reads the repo's own records: the 10 Sep Studio audit, the 21 Sep public audit, `docs/sound-check.md`, and the strategy docs locked 23–24 Sep. There is no new Studio read, so the retention figures below are from 10 Sep.

## Verdict

**8 subscribers. 48 public Shorts in the Shorts tab with 4,806 views (median 63). Nine longs with 131 views between them.** The channel is about eight weeks old.

The channel is not suppressed. There are no strikes, no claims, and new Shorts still get a feed test on day one (10 Sep Studio audit). Views are low for three reasons, in this order:

1. **Most viewers swipe away in the first seconds.** The last Studio read had 31.7% stayed-to-watch across Shorts, and no Short was above 46%. YouTube runs a small test on each new Short and stops once it sees that number. That is why every Short spikes on day one and then stops. Small channels that grow usually sit around 60–80%.
2. **Broken or self-contradicting uploads keep reaching the public**, and each one spends a feed test that a re-upload does not get back. This week four Moon Shorts went out with no voice at all.
3. **The plan changes every few days, and the newest rules undo the evidence.** The Monday Moon Short breaks a rule that was proven on 9–10 Sep. So did today's Andromeda launch.

Longs are a separate issue. They get almost no impressions because 8 subscribers gives YouTube no audience to test them on, and the search terms they target are held by much larger channels. The fix there is patience plus Shorts that hold viewers, not more longs.

## 1. The numbers today

### Longs

| Views | Length | Title | Live |
|------:|-------:|-------|------|
| 0 | 10:21 | Everything you need to know about the Andromeda crash #space #astronomy #science | 4 hours, **Premiere** |
| 4 | 8:39 | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone | 7 days |
| 14 | 9:43 | What Happens If You Get Near a Neutron Star | 2 weeks |
| 15 | 9:19 | Could Life Exist Under The Ice Of Europa? | 3 weeks |
| 41 | 8:38 | What Happens When the Last Star Dies? \| Orbit's Cosmic Journey | 4 weeks |
| 28 | 16:33 | JWST Found Galaxies That Shouldn't Exist Yet | 1 month |
| 13 | 21:29 | Alien Worlds: The Strangest Planets We've Ever Found | 1 month |
| 4 | 21:13 | What Happens If You Fall Into a Black Hole? | 1 month |
| 12 | 18:32 | Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | 2 months |

Moon has one more view than it had three days ago. Neutron has three more in two weeks. A long here gets 10–40 views in its lifetime.

### Shorts

- 9 Shorts are at 200 views or more. 19 are under 50.
- Top five: What Remains After the Last Star Dies? (622), Why You Can't Stand on a Neutron Star (419), The Sky Is Already Running Out of Light (292), Why Europa Is Hiding a Massive Ocean (291), Is the Moon Leaving Us? (290).
- Each winner is 22–27 seconds and promises something concrete: your body failing, something running out, or one number.

## 2. Why the views are low

### 2a. Viewers leave in the first two seconds

This is the main reason. Everything else in this audit makes it worse.

From the 10 Sep Studio read: stayed-to-watch 31.7%, swiped away 68.3%. The best Short (*Europa Sprays Its Ocean*) held 46%. The most-viewed Shorts held 15–39%. View counts do not follow retention. They follow the size of the day-one test, and retention decides whether a second day happens. None has had one yet.

Why viewers swipe (partly judgment, from the thumbnails, titles, and the 10 Sep frame checks):

- **The first second looks like every other AI space channel.** Glowing Veo nebula or planet, a caption, and a smooth AI narrator is the most crowded format in space content in 2026, and feed viewers have learned to swipe past it. A still globe with a caption held 15–17%. A moving plume held 46%.
- **Orbit is the one thing no other channel has, but it is used as decoration or a bumper.** When Orbit opened a Short with nothing happening, feed traffic dropped to zero (`TE_HDKAnqms`, 2 views). That result does not mean Orbit is bad. It means Orbit with no stakes looks like an intro card. See §3a.
- **Near-identical Shorts in a row.** Six Europa Shorts opened on the same frame (0–3 bits apart by perceptual hash). Seven Neutron titles in a row ended "…Neutron Star". The feed treats a run like that as one idea being tested again.

### 2b. Broken uploads spend tests that re-uploads cannot win back

| What shipped | Evidence | Cost |
|---|---|---|
| **Four Moon Shorts with no voice at all**, public 21–24 Sep (`Roh1QI2fTjs`, `Y_SQGPd4Amc`, `oFTYeBFtSQ4`, `c_iLsiU5qTA`) | `docs/sound-check.md`: whole file at about −90 dB | The replacements have **2, 3, 4 and 6 views**. The three Moon Shorts that went out with a voice have **290, 253 and 100**. |
| Orbit-first opens (`TE_HDKAnqms`, `mAAMsbhm88w`) | 10 Sep audit: 0% Shorts-feed traffic | 2 views. The second one was caught before it aired. |
| Same cut public three times (Sky) | 10 Sep audit | Split one idea's test three ways. Now fixed. |

**This corrects the 21 Sep audit.** That audit put the 21-view *What's Dragging the Moon Away From Earth?* down to a vague title ("the cleanest A/B this channel has"). That upload (`Roh1QI2fTjs`) was **silent**. Its title was never tested. Do not use that row as evidence about titles.

A re-upload of an idea that already went out does not get a fresh test. The four replacements prove this. Duplicate uploads of the same content also count against a channel under YouTube's reused / inauthentic content rules, which matters when you apply for the Partner Programme. Fix a video before it goes out. Do not plan on re-uploading it.

### 2c. The plan keeps changing, and the newest version goes against the evidence

Twelve docs in this repo say "locked". Several of them now disagree with each other, and with the only data the channel has.

| Rule backed by data | Where the data is | What happened since |
|---|---|---|
| Do not open a Short on Orbit. The first second must be the world, already moving. | 10 Sep audit, §4b/§6 (0% feed traffic); `gate_shorts_open.py` | `FAMILIAR_DANGER_STRATEGY.md` (23 Sep) says: *"Spoken in the first second. Orbit is on screen, looking at the camera."* The Monday Moon Short is **scheduled for Mon 5 Oct 11:30** with that open. |
| No Premieres while subscribers are under a few hundred | 10 Sep audit, §6.6 (13 impressions and 0 views in the Neutron Premiere's first hour) | **Andromeda premiered today.** 0 views after 4 hours. |
| Keep the Andromeda title *What Happens When Andromeda Hits the Milky Way?*, the shape of the only long that worked | 21 Sep audit, item 1 | The live title is *Everything you need to know about the Andromeda crash #space #astronomy #science*, which has hashtags in the title and no question. |
| Wonder, not dread. No fear titles. | `FAMILIAR_DANGER_STRATEGY.md` | The Andromeda thumbnail says **COMING FOR US?** The 25 Sep Short is *Is Andromeda Coming to Destroy Us?* |
| Three Shorts and one long a week | `FAMILIAR_DANGER_STRATEGY.md` (23 Sep) | 25 Sep–7 Oct has ten Shorts and two longs scheduled, seven of them Andromeda Shorts on consecutive days. |
| A new angle, not a second copy of a winner | `WEEK_PLAN_3_SHORTS_1_LONG_2026-09-23.md` | The Fri 2 Oct Short is titled *What Remains After the Last Star Dies*, which matches the 622-view Short. The Wed 7 Oct Short is *What happens if you touch a neutron star?*, which matches `Rp_8J6_6IIk`. Two Shorts with the same title compete for the same search and look like re-uploads. |

When the plan changes every 2–3 days, no single idea gets a clean test. Most of the effort has gone into the pipeline: about 50 merged branches, more than 20 one-off fix scripts in `audits/`, and posting scripts up to `_v17`/`_v18`. Much less has gone into the first two seconds of one Short.

### 2d. Longs: no audience for YouTube to test them on

- Longs had 13–170 lifetime impressions each (10 Sep). With 8 subscribers, Browse and Suggested have nobody to show them to.
- About 0.1% of Shorts viewers go on to a long. The Related links are set up correctly (checked 10 Sep).
- The search terms are owned by very large channels. "What happens if you fall into a black hole", "Fermi paradox" and "JWST galaxies too early" are held by channels with millions of subscribers. A new channel's 18–21 minute film on the same term cannot rank.
- The thumbnails (checked today) are clean but generic. They are AI space art with two to four words in yellow and white, and in a feed they are hard to tell apart from dozens of other channels. Orbit, the one recognisable brand element, appears on only two of the nine (Black Hole and Fermi). Those two are also the longest films, so this data cannot say whether Orbit on a thumbnail helps or hurts.

### 2e. Things that are not the cause

- Strikes, copyright, or restrictions: none (10 Sep).
- The niche: space mysteries win on this channel when the packaging is concrete.
- Related links, description links, and pins: correct.
- Instagram, Facebook and Threads mirrors: 0.8% of views came from outside YouTube. They are housekeeping, not growth.
- The AI disclosure setting (turned on for every upload in `a259d37`): YouTube says the label does not affect distribution. For clearly animated content it is optional. Keep it on, since it is the safe choice.
- Posting time and day.

## 3. What to do, in order

### This week (no new generation)

1. **Fix the Andromeda long's packaging now.** Change the title back to *What Happens When Andromeda Hits the Milky Way?* and take the hashtags out of the title. They already sit in the description. Make the thumbnail agree with the title. *COMING FOR US?* against "Everything you need to know" is two different promises, and neither is the wonder the channel says it is about. Changing a title four hours after launch costs nothing.
2. **Check every scheduled Short with the sound on, on a phone, before it airs.** That covers the seven Andromeda Shorts (25 Sep–1 Oct), Last Star (2 Oct), Moon (5 Oct) and Neutron (7 Oct). For each one, check three things:
   - you can hear the narrator from the first second;
   - the first frame is a moving world shot, not Orbit and not a still image;
   - its first frame differs from the previous day's.
   Any Short that fails goes private until it is fixed. Do not re-upload after it airs.
3. **Add a hard audio check to `tools/gate_shorts_open.py`.** Fail any file with no audio stream, or whose narration window reads below about −40 dB mean (ffmpeg `volumedetect`). The 10 Sep gate checked only the picture, and the silent Moon week got through it.
4. **Retitle the two duplicate-title Shorts** (2 Oct *What Remains After the Last Star Dies*, 7 Oct *What happens if you touch a neutron star?*) so each is a new promise, and remove the hashtags from the 7 Oct title.
5. **Settle the Orbit-first question with a test, not another rule change.** Decided 24 Sep, and written into `FAMILIAR_DANGER_STRATEGY.md`: new Shorts open on the moving world, and Orbit arrives from about 1.5 seconds. The three Orbit-first Shorts already scheduled (2, 5 and 7 Oct) air unchanged as a labelled test against the world-first Andromeda Shorts, judged on stayed-to-watch at 48 hours.

### The next four weeks: one goal, one number

6. **Freeze the plan for four weeks.** Stop writing new "locked" strategy docs. Every week, the only question is whether stayed-to-watch went up.
7. **Measure one number: stayed-to-watch at 48 hours, in Studio, for every Short.** Aim for more than 45% by mid-October and 60% or more after that. Write down the first frame of every Short under 35%. Views are the result, not the goal.
8. **Make three strong Shorts a week, not seven or ten.** Spend the time the extra uploads would take on the first two seconds:
   - The picture moves at frame 0, on the thing the title names.
   - The first spoken line is the promise ("You could never stand on this star").
   - Something visibly changes by 2 seconds.
   - 22–27 seconds, and the loop comes back to the opening shot.
9. **Make Orbit the reason to stay, not the intro.** Orbit reacting to something happening (being pulled, freezing, stretching) is something no other channel can show. Orbit looking at the camera over a static shot looks like a channel ident. Test one Short a week where Orbit is caught up in the danger from about 1 second, and compare it with the week's world-first Shorts.
10. **Only make a long about a topic whose Short has already worked**: more than 200 views and more than 40% stayed. Last Star is the only long with any audience, and it came after its Shorts had already won. Keep longs to 8–9 minutes. Title them for the search phrase people actually type (*What Happens When Andromeda Hits the Milky Way?*, not *Everything you need to know…*).
11. **Do not re-upload, remint or replace anything that is already public.** Leave winners alone. Leave losers up as data.

### What good looks like by late October

- Stayed-to-watch above 45% on at least half of the month's Shorts.
- At least one Short still getting views three or more days after posting, instead of stopping after day one.
- Subscribers in the tens, then the hundreds. After that, longs start getting Browse traffic without extra work.

Until then, expect a long to get about 10–40 views. That is normal for a channel with 8 subscribers, not a sign that something is broken.

## Re-measure

Wed 30 Sep, after five Andromeda Shorts: public views, Studio stayed-to-watch at 48 hours for each, and Andromeda long impressions and CTR. Record them next to the 10 Sep table so the trend is visible.

## 4. Studio fix list (24 Sep)

Applied in the repo this pass: the sound check in `tools/gate_shorts_open.py`, and items 5–11 in `FAMILIAR_DANGER_STRATEGY.md`, the week plan and the matching Cursor rules.

The Studio changes need the YouTube connection, which lives in the Content Ops database. They could not be run from the audit session. Run them from a machine with `07_Content-Ops/.env`:

```bash
cd 07_Content-Ops
npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json --dry-run
npx tsx scripts/retitle-videos.ts --file ../00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/STUDIO_FIXES.json
```

The script changes titles only, and skips any video whose title has changed since this audit. The result is written to `STUDIO_FIXES_RESULT.json`.

| # | Video | Change | How |
|---|-------|--------|-----|
| 1 | `ojk-dfOpAmw` Andromeda long | Title → *What Happens When Andromeda Hits the Milky Way?* | `STUDIO_FIXES.json` |
| 2 | `Ih2zhZTbIR0` Fri 2 Oct Short | Title → *The Last Stars Will Shine for 10 Trillion Years* (was a copy of the 622-view Short) | `STUDIO_FIXES.json` |
| 3 | `pL339HhjDwo` Wed 7 Oct Short | Title → *This Star Is 20 km Wide and Heavier Than the Sun* (was a copy of `Rp_8J6_6IIk`, with hashtags, and did not match the film) | `STUDIO_FIXES.json` |
| 4 | `ojk-dfOpAmw` thumbnail | Replace *COMING FOR US?* with wording that matches the new title, for example *WHEN THEY MEET* | Studio, by hand |
| 5 | `xQlV9G9lqLI` Mon 28 Sep Short | Its title *What Happens When Andromeda Hits The Milky Way?* will duplicate the long after fix 1. Retitle it for what the Short actually shows. | Studio, by hand after watching it |
| 6 | `P9Jiw-MwUEU` Fri 25 Sep Short | *Is Andromeda Coming to Destroy Us?* is a fear title, against the lane rule. Retitle for what it shows, for example *Is Andromeda Already in Our Sky?* | Studio, by hand after watching it, before 11:30 on 25 Sep |
| 7 | All seven Andromeda Shorts (25 Sep–1 Oct) | Watch each on a phone with the sound on: voice from the first second, a moving world at 0 s, a different opening from the previous day | Studio preview |

**Also noted (no change needed now).** The Fri 2 Oct and Wed 7 Oct Shorts name their long on screen and in the voiceover by the wrong title. Fri says *What Remains After the Last Star Dies?*, but the long is *What Happens When the Last Star Dies?* Wed says *Why You Can't Stand on a Neutron Star*, which is a Short; the long is *What Happens If You Get Near a Neutron Star*. The Related link still points at the right long, so leave them. Future scripts should copy the long's live title exactly.

