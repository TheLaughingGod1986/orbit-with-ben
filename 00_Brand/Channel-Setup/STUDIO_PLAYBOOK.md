# Orbit With Ben — studio playbook

How to make an Orbit film, from topic to the week after it's live. Written 25 Sep 2026. It replaces:
- the house/UAT bible;
- the Omni long-form playbook;
- the long-form story/VO gate;
- the Moon Leaving v04 lock;
- the Growth System v2 docs;
- the 27 old Cursor rules.

Those are in `_archive/` for history only.

**The strategy** (what to make, the week, the hooks, the test plan) is `FAMILIAR_DANGER_STRATEGY.md`. **Titles and thumbnails** are `THUMBNAIL_AND_TITLE_RULES.md`. This file is **how** to build and ship. Where they overlap, the order of precedence is in `AGENTS.md`.

Channel: **Orbit With Ben** · `@OrbitWithBen` · `UC_esArsDKd3GJvOkeO0DUog`. Pixar-warm space storytelling with documentary bones. Wonder, not dread.

---

## 1. The week

| Slot | What | When (UK) |
|---|---|---|
| Sunday | One long, 8–9 min, **normal publish (no Premiere)** | 18:00 |
| Mon · Wed · Fri | Three Shorts, 22–27 s. One teases the new long, two promote films already up. | 11:30 |

- Never more than one Short a day.
- Never a second long on a subject that already has a public long.
- 12 Oct – 6 Nov is the four-week test (`FAMILIAR_DANGER_STRATEGY.md`). Every Wednesday is a *Could Orbit Survive…?* Short (`could-orbit-survive/`).

## 2. Pick the topic (before any script)

1. **Use the channel's own data.** Read the latest `audits/weekly/<date>/REPORT.md`, `audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md` and `audits/THUMBNAIL_TITLE_AUDIT_2026-09-25/`. What wins is a familiar thing in danger (the Moon, the Sun, a star, your body) told as an ending, a body impossibility, a yes/no question, something hidden, or one real number.
2. **Competition check.** Search the exact title on YouTube, signed out. If all top five results are channels with millions of subscribers, narrow the angle.
3. **Score it:** `templates/TOPIC_OPPORTUNITY_SCORE.md`.
4. **Pre-build vidIQ audit:** copy `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` into the project's `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`. Wonder beats a higher vidIQ score for fear or conspiracy.
5. **Scaffold:** copy `02_Video-Projects/_template_NNN_Episode-Slug/` to `02_Video-Projects/NNN_Slug/`.

## 3. Script

### Long (8–9 min, about 1,200–1,300 spoken words)

- **First 3 s of picture:** the danger itself. No logo, no title card, no Orbit.
- **Sentence one** is the promise. Name the payoff within 30 s: curiosity by 5 s, stakes by 15 s, journey by 30 s.
- **4–6 acts,** told as cause and effect (this happened, but, therefore), not a list of facts. Each act: entry, show, one teach, turn, exit.
- **The world does the science.** Orbit appears in 1–2 inquisitive or story beats only.
- **Picture changes about every 4–6 s:** a new view, the named thing on screen, or a sound cue with a graphic.
- **Every number is sourced.** Sources go in the description.
- **One subscribe beat, mid-film** (added 25 Sep 2026). Put a `[SUBSCRIBE BEAT]` marker right after the first payoff, 25–50% of the way through the spoken words, followed by one line of 20 words or fewer from `templates/SUBSCRIBE_BEAT_LINES.md`:
  - no numbers, no stock phrases ("like and subscribe", "hit the bell");
  - rotate the lines;
  - the picture keeps moving under it.

  `gate:episode` fails a script without exactly one valid beat.
- **No goodbye and no second ask** ("in conclusion", "thanks for watching", "like and subscribe"). The last spoken line hands off to the next film ("Next, Orbit falls into Jupiter.") and the end screen shows it.
- **Layout:** every scene carries `[VISUAL MUST: …]` and `[TEACH: …]`. Only the Orbit beats carry `[ORBIT ACTS: …]`. The gate flags more than 2 Orbit beats.
- **Gates (both must pass before any voice or picture spend):**
  ```bash
  cd 07_Content-Ops && npm run review:script -- --file <script.md>        # 90 or more
  npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>       # PASS
  ```

