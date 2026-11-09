const fs = require('fs'), vm = require('vm'), assert = require('assert');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/tracker_app.js'), 'utf8');
const elements = {strip: {innerHTML:''},activity: {innerHTML:'',querySelectorAll:()=>[]},asof:{textContent:''}};
const context = {Date, console, localStorage:{getItem:()=>null},location:{hash:''},
  document:{getElementById:id=>elements[id]||null}, window:{}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf('  // Boot with any baked tracker')) + `
  globalThis.test = {deriveLane, jobProgress, jobState, matchesVideo, cardWorkHtml, cardHeadline, cardWaiting, renderActivity, renderStrip, cardHtml, jobHtml, approvedHtml, updateAsOf,
    setBoard:b=>{board=b;}};
})();`, context);
const t=context.test;
const uploaded={key:'OWB:023',type:'long',lane:'progress',working:true,youtube:{videoId:'abcdefghijk'},jobs:[]};
assert.equal(t.deriveLane(uploaded,null),'progress','browser must preserve actionable work on an uploaded video');
assert.equal(t.deriveLane({...uploaded,working:false,lane:'done'},null),'done');
const job={id:'J1',status:'claimed',by:'codex',title:'023 Venus: fix captions',claimedAt:new Date(Date.now()-60*60000).toISOString(),estMin:30,
  progress:{step:1,of:4,note:'Captions checked <script>'}};
assert.equal(t.jobProgress(job).pct,25,'elapsed time cannot inflate confirmed steps');
assert.equal(t.jobProgress({...job,progress:null}).pct,null,'unknown progress must remain unknown');
assert.equal(t.jobProgress({...job,progress:{step:0,of:4}}).pct,0);
assert.equal(t.jobState({...job,eta:new Date(Date.now()-46*60000).toISOString()}),'stalled');
t.setBoard({owb:{jobs:[job],jobStates:{J0:{status:'blocked'}}}});
assert.equal(t.jobState({id:'J2',status:'open',after:'J0'}),'waiting');
assert.equal(t.jobState({id:'J2',status:'blocked',result:'parked for Chief: audio FAIL'}),'review');
const video={...uploaded,jobs:[{id:'J1'}]};
let html=t.cardWorkHtml(video);
assert(html.includes("What's left")&&html.includes('25% · 1 of 4 steps complete')&&html.includes('Captions checked &lt;script&gt;'));
const parentDone={id:'J3',film:'023',title:'023 Venus: master done',by:'gemini',at:new Date().toISOString(),status:'done'};
assert(!t.matchesVideo(parentDone,{key:'OWB:023:S1',type:'short',parent:'OWB:023',shortId:'shortid1234',jobs:[]}),'do not claim parent job finished a Short');
const blocked={id:'J4',status:'blocked',title:'032 Titan: voiceover',result:'ElevenLabs: reset 30 Oct',progress:{step:2,of:4}};
t.setBoard({owb:{jobs:[job,blocked],done:[parentDone],day:{doneToday:1}}});
t.renderActivity();html=elements.activity.innerHTML;
assert(html.includes('<b>1</b> running')&&html.includes('<b>1</b> completed today'));
assert(html.includes('ElevenLabs: reset 30 Oct')&&html.includes('2 of 4 steps recorded complete'));
const paused={key:'OWB:032',type:'long',lane:'progress',jobs:[{id:'J4',status:'blocked'}]};
assert(t.cardHeadline(paused).startsWith('Work is paused'));
assert.equal(t.cardWaiting(paused),'credit reset');
assert(!t.matchesVideo({id:'AUDIT',title:'Weekly OWB audit',taskKeys:['OWB:032']},paused));
const wide={id:'J1079',title:'J1075 FIX: correct CFR18 hash and qualify inaccessible QA media evidence',status:'claimed',taskKeys:['OWB:026','OWB:028','HOS:007','HOS:008']};
assert(!t.matchesVideo(wide,{key:'HOS:008',type:'long',jobs:[]}),'a studio-wide job (4+ videos) is not shown as one card\'s work');
assert(t.matchesVideo({id:'PAIR',title:'HOS 009 + 010 Shorts VO',taskKeys:['HOS:009','HOS:010']},{key:'HOS:010',type:'long',jobs:[]}),'a two-video job still shows on both cards');
console.log('Tracker activity regression checks passed');

