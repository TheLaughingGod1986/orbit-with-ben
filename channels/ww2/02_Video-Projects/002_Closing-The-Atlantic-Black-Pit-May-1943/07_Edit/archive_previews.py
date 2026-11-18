#!/usr/bin/env python3
"""Build archive inspection sheet and a no-text thumbnail candidate, never publish."""
import argparse,json,pathlib
from PIL import Image,ImageOps,ImageDraw,ImageFont

def main():
 p=argparse.ArgumentParser();p.add_argument('--media',type=pathlib.Path,required=True);a=p.parse_args()
 film=pathlib.Path(__file__).resolve().parents[1];records=json.loads((film/'07_Edit/ARCHIVE_HARVEST.json').read_text());out=a.media/'03_Picture/previews';out.mkdir(parents=True,exist_ok=True)
 font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
 sheet=Image.new('RGB',(1440,390*((len(records)+2)//3)),(240,237,228));d=ImageDraw.Draw(sheet)
 for i,r in enumerate(records):
  x=(i%3)*480;y=(i//3)*390
  if r.get('file'):
   with Image.open(r['file']) as im:tile=ImageOps.contain(im.convert('RGB'),(460,310));sheet.paste(tile,(x+(480-tile.width)//2,y+10))
  d.text((x+12,y+326),f"{r['key']} | {r['id']}",font=font,fill='black');d.text((x+12,y+354),r.get('date',''),font=font,fill='black')
 sheet.save(out/'archive_contact_v01.jpg',quality=93)
 r=next((r for r in records if r['key']=='P1' and r.get('file')),None)
 if r:
  with Image.open(r['file']) as im:
   thumb=ImageOps.fit(ImageOps.autocontrast(im.convert('L')), (1280,720),centering=(.5,.45)).convert('RGB')
  thumb.save(out/'thumbnail_A_candidate_v01.jpg',quality=96)
  ImageOps.contain(thumb,(168,94)).save(out/'thumbnail_A_phone_v01.jpg',quality=95)
 print(out)
if __name__=='__main__':main()
