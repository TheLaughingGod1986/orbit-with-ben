// Failure/loading, long content, broken image and unchanged-refresh checks for V3. No live writes.
const {chromium}=require('playwright'),assert=require('assert');
const base=process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8765';
const video={key:'OWB:999',number:'999',title:'A long video title '.repeat(25),channel:'OWB',type:'long',lane:'progress',jobs:[]};
const board={tracker:{videos:[video,{...video,key:'OWB:998',number:'998',title:'Public video with missing image',lane:'done',youtube:{videoId:'abcdefghijk',state:'live',privacy:'public'}}]},models:{checkedAt:new Date().toISOString(),models:[]},owb:{jobs:[]}};
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{
  for(const width of [375,390,430,768,1280]){
    const p=await b.newPage({viewport:{width,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
    let release,mode='hold',sha='initial',reads=0;
    const gate=new Promise(r=>release=r);
    await p.route('**/*',async r=>{const q=r.request(),u=q.url();assert(q.method()==='GET','error QA never writes');
      if(u.includes('/api/ref'))return r.fulfill({json:{object:{sha}}});
      if(u.includes('board.json')){reads++;if(mode==='hold')await gate;if(mode==='fail')return r.fulfill({status:503,body:'temporary'});return r.fulfill({json:board})}
      if(u.includes('heartbeat.json'))return r.fulfill({json:{}});if(u.includes('i.ytimg.com'))return r.abort();return r.continue();});
    await p.goto(base,{waitUntil:'domcontentloaded'});
    assert((await p.locator('main').innerText()).includes('Loading'));
    mode='fail';release();await p.getByRole('status').filter({hasText:'Retrying automatically'}).waitFor();
    mode='ok';await p.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
    await p.locator('.featured-video').waitFor();assert((await p.locator('.featured-heading h3').innerText()).length>300);
    assert.equal(await p.locator('.featured-heading h3').evaluate(x=>getComputedStyle(x).overflow),'visible');
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    assert((await p.locator('.featured-video').innerText()).includes('9 unconfirmed'));
    const readCount=reads;await p.evaluate(()=>{window.keptCard=document.querySelector('.featured-video');document.dispatchEvent(new Event('visibilitychange'))});
    await p.waitForTimeout(100);assert(await p.evaluate(()=>window.keptCard===document.querySelector('.featured-video')),'unchanged DOM retained');assert.equal(reads,readCount,'same SHA does not fetch board twice');
    sha='next';mode='fail';await p.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));await p.waitForTimeout(100);
    assert(await p.locator('.featured-video').isVisible(),'transient failure keeps loaded content');
    await p.evaluate(()=>scrollTo(0,document.body.scrollHeight));const bottom=await p.locator('.overview-activity').boundingBox(),nav=await p.locator('#nav').boundingBox();assert(bottom.y+bottom.height<=nav.y,'last card clears bottom nav');
    mode='ok';await p.goto(base+'/#videos');await p.getByRole('heading',{name:'Videos',exact:true}).waitFor();
    await p.waitForTimeout(100);assert.equal(await p.locator('.thumb img').count(),0,'broken thumbnails fall back to the channel tile');
    assert((await p.locator('.thumb .tile').allTextContents()).includes('998'));
    assert.deepEqual(errors,[]);await p.close();
  }
  console.log('Studio V3 failure/refresh QA OK: five widths; loading, retry, retained content/DOM, long titles, unknown milestones, no overflow or writes');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