### Short (22–27 s, about 55–65 words)

- **Two lines, then one hard fact.** Line 1 (5–7 words) is the familiar thing in danger, said in the first second. Line 2 is what they get if they stay.
- **The first two seconds** (`FAMILIAR_DANGER_STRATEGY.md` → *The first two seconds*):
  1. start mid-action;
  2. the named thing is on screen at frame 0, moving;
  3. the first words are the claim;
  4. a visible change by about 1 s, with a sound effect on frame 0;
  5. a hook caption on frame 0 (2–4 words, cap height about 8–10% of frame);
  6. Orbit arrives about a second later, caught in the danger.
- **The promoted film's exact live title** is on screen at 9–14 s.
- **The last 4 s** return to the opening picture so the Short loops.
- **The spoken end line depends on the test week** (the week-2 test drops "Watch the full film"). When the film is named, use its exact live title.
- **Captions** run the whole way.
- The long-form script reviewer caps Shorts below 90. **Don't pad a Short to chase it.**

## 4. Voice

- **ElevenLabs "Ben Orbit Narrator" only.** Voice id `kDch6ACCIpqgQ0NsU9kk`.
- **Settings:** model `eleven_v3`, stability 0.34, similarity 0.78, style 0.42, speed 1.04, speaker boost on. Import from `04_Audio/tools/orbit_voice.py`. Week 3 of the test runs about 10% faster.
- **British** spelling and pronunciation. Warm, calm authority, never trailer voice.
- **VO before picture.** Speech around −19 to −28 dB mean. **A silent or stripped narration never ships.**
- Never use a video model's own speech as VO.

## 5. Picture

**Home: Google AI Studio.**

| Job | Tool |
|---|---|
| World plates | **Veo** (Fast by default; one Quality hero if it earns the thumbnail) |
| Orbit moving | **Omni, only for Orbit** |
| Stills / boards | AI Studio image |

No Kling, Seedance or ElevenLabs Image & Video.

- **Stills first:** one open still, two science plates, one Orbit reference. Then 2–3 Veo Fast money shots (about 8 s). Never Omni the whole film. Never Omni world B-roll.
- **Picture matches the sentence.** If the line names Jupiter, the shot is Jupiter; one craft if the line says one craft. Mute the VO and the beat should still read. When picture and VO disagree, the picture is wrong.
- **Silent picture.** Mute or strip Veo/Omni baked audio (`generate_audio=False`, and strip on download). No readable text or logos in generated plates. Text is added in the edit.
- **Never** reuse a cutscene inside one film, loop scenery to pad, slow-mo stretch (`setpts` > 1×), freeze-pad, or Ken-Burns a text card. A Short's first/last-frame loop is intended, not padding.
- **Clean vacuum:** near-black space, few pinpricks.
- **Environment honesty:** no bubbles in vacuum; water SFX only underwater.
- **Ocean or shore POV:** no Earth globe in the sky. One Earth and one Moon, or one Moon only. Check a mid-plate frame, not just the first and last.
- **Frame sizes** (`YOUTUBE_FRAME_SIZES.md`): long 1920×1080 MP4; Short 1080×1920; long thumbnail file 1280×720.

## 6. Orbit (character lock)

