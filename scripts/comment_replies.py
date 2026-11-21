#!/usr/bin/env python3
"""Read new comments on every registered channel, triage them, and draft a reply.

The run is registry-driven: token name, voice and topic bans come from the channel
record and from that channel's studio/RULES.md ("## Comment voice"). Nothing is
posted until 05_Analytics/comments/VOICE_APPROVED contains a yes. That file is
Ben's one voice check. Until then this is a dry run.

Never deletes, hides or reports a comment, and never changes pinning or privacy.
A claimed correction is escalated for a facts check. This tool does not edit a
pinned comment and does not invent a number that was not in the comment.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import channels  # noqa: E402

LIST_COST = 1
VIDEO_COST = 1
INSERT_COST = 50
DAILY_CAP = 3000
MAX_REPLIES = 20
MAX_PAGES = 2
FRESH_HOURS = 48
VOICE_FILE = pathlib.Path("05_Analytics") / "comments" / "VOICE_APPROVED"
SAMPLE_FILE = pathlib.Path("05_Analytics") / "comments" / "VOICE_SAMPLES.md"

EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)")
EMOJI = re.compile("[" "\U0001F300-\U0001FAFF" "\U00002600-\U000027BF" "]+")
QUESTION = re.compile(
    r"\?|\b(how|why|what|when|where|who|which|can you|could you|is it|are these|do you)\b",
    re.I)
IDEA = re.compile(r"\b(?:video|film|episode)\s+(?:on|about)\s+(.{3,80})", re.I)
SPAM = re.compile(
    r"(check out my|sub4sub|bit\.ly|onlyfans|airdrop|click here|free followers|https?://|www\.)",
    re.I)
ABUSE = re.compile(r"\b(idiot|moron|kill yourself|kys|stupid channel)\b", re.I)
BAIT = re.compile(r"\b(you won't believe|first comment|like if you|who else)\b", re.I)
CRITIC = re.compile(r"\b(boring|clickbait|unsubscribe|waste of time|hate this|not worth)\b", re.I)
ESCALATE = (
    ("sponsor", re.compile(r"\b(sponsor|sponsorship|collab|business enquir|press|journalist|media kit)\b", re.I)),
    ("copyright", re.compile(r"\b(copyright|dmca|lawyer|legal action|lawsuit)\b", re.I)),
    ("correction", re.compile(
        r"\b(you(?:'re| are) wrong|incorrect|factually|you got .{0,40}wrong|that's a mistake|this is wrong)\b", re.I)),
    ("threat", re.compile(r"\b(kill you|i will find you|i'll find you|doxx|threaten)\b", re.I)),
    ("personal", re.compile(
        r"\b((?:your|his|her) (?:wife|husband|family|kids|children|mum|mom|dad|address|phone))\b", re.I)),
    ("harm", re.compile(
        r"\b(hope it (?:crashes|hits|kills)|populated area|kill (?:people|everyone|them))\b", re.I)),
)
STOCK = re.compile(
    r"^(great question|good question|thanks for watching|awesome comment|love this comment)\b", re.I)
PROMISE = re.compile(r"\b(next (?:video|film)|coming soon|stay tuned|future film|we will (?:make|cover))\b", re.I)
HUMAN_CLAIM = re.compile(r"\b(i am human|i'm human|i am a real person|i'm a real person)\b", re.I)
BEN_CLAIM = re.compile(r"\bben (personally|himself|filmed|said|replied)\b", re.I)
LINK = re.compile(r"https?://|www\.|\bsubscribe\b", re.I)
AMERICAN = (
    (re.compile(r"\bfavorite\b", re.I), "favourite"),
    (re.compile(r"\bcolors\b", re.I), "colours"),
    (re.compile(r"\bcolor\b", re.I), "colour"),
    (re.compile(r"\brealizes\b", re.I), "realises"),
    (re.compile(r"\brealize\b", re.I), "realise"),
    (re.compile(r"\bcenter\b", re.I), "centre"),
    (re.compile(r"\btoward\b", re.I), "towards"),
)
OPENERS = (
    "You wrote about \"{bit}\".",
    "The part that stands out is \"{bit}\".",
    "\"{bit_cap}\" is a fair thing to raise.",
    "Taking \"{bit}\" on its own.",
    "Your note comes down to \"{bit}\".",
    "What you picked out is \"{bit}\".",
)
CLOSES = (
    "The film keeps to the account in its sources, so this reply adds no fresh figure.",
    "What the film shows is the sourced account, and that is the one to trust here.",
    "The sources under the video are the check on that, rather than a new claim.",
    "That stays with the film's sources, which are the ones named under the video.",
    "The careful answer is the one already sourced in the film.",
    "Nothing new is added here beyond what those sources already back.",
)
IDEA_CLOSES = (
    "That request is noted with the others, and there is no date to promise.",
    "It is on the list of requests, with no promise of a film.",
    "Noted, alongside the other requests. No date is promised.",
)
AI_LINES = (
    "The channel uses AI tools to help reply.",
    "Fair to ask. The channel uses AI tools to help reply.",
    "Happy to say it plainly. The channel uses AI tools to help reply.",
)
EXAMPLES = (
    "How did you work out that distance?",
    "Is the number in the film the average or the closest pass?",
    "What does that part look like from the surface?",
    "Are these replies written by a person or by an AI tool?",
    "Could you do a film about the rings of that planet?",
)


def redact(text: str) -> str:
    text = EMAIL.sub("[email]", text or "")
    return PHONE.sub("[phone]", text)


def to_british(text: str) -> str:
    for pattern, repl in AMERICAN:
        text = pattern.sub(repl, text)
    return text


def voice_text(channel: dict, checkout: pathlib.Path | None) -> str:
    """The Comment voice section of studio/RULES.md, else the registry fallback."""
    if checkout:
        rules = checkout / "studio" / "RULES.md"
        if rules.is_file():
            text = rules.read_text(errors="replace")
            match = re.search(r"^## Comment voice\s*$", text, re.M)
            if match:
                rest = text[match.end():]
                nxt = re.search(r"^## ", rest, re.M)
                return (rest[: nxt.start()] if nxt else rest).strip()
    return str((channel.get("comments") or {}).get("voice") or "").strip()


def is_question(text: str) -> bool:
    return bool(QUESTION.search(text or ""))


def idea_subject(text: str) -> str:
    match = IDEA.search(text or "")
    if not match:
        return ""
    return match.group(1).strip(" ?.!\"'")[:80]


def snippet(text: str) -> str:
    clean = redact(re.sub(r"\s+", " ", text or "").strip())
    clean = re.sub(r"^(hi|hello|hey)[,!\s]+", "", clean, flags=re.I)
    sentence = re.split(r"[.!?]", clean)[0].strip()
    words = sentence.split()
    if len(words) > 12:
        words = words[:12]
    bit = " ".join(words).strip(" \"'")
    if bit:
        bit = bit[:1].lower() + bit[1:]
    return bit or "that"


def _index(key: str, n: int) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % n


def opening_of(text: str) -> str:
    return " ".join(text.split()[:4]).lower()


def lint(text: str, comment: str, used: set[str]) -> list[str]:
    problems = []
    if LINK.search(text) or "subscribe" in text.lower():
        problems.append("link or subscribe")
    if STOCK.search(text.strip()):
        problems.append("stock opener")
    if EMOJI.search(text):
        problems.append("emoji")
    if HUMAN_CLAIM.search(text):
        problems.append("claims to be human")
    if BEN_CLAIM.search(text):
        problems.append("claims a personal act")
    if PROMISE.search(text):
        problems.append("promises a film")
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not 1 <= len(sentences) <= 3:
        problems.append("length")
    extra = set(re.findall(r"\d[\d,.]*", text)) - set(re.findall(r"\d[\d,.]*", comment or ""))
    if extra:
        problems.append("new number")
    words = {w.lower().strip(".,!?\"'") for w in re.findall(r"[A-Za-z]{4,}", comment or "")}
    reply_words = {w.lower().strip(".,!?\"'") for w in re.findall(r"[A-Za-z]{4,}", text)}
    if words and not (words & reply_words):
        problems.append("not specific")
    if opening_of(text) in used:
        problems.append("repeat")
    return problems


def draft_reply(comment: dict, profile: dict, used: set[str] | None = None) -> str:
    """One to three British sentences, specific to this comment, with no new fact."""
    used = used if used is not None else set()
    text = redact(comment.get("text") or "")
    bit = snippet(text)
    bit_cap = bit[0].upper() + bit[1:] if bit else "That"
    key = str(comment.get("id") or bit)
    configured = (profile.get("ai_line") or "").strip() or AI_LINES[0]
    if re.search(r"\b(ai|artificial|automated|a bot|robot)\b", text, re.I) and is_question(text):
        for shift in range(len(OPENERS)):
            opener = OPENERS[(_index(key + "ai", len(OPENERS)) + shift) % len(OPENERS)]
            line = to_british(f"{opener.format(bit=bit, bit_cap=bit_cap)} {configured}")
            if not lint(line, text, used):
                return line
        return to_british(f"You asked about \"{bit}\". {configured}")
    if comment.get("idea") or idea_subject(text):
        pool = IDEA_CLOSES
        for shift in range(len(OPENERS)):
            opener = OPENERS[(_index(key + "idea", len(OPENERS)) + shift) % len(OPENERS)]
            close = pool[(_index(key + "close", len(pool)) + shift) % len(pool)]
            line = to_british(f"{opener.format(bit=bit, bit_cap=bit_cap)} {close}")
            if not lint(line, text, used):
                return line
        return to_british(f"You asked about \"{bit}\". That request is noted, and no date is promised.")
    for shift in range(len(OPENERS)):
        opener = OPENERS[(_index(key, len(OPENERS)) + shift) % len(OPENERS)]
        close = CLOSES[(_index(key + "c", len(CLOSES)) + shift) % len(CLOSES)]
        line = to_british(f"{opener.format(bit=bit, bit_cap=bit_cap)} {close}")
        if not lint(line, text, used):
            return line
    return to_british(f"You wrote about \"{bit}\". The film stays with its sources on that.")


def triage(comment: dict, profile: dict) -> tuple[str, str]:
    """reply, log, escalate or ignore. Escalate and ignore are never auto-replied."""
    text = comment.get("text") or ""
    if comment.get("by_channel"):
        return "ignore", "own comment"
    if not redact(text).strip() or (EMOJI.sub("", text).strip() == "" and not is_question(text)):
        return "ignore", "empty"
    if EMAIL.search(text) or PHONE.search(text):
        return "escalate", "personal information"
    for reason, pattern in ESCALATE:
        if pattern.search(text):
            return "escalate", reason
    never = (profile.get("comments") or profile).get("never_re") or profile.get("never_re") or []
    for raw in never:
        if re.search(raw, text, re.I):
            return "escalate", "channel ban"
    if SPAM.search(text) or ABUSE.search(text) or BAIT.search(text):
        return "ignore", "spam"
    if CRITIC.search(text):
        return "log", "critic"
    if idea_subject(text):
        return ("reply", "idea") if is_question(text) else ("log", "idea")
    if is_question(text) or len(text.split()) >= 8:
        return "reply", "question" if is_question(text) else "note"
    if len(text.split()) < 4:
        return "log", "short"
    return "log", "note"


def priority(comment: dict, now: dt.datetime) -> tuple:
    published = _parse(comment.get("video_published") or comment.get("published"))
    age = (now - published).total_seconds() / 3600 if published else 10_000
    fresh = 0 if age <= FRESH_HOURS else 1
    question = 0 if comment.get("question") else 1
    stamp = published.timestamp() if published else 0
    return (fresh, question, -stamp)


def _parse(value) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def flatten_thread(thread: dict, channel_id: str) -> list[dict]:
    """Top-level comments and replies, minus the channel's own posts."""
    snip = ((thread.get("snippet") or {}).get("topLevelComment") or {})
    top = snip.get("snippet") or {}
    top_id = snip.get("id") or ""
    video = (thread.get("snippet") or {}).get("videoId") or top.get("videoId") or ""
    replies = ((thread.get("replies") or {}).get("comments") or [])
    authors = []
    rows = []

    def row(cid, body, published, parent, author):
        own = bool(channel_id) and author == channel_id
        authors.append((published or "", own, cid))
        return {
            "id": cid,
            "video": video,
            "thread": top_id or cid,
            "text": body or "",
            "published": published or "",
            "parent": parent,
            "author_channel": author,
            "by_channel": own,
        }

    if top_id:
        author = ((top.get("authorChannelId") or {}).get("value") or "")
        rows.append(row(top_id, top.get("textOriginal") or top.get("textDisplay") or "",
                        top.get("publishedAt"), None, author))
    for reply in replies:
        body = reply.get("snippet") or {}
        author = ((body.get("authorChannelId") or {}).get("value") or "")
        rows.append(row(reply.get("id") or "", body.get("textOriginal") or "",
                        body.get("publishedAt"), body.get("parentId") or top_id, author))
    channel_times = [t for t, own, _cid in authors if own and t]
    latest_own = max(channel_times) if channel_times else ""
    for item in rows:
        item["follow_up"] = bool(latest_own) and not item["by_channel"] and item["published"] > latest_own
        item["channel_already_replied"] = bool(latest_own) and not item["follow_up"] and not item["by_channel"]
    return rows


