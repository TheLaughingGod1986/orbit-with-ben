# Archived from 05_Analytics/kanban/board_site/build.py under J2464 (row F-02a: retired /classic board).
PAGE = HERE.parent / "studio_kanban.html"

FOOTER = ('<footer><details><summary>Data sources and refresh</summary>This board updates itself. The Mac mini rebuilds its data from <span class="mono">main</span> of both '
          'repos whenever a job in the queue moves (claimed, a step done, done, blocked, released) and checks every minute, and pushes it only '
          'when something changed (<span class="mono">scripts/board_publish.py</span> → branch <span class="mono">board-data</span>). '
          'This page re-reads it every minute; the time at the top is the last real change. <b>HOS</b> comes from '
          '<span class="mono">00_Brand/Channel-Setup/PIPELINE.json</span> in history-of-science; <b>OWB</b> from each film\'s '
          '<span class="mono">02_Video-Projects/&lt;film&gt;/status.json</span>, the job queue and '
          '<span class="mono">05_Analytics/kanban/film_briefs.json</span> in orbit-with-ben ("chief" is shown as Grok). '
          'Your ticks are saved straight away with your board link; the Mac mini picks them up within about a minute. '
          'YouTube numbers: <a href="/tracker">Channel Tracker</a>. Studio app: <a href="/">/</a> · video board: <a href="/board">/board</a>.</details></footer>')

RELEASE_RECORDS = {}
for status_file in (ROOT / "02_Video-Projects").glob("*/status.json"):
    film = json.loads(status_file.read_text()).get("film", "")
    receipt = release_record(film)
    if receipt:
        RELEASE_RECORDS["OWB:" + film] = receipt

PATCHES = [
    ("const RELEASE_RECORDS = {};", "const RELEASE_RECORDS = " + json.dumps(RELEASE_RECORDS).replace("</", "<\\/") + ";"),
    ('<div class="sub" id="asof">Loading…</div>',
     '<div class="sub" id="asof">Loading…</div><div class="sub"><a href="/board" style="color:inherit">Video board →</a> · <a href="/tracker" style="color:inherit">Channel Tracker →</a></div>'),
    ("dbApi = db;", "dbApi = db.canWrite===false ? null : db;"),
    ('t.textContent = `Updated by the studio agent · ${fw(fromDb.hosAt || fromDb.owbAt)}`;',
     't.textContent = `Last change ${fw((window.__boardData||{}).dataChangedAt || fromDb.hosAt || fromDb.owbAt)} · checks every minute`;'),
    ('bits.push(`HOS board updated ${fd(pd(data.updated))} by ${data.updated_by||"—"}`);',
     'bits.push(`HOS updated ${source==="db"&&fromDb.hosAt?fw(fromDb.hosAt):fd(pd(data.updated))} by ${data.updated_by||"—"}`);'),
]


def build_classic(out: pathlib.Path) -> None:
    html = PAGE.read_text()
    for old, new in PATCHES:
        if html.count(old) != 1:
            sys.exit(f"build: expected one `{old[:60]}…` in studio_kanban.html; the page changed, update PATCHES")
        html = html.replace(old, new)
    start, end = html.find("<footer>"), html.find("</footer>")
    if start < 0 or end < start or html.count("<footer>") != 1:
        sys.exit("build: expected one <footer> in studio_kanban.html")
    html = html[:start] + FOOTER + html[end + len("</footer>"):]
    marker = "\n<script>\n"
    if html.count(marker) != 1:
        sys.exit("build: expected one bare <script> line in studio_kanban.html")
    html = html.replace(marker, "\n<script>\n" + (HERE / "shim.js").read_text() + "</script>" + marker, 1)
    end = "</script>\n\n</body></html>"
    if html.count(end) != 1:
        sys.exit("build: expected the page to end with its script, then </body></html>")
    html = html.replace(end, "</script>\n<script>\n" + (HERE / "live.js").read_text() + "</script>\n\n</body></html>")
    (out / "classic.html").write_text(versioned_page(html))
    print(f"built {out / 'classic.html'} ({len(html):,} bytes)")
