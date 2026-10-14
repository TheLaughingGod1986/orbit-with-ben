#!/bin/bash
set -e
cd /private/tmp/j0148-codex-wt
EP=02_Video-Projects/026_How-Far-Is-The-Nearest-Star
PK="$EP/07_Edit-Project/rough_v05d_pack"
python3 "$EP/07_Edit-Project/_overlay_nearest_star_v05d.py"
python3 scripts/picture_qa.py /private/tmp/026_NearestStar_v05d_PHONE.mp4 --cuts "$PK/cuts_v05d.json" --pool "$EP/07_Edit-Project/pool_v03.json" --reviewed-ok "$PK/polish_reviewed_ok_v05b.json" --out-dir "$PK/picture_qa_v05d" > "$PK/picture_qa_v05d.txt" 2>&1
python3 scripts/polish_gate.py /private/tmp/026_NearestStar_v05d_PHONE.mp4 --cuts "$PK/cuts_v05d.json" --reviewed-ok "$PK/polish_reviewed_ok_v05b.json" --out "$PK/polish_gate_v05d.json" > "$PK/polish_gate_v05d.txt" 2>&1
