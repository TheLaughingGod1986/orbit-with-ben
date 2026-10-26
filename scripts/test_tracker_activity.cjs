const fs = require('fs'), vm = require('vm'), assert = require('assert');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/tracker_app.js'), 'utf8');
const elements = {strip: {innerHTML:''},activity: {innerHTML:'',querySelectorAll:()=>[]}};
const context = {Date, console, localStorage:{getItem:()=>null},location:{hash:''},
  document:{getElementById:id=>elements[id]||null}, window:{}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf('  // Boot with any baked tracker')) + `
  globalThis.test = {deriveLane, jobProgress, jobState, matchesVideo, cardWorkHtml, cardHeadline, cardWaiting, renderActivity, renderStrip,
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
assert(html.includes('1 job remaining')&&html.includes('25% confirmed')&&html.includes('Captions checked &lt;script&gt;'));
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
console.log('Tracker activity regression checks passed');

const chiefReview={job:'J0956',title:'Neptune <review>',agent:'codex',startedAt:new Date().toISOString(),expiresAt:new Date(Date.now()+60000).toISOString()};
t.setBoard({owb:{jobs:[]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:chiefReview,next:[{id:'J0974',title:'Apophis review'}]}}});
t.renderStrip();html=elements.strip.innerHTML;
assert(html.includes('J0956 · Chief review')&&html.includes('Neptune &lt;review&gt;'));
assert(html.includes('J0974 · Next Chief task'));
assert(!html.includes('No job is currently claimed')&&!html.includes('Nothing else queued'));
t.setBoard({owb:{jobs:[]},models:{chief:{name:'Codex'},models:[],chiefWork:{active:{...chiefReview,expiresAt:new Date(Date.now()-60000).toISOString()},next:[]}}});
t.renderStrip();assert(!elements.strip.innerHTML.includes('J0956 · Chief review'),'expired Chief reviews must not look active');
