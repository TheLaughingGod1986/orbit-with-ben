#!/usr/bin/env python3
"""Bounded external MacBook handoff. No side effects on import; see J3892 README.

The private plan is a capability pinned by its digest, not another job queue.
Only an unchanged trusted thread activation authorizes service replacement.
"""
from __future__ import annotations
import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import subprocess
import sys
import time
import uuid
from macbook import render_worker_plist

LABEL = render_worker_plist.SERVICE_LABEL
TERMINAL = {"done", "cancelled"}
DIGEST = re.compile(r"[0-9a-f]{64}")

class Refused(RuntimeError):
    pass

def require(ok, reason):
    if not ok:
        raise Refused(reason)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def private_write(path, data):
    path = Path(path)
    require(not path.is_symlink(), "symlink output")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def timestamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()

def loaded_settings(text):
    # State, PID, run count and inherited launchd bookkeeping are intentionally
    # excluded. Preserve the raw print privately as well as these exact sections.
    sections = {}
    lines = text.splitlines()
    for name in ("arguments", "environment"):
        start = next((i for i, s in enumerate(lines) if s.strip() == name + " = {"), None)
        require(start is not None, "missing loaded settings")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "}"), None)
        require(end is not None, "invalid loaded settings")
        sections[name] = [s.strip() for s in lines[start + 1:end]]
    return sections

def loaded_matches(text, proposed):
    settings = loaded_settings(text)
    doc = plistlib.loads(proposed)
    require(settings["arguments"] == doc["ProgramArguments"], "loaded arguments mismatch")
    pairs = {}
    for row in settings["environment"]:
        require(" => " in row, "invalid loaded environment")
        key, value = row.split(" => ", 1)
        require(key not in pairs, "duplicate loaded environment")
        pairs[key] = value
    expected = doc.get("EnvironmentVariables", {})
    require(all(pairs.get(k) == str(v) for k,v in expected.items()), "loaded environment mismatch")
    require(not (set(pairs) - set(expected) - {"OSLogRateLimit", "XPC_SERVICE_NAME"}), "unexpected loaded environment")


def proposal(installed, engines, url):
    doc = plistlib.loads(installed)
    require(doc.get("Label") == LABEL, "wrong service")
    doc["ProgramArguments"] = ["/bin/zsh", "-lc",
        'if [[ ! -f "$STUDIO_REPO/scripts/macbook_worker.py" ]]; then '
        'GIT_LFS_SKIP_SMUDGE=1 git clone -q --branch main --depth 50 "$STUDIO_GIT_URL" '
        '"$STUDIO_REPO" || exit 1; fi; exec python3 "$STUDIO_REPO/scripts/macbook_worker.py" run']
    env = doc.setdefault("EnvironmentVariables", {})
    env["STUDIO_REPO"] = str(engines[0])
    env["STUDIO_GIT_URL"] = url
    return plistlib.dumps(doc, sort_keys=False)

def validate_activation(c, plan, plan_hash, now):
    require(c.get("author_association") in {"OWNER", "MEMBER", "COLLABORATOR"}
            and c.get("user", {}).get("type") == "User", "untrusted activation")
    require(c.get("issue_url") == plan["issue_url"], "wrong thread")
    require(c.get("created_at") == c.get("updated_at"), "edited activation")
    age = now - timestamp(c["created_at"])
    require(0 <= age <= 3600 and timestamp(c["created_at"]) >= plan["created"], "stale activation")
    # Trusted owner/collaborator explicitly attests the elected role AND global
    # drain; a tag or arbitrary prose is not a command. No fuzzy parser.
    pattern = (r"\[Chief\] MACBOOK-CUTOVER J3892 coordinator=" + re.escape(plan["job"]) + " "
               + re.escape(plan["nonce"]) + " " + plan_hash
               + r" chief=(claude|codex|gemini|chief) commit=([0-9a-f]{40}) queue=([0-9a-f]{64}) global-freeze=confirmed")
    match = re.fullmatch(pattern, c.get("body", ""))
    require(match is not None, "invalid activation command")
    return {"id": c["id"], "hash": digest(canonical(c)), "chief": match[1],
            "commit": match[2], "queue": match[3]}

def process_identity(row):
    return {key: row[key] for key in ("pid", "pgid", "start")}

