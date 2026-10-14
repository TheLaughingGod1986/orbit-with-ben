set -e
ED="/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/07_Edit-Project"; PK="$ED/full_rough_v05d_pack"; M=/private/tmp/024_LightSpeed_full_rough_v05d.mp4
cd "$ED"
python3 _assemble_light_speed_full_v05d.py
python3 _overlay_light_speed_v05d.py
cd /Users/benjaminoats/YouTube/orbit-with-ben
python3 scripts/picture_qa.py $M --cuts "$PK/cuts_v05d.json" --pool "$ED/_evidence/light_speed_harvest_v01.json" --reviewed-ok "$PK/reviewed_ok_v05d.json" --out-dir "$PK/picture_qa_v05d" > "$PK/picture_qa_v05d.txt" 2>&1 || echo "picture_qa exit $?" >> "$PK/picture_qa_v05d.txt"
python3 scripts/polish_gate.py $M --cuts "$PK/cuts_v05d.json" --reviewed-ok "$PK/reviewed_ok_v05d.json" --out "$PK/polish_gate_v05d.json" > "$PK/polish_gate_v05d.txt" 2>&1 || echo "polish_gate exit $?" >> "$PK/polish_gate_v05d.txt"
A=$(ffmpeg -v error -i /private/tmp/024_LightSpeed_full_rough_v05c.mp4 -map 0:a -c copy -f md5 -); B=$(ffmpeg -v error -i $M -map 0:a -c copy -f md5 -)
printf '{"audio_md5_v05c":"%s","audio_md5_v05d":"%s","same_audio":%s}\n' "$A" "$B" $([ "$A" = "$B" ] && echo true || echo false) > "$PK/audio_v05d.json"
ffmpeg -hide_banner -i $M -vf "blackdetect=d=0.1:pix_th=0.10:pic_th=0.98,freezedetect=n=-50dB:d=1" -an -f null - 2>&1 | grep -E "black_|freeze" > "$PK/freeze_black_v05d.txt" || true
python3 - "$M" "$PK" <<'EOF'
import sys, subprocess as sp
from PIL import Image, ImageDraw
m, pk = sys.argv[1], sys.argv[2]
def grab(t, w):
    p = f'/tmp/v05d_{t:.2f}.jpg'
    sp.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', m, '-frames:v', '1', '-vf', f'scale={w}:-2', p], check=True)
    return Image.open(p)
grab(11.9, 1920).save(f'{pk}/row2_still_v05d.jpg', quality=90)
ts = [6.0, 7.0, 8.0, 9.0, 9.7, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 14.0]
board = Image.new('RGB', (4 * 480, 3 * 290), (18, 18, 22)); d = ImageDraw.Draw(board)
for i, t in enumerate(ts):
    x, y = i % 4 * 480, i // 4 * 290
    board.paste(grab(t, 480), (x, y)); d.text((x + 6, y + 274), f'0:{t:05.2f}', fill='white')
board.save(f'{pk}/strip_0m06_0m14_v05d.jpg', quality=88)
EOF
cp $M "$ED/024_LightSpeed_full_rough_v05d.mp4"
