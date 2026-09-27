#!/usr/bin/env python3
"""Threads Graph API publish (when THREADS_CREDENTIALS has token + user id)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://graph.threads.net/v1.0"


def _post(url: str, form: dict) -> tuple[int, dict | str]:
    body = urllib.parse.urlencode(form).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as resp:
            raw = resp.read().decode()
            try:
                return resp.status, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw) if raw else {"error": str(e)}
        except json.JSONDecodeError:
            return e.code, {"error": raw or str(e)}


def _get(url: str) -> tuple[int, dict | str]:
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            raw = resp.read().decode()
            try:
                return resp.status, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw) if raw else {"error": str(e)}
        except json.JSONDecodeError:
            return e.code, {"error": raw or str(e)}


def publish_video(
    *,
    video_path: Path,
    caption: str,
    creds: dict,
) -> dict:
    """
    Threads video publish requires a publicly reachable video_url.
    Local files need staging (MEDIA_PUBLIC_BASE_URL) — CDP is preferred locally.
    """
    user_id = creds.get("threads_user_id")
    token = creds.get("access_token")
    if not user_id or not token:
        return {"status": "missing_credentials", "error": "missing threads_user_id or access_token"}

    public_base = (creds.get("media_public_base_url") or "").rstrip("/")
    if not public_base:
        return {
            "status": "needs_public_url",
            "method": "graph",
            "hint": "Set media_public_base_url or use preferred_method=cdp",
        }

    video_path = Path(video_path)
    video_url = f"{public_base}/{video_path.name}"

    status, body = _post(
        f"{API}/{user_id}/threads",
        {
            "media_type": "VIDEO",
            "video_url": video_url,
            "text": caption,
            "access_token": token,
        },
    )
    if status >= 400 or not isinstance(body, dict) or not body.get("id"):
        return {
            "status": "container_failed",
            "method": "graph",
            "http": status,
            "response": body,
        }

    creation_id = str(body["id"])
    ready = False
    last = None
    for _ in range(40):
        st, sb = _get(
            f"{API}/{creation_id}?fields=status,error_message&access_token={urllib.parse.quote(token)}"
        )
        last = sb
        if isinstance(sb, dict):
            code = str(sb.get("status") or "").upper()
            if code in {"FINISHED", "PUBLISHED"}:
                ready = True
                break
            if code == "ERROR":
                return {
                    "status": "processing_error",
                    "method": "graph",
                    "creation_id": creation_id,
                    "response": sb,
                }
        time.sleep(2)
    if not ready:
        return {
            "status": "processing_timeout",
            "method": "graph",
            "creation_id": creation_id,
            "response": last,
        }

    pub_status, pub_body = _post(
        f"{API}/{user_id}/threads_publish",
        {"creation_id": creation_id, "access_token": token},
    )
    if pub_status >= 400 or not isinstance(pub_body, dict) or not pub_body.get("id"):
        return {
            "status": "publish_failed",
            "method": "graph",
            "creation_id": creation_id,
            "http": pub_status,
            "response": pub_body,
        }

    media_id = str(pub_body["id"])
    username = creds.get("threads_username") or creds.get("username") or "orbitwithben"
    return {
        "status": "ok",
        "method": "graph",
        "media_id": media_id,
        "creation_id": creation_id,
        "url": f"https://www.threads.net/@{username}",
        "permalink": f"https://www.threads.net/@{username}/post/{media_id}",
    }
