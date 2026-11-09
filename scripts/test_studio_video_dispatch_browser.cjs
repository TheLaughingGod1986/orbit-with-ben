// Build/serve dist first. All state refreshes are fixtures; never writes to production.
const {chromium}=require('playwright'),assert=require('assert'),fs=require('fs'),path=require('path');
const base=process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8788';
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
try{for(const width of [375,390,430,768,1280]){
 const now=new Date().toISOString();let sha='one';
 const admin={id:'Janalytics',status:'claimed',by:'codex',title:'Daily Studio read',remaining_action:'Validate collected metrics and rebuild the tracker',claimedAt:new Date(Date.now()-10*60000).toISOString(),progress:{step:2,of:4,at:now}};
 const next={id:'Jnext',status:'open',repo:'hos',film:'009',stage:'picture',kind:'chief',title:'Scope remaining picture rows',remaining_action:'Chief checks the balance and scopes the remaining picture rows'};
 const engineering={id:'Jengineering',status:'open',title:'Implement capacity-aware dispatch',kind:'assembly'};
 const picture={id:'picture',label:'Picture',state:'doing',jobs:[next]};
 const video={key:'HOS:009',number:'009',channel:'HOS',type:'long',title:"Why Doesn't the Moon Fall to Earth?",lane:'progress',jobs:[next],production:{milestones:[{id:'topic',state:'done'},{id:'script',state:'done'},{id:'vo',state:'done'},picture],activeStages:['picture'],eta:{state:'unavailable'}}};
 const board={publishedAt:now,tracker:{videos:[video]},owb:{jobs:[admin,next,engineering]},models:{checkedAt:now,chief:{agent:'claude'},models:[]},workflow:{at:now,active:[],states:{Janalytics:{state:'running'},Jnext:{state:'queued'},Jengineering:{state:'queued'}},next:{...engineering,worker:'gemini'}}};
 const page=await browser.newPage({viewport:{width,height:844}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',route=>{const q=route.request(),u=q.url();assert.equal(q.method(),'GET','no Review or production writes');
  if(u.includes('/api/ref'))return route.fulfill({json:{object:{sha}}});
  if(u.includes('board.json'))return route.fulfill({json:board});
  if(u.includes('heartbeat.json'))return route.fulfill({json:{}});
  if(!u.startsWith(base))return route.abort();return route.continue();
 });
 await page.goto(base);await page.locator('.video-next-work').waitFor();
 assert.equal(await page.locator('.activity-category').innerText(),'Analytics');
 let text=await page.locator('.video-next-work').innerText();
 assert(text.includes('Chief decision queued')&&text.includes('Start time not confirmed'));
 assert(text.includes('remaining')&&text.includes('does not confirm when this video task starts'));
 assert(text.includes('Next recorded dispatch: Engineering.'));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(process.env.STUDIO_QA_SCREENSHOTS){fs.mkdirSync(process.env.STUDIO_QA_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.STUDIO_QA_SCREENSHOTS,`dispatch-outlook-${width}.png`),fullPage:true});}
 // Same board refresh: a real next selection replaces the earlier engineering selection.
 next.kind='video';board.workflow.next={...next,worker:'gemini'};sha='two';
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 await page.getByRole('link',{name:/Selected next · not yet claimed/}).waitFor();
 assert((await page.locator('.video-next-work').innerText()).includes('Start time not confirmed'));
 await page.locator('.video-next-work>a').click();
 const selected=page.locator('#job-Jnext');await selected.waitFor();
 assert(await selected.evaluate(e=>e.classList.contains('selected-job')),'opens and highlights actual next job');
 await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
 admin.title='Check source quotations';admin.remaining_action='Review direct evidence';admin.film='059';sha='other-video';
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 await page.getByText(/Current video production task on another video/).waitFor();
 admin.title='Repair dispatcher capacity';admin.remaining_action='Validate the implementation';sha='three';
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 await page.locator('.activity-category[data-category="engineering"]').waitFor();
 // A claim is distinct from a selected job, and still does not complete a milestone.
 next.status='claimed';next.by='gemini';next.claimedAt=now;next.progress={step:1,of:3,at:now};next.urgent=1;
 board.workflow.states.Jnext.state='running';board.workflow.next=null;sha='four';
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 await page.getByRole('link',{name:/Working on this video/}).waitFor();
 assert.equal(await page.locator('.activity-category').innerText(),'Video production');
 assert((await page.locator('.featured-video').innerText()).includes('3 of 9 milestones complete'));
 assert(!(await page.locator('.video-next-work').innerText()).includes('does not confirm when'));
 next.status=admin.status='done';board.workflow.states.Jnext.state=board.workflow.states.Janalytics.state='done';sha='five';
 await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
 await page.getByRole('link',{name:/Next task not recorded/}).waitFor();
 for(const tab of ['Videos','Review','Agents','Schedule','Overview']){
  await page.locator('#nav').getByRole('link',{name:new RegExp(tab)}).click();
  await page.getByRole('heading',{name:tab==='Overview'?'Studio':tab,exact:true}).waitFor();
 }
 await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));
 const last=await page.locator('.overview-activity').boundingBox(),nav=await page.locator('#nav').boundingBox();
 assert(last.y+last.height<=nav.y,'bottom navigation clears final content');
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
 await page.close();console.log(`Studio video dispatch ${width}: PASS`);
}}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
