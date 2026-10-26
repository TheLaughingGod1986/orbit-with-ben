# Studio Kanban

**Studio videos (Ben, 26 Oct 2026):** https://studio-kanban.vercel.app uses the per-video column design:
Upcoming, In progress, Changes requested, Ready for OK, Approved on its way, and Done on YouTube.
Channel and Longs/Shorts filters sit above the models and live work panel. One card represents each video,
with play links and the existing approval controls. Restored at Ben's request from the screenshots of this layout.
The page lives in `board_site/tracker_app.js` and `video_tracker.html`; live data still comes from `board.json`.
The earlier swim-lane board remains at `/classic`.

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

## Ready for OK = jobs waiting on Ben (25 Oct 2026)

A card is in **Ready for OK** for every job that sets `awaits_ben` (`python3 scripts/jobs.py awaits <id> --what ... --file
"<OWB UAT/...mp4>" --version vNN --due "YYYY-MM-DD HH:MM" [--card HOS:007] [--add] --agent chief --git`). Shorts that aren't
uploaded get their own card; `--card` moves an existing long's card. Each card has a signed Play link and its deadline.
Approve posts `[Ben] OK <id> vNN (...)` plus "Release held job <id>" on #264 / HOS #180. `scripts/board_check.py` runs
every 5 min, started by board_publish.py. It writes `~/_desk/state/board/board_check.json` (`ok`, `problems`, `cards`)
and `~/_desk/state/board/BOARD_CHECK_FLAG` (`OK <time>` / `FAIL <time>: ...`). A repeat failure posts one
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
