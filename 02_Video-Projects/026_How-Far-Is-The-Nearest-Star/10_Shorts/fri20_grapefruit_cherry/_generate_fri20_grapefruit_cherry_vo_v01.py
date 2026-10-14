#!/usr/bin/env python3
"""026 Nearest star Short Fri 20 Nov (Grapefruit / cherry scale) VO — Ben Orbit Narrator LOCK (orbit_voice).
Delegates to ../_short_vo_pipeline_v01.py
"""
from pathlib import Path
import subprocess, sys
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parents[1] / "_short_vo_pipeline_v01.py"), "fri20_grapefruit_cherry"])
