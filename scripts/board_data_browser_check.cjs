// The board in a real browser with GitHub's public file addresses blocked (J2532's done-when).
//
//   node scripts/board_data_browser_check.cjs <built site folder>
//
// Serves the built pages and the real api/data.js from this machine, with a stand-in for GitHub behind the function,
// and opens the three pages three ways: private and signed in, private and not signed in, public and not signed in.
// Prints one JSON line: for each way, what each page showed and every request a page made to GitHub directly
// (there should be none). scripts/test_board_data_api.py runs this and judges the line. Nothing leaves this machine.
const http = require('http'), fs = require('fs'), path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const dist = process.argv[2];
const SITE = path.join(__dirname, '../05_Analytics/kanban/board_site');
const TOKEN = 'browser-check-token', HEAD = 'd'.repeat(40);
const PAGES = { '/': 'index.html', '/ai': 'ai.html', '/tracker': 'tracker.html' };
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png',
  '.webmanifest': 'application/manifest+json', '.svg': 'image/svg+xml' };

(async () => {
  if (!dist || !fs.existsSync(path.join(dist, 'index.html'))) throw new Error('give the built site folder (build.py --out)');
  process.env.BOARD_KEY = 'browser-check-key';
  process.env.BOARD_GH_TOKEN = TOKEN;
  const data = await import(pathToFileURL(path.join(SITE, 'api/data.js')));
  const { makeSession } = await import(pathToFileURL(path.join(SITE, 'benauth.js')));

  // What "GitHub" holds: a real board.json shape with one film, the real tracker snapshot, a heartbeat.
  const board = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/ai_board.json'), 'utf8'));
  board.tracker = { videos: [{ key: 'OWB:019', channel: 'OWB', number: '019', title: 'Andromeda', type: 'long', lane: 'progress', jobs: [], youtube: null, air: '' }] };
  const files = { 'board.json': JSON.stringify(board), 'tracker.json': fs.readFileSync(path.join(__dirname, '../05_Analytics/dashboard/data.json'), 'utf8'),
    'heartbeat.json': JSON.stringify({ at: new Date().toISOString(), state: 'idle', why: ['no MacBook job waiting'], job: '' }) };
  const world = { private: true };
  const answer = (status, body) => ({ ok: status >= 200 && status < 300, status, json: async () => JSON.parse(body), text: async () => body });
  globalThis.fetch = async (url, init = {}) => {   // only api/data.js calls this: its reads of GitHub
    const auth = ((init.headers || {}).authorization || '') === 'Bearer ' + TOKEN;
    if (world.private && !auth) return answer(404, '{}');
    if (/^https:\/\/raw\.githubusercontent\.com\//.test(url)) return answer(200, files[url.split('/').pop()] || '{}');
    if (/git\/ref\/heads\/board-data$/.test(url)) return answer(200, JSON.stringify({ object: { sha: HEAD } }));
    const m = /contents\/([\w.]+)\?ref=/.exec(url);
    return m && files[m[1]] ? answer(200, files[m[1]]) : answer(404, '{}');
  };

  const server = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://localhost');
    if (u.pathname === '/api/data') {
      req.query = Object.fromEntries(u.searchParams);
      res.status = c => { res.statusCode = c; return res; };
      res.json = j => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(j)); return res; };
      res.send = b => { res.end(b); return res; };
      return data.default(req, res).catch(e => { res.statusCode = 500; res.end(String(e)); });
    }
    if (u.pathname === '/api/ref') { res.statusCode = 502; return res.end('{"error":"off for this check"}'); }   // the old way must not be needed
    if (u.pathname === '/api/checks') { res.setHeader('Content-Type', 'application/json'); return res.end('{"checks":{}}'); }
    const file = path.join(dist, PAGES[u.pathname] || path.normalize(u.pathname).replace(/^(\.\.[/\\])+/, ''));
    if (!file.startsWith(dist) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.statusCode = 404; return res.end('not found'); }
    res.setHeader('Content-Type', TYPES[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  });
  await new Promise(done => server.listen(0, '127.0.0.1', done));
  const base = `http://127.0.0.1:${server.address().port}`;

  const browser = await chromium.launch();
  const ways = { 'private, signed in': { private: true, signedIn: true }, 'private, not signed in': { private: true, signedIn: false },
    'public, not signed in': { private: false, signedIn: false } };
  const seen = {};
  const settled = (page, id, done) => page.waitForFunction(([i, d]) => new RegExp(d).test((document.getElementById(i) || {}).innerText || ''), [id, done], { timeout: 15000 })
    .catch(() => {}).then(() => page.locator('#' + id).innerText());
  for (const [name, way] of Object.entries(ways)) {
    world.private = way.private;
    data.forget();
    const context = await browser.newContext();
    const github = [];
    await context.route(u => !u.href.startsWith(base), route => route.abort());   // nothing but this machine
    await context.route(/^https?:\/\/(raw\.githubusercontent\.com|api\.github\.com)\//, route => { github.push(route.request().url()); route.abort(); });
    if (way.signedIn) await context.addCookies([{ name: 'studio_ben', value: makeSession(process.env.BOARD_KEY), url: base }]);
    const page = await context.newPage();
    await page.goto(base + '/#videos');
    const studio = await settled(page, 'view', 'To do|private|Could not load');
    await page.goto(base + '/ai');
    const ai = await settled(page, 'asof', 'checks every minute|private|Could not load');
    await page.goto(base + '/tracker');
    const tracker = await settled(page, 'livestamp', 'Latest saved snapshot fetched|private|Couldn.t reach');
    seen[name] = { studio, ai, tracker, github };
    await context.close();
  }
  await browser.close();
  server.close();
  console.log(JSON.stringify(seen));
})().catch(e => { console.error(e); process.exit(1); });