def descendants(owners, processes):
    """Conservatively retain every observed descendant identity, even if detached."""
    known = {o["pid"] for o in owners}
    found = []
    while True:
        batch = [p for p in processes if p["pid"] not in known and p.get("ppid") in known]
        if not batch:
            return found
        found.extend(process_identity(p) for p in batch)
        known.update(p["pid"] for p in batch)


def drained(plan, jobs, processes, supervisor):
    coord = next((j for j in jobs if j.get("id") == plan["job"]), {})
    require(coord.get("status") in TERMINAL, "coordinator is not terminal")
    require(not any(j.get("status") == "claimed" and j.get("by") in {"macbook", "macbook-2"}
                    for j in jobs), "MacBook claim remains")
    for owner in plan["owners"]:
        # A reused PID is ambiguous, never interpreted as proof of exit.
        require(not any(p["pid"] == owner["pid"] for p in processes), "owner PID remains or reused")
        require(not any(p["pgid"] == owner["pgid"] for p in processes), "owner process group remains")
    require(not descendants(plan["owners"], processes), "owner descendant remains")
    for p in processes:
        if p["pid"] == supervisor:
            continue
        command = p["command"]
        binary = Path(command.split()[0]).name if command.split() else ""
        require("macbook_worker.py" not in command
                and "/_desk/worker/" not in command and "/studio-live/" not in command and binary not in
                {"codex", "claude", "agy", "agent", "caffeinate"}
                and not re.search(r"(?:^|[/\s])(?:codex|claude|agy|agent)(?:[/\s]|$)", command), "worker or agent child remains")

class System:
    """All command execution has a timeout; tests replace this entire adapter."""
    def __init__(self, deadline=None):
        self.deadline = deadline

    def run(self, argv, cwd=None, input=None):
        remaining = self.deadline - time.time() if self.deadline else 30
        require(remaining > 0, "deadline expired")
        r = subprocess.run(argv, cwd=cwd, capture_output=True, input=input, timeout=min(30, remaining))
        require(r.returncode == 0, "external command failed (private diagnostics withheld)")
        return r.stdout

    def api(self, path):
        return json.loads(self.run(["gh", "api", path]))

    def post(self, plan, body):
        return self.run(["gh", "api", "--method", "POST",
            f"repos/{plan['authority_repo']}/issues/{plan['thread']}/comments", "--input", "-"],
            input=canonical({"body": body}))

    def processes(self):
        rows = []
        for line in self.run(["ps", "-axo", "pid=,ppid=,pgid=,lstart=,command="]).decode().splitlines():
            parts = line.split(None, 8)
            require(len(parts) == 9, "incomplete process table")
            rows.append({"pid": int(parts[0]), "ppid": int(parts[1]), "pgid": int(parts[2]),
                         "start": " ".join(parts[3:8]), "command": parts[8]})
        require(bool(rows), "empty process table")
        return rows

    def queue(self, plan):
        # The production queue exceeds GitHub's inline-content size limit.
        raw = self.run(["gh", "api", "-H", "Accept: application/vnd.github.raw+json",
                        f"repos/{plan['authority_repo']}/contents/jobs/queue.json?ref=main"])
        return json.loads(raw)["jobs"]

    def loaded(self):
        return self.run(["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"])

    def comments(self, plan):
        # Fetch all pages via gh; only parse exact commands below.
        pages = json.loads(self.run(["gh", "api", "--paginate", "--slurp",
              f"repos/{plan['authority_repo']}/issues/{plan['thread']}/comments?per_page=100"]))
        return [c for page in pages for c in page]

    def comment(self, plan, cid):
        return self.api(f"repos/{plan['authority_repo']}/issues/comments/{cid}")

    def git(self, root, *args):
        return self.run(["git", "-C", str(root), *args]).decode().strip()

    def production(self, plan, activation):
        meta = self.api(f"repos/{plan['production_repo']}")
        require(meta.get("private") is True, "production destination must be private")
        branch = self.api(f"repos/{plan['production_repo']}/git/ref/heads/main")
        require(branch["object"]["sha"] == activation["commit"], "production main changed")
        commit = self.api(f"repos/{plan['production_repo']}/git/commits/{activation['commit']}")
        require(commit.get("parents") == [], "production export must be a root commit")
        # Freeze/export must be fresh, not the parentless rehearsal root.
        require(plan["created"] <= timestamp(commit["committer"]["date"]) <= time.time(), "stale production export")

    def update_engine(self, root, plan, activation, backup):
        require(not self.git(root, "status", "--porcelain"), "dirty staged engine")
        require(self.git(root, "rev-parse", "HEAD") == plan["staged_heads"][str(root)], "staged head changed")
        require(self.git(root, "branch", "--show-current") == "main", "staged engine is not main")
        require(self.git(root, "remote", "get-url", "origin") == plan["production_url"], "wrong engine origin")
        self.git(root, "fetch", plan["production_url"], "refs/heads/main")
        require(self.git(root, "rev-parse", "FETCH_HEAD") == activation["commit"], "fetch mismatch")
        # git text normalization adds no newline here; hash exact blob instead.
        qbytes = self.run(["git", "-C", str(root), "show", f"{activation['commit']}:jobs/queue.json"])
        require(digest(qbytes) == activation["queue"], "frozen queue mismatch")
        drained(plan, json.loads(qbytes)["jobs"], self.processes(), os.getpid())
        registry = json.loads(self.git(root, "show", f"{activation['commit']}:channels/channels.json"))
        require(registry["studio"]["github"] == plan["production_repo"], "wrong production registry")
        for path, expected in plan["production_sources"].items():
            data = self.run(["git", "-C", str(root), "show", f"{activation['commit']}:{path}"])
            require(digest(data) == expected, "production source mismatch")
        # Preserve the rehearsal main ref without resetting or deleting anything.
        self.git(root, "branch", "-m", "main", backup)
        self.git(root, "switch", "-c", "main", activation["commit"])

    def replace(self, plan, proposed, attempt):
        target = Path(plan["installed"])
        require(not target.is_symlink(), "symlink service")
        metadata = target.stat()
        require(metadata.st_uid == os.getuid(), "service is not owned by this user")
        domain = f"gui/{os.getuid()}"
        # Atomic rename only after exclusive file creation. Never restore an old
        # stale queue/service automatically on failure; leave paused for Chief.
        temp = target.with_name(target.name + "." + attempt)
        private_write(temp, proposed)
        os.chmod(temp, metadata.st_mode & 0o777)
        require(temp.stat().st_gid == metadata.st_gid, "service group changed")
        self.run(["launchctl", "bootout", domain + "/" + LABEL])
        os.replace(temp, target)
        self.run(["launchctl", "bootstrap", domain, str(target)])
        text = self.loaded().decode()
        loaded_matches(text, proposed)
        return text.encode()

