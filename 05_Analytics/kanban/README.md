# Studio Kanban

Live board: https://studio-kanban.vercel.app (self-updating; see `scripts/board_publish.py` and `board_site/build.py`).
The page is `studio_kanban.html`; its data is built by `scripts/kanban_snapshot.py --db-out` and published by the Mac
mini to the `board-data` branch after every job change and every 5 minutes.

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
note's `you` in `film_briefs.json` as usual. The button then appears by itself within 5 minutes. Never upload or change
privacy just to get a link; a private upload counts only once the upload job has made it.