class Quota:
    def __init__(self, path: pathlib.Path, now: dt.datetime):
        self.path = path
        self.day = now.astimezone(dt.timezone.utc).date().isoformat()
        self.units = 0
        if path.is_file():
            try:
                saved = json.loads(path.read_text())
            except ValueError:
                saved = {}
            if saved.get("date") == self.day:
                self.units = int(saved.get("units") or 0)

    def room(self, cost: int) -> bool:
        return self.units + cost <= DAILY_CAP

    def charge(self, cost: int) -> None:
        if not self.room(cost):
            raise RuntimeError("daily comment unit cap reached")
        self.units += cost
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"date": self.day, "units": self.units}) + "\n")


def comments_dir(slug: str) -> pathlib.Path:
    path = channels.analytics_dir(slug) / "comments"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_json(path: pathlib.Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text())
    except ValueError:
        return default


def _append(path: pathlib.Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def recent_openings(directory: pathlib.Path, now: dt.datetime) -> set[str]:
    found = set()
    path = directory / "replies.jsonl"
    if not path.is_file():
        return found
    cutoff = now - dt.timedelta(days=7)
    for line in path.read_text(errors="replace").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        when = _parse(row.get("time"))
        if when and when >= cutoff and row.get("text"):
            found.add(opening_of(row["text"]))
    return found


def seen_ids(directory: pathlib.Path) -> set[str]:
    return set(_read_json(directory / "seen.json", []))


def remember(directory: pathlib.Path, comment_id: str) -> None:
    current = seen_ids(directory)
    current.add(comment_id)
    (directory / "seen.json").write_text(json.dumps(sorted(current)) + "\n")


def log_idea(directory: pathlib.Path, subject: str, video: str) -> None:
    path = directory / "ideas.json"
    data = _read_json(path, {})
    row = data.get(subject) or {"subject": subject, "count": 0, "videos": []}
    row["count"] = int(row.get("count") or 0) + 1
    if video and video not in row["videos"]:
        row["videos"].append(video)
    data[subject] = row
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def voice_approved(root: pathlib.Path | None = None) -> bool:
    path = (root or channels.ROOT) / VOICE_FILE
    if not path.is_file():
        return False
    return bool(re.search(r"\byes\b", path.read_text(errors="replace"), re.I))


def example_comments() -> list[dict]:
    return [{"id": f"example-{i}", "video": "", "thread": f"example-{i}", "text": text,
             "published": "", "example": True, "question": True} for i, text in enumerate(EXAMPLES, 1)]


def _profile(channel: dict) -> dict:
    try:
        checkout = channels.checkout(channel["slug"])
    except KeyError:
        checkout = None
    cfg = dict(channel.get("comments") or {})
    cfg["voice"] = voice_text(channel, checkout)
    cfg["name"] = channel.get("name") or channel["slug"]
    cfg["slug"] = channel["slug"]
    cfg["channel_id"] = ((channel.get("youtube") or {}).get("id") or "")
    return cfg


def _studio_root() -> pathlib.Path:
    """The checkout that holds the studio .env. A linked worktree does not."""
    root = channels.ROOT
    if (root / "07_Content-Ops" / ".env").is_file():
        return root
    try:
        import subprocess
        common = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--git-common-dir"], text=True).strip()
        main = pathlib.Path(common).resolve().parent
        if (main / "07_Content-Ops" / ".env").is_file():
            return main
    except (OSError, subprocess.SubprocessError):
        pass
    return root


def _env_path(profile: dict) -> pathlib.Path:
    rel = profile.get("env_file") or "07_Content-Ops/.env"
    if profile.get("env_from") == "checkout":
        root = channels.checkout(profile["slug"]) or channels.repo_path(profile["slug"])
    else:
        root = _studio_root()
    return pathlib.Path(root) / rel


def read_env(path: pathlib.Path) -> dict:
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def _token(env: dict, name: str) -> str:
    """Exchange a refresh token. The values never leave this function as text."""
    if not name or name not in env or "GOOGLE_CLIENT_ID" not in env or "GOOGLE_CLIENT_SECRET" not in env:
        raise RuntimeError("upload login missing")
    body = urllib.parse.urlencode({
        "client_id": env["GOOGLE_CLIENT_ID"],
        "client_secret": env["GOOGLE_CLIENT_SECRET"],
        "refresh_token": env[name],
        "grant_type": "refresh_token",
    }).encode()
    request = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"token refresh failed ({exc.code})") from None
    token = payload.get("access_token") or ""
    if not token:
        raise RuntimeError("token refresh failed")
    return token


