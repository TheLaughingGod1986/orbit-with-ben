// Build board_site and serve dist first. All board reads and Review writes are intercepted fixtures.
const {chromium}=require('playwright'), {execFileSync}=require('child_process'), assert=require('assert'), path=require('path');
const root=path.join(__dirname,'..');
const production=JSON.parse(execFileSync('python3',['-c',`
import json,sys
sys.path.insert(0,'scripts')
from uat_outlook import PLAN,forecast
from datetime import datetime,timezone
now=datetime.now(timezone.utc)
v=dict(key='OWB:999',channel='OWB',type='long',lane='progress')
stages={k:dict(state='done' if k in ('topic','script','sources') else 'unknown') for k in PLAN}
stages['script'].update(version='v01',score=92.1)
stages['picture']=dict(state='review',owner='chief',note='J1191 complete (parked for Chief picture PASS): all 101/101 Flow v03 rows minted and KEEP. /private/tmp/retained-original-note')
jobs=[dict(id='J1191',stage='picture',status='blocked',by='chief',hold=dict(type='approval',condition='Awaiting Chief picture approval'))]
print(json.dumps(forecast(v,stages,jobs,{},now)))
`],{cwd:root,encoding:'utf8'}));
const v={key:'OWB:999',checkId:'OWB-999',number:'999',channel:'OWB',type:'long',title:'Inside a Black Hole',lane:'progress',version:'v01',jobs:[],production};
const board={tracker:{videos:[v,{...v,key:'HOS:998',checkId:'HOS-998',title:'The Willow Tree That Was Made of Air',channel:'HOS'},
  {...v,key:'OWB:997',checkId:'OWB-997',title:'Finished UAT film',lane:'ready',readyFor:'Ben',watch:{url:'https://example.com/cut',version:'v01'}},
  {...v,key:'OWB:996',checkId:'OWB-996',title:'Second UAT film',lane:'ready',readyFor:'Ben',watch:{url:'https://example.com/cut',version:'v01'}},
  {...v,key:'OWB:995',title:'Backlog film',lane:'upcoming',production:undefined},
  {...v,key:'OWB:994',title:'Published film',lane:'done',youtube:{state:'live',privacy:'public',videoId:'abcdefghijk'}},
  {...v,key:'OWB:993',title:'Legacy data film',production:undefined}]},models:{checkedAt:new Date().toISOString(),models:[]},owb:{jobs:[{id:'JADMIN',status:'open',by:'codex',title:'Internal queue detail stays in Agents'}]}};
