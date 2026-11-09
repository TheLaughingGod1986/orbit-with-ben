#!/usr/bin/env python3
"""031 row-specific alpha scale overlays. £0; moving composites still required.

Duration brackets are qualitative: 'a few hundred' is not assigned an invented
number. Generation cells are a literal tally at 25 years per generation, not
portraits or a demographic model. Gravity bars share zero and a common scale.
"""
from PIL import Image, ImageDraw
from mechanism_graphics import W, H, GOLD, WHITE, BLUE, ease
from evidence_graphics import caption, main as render

SPECS = [
    dict(row=36, mode='durations', start_s=373.84, duration_s=4.88,
         cue='The collapse took', source_rows=[14], alpha=True,
         geometry='Qualitative brackets; lengths do not encode unspecified durations'),
    dict(row=44, mode='gravity', start_s=449.92, duration_s=2.28,
         cue='with just over a third', source_rows=[17], alpha=True,
         geometry='Common zero; Mars 0.38 relative to Earth 1.00'),
    dict(row=52, mode='generations', start_s=534.48, duration_s=3.44,
         cue='For forty to four hundred human generations', source_rows=[18], alpha=True,
         geometry='400 cells; first 40 blue; remaining 360 gold; each cell = one generation'),
]


def bracket(dr, x, y, width, p, colour):
    end=x+round(width*ease(p))
    dr.line((x,y,end,y),fill=colour,width=6)
    for xx in (x,end):dr.line((xx,y-16,xx,y+16),fill=colour,width=5)


def durations(dr,t):
    # Two equal qualitative brackets avoid implying a measured 300-year phase.
    # Text stays in the right half, leaving the aurora plate's left side clear.
    if t<2.34:
        bracket(dr,1080,620,640,t/.9,BLUE)
        caption(dr,(1400,510),'COLLAPSE',54,WHITE,t,0,2.34)
        caption(dr,(1400,735),'A FEW HUNDRED YEARS',48,GOLD,t,.66,2.34)
    if t>=2.34:
        bracket(dr,1080,620,640,(t-2.34)/.7,BLUE)
        caption(dr,(1400,510),'WEAK PHASE',54,WHITE,t,2.34,4.88)
        caption(dr,(1400,735),'LESS THAN 1,000 YEARS',48,GOLD,t,3.58,4.88)


def gravity(dr,t):
    # Labels are the body names and physical quantity from the locked line.
    x0,x1=1080,1740
    p=ease(t/.92)
    for y,ratio,name,colour in [(510,1.,'EARTH',WHITE),(730,.38,'MARS',BLUE)]:
        dr.line((x0,y,x1,y),fill=(110,125,145,140),width=3)
        dr.rounded_rectangle((x0,y-15,x0+max(1,660*ratio*p),y+15),radius=8,fill=colour)
        caption(dr,(1400,y-75),name,48,colour,t,0,2.28)
    caption(dr,(1400,325),'GRAVITY',54,WHITE,t,0,2.28)
    caption(dr,(1400,870),'0.38 × EARTH',52,GOLD,t,.92,2.28)


def generations(dr,t):
    # Two rows of 20 cells = 40; twenty rows = 400. Numeric endpoints follow VO.
    n=round(40*ease(t/.7)) if t<1.04 else 40+round(360*ease((t-1.04)/.72))
    for i in range(400):
        x=1150+(i%20)*25; y=355+(i//20)*23
        colour=(BLUE if i<40 else GOLD) if i<n else (110,125,145,100)
        dr.rounded_rectangle((x,y,x+16,y+14),radius=3,fill=colour)
    caption(dr,(1400,260),'40 GENERATIONS',52,BLUE,t,.2,1.04)
    caption(dr,(1400,260),'40–400 HUMAN GENERATIONS',48,GOLD,t,1.04,3.44)
    caption(dr,(1400,900),'1,000–10,000 YEARS',48,WHITE,t,1.86,3.44)


def frame(spec,t):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    globals()[spec['mode']](ImageDraw.Draw(im),t)
    opacity=max(0,min(1,t/.4,(spec['duration_s']-t)/.4))
    im.putalpha(im.getchannel('A').point(lambda p:round(p*opacity)))
    return im


def main(argv=None):
    return render(argv,specs=SPECS,render_frame=frame)


if __name__=='__main__':main()