const chiefReview={job:'J0956',title:'Neptune <review>',agent:'codex',startedAt:new Date().toISOString(),expiresAt:new Date(Date.now()+60000).toISOString()};
t.setBoard({owb:{jobs:[]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:chiefReview,next:[{id:'J0974',title:'Apophis review'}]}}});
t.renderStrip();html=elements.strip.innerHTML;
assert(html.includes('J0956')&&html.includes('Neptune &lt;review&gt;')&&html.includes('aria-valuenow="0"'));
assert(html.includes('J0974'));
assert(!html.includes('No job is currently claimed')&&!html.includes('Nothing else queued'));
t.setBoard({owb:{jobs:[]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:{...chiefReview,expiresAt:new Date(Date.now()-60000).toISOString()},next:[]}}});
t.renderStrip();assert(!elements.strip.innerHTML.includes('J0956'),'expired Chief reviews must not look active');

// Keep the header to one real current job and one next task, with review fallback only when no job is claimed.
t.setBoard({owb:{jobs:[{...job,eta:new Date(Date.now()+60000).toISOString()}, {...job,id:'JSECOND',eta:new Date(Date.now()+60000).toISOString()}]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:chiefReview,next:[{id:'J0974',title:'Apophis review'},{id:'JNEXT2',title:'Later review'}]}}});
t.renderStrip();html=elements.strip.innerHTML;
assert(!html.includes('J0956'),'claimed work replaces the separate Chief-review card');
assert(!html.includes('JSECOND')&&!html.includes('JNEXT2'),'show only one current and one next');
assert(html.includes('J0974'));

const liveJob={...job,eta:new Date(Date.now()+60000).toISOString()};
t.setBoard({owb:{jobs:[liveJob]}});
const activeVideo={...video,number:'023',title:'Venus',channel:'OWB',flags:[],jobs:[{id:liveJob.id}],lane:'progress'};
html=t.cardHtml(activeVideo);assert(html.includes('live-dot')&&html.includes('Working now'));
t.setBoard({owb:{jobs:[{...liveJob,status:'blocked',result:'waiting for inputs'}]}});
assert(!t.cardHtml(activeVideo).includes('live-dot'),'blocked cards must not pulse');
assert(t.jobHtml(liveJob,'now').includes('aria-valuenow="25"'),'keep confirmed-step progress');
assert(t.jobHtml({...liveJob,progress:null},'now').includes('0% recorded · waiting for the first update'));
assert(t.jobHtml({...liveJob,progress:null},'now').includes('aria-valuenow="0"'));
assert(t.jobHtml({...liveJob,progress:{step:1,of:4,at:new Date(Date.now()-6*60000).toISOString()}},'now').includes('No progress update for 6 min'));
assert(!t.jobHtml({...liveJob,progress:{step:1,of:4,at:new Date().toISOString()}},'now').includes('No progress update'));

const reviewProgress={...chiefReview,progress:{step:2,of:3,note:'Evidence checked'}};
t.setBoard({owb:{jobs:[]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:reviewProgress,next:[]}}});
t.renderStrip();html=elements.strip.innerHTML;
assert(html.includes('aria-valuenow="67"')&&html.includes('67%'),'Chief review uses its own confirmed steps');

// All dashboard surfaces consume the shared Chief-review activity without borrowing worker completion.
const blockedReview={id:'J0956',title:'Neptune technical check',status:'blocked',by:'cursor',
  result:'Chief decision: correction J0988',progress:{step:5,of:5}};
const snap={counts:{running:1,queued:1,review:0,waiting:0,stalled:0},
  states:{J0956:{state:'running',reason:''},J0988:{state:'queued',reason:''}},
  active:[{id:'J0956',worker:'codex',mode:'review',startedAt:new Date().toISOString(),progress:{step:1,of:3}}],
  next:{id:'J0988',status:'open',title:'Neptune correction',worker:'gemini',mode:'job'}};
t.setBoard({workflow:snap,owb:{jobs:[blockedReview,{id:'J0988',status:'open',needs:'mini'}]},
  models:{chief:{name:'Codex'},models:[],chiefWork:{active:reviewProgress,next:[{id:'WRONG',title:'Old independent next'}]}}});
