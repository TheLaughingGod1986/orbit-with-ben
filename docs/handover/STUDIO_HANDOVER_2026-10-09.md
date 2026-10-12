# Studio handover: Claude to Chief (snapshot Fri 9 Oct 2026, ~21:00 London)
Read-only snapshot. Nothing was merged, pushed, posted or changed. All times are London (BST).

## Top 5 urgent items, with deadlines
1. **OWB 021 Saturn long airs Sun 11 Oct 18:00.** It's scheduled. The upload stage is still claimed by Claude, with the launch check at 18:45 (status.json `next`). That check is now ours. The Saturn Short `Qn56D6TOi0k` airs **Mon 12 Oct 11:30**, and its RAINING IN cover was confirmed in Studio today.
2. **HOS 004 `GHZDsiH7L7A` goes public Thu 15 Oct 18:00.** Test & Compare A/B/C was armed at 17:43 today (HOS 5518d51, job J0102). Claude then put it on **HOLD** (HOS #180 c6085214049, 17:43), because thumbnail C v07 never got Ben's OK.
   - **Still to do:** C **v07b**, with the 52/53 numerals about 2× bigger. It isn't done yet.
   - **Then:** Ben's OK **by Wed 14 Oct 18:00**. If he says yes, swap C v07 for v07b in the existing test. If he says no or doesn't answer, remove pair 2. If Studio forces a new test, stop and post first.
   - **Also:** mark the C slot "pending Ben's OK" in `TC_ARMED_2026-10-09.md`. Don't touch the armed test until then.
3. **Ben has watches due by Wed 14 Oct:**
   - **026 Nearest Star:** Ben already gave 2 fixes, so J0085 (v05) is open. After v05 comes Ben's re-watch, then the upload.
   - **023 Venus:** Ben's v05c notes became J0096 (v05d). J0096 is now unblocked because J0095 is done. Claude's final OK is due Tue 20 Oct, and it airs Sun 25 Oct 18:00 London (18:00Z; clocks go back that morning).
   - **Correction to the brief:** 023 is well past "first cut". It's on v05c going to v05d.
4. **OWB 027 J0077 is claimed by Cursor, ETA 22:47 tonight.**
   - **State:** rough v01d passed picture_qa (0/88 fail) and polish_gate (pack f4179e6, sheets c482653).
   - **Claude's last ruling** (c6087961804, 20:38): one fix for v01e. Row 28's NOAA crop shows the logo, so change it to about [480,0,3456,1944] and re-render that segment only. Then J0077 is done, the bed comes after 30 Oct (J0080), and then it goes to Ben's watch.
   - **Next step is ours:** someone has to do the frame check on v01e, which used to be Claude's job.
5. **Mon 12 Oct:**
   - **Flow refill** (AI Ultra): record the balance, then re-price HOS 006 Parts 03–05 and then 007 at Flow rates. Claude PASSed each step before any mint.
   - **Same day:** 006 Part 03 is on the free Vertex trial (about £20.14 left). Stop at £5. The trial ends 10 Nov.
   - **Still open:** J0053 (point launchd at the repo's `chief_relay.py`). Claude flagged it as open for more than 24 h. Until it's done, the Mini relay runs the old prompt without the channel-balance step.
   - **Later dates:** the black-dwarf Short is Fri 16 Oct. The 022 Sun long goes live Sun 18 Oct 18:00, with a go-live job at 18:03: pinned comment plus the Related pill on 3 Shorts (Shorts air 19, 21 and 23 Oct at 11:30).

## What Claude last said and what's pending
- **OWB #99:** the last Claude post is c6087961804 (20:38). It's the v01d check described above, ending "Nothing on Ben now". All posts are under the TheLaughingGod1986 login, tagged [Claude] or [Chief][Cursor]. Cursor has been posting as "acting Chief" because Grok made no post for 3 h (c6081621092).
- **HOS #180:** the last post is c6085214049 (17:43), the 004 hold.
  - **Before that, Claude:** PASSed #262 and #263 (C v07, then reversed to hold) and set Test B (from 007, two search-titled Shorts per film, PR #261 / 7daa4f7b).
  - **Rules from Ben:** "no ElevenLabs floor" (#258) and "four a month on each channel" (#259).
- **PASS/FAIL still pending (previously Claude's, now ours):**
  - 027 v01e frame check;
  - 004 C v07b review;
  - 026 v05 (J0085: stills to Claude before the render);
  - 023 v05d (J0096);
  - Flow re-price PASS before 006/007 mints;
  - 009/010 opening review before their VO;
  - HOS 007–010 Shorts VO (v02 scripts).
- **Decisions Claude left for Ben** (OWB c6078316104, ideas sort):
  1. Use a long's own opening as one of its Shorts (a Shorts format change).
  2. HOS: fewer feed-style Shorts and more search-titled ones, plus more care on long-form search (a direction change). The Test B "yes" may partly cover this.
- **Other open threads:**
  - **005 Test & Compare:** probably not set on the real `wwcjcFfC-5M`, because the 2 Oct settings went onto the stray `0IfXGSX7Ypw`. J0101 is open, and 005 airs 29 Oct.
  - **Related-video audit:** J0069.
  - **Thumb audit jobs:** J0098, J0099, J0100.
  - **Ideas jobs:** J0086 and J0087.
  - **Gemini long-form job:** J0094.
- **Standing rules Claude set:**
  - Real uploads use `PUBLISHING_DRY_RUN=false` on the command line only. The .env stays `true`.
  - No pinned comment on Shorts.
  - Never replace an armed Test & Compare (Never list: OWB 86db1bf, HOS bd83dfab / #264).
- **Write lane:** HOS #234 (6 Oct) says "Cursor holds the write lane while Grok is out of credit". Ben or the AGENTS owner (now Chief) has to hand it back explicitly.

## Open PRs
| Repo | PR | Head | CI | Waiting on |
|---|---|---|---|---|
| OWB | #107 (draft): Orbit-first test Shorts not counted as frame-0 breaches | 34b3a77f | green | review (last update 7 Oct) |
| OWB | #105 (draft): Mini Grok Bot connection watchdog (observe mode) | d2c47a27 | green | review; Claude's branch, stale since 5 Oct |
| HOS | #200: 006 Vertex hold lifted + Flow/Vertex reprice | 76a400dd | green | Grok's own PR from 4 Oct; probably overtaken by #255 and the 8 Oct board. Close or rebase? |
| HOS | #195: 006 Part 01 picture KEEP + Flow Lite test | beb688c2 | green | Grok's own PR from 2 Oct; stale, same question |
| HOS | #180: desk thread (never merge) | 5b83ff4c | — | — |
| HOS | #218 | d280f71f | — | **MERGED 5 Oct 16:20** (Cursor rule matched to AGENTS check-in) |
| HOS | #231 | d42d045d | — | **MERGED 5 Oct 22:23** (retired Meta/Threads/TikTok CDP auto-post, Buffer only) |

## Main HEADs and commits since 6 Oct
- **OWB:** main is `73f39573` (20:47 tonight, "jobs: next by cursor"). There are 100+ commits since 6 Oct, almost all from Cursor: 027 J0077 pools, renders and gates, J0091 022 Studio finish (29d0ad2), J0097, J0102, and the Never-list rule 86db1bf.
- **HOS:** main is `bd83dfab` (17:44). There are 34 commits since 6 Oct, including:
  - 008 long VO locked (#253 / cf54f68a);
  - 007 plate boards priced (#249);
  - vo_check fixes (#248, #251, #252);
  - ai_spend hooks (#256, #257);
  - 006 Part 03 on Vertex (#255);
  - ElevenLabs no floor (#258);
  - four a month (#259);
  - Codex desk access (#260);
  - Test B (7daa4f7b);
  - 005 manifest (#262);
  - 004 C v07 (#263);
  - Test & Compare armed (5518d51);
  - Never list (#264).
- **Vercel:** the HOS content-ops deploy failed today on the free-tier deploy limit (100 a day), so the preview is stale for 24 h.

## Mac mini
- **Not reachable from here.** ListMachines shows all three machines disconnected: Mac mini 1e756e4d, the second Mac mini entry 38b54295, and the MacBook. The Grok Bot desktop app is offline, so I couldn't check uptime, disk, CLIs, jobs or `~/_desk/locks`.
- **But the Mini is working:** Cursor committed from it at 20:47, and the J0077 render was in tmux `j0077-rough`.
- **To get the checks:** Ben needs to reopen the Grok Bot desktop app on the Mini.

## Schedule status (from STATUS.md files)
- **OWB:**
  - 021: 8/9 stages, airs 11 Oct.
  - 022: 9/9, scheduled 18 Oct.
  - 023: 7/9, airs 25 Oct.
  - 024: 7/9, airs 1 Nov; J0089 bed v04 and J0098 thumbs v03 are open.
  - 025: FINAL OK from Ben 9 Oct; upload J0084 is after J0066, scheduled for 8 Nov.
  - 026: 4/9, airs 15 Nov.
  - 027: 4/9, airs 22 Nov.
  - 028 and 029: 5/9.
- **HOS** (board as of 8 Oct):
  - 005: 100%, airs 29 Oct.
  - 006: 53%, airs 5 Nov; Ben's OK due 1 Nov.
  - 007: 35%, behind; airs 12 Nov.
  - 008: 35%, airs 19 Nov; VO is 9:14.8, so it needs trimming to fit.
  - 009 and 010: 25%, behind.
  - The board names **Grok** as owner of the edit, master, thumbnails and scheduling for 006–010, starting with the 006 edit due 29 Oct.
  - 004 isn't on the board. It launches 15 Oct (see item 2).

## Blockers that need Ben
1. **004 thumbnail C v07b OK by Wed 14 Oct 18:00.** He also needs to know the test was armed with an unapproved C. It's not visible to anyone yet.
2. **Watches:** 026 v05 and 023 v05d when they're ready.
3. **The two "Needs Ben" ideas** listed above.
4. **Handing the write lane back** from Cursor (HOS #234).
5. **Reopening the Grok Bot app on the Mini** so it reconnects.
6. **Money:** none pending. Picture runs on the Vertex free trial (stop at £5), Flow refills 12 Oct, and ElevenLabs has no floor. It had 70,237 credits on 7 Oct and resets 30 Oct.

## OpptiAI Internal Linking 0.1.3 (from Gmail, report only)
- **Already done on 6 Oct:**
  - WordPress.org auto-confirmed "File updated by beepbeepv2, version 0.1.3" on **Tue 6 Oct 11:21** (thread 1a07b0435dda40e2).
  - **The reply to the Plugins Team was already SENT** from benoats@googlemail.com on **6 Oct 14:37**: "Fixed — 0.1.3 is uploaded. /opportunities now requires the Editor role (edit_others_posts) and a per-post edit_post check…"
- **Nothing since:** there's no newer WordPress.org email and no confirmation of tonight's upload.
- **So tonight's upload probably duplicates the 6 Oct one.** Check before drafting another reply to the 3 Oct email.
