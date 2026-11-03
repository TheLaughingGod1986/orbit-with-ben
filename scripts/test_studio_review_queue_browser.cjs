const {chromium}=require('playwright'),assert=require('assert');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{for(const width of [375,390,430,768,1280]){
 const page=await browser.newPage({viewport:{width,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));const now=new Date().toISOString();
 const parent={id:'J1834',status:'blocked',stage:'edit',by:'codex',title:'ISS acquisition',hold:{condition:'Parked for Chief approval of delivered ISS candidate',check_at:new Date(Date.now()+60*6e4).toISOString()},remaining_action:'Chief views moving preview'};
 const task={id:'J1841',status:'open',kind:'chief',recheck_of:'J1834',title:'Review delivered ISS candidate'};
 const busy={id:'J1835',status:'claimed',by:'codex',title:'Verify another film',remaining_action:'Check the other film',claimedAt:now};
 const video={key:'OWB:030',channel:'OWB',type:'long',title:'Apophis',lane:'progress',jobs:[parent],production:{activeStages:['edit'],milestones:[{id:'edit',label:'Edit',state:'blocked',reviewer:'chief',jobs:[parent]}]}};
 const board={tracker:{videos:[video]},owb:{jobs:[parent,task,busy]},models:{checkedAt:now,chief:{agent:'codex'},models:[]},workflow:{at:now,states:{J1841:{state:'queued'},J1835:{state:'running'}}}};
 await page.route('**/*',r=>{const q=r.request(),url=q.url();assert.equal(q.method(),'GET');if(url.includes('/api/ref'))return r.fulfill({json:{object:{sha:'review-queue'}}});if(url.includes('board.json'))return r.fulfill({json:board});if(url.includes('heartbeat.json'))return r.fulfill({json:{at:now,state:'waiting',why:['in use (0 min idle, needs 10)']}});return r.continue()});
 await page.goto((process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8768')+'/#v=OWB%3A030');const guide=page.locator('[data-stage="edit"] .blocker-guide');await guide.waitFor();
 assert((await page.locator('[data-stage="edit"] > summary').innerText()).includes('Awaiting review'));
 const text=(await guide.innerText()).toLowerCase();assert(text.includes('awaiting chief review')&&text.includes('eligible now')&&text.includes('working on j1835')&&text.includes('does not schedule or delay'));
 await guide.getByText('Reviewer availability and MacBook',{exact:true}).click();assert((await guide.innerText()).includes('No reliable reviewer-free time'));assert((await guide.innerText()).includes('in use'));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await guide.getByRole('link',{name:/Open review job J1841/}).click();await page.locator('#job-J1841.selected-job').waitFor();assert.deepEqual(errors,[]);await page.close();
}console.log('Review queue browser QA OK: five widths; immediate review vs follow-up, busy reviewer job, honest availability, MacBook guard, direct job navigation, no overflow/errors/writes');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
