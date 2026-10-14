set -e
ED="/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project"; PK="$ED/rough_v05c_pack"; M=/private/tmp/026_NearestStar_v05c_PHONE.mp4
cd "$ED"
python3 _overlay_nearest_star_v05c.py
cd /Users/benjaminoats/YouTube/orbit-with-ben
python3 scripts/picture_qa.py $M --cuts "$PK/cuts_v05c.json" --pool "$ED/pool_v03.json" --reviewed-ok "$PK/polish_reviewed_ok_v05b.json" --out-dir "$PK/picture_qa_v05c" > "$PK/picture_qa_v05c.txt" 2>&1 || echo "picture_qa exit $?" >> "$PK/picture_qa_v05c.txt"
python3 scripts/polish_gate.py $M --cuts "$PK/cuts_v05c.json" --reviewed-ok "$PK/polish_reviewed_ok_v05b.json" --out "$PK/polish_gate_v05c.json" > "$PK/polish_gate_v05c.txt" 2>&1 || echo "polish_gate exit $?" >> "$PK/polish_gate_v05c.txt"
A=$(ffmpeg -v error -i /private/tmp/nearest026_rough_work_v05b/026_NearestStar_v05b_PHONE.mp4 -map 0:a -c copy -f md5 -); B=$(ffmpeg -v error -i $M -map 0:a -c copy -f md5 -)
printf '{"audio_md5_v05b":"%s","audio_md5_v05c":"%s","same_audio":%s}\n' "$A" "$B" $([ "$A" = "$B" ] && echo true || echo false) > "$PK/audio_v05c.json"
