#!/usr/bin/env python3
"""Generate the final missing Seedance bed (scene-096) and exit."""
from __future__ import annotations

import asyncio
import urllib.request
from pathlib import Path

import httpx

import _animate_bold_scenes_elevenlabs_v10 as m
import _seedance_pipeline_v11 as p

SCENE = m.SCENES / "scene-096_board-24-panel-4_v01.png"
BEARER = Path("/tmp/elevenlabs_bearer.txt")


async def dismiss(cdp) -> None:
    await cdp.evaluate(
        """(() => {
          document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
          const skip=[...document.querySelectorAll('button')].find(b=>
            /not now|maybe later|close|dismiss|skip|no thanks/i.test(
              (b.innerText||b.getAttribute('aria-label')||'')
            )
          );
          if (skip) skip.click();
          const x=[...document.querySelectorAll('button')].find(
            b => (b.getAttribute('aria-label')||'') === 'Close'
          );
          if (x) x.click();
          return true;
        })()"""
    )
    await asyncio.sleep(0.4)


async def ui_state(cdp) -> dict:
    return await cdp.evaluate(
        """(() => {
          const gen=document.querySelector('button[aria-label="Generate"]');
          const left=(document.body.innerText||'').match(/(\\d[\\d,]*)\\s*left/i);
          const upgrade=/Upgrade to continue/i.test(document.body.innerText||'');
          return {
            hasGenerate: !!gen,
            disabled: gen ? !!gen.disabled : null,
            creditsLeft: left ? left[1] : null,
            upgradeModal: upgrade,
            url: location.href
          };
        })()"""
    )


async def main() -> None:
    if m.is_ready(SCENE):
        print("already ready")
        return

    cdp = await m.connect_cdp()
    try:
        await m.ensure_composer(cdp)
        await dismiss(cdp)
        await m.ensure_seedance_settings(cdp)
        await dismiss(cdp)
        tok = await m.page_token(cdp)
        BEARER.write_text(tok)

        state = await ui_state(cdp)
        print("ui", state)
        await cdp.screenshot(Path("/tmp/el_scene096_pre.png"))
        if state.get("upgradeModal") or not state.get("hasGenerate") or state.get("disabled"):
            raise RuntimeError(f"blocked: {state}")

        m.load_known_ids()
        await m.seed_known_ids_from_api(cdp)
        gid = await p.submit_one(cdp, SCENE)
        print("queued", gid)

        dest = m.out_path(SCENE)
        for i in range(100):
            await asyncio.sleep(4)
            try:
                tok = await m.page_token(cdp)
                BEARER.write_text(tok)
            except Exception as exc:
                print("token refresh fail", exc)
            headers = {"Authorization": f"Bearer {BEARER.read_text().strip()}"}
            r = httpx.get(
                f"https://api.us.elevenlabs.io/v1/content/generations/{gid}",
                headers=headers,
                timeout=60,
            )
            if r.status_code != 200:
                print("http", r.status_code)
                continue
            meta = r.json()
            st = meta.get("status")
            print(f"status {i}: {st}")
            if st == "completed":
                url = meta.get("download_url") or meta.get("content_url")
                tmp = dest.with_suffix(".partial.mp4")
                urllib.request.urlretrieve(url, tmp)
                tmp.replace(dest)
                m.append_progress(
                    {
                        "scene": SCENE.name,
                        "status": "generated",
                        "generation_id": gid,
                        "output": str(dest),
                        "bytes": dest.stat().st_size,
                        "via": "scene096-final",
                    }
                )
                print("SAVED", dest.stat().st_size)
                return
            if st in {"failed", "error"}:
                raise RuntimeError(str(meta)[:500])
        raise TimeoutError("scene-096 did not complete")
    finally:
        try:
            await cdp.__aexit__(None, None, None)
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
    print("ready", m.is_ready(SCENE), "missing", len(m.missing_scenes()))
