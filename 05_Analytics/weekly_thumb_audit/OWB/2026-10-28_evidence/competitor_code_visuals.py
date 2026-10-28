import csv,json,re,pathlib
import numpy as np
from PIL import Image
O=pathlib.Path(__file__).parent
# Manual visual coding of the four contact sheets, 28 Oct 2026; no automated OCR guesses.
lines='''THIS IS URANUS|large|white|scene|horizon with text centre|unfamiliar view of named planet|WEIRDEST
NEW THEORY|large|white|object|diagonal layered discs and central text|new explanation|NEW
WHAT WE FOUND|large|white|scene|central void inside starfield|concealed discovery|HIDING
DON'T GO HERE|large|white|scene|bright horizon below top text|forbidden location|BLACK HOLE
MOON BASE|large|white|scene|bright ground below top text|human settlement|DANGER
MERCURY MAKES NO SENSE|large|white|object|whole planet below top text|temperature contradiction|COLD
TRITON UPDATE|large|white|scene|geyser against planet and top text|new habitability result|HABITABLE
FINALLY SEEN|large|white|scene|false-colour band below top text|newly visible phenomenon|UNEXPECTED
MAGNETAR|large|white|object|cropped stellar limb and field lines|strange object identified|STRANGEST
DON'T GO HERE|large|white|scene|crater terrain below top text|landing impossibility|CAN'T LAND
WORMHOLE SIGNAL?|large|white|object|arrow points to small bright blur|evidence of exotic object|WORMHOLE
IT'S WAKING UP|large|white|object|bright flare below top text|switching-on event|FIRST TIME
10 BILLION YEARS OF EARTH|large|white|scene|dinosaur silhouette under top text|whole planetary lifetime|ENTIRE
SIGNAL ON MARS?|large|white|object|metal dome on red ground|hidden structures|HIDDEN
DARK ENERGY BREAKTHROUGH|large|white|object|blue object below top text|measurement breakthrough|FIRST TIME
THIS IS THE SUN|medium|black|object|portrait bright solar texture|extreme detail|MOST DETAILED
ATTACK ON ANDROMEDA|medium|white|object|diagonal galaxy with centre label|galactic interaction framed as attack|ATTACK
EXPLAINED IN TWO / HOW PLANETS FORM|small|white|object|portrait planet with stacked labels|mechanism explanation|FORMATION
EXPLAINED IN TWO / GENERAL RELATIVITY|small|white|object|portrait lens and grid with stacked labels|mechanism explanation|RELATIVITY
EINSTEIN HATED THIS IDEA.|large|white|face|cropped face below boxed text and diagram|famous-person disagreement|ENTANGLED
SOLAR SYSTEM|medium|white and yellow arrow|object|tiny reference ring above enormous stellar limb|scale surprise|LARGEST
[none]|none|none|object|bright centre with thin orbit-like paths|particle identity|GOD PARTICLE
[none readable]|none readable|yellow marker|object|portrait false-colour map and dashed circle|anomalous region|BIGGEST MYSTERY
95% DEATH RATE|large|white|scene|central character amid cells below top text|survival against odds|SURVIVED
WE LOST CONTROL|large|white|object|huge eye below top text|loss of control|TERRIFYING
HEY!|large|white|scene|two characters with speech arrow|interaction and personal relevance|HALF
LOST FOREVER|large|white|object|illuminated artefact face below top text|lost civilization|FIRST
100% VIRUS|large|white|scene|needle and human anatomy below top text|unexpected treatment|CURED
OMEGA ALIENS / EARTH|large|white|object|giant craft and tiny Earth reference|civilization scale|GODLIKE
IT'S IMPOSSIBLE*|large|white|scene|small craft against luminous barrier|travel limit|NEVER
[small label unreadable]|small|white|face|portrait anthropomorphic Sun|cooling hot familiar object|COOL DOWN
[none]|none|none|object|whole Earth centred in portrait|resource exhaustion|RUN OUT
Can You NEVER SLEEP?|medium|yellow and white|face|face under stacked question|human limit|NEVER
WHAT IS DUST?|medium|white and pink|object|magnifier and hand with stacked text|familiar thing redefined|NOT WHAT YOU THINK
This Organ Regrows Every Month!|small|white and pink|face|face under stacked label|regeneration surprise|REGROW
[small label unreadable]|small|white|object|radial vivid tendrils from centre|altered perception|MAGIC
Does STRESS Make You More Productive?|small|white and yellow|face|character and computer with stacked text|counterintuitive effect|STRESS
GRAVITY MATTERS / 10% increase|medium|white and orange|object|whole Earth between top and bottom text|physical what-if|10%
HOW DO SSRI ANTI-DEPRESSANTS REALLY WORK?|small|white and pink|object|portrait brain below stacked question|hidden mechanism|WORK
[paper labels unreadable]|small|blue and black|scene|brain and scattered papers|treatment mechanism|WORKS
Your Bones Produce Real Electricity!|small|white|object|skeleton under tiny label|body surprise|ELECTRIC
EBOLA / What Makes It So Hard to Stop?|medium|white and pink|object|Earth between top and bottom labels|persistence paradox|COMING BACK
How Does Flu Kill You?|small|white and pink|object|virus below stacked question|disease mechanism|DOES TO YOUR BODY
THIS COULD ACTUALLY HAPPEN.|small|white|object|small whole Earth under top label in dark portrait|unwanted planetary event|NEVER'''.splitlines()
order=json.loads((O/'coded_order.json').read_text()); assert len(lines)==len(order),(len(lines),len(order))
study=json.loads((O/'study.json').read_text());lookup={e['id']:e for g in study['groups'] for e in g['all_90d']}
rows=[]
for item,line in zip(order,lines):
 e=lookup[item['id']]; text,size,colour,subject,comp,gap,hook=line.split('|')
 with Image.open(O/'thumbs'/f"{e['id']}.jpg") as im:
  rgb=np.array(im.convert('RGB'),dtype=float);luma=rgb@np.array([.2126,.7152,.0722]); sat=np.asarray(im.convert('HSV'))[:,:,1]
 title=e['title'];shape='What happens if' if title.lower().startswith(('what if','what happens if')) else 'question' if title.endswith('?') else 'number' if re.search(r'\d',title) else 'statement'
 rows.append({'id':e['id'],'channel_format':item['group'],'title':title,'published':e['published'],'views':e['views'],'views_per_day':round(e['views_per_day'],2),'title_shape':shape,'title_chars':len(title),'title_hook':hook,'thumbnail_words':text,'text_size_relative_to_thumb':size,'text_colour':colour,'subject_type':subject,'composition':comp,'curiosity_gap':gap,'luma_std_whole_rendition':round(float(luma.std()),1),'near_black_pct_luma_lt20_whole_rendition':round(float((luma<20).mean()*100),1),'mean_saturation_whole_rendition':round(float(sat.mean()),1),'source':e['url']})
with (O/'visual_coding.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
print('Coded',len(rows))
