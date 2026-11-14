#!/bin/sh
# J01 Journey Film 01 vertical trailer v01 for Buffer posts (J2823, STUDIO_PLAYBOOK §12).
# Cold open VO ends at 49.840 s ("It begins right where you are sitting.").
# Chapter Card 1 ("Part 1 — Earth's Rotation") begins at 50.162 s.
# We take 0.000-50.125 s of the cold open and hold the final cold-open frame for 0.875 s
# to 51.000 s (1224 frames at 24 fps CFR), fading video and audio over 50.50-51.00 s.
# "Full film on YouTube" sits in the lower band from 47.50 s.
# Full 16:9 frame (608x342) centred on a blurred, darkened 9:16 (608x1080) copy of itself,
# loudnormed to -14.0 LUFS.
set -e
SRC="${1:-/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4}"
OUT="${2:-/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package/Trailer/j01_trailer_v01.mp4}"
[ -f "$SRC" ] || { echo "missing source video: $SRC"; exit 1; }
mkdir -p "$(dirname "$OUT")"

WORK_DIR="/Volumes/MiniWork/scratch/j01_trailer_build"
mkdir -p "$WORK_DIR"
CARD="$WORK_DIR/full_film_card_v01.png"
PASS1="$WORK_DIR/j01_trailer_pass1.mp4"

python3 - "$CARD" <<'EOF'
import sys
from PIL import Image, ImageDraw, ImageFont
W, H = 608, 1080
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
t = "Full film on YouTube"
w = d.textlength(t, font=f)
d.text(((W - w) / 2, 878), t, font=f, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 230))
im.save(sys.argv[1])
EOF

ffmpeg -y -ss 0 -t 50.125 -i "$SRC" -loop 1 -t 51.0 -i "$CARD" -filter_complex "\
[0:v]tpad=stop_mode=clone:stop_duration=0.875,split[a][b];\
[a]scale=608:1080:force_original_aspect_ratio=increase,crop=608:1080,gblur=sigma=24,eq=brightness=-0.18[bg];\
[b]scale=608:342[fg];\
[1:v]format=rgba,fade=t=in:st=47.5:d=0.4:alpha=1[card];\
[bg][fg]overlay=(W-w)/2:(H-h)/2[v0];\
[v0][card]overlay=0:0:enable='gte(t,47.5)',fade=t=out:st=50.5:d=0.5,fps=24,format=yuv420p,setsar=1[v];\
[0:a]apad=pad_dur=0.875,atrim=0:51.0,afade=t=out:st=50.5:d=0.5[au]" \
  -map "[v]" -map "[au]" -r 24 -fps_mode cfr -c:v libx264 -crf 18 -preset medium -c:a pcm_s16le "$PASS1"

STATS=$(ffmpeg -hide_banner -nostats -i "$PASS1" -af loudnorm=I=-14.0:TP=-1.0:LRA=11.0:print_format=json -f null - 2>&1 | awk '/^{/,/^}/')
MI=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin)['input_i'])")
MTP=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin)['input_tp'])")
MLRA=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin)['input_lra'])")
MTH=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin)['input_thresh'])")
OFF=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin)['target_offset'])")

ffmpeg -y -i "$PASS1" \
  -c:v copy \
  -af "loudnorm=I=-14.0:TP=-1.0:LRA=11.0:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTH}:offset=${OFF}:linear=true,aresample=48000" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUT"

rm -rf "$WORK_DIR"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,avg_frame_rate -show_entries format=duration -of json "$OUT"
echo "wrote $OUT"
