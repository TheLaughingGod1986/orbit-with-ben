// J2798: real-browser traffic measurement against the real API and a local board fixture.
// node scripts/board_updates_browser_measure.cjs <built-site> <board-fixture.json> <result.json>
// Uses installed Chrome. Runs ten idle minutes, then ten minutes containing one fixture film change.
// No live film, approval store, network service or channel state is changed.
const http = require('http'), fs = require('fs'), path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const {execFileSync} = require('child_process');

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
  let board = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  let history = null;
  const files = {'board.json': JSON.stringify(board), 'tracker.json': fs.readFileSync(path.join(__dirname, '../05_Analytics/dashboard/data.json'), 'utf8'), 'heartbeat.json': '{}'};
  function publish(next) {
    const input = JSON.stringify({board:next, previous:board, history});
    history = JSON.parse(execFileSync('python3', ['-c', 'import sys,json;sys.path.insert(0,"scripts");from board_publish import updates_payload;x=json.load(sys.stdin);print(json.dumps(updates_payload(x["board"],x["previous"],x["history"],"tracker")))'], {input, cwd:path.join(__dirname,'..'), encoding:'utf8'}));
    board=next;files['board.json']=JSON.stringify(board);files['updates.json']=JSON.stringify(history);
  }
  publish(structuredClone(board));
  const world = { private: false, head:HEAD };
  const answer = (status, body) => ({ ok: status >= 200 && status < 300, status, json: async () => JSON.parse(body), text: async () => body });
  globalThis.fetch = async (url, init = {}) => {   // only api/data.js calls this: its reads of GitHub
    const auth = ((init.headers || {}).authorization || '') === 'Bearer ' + TOKEN;
    if (world.private && !auth) return answer(404, '{}');
    if (/^https:\/\/raw\.githubusercontent\.com\//.test(url)) return answer(200, files[url.split('/').pop()] || '{}');
    if (/git\/ref\/heads\/board-data$/.test(url)) return answer(200, JSON.stringify({ object: { sha: world.head } }));
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

  const browser = await chromium.launch({channel:'chrome'});
  const result = {};
  for (const route of ['/', '/tracker']) {
    const context = await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});
    const page=await context.newPage(), cdp=await context.newCDPSession(page), rows=[], urls={};
    await cdp.send('Network.enable');
    cdp.on('Network.requestWillBeSent',e=>{urls[e.requestId]=new URL(e.request.url).pathname;});
    cdp.on('Network.loadingFinished',e=>rows.push({at:Date.now(),bytes:e.encodedDataLength,url:urls[e.requestId]}));
    const start=Date.now();await page.goto(base+route);
    await page.waitForFunction(route==='/' ? "!!document.querySelector('#view .card, #view .panel, #view h2')" : "document.getElementById('livestamp').textContent.includes('Latest saved')",{},{timeout:30000});
    result[route]={firstRenderMs:Date.now()-start,rows};
  }
  const start=Date.now();
  for(let minute=1;minute<=20;minute++) {
    await new Promise(done=>setTimeout(done,60000));
    const next=structuredClone(board);next.publishedAt=new Date().toISOString();
    if(minute===10) next.tracker.videos[0].title += ' (browser fixture change)';
    publish(next);world.head=minute.toString(16).padStart(40,'0');
  }
  await new Promise(done=>setTimeout(done,3000));
  for(const row of Object.values(result)) {
    row.idleBytes=row.rows.filter(x=>x.at>=start && x.at<start+600000).reduce((sum,x)=>sum+x.bytes,0);
    row.oneFilmChangeBytes=row.rows.filter(x=>x.at>=start+600000).reduce((sum,x)=>sum+x.bytes,0);
  }
  fs.writeFileSync(process.argv[4],JSON.stringify(result,null,2));
  await browser.close();server.close();
  console.log('Ten-minute idle and one-film-change captures complete.');
})().catch(e => { console.error(e); process.exit(1); });
