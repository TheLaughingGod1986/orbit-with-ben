// Mixed project/cut data remains honest before and after the Mini publisher upgrades. No live writes.
const {chromium}=require('playwright'),assert=require('assert'),fs=require('fs');
const base=process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8772';
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{
for(const width of [375,390,430,768,1280]){
 const page=await browser.newPage({viewport:{width,height:844}}),errors=[];page.on('pageerror',e=>errors.push(e.message));let sha='legacy';
 const rows=['topic','script','sources','vo','shots','picture','edit','thumbs','qa'].map(id=>({id,state:id==='edit'?'blocked':id==='qa'?'unknown':'done',source:id==='edit'?{note:'AR cohort: original cut is separate'}:{}}));
 const video={key:'OWB:030',checkId:'OWB-030',channel:'OWB',number:'030',title:'Apophis Closer Than Our Satellites',type:'long',version:'v13a',lane:'progress',jobs:[],watch:{url:'https://example.test/approved-cut',file:'OWB UAT/030_apophis_short_v13a_PHONE.mp4'},production:{milestones:rows}};
 const board={tracker:{videos:[video]},owb:{jobs:[]},models:{checkedAt:new Date().toISOString(),models:[]}};
 await page.route('**/*',r=>{const q=r.request(),u=q.url();assert.equal(q.method(),'GET');if(u.includes('/api/ref'))return r.fulfill({json:{object:{sha}}});if(u.includes('board.json'))return r.fulfill({json:board});if(u.includes('heartbeat.json'))return r.fulfill({json:{}});return r.continue()});
 await page.goto(base);await page.locator('.featured-video').waitFor();let text=await page.locator('.featured-video').innerText();
 assert(text.includes('Short')&&text.includes('Cut progress')&&text.includes('Unconfirmed')&&text.includes('Related work'));assert(!/78%|0%/.test(text));
 assert.equal(await page.locator('.featured-video [role="progressbar"]').count(),0);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(process.env.STUDIO_QA_SCREENSHOTS)await page.screenshot({path:process.env.STUDIO_QA_SCREENSHOTS+`/cut-scope-overview-${width}.png`});
 await page.locator('.featured-video').click();await page.getByRole('heading',{name:'Progress for this cut unconfirmed',exact:true}).waitFor();assert.equal(await page.locator('main .progress-number,main [role="progressbar"]').count(),0);
 const history=page.locator('details').filter({has:page.locator(':scope > summary').filter({hasText:'Related project history'})}).first();
 // Use an explicit disclosure selector to avoid matching its nested stage disclosures.
 const disclosure=page.locator('[data-disclosure="OWB:030-project-history"]');assert.equal(await disclosure.evaluate(e=>e.open),false);await disclosure.locator(':scope > summary').click();assert((await disclosure.innerText()).includes('7 of 9'));assert.equal(await page.locator('[data-stage="topic"] small').innerText(),'Completed');
 video.type='short';video.cutFormatCorrected=true;video.production={scope:'unconfirmed_cut',milestones:rows.map(m=>({...m,state:'unknown',source:{}})),projectHistory:{milestones:rows}};sha='new-publisher';await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await page.waitForTimeout(200);assert(await disclosure.evaluate(e=>e.open),'refresh preserves expanded project history');
 if(process.env.STUDIO_QA_SCREENSHOTS&&width===390)await page.screenshot({path:process.env.STUDIO_QA_SCREENSHOTS+'/cut-scope-history-390.png'});
 await page.locator('#nav').getByRole('link',{name:/Videos/}).click();await page.getByRole('button',{name:'Shorts',exact:true}).click();await page.getByRole('link',{name:/Apophis Closer/}).waitFor();assert(!(await page.locator('main').innerText()).includes('78%'));
 for(const tab of ['Review','Agents','Schedule','Overview']){await page.locator('#nav').getByRole('link',{name:new RegExp(tab)}).click();await page.getByRole('heading',{name:tab==='Overview'?'Studio':tab,exact:true}).waitFor();}
 await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));const activity=await page.locator('.overview-activity').boundingBox(),nav=await page.locator('#nav').boundingBox();assert(activity.y+activity.height<=nav.y);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);await page.close();
}console.log('Cut scope mobile QA OK: five widths, legacy/new payloads, truthful format/progress, preserved history, deep links, filters/all tabs, no overflow/errors/writes');}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
