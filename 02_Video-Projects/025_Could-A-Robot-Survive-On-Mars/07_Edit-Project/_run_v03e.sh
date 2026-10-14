#!/bin/bash
# J0068 v03e: render, then picture_qa and music_gate on the cut (AGENTS.md lesson 7). Run detached in tmux.
set -u
ROOT=/Users/benjaminoats/YouTube/orbit-with-ben
EP=$ROOT/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars
ED=$EP/07_Edit-Project
PACK=$ED/full_rough_v03e_pack
CUT=/private/tmp/mars025_full_work_v03e/025_MarsRobot_full_rough_v03e.mp4
cd "$ED" || exit 2
python3 _assemble_mars_robot_full_v03e.py || exit 3
python3 "$ROOT/scripts/picture_qa.py" "$CUT" --cuts "$PACK/cuts_v03e.json" --pool "$ED/nasa_pool_v01.json" --out-dir "$PACK" --reviewed-ok "$PACK/polish_reviewed_ok_v03e.json" > "$PACK/picture_qa_v03e.txt" 2>&1
PQ=$?
cd "$ROOT" || exit 2
python3 scripts/music_gate.py "$EP" --bed "$EP/05_Music/mars-robot_score_bed_v02_full.mp3" --video "$CUT" \
  --others 02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/05_Music/saturn-rings_score_bed_v01.mp3 \
           02_Video-Projects/022_Is-the-Sun-Getting-Brighter/05_Music/sun-brighter_score_bed_v01.mp3 \
  --out "$PACK/music_gate.json" > "$PACK/music_gate_v03e.txt" 2>&1
MG=$?
echo "picture_qa=$PQ music_gate=$MG" > "$PACK/gates_exit_v03e.txt"
[ $PQ -eq 0 ] && [ $MG -eq 0 ] || exit 4
UAT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
ffmpeg -y -hide_banner -i "$CUT" -c:v libx264 -preset medium -crf 23 -maxrate 1800k -bufsize 3600k -c:a aac -b:a 160k -movflags +faststart /tmp/025_MarsRobot_v03e_PHONE.mp4 || exit 5
cp /tmp/025_MarsRobot_v03e_PHONE.mp4 "$UAT/025_MarsRobot_v03e_PHONE.mp4" || exit 5
