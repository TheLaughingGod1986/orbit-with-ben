#!/usr/bin/env python3
"""Submit Seedance jobs via ElevenLabs UI, harvest via HTTP, then rebuild v10.

Faster than waiting inline: submit → record gid → continue; a parallel
harvester downloads completed clips into the matching scene files.
"""
from __future__ import annotations

import asyncio
import json
import re
import time
import urllib.request
from pathlib import Path

import httpx

import _animate_bold_scenes_elevenlabs_v10 as m

PENDING = Path(__file__).with_name("bold-explainer-v11-pending.jsonl")
MAX_IN_FLIGHT = 3
SUBMIT_PAUSE = 2.0


def motion_key(prompt: str) -> str:
    mobj = re.search(r"comes alive\.\s*(.+?)\.\s*Stable cinematic", prompt or "", re.S)
    return (mobj.group(1).strip().lower() if mobj else (prompt or "")[:80].lower())


def refresh_token_from_cdp(cdp) -> str:
    # Token is refreshed inside page calls; also mirror to disk for harvester.
    async def _inner():
        tok = await cdp.evaluate(
            """(() => {
              const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
              return auth.stsTokenManager.accessToken;
            })()"""
        )
        Path("/tmp/elevenlabs_bearer.txt").write_text(tok)
        return tok

    return _inner()


def load_pending() -> dict[str, str]:
    """gid -> scene name"""
    mapping: dict[str, str] = {}
    if PENDING.exists():
        for line in PENDING.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("gid") and rec.get("scene"):
                mapping[rec["gid"]] = rec["scene"]
    return mapping


def append_pending(gid: str, scene: str) -> None:
    with PENDING.open("a") as handle:
        handle.write(json.dumps({"gid": gid, "scene": scene, "ts": time.time()}) + "\n")


def bearer() -> str:
    return Path("/tmp/elevenlabs_bearer.txt").read_text().strip()


def used_generation_ids() -> set[str]:
    used: set[str] = set()
    if m.PROGRESS.exists():
        for line in m.PROGRESS.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            gid = rec.get("generation_id")
            if gid and rec.get("status") == "generated":
                used.add(gid)
    return used


def harvest_once(pending: dict[str, str]) -> int:
    """Download completed gens. Prefer pending gid→scene map; never reuse a gid.

    Never overwrite an existing ready bed. Motion-key fallback only assigns to
    scenes that are still missing after pending-map downloads in this pass.
    """
    headers = {"Authorization": f"Bearer {bearer()}"}
    r = httpx.get(
        "https://api.us.elevenlabs.io/v1/content/generations?per_page=40",
        headers=headers,
        timeout=60,
    )
    if r.status_code == 401:
        return -1
    r.raise_for_status()
    gens = r.json().get("generations") or r.json().get("items") or []
    downloaded = 0
    used = used_generation_ids()
    claimed: set[str] = set()  # scene names claimed this pass

    def _download(scene: Path, gid: str, g: dict) -> bool:
        dest = m.out_path(scene)
        if m.is_ready(scene) or scene.name in claimed:
            return False
        url = g.get("download_url") or g.get("content_url")
        if not url:
            detail = httpx.get(
                f"https://api.us.elevenlabs.io/v1/content/generations/{gid}",
                headers=headers,
                timeout=60,
            ).json()
            url = detail.get("download_url") or detail.get("content_url")
        if not url:
            return False
        tmp = dest.with_suffix(".partial.mp4")
        urllib.request.urlretrieve(url, tmp)
        tmp.replace(dest)
        m.append_progress(
            {
                "scene": scene.name,
                "status": "generated",
                "generation_id": gid,
                "output": str(dest),
                "bytes": dest.stat().st_size,
                "via": "pipeline-harvest",
            }
        )
        used.add(gid)
        claimed.add(scene.name)
        print(f"HARVEST {scene.name} <- {gid} ({dest.stat().st_size})", flush=True)
        return True

    # Pass 1: exact pending gid → scene map only
    by_id = {g.get("id"): g for g in gens if g.get("id")}
    for gid, scene_name in list(pending.items()):
        g = by_id.get(gid)
        if not g or g.get("status") != "completed" or gid in used:
            continue
        scene = m.SCENES / scene_name
        if not scene.exists():
            continue
        if _download(scene, gid, g):
            downloaded += 1

    # Pass 2: motion-key fallback for leftover completed gens / missing scenes
    queues: dict[str, list[Path]] = {}
    for sc in m.missing_scenes():
        if sc.name in claimed:
            continue
        queues.setdefault(motion_key(m.prompt_for(sc)), []).append(sc)

    for g in gens:
        gid = g.get("id")
        if not gid or gid in used or g.get("status") != "completed":
            continue
        if gid in pending:
            continue  # already handled or still generating / already ready
        k = motion_key(g.get("prompt") or "")
        if not queues.get(k):
            continue
        scene = queues[k].pop(0)
        if _download(scene, gid, g):
            downloaded += 1
    return downloaded


