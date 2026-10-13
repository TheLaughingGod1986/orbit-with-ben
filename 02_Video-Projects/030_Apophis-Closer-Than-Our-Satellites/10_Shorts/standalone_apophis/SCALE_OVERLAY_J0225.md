# J0225 overlay handoff

Codex, 13 October 2026. No spend. Technical verification only; Chief retains visual approval.

Media is in this directory's code_graphics_v01/ on the Mac Mini: code_graphic_030short_r05_scale_v01.mov and matching PNG. Sidecar JSON records hashes, geometry, source and tick timings. Media is not committed.

Rebuild: python3 _build_code_graphic_scale_v01.py --earth ../../../023_What-Happened-To-Venus/07_Edit-Project/blue_marble.jpg

Requires Pillow, numpy, ffmpeg and macOS Arial Black. NASA Blue Marble reused from 023 (provenance in its code_graphics.py and 027's corresponding renderer). Original recorded URL: https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg . Texture projected onto shaded sphere. Both altitudes measured from surface. Yellow straight segment is a schematic flyby, not an orbit.

Assembly: start clip 0.5 s before trimmed VO word 36,000 (raw VO 18.58 s; realign after trimming). Ticks at offsets 0.5 and 1.1 s. Silent overlay; assembler adds house ticks. Composite straight alpha over moving graded plate, outside first 2 s and title interval. No corner credit on Short.

Verification: ProRes 4444 with alpha (decoded yuva444p12le), 1080x1920, 30 fps, 108 frames, 3.600 s. All 108 decoded alpha frames inside y 656–1264; endpoints transparent. Fully built bounds x 261–817 and y 695–1250. Measured Arial Black cap height 69 px; tick spacing 0.6 s; longest static hold 1.6 s. Full-build still inspected: labels clear of Earth and ring. TECHNICAL_CHECK_J0225.json records results.

Next: Chief visual review and downstream assembly. No final picture PASS issued.