@contextlib.contextmanager
def slot_locks(paths):
    with contextlib.ExitStack() as stack:
        for path in paths:
            require(Path(path).is_file() and not Path(path).is_symlink(), "missing or symlink lock")
            f = stack.enter_context(open(path, "r+"))
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Refused("slot lock held") from None
        yield

def preflight(plan, io, activation=None):
    require(time.time() < plan["deadline"], "deadline expired")
    require(not Path(plan["cancel"]).exists(), "cancelled locally")
    # Re-read cancellation at each boundary, not only during the wait loop.
    if activation:
        require(not any(c.get("body") == f"[Chief] MACBOOK-CANCEL J3892 coordinator={plan['job']} {plan['nonce']}"
                    and c.get("author_association") in {"OWNER", "MEMBER", "COLLABORATOR"}
                    and c.get("user", {}).get("type") == "User" for c in io.comments(plan)), "cancelled on thread")
    require(Path(plan["pause"]).is_file(), "worker pause absent")
    from macbook_cutover_control import owned_pause
    owned_pause(plan, Path(plan["cancel"]).parent)
    require(not Path(plan["marker"]).exists(), "engine marker already exists")
    for path, expected in plan["sources"].items():
        require(digest(Path(path).read_bytes()) == expected, "source hash changed")
    installed = Path(plan["installed"]).read_bytes()
    require(digest(installed) == plan["installed_hash"], "installed service changed")
    require(digest(canonical(loaded_settings(io.loaded().decode()))) == plan["loaded_hash"], "loaded settings changed")
    proposed = proposal(installed, plan["engines"], plan["production_url"])
    require(digest(proposed) == plan["proposal_hash"], "proposal changed")
    drained(plan, io.queue(plan), io.processes(), os.getpid())
    if activation:
        current = validate_activation(io.comment(plan, activation["id"]), plan, plan["plan_hash"], time.time())
        require(current == activation, "activation changed")
        io.production(plan, activation)
    return installed, proposed