- **Canonical still:** `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (plus `…-v01.png`). Never use anything under `_Rejected/`.
- **Model:**
  - matte orange floater, no legs;
  - one large black curved visor that is the face, with two cream eyes with dark pupils;
  - stubby arms with dark three-finger hands;
  - one antenna with a glowing tip;
  - exactly one soft underside glow.
- **Hard rejects, regenerate:**
  - two Orbits, or a second face on the back;
  - blank white eyes, no visor, slit LEDs;
  - legs, white belly, glowing yellow belly;
  - text on the body;
  - twin or side thrusters;
  - a melted or void face, a generic toy robot.
- **When Omni is used:** attach the identity still and a composition start frame at the right scale. Spot-check the start, middle and end of each take. Archive rejects as `_rejected_*` and bump `v0N`.
- **Dosage:**
  - Longs: 1–2 beats, and Orbit acts in the scene (turns, tips, dives), never parked as wallpaper.
  - Shorts: never at frame 0; arrives at about 1 s, caught in the danger.
  - Thumbnails: never, until a Test & Compare on a long with more than 1,000 impressions says otherwise.

## 7. Assembly and technical checks

- **Normalise every input to 1920×1080 stereo before concat.** Probe after: audio and video durations must match.
- **Remint = picture only.** Take video from the remint and audio from the original part (`-map 0:v:0 -map 1:a:0`). Never `-c copy` a remint's own audio.
- **Chapter cards:** a soft starfield/gradient card (never a flat black box), about 1.5 s breath lead-in, music continuing underneath.
- **End hold:** at least 15–20 s of slow picture after the last line. Music fades over about 10 s, picture fades to black over the last 2 s. **A silent hold fails.**
- **Bed parity** across parts: about −20 dB mean under VO.
- **Large file transfers:** chunk ≤500 KB and verify the sha256.
- **Subscribe cue:** under the `[SUBSCRIBE BEAT]` line, a 4-second subscribe cue in the lower-right corner (small button, no sound louder than the VO) over the moving picture. Orbit may nod or point toward it in-scene. Never a full-screen card.
- **Export** to `09_Final-Export/<slug>_broadcast_v0N.mp4`.
- **Shorts gate on every export:**
  ```bash
  python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
  ```
  - It fails on: no narration or near-silence; Orbit at 0 s; an opening within 10 dHash bits of any Short within 14 days of the air date; 40 s or longer.
  - It warns on: a still-looking first second.
  - Treat a warning as a re-cut of the opening.
  - After upload, register the Short: `gate_shorts_open.py add --id … --date … --title … --file <mp4> --status scheduled`.
- **Watch it once on a phone with the sound on** before it goes anywhere.

## 8. Titles and thumbnails

Follow `THUMBNAIL_AND_TITLE_RULES.md`:
- one of the six title shapes; no hedged claims, hashtags, suffixes or repeat titles;
- thumbnails of 2–4 words, readable at 168×94, adding to the title rather than repeating it;
- no Orbit.

Tools:
- **Builders:** `tools/build_melodysheep_long_thumbs_v01.py` (long), `tools/build_yellow_white_short_thumbs_v04.py` (Short cover, 1080×1920, centre-safe for the 16:9 crop).
- **Check:** `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb> --out <sheet>`.
- **Plate:** the strongest frame from the film's own master. If none works, an AI Studio still with no text in it. Text always comes from the builders, never from AI.
- **Longs:** 3 variants in Studio Test & Compare. Don't judge CTR under about 500 impressions.

## 9. Upload and Studio finish

1. **Upload through the Data API package:**
   `cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> [--dry-run]`
   (manifest: `templates/YOUTUBE_PACKAGE_MANIFEST.json`).
   - Upload private, with `publishAt`.
   - Set `privacyStatus` and `madeForKids` explicitly.
   - Altered/synthetic content: **yes**.
2. **Long:**
   - normal publish, Sunday 18:00, **no Premiere** until subscribers are in the hundreds;
   - description: opens on the real subject, then chapters, then sources;
   - Test & Compare with 3 thumbs;
   - end screen: the best related long + Subscribe;
   - captions: Studio auto-sync from the VO script;
   - one pinned comment: the film's open question plus a thank-you with the subscriber milestone (no number under 10). Post it with `npx tsx --env-file=.env scripts/update-pinned-comment.ts --create --video <id> --question "…?"` (records it in `PINNED_COMMENTS.json`), then pin it in Studio. The API can't pin.
3. **Short:**
   - desktop Studio **Related video** → the long that Short promotes. This is the only Short → long link. Set it once the long has an id.
   - no new pinned comments;
   - zero `/go/` links;
   - a custom cover.
4. **One video = one upload.**
   - Never swap the file on an existing id, and never re-upload an idea that already went public.
   - A recut gets a new id. The old one goes private, never deleted.
   - Fix problems **before** upload.
5. **Title-only changes:** `07_Content-Ops/scripts/retitle-videos.ts` (keeps the description, tags and schedule).
6. **Studio-only jobs** (no API) go through the desktop Studio CDP scripts:
   - Related video, Test & Compare, end screens and covers;
   - pattern: `scripts/apply_yellow_white_v04_thumbs.py`;
   - Chrome launcher: `audits/start_studio_chrome_cdp.sh`;
   - image-only inputs; never Replace, never `thumbnails.set`.
7. **Buffer mirror** (§12): `youtube:package` schedules the Instagram, Facebook and Threads posts itself. Check the `buffer` block in the result. Same step, same sign-off: Ben's OK to upload covers the Buffer posts.

## 10. Measure

- **Every Monday at 07:47 UTC,** a routine runs `tools/weekly_public_audit.py` and puts `audits/weekly/<date>/REPORT.md` on main.
- **After 48 h:** add stayed-to-watch from Studio for each Short to `could-orbit-survive/TEST_LOG.md`.
- **KPI:** Shorts stayed-to-watch at 48 h. The 10 Sep baseline is 31.7%; aim for more than 45%, then 60%.
- **Longs:** impressions, CTR (4–7% band once past about 500 impressions), average % viewed (about 50%).
- **A weak Short is a result, not a re-upload.**
- **Every Monday, after the report:**
  - refresh the pinned comments with `cd 07_Content-Ops && npx tsx --env-file=.env scripts/update-pinned-comment.ts` (dry run first). It only edits text, and only when the milestone changed;
  - in Studio, check each new long's retention graph at the subscribe beat. If more than about 2–3 points drop away there compared with the surrounding slope, shorten or move the beat in the next film's script.

## 11. Affiliate (longs only)

- A `/go/` link only when **that film names the product** in VO or on screen. Topic fit isn't enough.
- **Limits:** one product per film, placed late, after the wonder line, not a shop read.
- **Link:** `https://orbit-content-ops.vercel.app/go/{slug}` only, in the long's description, under `If you want to go further.`
- **Last line of the affiliate block:** `Some of these links are affiliate links. We only share things we'd still point you to with no commission.`
- **Shorts:** zero links.
- Never invent ASINs. Never commit the Amazon tag.
- Details: `docs/AFFILIATE_MONETISATION_SYSTEM.md`.

