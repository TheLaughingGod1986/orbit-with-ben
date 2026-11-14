"""The studio board address, shared by all Python clients."""
import json
import os
from pathlib import Path
from urllib.request import Request


def site_url():
    override = os.environ.get("BOARD_SITE_URL")
    if override:
        return override.rstrip("/")
    setting = Path(__file__).resolve().parents[1] / "studio/board_site.json"
    return json.loads(setting.read_text())["url"].rstrip("/")


def board_request(url):
    """Identify studio tools: Cloudflare rejects urllib's default user agent."""
    return Request(url, headers={"User-Agent": "studio-kanban client"})
