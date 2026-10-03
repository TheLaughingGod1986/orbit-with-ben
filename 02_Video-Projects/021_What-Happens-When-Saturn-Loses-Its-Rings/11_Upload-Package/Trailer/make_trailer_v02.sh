#!/bin/sh
# Saturn trailer v02 for the Buffer posts (Claude, PR #99 5967962897 + 5974650494).
# The film's own cold open, 0:00-0:18.0: VO ends at 17.40 ("...nothing around it at all."), the picture holds,
# then fades over 17.5-18.0, before the first chapter card (18.05). Full 16:9 frame centred on a blurred,
# darkened 9:16 copy of itself, so Saturn is never cropped out.
#   sh make_trailer_v02.sh <path/to/saturn_first_cut_v03f.mp4> [out.mp4]
set -e
SRC="$1"; OUT="${2:-saturn_long_trailer_v02_18s.mp4}"
[ -f "$SRC" ] || { echo "usage: sh make_trailer_v02.sh saturn_first_cut_v03f.mp4 [out.mp4]"; exit 1; }
ffmpeg -y -ss 0 -t 18.0 -i "$SRC" -filter_complex "\
[0:v]split[a][b];\
[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.18[bg];\
[b]scale=1080:-2[fg];\
[bg][fg]overlay=(W-w)/2:(H-h)/2,fade=t=out:st=17.5:d=0.5,format=yuv420p[v];\
[0:a]afade=t=out:st=17.5:d=0.5[au]" \
  -map "[v]" -map "[au]" -r 30 -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
echo "wrote $OUT"
