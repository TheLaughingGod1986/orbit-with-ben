#!/usr/bin/env python3
"""
Publish Orbit shorts to Instagram Reels + Facebook Page Reels via Graph API.

Uses Meta resumable upload so local files work without a public media URL.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH = "https://graph.facebook.com/v21.0"


def _req(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict | None = None,
    form: dict | None = None,
) -> tuple[int, dict | str]:
    hdrs = dict(headers or {})
    body = data
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
    request = urllib.request.Request(url, data=body, headers=hdrs, method=method)
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


def _token(creds: dict) -> str:
    return creds.get("page_access_token") or creds.get("access_token") or ""


def publish_instagram_reel(
    *,
    video_path: Path,
    caption: str,
    creds: dict,
) -> dict:
    ig_id = creds.get("instagram_business_account_id")
    token = _token(creds)
    if not ig_id or not token:
        return {"status": "missing_credentials", "platform": "instagram"}
    if not creds.get("publish_instagram", True):
        return {"status": "disabled", "platform": "instagram"}

    video_path = Path(video_path)
    size = video_path.stat().st_size

    # 1) Create resumable REELS container
    create_url = f"{GRAPH}/{ig_id}/media"
    status, body = _req(
        create_url,
        method="POST",
        form={
            "media_type": "REELS",
            "upload_type": "resumable",
            "caption": caption,
            "share_to_feed": "true",
            "access_token": token,
        },
    )
    if status >= 400 or not isinstance(body, dict) or not body.get("id"):
        return {
            "status": "container_failed",
            "platform": "instagram",
            "http": status,
            "response": body,
        }

    container_id = str(body["id"])
    upload_uri = body.get("uri") or body.get("upload_url")
    if not upload_uri:
        # Some Graph versions return uri under nested keys
        upload_uri = (body.get("video_upload") or {}).get("uri")
    if not upload_uri:
        return {
            "status": "missing_upload_uri",
            "platform": "instagram",
            "container_id": container_id,
            "response": body,
        }

    # 2) Upload binary to rupload
    video_bytes = video_path.read_bytes()
    up_status, up_body = _req(
        upload_uri,
        method="POST",
        data=video_bytes,
        headers={
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(size),
            "Content-Type": "application/octet-stream",
        },
    )
    if up_status >= 400:
        return {
            "status": "upload_failed",
            "platform": "instagram",
            "container_id": container_id,
            "http": up_status,
            "response": up_body,
        }

    # 3) Poll container
    ready = False
    last_code = None
    for _ in range(45):
        st, sb = _req(
            f"{GRAPH}/{container_id}?fields=status_code,status&access_token={urllib.parse.quote(token)}"
        )
        if isinstance(sb, dict):
            last_code = sb.get("status_code") or (sb.get("status") or {}).get("code")
            if last_code == "FINISHED":
                ready = True
                break
            if last_code == "ERROR":
                return {
                    "status": "processing_error",
                    "platform": "instagram",
                    "container_id": container_id,
                    "response": sb,
                }
        time.sleep(2)
    if not ready:
        return {
            "status": "processing_timeout",
            "platform": "instagram",
            "container_id": container_id,
            "last_code": last_code,
        }

    # 4) Publish
    pub_status, pub_body = _req(
        f"{GRAPH}/{ig_id}/media_publish",
        method="POST",
        form={"creation_id": container_id, "access_token": token},
    )
    if pub_status >= 400 or not isinstance(pub_body, dict) or not pub_body.get("id"):
        return {
            "status": "publish_failed",
            "platform": "instagram",
            "container_id": container_id,
            "http": pub_status,
            "response": pub_body,
        }

    media_id = str(pub_body["id"])
    permalink = None
    try:
        _, per = _req(
            f"{GRAPH}/{media_id}?fields=permalink&access_token={urllib.parse.quote(token)}"
        )
        if isinstance(per, dict):
            permalink = per.get("permalink")
    except Exception:
        pass

    return {
        "status": "ok",
        "platform": "instagram",
        "media_id": media_id,
        "container_id": container_id,
        "url": permalink,
    }


def publish_facebook_reel(
    *,
    video_path: Path,
    caption: str,
    creds: dict,
) -> dict:
    page_id = creds.get("page_id")
    token = _token(creds)
    if not page_id or not token:
        return {"status": "missing_credentials", "platform": "facebook"}
    if not creds.get("publish_facebook", True):
        return {"status": "disabled", "platform": "facebook"}

    video_path = Path(video_path)
    size = video_path.stat().st_size

    # Start upload session
    start_status, start_body = _req(
        f"{GRAPH}/{page_id}/video_reels",
        method="POST",
        form={
            "upload_phase": "start",
            "file_size": str(size),
            "access_token": token,
        },
    )
    if start_status >= 400 or not isinstance(start_body, dict):
        return {
            "status": "start_failed",
            "platform": "facebook",
            "http": start_status,
            "response": start_body,
        }

    video_id = start_body.get("video_id")
    upload_url = start_body.get("upload_url")
    if not video_id or not upload_url:
        return {
            "status": "missing_upload_session",
            "platform": "facebook",
            "response": start_body,
        }

    video_bytes = video_path.read_bytes()
    up_status, up_body = _req(
        upload_url,
        method="POST",
        data=video_bytes,
        headers={
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(size),
            "Content-Type": "application/octet-stream",
        },
    )
    if up_status >= 400:
        return {
            "status": "upload_failed",
            "platform": "facebook",
            "video_id": video_id,
            "http": up_status,
            "response": up_body,
        }

    finish_status, finish_body = _req(
        f"{GRAPH}/{page_id}/video_reels",
        method="POST",
        form={
            "upload_phase": "finish",
            "video_id": str(video_id),
            "video_state": "PUBLISHED",
            "description": caption,
            "access_token": token,
        },
    )
    if finish_status >= 400:
        return {
            "status": "finish_failed",
            "platform": "facebook",
            "video_id": video_id,
            "http": finish_status,
            "response": finish_body,
        }

    return {
        "status": "ok",
        "platform": "facebook",
        "video_id": str(video_id),
        "url": f"https://www.facebook.com/reel/{video_id}",
        "response": finish_body if isinstance(finish_body, dict) else None,
    }


def publish_both(
    *,
    video_path: Path,
    caption: str,
    creds: dict,
) -> dict:
    platforms: dict = {}
    if creds.get("publish_instagram", True):
        platforms["instagram"] = publish_instagram_reel(
            video_path=video_path, caption=caption, creds=creds
        )
    else:
        platforms["instagram"] = {"status": "disabled", "platform": "instagram"}

    if creds.get("publish_facebook", True):
        platforms["facebook"] = publish_facebook_reel(
            video_path=video_path, caption=caption, creds=creds
        )
    else:
        platforms["facebook"] = {"status": "disabled", "platform": "facebook"}

    ok_statuses = {"ok", "disabled", "skipped"}
    all_ok = all(p.get("status") in ok_statuses for p in platforms.values())
    any_ok = any(p.get("status") == "ok" for p in platforms.values())
    return {
        "status": "ok" if all_ok else ("partial" if any_ok else "failed"),
        "method": "graph",
        "platforms": platforms,
    }