def _get(url: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, method="POST" if payload is not None else "GET")
    request.add_header("Authorization", "Bearer " + token)
    if payload is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"youtube http {exc.code}") from None


class LiveClient:
    def __init__(self, token: str):
        self.token = token

    def list_threads(self, channel_id: str) -> list[dict]:
        threads = []
        page = ""
        for _ in range(MAX_PAGES):
            query = {
                "part": "snippet,replies",
                "allThreadsRelatedToChannelId": channel_id,
                "maxResults": "20",
                "order": "time",
                "textFormat": "plainText",
            }
            if page:
                query["pageToken"] = page
            url = "https://www.googleapis.com/youtube/v3/commentThreads?" + urllib.parse.urlencode(query)
            payload = _get(url, self.token)
            threads.append(payload)
            page = payload.get("nextPageToken") or ""
            if not page:
                break
        return threads

    def list_videos(self, ids: list[str]) -> dict:
        if not ids:
            return {}
        query = urllib.parse.urlencode({
            "part": "snippet",
            "id": ",".join(ids[:50]),
            "fields": "items(id,snippet/publishedAt,snippet/title)",
        })
        payload = _get("https://www.googleapis.com/youtube/v3/videos?" + query, self.token)
        out = {}
        for item in payload.get("items") or []:
            snip = item.get("snippet") or {}
            out[item.get("id")] = {"published": snip.get("publishedAt") or "", "title": snip.get("title") or ""}
        return out

    def insert(self, parent_id: str, text: str) -> dict:
        url = "https://www.googleapis.com/youtube/v3/comments?part=snippet"
        payload = _get(url, self.token, {"snippet": {"parentId": parent_id, "textOriginal": text}})
        return {"id": payload.get("id") or ""}


