#!/bin/sh
# Nearest Star trailer v01 for the Buffer posts (J0326), same build as Light Speed / Mars:
# the film's own cold open, cut before the first chapter card.
# VO ends at 32.70 ("...to get there."). Chapter card "The Star You Cannot See" starts at 33.54
# (overlays_v05d.json card_0). The picture holds, then fades over 33.0-33.5.
# "Full film on YouTube" sits in the lower band from 30.5 s (STUDIO_PLAYBOOK §12).
# Full 16:9 frame centred on a blurred, darkened 9:16 copy of itself.
#   sh make_trailer_v01.sh <path/to/026_NearestStar_v05d.mp4> [out.mp4]
set -e
SRC="$1"; OUT="${2:-nearest_star_long_trailer_v01_34s.mp4}"
[ -f "$SRC" ] || { echo "usage: sh make_trailer_v01.sh 026_NearestStar_v05d.mp4 [out.mp4]"; exit 1; }
CARD="$(dirname "$0")/full_film_card_v01.png"
python3 - "$CARD" <<'EOF'
import sys
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
t = "Full film on YouTube"
w = d.textlength(t, font=f)
d.text(((W - w) / 2, 1560), t, font=f, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 230))
im.save(sys.argv[1])
EOF
ffmpeg -y -ss 0 -t 33.5 -i "$SRC" -loop 1 -t 33.5 -i "$CARD" -filter_complex "\
[0:v]split[a][b];\
[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.18[bg];\
[b]scale=1080:-2[fg];\
[1:v]format=rgba,fade=t=in:st=30.5:d=0.4:alpha=1[card];\
[bg][fg]overlay=(W-w)/2:(H-h)/2[v0];\
[v0][card]overlay=0:0:enable='gte(t,30.5)',fade=t=out:st=33.0:d=0.5,format=yuv420p,setsar=1[v];\
[0:a]afade=t=out:st=33.0:d=0.5[au]" \
  -map "[v]" -map "[au]" -r 30 -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
echo "wrote $OUT"
