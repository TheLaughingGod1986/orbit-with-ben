"""J1208 bounded Flow first takes. One submit per subject; no retries/fallback."""
import importlib.util, json, sys, time, subprocess, hashlib, os
from pathlib import Path
from playwright.sync_api import sync_playwright
OWB=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
HOS=Path('/Users/benjaminoats/YouTube/History Of Science')
sys.path.insert(0,str(OWB/'scripts'))
from cdp_tabs import reuse_page
spec=importlib.util.spec_from_file_location('account_reader',HOS/'02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py')
account=importlib.util.module_from_spec(spec);spec.loader.exec_module(account)
OUT=Path.home()/'_desk/handoff/J1208/flow-20261105'
PROMPTS={
'S5':'''Create one continuous 8 second vertical 9:16 realistic astronomical explanatory illustration. A single bright shooting star, a meteor, is already visibly travelling across a realistic dusk-to-night sky from the very first frame. A long luminous atmospheric streak travels steadily across the central sky for the opening four seconds above an unobtrusive low dark landscape. Wide sky view; the meteor remains clear within the vertical composition. Locked steady camera. Natural sky luminance and believable bright meteor light; some faint stars. This is an illustrative meteor, no named historical event. No exploding star, impact, macro fireball, constellations, labels, reticles, diagram, UI, captions, watermark, logos, Orbit or characters. No camera shake, zoom, still animation, reverse motion or repeated frames. Silent: no speech, music or sound.''',
'S6':'''Create one continuous 8 second vertical 9:16 realistic scientific explanatory illustration of the surface atmosphere of Saturn's moon Titan. An eye-level wide view over low-relief gently undulating terrain under a muted orange atmospheric haze, informed by Huygens optical appearance. Physically plausible subtle drifting haze changes visibly throughout the shot, including the first four seconds; soft diffuse amber light, natural terrain texture, level horizon. Locked steady camera. A general illustration, NOT a reconstruction of a measured landing location. The haze illustrates optical appearance only and does not measure pressure. No dramatic mountains, Earth-blue sky, underwater scene, rings in the sky, radar swath, fabricated scientific geometry, labels, diagram, UI, captions, watermark, logos, humans, Orbit or characters. No camera shake, zoom, still animation, reverse motion or repeated frames. Silent: no speech, music or sound.'''}
OUT.mkdir(parents=True,exist_ok=True)
logpath=OUT/'generation.json'
log=json.loads(logpath.read_text()) if logpath.exists() else {'job':'J1208','route':'Flow Veo 3.1 Fast via reused CDP 9222 tab','takes':{},'source_recipe':{'preroll':[0,1.15],'opening':[1.15,3.85],'speed':1,'classification':'generated explanatory illustration','disclosure_required':True,'approval':'PENDING; no KEEP'}}
def save():logpath.write_text(json.dumps(log,indent=2)+'\n')
def run(*args):subprocess.run([sys.executable,str(OWB/'scripts/ai_spend.py'),*args],cwd=OWB,check=True,capture_output=True)
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp('http://127.0.0.1:9222');page=reuse_page(b.contexts[0],'flow.google.com');page.set_default_timeout(5000)
 page.goto('https://flow.google.com/project/d7bceb4d-ec9b-4e01-8d9a-33fdd7c34ef9',wait_until='domcontentloaded');page.wait_for_timeout(2000)
 for subject,prompt in PROMPTS.items():
  if subject in log['takes']:
   if log['takes'][subject]['status']=='CANDIDATE_NOT_REVIEWED':continue
   raise SystemExit('STOP: existing submission record; inspect, never resubmit')
  page.keyboard.press('Escape');page.wait_for_timeout(300)
  back=page.locator('.cdk-overlay-backdrop').last
  if back.count() and back.is_visible():back.click(force=True)
  page.wait_for_timeout(300)
  page.locator('[aria-label="Account details"]').click();page.wait_for_timeout(1500)
  credits,who=account.read_account(page)
  if who!=account.REQUIRED or credits is None or credits<20:raise SystemExit('STOP: account/balance not verified')
  page.keyboard.press('Escape');page.wait_for_timeout(300)
  back=page.locator('.cdk-overlay-backdrop').last
  if back.count() and back.is_visible():back.click(force=True)
  page.wait_for_timeout(300)
  run('record','--pool','flow','--left',str(credits),'--by','codex','--note','J1208 live Flow preflight')
  page.get_by_role('button',name='Settings trigger',exact=True).click();page.wait_for_timeout(500)
  text=page.locator('body').inner_text()
  if 'Veo 3.1 - Fast' not in text:raise SystemExit('STOP wrong model')
  if 'Generating will use 10 credits' not in text:raise SystemExit('STOP price not 10')
  page.locator('button').filter(has_text='9:16').last.click();page.wait_for_timeout(300)
  # All settings remain visible after aspect changes. Use text filter to avoid role name whitespace.
  for label in ['8s','x1']:
   loc=page.locator('button').filter(has_text=__import__('re').compile('^'+label+'$')).last
   loc.click();page.wait_for_timeout(300)
  page.keyboard.press('Escape');page.wait_for_timeout(300)
  back=page.locator('.cdk-overlay-backdrop').last
  if back.count() and back.is_visible():back.click(force=True)
  page.wait_for_timeout(300)
  pill=page.get_by_role('button',name='Settings trigger',exact=True).inner_text()
  if not all(s in pill for s in ('8s','crop_9_16','x1')):raise SystemExit('STOP settings mismatch '+pill)
  editor=page.get_by_role('textbox',name='What do you want to create?',exact=True)
  editor.fill(prompt)
  # Existing start/end slots must be empty. No leftover source attachments allowed.
  if page.locator('button[aria-label*="Remove"]').count():raise SystemExit('STOP attached asset needs inspection')
  before=set(page.locator('img').evaluate_all('(es)=>es.map(e=>e.src)'))
  ent={'prompt':prompt,'before_credits':credits,'model':'Veo 3.1 - Fast','settings':pill,'status':'SUBMITTING','expected_credits':10,'project':page.url,'at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
  log['takes'][subject]=ent;save()
  # Exactly one click. Any uncertainty stops rather than retrying.
  page.get_by_role('button',name='Start generation',exact=True).click();page.wait_for_timeout(1200)
  run('spend','--pool','flow','--amount','10','--film','OWB:030','--what',f'J1208 {subject} Flow Veo3.1 Fast 8s candidate take1','--by','codex')
  ent['status']='SUBMITTED';save();print(subject,'submitted 10 credits',flush=True)
  dest=OUT/(subject+'_flow_t1.mp4');deadline=time.time()+360
  while time.time()<deadline and not dest.exists():
   page.wait_for_timeout(5000)
   body=page.locator('body').inner_text()
   if 'failed' in body.lower():ent['status']='FLOW_FAILURE';save();raise SystemExit('Flow failure; no retry')
   imgs=page.locator('img').all()
   for img in imgs:
    src=img.get_attribute('src') or ''
    if src in before:continue
    box=img.bounding_box()
    if not box or box['width']<80:continue
    img.hover();page.wait_for_timeout(1200)
    for url in page.locator('video').evaluate_all('(es)=>es.map(e=>e.currentSrc||e.src).filter(Boolean)'):
     response=page.context.request.get(url,timeout=30000)
     data=response.body()
     if response.ok and b'ftyp' in data[:64] and len(data)>150000:
      dest.write_bytes(data);break
    if dest.exists():break
   print(subject,'waiting; file=',dest.exists(),flush=True)
  if not dest.exists():ent['status']='NEEDS_HARVEST';save();raise SystemExit('STOP harvest timeout; do not remint')
  # Keep downloaded original; silent derivative is a separate file.
  silent=OUT/(subject+'_flow_t1_silent.mp4')
  subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-map','0:v:0','-c:v','copy','-an',str(silent)],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(silent)]))
  ent.update(status='CANDIDATE_NOT_REVIEWED',path=str(silent),sha256=hashlib.sha256(silent.read_bytes()).hexdigest(),probe=probe)
  page.keyboard.press('Escape');page.wait_for_timeout(500)
  page.locator('[aria-label="Account details"]').click();page.wait_for_timeout(1500)
  ent['after_credits'],_=account.read_account(page);save()
  print(subject,'saved',silent,ent['sha256'],flush=True)
print('DONE: candidates require exact-source review; no KEEP',flush=True)
