#!/usr/bin/env python3
"""Orbit CG via Google AI Studio Veo UI (secondary Ultra path).

Prefer Google Flow for routine CG:
  04_Audio/tools/orbit_flow_veo_ui.py

AI Studio often still requires a paid Gemini API key selected in the Playground
even when the ULTRA badge is visible. Keep this helper as a secondary UI path.

Channel VO stays on ElevenLabs TTS → Ben Orbit Narrator (see orbit_voice.py).

One-time auth (headed):
  python3 04_Audio/tools/orbit_aistudio_veo_ui.py --login

Generate:
  python3 04_Audio/tools/orbit_aistudio_veo_ui.py --probe

Preferred default:
  python3 04_Audio/tools/orbit_flow_veo_ui.py --probe
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import orbit_gemini_veo as veo  # noqa: E402 — shared prompt lock / strip_audio

# Persistent Google-logged Chromium profile (Ultra account)
DEFAULT_PROFILE = Path(
    os.environ.get(
        "ORBIT_AISTUDIO_PROFILE",
        str(Path.home() / "code" / "youtube" / ".playwright-aistudio-profile"),
    )
)

# Prefer Veo 3.1 Fast in Studio; fall back through known video entry URLs
DEFAULT_MODEL = os.environ.get(
    "ORBIT_AISTUDIO_VEO_MODEL", "veo-3.1-fast-generate-preview"
)
VIDEO_URLS = [
    "https://aistudio.google.com/prompts/new_video?model={model}",
    "https://aistudio.google.com/generate-video",
    "https://aistudio.google.com/models/veo-3",
    "https://aistudio.google.com/app/prompts/new_video?model={model}",
]

# Mag1cFall / AI Studio Angular selectors (plus text fallbacks in helpers)
SEL = {
    "root": "ms-video-prompt, ms-prompt-input, [class*='video-prompt']",
    "prompt": (
        'textarea[aria-label="Enter a prompt to generate a video"], '
        'textarea[aria-label*="prompt" i], '
        'ms-video-prompt textarea, '
        "textarea"
    ),
    "add_media": (
        'ms-add-media-button button[aria-label="Add an image to the prompt"], '
        'button[aria-label*="Add an image" i], '
        'button[aria-label*="Add media" i], '
        'button[aria-label*="Upload" i]'
    ),
    "run": (
        'ms-run-button button[aria-label="Run"], '
        'button[aria-label="Run"], '
        'button:has-text("Run")'
    ),
    "gallery_item": (
        "ms-video-generation-gallery-video, "
        "[class*='video-generation-gallery'] video, "
        "ms-video-generation-gallery video"
    ),
    "download": (
        'ms-video-generation-gallery-video button[aria-label="Download video"], '
        'button[aria-label="Download video"], '
        'button[aria-label*="Download" i]'
    ),
    "neg": (
        'ms-run-settings textarea[aria-label*="negative" i], '
        'textarea[aria-label*="negative prompt" i]'
    ),
    "duration": "mat-select#duration-selector, mat-select[aria-label*='duration' i]",
}


def profile_path(override: Path | None = None) -> Path:
    p = override or DEFAULT_PROFILE
    p.mkdir(parents=True, exist_ok=True)
    return p


def launch_context(
    playwright,
    *,
    headed: bool,
    profile: Path,
    slow_mo: int = 0,
):
    """Launch persistent Chromium with the Ultra Google session."""
    args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    ctx = playwright.chromium.launch_persistent_context(
        user_data_dir=str(profile),
        headless=not headed,
        viewport={"width": 1440, "height": 960},
        accept_downloads=True,
        args=args,
        slow_mo=slow_mo or 0,
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    return ctx, page


def dismiss(page) -> None:
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(200)
    page.evaluate(
        """() => {
          const re = /Accept all|I agree|Got it|Not now|Maybe later|Remind me later|^Close$|Dismiss/i;
          [...document.querySelectorAll('button,[role="button"]')].forEach(b => {
            const t = (b.innerText || b.getAttribute('aria-label') || '').trim();
            if (re.test(t) && t.length < 48) { try { b.click(); } catch (e) {} }
          });
        }"""
    )
    page.wait_for_timeout(300)


def looks_logged_in(page) -> bool:
    url = (page.url or "").lower()
    if "accounts.google.com" in url and ("signin" in url or "servicelogin" in url):
        return False
    body = ""
    try:
        body = page.locator("body").inner_text(timeout=5000)[:2500]
    except Exception:
        return False
    low = body.lower()
    if "sign in" in low and ("google account" in low or "to continue to" in low):
        return False
    # Marketing landing ("Get started") is not a real Studio session
    if "get started" in low and "generate videos with veo" not in low and "ms-video" not in (page.content()[:2000].lower() if False else ""):
        if page.locator("ms-video-prompt").count() == 0 and page.locator("ms-run-button").count() == 0:
            if "playground" not in low and "untitled prompt" not in low:
                return False
    if page.locator("ms-video-prompt").count() or page.locator("ms-run-button").count():
        return True
    if any(x in low for x in ("untitled prompt", "run settings", "playground", "benoats@", "ultra")):
        return True
    return "sign in with google" not in low and "aistudio.google.com" in url


def navigate_video_studio(page, model: str = DEFAULT_MODEL) -> str:
    """Open AI Studio video composer; return the URL that loaded."""
    last_err: Exception | None = None
    for tmpl in VIDEO_URLS:
        url = tmpl.format(model=model)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            dismiss(page)
            # Prefer pages that expose a prompt box or video root
            if page.locator(SEL["prompt"]).count() > 0:
                return page.url
            if page.locator(SEL["root"]).count() > 0:
                return page.url
            if looks_logged_in(page) and "aistudio.google.com" in page.url:
                return page.url
        except Exception as e:
            last_err = e
            continue
    if last_err:
        raise RuntimeError(f"Could not open AI Studio video UI: {last_err}")
    raise RuntimeError("Could not open AI Studio video UI")


def click_first(page, selector: str, *, timeout_ms: int = 8000) -> bool:
    loc = page.locator(selector)
    n = loc.count()
    for i in range(n):
        el = loc.nth(i)
        try:
            if not el.is_visible(timeout=800):
                continue
            el.click(timeout=timeout_ms)
            return True
        except Exception:
            continue
    return False


def set_prompt(page, prompt: str) -> None:
    dismiss(page)
    box = page.locator(SEL["prompt"]).first
    try:
        box.wait_for(state="visible", timeout=30_000)
        box.click(timeout=5000)
        # Clear existing
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(100)
        # insert_text avoids some Angular input lag vs fill()
        page.keyboard.insert_text(prompt)
        page.wait_for_timeout(200)
        return
    except Exception:
        pass
    # Fallback: any large textarea
    page.evaluate(
        """(text) => {
          const areas = [...document.querySelectorAll('textarea')];
          const box = areas.find(a => {
            const r = a.getBoundingClientRect();
            return r.width > 200 && r.height > 40;
          }) || areas[0];
          if (!box) throw new Error('no textarea');
          box.focus();
          box.value = text;
          box.dispatchEvent(new Event('input', { bubbles: true }));
          box.dispatchEvent(new Event('change', { bubbles: true }));
        }""",
        prompt,
    )


def attach_orbit_image(page, ref: Path) -> bool:
    """Upload Orbit reference as start / prompt image."""
    if not ref.exists():
        print(f"WARN: Orbit ref missing: {ref}", flush=True)
        return False
    dismiss(page)
    click_first(page, SEL["add_media"], timeout_ms=4000)
    page.wait_for_timeout(500)
    # Also try text-labelled controls
    page.evaluate(
        """() => {
          const re = /add (an )?image|start frame|reference|upload image|add media/i;
          const hit = [...document.querySelectorAll('button,label,[role="button"]')].find(el => {
            const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).trim();
            const r = el.getBoundingClientRect();
            return r.width > 8 && r.height > 8 && re.test(t);
          });
          if (hit) try { hit.click(); } catch (e) {}
        }"""
    )
    page.wait_for_timeout(400)

    inputs = page.locator('input[type="file"]')
    n = inputs.count()
    for i in range(n):
        try:
            accept = (inputs.nth(i).get_attribute("accept") or "").lower()
            if accept and "video" in accept and "image" not in accept:
                continue
            inputs.nth(i).set_input_files(str(ref), timeout=8000)
            print(f"orbit image: set_input_files idx={i} accept={accept!r}", flush=True)
            page.wait_for_timeout(900)
            page.keyboard.press("Escape")
            return True
        except Exception as e:
            print(f"orbit image: idx={i} skip ({e})", flush=True)
    print("WARN: could not attach Orbit image via file input", flush=True)
    return False


def set_negative_prompt(page, negative: str) -> None:
    if not negative:
        return
    # Open run settings if needed
    page.evaluate(
        """() => {
          const hit = [...document.querySelectorAll('button,[role="button"]')].find(el => {
            const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).toLowerCase();
            return /run settings|settings|tune/i.test(t) && t.length < 40;
          });
          if (hit) try { hit.click(); } catch (e) {}
        }"""
    )
    page.wait_for_timeout(400)
    loc = page.locator(SEL["neg"])
    if loc.count() == 0:
        return
    try:
        loc.first.fill(negative, timeout=5000)
    except Exception:
        pass


def set_aspect_and_duration(
    page, *, aspect_ratio: str = "16:9", duration_seconds: int = 8
) -> None:
    # Aspect ratio radio / button
    page.evaluate(
        """(ar) => {
          const hit = [...document.querySelectorAll('button,[role="radio"],ms-aspect-ratio-radio-button button')].find(el => {
            const t = (el.innerText || el.getAttribute('aria-label') || '').replace(/\\s+/g, '');
            return t.includes(ar.replace(/\\s+/g, ''));
          });
          if (hit) try { hit.click(); } catch (e) {}
        }""",
        aspect_ratio,
    )
    page.wait_for_timeout(200)
    # Duration dropdown
    dd = page.locator(SEL["duration"])
    if dd.count() == 0:
        return
    try:
        dd.first.click(timeout=3000)
        page.wait_for_timeout(300)
        opt = page.locator(f'mat-option:has-text("{duration_seconds}")')
        if opt.count() == 0:
            opt = page.locator(f'[role="option"]:has-text("{duration_seconds}")')
        if opt.count():
            opt.first.click(timeout=3000)
        else:
            page.keyboard.press("Escape")
    except Exception:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass


def ensure_api_key_linked(page) -> dict:
    """Veo in AI Studio requires a paid Gemini API key selected (Ultra login alone is not enough).

    Returns status dict. Does not invent keys — opens the picker so a billed key can be chosen.
    """
    status = {"needed": False, "selected": False, "message": ""}
    try:
        body = page.locator("body").inner_text(timeout=4000)[:2500].lower()
    except Exception:
        body = ""
    need = (
        "requires a paid api key" in body
        or "select an api key" in body
        or page.locator('button[aria-label="No API key selected"]').count() > 0
    )
    status["needed"] = bool(need)
    if not need and page.locator('button[aria-label*="API key" i]').count():
        # Already may have a key — treat as ok
        aria = ""
        try:
            aria = page.locator('button[aria-label*="API key" i]').first.get_attribute("aria-label") or ""
        except Exception:
            pass
        if aria and "no api key" not in aria.lower():
            status["selected"] = True
            status["message"] = aria
            return status

    # Open key picker
    for name in ("No API key selected", "Get API key", "API key"):
        try:
            page.get_by_role("button", name=name).click(timeout=2000)
            page.wait_for_timeout(800)
            break
        except Exception:
            continue

    # Prefer an existing key option if present
    picked = page.evaluate(
        """() => {
          const opts = [...document.querySelectorAll('button,[role="option"],mat-option,li')];
          const hit = opts.find(el => {
            const t = ((el.innerText||'') + ' ' + (el.getAttribute('aria-label')||'')).trim();
            const r = el.getBoundingClientRect();
            if (r.width < 40 || r.height < 16) return false;
            if (/No API key selected|Get API key|Create key|Import|Set up billing|Link a paid/i.test(t)) return false;
            return /AIza|API key|\\\\.\\.\\.|projects\\//i.test(t) || /\\\\w{4}\\\\.\\\\.\\\\.\\\\w{4}/.test(t);
          });
          if (hit) { hit.click(); return (hit.innerText||'').slice(0,120); }
          return '';
        }"""
    )
    if picked:
        status["selected"] = True
        status["message"] = f"picked:{picked}"
        page.wait_for_timeout(500)
        return status

    status["message"] = (
        "AI Studio Veo needs a paid Gemini API key selected in the UI "
        "(button shows 'No API key selected'). Create/link one under "
        "aistudio.google.com/api-keys with billing, then re-run. "
        "Ultra login alone does not unlock Veo GenerateVideo."
    )
    return status


def click_run(page) -> bool:
    dismiss(page)
    # Cookie / consent banners sit over the Run control
    try:
        page.get_by_role("button", name="Understood").click(timeout=1500)
        page.wait_for_timeout(300)
    except Exception:
        pass
    dismiss(page)

    # AI Studio Run button often has no aria-label — text is "Run" + shortcut glyphs
    for loc in (
        page.locator("ms-run-button button").first,
        page.locator("button.ctrl-enter-submits").first,
        page.get_by_role("button", name="Run").first,
        page.locator('button:has-text("Run")').first,
    ):
        try:
            if loc.count() == 0:
                continue
            loc.scroll_into_view_if_needed(timeout=3000)
            if loc.is_enabled(timeout=2000):
                loc.click(timeout=8000)
                return True
        except Exception:
            continue

    if click_first(page, SEL["run"], timeout_ms=8_000):
        return True

    clicked = bool(
        page.evaluate(
            """() => {
              const hit = [...document.querySelectorAll('button')].find(b => {
                const a = (b.getAttribute('aria-label') || '').trim();
                const t = (b.innerText || '').trim().split('\\n')[0].trim();
                const cls = (b.className || '').toString();
                if (b.disabled) return false;
                return a === 'Run' || /^Run$/i.test(t) || /^Generate$/i.test(t)
                  || cls.includes('ctrl-enter-submits');
              });
              if (!hit) return false;
              hit.click();
              return true;
            }"""
        )
    )
    if clicked:
        return True

    # Shortcut fallback (AI Studio: ⌘/Ctrl + Enter)
    try:
        page.keyboard.press("Meta+Enter")
        page.wait_for_timeout(400)
        return True
    except Exception:
        try:
            page.keyboard.press("Control+Enter")
            return True
        except Exception:
            return False


def gallery_ready_count(page) -> int:
    return int(
        page.evaluate(
            """() => {
              const items = [...document.querySelectorAll(
                'ms-video-generation-gallery-video, ms-video-generation-gallery video, video'
              )];
              let n = 0;
              for (const el of items) {
                const root = el.closest('ms-video-generation-gallery-video') || el.parentElement || el;
                const dl = root.querySelector('button[aria-label="Download video"], button[aria-label*="Download"]');
                const vid = root.querySelector('video') || (el.tagName === 'VIDEO' ? el : null);
                const src = vid ? (vid.getAttribute('src') || '') : '';
                if ((dl && dl.offsetParent !== null) || src.startsWith('blob:') || src.startsWith('data:')) n++;
              }
              return n;
            }"""
        )
    )


def wait_for_video(page, *, before_count: int, timeout_s: int = 480) -> None:
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        n = gallery_ready_count(page)
        print(f"  gallery ready={n} (before={before_count}) · {int(time.time() - t0)}s", flush=True)
        if n > before_count:
            return
        # Error banners
        try:
            body = page.locator("body").inner_text(timeout=2000)[:2000].lower()
            if "quota" in body and ("exceed" in body or "limit" in body):
                raise RuntimeError("AI Studio quota / rate limit — wait or check Ultra plan")
            if "permission denied" in body:
                raise RuntimeError(
                    "AI Studio Veo permission denied — link a paid Gemini API key "
                    "(button: No API key selected → Create key / Set up billing)."
                )
            if "requires a paid api key" in body or "select an api key" in body:
                raise RuntimeError(
                    "AI Studio Veo requires a paid API key selected in the UI "
                    "(Ultra login alone is not enough)."
                )
            if "something went wrong" in body or "failed to generate" in body:
                raise RuntimeError("AI Studio reported generation failure")
        except RuntimeError:
            raise
        except Exception:
            pass
        page.wait_for_timeout(5000)
    raise TimeoutError(f"AI Studio video not ready after {timeout_s}s")


def download_latest(page, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Prefer Download button
    dl = page.locator(SEL["download"])
    if dl.count() == 0:
        # last resort: any download near video gallery
        dl = page.locator('button[aria-label*="Download" i]')
    if dl.count() == 0:
        raise RuntimeError("No Download video control found")

    with page.expect_download(timeout=180_000) as info:
        dl.last.click(timeout=15_000)
    download = info.value
    download.save_as(str(dest))
    if not veo.already_done(dest):
        raise RuntimeError(f"download too small: {dest} ({dest.stat().st_size if dest.exists() else 0})")


def generate_clip(
    page,
    prompt: str,
    dest: Path,
    *,
    model: str = DEFAULT_MODEL,
    duration_seconds: int = 8,
    aspect_ratio: str = "16:9",
    orbit_ref: Path | None = None,
    timeout_s: int = 480,
) -> dict:
    """Generate one silent Veo clip via AI Studio UI + Ultra session."""
    ref = orbit_ref or veo.ORBIT_REF
    t0 = time.time()
    url = navigate_video_studio(page, model=model)
    print(f"  studio: {url}", flush=True)
    if not looks_logged_in(page):
        raise RuntimeError(
            "Not logged into Google AI Studio.\n"
            "Run once with --login (headed) on the Ultra Google account:\n"
            "  python3 04_Audio/tools/orbit_aistudio_veo_ui.py --login"
        )

    key_status = ensure_api_key_linked(page)
    if key_status.get("needed") and not key_status.get("selected"):
        raise RuntimeError(key_status.get("message") or "Paid API key not selected in AI Studio")

    before = gallery_ready_count(page)
    set_aspect_and_duration(
        page, aspect_ratio=aspect_ratio, duration_seconds=duration_seconds
    )
    set_negative_prompt(page, veo.NEGATIVE)
    attached = attach_orbit_image(page, ref)
    set_prompt(page, prompt)
    page.wait_for_timeout(400)
    if not click_run(page):
        raise RuntimeError("Could not click Run / Generate in AI Studio")
    print("  submitted Run", flush=True)
    wait_for_video(page, before_count=before, timeout_s=timeout_s)
    download_latest(page, dest)
    veo.strip_audio(dest)
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "model": model,
        "engine": "aistudio-ui-veo",
        "orbit_ref": str(ref),
        "orbit_attached": attached,
        "url": url,
    }


def login_flow(profile: Path) -> None:
    """Headed browser: user signs into Ultra Google account, then Enter."""
    from playwright.sync_api import sync_playwright

    print(f"Profile: {profile}", flush=True)
    print("Opening AI Studio — sign in with the Google One Ultra account…", flush=True)
    with sync_playwright() as p:
        ctx, page = launch_context(p, headed=True, profile=profile, slow_mo=50)
        try:
            navigate_video_studio(page)
            print(
                "\nWhen you see the video prompt UI (logged in), return here and press Enter.\n",
                flush=True,
            )
            try:
                input()
            except EOFError:
                # Non-interactive: wait until logged in or timeout
                print("No TTY — waiting up to 5 min for login…", flush=True)
                deadline = time.time() + 300
                while time.time() < deadline:
                    if looks_logged_in(page):
                        break
                    page.wait_for_timeout(3000)
            if not looks_logged_in(page):
                raise SystemExit("Still not logged in — re-run --login")
            print("OK — AI Studio session saved.", flush=True)
        finally:
            ctx.close()


def dump_probe(page, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    shot = out_dir / "aistudio_probe.png"
    html = out_dir / "aistudio_probe.html"
    page.screenshot(path=str(shot), full_page=True)
    html.write_text(page.content(), encoding="utf-8")
    summary = {
        "url": page.url,
        "logged_in": looks_logged_in(page),
        "prompt_count": page.locator(SEL["prompt"]).count(),
        "run_count": page.locator(SEL["run"]).count(),
        "screenshot": str(shot),
        "html": str(html),
    }
    (out_dir / "aistudio_probe.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--login", action="store_true", help="Headed Google Ultra login")
    ap.add_argument("--probe", action="store_true", help="One short Orbit test clip")
    ap.add_argument("--prompt", default="", help="Scene action (Orbit-in-scene)")
    ap.add_argument("--out", type=Path, default=Path("/tmp/orbit_aistudio_veo_probe.mp4"))
    ap.add_argument("--pass-id", default="p0")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--profile", type=Path, default=None)
    ap.add_argument("--headed", action="store_true", help="Show browser (debug)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--dump-ui",
        type=Path,
        default=None,
        help="Navigate + dump screenshot/HTML (no generate)",
    )
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
    print(f"model={args.model} · engine=aistudio-ui", flush=True)

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
                navigate_video_studio(page, model=args.model)
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