async def count_in_flight(cdp, pending: dict[str, str]) -> int:
    """Count only mapped pending gids that are still generating.

    Orphan/unmapped API jobs must not block new submits — they confuse the
    queue after crashes and get picked up by motion-key harvest when done.
    """
    if not pending:
        return 0
    gens = await m.list_generations(cdp, per_page=40)
    by_id = {g.get("id"): g for g in gens}
    n = 0
    for gid in pending:
        status = (by_id.get(gid) or {}).get("status")
        if status in {"generating", "pending", "queued"}:
            n += 1
        elif status is None:
            name = pending.get(gid)
            if name and not m.is_ready(m.SCENES / name):
                n += 1
        elif status == "completed":
            # Still pending map entry until harvest lands the file
            name = pending.get(gid)
            if name and not m.is_ready(m.SCENES / name):
                n += 1
    return n


async def submit_one(cdp, scene: Path) -> str:
    prompt = m.prompt_for(scene)
    print(f"SUBMIT {scene.name}", flush=True)
    await m.ensure_composer(cdp)
    await m.ensure_seedance_settings(cdp)
    await m.set_start_frame(cdp, scene)
    await m.set_prompt(cdp, prompt)
    check = await cdp.evaluate(
        """(() => {
          const ed=[...document.querySelectorAll('[contenteditable="true"]')]
            .find(el => el.getBoundingClientRect().width > 100);
          return ed ? (ed.innerText || '').slice(0, 60) : '';
        })()"""
    )
    if "Hand-painted" not in (check or ""):
        raise RuntimeError(f"bad prompt: {check!r}")
    before = set(m.KNOWN_GENERATION_IDS)
    await asyncio.sleep(0.6)
    await m.click_generate(cdp)
    try:
        gid = await m.wait_for_generation_id(cdp, prompt=prompt, timeout=90)
    except TimeoutError:
        # Gen may exist but was marked known mid-poll; recover by newest match.
        gens = await m.list_generations(cdp, per_page=20)
        needle = prompt[:100]
        cand = None
        for item in gens:
            gid = item.get("id")
            if not gid:
                continue
            if needle not in (item.get("prompt") or ""):
                continue
            if gid in before:
                continue
            cand = gid
            break
        if not cand:
            # last resort: newest generating with matching prompt including known
            for item in gens:
                if item.get("status") not in {"generating", "pending", "queued", "completed"}:
                    continue
                if needle not in (item.get("prompt") or ""):
                    continue
                gid = item.get("id")
                if gid and not m.is_ready(scene):
                    # only if this gid isn't already mapped to another missing scene
                    mapped = load_pending()
                    if gid not in mapped:
                        cand = gid
                        break
        if not cand:
            raise
        gid = cand
        m.KNOWN_GENERATION_IDS.add(gid)
        print(f"  recovered gid after wait timeout: {gid}", flush=True)
    append_pending(gid, scene.name)
    print(f"  queued {gid}", flush=True)
    return gid


async def reconnect(cdp):
    print("Reconnecting CDP...", flush=True)
    try:
        await cdp.__aexit__(None, None, None)
    except Exception:
        pass
    await asyncio.sleep(2)
    cdp = await m.connect_cdp()
    await m.ensure_composer(cdp)
    await m.seed_known_ids_from_api(cdp)
    try:
        tok = await cdp.evaluate(
            """(() => {
              const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
              return auth.stsTokenManager.accessToken;
            })()"""
        )
        Path("/tmp/elevenlabs_bearer.txt").write_text(tok)
    except Exception as exc:
        print(f"token refresh failed: {exc}", flush=True)
    return cdp


