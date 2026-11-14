"""The studio board address, shared by all Python clients."""
import json
import os
from pathlib import Path

def site_url():
    return os.environ.get("BOARD_SITE_URL", json.loads((Path(__file__).resolve().parents[1] / "studio/board_site.json").read_text())["url"]).rstrip("/")
