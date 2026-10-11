set -e
cd "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project"
O=code_out_v06; P=python3
$P code_graphics.py speed $O/row03 --seconds 6.6
$P code_graphics.py bulge $O/row08 --seconds 12.5 --label '43 km wider'
$P code_graphics.py air $O/row10 --seconds 14 --label 'the air keeps going'
$P code_graphics.py air $O/row11 --seconds 14 --label 'the air keeps going' --label2 'faster than sound'
$P code_graphics.py speed $O/row13 --seconds 12 --label 'Britain 1,000 km/h' --label2 'faster than a jet'
$P code_graphics.py oceans $O/row17 --seconds 5.4
$P code_graphics.py oceans $O/row18-19 --seconds 15 --label 'polar oceans' --label2 'one band of land'
$P code_graphics.py dayyear $O/row20 --seconds 16 --label '1 day = 1 year'
$P code_graphics.py tides $O/row24-25 --seconds 24 --label '4 cm a year'
$P code_graphics.py clock $O/row30 --seconds 5.0 --label '22 hours'
$P code_graphics.py clock $O/row33 --seconds 12
$P code_graphics.py tides $O/row35 --seconds 14
$P code_graphics.py speed $O/row35 --seconds 12
find $O -name '*.png' -delete; find $O -type d -empty -delete