## 12. Social: Buffer mirrors YouTube

Set 27 Sep 2026. **Buffer is the only way anything reaches social.** The old Mac LaunchAgents and Chrome posting scripts are in `_archive/00_Brand/Channel-Setup/{Meta,Threads,TikTok,social}/`, and the ops app's worker refuses social jobs.

**The rule:** every video uploaded and scheduled on YouTube gets the same post in Buffer on Instagram, Facebook and Threads, **for exactly the time it goes public on YouTube.** It uses the same title, the description's opening paragraph and the tags as hashtags, all read from the live YouTube record, never retyped.

| YouTube | Instagram | Facebook Page | Threads |
|---|---|---|---|
| Short | Reel (the mp4), frame 0 as cover, AI label on | Reel (the mp4) | Video (the mp4) |
| Long | The thumbnail as an image post, "New film on YouTube. Link in bio." | YouTube link card | YouTube link card |

Hashtags: 5 on Instagram, 3 on Facebook, 1 on Threads, taken in order from the YouTube tags. Links are stripped from the caption; a long's link rides on the card.

**Automatic (from 27 Sep 2026): uploading is the whole job.**
- **At upload.** `npm run youtube:package` finishes a live upload, then puts the Short's mp4 (or the long's thumbnail) on the public Vercel Blob store. It reads the video back from YouTube and schedules the three Buffer posts through the Buffer API. For a Short, the long is the package's `relatedVideoId`; pass `--standalone` for a Short with no long. The upload result JSON has a `buffer` block. A Buffer problem never fails the upload: it prints "Buffer mirror incomplete" with the reason.
- **Every day at 07:00 UK** (06:00 UTC), the ops app's `/api/cron/buffer-check` compares Buffer with YouTube. A moved time moves the Buffer posts, and a video that's no longer going public has its posts deleted. Its log also lists scheduled uploads that were never mirrored (for example, ones uploaded by hand in Studio).
- **Anything uploaded another way**, or a re-run: `cd 07_Content-Ops && npx tsx --env-file=.env scripts/buffer-mirror.ts mirror --video <id> --long <longId> --media <short.mp4>` (Short), or `mirror --video <longId> --thumb <thumb.jpg>` (long). `plan` instead of `mirror` shows what it would do and changes nothing.
- **Straight after a Studio change**, don't wait for 07:00: `buffer-mirror.ts check`.
- What was posted is kept in the ops database (table `BufferMirrorPost`). The Mac and Vercel share it, so each video goes out once per channel.
- **Fallback without the API key:** `plan` saves `social/buffer-plans/<id>.json`. Send each action through the Buffer MCP exactly as written, then run `buffer-mirror.ts record --video <id> --channel <c> --post-id <bufferId>` (or `--deleted`).

