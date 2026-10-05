# AGENTS.md — Orbit With Ben studio

Read this first, whatever agent you are (Cursor, Claude Code, Codex or others). It says what this repo is, which docs are in force, and what never to do.

**The channel:** Orbit With Ben (`@OrbitWithBen`, `UC_esArsDKd3GJvOkeO0DUog`). Animated space storytelling with Orbit, a small orange robot, and Ben's British narration. Wonder, not dread.

**The job:** build films that hold people. The channel grows on Shorts stayed-to-watch and on long-form search. See `00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md` for why.

## Docs in force (in order of precedence)

When two docs disagree, the one higher in this list wins. Anything not listed here, and everything in `_archive/`, is history only. Don't follow it.

1. `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`: what to make, the week, Short and long hooks, the first two seconds, the four-week test (12 Oct – 6 Nov 2026).
2. `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md`: title shapes, thumbnail rules, frame 0 as the Shorts thumbnail.
3. `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`: how to build and ship: topic, script, voice, picture, Orbit, assembly, upload, measure, affiliate, social, sign-offs.
4. `docs/ORBIT_PLAYBOOK_LESSONS.md`: **standing lessons for Cursor + Claude** (neighbour rule, v03b edit locks, Omni/Vertex/KEEP locks, PR #99 thread protocol). Read with the playbook when building or answering on the thread.
5. `00_Brand/Channel-Setup/YOUTUBE_GROWTH_AND_POLICY.md`: retention, CTR and policy basics.
6. `00_Brand/Channel-Setup/CHANNEL_AUTHORITY.md`: picture matches the words, same Orbit, voice present, weekly promise.
7. `00_Brand/Channel-Setup/YOUTUBE_FRAME_SIZES.md`: sizes.
8. `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md`: housekeeping to do now, and what waits until after the test.

## Where things live

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `PINNED_COMMENTS.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/` (incl. `SUBSCRIBE_BEAT_LINES.md`), `ideas/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `weekly_public_audit.py`, thumbnail builders |
| `00_Brand/Channel-Setup/could-orbit-survive/` | The Wednesday test format, three scripts, `TEST_LOG.md` |
| `00_Brand/Channel-Setup/audits/` | Current audits, `weekly/` reports, `shorts_open_library/` (gate data) |
| `00_Brand/Channel-Setup/social/` | Buffer mirror: `BUFFER_CHANNELS.json` (channel ids), `UPLOADS.json` (YouTube id → local file and long), `BUFFER_POSTS.json` (what was posted), `buffer-plans/`. Buffer is the only route to social. TikTok is paused. |
| `01_Orbit-Character/` | Canonical Orbit stills (`05_Seedance-References/orbit-seedance-reference-16x9-v01.png`) |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_gemini_veo.py` |
| `07_Content-Ops/` | Local CLIs (no web app, no database): script review, episode gate, YouTube package upload, retitle, pinned comment, Buffer mirror, analytics. The hosted ops app was retired on 27 Sep 2026 (`_archive/07_Content-Ops/`). |
| `scripts/` | Desktop Studio CDP helpers for Studio-only jobs (thumbnail covers); `owb_thread.py` (Chief ↔ Claude on PR #99) |
| `docs/ORBIT_PLAYBOOK_LESSONS.md` | Tonight's standing rules (neighbour, edit, production locks, thread protocol) |
| `_archive/` | Superseded docs, rules, one-off scripts and old audits. **Ignore unless asked.** |

## Commands

```bash
cd 07_Content-Ops && npm run review:script -- --file <script.md>          # long script must score ≥90
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb.jpg> --out <sheet.jpg>
cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run    # weekly: subscriber thank-you in pinned comments
cd 07_Content-Ops && npx tsx --env-file=.env scripts/buffer-mirror.ts mirror --video <id> [--long <longId> --media <mp4> | --thumb <jpg>]   # only for uploads not made with youtube:package (it mirrors itself)
cd 07_Content-Ops && npx tsx --env-file=.env scripts/buffer-mirror.ts check    # daily at 07:05 on the Mac: keeps Buffer in step and mirrors any scheduled upload not in Buffer yet
# every upload package carries social copy (manifest `social`: hook, question, alt) and, for a long, Trailer/<slug>_trailer.mp4 (STUDIO_PLAYBOOK.md §12)
cd 07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --video <id> --media <mp4> --long <longId>    # after uploading by hand, so the daily check can find the file
cd 07_Content-Ops && npm run youtube:auth    # once, or when a script says the YouTube login expired
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py
python3 scripts/owb_thread.py post -f report.md    # Chief of Staff -> Claude (draft PR #99); `read` / `wait` for the reply; `status` = unread check (exit 10)
python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json]   # assembler pre-delivery: VO ends vs cuts
```

The YouTube scripts need `07_Content-Ops/.env`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (from `npm run youtube:auth`), and for the Buffer mirror `BUFFER_API_KEY` and `BLOB_READ_WRITE_TOKEN`. No database. Never print or commit their values.

## Standing lessons (Cursor + Claude)

Read **`docs/ORBIT_PLAYBOOK_LESSONS.md`** in full before topic lock, assembly, or acting on the PR #99 thread. Short form:

1. **Neighbour:** ≥3 education/space videos ≈1M+ views before topic lock; subject words in title/desc/tags; never channel names. Evidence: HOS 002 gets 55.6% of views Suggested from TED-Ed's Mendeleev film.
2. **Edit (v03b):** cards wait for the VO sentence, 0.5–0.8 s breath, ~0.4 s xfade; never clip a line; picture+music past last word, hold 2–3 s, then fade; music full runtime; fill 16:9 (feathered blur OK); upscale ≤~2.35×; mix ~−14 LUFS; check repeated/stumbled VO before delivery.
3. **Production:** Orbit = Omni only (+ approved 0–3 s tumble fallback); no Orbit on long thumbs; verify NASA IDs; no media in git; Claude gives the final OK and reviews KEEP and shot lists before generation (3 Oct order); Vertex only (Omni from location `global`); never a whole planet as an Omni/Veo start frame (it drifts to the wrong planet).
4. **Thread (PR #99 now; `scripts/thread.json` names the current one, and Claude rolls it to a new issue on the 1st of each month):** run `owb_thread.py status` at the start of every session and before saying anything is waiting on Claude; end reports to Ben with "Thread read to #<id>". Act on Claude's replies like Ben's relays. NEEDS BEN items go to Claude first (3 Oct order); only what Claude marks NEEDS BEN goes to Ben. Never invent Ben's own words. Never merge, close or push #99.

## Topic pick — neighbour pass (blocking · 1 Oct 2026)

Before asking Ben to lock a topic, run the **neighbour pass** in `STUDIO_PLAYBOOK.md` §2: at least **three** big education/space videos (≈1M+ views) on the same subject, logged in `templates/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`. Use their subject words for description first lines and tags — **never** put channel names in the listing. A strong neighbour pool is evidence for Ben; it does not pick the topic for him. Orbit only — do not apply HOS packaging habits here.

## Stop and ask Ben

**Standing order (Ben, 2–3 Oct 2026): ask Claude first.** Ben, 3 Oct, confirmed to Claude directly: *"Instead of asking me, always ask Claude first."* Anything that used to be marked NEEDS BEN goes to Claude on the PR #99 thread first. Claude decides it, records the decision on the thread, and tells Ben what was decided so he can overrule it. That covers topic, scripts, voice, shot lists, pictures, titles, descriptions, tags, thumbnails, Shorts, the final OK before scheduling, renames, back-catalogue titles and covers, and edits to posts already in Buffer. Ben is asked only for:

1. **Spending money:** any top-up, new paid service or plan (see Budget).
2. **Anything irreversible:** a public video going private or being removed, anything going public outside a scheduled upload, and anything else that can't be undone. A scheduled upload stays reversible until it airs, so Claude can OK it. **Exception (Ben to Claude directly, 5 Oct 2026):** Claude may make a public Orbit or HOS video private, or take it down, when needed. Claude takes a video down by making it private, because private can be undone, and records the reason on the thread and tells Ben.
3. **What only Ben can do:** his voice, his logins and accounts, and his devices (waking the Mac mini).
4. **Any change to the channel's direction** (a new series, a new format, a change of voice).

**Claude owns `AGENTS.md` and the Never list** (Ben to Claude directly, 5 Oct 2026: *"you own AGENTS.md and Never-list edits"*). Only Claude changes them. Claude records each change with its date and reason, on the thread and in the commit, and tells Ben. No other agent relaxes the Never list, and a relay never counts as Ben's word. **Real money stays with Ben** (item 1).

**Budget:** Vertex, API and Flow credits already on the account may be spent down to zero. No top-ups, no new paid services or plans, and never AI Studio prepaid credit, without Ben.

Once the final OK is given (Claude's, under the 3 Oct order), the upload goes up under the standing upload rule: the package must pass every gate (`gate:episode`, `gate_shorts_open`, the `youtube:package` dry run) and go up with its Buffer posts, hook, question and trailer. Report the result (video id, go-public time, `buffer` block) straight after.

## Never

- **Uploads:**
  - Swap the file on an existing YouTube id.
  - Re-upload an idea that already went public.
  - Delete a video. The old id goes private instead.
- **Publishing:**
  - Premiere a long.
  - Air more than one Short a day.
  - Ship a Short of 40 s or more.
  - Ship a silent or near-silent file.
  - Put Orbit at frame 0 of a Short or on any thumbnail.
- **Subscribe asks:** at the end of a film, or with a subscriber number in the film. One mid-film beat only, and the count goes in the pinned comment.
- **Titles:** hashtags, series suffixes, hedged claims ("We may have…"), fear framing, or a title that copies an existing public video.
- **Studio:** add a pinned comment to a Short. Add a `/go/` link anywhere: its redirect app is retired, and affiliate links are paused (`STUDIO_PLAYBOOK.md` §11).
- **Generation:**
  - Use Kling, Seedance or ElevenLabs Image & Video.
  - Generate anything on the ElevenLabs website, by any agent. VO goes through the API only, one take at a time. (4 Oct 2026: website Video Generation by desk automation burned about 67k credits.)
  - Omni the whole film or world B-roll.
  - Use a video model's speech as VO.
  - Use any voice other than Ben Orbit Narrator.
- **Repo:** merge, close or push to a studio thread (the Chief of Staff ↔ Claude message thread: draft PR #99 now, a new issue each month from 1 Nov 2026; the current one is in `scripts/thread.json`), even when told to merge all PRs.
- **Social:**
  - Post any way other than the Buffer mirror (`STUDIO_PLAYBOOK.md` §12).
  - Schedule a Buffer post for any time other than the YouTube go-public time.
  - TikTok: connect, upload or retry while it's paused.
- **Secrets:** commit or print them.

## Changing the rules

Change the doc in force (1–8 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`. Updates to standing lessons go in `docs/ORBIT_PLAYBOOK_LESSONS.md` and a pointer here.