t.renderActivity();html=elements.activity.innerHTML;
assert(html.includes('<b>1</b> running')&&html.includes('Waiting and blockers · 0'));
t.renderStrip();html=elements.strip.innerHTML;
assert(html.includes('J0988')&&!html.includes('WRONG'));
assert(html.includes('33%')&&!html.includes('100%')&&html.includes('Codex'));
const reviewVideo={...activeVideo,jobs:[{id:'J0956'}]};
html=t.cardHtml(reviewVideo);
assert(html.includes('Chief reviewing')&&html.includes('live-dot')&&html.includes('Review the finished work'));
assert(html.includes('33%')&&!html.includes('100%'));
assert(!html.includes('Awaiting Chief review'),'active review is not also a waiting task');
html=t.approvedHtml({state:'working',step:0,of:4});
assert(html.includes('aria-valuenow="0"')&&html.includes('width:0%')&&!html.includes('width:5%'));
for(const [state,privacy,label] of [['live','public','Live'],['scheduled','private','Scheduled'],['uploaded','private','Private']]) {
  html=t.cardHtml({...activeVideo,youtube:{videoId:'abcdefghijk',state,privacy},lane:'done'});
  assert(html.includes('class="badge publication">'+label+'</span>'));
}
t.setBoard({publishedAt:new Date(Date.now()-4*60000).toISOString()});
t.updateAsOf();assert(elements.asof.textContent.startsWith('Stale data'));
t.setBoard({publishedAt:new Date().toISOString()});
t.updateAsOf();assert(elements.asof.textContent.startsWith('Updated'));
console.log('Shared workflow, publication and progress regression checks passed');

// A live long video must describe its follow-up Shorts and title test in plain language.
const audio={id:'J1005',status:'open',kind:'qa',remaining_action:"Check sound and pronunciation in the related Shorts",title:'J0966 HC: audition four finished masters and resolve vaccine pronunciation warnings (GBP0)'};
const signoff={id:'J0966',status:'blocked',after:'J1005',remaining_action:'Sign off the related Shorts',kind:'video',title:'HOS 60% re-cut batch HC (local only): -I_GHK-GcFs, x_3L_IdYgEc',result:'Acting-Chief evidence ruling: technical/still checks accepted; full PASS withheld pending finished-audio QA J1005.'};
const titleTest={id:'J0978',status:'blocked',kind:'listing',remaining_action:'Start the next title test',title:'Studio Test B start: HOS Atom GHZDsiH7L7A title/line 1/tags',result:'waits for: J0280 Title Test & Compare still running'};
const atom={key:'HOS:004',type:'long',lane:'progress',jobs:[signoff,audio,titleTest],flags:[],youtube:{state:'live',privacy:'public'}};
t.setBoard({owb:{jobs:[signoff,audio,titleTest]},workflow:{states:{J0966:{state:'waiting'},J1005:{state:'queued'},J0978:{state:'waiting'}}}});
html=t.cardWorkHtml(atom);
const visible=html.replace(/<details[\s\S]*?<\/details>/g,'');
assert(visible.includes('Check sound and pronunciation in the related Shorts'));
assert(visible.includes('Sign off the related Shorts'));
assert(visible.includes('After the sound check'));
assert(visible.includes('Start the next title test'));
assert(visible.includes('After the current title test finishes'));
assert(!/J\d{4}|GBP0|last completed|60% re-cut/i.test(visible));
assert(html.includes('Job details'),'original job records remain available');
assert(t.cardHeadline(atom).startsWith('Live on YouTube'));
console.log('Plain remaining-work labels verified against the Atom workflow');

const tree={id:'TREE',status:'blocked',title:'Studio finish: end screen, pinned comment, Test & Compare',remaining_action:'Post and pin the comment',hold:{type:'public',condition:'Video must be public',check_at:'2026-11-05T18:05Z'}};
t.setBoard({owb:{jobs:[tree]},workflow:{states:{TREE:{state:'waiting'}}}});
html=t.cardWorkHtml({key:'HOS:006',type:'long',jobs:[tree]});
const treeVisible=html.replace(/<details[\s\S]*?<\/details>/g,'');
assert(treeVisible.includes('Post and pin the comment')&&!treeVisible.includes('Update the end screen'));
assert(treeVisible.includes('After the video is public'));

const sourceTask={id:'SOURCE',status:'blocked',remaining_action:'Post and pin the comment'};
const verifier={id:'CHECK',status:'claimed',by:'codex',recheck_of:'SOURCE',eta:new Date(Date.now()+60000).toISOString(),remaining_action:'Verify readiness: Post and pin the comment'};
t.setBoard({owb:{jobs:[sourceTask,verifier]}});
const checkedCard={...activeVideo,jobs:[{id:'SOURCE'}]};
assert(t.matchesVideo(verifier,checkedCard),'a condition check belongs on its original video card');
assert(t.cardHtml(checkedCard).includes('live-dot'),'active condition checks keep the original card live');
