# Studio Kanban

**Videos tab (live, Ben 7 Nov 2026):** https://studio-kanban.vercel.app → **Videos** shows nine exclusive swim lanes:

**Backlog → To do → In progress → QA → UAT → Passed → Scheduled → Live → Post-live.**

The 3×3 chips are **computed** from tracker / job / YouTube state (`scripts/video_tracker.py` + `board_site/studio_app.js` `videoLane`) — not Chief dragging cards by hand or by air date. Ben only acts in **UAT** (Approve → **Passed**, ready to schedule; Request changes / notes → **In progress** for the agents). Every other lane is agent-run. Planned Shorts on **Backlog** are board-only placeholders (HOS 4 / Orbit 2 per upcoming long, including undated Orbit backlog longs) with no invented YouTube ids or air dates; parents that already have uploaded/live Shorts do not get extras. Full workflow + locked cadence slots: `AGENTS.md` → **Videos tab**. Media paths: `AGENTS.md` → **Film folders on the NAS** (working media on `/Volumes/data/studio-live`; uploads stay Mini-only; MacBook harvest/assembly only when that film's studio-live folder exists).

Channel and Longs/Shorts filters sit above the models and live work panel. One card represents each video, with play links and the existing approval controls. Live data comes from `board.json` (`tracker` section from `scripts/video_tracker.py`; the UI remaps tracker lanes to the nine Videos lanes in `board_site/studio_app.js`).

Approve / Request changes still post `[Ben] OK/changes …` via `/api/checks` (OWB desk issue **#264**, HOS **#180**).

**One tap, no code (25 Oct 2026, Ben: "Just need to approve no need for code"):** the page never asks for a code. Ben's
phone is recognised by an HttpOnly cookie `studio_ben` (400 days, renewed on every board load; `board_site/benauth.js`).
It's set once by a one-time "link this phone" link from `python3 scripts/board_pair_link.py` on the Mini (written to
`~/.config/studio-kanban/ben_pair_link`, 0600, never printed; works once, expires in 7 days; send it only in Ben's private
chat). A phone that still has the old `#k=` board code upgrades to the cookie by itself. Anyone else gets 401 and nothing
posts. Test without approving: `POST /api/checks {"id": "...", "doc": {...}, "dryRun": true}` returns the line it would post.
Revoke every linked phone by rotating `BOARD_KEY` in Vercel.

Job and video progress (18 Oct 2026, classic board): the Now box and video rows use the same live queue and
channel-qualified video links. Workers record the chosen video(s) with `jobs.py progress ... --films HOS:006` and a
concrete `--note` after each step.

Live data: `scripts/kanban_snapshot.py --db-out` → `scripts/board_publish.py` → `board-data` branch (`board.json` now
includes a `tracker` section). Page deploys are separate (Chief after review).

## UAT = jobs waiting on Ben (25 Oct 2026; lane name live 7 Nov 2026)

A card sits in Videos → **UAT** for every job that sets `awaits_ben` (`python3 scripts/jobs.py awaits <id> --what ... --file
"<OWB UAT/...mp4>" --version vNN --due "YYYY-MM-DD HH:MM" [--card HOS:007] [--add] --agent chief --git`). Shorts that aren't
uploaded get their own card; `--card` moves an existing long's card. Each card has a signed Play link and its deadline.
**Approve** moves the film to **Passed** and posts `[Ben] OK <id> vNN (...)` plus "Release held job <id>" on #264 / HOS #180.
**Request changes** / notes send it back to **In progress**. `scripts/board_check.py` runs every 5 min, started by
board_publish.py. It writes `~/_desk/state/board/board_check.json` (`ok`, `problems`, `cards`) and
`~/_desk/state/board/BOARD_CHECK_FLAG` (`OK <time>` / `FAIL <time>: ...`). A repeat failure posts one
`[Chief] board-check` note on #264.

## Deploying the page (studio-kanban has no Git link)

The Vercel project `studio-kanban` (prj_vZED3mMIu9NfPnBdoME18ALtfVNk, team bens-projects-11c93b15, Hobby) is **not
connected to GitHub** (checked 25 Oct 2026), so a merge never auto-builds it. That is on purpose: main takes dozens of
`jobs:` pushes a day, and on Hobby every triggered build, ignored or cancelled ones included, counts toward the
100-a-day deploy cap (the same reason `orbit-content-ops` has git auto-deploy off). Data needs no deploy. Only a change
under `board_site/` or the pages it builds does. After such a merge, deploy main by hand at its merge sha:

- **Vercel MCP** `create_deployment`: `{"teamId": "team_UPErYpfb3ww71LYTIWUoKvcH", "requestBody": {"name": "studio-kanban",
  "project": "studio-kanban", "target": "production", "gitSource": {"type": "github", "org": "TheLaughingGod1986",
  "repo": "orbit-with-ben", "ref": "main", "sha": "<merge sha>"}, "projectSettings": {"framework": null,
  "rootDirectory": "05_Analytics/kanban/board_site", "installCommand": "npm install", "buildCommand": "python3 build.py",
  "outputDirectory": "dist", "sourceFilesOutsideRootDirectory": true}}, "forceNew": "1", "skipAutoDetectionConfirmation": "1"}`.
  **Always pass `projectSettings`.** Without them Vercel builds the repo root, finds nothing to serve, and the live site
  returns 404 on every path. That happened on 25 Oct 2026 08:54 London (dpl_8Ca8ziAEVP6s9FGrsxHmrH6CgoAE). The fix was
  redeploying with the settings above (dpl_8dxxvQKf9cic7UqvR1ND5Ko5ZdNg, 200 again by 08:57).
- **CLI** (where `vercel` is signed in): `cd 05_Analytics/kanban/board_site && npx vercel deploy --prod --scope bens-projects-11c93b15`
  (uses `.vercel/project.json`).

Then check the deployment is READY and that `curl -s -o /dev/null -w '%{http_code}' https://studio-kanban.vercel.app/` prints 200.

## Channel Tracker web app (Ben, 10 Oct 2026)

https://studio-kanban.vercel.app/tracker is the Channel Tracker (`05_Analytics/dashboard/template.html`, the page behind
`dashboard.html`) as a phone web app on the same site: "Add to Home Screen" opens it full screen (`board_site/tracker.webmanifest`,
icons in `board_site/static/`). The board header links to it and it links back.