async def main() -> None:
    m.OUT.mkdir(parents=True, exist_ok=True)
    m.load_known_ids()
    pending = load_pending()
    print(f"Pending map: {len(pending)}  Missing: {len(m.missing_scenes())}", flush=True)

    cdp = await m.connect_cdp()
    try:
        await m.ensure_composer(cdp)
        await m.seed_known_ids_from_api(cdp)
        tok = await cdp.evaluate(
            """(() => {
              const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
              return auth.stsTokenManager.accessToken;
            })()"""
        )
        Path("/tmp/elevenlabs_bearer.txt").write_text(tok)
        harvest_once(pending)

        idle_rounds = 0
        while True:
            try:
                pending = {
                    gid: name
                    for gid, name in {**load_pending(), **pending}.items()
                    if not m.is_ready(m.SCENES / name)
                }
                todo = [
                    s
                    for s in m.missing_scenes()
                    if s.name not in set(pending.values())
                ]
                print(
                    f"\nloop missing={len(m.missing_scenes())} to_submit={len(todo)} in_map={len(pending)}",
                    flush=True,
                )
                if len(m.missing_scenes()) == 0:
                    break

                in_flight = await count_in_flight(cdp, pending)
                print(f"  in_flight={in_flight}", flush=True)

                if todo and in_flight < MAX_IN_FLIGHT:
                    scene = todo[0]
                    try:
                        gid = await submit_one(cdp, scene)
                        pending[gid] = scene.name
                        m.KNOWN_GENERATION_IDS.add(gid)
                        idle_rounds = 0
                    except Exception as exc:
                        print(f"ERROR submit {scene.name}: {exc}", flush=True)
                        m.append_progress(
                            {"scene": scene.name, "status": "error", "error": str(exc)}
                        )
                        try:
                            await cdp.screenshot(Path(f"/tmp/el_err_{scene.stem}.png"))
                        except Exception:
                            pass
                        cdp = await reconnect(cdp)
                        await asyncio.sleep(3)
                else:
                    idle_rounds += 1
                    await asyncio.sleep(5)

                try:
                    tok = await cdp.evaluate(
                        """(() => {
                          const auth=JSON.parse(localStorage.getItem('firebase:authUser:AIzaSyBSsRE_1Os04-bxpd5JTLIniy3UK4OqKys:[DEFAULT]'));
                          return auth.stsTokenManager.accessToken;
                        })()"""
                    )
                    Path("/tmp/elevenlabs_bearer.txt").write_text(tok)
                except Exception:
                    cdp = await reconnect(cdp)

                n = harvest_once(pending)
                if n and n > 0:
                    idle_rounds = 0
                await asyncio.sleep(SUBMIT_PAUSE)

                if len(m.missing_scenes()) == 0:
                    break

                if (not todo) and in_flight == 0:
                    pending = load_pending()
                    harvest_once(pending)
                    pending = {
                        gid: name
                        for gid, name in pending.items()
                        if not m.is_ready(m.SCENES / name)
                    }
                    if len(m.missing_scenes()) == 0:
                        break
                    if idle_rounds >= 3:
                        print("No in-flight; clearing stale pending for resubmit", flush=True)
                        pending = {}
                        idle_rounds = 0

            except Exception as exc:
                print(f"LOOP ERROR: {exc}", flush=True)
                try:
                    cdp = await reconnect(cdp)
                except Exception as exc2:
                    print(f"reconnect failed: {exc2}", flush=True)
                    await asyncio.sleep(10)
                    try:
                        cdp = await m.connect_cdp()
                    except Exception as exc3:
                        print(f"connect failed: {exc3}", flush=True)
                        await asyncio.sleep(20)
                try:
                    harvest_once(pending)
                except Exception:
                    pass

    finally:
        try:
            await cdp.__aexit__(None, None, None)
        except Exception:
            pass

    print(f"Finished. Missing: {len(m.missing_scenes())}", flush=True)
    if len(m.missing_scenes()) == 0:
        print("Rebuilding v10 music+chapters master...", flush=True)
        import subprocess

        script = (
            Path(__file__).resolve().parent / "_build_bold_explainer_v10_music_chapters.py"
        )
        subprocess.check_call(
            [
                str(Path(__file__).resolve().parent / ".venv_orbit/bin/python3"),
                "-u",
                str(script),
            ]
        )


if __name__ == "__main__":
    import traceback

    try:
        asyncio.run(main())
    except Exception:
        traceback.print_exc()
        raise
