#!/usr/bin/env python3
"""Hook for YouTube publish-now scripts: mirror one short to Threads after Public."""
from __future__ import annotations

import sys
from pathlib import Path

AUTO = Path(__file__).resolve().parent
# Force this package's modules ahead of Meta/TikTok siblings on sys.path
sys.path = [str(AUTO)] + [p for p in sys.path if p != str(AUTO)]


import importlib.util as _ilu
from pathlib import Path as _P
def _threads_load(name: str):
    auto = _P(__file__).resolve().parent
    key = f"orbit_threads_auto_{name}"
    import sys as _sys
    if key in _sys.modules:
        return _sys.modules[key]
    path = auto / f"{name}.py"
    spec = _ilu.spec_from_file_location(key, path)
    mod = _ilu.module_from_spec(spec)
    _sys.modules[key] = mod
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

load = _threads_load

caption = load("caption")
config = load("config")
discover = load("discover")
ensure_chrome = load("ensure_chrome")
graph_publish = load("graph_publish")
ledger = load("ledger")
studio_upload = load("studio_upload")


def notify_short_live(project_root: str | Path, short: dict) -> dict:
    """
    Call after a short is set Public on YouTube.

    Prefers CDP (THREADS_CREDENTIALS preferred_method=cdp) so local MP4s work.
    Graph API is used when token + threads_user_id + public media URL are ready.
    """
    project_root = Path(project_root)
    item = dict(short)
    item["_project"] = project_root.name
    if ledger.is_posted(item):
        return {"status": "already_posted", "key": item.get("video_id")}

    path = discover.resolve_file(project_root, item)
    if not path or not path.exists():
        return {"status": "missing_file", "file": item.get("file")}

    text = caption.threads_caption(item)
    needle = caption.confirm_needle(item, text)
    creds = config.load_credentials()
    ready, missing = config.credentials_ready(creds)
    preferred = str(creds.get("preferred_method") or "cdp").lower()
    audit_dir = AUTO.parent / "audit" / "auto"

    result: dict
    if preferred == "graph" and ready:
        result = graph_publish.publish_video(
            video_path=path, caption=text, creds=creds
        )
        if result.get("status") != "ok":
            # Fall back to CDP for local files
            chrome = ensure_chrome.ensure_chrome()
            if chrome.get("ok"):
                result = studio_upload.post_short(
                    video_path=path,
                    caption=text,
                    confirm_needle=needle,
                    audit_dir=audit_dir,
                    port=chrome.get("port"),
                )
    else:
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
        if result.get("status") not in {"ok", "unconfirmed"} and ready:
            graph = graph_publish.publish_video(
                video_path=path, caption=text, creds=creds
            )
            if graph.get("status") == "ok":
                result = graph

    if result.get("status") in {"ok", "unconfirmed"}:
        ledger.mark_posted(item, result)
    return result
