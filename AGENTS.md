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
| `05_Analytics/` | Channel tracker (6 Oct 2026), OWB + HOS: `<channel>/snapshots/<date>.json` (every video, daily), `channel_daily.json` (YouTube Analytics), `<channel>/REPORT.md` (daily/weekly/monthly growth and every video), `dashboard/` (template + built page). Written by the Mac's 06:40 job; never edit by hand. |
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
cd 07_Content-Ops && npm run analytics:snapshot [-- --channel owb|hos]   # daily at 06:40 on the Mac (launchd/analytics-snapshot.sh, own worktree): read-only stats for every video
cd 07_Content-Ops && npm run analytics:report    # rebuilds 05_Analytics REPORT.md + dashboard from the snapshots (no network)
python3 00_Brand/Channel-Setup/tools/gate_upcoming.py --snapshot <owb snapshot> --uploads 00_Brand/Channel-Setup/social/UPLOADS.json --media-root <checkout> --out 05_Analytics/owb/UPCOMING_SHORTS_GATE.md --add   # runs in the 06:40 job: gates every Short scheduled in the next 14 days, report only
cd 07_Content-Ops && npx tsx --env-file=.env scripts/youtube-auth.ts --analytics owb|hos    # Ben, once per channel: read-only YouTube Analytics sign-in
python3 scripts/owb_thread.py post -f report.md    # Chief of Staff -> Claude (draft PR #99); `read` / `wait` for the reply; `status` = unread check (exit 10)
python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json]   # assembler pre-delivery: VO ends vs cuts
```

The YouTube scripts need `07_Content-Ops/.env`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (from `npm run youtube:auth`), `YT_ANALYTICS_REFRESH_TOKEN_OWB` / `_HOS` (read-only tracker sign-ins), and for the Buffer mirror `BUFFER_API_KEY` and `BLOB_READ_WRITE_TOKEN`. No database. Never print or commit their values.

## Standing lessons (Cursor + Claude)

Read **`docs/ORBIT_PLAYBOOK_LESSONS.md`** in full before topic lock, assembly, or acting on the PR #99 thread. Short form:

1. **Neighbour:** ≥3 education/space videos ≈1M+ views before topic lock; subject words in title/desc/tags; never channel names. Evidence: HOS 002 gets 55.6% of views Suggested from TED-Ed's Mendeleev film.
2. **Edit (v03b):** cards wait for the VO sentence, 0.5–0.8 s breath, ~0.4 s xfade; never clip a line; picture+music past last word, hold 2–3 s, then fade; music full runtime; fill 16:9 (feathered blur OK); upscale ≤~2.35×; mix ~−14 LUFS; check repeated/stumbled VO before delivery.
3. **Production:** Orbit = Omni only (+ approved 0–3 s tumble fallback); no Orbit on long thumbs; verify NASA IDs; no media in git; Claude gives the final OK and reviews KEEP and shot lists before generation (3 Oct order); Vertex only (Omni from location `global`); never a whole planet as an Omni/Veo start frame (it drifts to the wrong planet).
4. **Thread (PR #99 now; `scripts/thread.json` names the current one, and Claude rolls it to a new issue on the 1st of each month):** run `owb_thread.py status` at the start of every session and before saying anything is waiting on Claude; end reports to Ben with "Thread read to #<id>". Act on Claude's replies like Ben's relays. NEEDS BEN items go to Claude first (3 Oct order); only what Claude marks NEEDS BEN goes to Ben. Never invent Ben's own words. Never merge, close or push #99.
5. **Shorts feed (5 Oct):**
   - Judge a Short by its day-1 Shorts-feed share (50% or more means fed), not by % viewed under ~50 views.
   - Stop a topic after 2 not-fed Shorts in a row, and run at most 6 in a row on one topic; then give it a 2-week break.
   - Every Short gets its own open, with frame 0 showing the titled subject and no opening background reused from the last 10 Shorts.
   - Aim for 60% or more average viewed on day 1.
   - End on the long's exact listing title and its video id, with a music bed for the full length.
   - Details: lessons doc §6.
6. **YouTube state changes leave a record (6 Oct).** Any change to a video's privacy or `publishAt`, by any agent, script or Studio click, gets a line on the thread in the same session, with the id, the old and new state, and who OK'd it. If it's a Short, update its open-gate library status in the same commit (`gate_shorts_open.py status`, or `fetch` once it's public). Lesson: `CtllH6VOhEI` was rescheduled on 1 Oct by an untracked one-off script. FIX_LOG said private for 5 days while it was live, and the Shorts gate didn't compare against it.

## Topic pick — neighbour pass (blocking · 1 Oct 2026)

Before asking Ben to lock a topic, run the **neighbour pass** in `STUDIO_PLAYBOOK.md` §2: at least **three** big education/space videos (≈1M+ views) on the same subject, logged in `templates/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`. Use their subject words for description first lines and tags — **never** put channel names in the listing. A strong neighbour pool is evidence for Ben; it does not pick the topic for him. Orbit only — do not apply HOS packaging habits here.

## Who does what (7 Oct 2026)

| Agent | Where | Does |
|---|---|---|
| **Claude** | Cloud sessions | Scripts, reviews and final OKs (3 Oct order), shot lists, code and tools, the channel tracker. Can't reach the Mini. |
| **Chief (Grok Bot)** | Mac mini | **First in line for Chief.** Runs the Mini: picture, edit, uploads, Studio jobs. Drives Gemini and the assembler. Posts on the studio thread. |
| **Cursor** | Mac mini (`agent` CLI) | Code on the Mini. **Next in line for Chief** (see "Chief relay"): while Grok is out, the relay wakes it every 30 min to do one job as acting Chief. |
| **Codex** | Mac mini (`codex` CLI) | **Third in line for Chief:** acts as Chief when Grok and Cursor are both down. Otherwise code jobs when Ben starts it. |
| **Gemini** | Mac mini (Antigravity `agy` CLI) | **The second check on facts and numbers.** Drafts `01_Script/SOURCES.md` with exact quotes and links, verifies every row of Claude's `CLAUDE_CLAIMS` file, and flags errors. It never rewrites spoken lines (Claude's call). Run by whoever is Chief; claims as `<driver>/gemini` (e.g. `chief/gemini`, `cursor/gemini`). No spend. |
| **Ben** | | Real money, things only he can do, and changes of direction. |

Every script gets a Gemini source and claims pass before VO is locked. Gemini only runs when the Chief (or whoever is acting Chief) starts it, so a script waiting on sources is the Chief's job to kick off.

## Job queue (7 Oct 2026)

Work goes through `scripts/jobs.py` (`jobs/queue.json`, shown in `JOBS.md` and on the Studio Kanban), not prose addressed to one agent. **A job says what it needs, not who does it**, so whichever agent is up does it.

| Agent | `--can` |
|---|---|
| Chief (Grok Bot) | `mini,gemini,any` |
| Cursor | `mini,gemini,any` |
| Codex | `mini,gemini,any` |
| Claude | `cloud,any` |

- **Claude adds every task as a job:** `jobs.py add --needs mini|gemini|cloud|ben|any --title … --body-file … [--film NNN --stage …] [--after Jnnnn] [--ref <thread comment>] --by claude --git`. The thread carries the discussion and links the job id.
- **Every agent, at the start of every session and every loop:** `python3 scripts/jobs.py next --agent <you> --can <yours> --git`. It returns the job you already hold, or claims the next one you can do: quick jobs (`--eta` 60 or less) first, then oldest first. Exit 10 means nothing is waiting. Then `done`, `block --reason` (anything needing Ben), `release --note` at a stopping point, or `renew --eta N` if you're still on it.
- **A claim past its ETA is stalled,** and the next able agent takes it over. So don't sit on a claim; release it if you stop.
- A job with `--film/--stage` claims that board stage too, so the board and the queue always agree.

## Chief relay (7 Oct 2026)

Ben: the Chief of Staff is in charge, and when it's down or out of credit the next one in line takes over. **Chain: Grok Bot (`chief`) → Cursor (`cursor`) → Codex (`codex`).** The first one that is up is the acting Chief. `scripts/chief_relay.py` runs it on the Mini (launchd `com.owb.chief-relay`, every 30 min, 08:00–22:00):

- **Grok Bot** is an app with no CLI, so nobody can prompt it to report in, and its app files only show the app is open, not that it has credit. It counts as up when it has posted on the studio thread as plain "[Chief]" in the last 3 hours, or run `jobs.py … --agent chief`. Cursor and Codex posts are tagged "[Cursor]"/"[Codex]" or say "covering", so they don't count. While Grok is up the relay does nothing.
- **Cursor or Codex:** otherwise the relay wakes the first one that's up for **one** job (25-minute cap). A run that ends with out of credit, usage limit or signed out marks that agent down for 3 hours, and the same run passes the job to the next in line.
- **Grok takes back over by itself:** its first post on the thread after its credit returns makes it Chief again, and the others stand down. Nobody flips anything by hand.
- Each change of Chief is posted once on the thread ("Chief relay: … is acting Chief"). If all three are down it says so once; top-ups stay Ben's call.
- Commands: `chief_relay.py status` (who's Chief and why), `down <agent> --reason … [--until …]`, `up <agent>`, `seen chief`. Pause: `touch ~/_desk/state/chief-relay.pause`.
- **Gemini isn't in the chain.** It's the checker and can't run the Mini, so whoever is acting Chief runs it (`agy`) for every job that `--needs gemini`. `status` shows it on its own line.
- **Thread posts name the writer:** the relay sets `OWB_AGENT` for the CLI it wakes, so `owb_thread.py post` writes "[Chief] [Cursor] …" or "[Chief] [Codex] …". Grok's posts stay "[Chief]".
- **Long work outlives the 25-minute run:** renders, big downloads and batches start detached in `tmux` with a log and a `.done` file. The run releases the job with a note naming them, and the next run checks the `.done` file. Never start a second copy of a render that's still running.
- **If the Mini goes quiet:** Claude's 2-hourly check runs `jobs.py watch`. If Mini work is waiting and nothing has touched the queue for 3 hours, it posts here and pushes Ben's phone once. It also pushes Ben when a job needs him or is blocked on him.
- **Acting Chief** uses its own agent id everywhere (`--agent cursor`, `--by codex`), never `chief`. Only Grok Bot is `chief`, because that id is Grok's heartbeat. Its reports start "<Name> covering".

## Studio board and claims (5 Oct 2026)

- **State lives in `02_Video-Projects/<film>/status.json`, not in the thread.** Start every session with `python3 scripts/studio.py board`. Read the thread only for decisions. `STATUS.md` at the repo root is the same board as a page for Ben (what's being worked on, how far through, next step, ETA). `claim`/`release`/`set` regenerate it, and CI fails if it's stale.
- **Claim before you work or spend:** `python3 scripts/studio.py claim <film> <stage> --by <agent> --eta <min> --git`. This works the same for Mini jobs, Cursor, Codex and cloud Claude sessions, so a stage can't be done twice.
  - If the claim exits 75, someone else holds that stage. Stop.
  - When you finish, run `release … --state review|done --ref <sha> --git`.
- **Stalled jobs:** a claim past its ETA counts as stalled. `studio.py stale` lists stalled claims; the Mini runs it every 15 minutes and posts any hit to the thread.
- **Background jobs commit from their own clean worktree** (`git worktree add /tmp/<job>-wt origin/main`), never from the shared Mini checkout. On 5 Oct, uncommitted Buffer JSON in that checkout blocked the 027 SOURCES commit for 6 hours.
- **Mini-only resources:** the ElevenLabs pool, Vertex and Studio writers also keep their `desk-lock` (`07_Content-Ops/scripts/desk-lock.sh`).
- **VO takes:** use `04_Audio/tools/vo_take.py` (`--script` for a long, `--text` for a Short or pickup; `--dry-run` first). It locks the voice, makes one take, keeps the 20k floor (any ElevenLabs spend, music beds included, stops if the pool would end under 20,000 credits), runs Scribe, and writes one `<stem>_TAKE.json` plus a line in `04_Audio/elevenlabs_ledger.jsonl`. Don't copy a new `_generate_*.py` for a take.

## NAS archive (5 Oct 2026)

The Synology share (`/Volumes/data/mac-mini-archive/`) is the archive, and often holds the **only** copy: the 3 Oct and 5 Oct moves deleted the Mini copies after checking them.
- **Never delete anything on the NAS.** "Looks like a partial duplicate" is not proof. On 5 Oct the HOS 003 folder held 1,090 files that existed nowhere else.
- **Moving files to the NAS:**
  1. rsync, then SHA-256 manifests on both sides;
  2. delete the Mini copy only on a full match;
  3. leave a `MOVED_TO_NAS.txt` in the Mini folder.
- **Restoring:** git-tracked files are never overwritten from the NAS; the git copy wins.
- Any job that moves files claims first (`studio.py claim … --git`) and runs in detached tmux. On STOP, its last act is to post the STOP line or set its stage to `blocked`.

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