def _quota_for(env: dict, now: dt.datetime) -> Quota:
    client_id = env.get("GOOGLE_CLIENT_ID") or "missing"
    qid = hashlib.sha256(client_id.encode()).hexdigest()[:12]
    return Quota(channels.studio_records("comments", "quota", f"{qid}.json"), now)


def _samples(comments: list[dict], profile: dict, used: set[str], live: bool) -> list[dict]:
    rows = []
    for comment in comments:
        if len(rows) >= 5 and any(r.get("honest") for r in rows):
            break
        action, reason = triage(comment, profile)
        if action != "reply" and not comment.get("example"):
            continue
        text = draft_reply(comment, profile, used)
        used.add(opening_of(text))
        rows.append({
            "viewer": redact(comment.get("text") or ""),
            "reply": text,
            "example": bool(comment.get("example")),
            "live": live and not comment.get("example"),
            "reason": reason,
            "honest": bool(re.search(r"\bAI tools\b", text)),
        })
        if len(rows) >= 5 and any(r.get("honest") for r in rows):
            break
    if not any(r.get("honest") for r in rows):
        honest = next(c for c in example_comments() if "AI" in c["text"])
        text = draft_reply(honest, profile, used)
        rows.append({"viewer": honest["text"], "reply": text, "example": True, "live": False,
                     "reason": "honest", "honest": True})
    return rows[:6]


