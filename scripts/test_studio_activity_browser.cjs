const {chromium}=require('playwright'),assert=require('assert');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{for(const width of [375,390,430,768,1280]){
 const page=await browser.newPage({viewport:{width,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const now=new Date().toISOString();let sha='one';const job={id:'Jactive',by:'codex',status:'claimed',title:'Assemble film',remaining_action:'Finish the recorded edit',claimedAt:new Date(Date.now()-10*6e4).toISOString(),progress:{step:2,of:5,at:now}};
 const board={tracker:{videos:[]},models:{checkedAt:now,models:[]},owb:{jobs:[job,{...job,id:'Jsecond'},{id:'Jqueued',status:'open'},{id:'Jheld',status:'blocked'}]}};
 await page.route('**/*',r=>{const q=r.request(),url=q.url();assert.equal(q.method(),'GET');if(url.includes('/api/ref'))return r.fulfill({json:{object:{sha}}});if(url.includes('board.json'))return r.fulfill({json:board});if(url.includes('heartbeat.json'))return r.fulfill({json:{}});return r.continue()});
 await page.goto(process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8765');await page.locator('.active-job-card').waitFor();
 const text=await page.locator('.active-job-card').innerText();assert(text.includes('Codex is working')&&text.includes('Jactive')&&text.includes('Finish the recorded edit')&&text.includes('2 of 5 steps')&&text.includes('+1 other active job')&&text.includes('Task ETA:'));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(process.env.STUDIO_QA_SCREENSHOTS&&width===390)await page.screenshot({path:process.env.STUDIO_QA_SCREENSHOTS+'/active-job-390.png'});
 await page.locator('.active-job-card').click();const selected=page.locator('#job-Jactive');await selected.waitFor();assert(await page.locator('[data-disclosure="agent-queue"]').evaluate(e=>e.open));assert(await selected.evaluate(e=>e.classList.contains('selected-job')));
 await page.waitForTimeout(100);const box=await selected.boundingBox();assert(box.y<844&&box.y+box.height>0,'linked job scrolled into view');
 await page.locator('#nav').getByRole('link',{name:/Overview/}).click();job.progress={step:3,of:5,at:now};sha='two';await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await page.getByText('3 of 5 steps · 60%',{exact:true}).waitFor();
 delete job.progress;delete job.claimedAt;board.owb.jobs=[job];sha='three';await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await page.getByText('Task progress not recorded',{exact:true}).waitFor();assert.equal(await page.locator('.active-job-card [role="progressbar"]').count(),0);assert((await page.locator('.active-job-card').innerText()).includes('Task ETA unavailable'));
 board.owb.jobs=[];sha='four';await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await page.getByText('Studio waiting for next job',{exact:true}).waitFor();assert.equal(await page.locator('.active-job-card').count(),0);
 assert.deepEqual(errors,[]);await page.close();
}console.log('Studio activity browser QA OK: five widths, primary/multiple jobs, linked highlighted queue, live progress refresh, missing progress/ETA and idle; no writes or overflow');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