def execute(plan, io, activation, attempt_dir, locks=slot_locks):
    attempt_dir = Path(attempt_dir)
    with locks(plan["locks"]):
        installed, proposed = preflight(plan, io, activation)
        private_write(attempt_dir / "installed.plist", installed)
        metadata = Path(plan["installed"]).stat()
        private_write(attempt_dir / "installed-metadata.json", canonical({"mode": metadata.st_mode & 0o777,
                      "uid": metadata.st_uid, "gid": metadata.st_gid}))
        private_write(attempt_dir / "loaded-before.txt", io.loaded())
        private_write(attempt_dir / "proposed.plist", proposed)
        for i, root in enumerate(plan["engines"]):
            io.update_engine(Path(root), plan, activation, "pre-cutover-" + attempt_dir.name + f"-{i}")
        # Recheck job/owner/group/claims, settings, immutable command and exact
        # production ref immediately before the destructive service boundary.
        _, proposed = preflight(plan, io, activation)
        private_write(attempt_dir / "replacement-started", b"paused; do not auto-resume\n")
        loaded = io.replace(plan, proposed, attempt_dir.name)
        private_write(attempt_dir / "loaded-after.txt", loaded)
        marker = {"version": 1, "github": plan["production_repo"]}
        private_write(plan["marker"], canonical(marker))
        # Guard is tested in-process, never by invoking an old worker/queue.
        import engine_guard
        for root in plan["old_engines"]:
            require(str(engine_guard.refusal(root, plan["marker"])).startswith("This engine repository is retired;"), "old engine did not refuse")
        for root in plan["engines"]:
            require(engine_guard.refusal(root, plan["marker"]) is None, "new engine refused")
        require(Path(plan["pause"]).is_file(), "pause disappeared")
        private_write(attempt_dir / "success.json", canonical({"activation": activation, "paused": True}))

def supervise(plan_path, expected):
    from macbook_cutover_control import control_lock
    with control_lock(Path(plan_path).parent):
        return _supervise(plan_path, expected)

def _supervise(plan_path, expected):
    raw = Path(plan_path).read_bytes()
    require(digest(raw) == expected, "plan changed")
    plan = json.loads(raw)
    plan["plan_hash"] = expected
    directory = Path(plan_path).parent
    io = System(plan["deadline"])
    require(os.getsid(0) == os.getpid(), "supervisor must have its own session")
    require(os.getpgrp() not in {o["pgid"] for o in plan["owners"]}, "supervisor shares owner group")
    private_write(directory / "supervisor.json", canonical({"pid": os.getpid(), "pgid": os.getpgrp(),
        "start": next(p["start"] for p in io.processes() if p["pid"] == os.getpid()),
        "result": str(directory / "result.json"), "deadline": plan["deadline"]}))
    try:
        activation = None
        while time.time() < plan["deadline"]:
            require(not (directory / "cancel").exists(), "cancelled locally")
            # Keep identities of detached descendants observed while owners are
            # still alive; group exit alone must not lose a child that called setsid.
            census = io.processes()
            own = next(p for p in census if p["pid"] == os.getpid())
            ignored = {os.getpid()} | {p["pid"] for p in descendants([process_identity(own)], census)}
            observed = descendants(plan["owners"], [p for p in census if p["pid"] not in ignored])
            if observed:
                plan["owners"].extend(observed)
                private_write(directory / ("descendants-" + uuid.uuid4().hex + ".json"), canonical(observed))
            comments = io.comments(plan)
            prefix = f"[Chief] MACBOOK-CUTOVER J3892 coordinator={plan['job']} {plan['nonce']} "
            cancels = [c for c in comments if c.get("body") == f"[Chief] MACBOOK-CANCEL J3892 coordinator={plan['job']} {plan['nonce']}"
                       and c.get("author_association") in {"OWNER", "MEMBER", "COLLABORATOR"}
                       and c.get("user", {}).get("type") == "User"]
            require(not cancels, "cancelled on thread")
            candidates = [c for c in comments if c.get("body", "").startswith(prefix)]
            require(len(candidates) <= 1, "ambiguous activation")
            if candidates:
                current = validate_activation(candidates[0], plan, expected, time.time())
                require(activation is None or activation == current, "activation changed")
                activation = current
                # No service replacement until the coordinator actually exits.
                try:
                    with slot_locks(plan["locks"]):
                        preflight(plan, io, activation)
                except Refused as e:
                    if str(e) not in {"slot lock held", "coordinator is not terminal", "MacBook claim remains",
                                      "owner PID remains or reused", "owner process group remains", "worker or agent child remains", "owner descendant remains"}:
                        raise
                else:
                    attempt = directory / ("attempt-" + uuid.uuid4().hex)
                    attempt.mkdir(mode=0o700)
                    private_write(directory / "activation.json", canonical(activation))
                    from macbook_cutover_control import owned_pause
                    owned_pause(plan, directory)
                    execute(plan, io, activation, attempt)
                    private_write(directory / "result.json", canonical({"status": "installed-paused", "attempt": str(attempt)}))
                    return
            time.sleep(5)
        raise Refused("deadline expired")
    except Exception as e:
        # Never log raw subprocess output, configuration or exception payloads.
        reason = str(e) if isinstance(e, Refused) else type(e).__name__
        private_write(directory / "result.json", canonical({"status": "stopped-paused", "reason": reason}))
        raise Refused(reason) from None

