// Build/serve board_site dist first. Requests use fixtures; no production writes.
const {chromium}=require('playwright'),{execFileSync}=require('child_process');
const assert=require('assert'),path=require('path'),fs=require('fs');
const root=path.join(__dirname,'..');
const production=JSON.parse(execFileSync('python3',['-c',`
import json,sys
sys.path.insert(0,'scripts')
from uat_outlook import forecast
from datetime import datetime,timezone
stages={'topic':{'status':'done'},'script':{'status':'done'},'facts':{'status':'done'},'vo':{'status':'done'},
        'picture':{'status':'doing','steps':[70,90],'steps_unit':'board rows rendered'},'thumbnails':{'status':'todo'}}
v={'key':'HOS:009','channel':'HOS','type':'long','lane':'progress'}
jobs=[{'id':'JSCOPE','stage':'picture','status':'open','remaining_action':'Chief rechecks Flow balance and scopes the remaining 20 picture rows.'}]
print(json.dumps(forecast(v,stages,jobs,{},datetime.now(timezone.utc))))
`],{cwd:root,encoding:'utf8'}));
const v={key:'HOS:009',checkId:'HOS-009',number:'009',channel:'HOS',type:'long',title:"Why Doesn't the Moon Fall to Earth?",lane:'progress',jobs:[],production};
const board={tracker:{videos:[v]},owb:{jobs:[]},models:{checkedAt:new Date().toISOString(),models:[]}};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const errors=[];
 try{
  for(const width of [375,390,430,768,1280]){
   const page=await browser.newPage({viewport:{width,height:844}});
   page.on('pageerror',e=>errors.push(e.message));
   await page.route('**/*',route=>{
    const r=route.request(),url=r.url();assert.equal(r.method(),'GET','no writes');
    if(url.includes('/api/ref'))return route.fulfill({json:{object:{sha:'hos-rows-fixture'}}});
    if(url.includes('board.json'))return route.fulfill({json:board});
    if(url.includes('heartbeat.json'))return route.fulfill({json:{}});
    if(!url.startsWith(process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8786'))return route.abort();
    return route.continue();
   });
   await page.goto(process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8786');
   await page.locator('.featured-video').waitFor();
   const text=await page.locator('.featured-video').innerText();
   assert(text.includes('4 of 9 milestones complete')&&text.includes('44%'));
   assert(text.includes('70/90 picture rows recorded'),'stage rows remain distinct from milestone completion');
   assert(text.includes('Chief rechecks Flow balance and scopes the remaining 20 picture rows.'),'recorded stage action is shown');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal overflow');
   if(process.env.STUDIO_QA_SCREENSHOTS){fs.mkdirSync(process.env.STUDIO_QA_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.STUDIO_QA_SCREENSHOTS,`hos-rows-${width}.png`),fullPage:true});}
   await page.locator('.featured-video').click();
   await page.getByRole('heading',{name:v.title,exact:true}).waitFor();
   assert((await page.locator('main').innerText()).includes('70/90 picture rows recorded'));
   for(const tab of ['Videos','Review','Agents','Schedule','Overview']){
    await page.locator('#nav').getByRole('link',{name:new RegExp(tab)}).click();
    await page.getByRole('heading',{name:tab==='Overview'?'Studio':tab,exact:true}).waitFor();
   }
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.close();console.log(`HOS recorded-stage rows/mobile navigation ${width}: PASS`);
  }
  assert.deepEqual(errors,[],'no browser errors');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
