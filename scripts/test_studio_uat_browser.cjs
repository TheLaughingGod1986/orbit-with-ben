// Run after board_site/build.py and start a static server. Network fixtures never write to the live board.
const {chromium} = require('playwright');
const {execFileSync} = require('child_process');
const assert = require('assert');
const path = require('path');
const root = path.join(__dirname, '..');
const production = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0, 'scripts')
from uat_outlook import PLAN,forecast
from datetime import datetime,timezone
now=datetime.now(timezone.utc)
v=dict(key='OWB:999',channel='OWB',type='long',lane='progress')
stages={key:dict(state='done') for key in PLAN}
stages['qa']=dict(state='doing',since=now.isoformat())
samples={('OWB','long','qa'):[(10,'OWB:001'),(20,'OWB:002'),(30,'OWB:003')]}
print(json.dumps(forecast(v,stages,[dict(id='JQA',stage='qa',status='claimed',by='chief')],samples,now)))
`], {cwd: root, encoding: 'utf8'}));
const video = {key: 'OWB:999', channel: 'OWB', number: '999', type: 'long', title: 'Preview milestone film', lane: 'progress', jobs: [], production};
const board = {tracker: {videos: [video,
  {...video, key: 'HOS:998', channel: 'HOS', title: 'Flow held film', production: {...production, eta: {state: 'unavailable', reasons: ['Manual Flow <operator> needs to act', 'Credit reset has no confirmed time']}}},
  {...video, key: 'OWB:997', title: 'Finished review film', lane: 'ready', readyFor: 'Ben', watch: {url: 'https://example.com/preview', version: 'v01'}},
  {...video, key: 'OWB:996', title: 'Older snapshot film', production: undefined}]},
  models: {checkedAt: new Date().toISOString(), models: []}, owb: {jobs: []}};
(async () => {
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', args: ['--no-sandbox']});
  const errors = [], writes = [];
  try {
    for (const width of [360, 390, 1280]) {
      const page = await browser.newPage({viewport: {width, height: 844}});
      page.on('pageerror', e => errors.push(e.message));
      await page.route('**/*', route => {
        const request = route.request(), url = request.url();
        if (request.method() !== 'GET') { writes.push(url); return route.abort(); }
        if (url.includes('/api/ref')) return route.fulfill({json: {object: {sha: 'fixture'}}});
        if (url.includes('board.json')) return route.fulfill({json: board});
        if (url.includes('heartbeat.json')) return route.fulfill({json: {}});
        return route.continue();
      });
      await page.goto(process.env.STUDIO_PREVIEW_URL || 'http://127.0.0.1:8765');
      await page.getByRole('heading', {name: /Next videos toward UAT/}).waitFor();
      assert((await page.locator('main').innerText()).includes('UAT in about'));
      assert((await page.locator('main').innerText()).includes('Older snapshot film'));
      await page.getByRole('link').filter({hasText: 'Preview milestone film'}).first().click();
      await page.getByRole('heading', {name: 'Production toward UAT'}).waitFor();
      assert((await page.locator('main').innerText()).includes('89%'));
      assert((await page.locator('main').innerText()).includes('Critical path: qa'));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `detail overflow at ${width}`);
      if (process.env.STUDIO_QA_SCREENSHOTS) await page.screenshot({path: `${process.env.STUDIO_QA_SCREENSHOTS}/studio-uat-${width}.png`, fullPage: true});
      await page.getByRole('link', {name: /Review/}).last().click();
      await page.getByRole('heading', {name: 'Review', exact: true}).waitFor();
      const review = await page.locator('main').innerText();
      assert(review.includes('Finished review film'));
      assert(!review.includes('Preview milestone film') && !review.includes('Flow held film'));
      await page.goto((process.env.STUDIO_PREVIEW_URL || 'http://127.0.0.1:8765') + '/#v=HOS%3A998');
      await page.getByRole('heading', {name: 'Production toward UAT'}).waitFor();
      assert((await page.locator('main').innerText()).includes('Manual Flow <operator> needs to act'));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `blocked overflow at ${width}`);
      await page.close();
    }
    assert.deepEqual(errors, []);
    assert.deepEqual(writes, []);
    console.log('Studio UAT browser QA OK: 360, 390, 1280px; producer data, detail, review isolation, no writes, no page errors');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
