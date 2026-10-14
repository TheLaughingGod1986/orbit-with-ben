set -e
ED="/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project"; PK="$ED/full_rough_v05c_pack"; M=/private/tmp/024_LightSpeed_full_rough_v05c.mp4
cd "$ED"
python3 _overlay_light_speed_v05c.py
cd /Users/benjaminoats/YouTube/orbit-with-ben
python3 scripts/picture_qa.py $M --cuts "$PK/cuts_v05c.json" --pool "$ED/_evidence/light_speed_harvest_v01.json" --reviewed-ok "$PK/reviewed_ok_v05.json" --out-dir "$PK/picture_qa_v05c" > "$PK/picture_qa_v05c.txt" 2>&1 || echo "picture_qa exit $?" >> "$PK/picture_qa_v05c.txt"
python3 scripts/polish_gate.py $M --cuts "$PK/cuts_v05c.json" --reviewed-ok "$PK/reviewed_ok_v05.json" --out "$PK/polish_gate_v05c.json" > "$PK/polish_gate_v05c.txt" 2>&1 || echo "polish_gate exit $?" >> "$PK/polish_gate_v05c.txt"
A=$(ffmpeg -v error -i /private/tmp/024_LightSpeed_full_rough_v05b.mp4 -map 0:a -c copy -f md5 -); B=$(ffmpeg -v error -i $M -map 0:a -c copy -f md5 -)
printf '{"audio_md5_v05b":"%s","audio_md5_v05c":"%s","same_audio":%s}\n' "$A" "$B" $([ "$A" = "$B" ] && echo true || echo false) > "$PK/audio_v05c.json"
