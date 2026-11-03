const {chromium}=require('playwright'),assert=require('assert');
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{for(const width of [375,390,430,768,1280]){
 const page=await browser.newPage({viewport:{width,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const ids=['topic','script','sources','vo','shots','picture','edit','thumbs','qa'];
 const video={key:'OWB:027',number:'027',channel:'OWB',type:'long',title:'Scheduled video with missing QA history',lane:'progress',youtube:{state:'scheduled',videoId:'example',publishAtLondon:'Sun 22 Nov 2026 18:00 GMT'},jobs:[{id:'Jother',status:'blocked',stage:'',title:'Separate Short repair'}],production:{activeStages:[],milestones:ids.map(id=>({id,label:id==='qa'?'Chief QA':id,state:id==='qa'?'unknown':'done',dependsOn:id==='qa'?['edit','thumbs']:[]}))}};
 const data={tracker:{videos:[video]},owb:{jobs:video.jobs},models:{checkedAt:new Date().toISOString(),models:[]}};
 await page.route('**/*',r=>{const q=r.request();assert.equal(q.method(),'GET');const url=q.url();if(url.includes('/api/ref'))return r.fulfill({json:{object:{sha:'stage-explanation'}}});if(url.includes('board.json'))return r.fulfill({json:data});if(url.includes('heartbeat.json'))return r.fulfill({json:{}});return r.continue()});
 await page.goto((process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8768')+'/#v=OWB%3A027');
 const card=page.locator('[data-stage="qa"]');await card.waitFor();if(!await card.evaluate(e=>e.open))await card.locator(':scope > summary').click();
 const text=await card.innerText();assert(text.includes('QA decision not recorded')&&text.includes('already scheduled')&&text.includes('22 Nov'));
 assert(!text.includes('Unassigned')&&!text.includes('Open stage details for')&&!text.includes('Separate Short repair'));
 assert(text.includes('Chief owns QA decisions')&&text.includes('not a reason to restart production'));
 await card.locator(':scope > summary').focus();await page.keyboard.press('Enter');assert.equal(await card.evaluate(e=>e.open),false);await page.keyboard.press('Enter');assert(await card.evaluate(e=>e.open));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.equal(await page.locator('#nav a').count(),5);assert.deepEqual(errors,[]);await page.close();
}console.log('Stage explanation browser QA OK: five widths, missing QA history vs scheduled release, unrelated-job scope, keyboard disclosure, deep link, no overflow or writes');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
