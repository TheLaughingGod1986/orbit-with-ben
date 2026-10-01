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
python3 scripts/owb_thread.py post -f report.md    # Chief of Staff -> Claude (draft PR #99); `read` / `wait` for the reply
python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json]   # assembler pre-delivery: VO ends vs cuts
```

The YouTube scripts need `07_Content-Ops/.env`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (from `npm run youtube:auth`), and for the Buffer mirror `BUFFER_API_KEY` and `BLOB_READ_WRITE_TOKEN`. No database. Never print or commit their values.

## Standing lessons (Cursor + Claude)

Read **`docs/ORBIT_PLAYBOOK_LESSONS.md`** in full before topic lock, assembly, or acting on the PR #99 thread. Short form:

1. **Neighbour:** ≥3 education/space videos ≈1M+ views before topic lock; subject words in title/desc/tags; never channel names. Evidence: HOS 002 gets 55.6% of views Suggested from TED-Ed's Mendeleev film.
2. **Edit (v03b):** cards wait for the VO sentence, 0.5–0.8 s breath, ~0.4 s xfade; never clip a line; picture+music past last word, hold 2–3 s, then fade; music full runtime; fill 16:9 (feathered blur OK); upscale ≤~2.35×; mix ~−14 LUFS; check repeated/stumbled VO before delivery.
3. **Production:** Orbit = Omni only (+ approved 0–3 s tumble fallback); no Orbit on long thumbs; verify NASA IDs; no media in git; Ben OKs anything public; nothing is KEEP until Ben reviews; shot list to Ben before generation; Vertex only.
4. **Thread (PR #99):** act on Claude's replies like Ben's relays, except **NEEDS BEN** → Chief of Staff for Ben. Claude's reply is never Ben's OK. Never merge, close or push #99.

## Topic pick — neighbour pass (blocking · 1 Oct 2026)

Before asking Ben to lock a topic, run the **neighbour pass** in `STUDIO_PLAYBOOK.md` §2: at least **three** big education/space videos (≈1M+ views) on the same subject, logged in `templates/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`. Use their subject words for description first lines and tags — **never** put channel names in the listing. A strong neighbour pool is evidence for Ben; it does not pick the topic for him. Orbit only — do not apply HOS packaging habits here.

## Stop and ask Ben at each of these points

1. Topic (after the neighbour pass is filled)
2. Long script (after it reaches 90)
3. Short scripts
4. Voice
5. Moving picture (never judge from stills)
6. Thumbnails
7. Anything that goes public, is renamed, or is deleted. **Standing exception (Ben, 28 Sep 2026): uploads.** A scheduled upload whose topic, scripts, voice, moving picture and thumbnails Ben has already OK'd, and whose package passes every gate (`gate:episode`, `gate_shorts_open`, the `youtube:package` dry run), goes up without asking, with its Buffer posts, hook, question and trailer. Report the result (video id, go-public time, `buffer` block) straight after. Renames, deletes, back catalogue (`--allow-late`) and edits to posts already in Buffer still need his OK.

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
  - Omni the whole film or world B-roll.
  - Use a video model's speech as VO.
  - Use any voice other than Ben Orbit Narrator.
- **Repo:** merge, close or push to draft PR #99 (the Chief of Staff ↔ Claude message thread), even when told to merge all PRs.
- **Social:**
  - Post any way other than the Buffer mirror (`STUDIO_PLAYBOOK.md` §12).
  - Schedule a Buffer post for any time other than the YouTube go-public time.
  - TikTok: connect, upload or retry while it's paused.
- **Secrets:** commit or print them.

## Changing the rules

Change the doc in force (1–8 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`. Updates to standing lessons go in `docs/ORBIT_PLAYBOOK_LESSONS.md` and a pointer here.