- **Data:** read at runtime from `tracker.json` on the `board-data` branch, which is main's
  `05_Analytics/dashboard/data.json` byte for byte. `scripts/board_publish.py` puts it there: the 06:40 snapshot job
  (`07_Content-Ops/launchd/analytics-snapshot.sh`) runs it right after pushing the new snapshot to main, and the 5-minute
  launchd run catches any other change. A broken or missing data.json on main keeps the last good copy.
- **Page:** `board_site/build.py` builds `dist/tracker.html` from the template (small checked patches, like the board) plus
  `board_site/tracker_loader.js`. It shows this phone's saved copy at once, then the live file (reloading once if newer),
  and re-checks when you come back to it and every 15 minutes. With no network it shows the copy built in at deploy time
  and says so. Data never needs a redeploy; a template change does (the next routine redeploy of studio-kanban from main).

## Watch links (Ben, 9 Oct 2026)

Whenever the board has a cut for Ben to watch, his card and the "Ready for you to check" card show a **▶ Watch vNN**
button that opens it on his phone. `kanban_snapshot.py` picks one link per film (`board/briefs.watch["OWB:026"]`):

1. **Explicit** `watch: {"url": ..., "version": "v05d", "label": "optional"}` on the film: top level of OWB
   `02_Video-Projects/NNN_*/status.json`, the film in HOS `00_Brand/Channel-Setup/PIPELINE.json`, or the film's note in
   `film_briefs.json`. Allowed: `https://youtu.be/`, `https://www.youtube.com/`, `https://studio.youtube.com/`,
   `https://www.icloud.com/` (an iCloud share link Ben made). Use it only when 2 and 3 can't find the right cut.
2. **The film's long upload** in `00_Brand/Channel-Setup/social/UPLOADS.json` (private or scheduled YouTube video, plus a
   Studio link), unless a newer cut is in the UAT folder.
3. **The newest cut in iCloud Drive**: `OWB UAT/NNN_*_vNN*.mp4`, or `HOS UAT/NNN_*/…_vNN*.mp4` (Shorts and stills
   folders skipped); the `*_PHONE.mp4` copy of that version when there is one. It opens in the Files app
   (`shareddocuments://` link): the file is already in Ben's iCloud Drive, so nothing is shared or uploaded.