**It refuses:**
- a Short that goes public before its long;
- a video public for more than a day (back catalogue needs Ben's OK, then `--allow-late`);
- a time less than 10 minutes away (wait until it's public, then `mirror`: it shares now);
- a video with no go-public time;
- a file it can't host at a direct public URL (Buffer fetches media when the post goes out; no share links, no signed URLs).

It never uploads the file for a video it refuses. If one channel fails, the others still go out, and the failure is reported.

**Never:**
- TikTok. It stays paused (account ban) and isn't connected in Buffer. Don't connect it until Ben lifts the pause.
- A post from Buffer's queue slots. Always `customScheduled` at the YouTube time, or `shareNow` once it's public.
- A Buffer post edited by hand to a different time from YouTube.

**One-time setup:**
1. On the posting Mac, stop the old jobs:
   `for a in dev.orbit.meta-live-shorts dev.orbit.threads-live-shorts dev.orbit.live-longs-social dev.orbit.tiktok-live-shorts dev.orbit.tiktok-reupload-missing; do launchctl bootout gui/$(id -u)/$a 2>/dev/null; rm -f ~/Library/LaunchAgents/$a.plist; done`
2. In Buffer, connect the Instagram (business, linked to the Page), Facebook Page and Threads accounts. No TikTok. Put the organization id and the three channel ids in `social/BUFFER_CHANNELS.json` (from `get_account` and `list_channels` in the Buffer MCP). Ids aren't secret.
3. `07_Content-Ops/.env` on the upload Mac must hold the real values: `DATABASE_URL` (Neon, `postgresql://…`), `ORBIT_TOKEN_ENCRYPTION_KEY`, `GOOGLE_CLIENT_ID`/`SECRET`, `BUFFER_API_KEY` (Buffer → Settings → API) and `BLOB_READ_WRITE_TOKEN`. Ben types these in himself. Never paste them into chat, print them, or commit them.
4. Vercel, project orbit-content-ops:
   - connect a **public** Blob store (this adds `BLOB_READ_WRITE_TOKEN`);
   - add `BUFFER_API_KEY` and `CRON_SECRET` (any long random string) to Production;
   - redeploy. The deploy creates the `BufferMirrorPost` table and turns on the daily job.
5. Optional: the Buffer MCP (`.cursor/mcp.json`, OAuth) for looking at the queue from Cursor, and for the fallback.

## 13. Ben signs off

Stop and wait for Ben's OK at each of these points:
1. topic;
2. long script (after it reaches 90);
3. Short scripts;
4. voice (listen);
5. picture (QA/UAT on the moving cut, never stills);
6. thumbnails;
7. anything that goes public.

Docs-only PRs may merge. Video-cut PRs wait for Ben's UAT.