def prepare(config_path, out, io):
    """Read-only machine snapshot; no pause/service/marker changes."""
    config_path = Path(config_path)
    require(not config_path.is_symlink() and config_path.stat().st_mode & 0o077 == 0, "config must be private")
    plan = json.loads(config_path.read_bytes())
    out = Path(out)
    require(out.resolve().is_relative_to((Path.home() / "_desk/state").resolve()), "handoff must be in private state")
    require(not out.is_symlink(), "symlink state directory")
    out.mkdir(mode=0o700)
    require(out.stat().st_mode & 0o077 == 0, "state directory must be private")
    require(plan["job"] != "J3012", "use terminal coordination child, not parent")
    require(plan["engines"] == [str(Path.home() / "_desk/worker/studio"),
                                str(Path.home() / "_desk/worker/slot2/studio")], "wrong engine roots")
    state = Path.home() / "_desk/state"
    require(plan["locks"] == [str(state / "macbook-worker.lock"), str(state / "macbook-worker-2.lock")], "wrong locks")
    require(plan["pause"] == str(state / "macbook-worker.pause")
            and plan["marker"] == str(state / "active-studio.json"), "wrong state paths")
    require(plan["installed"] == str(Path.home() / "Library/LaunchAgents" / (LABEL + ".plist")), "wrong service path")
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", plan["production_repo"]), "invalid repository")
    require(plan["production_url"] == "https://github.com/" + plan["production_repo"] + ".git", "wrong production URL")
    require(plan["issue_url"] == f"https://api.github.com/repos/{plan['authority_repo']}/issues/{plan['thread']}", "wrong authority thread")
    require(len(plan["old_engines"]) == 2 and len(set(plan["old_engines"])) == 2, "two old engines required")
    plan["created"] = time.time()
    require(0 < plan["deadline"] - plan["created"] <= 3600, "invalid deadline")
    plan["nonce"] = uuid.uuid4().hex
    plan["cancel"] = str(out.resolve() / "cancel")
    processes = io.processes()
    plan["owners"] = [process_identity(next(p for p in processes if p["pid"] == pid)) for pid in plan.pop("owner_pids")]
    require(len({o["pid"] for o in plan["owners"]}) >= 2, "record agent and owning worker identities")
    plan["owners"].extend(descendants(plan["owners"], processes))
    installed = Path(plan["installed"]).read_bytes()
    loaded = io.loaded()
    loaded_matches(loaded.decode(), installed)
    # Exact expected hashes are supplied by the reviewed coordinator config;
    # preparation verifies them rather than silently blessing current bytes.
    require(digest(installed) == plan["installed_hash"], "installed hash mismatch")
    require(digest(canonical(loaded_settings(loaded.decode()))) == plan["loaded_hash"], "loaded hash mismatch")
    require(digest(proposal(installed, plan["engines"], plan["production_url"])) == plan["proposal_hash"], "proposal hash mismatch")
    mandatory = {str(Path(__file__).resolve()), str(Path(__file__).resolve().with_name("engine_guard.py")),
                 str(Path(__file__).resolve().with_name("macbook_cutover_control.py")), plan["installed"]}
    mandatory.update({str(Path(render_worker_plist.__file__).resolve()), str(render_worker_plist.TEMPLATE.resolve())})
    mandatory.update(str(Path(root) / "scripts" / name) for root in plan["old_engines"]
                     for name in ("macbook_worker.py", "engine_guard.py"))
    require(mandatory <= set(plan["sources"]), "helper, guards, old workers and installed service must be source-pinned")
    for path, expected in plan["sources"].items():
        require(digest(Path(path).read_bytes()) == expected, "source hash mismatch")
    require(set(plan["production_sources"]) >= {"scripts/macbook_worker.py", "scripts/engine_guard.py"}, "missing production source pins")
    require(all(DIGEST.fullmatch(v) for v in plan["production_sources"].values()), "invalid production source hash")
    for root in plan["engines"]:
        require(not io.git(root, "status", "--porcelain"), "dirty staged engine")
        require(io.git(root, "rev-parse", "HEAD") == plan["staged_heads"][root], "staged head changed")
    private_write(out / "installed-original.plist", installed)
    metadata = {path: {"mode": Path(path).stat().st_mode & 0o777,
                     "uid": Path(path).stat().st_uid, "gid": Path(path).stat().st_gid} for path in plan["sources"]}
    private_write(out / "original-metadata.json", canonical(metadata))
    private_write(out / "loaded-original.txt", loaded)
    # Explicitly list every private bootstrap/wrapper original in sources.
    originals = out / "originals"
    originals.mkdir(mode=0o700)
    for i, path in enumerate(plan["sources"]):
        private_write(originals / str(i), Path(path).read_bytes())
    # Recovery must not depend on a checkout staying on this revision. Bundle
    # the reviewed helpers and their import dependencies privately and pin each.
    bundle = out / "control"
    (bundle / "macbook").mkdir(parents=True, mode=0o700)
    files = {"macbook_cutover.py": Path(__file__).resolve(),
             "macbook_cutover_control.py": Path(__file__).with_name("macbook_cutover_control.py"),
             "engine_guard.py": Path(__file__).with_name("engine_guard.py"),
             "macbook/render_worker_plist.py": Path(render_worker_plist.__file__),
             "macbook/" + render_worker_plist.TEMPLATE.name: render_worker_plist.TEMPLATE}
    plan["control_bundle"] = {}
    for name, source in files.items():
        data = source.read_bytes()
        private_write(bundle / name, data)
        plan["control_bundle"][name] = digest(data)
    raw = canonical(plan)
    private_write(out / "plan.json", raw)
    return digest(raw)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--config", type=Path, required=True)
    prep.add_argument("--out", type=Path, required=True)
    for verb in ("launch", "supervise"):
        p = sub.add_parser(verb)
        p.add_argument("--plan", type=Path, required=True)
        p.add_argument("--sha256", required=True)
    args = ap.parse_args()
    if args.cmd == "prepare":
        print(prepare(args.config, args.out, System()))
        return
    require(DIGEST.fullmatch(args.sha256), "invalid plan digest")
    require(digest(args.plan.read_bytes()) == args.sha256, "plan changed")
    plan = json.loads(args.plan.read_bytes())
    require(0 < plan["deadline"] - time.time() <= 3600, "deadline must be within one hour")
    require(plan["job"].startswith("J") and len(plan["engines"]) == 2
            and len(set(plan["engines"])) == 2 and len(plan["locks"]) == 2, "invalid two-slot plan")
    if args.cmd == "supervise":
        supervise(args.plan, args.sha256)
        return
    directory = args.plan.parent
    require(directory.stat().st_mode & 0o077 == 0 and args.plan.stat().st_mode & 0o077 == 0, "plan must be private")
    require(str(Path(__file__).resolve()) in plan["sources"]
            and digest(Path(__file__).read_bytes()) == plan["sources"][str(Path(__file__).resolve())], "helper changed")
    require(Path(plan["pause"]).is_file(), "authorized coordinator must pause before launch")
    from macbook_cutover_control import arm
    arm(args.plan, args.sha256, dict(plan, plan_hash=args.sha256), System(time.time() + 60))
    private_write(directory / "launched", b"one launch only; fresh plan required for retry\n")
    with open(directory / "supervisor.log", "xb", opener=lambda p, f: os.open(p, f, 0o600)) as log:
        child = subprocess.Popen([sys.executable, str(directory / "control/macbook_cutover.py"), "supervise", "--plan", str(args.plan.resolve()),
            "--sha256", args.sha256], stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True,
            close_fds=True, cwd=directory)
    print(json.dumps({"supervisor_pid": child.pid, "result": str(directory / "result.json")}))

if __name__ == "__main__":
    try:
        main()
    except Refused as error:
        sys.exit(str(error))
