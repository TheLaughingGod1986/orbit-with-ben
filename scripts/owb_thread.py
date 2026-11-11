#!/usr/bin/env python3
"""The studio thread tool under its old name. The tool itself is scripts/studio_thread.py (11 Nov 2026).

Every brief, rule file and launchd job that runs `python3 scripts/owb_thread.py ...` keeps working, and a script that
imports this name gets the very same module, so nothing has to change on the Mini or the MacBook. New code uses
studio_thread.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import studio_thread  # noqa: E402

if __name__ == "__main__":
    studio_thread.main()
else:
    sys.modules[__name__] = studio_thread
