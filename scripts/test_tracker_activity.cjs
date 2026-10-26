const fs = require('fs'), vm = require('vm'), assert = require('assert');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname, '../05_Analytics/kanban/board_site/tracker_app.js'), 'utf8');
const elements = {activity: {innerHTML:'',querySelectorAll:()=>[]}};
const context = {Date, console, localStorage:{getItem:()=>null},location:{hash:''},
  document:{getElementById:id=>elements[id]||null}, window:{}};
vm.createContext(context);
vm.runInContext(source.slice(0, source.indexOf('  // Boot with any baked tracker')) + `
  globalThis.test = {deriveLane, jobProgress, jobState, matchesVideo, cardWorkHtml, cardHeadline, cardWaiting, renderActivity, jobBucket, nextAction, approvedRecords, workflowCounts, pipelineVideos, workflowJobHtml,
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

// Every current job has one primary bucket; approvals never hide blocked jobs.
const queue=[job,blocked,{id:'J5',status:'open',after:'J4',title:'Shared studio audit',repo:'owb'},
  {id:'J6',status:'open',title:'HOS 007 captions',repo:'hos'}];
const videoRows=[{key:'SCHEDULED',lane:'done',youtube:{videoId:'scheduled01',state:'scheduled'}},
  {key:'LIVE',lane:'progress',working:true,youtube:{videoId:'livevideo01',state:'live'}},
  {key:'READY',lane:'ready',readyFor:'Ben'}];
t.setBoard({owb:{jobs:queue,jobStates:{J4:{status:'blocked'},J7:{status:'done'}}},briefs:{approved:[
  {job:'J4',version:'v2',title:'Already approved but blocked',jobStatus:'open'},
  {job:'J7',version:'v1',title:'Approved and delivered',jobStatus:'open'}]}});
let c=t.workflowCounts(videoRows);
assert.equal(c.all,4);assert.equal(c.working+c.todo+c.blocked+c.waiting+c.stalled,c.all);
assert.equal(c.blocked,1);assert.equal(c.waiting,1);assert.equal(c.todo,1);
assert.equal(t.workflowCounts(videoRows,"HOS").all,1,"channel counts must match filtered rows");
assert.equal(c.needs,1);assert.equal(c.approved,2);
assert.equal(c.scheduled,1);assert.equal(c.live,1,'live publication stays visible despite unfinished work');
const duplicated=[...videoRows,{key:'OWB:OK:J7',lane:'done',youtube:{state:'scheduled',videoId:''}},
  {key:'DUPLICATE',youtube:{videoId:'scheduled01',state:'scheduled'}}];
assert.equal(t.workflowCounts(duplicated).scheduled,1,'approval placeholders and duplicate ids cannot inflate schedules');
assert(!t.pipelineVideos(duplicated).some(v=>v.key==='OWB:OK:J7'));
assert.equal(t.approvedRecords(videoRows).find(e=>e.job==='J4').jobStatus,'blocked');
assert.equal(t.approvedRecords(videoRows).find(e=>e.job==='J7').jobStatus,'done','completed approvals stay in history');
html=t.workflowJobHtml({...blocked,title:'<img src=x> Voiceover'});
assert(html.includes('Blocked because')&&html.includes('Next step')&&html.includes('You approved'));
assert(html.includes('&lt;img src=x&gt;')&&!html.includes('<img src=x>'));
// Reconcile the real published fixture too, when supplied, including every blocked job.
if(process.env.BOARD_FIXTURE){
 const b=JSON.parse(fs.readFileSync(process.env.BOARD_FIXTURE,'utf8'));t.setBoard(b);
 const count=t.workflowCounts(b.tracker.videos), expected=b.owb.jobs.filter(j=>j.status==='blocked').length;
 assert.equal(count.blocked,expected);assert.equal(count.all,b.owb.jobs.length);
 assert.equal(count.approved,b.briefs.approved.length);
 const pipeline=t.pipelineVideos(b.tracker.videos);
 assert.equal(count.scheduled,pipeline.filter(v=>v.youtube?.videoId&&v.youtube.state==='scheduled').length);
 assert.equal(count.live,pipeline.filter(v=>v.youtube?.videoId&&v.youtube.state==='live').length);
 const ids=b.owb.jobs.map(j=>j.id);assert.equal(new Set(ids).size,count.all);
 for(const j of b.owb.jobs)assert(t.workflowJobHtml(j).includes(`data-job="${j.id}"`));
 console.log(`Published fixture reconciled: ${count.all} current jobs, ${count.blocked} blocked, ${count.approved} approvals`);
}
t.setBoard({models:{chief:{name:'Gemini'}},owb:{jobStates:{}}});
assert(t.nextAction({kind:'chief',status:'open'}).startsWith('Gemini to claim'));
console.log('Tracker workflow regression checks passed');
