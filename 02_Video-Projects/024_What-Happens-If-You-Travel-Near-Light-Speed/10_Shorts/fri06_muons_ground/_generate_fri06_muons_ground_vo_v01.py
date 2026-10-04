#!/usr/bin/env python3
"""024 Light-speed Short Fri 6 (muons / ground) VO — Ben Orbit Narrator LOCK (orbit_voice).
Delegates to ../_short_vo_pipeline_v01.py
"""
from pathlib import Path
import subprocess, sys
subprocess.check_call([sys.executable, str(Path(__file__).resolve().parents[1] / "_short_vo_pipeline_v01.py"), "fri06_muons_ground"])