**For whoever hands Ben a cut (Cursor, Codex, Claude, Grok):** put it in `OWB UAT` / `HOS UAT/<NNN_film>/` with the film
number first and the version as `_vNN[letter]` in the name (e.g. `026_NearestStar_v05_PHONE.mp4`), and set the film
note's `you` in `film_briefs.json` as usual. The button then appears by itself within a couple of minutes. Never upload or change
privacy just to get a link; a private upload counts only once the upload job has made it.

## Mobile Studio UAT outlook (PR #382)

Overview's **Next videos toward UAT** and each video detail read `tracker.videos[].production`,
created by `scripts/uat_outlook.py` from the same snapshot used for lanes. The Review tab
continues to use finished cuts explicitly awaiting Ben; forecast progress never grants approval.

`production` contains `asOf`, `milestones` (`id`, `label`, `state`, evidence, dependencies,
optional historical sample count/range), `completed`, `total`, and `eta`. Milestone percent is
an equal count of recorded completed/skipped stages, not a weighted estimate of film effort.
Unknown stages are shown explicitly. Task steps remain in Agent work and cannot complete a milestone.
The UAT graph is topic → script → sources → voice and shot plan → picture → edit and packaging
→ Chief QA. Upload and Ben's watch duration are outside the graph. QA must be recorded explicitly
as `stages.qa` with `state`/`status`; an edit job finishing cannot stand in for Chief approval.
Longs use their own source stages. Shorts and synthetic cards never inherit a parent long's completion.

Historical durations come from actual `doing` → `done` stage transitions in Git (up to 80
path-changing commits per film or HOS pipeline), including intervening review/rework. A stage
already doing in the oldest available snapshot has no observable start and supplies no sample.
Workers may record exact timezone-aware `startedAt` and `completedAt` stage boundaries. Rework
cycles are combined per film. Samples stay within channel/format and exclude the current film;
there must be at least three comparable films for every unfinished stage. HOS history is read
from the sibling `history-of-science` checkout; unavailable or shallow history fails closed.

ETA uses median–80th-percentile stage durations, subtracts time since a recorded stage start,
and takes the longest dependency path across parallel branches. Confidence is low with 3–9
observations per remaining stage, medium with 10+, never a calibrated probability. Unknown
queue start, incomplete external dependencies, blocked work, shared worker capacity, manual
Flow/operator timing, missing stage/job coverage, requested changes or overruns suppress the
numeric estimate and expose reasons. Nothing substitutes keyword estimates or planned air dates.
Forecasts older than 75 minutes or beyond their range require an update; even an unchanged board
SHA re-renders the age check. Older board payloads show “not published yet.”

Page and data roll out separately: deploy this PR as a **preview** for Chief review. After Chief
approves and merges, the Mini must run the updated snapshot/publisher before live milestones
appear; a page-only preview still reads the current production board, which may lack this field.
Do not publish fixture forecasts to `board-data` or deploy production before Chief approval.

Validation:

```bash
python3 -m unittest discover -s scripts -p 'test_uat_outlook.py' -v
node scripts/test_studio_app.cjs
python3 05_Analytics/kanban/board_site/build.py
python3 -m http.server 8765 --directory 05_Analytics/kanban/board_site/dist
# Separate shell, with Playwright installed and Chromium available:
node scripts/test_studio_uat_browser.cjs
# Optional: STUDIO_PREVIEW_URL=<preview> STUDIO_QA_SCREENSHOTS=<existing directory>
```

Browser QA intercepts board reads with producer-generated fixture forecasts, checks 360/390/1280px,
Overview → detail navigation, unavailable reasons and Review isolation, and refuses every write.

## Studio V2 presentation (follow-up to merged PR #382)

The detail page now leads with a compact video header, a milestone-count progress/forecast hero,
and the current blocking/active stage. A nine-stage segmented strip and native `<details>` rows
keep the original evidence accessible. Only the current stage opens initially. Open stages,
technical disclosures and keyboard focus survive live polling; routes and Review POST documents
are unchanged. Native summary controls expose their expanded state to assistive technology.

Overview prioritises finished cuts awaiting Ben, then production outlook and the pipeline. Agent
health and queue diagnostics follow. Videos retains channel/format and Working/Waiting/Backlog
filters, and adds credible-UAT, recorded-update, stage and blocked sorting within those groups.
Missing estimates retain their recorded relative order. Publisher `asOf` is never treated as a
meaningful video update time. Pending estimates have one primary explanation; diagnostic reasons
are available under “How this estimate works.”

Backward-compatible telemetry additions in `production`:

