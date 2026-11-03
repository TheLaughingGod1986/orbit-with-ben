// Source-backed blocker guidance and job navigation. Fixture writes are never sent to live services.
const {chromium}=require('playwright'),assert=require('assert');
const base=process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8765';
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{for(const width of [375,390,430,768,1280]){
 const p=await browser.newPage({viewport:{width,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));let sha='one';
 const ids=['topic','script','sources','vo','shots','picture','edit','thumbs','qa'];
 const edit={id:'edit',label:'Edit',state:'blocked',evidence:'d0b04b5e0',source:{ref:'d0b04b5e0'},jobs:[]};
 const job={id:'J1471',status:'blocked',stage:'',by:'codex',title:'Correct the opening',remaining_action:'Identify approved moving ISS footage, then correct and review the openings',after:'J1468',hold:{type:'input',condition:'Approved ISS interval for AR2 0-2.4s plus loop preroll remains missing. Correct masters and run affected gates.',check_at:new Date(Date.now()+30*6e4).toISOString(),checked_at:new Date(Date.now()-10*6e4).toISOString()},result:'Inspection d0b04b5e0; retain all existing approval holds.'};
 const video={key:'OWB:030',number:'030',title:'Apophis Closer Than Our Satellites',channel:'OWB',type:'long',lane:'progress',jobs:[{id:'Jother',status:'blocked',by:'cursor',hold:{condition:'Another video-level gate'}},job],production:{asOf:new Date().toISOString(),activeStages:['edit'],milestones:ids.map(id=>id==='edit'?edit:{id,label:id,state:id==='qa'?'unknown':'done'}),eta:{state:'unavailable',reasons:['Edit: blocked timing']}}};
 const board={tracker:{videos:[video]},models:{checkedAt:new Date().toISOString(),models:[]},owb:{jobs:video.jobs,jobStates:{J1468:{status:'done'}}}};
 await p.route('**/*',r=>{const q=r.request(),u=q.url();assert.equal(q.method(),'GET');if(u.includes('/api/ref'))return r.fulfill({json:{object:{sha}}});if(u.includes('board.json'))return r.fulfill({json:board});if(u.includes('heartbeat.json'))return r.fulfill({json:{}});return r.continue()});
 await p.goto(base+'/#v=OWB%3A030');const guide=p.locator('.milestone-card[data-stage="edit"] .blocker-guide');await guide.waitFor();
 assert.equal(await p.locator('.current-stage .blocker-guide').count(),0);
 const milestone=p.locator('.milestone-card[data-stage="edit"]');
 await milestone.locator(':scope > summary').click();assert.equal(await milestone.evaluate(e=>e.open),false);
 await p.getByRole('button',{name:'More information about Edit: Blocked'}).click();
 assert(await milestone.evaluate(e=>e.open));await p.waitForTimeout(500);
 assert(await milestone.locator(':scope > summary').evaluate(e=>document.activeElement===e));
 assert(await milestone.evaluate(e=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<100));
 assert.equal(await guide.getAttribute('data-blocker-scope'),'reference');const text=await guide.innerText();
 assert(text.includes('International Space Station (ISS) is missing')&&text.includes(job.remaining_action)&&text.includes('Codex'));
 assert(text.includes('J1468 · Completed')&&text.includes('Next recorded check')&&text.includes('not a promise'));
 assert(!text.includes('Resolve the recorded blocker')&&!text.includes('Unassigned'));
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(process.env.STUDIO_QA_SCREENSHOTS&&width===390){await guide.scrollIntoViewIfNeeded();await p.screenshot({path:process.env.STUDIO_QA_SCREENSHOTS+'/blocker-guidance-390.png'});}
 await guide.getByText('Full recorded blocker',{exact:true}).click();assert((await guide.innerText()).includes(job.hold.condition));
 await guide.getByRole('link',{name:/Open blocking job J1471/}).click();await p.locator('#job-J1471.selected-job').waitFor();assert(await p.locator('[data-disclosure="agent-queue"]').evaluate(e=>e.open));
 await p.goto(base+'/#v=OWB%3A030');await guide.waitFor();job.hold.check_at=new Date(Date.now()-6e4).toISOString();sha='two';await p.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await guide.getByText(/Check overdue/).waitFor();
 video.jobs=[];board.owb.jobs=[];sha='three';await p.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await guide.getByText(/no stage-specific reason/).waitFor();assert((await guide.innerText()).includes('Not recorded'));assert.equal(await guide.getByRole('link',{name:/Open blocking job/}).count(),0);
 assert.deepEqual(errors,[]);await p.close();
}console.log('Studio blocker browser QA OK: five widths; stage-reference matching, real reason/action/owner, dependency state, follow-up/overdue, original evidence, missing metadata and linked queue; no writes/overflow');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
