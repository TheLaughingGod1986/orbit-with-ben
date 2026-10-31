"""Run only the two authorized J1100 pickups under the external pool lock."""
import sys,json,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
repo=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
sys.path.insert(0,str(repo/'04_Audio/tools'))
from el_auth import load_token
from el_client import request
import vo_take
out=repo/'02_Video-Projects'
evidence=Path('/Users/benjaminoats/_desk/reviews/J1100/pickups_1031')
evidence.mkdir(parents=True,exist_ok=True)
plans=[('027_What-If-Earth-Stopped-Spinning','J1100_s2_open_pickup_v01',"Why do you weigh less at Earth's equator? You weigh about half a percent less there."),('028_A-Star-Is-Coming-Toward-Us','J1100_s5_open_pickup_v01','How close will Gliese 710 come to the Sun?')]
for film,stem,text in plans:
 dest=out/film/'02_Voiceover'
 if (dest/(stem+'_TAKE.json')).exists():
  print('Already completed:',stem,flush=True);continue
 assert shutil.disk_usage('/private/tmp').free>=6*1024**3
 token,mode=load_token(prefer_api_key=True)
 code,body,_=request('GET','/v1/user/subscription',token,mode,timeout=60)
 assert code==200, f'subscription HTTP {code}'
 d=json.loads(body)
 safe={k:d.get(k) for k in ['status','tier','character_count','character_limit','can_extend_character_limit','allowed_to_extend_character_limit']}
 safe['at']=datetime.now(timezone.utc).isoformat()
 (evidence/(stem+'_balance.json')).write_text(json.dumps(safe,indent=2)+'\n')
 assert d.get('status')=='active'
 assert d.get('can_extend_character_limit') is False and d.get('allowed_to_extend_character_limit') is False
 remaining=d['character_limit']-d['character_count']
 assert remaining>=len(text)+100
 subprocess.run([sys.executable,str(repo/'scripts/ai_spend.py'),'record','--by','codex','--pool','elevenlabs','--left',str(remaining),'--total',str(d['character_limit']),'--note','J1100 fresh subscription balance under pool lock'],check=True)
 rc=vo_take.main(['--text',text,'--out',str(dest),'--stem',stem,'--order','J1100-Chief-29Oct-h41'])
 assert rc==0, f'vo_take returned {rc}'
 print('Completed:',stem,flush=True)
