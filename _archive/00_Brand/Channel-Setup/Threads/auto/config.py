#!/usr/bin/env python3
"""Load Threads credentials for Orbit shorts auto-post."""
from __future__ import annotations

import json
import os
from pathlib import Path

SETUP = Path(__file__).resolve().parents[1]
CREDS = SETUP / "THREADS_CREDENTIALS.json"
EXAMPLE = SETUP / "THREADS_CREDENTIALS.example.json"
ACCOUNTS = SETUP / "THREADS_ACCOUNTS.json"


def load_accounts() -> dict:
    if ACCOUNTS.exists():
        return json.loads(ACCOUNTS.read_text())
    return {}


def load_credentials() -> dict:
    """Merge file credentials with env overrides."""
    data: dict = {}
    if CREDS.exists():
        data = json.loads(CREDS.read_text())
    elif EXAMPLE.exists():
        data = {"_from_example": True}

    def env(key: str, *aliases: str) -> str | None:
        for k in (key, *aliases):
            v = os.environ.get(k)
            if v:
                return v
        return None

    overrides = {
        "access_token": env("THREADS_ACCESS_TOKEN"),
        "threads_user_id": env("THREADS_USER_ID"),
        "threads_username": env("THREADS_USERNAME", "THREADS_HANDLE"),
        "app_id": env("THREADS_APP_ID"),
        "app_secret": env("THREADS_APP_SECRET"),
    }
    for k, v in overrides.items():
        if v:
            data[k] = v

    data.setdefault("threads_username", "orbitwithben")
    data.setdefault("username", data.get("threads_username", "orbitwithben"))
    data.setdefault("preferred_method", "cdp")
    data.setdefault("cdp_port", 9222)
    return data


def credentials_ready(creds: dict | None = None) -> tuple[bool, list[str]]:
    creds = creds or load_credentials()
    missing: list[str] = []
    if creds.get("_from_example"):
        missing.append(
            "THREADS_CREDENTIALS.json (copy from THREADS_CREDENTIALS.example.json)"
        )
    token = creds.get("access_token")
    if not token or str(token).startswith("REPLACE_"):
        missing.append("access_token")
    uid = creds.get("threads_user_id")
    if not uid or str(uid).startswith("REPLACE_"):
        missing.append("threads_user_id")
    return (len(missing) == 0, missing)