def _write_summary(directory: pathlib.Path, card: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n")


def run_channel(channel: dict, *, now: dt.datetime, post: bool, client=None,
                threads: list | None = None, videos: dict | None = None, approved: bool = False) -> dict:
    """Triage one channel. A reply is posted only when the voice check has passed."""
    post = bool(post and approved)
    profile = _profile(channel)
    directory = comments_dir(channel["slug"])
    used = recent_openings(directory, now)
    seen = seen_ids(directory)
    error = ""
    raw_threads = threads
    video_meta = videos or {}
    if raw_threads is None and client is not None and profile.get("channel_id"):
        try:
            raw_threads = client.list_threads(profile["channel_id"])
            ids = []
            for page in raw_threads:
                for thread in page.get("items") or []:
                    vid = (thread.get("snippet") or {}).get("videoId")
                    if vid and vid not in ids:
                        ids.append(vid)
            if ids and hasattr(client, "list_videos"):
                video_meta = client.list_videos(ids)
        except RuntimeError as exc:
            error = str(exc)
            raw_threads = []
    comments = []
    for page in raw_threads or []:
        for thread in page.get("items") or []:
            for comment in flatten_thread(thread, profile.get("channel_id") or ""):
                meta = video_meta.get(comment["video"]) or {}
                comment["video_published"] = meta.get("published") or ""
                comment["title"] = meta.get("title") or ""
                comment["question"] = is_question(comment["text"])
                comment["idea"] = idea_subject(comment["text"])
                comments.append(comment)
    fresh = [c for c in comments if c["id"] and c["id"] not in seen and not c.get("by_channel")]
    ranked = sorted(fresh, key=lambda c: priority(c, now))
    replied = 0
    escalated = []
    themes: dict[str, int] = {}
    answered_threads = set()
    drafted = []
    for comment in ranked:
        for word in re.findall(r"[A-Za-z]{5,}", comment["text"].lower()):
            if word not in {"about", "would", "could", "there", "their", "which", "where", "these"}:
                themes[word] = themes.get(word, 0) + 1
        action, reason = triage(comment, profile)
        if comment.get("idea"):
            log_idea(directory, comment["idea"], comment.get("video") or "")
        if action == "escalate":
            escalated.append({"video": comment.get("video") or "", "comment_id": comment["id"],
                              "reason": reason, "text": redact(comment["text"])[:240],
                              "time": now.isoformat()})
            _append(directory / "escalations.jsonl", escalated[-1])
            continue
        if action != "reply":
            continue
        if comment.get("channel_already_replied") and not comment.get("follow_up"):
            continue
        if comment["thread"] in answered_threads and not comment.get("follow_up"):
            continue
        if replied >= MAX_REPLIES:
            break
        text = draft_reply(comment, profile, used)
        problems = lint(text, comment["text"], used)
        if problems:
            escalated.append({"video": comment.get("video") or "", "comment_id": comment["id"],
                              "reason": "draft rejected: " + ", ".join(problems),
                              "text": redact(comment["text"])[:240], "time": now.isoformat()})
            _append(directory / "escalations.jsonl", escalated[-1])
            continue
        if post:
            if client is None or not hasattr(client, "insert"):
                error = error or "no client to post"
                break
            result = client.insert(comment["id"], text)
            _append(directory / "replies.jsonl", {
                "video": comment.get("video") or "",
                "comment_id": comment["id"],
                "text": text,
                "reply_id": result.get("id") or "",
                "time": now.isoformat(),
            })
            remember(directory, comment["id"])
        used.add(opening_of(text))
        answered_threads.add(comment["thread"])
        replied += 1
        drafted.append(comment)
    if len(drafted) < 5:
        drafted = list(drafted) + example_comments()
    samples = _samples(drafted, profile, set(), live=bool(raw_threads))
    top = [w for w, _n in sorted(themes.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
    card = {
        "slug": channel["slug"],
        "name": profile["name"],
        "new": len(fresh),
        "replied": replied if post else 0,
        "drafted": replied,
        "escalated": len(escalated),
        "themes": top,
        "error": error,
        "at": now.isoformat(),
    }
    _write_summary(directory, card)
    return {"card": card, "samples": samples, "escalated": escalated, "error": error, "posted": replied if post else 0}


def board_cards() -> list[dict]:
    """One Comments card per registered channel, from the last summary. Never raises on a bad file."""
    rows = []
    for channel in channels.all_channels():
        path = channels.analytics_dir(channel["slug"]) / "comments" / "summary.json"
        data = _read_json(path, {})
        rows.append({
            "slug": channel["slug"],
            "name": channel.get("name") or channel["slug"],
            "new": int(data.get("new") or 0),
            "replied": int(data.get("replied") or 0),
            "escalated": int(data.get("escalated") or 0),
            "themes": list(data.get("themes") or [])[:3],
        })
    return rows


def _section(card: dict, samples: list[dict], voice: str) -> str:
    lines = [f"## {card['name']}", "", f"Voice: {voice or '(no Comment voice section yet)'}", ""]
    if card.get("error"):
        lines.append(f"Fetch: {card['error']}. Samples below include examples where a live comment was not available.")
        lines.append("")
    for i, sample in enumerate(samples, 1):
        kind = "live comment" if sample.get("live") else "example, not posted"
        lines.append(f"{i}. Viewer ({kind}): {sample['viewer']}")
        lines.append(f"   Reply: {sample['reply']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_samples(sections: list[str], path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        "# Comment voice samples",
        "",
        "Nothing in this file has been posted. Replies stay off until this folder's",
        "VOICE_APPROVED file contains a yes from Ben's one voice check.",
        "For the first two days after that, the Chief reads ten replies a day on each channel.",
        "",
    ]
    body.extend(sections)
    path.write_text("\n".join(body).rstrip() + "\n")


def batch_line(cards: list[dict]) -> str:
    parts = []
    for card in cards:
        if not card.get("escalated"):
            continue
        reasons = []
        for row in card.get("rows") or []:
            if row["reason"] not in reasons:
                reasons.append(row["reason"])
        parts.append(f"{card['name']}: {card['escalated']} ({', '.join(reasons[:3])})")
    if not parts:
        return ""
    return "Comments to look at today: " + "; ".join(parts) + "."


def live_client(profile: dict, now: dt.datetime):
    """Build a client and a quota bucket, or (None, None, reason) when the login is missing."""
    env = read_env(_env_path(profile))
    name = profile.get("token_env") or ""
    if not name or name not in env:
        return None, None, "upload login missing"
    try:
        token = _token(env, name)
    except RuntimeError as exc:
        return None, None, str(exc)
    return LiveClient(token), _quota_for(env, now), ""


def run_all(*, post: bool = False, now: dt.datetime | None = None, out: pathlib.Path | None = None,
            examples_only: bool = False) -> dict:
    now = now or dt.datetime.now(dt.timezone.utc)
    approved = voice_approved()
    do_post = bool(post and approved and not examples_only)
    sections = []
    cards = []
    posted = 0
    for channel in channels.all_channels():
        profile = _profile(channel)
        client = None
        note = ""
        quota = None
        if not examples_only:
            client, quota, note = live_client(profile, now)
        if client is not None and quota is not None:

            class _Capped:
                def __init__(self, inner, bucket):
                    self.inner = inner
                    self.bucket = bucket

                def list_threads(self, channel_id):
                    if not self.bucket.room(LIST_COST * MAX_PAGES):
                        raise RuntimeError("daily comment unit cap reached")
                    rows = self.inner.list_threads(channel_id)
                    self.bucket.charge(LIST_COST * max(1, len(rows)))
                    return rows

                def list_videos(self, ids):
                    if not ids:
                        return {}
                    if not self.bucket.room(VIDEO_COST):
                        return {}
                    self.bucket.charge(VIDEO_COST)
                    return self.inner.list_videos(ids)

                def insert(self, parent_id, text):
                    if not self.bucket.room(INSERT_COST):
                        raise RuntimeError("daily comment unit cap reached")
                    self.bucket.charge(INSERT_COST)
                    return self.inner.insert(parent_id, text)

            client = _Capped(client, quota)
        result = run_channel(channel, now=now, post=do_post, approved=approved, client=client,
                             threads=[] if client is None else None)
        if note and not result["error"]:
            result["card"]["error"] = note
            result["error"] = note
        result["card"]["rows"] = result["escalated"]
        sections.append(_section(result["card"], result["samples"], profile.get("voice") or ""))
        cards.append(result["card"])
        posted += result["posted"]
    out = out or (channels.ROOT / SAMPLE_FILE)
    write_samples(sections, out)
    line = batch_line(cards)
    if line:
        day = now.astimezone(dt.timezone.utc).date().isoformat()
        path = channels.studio_records("comments", f"for-ben-{day}.txt")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and line in path.read_text():
            pass
        else:
            path.write_text(line + "\n")
    return {"approved": approved, "posted": posted, "posting": do_post, "batch": line,
            "out": str(out), "cards": cards}


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft or post comment replies for every registered channel")
    parser.add_argument("command", choices=("dry-run", "run", "summary"))
    parser.add_argument("--out", default="")
    parser.add_argument("--examples-only", action="store_true")
    args = parser.parse_args()
    if args.command == "summary":
        json.dump(board_cards(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    out = pathlib.Path(args.out) if args.out else None
    result = run_all(post=args.command == "run", out=out, examples_only=args.examples_only)
    print(f"samples: {result['out']}")
    print(f"posted: {result['posted']}")
    print(f"voice approved: {result['approved']}")
    if result["batch"]:
        print(result["batch"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
