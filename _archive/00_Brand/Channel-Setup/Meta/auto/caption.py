#!/usr/bin/env python3
"""Build Instagram / Facebook Reel captions from SHORTS_UPLOAD_INDEX entries."""
from __future__ import annotations

import re


def meta_caption(short: dict, *, max_len: int = 2100) -> str:
    title = (short.get("title") or "").strip()
    desc = (short.get("description") or "").strip()

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

    if not prose:
        prose = title

    cta = "Full film on YouTube."
    parts = [prose, cta]
    if hashtags:
        parts.append(hashtags)
    elif "#orbitwithben" not in prose.lower():
        parts.append("#space #orbitwithben #reels")

    caption = " ".join(p for p in parts if p).strip()
    caption = re.sub(r"\s+", " ", caption)
    if len(caption) > max_len:
        caption = caption[: max_len - 1].rstrip() + "…"
    return caption


def confirm_needle(short: dict, caption: str) -> str:
    title = (short.get("title") or "").strip()
    if len(title) >= 12:
        return title[:40]
    return caption[:40]
