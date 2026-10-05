#!/usr/bin/env python3
"""026 Nearest star Short Mon 16 Nov (You Can't See the Nearest Star) VO — Ben Orbit Narrator LOCK (orbit_voice).
Delegates to ../_short_vo_pipeline_v01.py
"""
from pathlib import Path
import subprocess, sys
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parents[1] / "_short_vo_pipeline_v01.py"), "mon16_cant_see_nearest_star"])