(async()=>{
  const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
  const errors=[],writes=[];
  try {
    for(const width of [375,390,430,768,1280]) {
      const page=await browser.newPage({viewport:{width,height:844}});
      page.on('pageerror',e=>errors.push(e.message));
      await page.route('**/*',route=>{
        const request=route.request(),url=request.url();
        if(request.method()!=='GET') {
          assert(url.endsWith('/api/checks'),'only existing Review endpoint may be called');
          writes.push(request.postDataJSON());return route.fulfill({json:{ok:true}});
        }
        if(url.includes('/api/ref')) return route.fulfill({json:{object:{sha:'v2-fixture'}}});
        if(url.includes('board.json')) return route.fulfill({json:board});
        if(url.includes('heartbeat.json')) return route.fulfill({json:{}});
        if(url.includes('i.ytimg.com')) return route.abort();
        return route.continue();
      });
      const base=process.env.STUDIO_PREVIEW_URL||'http://127.0.0.1:8765';
      await page.goto(base);
      await page.getByRole('heading',{name:/Next for your review/}).waitFor();
      assert.equal(await page.locator('.overview-stats>a').count(),3);
      const statValues=await page.locator('.overview-stats b').allTextContents();
      assert.deepEqual(statValues,['2','3','0']);
      await page.getByRole('link',{name:/Studio status:/}).click();
      await page.getByRole('heading',{name:'Agents',exact:true}).waitFor();
      await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
      await page.locator('#nav').getByRole('link',{name:/Videos/}).click();
      await page.getByRole('button',{name:'HOS',exact:true}).click();
      await page.getByRole('button',{name:'Shorts',exact:true}).click();
      await page.getByRole('button',{name:/Backlog/}).click();
      await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
      await page.locator('.overview-stats>a').nth(1).click();
      await page.getByText('Producing · 3 unique videos').waitFor();
      assert(!(await page.locator('main').innerText()).includes('Published film'));
      await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
      await page.locator('.overview-stats>a').nth(2).click();
      await page.getByRole('heading',{name:/This week · scheduled/}).waitFor();
      await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
      await page.locator('.overview-stats>a').first().click();
      await page.getByRole('heading',{name:'Review',exact:true}).waitFor();
      await page.locator('#nav').getByRole('link',{name:/Overview/}).click();
      const featuredTitle=await page.locator('.featured-heading h3').innerText();
      await page.locator('.featured-video').click();
      await page.getByRole('heading',{name:featuredTitle,exact:true}).waitFor();
      for(const tab of ['Videos','Review','Agents','Schedule','Overview']) {
        await page.locator('#nav').getByRole('link',{name:new RegExp(tab)}).click();
        await page.getByRole('heading',{name:tab==='Overview'?'Studio':tab,exact:true}).waitFor();
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${tab} overflow at ${width}`);
        if(tab==='Agents') {await page.getByText('Job queue · 1 job',{exact:true}).click();assert((await page.locator('main').innerText()).includes('JADMIN'));}
        if(tab==='Overview') assert(!(await page.locator('main').innerText()).includes('JADMIN'));
      }
      if(process.env.STUDIO_QA_SCREENSHOTS) await page.screenshot({path:`${process.env.STUDIO_QA_SCREENSHOTS}/v2-overview-${width}.png`,fullPage:false});
      await page.goto(`${base}/#v=OWB%3A999`);
      await page.getByRole('progressbar',{name:'Milestone completion, not production time'}).waitFor();
      assert.equal(await page.getByRole('progressbar').getAttribute('aria-valuenow'),'3');
      const text=await page.locator('main').innerText();
      assert(text.includes('33%')&&text.includes('3 of 9 milestones complete'));
      assert(text.includes('Picture production')&&text.includes('101/101 Flow shots generated'));
      assert(text.includes('Chief reviews and approves this stage.')&&text.includes('Assigned agent: Grok'));
      assert(!text.includes('J1191 complete')&&!text.includes('/private/tmp/'),'raw evidence hidden by default');
      assert.equal(await page.locator('.milestone-card[open]').count(),1);
      const script=page.locator('details[data-stage="script"]');
      await script.locator(':scope > summary').focus();await page.keyboard.press('Enter');assert(await script.evaluate(x=>x.open));
      await page.keyboard.press('Space');assert(!(await script.evaluate(x=>x.open)));
      assert.equal(await script.locator(':scope > summary').getAttribute('aria-label'),'Script: Completed');
      const picture=page.locator('details[data-stage="picture"]');
      await picture.getByText('View technical details',{exact:true}).click();
      assert((await page.locator('main').innerText()).includes('/private/tmp/retained-original-note'));
      // Returning to visibility triggers poll with the same SHA; expanded evidence stays open.
      await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
      await page.waitForTimeout(150);
      assert(await page.locator('details[data-stage="picture"] details.technical').evaluate(x=>x.open));
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`detail overflow at ${width}`);
      await page.evaluate(()=>window.scrollTo(0,0));
      assert((await page.locator('.video-heading').boundingBox()).y>=16,'content starts below top inset');
      await picture.getByText('View technical details',{exact:true}).click();
      await page.evaluate(()=>window.scrollTo(0,0));
      if(process.env.STUDIO_QA_SCREENSHOTS) await page.screenshot({path:`${process.env.STUDIO_QA_SCREENSHOTS}/v2-detail-${width}.png`,fullPage:false});
      await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));
      const last=await page.locator('.video-technical').boundingBox(),nav=await page.locator('#nav').boundingBox();
      assert(last.y+last.height<=nav.y,'last disclosure clears fixed bottom nav');
      await page.getByRole('link',{name:'‹ Back to Videos'}).click();
      await page.getByLabel('Sort videos').selectOption('blocked');
      await page.getByLabel('Sort videos').selectOption('updated');
      await page.getByLabel('Sort videos').selectOption('stage');
      await page.getByLabel('Sort videos').selectOption('uat');
      await page.getByRole('button',{name:'Backlog',exact:false}).click();assert((await page.locator('main').innerText()).includes('Backlog film'));
      await page.goto(`${base}/#review`);
      const review=await page.locator('main').innerText();assert(!review.includes('Inside a Black Hole'));
      await page.getByRole('link').filter({hasText:'Finished UAT film'}).first().click();
      await page.getByRole('button',{name:'✓ Approve',exact:true}).click();
      await page.waitForFunction(()=>location.hash==='#review');
      await page.getByRole('link').filter({hasText:'Second UAT film'}).first().click();
      await page.locator('#uat-notes').fill('0:38 text does not match the voice');
      await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
      await page.waitForTimeout(100);
      assert.equal(await page.locator('#uat-notes').inputValue(),'0:38 text does not match the voice');
      await page.getByRole('button',{name:'Request changes',exact:true}).click();
      await page.waitForFunction(()=>location.hash==='#review');
      await page.close();
    }
    assert.deepEqual(errors,[]);
    assert.equal(writes.length,10);
    for(let i=0;i<writes.length;i+=2) {
      assert.equal(writes[i].doc.verdict,'ok');assert.equal(writes[i].doc.film,'OWB:997');
      assert.equal(writes[i+1].doc.verdict,'change');assert.deepEqual(writes[i+1].doc.fixes,[{t:'0:38',text:'text does not match the voice'}]);
    }
    console.log('Studio V2 browser QA OK: 375/390/430/768/1280px, five tabs, milestones, keyboard disclosures, refresh persistence, sorting, deep links, both intercepted UAT actions; no page errors or overflow');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
