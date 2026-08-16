#!/usr/bin/env python3
"""Hook for YouTube publish-now scripts: mirror one short to IG + FB after Public."""
from __future__ import annotations

import sys
from pathlib import Path

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from _sib import load

caption = load("caption")
config = load("config")
discover = load("discover")
ensure_chrome = load("ensure_chrome")
graph_publish = load("graph_publish")
ledger = load("ledger")
studio_upload = load("studio_upload")
suite_ids = load("suite_ids")


def notify_short_live(project_root: str | Path, short: dict) -> dict:
    """
    Call after a short is set Public on YouTube.

    Tries Graph API first (when META_CREDENTIALS.json is ready).
    Does not open Meta Create reel unless preferred_method is cdp.
    """
    project_root = Path(project_root)
    item = dict(short)
    item["_project"] = project_root.name
    if ledger.is_posted(item):
        return {"status": "already_posted", "key": item.get("video_id")}

    path = discover.resolve_file(project_root, item)
    if not path or not path.exists():
        return {"status": "missing_file", "file": item.get("file")}

    text = caption.meta_caption(item)
    needle = caption.confirm_needle(item, text)
    creds = config.load_credentials()
    ready, missing = config.credentials_ready(creds)
    preferred = str(creds.get("preferred_method") or "graph").lower()
    audit_dir = AUTO.parent / "audit" / "auto"

    result: dict
    if preferred == "graph" and ready:
        result = graph_publish.publish_both(
            video_path=path, caption=text, creds=creds
        )
    elif suite_ids.should_open_suite_composer(creds):
        chrome = ensure_chrome.ensure_chrome()
        if not chrome.get("ok"):
            return {
                "status": "chrome_unavailable",
                "error": chrome.get("error"),
                "graph_missing": missing,
            }
        result = studio_upload.post_short(
            video_path=path,
            caption=text,
            confirm_needle=needle,
            audit_dir=audit_dir,
            port=chrome.get("port"),
        )
        if result.get("status") not in {"ok"} and ready:
            graph = graph_publish.publish_both(
                video_path=path, caption=text, creds=creds
            )
            if graph.get("status") in {"ok", "partial"}:
                result = graph
    elif ready:
        result = graph_publish.publish_both(
            video_path=path, caption=text, creds=creds
        )
    else:
        return {
            "status": "graph_credentials_missing",
            "graph_missing": missing,
            "hint": "Not opening Meta Create reel. Set Graph tokens or preferred_method=cdp.",
        }

    if result.get("status") in {"ok", "partial"}:
        ledger.mark_posted(item, result)
    return result
