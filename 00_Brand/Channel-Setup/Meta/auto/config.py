#!/usr/bin/env python3
"""Load Meta credentials for Orbit shorts auto-post."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SETUP = Path(__file__).resolve().parents[1]
AUTO = Path(__file__).resolve().parent
CREDS = SETUP / "META_CREDENTIALS.json"
EXAMPLE = SETUP / "META_CREDENTIALS.example.json"
ACCOUNTS = SETUP / "META_ACCOUNTS.json"

if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

from _sib import load  # noqa: E402

suite_ids = load("suite_ids")


def load_accounts() -> dict:
    if ACCOUNTS.exists():
        return json.loads(ACCOUNTS.read_text())
    return {}


def load_credentials() -> dict:
    """Merge file credentials with env overrides and lock Orbit Suite IDs."""
    data: dict = {}
    if CREDS.exists():
        data = json.loads(CREDS.read_text())
    elif EXAMPLE.exists():
        # Example only — never treat placeholders as ready
        data = {"_from_example": True}

    def env(key: str, *aliases: str) -> str | None:
        for k in (key, *aliases):
            v = os.environ.get(k)
            if v:
                return v
        return None

    overrides = {
        "access_token": env("META_ACCESS_TOKEN", "FACEBOOK_ACCESS_TOKEN"),
        "page_access_token": env("META_PAGE_ACCESS_TOKEN", "FACEBOOK_PAGE_ACCESS_TOKEN"),
        "page_id": env("META_PAGE_ID", "FACEBOOK_PAGE_ID"),
        "instagram_business_account_id": env(
            "META_IG_USER_ID", "INSTAGRAM_BUSINESS_ACCOUNT_ID"
        ),
        "instagram_username": env("META_IG_USERNAME", "INSTAGRAM_USERNAME"),
    }
    for k, v in overrides.items():
        if v:
            data[k] = v

    if "page_access_token" not in data and data.get("access_token"):
        data["page_access_token"] = data["access_token"]

    data.setdefault("publish_instagram", True)
    data.setdefault("publish_facebook", True)
    data.setdefault("preferred_method", "graph")
    data.setdefault("cdp_port", 9223)
    return suite_ids.pin_suite_creds(data, load_accounts())


def credentials_ready(creds: dict | None = None) -> tuple[bool, list[str]]:
    creds = creds or load_credentials()
    missing: list[str] = []
    if creds.get("_from_example"):
        missing.append("META_CREDENTIALS.json (copy from META_CREDENTIALS.example.json)")
    token = creds.get("page_access_token") or creds.get("access_token")
    if not token or str(token).startswith("REPLACE_"):
        missing.append("access_token / page_access_token")
    if creds.get("publish_facebook") and (
        not creds.get("page_id") or str(creds.get("page_id")).startswith("REPLACE_")
    ):
        missing.append("page_id")
    if creds.get("publish_instagram") and (
        not creds.get("instagram_business_account_id")
        or str(creds.get("instagram_business_account_id")).startswith("REPLACE_")
    ):
        missing.append("instagram_business_account_id")
    return (len(missing) == 0, missing)
