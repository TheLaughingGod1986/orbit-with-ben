#!/usr/bin/env python3
"""Unit tests for Orbit Meta Reels composer Share-step pinning."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

AUTO = Path(__file__).resolve().parent
if str(AUTO) not in sys.path:
    sys.path.insert(0, str(AUTO))

import suite_ids  # noqa: E402


SCREENSHOT_SHARE_HANG = """
Create Edit Share
Who can see this?
Public
Restricted
Distribution
Additional options
options are only available for posts to a Facebook Page.
Your video is safe to publish! No copyright issues were found.
Orbit with Ben
Back
Share
"""

STALE_COMPOSER = (
    "https://business.facebook.com/latest/reels_composer"
    "?asset_id=1251385088056874&business_id=1203116147241086"
)


class PinSuiteCredsTests(unittest.TestCase):
    def test_replaces_benkay_ids_with_orbit_page(self):
        pinned = suite_ids.pin_suite_creds(
            {
                "business_id": suite_ids.BENKAY_BUSINESS_ID,
                "business_suite_asset_id": suite_ids.BENKAY_SUITE_ASSET_ID,
                "page_id": "REPLACE_WITH_FACEBOOK_PAGE_ID",
            }
        )
        self.assertEqual(pinned["business_id"], suite_ids.ORBIT_BUSINESS_ID)
        self.assertEqual(
            pinned["business_suite_asset_id"], suite_ids.ORBIT_PAGE_ASSET_ID
        )
        self.assertEqual(pinned["page_id"], suite_ids.ORBIT_PAGE_ID)

    def test_fills_missing_ids_from_accounts(self):
        pinned = suite_ids.pin_suite_creds(
            {},
            {
                "meta_business_portfolio": {"business_id": suite_ids.ORBIT_BUSINESS_ID},
                "facebook": {
                    "business_suite_asset_id": suite_ids.ORBIT_PAGE_ASSET_ID,
                    "page_id": suite_ids.ORBIT_PAGE_ID,
                },
            },
        )
        self.assertEqual(pinned["business_id"], suite_ids.ORBIT_BUSINESS_ID)
        self.assertEqual(
            pinned["business_suite_asset_id"], suite_ids.ORBIT_PAGE_ASSET_ID
        )


class ComposerUrlTests(unittest.TestCase):
    def test_composer_url_pins_orbit_page(self):
        url = suite_ids.composer_url(
            {
                "business_id": suite_ids.BENKAY_BUSINESS_ID,
                "business_suite_asset_id": suite_ids.BENKAY_SUITE_ASSET_ID,
            }
        )
        self.assertIn(f"asset_id={suite_ids.ORBIT_PAGE_ASSET_ID}", url)
        self.assertIn(f"business_id={suite_ids.ORBIT_BUSINESS_ID}", url)
        self.assertNotIn(suite_ids.BENKAY_BUSINESS_ID, url)
        self.assertNotIn(suite_ids.BENKAY_SUITE_ASSET_ID, url)

    def test_suite_url_rewrites_stale_query(self):
        url = suite_ids.suite_url(STALE_COMPOSER, {})
        self.assertFalse(suite_ids.url_has_stale_suite_ids(url))
        self.assertTrue(suite_ids.url_has_stale_suite_ids(STALE_COMPOSER))


class DiagnoseShareStepTests(unittest.TestCase):
    def test_screenshot_hang_is_wrong_asset(self):
        result = suite_ids.diagnose_share_step(SCREENSHOT_SHARE_HANG, STALE_COMPOSER)
        self.assertEqual(result["state"], "hung_wrong_asset")
        self.assertTrue(result["needs_page_asset"])
        self.assertIn("page_only_options_message", result["reasons"])
        self.assertIn("reels_composer", result["hint"])
        self.assertIn(suite_ids.ORBIT_PAGE_ASSET_ID, result["hint"])

    def test_page_only_message_without_stale_url_still_hangs(self):
        result = suite_ids.diagnose_share_step(SCREENSHOT_SHARE_HANG)
        self.assertEqual(result["state"], "hung_wrong_asset")

    def test_share_now_is_ready(self):
        result = suite_ids.diagnose_share_step(
            "Scheduling options\nShare now\nWho can see this?\nPublic"
        )
        self.assertEqual(result["state"], "ready")
        self.assertFalse(result["needs_page_asset"])

    def test_create_step(self):
        result = suite_ids.diagnose_share_step("Create reel\nAdd video\nUpload")
        self.assertEqual(result["state"], "create")


class ConfigPinTests(unittest.TestCase):
    def test_load_credentials_overrides_benkay(self):
        from _sib import load

        config = load("config")
        pinned = config.suite_ids.pin_suite_creds(
            {
                "business_id": suite_ids.BENKAY_BUSINESS_ID,
                "business_suite_asset_id": suite_ids.BENKAY_SUITE_ASSET_ID,
            },
            config.load_accounts(),
        )
        self.assertEqual(pinned["business_id"], suite_ids.ORBIT_BUSINESS_ID)
        self.assertEqual(
            pinned["business_suite_asset_id"], suite_ids.ORBIT_PAGE_ASSET_ID
        )

    def test_load_credentials_always_returns_orbit_page(self):
        from _sib import load

        config = load("config")
        creds = config.load_credentials()
        self.assertEqual(creds["business_id"], suite_ids.ORBIT_BUSINESS_ID)
        self.assertEqual(
            creds["business_suite_asset_id"], suite_ids.ORBIT_PAGE_ASSET_ID
        )


if __name__ == "__main__":
    unittest.main()
