#!/bin/bash
# J2478: Trim 2 (drop Line 2) spliced from supermoon_vo_v01, sentence gaps tightened to 0.30 s. No API call, never overwrites.
set -euo pipefail
cd "$(dirname "$0")/.."
IN=supermoon_vo_v01.wav; OUT=supermoon_vo_v03.wav
[ "$(shasum -a 256 "$IN" | cut -d' ' -f1)" = "26bfe66c4ec83e66e9abccd599db22903095d09b0776c0a4c623d94d732a17a3" ] || { echo "input is not the recorded v01"; exit 1; }
[ -e "$OUT" ] && { echo "$OUT exists"; exit 1; }
seg() { echo "[0:a]atrim=$1:$2,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st=$(echo "$2-$1-0.01" | bc):d=0.01[$3]"; }
G="anullsrc=r=48000:cl=stereo,atrim=0:0.22"
ffmpeg -hide_banner -loglevel error -i "$IN" -filter_complex "
$(seg 0 4.32 a);$(seg 9.45 14.68 b);$(seg 15.43 20.16 c);$(seg 21.01 23.36 d);
$G[g1];$G[g2];$G[g3];
[a][g1][b][g2][c][g3][d]concat=n=7:v=0:a=1[o]" -map "[o]" -c:a pcm_s16le -ar 48000 -ac 2 "$OUT"
