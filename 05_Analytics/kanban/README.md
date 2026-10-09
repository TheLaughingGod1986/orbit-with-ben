# Studio Kanban

Live board: https://studio-kanban.vercel.app (self-updating; see `scripts/board_publish.py` and `board_site/build.py`).
The page is `studio_kanban.html`; its data is built by `scripts/kanban_snapshot.py --db-out` and published by the Mac
mini to the `board-data` branch after every job change and every 5 minutes.

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
