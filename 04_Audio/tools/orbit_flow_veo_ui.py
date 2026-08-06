#!/usr/bin/env python3
"""Orbit CG via Google Flow Veo UI (Ultra plan — default picture path).

Uses Playwright against labs.google/fx/tools/flow so Google One → AI Ultra
Flow credits apply (Veo 3.1). Prefer this over AI Studio (needs billed API key)
and over GEMINI_API_KEY (separate billing).

Channel VO stays on ElevenLabs TTS → Ben Orbit Narrator (see orbit_voice.py).

One-time auth (headed) — same Google profile as AI Studio works:
  python3 04_Audio/tools/orbit_flow_veo_ui.py --login

Generate:
  python3 04_Audio/tools/orbit_flow_veo_ui.py --probe
  python3 04_Audio/tools/orbit_flow_veo_ui.py \\
    --prompt "Orbit floats beside JWST…" --out /tmp/orbit_test.mp4

Fallbacks (only if Flow UI is broken):
  python3 04_Audio/tools/orbit_aistudio_veo_ui.py --probe
  python3 04_Audio/tools/orbit_gemini_veo.py --probe
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import orbit_gemini_veo as veo  # noqa: E402 — shared prompt lock / strip_audio

FLOW_HOME = "https://labs.google/fx/tools/flow"
DEFAULT_PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        os.environ.get(
            "ORBIT_AISTUDIO_PROFILE",
            str(Path.home() / "code" / "youtube" / ".playwright-aistudio-profile"),
        ),
    )
)
DEFAULT_MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
MEDIA_REDIRECT_RE = re.compile(r"media\.getMediaUrlRedirect\?name=([a-f0-9\-]+)", re.I)


def profile_path(override: Path | None = None) -> Path:
    p = override or DEFAULT_PROFILE
    p.mkdir(parents=True, exist_ok=True)
    return p


def launch_context(playwright, *, headed: bool, profile: Path, slow_mo: int = 0):
    args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    kwargs = {
        "user_data_dir": str(profile),
        "headless": not headed,
        "viewport": {"width": 1440, "height": 900},
        "accept_downloads": True,
        "args": args,
        "slow_mo": slow_mo or 0,
    }
    # Prefer installed Chrome (matches Ultra Google session better)
    try:
        ctx = playwright.chromium.launch_persistent_context(channel="chrome", **kwargs)
    except Exception:
        ctx = playwright.chromium.launch_persistent_context(**kwargs)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    return ctx, page


def dismiss_banners(page) -> None:
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().split('\\n')[0];
            if (/^close$|^Dismiss$|^Got it$/i.test(t)) {
              try { b.click(); } catch (e) {}
            }
          }
        }"""
    )
    page.wait_for_timeout(300)


def looks_logged_in(page) -> bool:
    url = (page.url or "").lower()
    if "accounts.google.com" in url and ("signin" in url or "servicelogin" in url):
        return False
    try:
        body = page.locator("body").inner_text(timeout=5000)[:3000]
    except Exception:
        return False
    low = body.lower()
    if "sign in" in low and "google flow" in low and "ultra" not in low:
        return False
    return "labs.google" in url and (
        "ultra" in low or "new project" in low or "/project/" in url
    )


def visible_button(page, *needles: str):
    """Return first visible button whose inner_text contains all needles."""
    needles_l = [n.lower() for n in needles]
    buttons = page.locator("button")
    for i in range(buttons.count()):
        b = buttons.nth(i)
        try:
            box = b.bounding_box()
            if not box or box["width"] < 2 or box["height"] < 2:
                continue
            text = (b.inner_text(timeout=400) or "").lower().replace("\n", " ")
            if all(n in text for n in needles_l):
                return b
        except Exception:
            continue
    return None


def click_visible(page, *needles: str, timeout: int = 8000) -> bool:
    b = visible_button(page, *needles)
    if not b:
        return False
    b.click(timeout=timeout)
    return True


def editor_box(page) -> dict | None:
    return page.evaluate(
        """() => {
          const el = document.querySelector('[data-slate-editor="true"]');
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return {w: r.width, h: r.height, x: r.x, y: r.y};
        }"""
    )