- Each milestone retains `state` and adds `displayState`, `awaitingApproval`, `owner`, `reviewer`,
  concise `summary`, `version`, related `jobs`, and original `source` note/reference/time fields.
  These are read-only presentation fields. A recorded approval hold keeps the milestone incomplete
  even when a related job says it is done. Completed task steps cannot complete a video milestone.
- `activeStages` prioritises recorded blockers/approval waits, dependency impact and the critical
  path. Unknown stages are not selected just because they come first. Without recorded ownership
  the UI says Unassigned; an unspecified reviewer is not silently called Chief.
- `partialEstimates` contains stage-only ranges where that running stage has sufficient comparable
  historical evidence, a recorded start and no unresolved local/manual/capacity constraints.
  They never replace `eta`, which remains unavailable if the full UAT path is unknown.
- Confidence also considers historical spread. Competing claimed work by the same agents suppresses
  calendar ranges, including partial ranges. Unknown queue starts continue to suppress full ETAs.
- HOS history discovery supports the publisher's real `board-wt/hos` checkout and `HOS_REPO`, as
  well as the historical checkout names. No milestones are inferred from generated-asset counts.

No source stage/job records, approvals, publishing dates, media visibility or generation are
modified. Older board payloads still render using their recorded stage evidence. Full V2 metadata
requires the normal Mini publisher after an approved merge, independently of the page deployment.
Screenshots and the validation record are in `docs/review/studio-v2/QA.md`.

## Studio V3 Overview

Overview uses `overviewModel`, `producingVideos`, `scheduledThisWeek` and `featureVideo` in the
existing app. The three statistics open `#review`, `#videos&view=producing`, and
`#schedule&view=week`. Existing tab/video/UAT routes continue to work. Scope links reset stale
Videos filters; user-selected filters still work within the producing scope.

Producing excludes Backlog, published/scheduled work, done cards and cuts ready for Ben. A shared
job cannot increase the video count; stable keys and explicit YouTube IDs deduplicate aliases.
The schedule statistic counts recorded schedules in the London Monday–Sunday calendar week,
not a rolling seven days or planned air dates. Schedule labels these definitions explicitly.

One featured card uses existing milestone counts and UAT forecasts, with deterministic readiness,
blocker, focus/priority and meaningful-progress fallbacks. Unknown timing stays pending. Agent
names require fresh job timestamps; status combines real work, freshness and availability rather
than Chief presence. All operational details remain under Agents, including the expandable queue.

Unchanged render output retains the existing DOM. The existing poll cadence and same-SHA network
shortcut remain; transient refresh errors retain loaded content and an initial failure shows an
automatic-retry message. V2 technical disclosures and UAT notes remain protected.

See `docs/review/studio-v3/QA.md` for definitions, before/after captures and executed tests.

### Overview active job card

Studio activity shows one deduplicated `claimed` job from the existing board, prioritising recorded
urgency and otherwise preserving publisher order. It includes the recorded agent, ID, current
action (or title), valid integer step counts and the existing task ETA estimate when its inputs
are available. Percentages are task steps only; missing/invalid counts produce no bar. Completed
reported steps do not leave a countdown. Long actions are shortened on the card and remain intact
in Agents. Additional active jobs are counted, and queued/on-hold totals remain in the footer.

`#agents&job=<encoded-id>` opens the queue, highlights the corresponding row and scrolls/focuses it
once on entry. Subsequent refreshes update the card without forcing repeated scrolling. The normal
board polling and all UAT/publishing behaviour are unchanged. Tests: `test_studio_app.cjs` and
`test_studio_activity_browser.cjs` cover active, idle, multiple, missing/invalid progress, supported
ETA, queue linking and refresh transitions; the existing tab/UAT and failure suites also pass.

### Blocker guidance

Current-stage and expanded milestone cards show source-backed reasons, recorded unblock actions,
job owner/reviewer, follow-up/overdue check time, last check and dependency status. Exact stage job
mappings take precedence over matching recorded references; otherwise video-level holds are clearly
labelled as having an unconfirmed stage link. Missing details stay explicit. A check time is not a
release ETA. Job links open the existing highlighted Agents record; no hold is released by the UI.
Original conditions/actions/notes remain available, and other video holds can be expanded. No
production record or ownership is rewritten. See `docs/review/studio-blockers/QA.md` for the real
OWB030 example and tests, including `scripts/test_studio_blockers_browser.cjs`.
