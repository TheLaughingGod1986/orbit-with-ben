#!/usr/bin/env python3
"""Finish Instagram connection: Confirm on Page settings + Claim in Suite + Continue on Home."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
CDP = "http://127.0.0.1:9222"
ORBIT_BUSINESS = "1352434763139246"
ORBIT_ASSET = "1285932871266399"
PAGE_ID = "61592833318203"


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), full_page=True, timeout=15000)
        print("shot", name)
    except Exception as e:
        print("shot fail", name, e)


def dump(page) -> dict:
    text = ""
    try:
        text = page.inner_text("body")
    except Exception:
        pass
    pwd_count = 0
    try:
        pwd_count = page.locator('input[type="password"]').count()
    except Exception:
        pass
    return {
        "url": page.url,
        "snip": text[:2500],
        "password_field": pwd_count > 0,
        "connect_instagram": bool(re.search(r"Connect Instagram", text, re.I)),
        "no_ig_added": bool(re.search(r"No Instagram accounts added", text, re.I)),
        "review_connection": bool(
            re.search(
                r"Review Connection|Review account connection|Confirm your connection|confirm the connection|Get more features",
                text,
                re.I,
            )
        ),
        "orbitwithben": "orbitwithben" in text.lower(),
        "connected_complete": bool(re.search(r"Connected Instagram", text, re.I))
        and not bool(
            re.search(r"Review account connection|only includes some features", text, re.I)
        ),
    }


def click_force(page, pattern: str) -> str | None:
    try:
        loc = page.get_by_role("button", name=re.compile(pattern, re.I))
        if loc.count():
            loc.first.click(timeout=5000, force=True)
            return f"role:{pattern}"
    except Exception as e:
        print(" role click fail", pattern, str(e)[:120])
    try:
        loc = page.get_by_text(re.compile(pattern, re.I))
        if loc.count():
            loc.first.click(timeout=5000, force=True)
            return f"text:{pattern}"
    except Exception as e:
        print(" text click fail", pattern, str(e)[:120])
    try:
        ok = page.evaluate(
            """(pat) => {
              const re = new RegExp(pat, 'i');
              const nodes = [...document.querySelectorAll('button,[role=button],a,[role=link],div[tabindex]')];
              for (const el of nodes) {
                const t = (el.innerText || el.getAttribute('aria-label') || '').trim();
                if (re.test(t) && t.length < 80) {
                  el.click();
                  return t;
                }
              }
              return null;
            }""",
            pattern,
        )
        if ok:
            return f"js:{ok}"
    except Exception as e:
        print(" js click fail", pattern, str(e)[:120])
    return None


def dismiss_overlays(page) -> None:
    for pat in [r"^Done$", r"^Close$", r"^Not now$", r"^Dismiss$", r"^Skip$", r"^Got it$", r"^Maybe later$"]:
        try:
            loc = page.get_by_role("button", name=re.compile(pat, re.I))
            if loc.count() and loc.first.is_visible():
                loc.first.click(timeout=2000, force=True)
                page.wait_for_timeout(700)
                print("dismissed", pat)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
    except Exception:
        pass


def main() -> None:
    log: dict = {"steps": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]

        def _d(d):
            try:
                d.dismiss()
            except Exception:
                try:
                    d.accept()
                except Exception:
                    pass

        ctx.on("dialog", _d)

        # ===== Path C: Page settings Confirm =====
        page = ctx.new_page()
        page.on("dialog", _d)
        try:
            page.goto(
                "https://www.facebook.com/settings?tab=linked_instagram",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4000)
            info = dump(page)
            print("C start review=", info["review_connection"], "pwd=", info["password_field"])
            if "Confirm" not in info["snip"] and "Get more features" not in info["snip"]:
                clicked = click_force(page, r"^Review Connection$")
                print("reopen review", clicked)
                page.wait_for_timeout(3000)
            shot(page, "FIN_C00_modal.png")
            info = dump(page)
            log["steps"].append({"step": "FIN_C00", **info})
            print("C00 snip", info["snip"][:500])

            clicked = click_force(page, r"^Confirm$")
            print("C Confirm clicked", clicked)
            page.wait_for_timeout(5000)
            for pg in ctx.pages:
                print(" page:", pg.url[:140])
            info = dump(page)
            shot(page, "FIN_C01_after_confirm.png")
            log["steps"].append({"step": "FIN_C01_after_confirm", "clicked": clicked, **info})
            print("C01 pwd=", info["password_field"], "url=", info["url"][:120])
            print(info["snip"][:900])

            for pat in [
                r"^Continue as",
                r"^Continue$",
                r"Log in to Instagram",
                r"^Log in$",
                r"^Allow$",
                r"^Confirm$",
            ]:
                c2 = click_force(page, pat)
                if c2:
                    print("C follow-up", c2)
                    page.wait_for_timeout(4000)
                    shot(page, "FIN_C02_followup.png")
                    info = dump(page)
                    log["steps"].append({"step": "FIN_C02", "clicked": c2, **info})
                    print("C02", info["url"][:120], "pwd", info["password_field"])
                    print(info["snip"][:700])
                    for pg in list(ctx.pages):
                        if "instagram.com" in (pg.url or ""):
                            print(" switching to IG page", pg.url[:120])
                            page = pg
                            page.wait_for_timeout(3000)
                            shot(page, "FIN_C03_ig_page.png")
                            info = dump(page)
                            log["steps"].append({"step": "FIN_C03_ig", **info})
                            print(info["snip"][:800])
                            break
                    break
        except Exception as e:
            print("Path C error", e)
            log["steps"].append({"step": "FIN_C_error", "error": str(e)[:300]})

        # ===== Path A: Suite Continue =====
        page_a = ctx.new_page()
        page_a.on("dialog", _d)
        try:
            page_a.goto(
                f"https://business.facebook.com/latest/home?business_id={ORBIT_BUSINESS}&asset_id={ORBIT_ASSET}",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page_a.wait_for_timeout(4000)
            for pat in [r"^Done$", r"^Close$", r"^Not now$", r"^Dismiss$"]:
                click_force(page_a, pat)
                page_a.wait_for_timeout(500)
            shot(page_a, "FIN_A00.png")
            clicked = click_force(page_a, r"^Continue$")
            print("A Continue", clicked)
            page_a.wait_for_timeout(5000)
            shot(page_a, "FIN_A01.png")
            info = dump(page_a)
            log["steps"].append({"step": "FIN_A01", "clicked": clicked, **info})
            print("A01 pwd", info["password_field"], info["url"][:120])
            print(info["snip"][:800])
            for pg in ctx.pages:
                if "instagram" in (pg.url or "").lower():
                    print("A IG page", pg.url[:140])
                    shot(pg, "FIN_A_ig.png")
                    log["steps"].append({"step": "FIN_A_ig", **dump(pg)})
        except Exception as e:
            print("Path A error", e)
            log["steps"].append({"step": "FIN_A_error", "error": str(e)[:300]})

        # ===== Path B: Claim Instagram Account =====
        page_b = ctx.new_page()
        page_b.on("dialog", _d)
        try:
            page_b.goto(
                f"https://business.facebook.com/latest/settings/instagram_account?business_id={ORBIT_BUSINESS}",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page_b.wait_for_timeout(3000)
            click_force(page_b, r"^Add$")
            page_b.wait_for_timeout(2000)
            shot(page_b, "FIN_B00_claim_modal.png")
            clicked = click_force(page_b, r"Claim Instagram Account")
            print("B Claim", clicked)
            page_b.wait_for_timeout(5000)
            shot(page_b, "FIN_B01_after_claim.png")
            info = dump(page_b)
            log["steps"].append({"step": "FIN_B01", "clicked": clicked, **info})
            print("B01 pwd", info["password_field"], info["url"][:140])
            print(info["snip"][:900])
            for pg in ctx.pages:
                print(" B open", pg.url[:140])
                if "instagram.com" in (pg.url or ""):
                    shot(pg, "FIN_B_ig_login.png")
                    log["steps"].append({"step": "FIN_B_ig", **dump(pg)})
                    print("B IG", dump(pg)["snip"][:800])
        except Exception as e:
            print("Path B error", e)
            log["steps"].append({"step": "FIN_B_error", "error": str(e)[:300]})

        # Final verification
        page_v = ctx.new_page()
        try:
            page_v.goto(
                f"https://business.facebook.com/latest/home?business_id={ORBIT_BUSINESS}&asset_id={ORBIT_ASSET}",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page_v.wait_for_timeout(5000)
            for pat in [r"^Done$", r"^Close$", r"^Not now$"]:
                click_force(page_v, pat)
            shot(page_v, "FINAL_suite_home.png")
            home = dump(page_v)
            page_v.goto(
                f"https://business.facebook.com/latest/settings/instagram_account?business_id={ORBIT_BUSINESS}",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page_v.wait_for_timeout(4000)
            shot(page_v, "FINAL_ig_accounts.png")
            ig_acc = dump(page_v)
            page_v.goto(
                "https://www.facebook.com/settings?tab=linked_instagram",
                wait_until="domcontentloaded",
                timeout=90000,
            )
            page_v.wait_for_timeout(4000)
            shot(page_v, "FINAL_linked_ig.png")
            linked = dump(page_v)
            log["final"] = {"home": home, "ig_accounts": ig_acc, "linked": linked}
            print("FINAL home connect=", home["connect_instagram"], "review=", home["review_connection"])
            print("FINAL ig accounts no_ig=", ig_acc["no_ig_added"], "orbit=", ig_acc["orbitwithben"])
            print(
                "FINAL linked review=",
                linked["review_connection"],
                "complete=",
                linked.get("connected_complete"),
            )
            print("linked snip", linked["snip"][:700])
        finally:
            page_v.close()
            try:
                page.close()
            except Exception:
                pass
            try:
                page_a.close()
            except Exception:
                pass
            try:
                page_b.close()
            except Exception:
                pass

    (OUT / "CONNECT_FINISH.json").write_text(json.dumps(log, indent=2))
    print("WROTE CONNECT_FINISH.json")


if __name__ == "__main__":
    main()
