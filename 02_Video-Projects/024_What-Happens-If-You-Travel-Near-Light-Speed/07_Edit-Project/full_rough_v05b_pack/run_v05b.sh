set -e
ED="/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project"; PK="$ED/full_rough_v05b_pack"; M=/private/tmp/024_LightSpeed_full_rough_v05b.mp4
cd "$ED"
python3 _assemble_light_speed_full_v05b.py
cd /Users/benjaminoats/YouTube/orbit-with-ben
python3 scripts/picture_qa.py $M --cuts "$PK/cuts_v05b.json" --pool "$ED/_evidence/light_speed_harvest_v01.json" --reviewed-ok "$PK/reviewed_ok_v05.json" --out-dir "$PK/picture_qa_v05b" > "$PK/picture_qa_v05b.txt" 2>&1 || echo "picture_qa exit $?" >> "$PK/picture_qa_v05b.txt"
python3 scripts/polish_gate.py $M --cuts "$PK/cuts_v05b.json" --reviewed-ok "$PK/reviewed_ok_v05.json" --out "$PK/polish_gate_v05b.json" > "$PK/polish_gate_v05b.txt" 2>&1 || echo "polish_gate exit $?" >> "$PK/polish_gate_v05b.txt"
ffmpeg -hide_banner -nostats -i $M -vf "blackdetect=d=0.5:pix_th=0.10,freezedetect=n=0.003:d=1" -an -f null - 2> /private/tmp/light024_v05b_fb.txt || true
grep -E 'black_start|freeze_(start|duration|end)' /private/tmp/light024_v05b_fb.txt > "$PK/freeze_black_v05b.txt" || true
A5=$(ffmpeg -v error -i /private/tmp/024_LightSpeed_full_rough_v05.mp4 -map 0:a -c copy -f md5 -); A5b=$(ffmpeg -v error -i $M -map 0:a -c copy -f md5 -)
L=$(ffmpeg -hide_banner -nostats -i $M -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | tr -s ' ' | tr '\n' ' ')
printf '{"audio_md5_v05":"%s","audio_md5_v05b":"%s","same_audio":%s,"ebur128":"%s"}\n' "$A5" "$A5b" $([ "$A5" = "$A5b" ] && echo true || echo false) "$L" > "$PK/audio_v05b.json"
