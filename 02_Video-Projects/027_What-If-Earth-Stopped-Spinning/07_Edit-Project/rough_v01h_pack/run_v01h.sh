set -e
ED="/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project"; PK="$ED/rough_v01h_pack"; M=/private/tmp/027_EarthSpin_rough_v01h.mp4
cd "$ED"
python3 _overlay_earth_spin_v01h.py
cd /Users/benjaminoats/YouTube/orbit-with-ben
POOLS=""; for p in "$ED"/pool_v01*.json; do POOLS="$POOLS --pool $p"; done
python3 scripts/picture_qa.py $M --cuts "$PK/cuts_v01h.json" $POOLS --reviewed-ok "$PK/picture_qa_reviewed_ok_v01g.json" --out-dir "$PK/picture_qa_v01h" > "$PK/picture_qa_v01h.txt" 2>&1 || echo "picture_qa exit $?" >> "$PK/picture_qa_v01h.txt"
python3 scripts/polish_gate.py $M --cuts "$PK/cuts_v01h.json" --reviewed-ok "$PK/polish_reviewed_ok_v01g.json" --out "$PK/polish_gate_v01h.json" > "$PK/polish_gate_v01h.txt" 2>&1 || echo "polish_gate exit $?" >> "$PK/polish_gate_v01h.txt"
A=$(ffmpeg -v error -i /private/tmp/earth027_rough_work_v01g/027_EarthSpin_rough_v01g.mp4 -map 0:a -c copy -f md5 -); B=$(ffmpeg -v error -i $M -map 0:a -c copy -f md5 -)
printf '{"audio_md5_v01g":"%s","audio_md5_v01h":"%s","same_audio":%s}\n' "$A" "$B" $([ "$A" = "$B" ] && echo true || echo false) > "$PK/audio_v01h.json"