def ensure_project(page) -> str:
    """Land inside a Flow project editor. Returns project URL."""
    if "/project/" not in (page.url or ""):
        page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2000)
        dismiss_banners(page)
        if not click_visible(page, "new project"):
            # Open most recent project card
            href = page.evaluate(
                """() => {
                  const a = document.querySelector('a[href*="/project/"]');
                  return a ? a.href : null;
                }"""
            )
            if not href:
                raise RuntimeError("Could not find New project or existing Flow project")
            page.goto(href, wait_until="domcontentloaded", timeout=120_000)
        else:
            page.wait_for_url("**/project/**", timeout=60_000)
    page.wait_for_timeout(2500)
    dismiss_banners(page)
    # Wait for agent prompt
    deadline = time.time() + 40
    while time.time() < deadline:
        box = editor_box(page)
        if box and box["w"] > 50:
            break
        # Session may be closed — reopen
        if click_visible(page, "new session") or click_visible(page, "edit_square"):
            page.wait_for_timeout(1500)
        page.wait_for_timeout(500)
    if "/project/" not in page.url:
        raise RuntimeError(f"Not in Flow project: {page.url}")
    return page.url


def configure_veo_settings(page, *, model: str = DEFAULT_MODEL) -> None:
    """Open agent Settings → Never confirm → Veo model → 16:9 x1 → Save."""
    if not click_visible(page, "tune"):
        # Fallback: Settings near prompt
        if not click_visible(page, "settings"):
            raise RuntimeError("Flow Settings (tune) button not found")
    page.wait_for_timeout(900)

    # Never auto-spend confirmations
    never = page.locator('button:has-text("Never")')
    if never.count():
        never.first.click(timeout=5000)
        page.wait_for_timeout(200)

    # Video defaults: 16:9 + x1 (video section is lower in the panel)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            const r = b.getBoundingClientRect();
            if (r.y > 500 && t.includes('16:9')) b.click();
          }
          const x1 = [...document.querySelectorAll('button')].filter(
            (b) => (b.innerText || '').trim() === 'x1'
          );
          if (x1.length >= 2) x1[1].click();
          else if (x1.length === 1) x1[0].click();
        }"""
    )
    page.wait_for_timeout(200)

    # Model dropdown (Omni Flash or already-Veo)
    model_btn = page.locator(
        'button:has-text("Omni Flash"), button:has-text("Veo 3.1")'
    )
    if model_btn.count() == 0:
        raise RuntimeError("Flow video model dropdown not found")
    current = (model_btn.last.inner_text() or "").replace("\n", " ")
    if model not in current:
        model_btn.last.click(timeout=5000)
        page.wait_for_timeout(700)
        item = page.get_by_role("menuitem", name=model)
        if item.count() == 0:
            # Partial match
            item = page.locator(f'[role="menuitem"]:has-text("{model}")')
        if item.count() == 0:
            raise RuntimeError(f"Model menu item not found: {model}")
        item.first.click(timeout=5000)
        page.wait_for_timeout(300)

    save = page.locator('button:has-text("Save")')
    if save.count() == 0:
        # Back arrow also exits settings after changes
        back = page.locator('button:has-text("Back")')
        if back.count():
            back.first.click(timeout=5000)
        else:
            raise RuntimeError("Flow Settings Save/Back not found")
    else:
        save.first.click(timeout=5000)
    page.wait_for_timeout(900)

    box = editor_box(page)
    if not box or box["w"] < 50:
        # Settings may still be open — try Back
        if page.get_by_text("Confirm before generating").count():
            back = page.locator('button:has-text("arrow_back")')
            if back.count():
                back.first.click(timeout=3000)
                page.wait_for_timeout(600)


def upload_orbit_ref(page, ref: Path) -> bool:
    """Upload Orbit reference into the project media library."""
    if not ref.exists():
        raise FileNotFoundError(ref)
    if not click_visible(page, "add media"):
        raise RuntimeError("Add Media button not found")
    page.wait_for_timeout(600)
    up = page.locator('button:has-text("Upload media")')
    if up.count():
        with page.expect_file_chooser(timeout=10_000) as fc:
            up.first.click()
        fc.value.set_files(str(ref))
    else:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            raise RuntimeError("No Upload media control / file input")
        fi.first.set_input_files(str(ref))
    page.wait_for_timeout(3500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    return True


def set_prompt(page, prompt: str) -> None:
    box = editor_box(page)
    if not box or box["w"] < 40:
        raise RuntimeError("Flow prompt editor not visible (open agent session)")
    page.mouse.click(box["x"] + 24, box["y"] + max(6, box["h"] / 2))
    page.wait_for_timeout(150)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    # Chunk type for long prompts (Slate)
    page.keyboard.type(prompt, delay=2)
    page.wait_for_timeout(300)


def submit_create(page) -> None:
    if not click_visible(page, "arrow_forward"):
        # Last Create in prompt bar
        creates = page.locator('button:has-text("Create")')
        if creates.count() == 0:
            raise RuntimeError("Flow Create / arrow_forward not found")
        creates.last.click(timeout=8000)


def dismiss_soft_prompts(page) -> None:
    """Click safe confirmations (not blanket Yes)."""
    page.evaluate(
        """() => {
          const re = /Got it|I understand|Continue|Agree|Accept|Dismiss|^OK$|Generate (the )?video|Create video|Try again|Retry|Regenerate/i;
          for (const b of document.querySelectorAll('button,[role="button"],[role="menuitem"]')) {
            const t = (b.innerText || b.getAttribute('aria-label') || '')
              .trim().replace(/\\n/g, ' ');
            if (
              re.test(t) &&
              t.length < 100 &&
              !/new project|settings|add media|ultra|agent instructions|view settings|save|close/i.test(t)
            ) {
              try { b.click(); } catch (e) {}
            }
          }
        }"""
    )


def collect_media_ids(page) -> set[str]:
    html = page.content()
    return set(MEDIA_REDIRECT_RE.findall(html))


def absolute_media_url(name_or_url: str) -> str:
    if name_or_url.startswith("http"):
        return name_or_url
    if name_or_url.startswith("/"):
        return urljoin("https://labs.google", name_or_url)
    return (
        "https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name="
        + name_or_url
    )


def download_media(page, name_or_url: str, dest: Path) -> int:
    url = absolute_media_url(name_or_url)
    resp = page.request.get(url, timeout=180_000)
    if resp.status != 200:
        raise RuntimeError(f"media download HTTP {resp.status}: {url[:120]}")
    data = resp.body()
    ct = (resp.headers.get("content-type") or "").lower()
    if "video" not in ct and not data[:12].startswith(b"\x00\x00\x00"):
        # Still allow if large enough binary
        if len(data) < 200_000:
            raise RuntimeError(
                f"Unexpected media type {ct!r} size={len(data)} for {url[:120]}"
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def wait_and_download(
    page,
    dest: Path,
    *,
    before_ids: set[str],
    timeout_s: int = 480,
) -> str:
    """Wait for a new Flow media video and download it. Returns media id/url."""
    t0 = time.time()
    last_status = ""
    asked_status = False
    while time.time() - t0 < timeout_s:
        dismiss_soft_prompts(page)
        ids = collect_media_ids(page)
        new_ids = [i for i in ids if i not in before_ids]
        # Prefer ids that resolve as video/mp4
        for mid in reversed(new_ids):
            url = absolute_media_url(mid)
            try:
                head = page.request.get(url, timeout=60_000)
                ct = (head.headers.get("content-type") or "").lower()
                body = head.body()
                if "video" in ct and len(body) > 200_000:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(body)
                    return mid
            except Exception:
                continue

        body = ""
        try:
            body = page.locator("body").inner_text(timeout=3000)[:4000]
        except Exception:
            pass
        low = body.lower()
        status = ""
        for k in (
            "failed",
            "generating",
            "thinking",
            "queue",
            "high demand",
            "creating",
            "scheduled",
            "working",
        ):
            if k in low:
                status = k
                break
        line = f"  wait {int(time.time() - t0)}s status={status or '…'} new_media={len(new_ids)}"
        if line != last_status:
            print(line, flush=True)
            last_status = line

        # Agent queued due to demand — ask for status once after ~90s
        if (
            not asked_status
            and time.time() - t0 > 90
            and ("queue" in low or "high demand" in low or "scheduled" in low)
        ):
            try:
                set_prompt(
                    page,
                    "Please check the status of the Orbit video you scheduled and "
                    "share it when ready.",
                )
                submit_create(page)
                asked_status = True
                print("  asked agent for video status", flush=True)
            except Exception as e:
                print(f"  status ask skipped: {e}", flush=True)

        # Click into All Media / videos if present to surface completed clips
        if time.time() - t0 > 60 and int(time.time() - t0) % 45 < 4:
            click_visible(page, "view videos") or click_visible(page, "all media")

        page.wait_for_timeout(4000)

    raise TimeoutError(f"Flow video not ready after {timeout_s}s")


def generate_clip(
    page,
    prompt: str,
    dest: Path,
    *,
    model: str = DEFAULT_MODEL,
    orbit_ref: Path | None = None,
    timeout_s: int = 480,
    reuse_project: bool = False,
) -> dict:
    """Generate one silent Veo clip via Google Flow Ultra UI."""
    ref = orbit_ref or veo.ORBIT_REF
    t0 = time.time()

    if reuse_project and "/project/" in (page.url or ""):
        url = page.url
    else:
        page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(1500)
        dismiss_banners(page)
        url = ensure_project(page)

    if not looks_logged_in(page):
        raise RuntimeError(
            "Not logged into Google Flow.\n"
            "Run once with --login on the Ultra Google account:\n"
            "  python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
        )

    print(f"  flow: {url}", flush=True)
    before = collect_media_ids(page)
    configure_veo_settings(page, model=model)
    attached = upload_orbit_ref(page, ref)
    # Ensure prompt visible after upload
    box = editor_box(page)
    if not box or box["w"] < 40:
        click_visible(page, "new session")
        page.wait_for_timeout(1200)
    set_prompt(page, prompt)
    submit_create(page)
    print("  submitted Create", flush=True)
    media_id = wait_and_download(
        page, dest, before_ids=before, timeout_s=timeout_s
    )
    if not veo.already_done(dest):
        raise RuntimeError(
            f"download too small: {dest} ({dest.stat().st_size if dest.exists() else 0})"
        )
    veo.strip_audio(dest)
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "model": model,
        "engine": "flow-ui-veo",
        "orbit_ref": str(ref),
        "orbit_attached": attached,
        "media_id": media_id,
        "url": page.url,
    }


def login_flow(profile: Path) -> None:
    from playwright.sync_api import sync_playwright

    print(f"Profile: {profile}", flush=True)
    print("Opening Google Flow — sign in with the Google One Ultra account…", flush=True)
    with sync_playwright() as p:
        ctx, page = launch_context(p, headed=True, profile=profile, slow_mo=50)
        try:
            page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            print(
                "\nWhen you see Flow with ULTRA badge (logged in), return here and press Enter.\n",
                flush=True,
            )
            try:
                input()
            except EOFError:
                print("No TTY — waiting up to 5 min for login…", flush=True)
                deadline = time.time() + 300
                while time.time() < deadline:
                    if looks_logged_in(page):
                        break
                    page.wait_for_timeout(3000)
            if not looks_logged_in(page):
                raise SystemExit("Still not logged in — re-run --login")
            print("OK — Flow session saved.", flush=True)
        finally:
            ctx.close()


def dump_probe(page, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    shot = out_dir / "flow_probe.png"
    html = out_dir / "flow_probe.html"
    ensure_project(page)
    page.screenshot(path=str(shot), full_page=True)
    html.write_text(page.content(), encoding="utf-8")
    summary = {
        "url": page.url,
        "logged_in": looks_logged_in(page),
        "editor": editor_box(page),
        "ultra": page.locator('button:has-text("ULTRA")').count() > 0,
        "screenshot": str(shot),
        "html": str(html),
    }
    (out_dir / "flow_probe.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--login", action="store_true", help="Headed Google Ultra login")
    ap.add_argument("--probe", action="store_true", help="One short Orbit test clip")
    ap.add_argument("--prompt", default="", help="Scene action (Orbit-in-scene)")
    ap.add_argument("--out", type=Path, default=Path("/tmp/orbit_flow_veo_probe.mp4"))
    ap.add_argument("--pass-id", default="p0")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--profile", type=Path, default=None)
    ap.add_argument("--headed", action="store_true", help="Show browser (debug)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dump-ui", type=Path, default=None)
    ap.add_argument("--timeout", type=int, default=480)
    args = ap.parse_args()

    profile = profile_path(args.profile)

    if args.login:
        login_flow(profile)
        return

    if args.probe and not args.prompt:
        args.prompt = (
            "Orbit the orange robot floats beside the James Webb Space Telescope, "
            "cream eyes curious, soft underside glow, deep space stars behind."
        )

    prompt = ""
    if args.prompt:
        prompt = veo.build_prompt(args.prompt, pass_id=args.pass_id)

    print(f"Orbit ref: {veo.ORBIT_REF}", flush=True)
    print(f"profile={profile}", flush=True)
    print(f"model={args.model} · engine=flow-ui", flush=True)

    if args.dry_run:
        if prompt:
            print(prompt[:500], "…")
        else:
            print("(no prompt — dry-run OK)")
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = launch_context(
            p, headed=args.headed or bool(args.dump_ui), profile=profile
        )
        try:
            if args.dump_ui:
                page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                summary = dump_probe(page, args.dump_ui)
                print(json.dumps(summary, indent=2))
                return
            if not args.prompt:
                ap.error("Provide --prompt, --probe, --login, or --dump-ui")
            print(f"out={args.out}", flush=True)
            meta = generate_clip(
                page,
                prompt,
                args.out,
                model=args.model,
                timeout_s=args.timeout,
            )
            print(json.dumps(meta, indent=2))
            print(f"SAVED {args.out}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
