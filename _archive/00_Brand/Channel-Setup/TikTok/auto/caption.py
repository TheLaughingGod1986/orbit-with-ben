#!/usr/bin/env python3
"""Build TikTok caption from a SHORTS_UPLOAD_INDEX entry.

Lead with an existential / wonder hook (space-doc stop-scroll pattern), then
one clarifying line + soft YouTube funnel CTA + hashtags.
"""
from __future__ import annotations

import re


EXISTENTIAL_OPENERS = (
    r"^where is everybody",
    r"^what if",
    r"^cross this line",
    r"^would you",
    r"^are we alone",
    r"^it rains",
    r"^we found",
    r"^falling in",
    r"^time stops",
    r"^space is rude",
    r"^could any",
    r"^the point of no return",
    r"^what your eyes",
    r"^a world made",
    r"^three suns",
    r"^eyeball",
)


def _first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text).strip()


def existential_hook(short: dict) -> str:
    """Prefer title wonder-hook; fall back to first description sentence."""
    title = (short.get("title") or "").strip()
    # Strip trailing hashtags from title
    title = re.sub(r"\s#\w+(\s#\w+)*\s*$", "", title).strip()
    if title:
        # Soften ALL-CAPS leftovers
        if title.isupper():
            title = title.capitalize()
        return title

    desc = (short.get("description") or "").strip()
    first = _first_sentence(desc.split("\n\n")[0] if desc else "")
    return first or "One moment from the full film"


def tiktok_caption(short: dict, *, max_len: int = 2100) -> str:
    title = (short.get("title") or "").strip()
    desc = (short.get("description") or "").strip()
    hook = existential_hook(short)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", desc) if p.strip()]
    prose = ""
    hashtags = ""
    for p in paragraphs:
        if p.startswith("#") or re.match(r"^(Full |Watch )", p, re.I):
            if p.startswith("#"):
                hashtags = p
            continue
        lines = []
        for line in p.splitlines():
            if re.search(r"https?://|youtu\.be|Full film|Watch the full", line, re.I):
                continue
            lines.append(line)
        chunk = " ".join(x.strip() for x in lines if x.strip())
        if chunk and not prose:
            prose = chunk

    if not hashtags:
        tags = re.findall(r"#\w+", desc)
        if tags:
            seen: set[str] = set()
            uniq = []
            for t in tags:
                if t.lower() not in seen:
                    seen.add(t.lower())
                    uniq.append(t)
            hashtags = " ".join(uniq[:12])

    # Clarifier: if prose is just a longer restatement of the hook, keep one beat
    clarifier = ""
    if prose:
        hook_l = hook.lower().rstrip(".!?")
        prose_l = prose.lower()
        if not prose_l.startswith(hook_l[: min(24, len(hook_l))]):
            clarifier = _first_sentence(prose)
        else:
            # Use second sentence if present
            rest = prose[len(_first_sentence(prose)) :].strip()
            clarifier = _first_sentence(rest) if rest else ""

    cta = "Full film on YouTube."
    parts: list[str] = []
    # Hook always first — existential lead
    parts.append(hook.rstrip(".") + ("." if not hook.endswith(("?", "!")) else ""))
    if clarifier and clarifier.lower().rstrip(".!?") not in hook.lower():
        parts.append(clarifier)
    parts.append(cta)
    if hashtags:
        parts.append(hashtags)
    elif "#orbitwithben" not in (hook + prose).lower():
        parts.append("#space #orbitwithben #shorts")

    caption = " ".join(p for p in parts if p).strip()
    caption = re.sub(r"\s+", " ", caption)
    # Ensure opener still reads existential when title was weak
    if not any(re.search(p, caption, re.I) for p in EXISTENTIAL_OPENERS):
        if title and not caption.lower().startswith(title.lower()[:12]):
            caption = f"{hook} {caption}".strip()
            caption = re.sub(r"\s+", " ", caption)
    if len(caption) > max_len:
        caption = caption[: max_len - 1].rstrip() + "…"
    return caption


def confirm_needle(short: dict, caption: str) -> str:
    title = (short.get("title") or "").strip()
    if len(title) >= 12:
        return title[:40]
    return caption[:40]
