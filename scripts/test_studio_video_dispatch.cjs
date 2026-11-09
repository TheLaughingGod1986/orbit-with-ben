// Read-only Overview classification and featured-video dispatch semantics.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync(path.join(__dirname,'../05_Analytics/kanban/board_site/studio_app.js'),'utf8');
const context={Date,Intl,URLSearchParams,console,location:{hash:''},document:{getElementById:()=>({})},window:{}};
vm.createContext(context);
vm.runInContext(source.slice(0,source.indexOf('  // STUDIO_APP_TEST_HOOK'))+`
 globalThis.t={activityCategory,nextVideoTask,nextVideoWorkCard,activityCard,overview};
})();`,context);
const t=context.t,NOW=Date.parse('2026-11-04T14:30Z'),iso=minutes=>new Date(NOW+minutes*60000).toISOString();
function fixture(){
 const admin={id:'Jadmin',status:'claimed',by:'codex',title:'Daily Studio read',remaining_action:'Validate collected metrics and rebuild the tracker',claimedAt:iso(-10),progress:{step:2,of:4,at:iso(0)}};
 const next={id:'Jnext',status:'open',kind:'video',repo:'hos',film:'009',stage:'picture',title:'Generate remaining approved picture rows',remaining_action:'Generate the remaining scoped picture rows'};
 const video={key:'HOS:009',channel:'HOS',number:'009',type:'long',title:'Why Does the Moon Stay Up?',lane:'progress',jobs:[next],production:{milestones:[{id:'picture',label:'Picture',state:'doing',jobs:[next]}],activeStages:['picture'],eta:{state:'unavailable'}}};
 const board={publishedAt:iso(0),tracker:{videos:[video]},models:{checkedAt:iso(0),chief:{agent:'claude'},models:[]},owb:{jobs:[admin,next]},workflow:{at:iso(0),active:[],states:{Jadmin:{state:'running'},Jnext:{state:'queued'}},next:{...next,worker:'gemini'}}};
 return {board,video,admin,next};
}
{
 const {board,admin,next}=fixture();
 assert.equal(t.activityCategory(board,{...admin,taskKeys:['HOS:009']}).id,'analytics','analytics is not production just because linked to videos');
 assert.equal(t.activityCategory(board,{...next,title:'Implement capacity-aware dispatcher and portable overflow'}).id,'engineering');
 assert.equal(t.activityCategory(board,{...next,title:'Validate workflow handoff fixes'}).id,'engineering');
 assert.equal(t.activityCategory(board,{...next,title:'Monthly channel improvement review'}).id,'analytics');
 assert.equal(t.activityCategory(board,{...next,recheck_of:'Jparent',title:'Verify condition for Jparent'}).id,'coordination');
 assert.equal(t.activityCategory(board,{...next,title:'Chief: resolve 044 script orphan-review'}).id,'coordination');
 assert.equal(t.activityCategory(board,next).id,'production');
 assert.equal(t.activityCategory(board,{id:'other',title:'Check workstation'}).id,'operations');
 assert(t.activityCard(board,NOW).includes('data-category="analytics"'));
 board.progress24h={jobsDone:10,milestones:0,moved:[],hours:1};
 const home=t.overview(board,NOW);
 assert(home.indexOf('overview-activity')<home.indexOf('overview-p24'),'current work precedes lower-priority history');
}
{
 const {board,video}=fixture(),p=t.nextVideoTask(board,video,NOW);
 assert.equal(p.job.id,'Jnext');assert.equal(p.status,'Selected next · not yet claimed');
 assert.equal(p.timing,'Start time not confirmed');assert(p.context.includes('~10m remaining'));
 assert(p.context.includes('does not confirm when this video task starts'));
 assert(!p.timing.includes('10m'),'task ETA is never a start countdown');
 assert(t.nextVideoWorkCard(board,video,NOW).includes('#agents&job=Jnext'));
}
{
 const {board,video,next}=fixture();next.kind='chief';board.workflow.next.worker='claude';
 const p=t.nextVideoTask(board,video,NOW);
 assert.equal(p.status,'Chief decision queued');assert(p.responsibility.includes('Claude'));
 assert.equal(p.timing,'Start time not confirmed');
 next.status='blocked';next.hold={type:'chief'};board.workflow.states.Jnext.state='review';
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Chief decision queued','ready Chief review is not an external input wait');
}
{
 const {board,video,next}=fixture();next.status='blocked';next.hold={type:'credits'};board.workflow.states.Jnext.state='waiting';
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Waiting for credit');
 assert(t.nextVideoTask(board,video,NOW).timing.includes('resolving the recorded hold'));
 next.hold={type:'ben'};assert.equal(t.nextVideoTask(board,video,NOW).status,'Waiting for your approval');
}
{
 const {board,video,next}=fixture();next.after='Jdep';board.workflow.next=null;
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Waiting for a prerequisite');
 board.owb.jobStates={Jdep:{status:'done'}};
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Queued for this video','completed predecessor need not still be in live jobs');
}
{
 const {board,video,next}=fixture();next.status='claimed';next.by='gemini';next.claimedAt=iso(-1);next.progress={step:1,of:4,at:iso(0)};board.workflow.states.Jnext.state='running';
 const p=t.nextVideoTask(board,video,NOW);
 assert.equal(p.status,'Working on this video');assert.equal(p.timing,'Already started');assert.equal(p.context,'');
 next.status='open';board.workflow.active=[{id:'Jnext',worker:'gemini',phase:'starting',mode:'starting',startedAt:iso(-1),expiresAt:iso(2)}];board.workflow.states.Jnext.state='starting';
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Worker starting · claim pending');
}
{
 const {board,video}=fixture();board.publishedAt=board.models.checkedAt=board.workflow.at=iso(-120);
 const p=t.nextVideoTask(board,video,NOW);
 assert.notEqual(p.status,'Selected next · not yet claimed');assert(p.timing.includes('stale'));assert(!p.context.includes('~10m'));
}
{
 const {board,video,next}=fixture();next.status='claimed';next.by='gemini';board.workflow.states.Jnext.state='stalled';
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Claim recorded · activity unconfirmed');
}
{
 const {board,video,next}=fixture();next.status='claimed';next.by='gemini';next.claimedAt=iso(-30);next.progress={step:1,of:3,at:iso(-20)};board.workflow.states.Jnext.state='running';
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Claim recorded · activity unconfirmed','fresh board alone is not fresh work evidence');
}
{
 const {board,video,next}=fixture();next.stage='vo';video.production.milestones[0].jobs=[];
 assert.equal(t.nextVideoTask(board,video,NOW).status,'Next task not recorded','unrelated VO is not Picture successor');
 assert.equal(t.nextVideoTask(board,{...video,lane:'ready',readyFor:'Ben'},NOW),null);
 assert.equal(t.nextVideoTask(board,{...video,youtube:{state:'scheduled'}},NOW),null);
 assert.equal(t.nextVideoTask(board,{...video,production:{scope:'unconfirmed_cut',projectHistory:video.production}},NOW),null);
}
{
 const {board,video}=fixture();board.workflow.next={id:'Jengineering',title:'Fix dispatcher capacity'};
 assert.equal(t.nextVideoTask(board,video,NOW).dispatchNote,'Next recorded dispatch: Engineering.');
 video.title='<img src=x onerror=alert(1)>';
 const html=t.nextVideoWorkCard(board,video,NOW);assert(html.includes('&lt;img'));assert(!html.includes('<img'));
}
{
 const {board,video,admin}=fixture();admin.title='Check source quotations';admin.remaining_action='Review direct evidence';admin.film='059';
 assert(t.nextVideoTask(board,video,NOW).context.includes('on another video'),'other-film work is not presented as featured-video progress');
}
console.log('Studio video-dispatch checks PASS: category, actual stage handoff, selected/queued/working/starting/held/stale, task ETA separation, dependencies, scope, links and escaping');
