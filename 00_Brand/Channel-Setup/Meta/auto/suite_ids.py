#!/usr/bin/env python3
"""Locked Orbit Meta Business Suite IDs + Reels composer Share-step diagnosis.

The Facebook Page moved out of Benkay Creative on 2026-08-03. Opening the Reels
composer on the old portfolio / Instagram-only asset hangs on Share: the step
spinner never finishes, "Who can see this?" stays greyed out, and Suite shows
"options are only available for posts to a Facebook Page."
"""
from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

# Orbit with Ben portfolio + Page (see META_ACCOUNTS.json / PORTFOLIO.md).
ORBIT_BUSINESS_ID = "1352434763139246"
ORBIT_PAGE_ASSET_ID = "1285932871266399"
ORBIT_PAGE_ID = "61592833318203"

# Stale Benkay Creative portfolio + the IG/Suite asset used before the move.
BENKAY_BUSINESS_ID = "1203116147241086"
BENKAY_SUITE_ASSET_ID = "1251385088056874"
STALE_SUITE_IDS = frozenset({BENKAY_BUSINESS_ID, BENKAY_SUITE_ASSET_ID})

COMPOSER_PATH = "https://business.facebook.com/latest/reels_composer"
CONTENT_PATH = "https://business.facebook.com/latest/content_calendar"
HOME_PATH = "https://business.facebook.com/latest/home"

PAGE_ONLY_OPTION_MARKERS = (
    "only available for posts to a facebook page",
    "only available for posts to a facebook page.",
)
SHARE_READY_MARKERS = (
    "scheduling options",
    "share now",
)
SHARE_STEP_MARKERS = (
    "who can see this",
    "who can see this?",
)


def is_stale_suite_id(value: object) -> bool:
    return str(value or "").strip() in STALE_SUITE_IDS


def pin_suite_creds(creds: dict | None, accounts: dict | None = None) -> dict:
    """Copy creds and lock Orbit Page + portfolio IDs (never keep Benkay)."""
    data = dict(creds or {})
    accounts = accounts or {}
    portfolio = accounts.get("meta_business_portfolio") or {}
    facebook = accounts.get("facebook") or {}

    business = str(
        data.get("business_id")
        or portfolio.get("business_id")
        or ORBIT_BUSINESS_ID
    ).strip()
    asset = str(
        data.get("business_suite_asset_id")
        or facebook.get("business_suite_asset_id")
        or ORBIT_PAGE_ASSET_ID
    ).strip()
    page_id = str(
        data.get("page_id") or facebook.get("page_id") or ORBIT_PAGE_ID
    ).strip()

    if is_stale_suite_id(business) or not business or business.startswith("REPLACE_"):
        business = str(portfolio.get("business_id") or ORBIT_BUSINESS_ID).strip()
    if is_stale_suite_id(asset) or not asset or asset.startswith("REPLACE_"):
        asset = str(facebook.get("business_suite_asset_id") or ORBIT_PAGE_ASSET_ID).strip()
    if not page_id or page_id.startswith("REPLACE_"):
        page_id = str(facebook.get("page_id") or ORBIT_PAGE_ID).strip()

    data["business_id"] = business
    data["business_suite_asset_id"] = asset
    data["page_id"] = page_id
    data["business_portfolio_name"] = str(
        data.get("business_portfolio_name")
        or portfolio.get("name")
        or "Orbit with Ben"
    )
    return data


def _query_values(url: str) -> dict[str, list[str]]:
    return parse_qs(urlsplit(url).query, keep_blank_values=True)


def url_has_stale_suite_ids(url: str) -> bool:
    values = _query_values(url)
    for key in ("business_id", "asset_id"):
        for raw in values.get(key, []):
            if is_stale_suite_id(raw):
                return True
    return False


def suite_url(base: str, creds: dict | None = None) -> str:
    """Pin a Suite URL to the Orbit Page asset. Rewrites stale Benkay IDs."""
    pinned = pin_suite_creds(creds)
    asset = str(pinned.get("business_suite_asset_id") or "").strip()
    biz = str(pinned.get("business_id") or "").strip()
    parts = urlsplit(base or COMPOSER_PATH)
    query = parse_qs(parts.query, keep_blank_values=True)
    if asset and not asset.startswith("REPLACE_"):
        query["asset_id"] = [asset]
    if biz and not biz.startswith("REPLACE_"):
        query["business_id"] = [biz]
    new_query = urlencode(query, doseq=True)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))


def composer_url(creds: dict | None = None) -> str:
    return suite_url(COMPOSER_PATH, creds)


def suite_home_url(creds: dict | None = None) -> str:
    return suite_url(HOME_PATH, creds)


def is_composer_url(url: str) -> bool:
    return "reels_composer" in (url or "").lower()


def should_open_suite_composer(
    creds: dict | None = None, *, cdp_flag: bool = False
) -> bool:
    """True only when CDP is explicit.

    The 5-minute LaunchAgent used to fall back to Create reel whenever Graph
    tokens were missing, which reopened the hung Share tab after it was closed.
    Graph remains the default; pass --cdp or set preferred_method=cdp to opt in.
    """
    if cdp_flag:
        return True
    preferred = str((creds or {}).get("preferred_method") or "graph").lower()
    return preferred == "cdp"


def diagnose_share_step(page_text: str, url: str = "") -> dict:
    """Classify Meta Reels composer Share-step state from visible text + URL.

    hung_wrong_asset: Share spinner / greyed audience because the selected
    destination is not a Facebook Page (Instagram-only or stale Benkay IDs).
    Clicking Share in that state does nothing.
    """
    text = (page_text or "").lower()
    url = url or ""
    reasons: list[str] = []
    page_only = any(m in text for m in PAGE_ONLY_OPTION_MARKERS)
    who_can_see = any(m in text for m in SHARE_STEP_MARKERS)
    ready_ui = any(m in text for m in SHARE_READY_MARKERS)
    stale_url = url_has_stale_suite_ids(url)
    copyright_ok = "safe to publish" in text

    if stale_url:
        reasons.append("url_has_stale_benkay_ids")
    if page_only:
        reasons.append("page_only_options_message")
    if who_can_see:
        reasons.append("who_can_see_this_visible")
    if copyright_ok:
        reasons.append("copyright_check_passed")

    if stale_url or (page_only and who_can_see and not ready_ui):
        return {
            "state": "hung_wrong_asset",
            "needs_page_asset": True,
            "reasons": reasons,
            "hint": (
                "Reels Share is stuck because this composer is not the Orbit "
                "Facebook Page. Close extra Suite tabs and open the Page "
                f"composer: {composer_url()}"
            ),
        }

    if ready_ui:
        return {
            "state": "ready",
            "needs_page_asset": False,
            "reasons": reasons + ["share_ready_markers"],
            "hint": "",
        }

    if who_can_see and not page_only:
        return {
            "state": "ready",
            "needs_page_asset": False,
            "reasons": reasons + ["audience_controls_present"],
            "hint": "",
        }

    if "add video" in text or "select video" in text:
        return {
            "state": "create",
            "needs_page_asset": stale_url,
            "reasons": reasons + ["create_step"],
            "hint": "",
        }

    return {
        "state": "unknown",
        "needs_page_asset": stale_url,
        "reasons": reasons,
        "hint": "",
    }
