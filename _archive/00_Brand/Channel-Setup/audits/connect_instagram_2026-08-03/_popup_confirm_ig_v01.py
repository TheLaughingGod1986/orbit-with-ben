#!/usr/bin/env python3
"""Capture IG login popup from Confirm connection / Suite Connect Instagram."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
CDP = "http://127.0.0.1:9222"
ORBIT_BUSINESS = "1352434763139246"
ORBIT_ASSET = "1285932871266399"


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), full_page=True, timeout=15000)
        print("shot", name, (page.url or "")[:100])
    except Exception as e:
        print("shot fail", name, e)


def dialogs(page):
    return page.evaluate(
        """() => [...document.querySelectorAll('[role=dialog]')].map(d => ({
          text:(d.innerText||'').slice(0,500),
          buttons:[...d.querySelectorAll('button,[role=button]')].map(b=>(b.innerText||'').trim()).filter(t=>t&&t.length<60)
        })).filter(d => !(d.text||'').startsWith('Notification'))"""
    )


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()

        page.goto(
            "https://www.facebook.com/settings?tab=linked_instagram",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        page.evaluate(
            """() => {
              for (const el of document.querySelectorAll('button,[role=button],a')) {
                if ((el.innerText||'').trim()==='Review Connection') el.click();
              }
            }"""
        )
        page.wait_for_timeout(2000)
        page.evaluate(
            """() => {
              for (const d of document.querySelectorAll('[role=dialog]')) {
                for (const el of d.querySelectorAll('button,[role=button]')) {
                  if ((el.innerText||'').trim()==='Confirm') { el.click(); return; }
                }
              }
            }"""
        )
        page.wait_for_timeout(2500)
        shot(page, "POP_00_confirm_connection_modal.png")
        print("dialogs before", dialogs(page))

        popup = None
        try:
            with ctx.expect_page(timeout=15000) as pi:
                page.evaluate(
                    """() => {
                      for (const d of document.querySelectorAll('[role=dialog]')) {
                        for (const el of d.querySelectorAll('button,[role=button]')) {
                          if ((el.innerText||'').trim()==='Confirm connection') {
                            el.click(); return true;
                          }
                        }
                      }
                      return false;
                    }"""
                )
            popup = pi.value
            print("POPUP opened", popup.url[:160])
        except Exception as e:
            print("no popup on Confirm connection:", str(e)[:160])
            page.wait_for_timeout(4000)
            print("dialogs after", dialogs(page))
            shot(page, "POP_01_no_popup.png")
            for fr in page.frames:
                u = fr.url or ""
                if "instagram" in u or "login" in u:
                    print("FRAME", u[:160])
                    try:
                        print(fr.inner_text("body")[:500])
                    except Exception as ex:
                        print("frame err", ex)

        if popup:
            popup.wait_for_timeout(2000)
            shot(popup, "POP_02_popup.png")
            print(popup.inner_text("body")[:900])
            popup.evaluate(
                """() => {
                  for (const el of document.querySelectorAll('button,[role=button],a')) {
                    const t=(el.innerText||'').trim();
                    if (/log in as orbitwithben|continue as|continue|allow|log in/i.test(t) && t.length<80) {
                      el.click(); return t;
                    }
                  }
                }"""
            )
            try:
                popup.wait_for_timeout(10000)
                shot(popup, "POP_03_after_login.png")
                print("popup after", popup.url[:160])
                print(popup.inner_text("body")[:800])
            except Exception as e:
                print("popup closed", e)

        # message settings
        page.wait_for_timeout(2000)
        print("main dialogs", dialogs(page))
        page.evaluate(
            """() => {
              for (const d of document.querySelectorAll('[role=dialog]')) {
                const t=d.innerText||'';
                if (/Choose Instagram message settings/i.test(t)) {
                  for (const c of d.querySelectorAll('input[type=checkbox]')) {
                    if(!c.checked) c.click();
                  }
                  for (const el of d.querySelectorAll('button,[role=button]')) {
                    if ((el.innerText||'').trim()==='Confirm') {
                      el.click(); return 'confirmed messages';
                    }
                  }
                }
              }
              return null;
            }"""
        )
        page.wait_for_timeout(5000)
        shot(page, "POP_04_after_flow.png")

        # Suite Connect Instagram
        page2 = ctx.new_page()
        page2.goto(
            f"https://business.facebook.com/latest/home?business_id={ORBIT_BUSINESS}&asset_id={ORBIT_ASSET}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page2.wait_for_timeout(4000)
        page2.evaluate(
            """() => {
              for (const lab of ['Done','Close','Not now','Dismiss']) {
                for (const el of document.querySelectorAll('button,[role=button]')) {
                  if ((el.innerText||'').trim()===lab) el.click();
                }
              }
            }"""
        )
        page2.wait_for_timeout(1000)
        shot(page2, "POP_suite_home.png")
        popup2 = None
        try:
            with ctx.expect_page(timeout=15000) as pi:
                loc = page2.get_by_role("link", name=re.compile(r"^Connect Instagram$", re.I))
                if loc.count():
                    loc.first.click(force=True, timeout=5000)
                else:
                    page2.get_by_text("Connect Instagram", exact=True).first.click(
                        force=True, timeout=5000
                    )
            popup2 = pi.value
            print("Suite Connect popup", popup2.url[:160])
        except Exception as e:
            print("Suite Connect no popup", str(e)[:150])
            page2.wait_for_timeout(4000)
            shot(page2, "POP_suite_after_connect.png")
            print("suite after", page2.url[:120])
            print(page2.inner_text("body")[:700])
            for pg in ctx.pages:
                if "instagram.com" in (pg.url or ""):
                    popup2 = pg
                    print("found ig tab", pg.url[:160])

        if popup2:
            try:
                popup2.wait_for_timeout(2000)
                shot(popup2, "POP_suite_oauth.png")
                print("suite oauth", popup2.url[:160])
                print(popup2.inner_text("body")[:700])
                popup2.evaluate(
                    """() => {
                      for (const el of document.querySelectorAll('button,[role=button],a')) {
                        const t=(el.innerText||'').trim();
                        if (/log in as orbitwithben|continue as|continue|allow/i.test(t) && t.length<80) {
                          el.click(); return t;
                        }
                      }
                    }"""
                )
                popup2.wait_for_timeout(10000)
                shot(popup2, "POP_suite_oauth_after.png")
                print("suite oauth after", popup2.url[:160])
            except Exception as e:
                print("suite oauth err", e)

        page3 = ctx.new_page()
        page3.goto(
            f"https://business.facebook.com/latest/settings/instagram_account?business_id={ORBIT_BUSINESS}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page3.wait_for_timeout(5000)
        ig = page3.inner_text("body")
        shot(page3, "POP_FINAL_ig.png")
        page3.goto(
            f"https://business.facebook.com/latest/home?business_id={ORBIT_BUSINESS}&asset_id={ORBIT_ASSET}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page3.wait_for_timeout(4000)
        page3.evaluate(
            """() => {
              for (const lab of ['Done','Close','Not now','Dismiss']) {
                for (const el of document.querySelectorAll('button,[role=button]')) {
                  if ((el.innerText||'').trim()===lab) el.click();
                }
              }
            }"""
        )
        home = page3.inner_text("body")
        shot(page3, "POP_FINAL_home.png")
        page3.goto(
            "https://www.facebook.com/settings?tab=linked_instagram",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page3.wait_for_timeout(4000)
        linked = page3.inner_text("body")
        shot(page3, "POP_FINAL_linked.png")

        out = {
            "suite_empty": "No Instagram accounts added" in ig,
            "home_connect": "Connect Instagram" in home,
            "home_confirm": "Confirm Instagram" in home,
            "review_needed": "Review account connection" in linked
            or "only includes some features" in linked,
            "ig_snip": ig[:800],
            "home_snip": home[:700],
            "linked_snip": linked[linked.find("Connected Instagram") :][:700]
            if "Connected Instagram" in linked
            else linked[:500],
        }
        print("FINAL", {k: v for k, v in out.items() if not k.endswith("snip")})
        (OUT / "POPUP_FLOW_RESULT.json").write_text(json.dumps(out, indent=2))
        page.close()
        page2.close()
        page3.close()
    print("done")


if __name__ == "__main__":
    main()
