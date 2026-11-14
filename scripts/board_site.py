"""The studio board address, shared by all Python clients."""
import json
import os
from pathlib import Path


def _config():
    return json.loads((Path(__file__).resolve().parents[1] / "studio/board_site.json").read_text())


def site_url():
    return (os.environ.get("BOARD_SITE_URL") or _config()["url"]).rstrip("/")


def read_url():
    """Where Mini/server tools read the board API, falling back to site_url() so Ben's links keep site_url()."""
    cfg = _config()
    return (os.environ.get("BOARD_READ_URL") or os.environ.get("BOARD_SITE_URL")
            or cfg.get("readUrl") or cfg["url"]).rstrip("/")
