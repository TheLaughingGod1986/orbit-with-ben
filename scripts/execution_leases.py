"""Bounded local process receipts for capacity dispatch; not a job tracker.

The canonical queue owns reservations/claims. This locked registry only proves
which supervised processes still occupy one registered host. Remote records
must be verified on their own host, never by probing a remote PID locally.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import json
import os
import pathlib
import re
import signal
import subprocess
import tempfile
import time

import workflow_state as workflow


def process_identity(pid):
    """Bind PID to OS start time so PID reuse cannot preserve an old lease."""
    return _process_identity(pid, ["-o", "lstart=", "-o", "comm="])


def child_identity(pid):
    # macOS Python execs its application binary after Popen returns. exec does
    # not create a new process: its birth time is the stable PID identity. The
    # canonical approved argv remains the launcher's responsibility.
    return _process_identity(pid, ["-o", "lstart="])


def _process_identity(pid, fields):
    if type(pid) is not int or pid <= 0:
        return None
    try:
        result = subprocess.run(["ps", "-p", str(pid), *fields],
                                capture_output=True, text=True, timeout=3)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        if result.returncode == 1 and not result.stdout.strip() and not result.stderr.strip():
            return None  # ps positively found no such PID.
        raise RuntimeError("process identity probe failed")
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError("process identity probe unavailable") from error


def group_members(pgid):
    """Observe executing group members; errors are never an empty group.

    Zombies cannot execute work and are excluded. No command arguments or
    environment values are collected. This probe is local-host only.
    """
    if type(pgid) is not int or pgid <= 1:
        raise ValueError("positive child process group required")
    result = subprocess.run(["ps", "-axo", "pid=,pgid=,stat="],
                            capture_output=True, text=True, timeout=3)
    if result.returncode != 0 or result.stderr.strip():
        raise RuntimeError("process group observation unavailable")
    members = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 3 or not parts[0].isdigit() or not parts[1].isdigit():
            raise RuntimeError("malformed process group observation")
        if int(parts[1]) == pgid and not parts[2].startswith("Z"):
            members.append(int(parts[0]))
    if not result.stdout.strip():
        raise RuntimeError("empty process table is not exit evidence")
    return members


class Registry:
    def __init__(self, root, host, limit, *, probe=process_identity, child_probe=child_identity):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", host) or type(limit) is not int or not 1 <= limit <= 8:
            raise ValueError("registered host and bounded configured limit required")
        self.root = pathlib.Path(root)
        self.host, self.limit, self.probe = host, limit, probe
        self.child_probe = child_probe

    @contextlib.contextmanager
    def locked(self):
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / (self.host + ".lock")).open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            path = self.root / (self.host + ".json")
            try:
                # Corrupt/truncated records cannot silently become spare slots.
                rows = json.loads(path.read_text()) if path.exists() else []
                if not isinstance(rows, list) or len(rows) > 8:
                    raise ValueError("invalid execution registry")
                yield rows
                fd, temporary = tempfile.mkstemp(prefix=self.host + "-", dir=self.root)
                try:
                    with os.fdopen(fd, "w") as out:
                        json.dump(rows, out, allow_nan=False)
                        out.flush()
                        os.fsync(out.fileno())
                    os.replace(temporary, path)
                finally:
                    pathlib.Path(temporary).unlink(missing_ok=True)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def _live(self, rows, at):
        live = []
        for row in rows:
            end = self._validate_row(row, at)
            if self.probe(row["pid"]) == row["process_identity"]:
                # A timer is not process-exit proof. A stuck supervisor keeps its
                # slot occupied until it is confirmed dead, even after its cap.
                live.append(dict(row, overdue=at >= end, process_validated=True))
            elif row.get("child_may_exist") is True:
                # A dead supervisor is not proof its child session is dead.
                # Quarantine this slot until explicit process-group cleanup.
                # Never silently turn an orphaned launch into spare capacity.
                live.append(dict(row, process_validated=False, recovery_required=True))
        return live

    def _validate_row(self, row, at):
        if not isinstance(row, dict) or row.get("host") != self.host:
            raise ValueError("execution registry host mismatch")
        start, end = workflow.timestamp(row.get("startedAt")), workflow.timestamp(row.get("expiresAt"))
        if (not start or not end or not start <= at or not end > start
                or type(row.get("pid")) is not int or row["pid"] <= 0
                or any(not isinstance(row.get(k), str) or not row[k]
                       for k in ("token", "job", "worker", "account", "process_identity"))):
            raise ValueError("malformed execution registry is not spare capacity")
        return end

    def observe(self, at):
        with self.locked() as rows:
            live = self._live(rows, at)
            # Only confirmed dead, unarmed records go. Possible orphan sessions
            # remain quarantined; canonical queue claims are always untouched.
            rows[:] = live
            return [dict(row, at=at.isoformat()) for row in live]

    def arm(self, token, pid):
        """Persist possible-child state BEFORE spawn; crashes quarantine capacity."""
        with self.locked() as rows:
            row = next((r for r in rows if r.get("token") == token), None)
            if (not row or row.get("pid") != pid
                    or self.probe(pid) != row.get("process_identity")):
                raise ValueError("only the live recorded supervisor may arm a launch")
            row["child_may_exist"] = True

    def attach(self, token, pid, child_pid):
        """Bind the spawned session leader before allowing orphan recovery.

        A crash between arm/spawn/attach remains quarantined. Never guess a
        child PID from its command, age, log or another host's process table.
        """
        identity = self.child_probe(child_pid)
        if not identity or os.getpgid(child_pid) != child_pid or child_pid == pid:
            raise ValueError("validated independent child group required")
        with self.locked() as rows:
            row = next((r for r in rows if r.get("token") == token), None)
            if (not row or row.get("pid") != pid or not row.get("child_may_exist")
                    or self.probe(pid) != row.get("process_identity") or row.get("child_pid")):
                raise ValueError("only the armed supervisor may attach one child")
            row.update(child_pid=child_pid, child_identity=identity)

    def reconcile(self, at, *, members=group_members, kill_group=os.killpg,
                  timeout=2, monotonic=time.monotonic, pause=time.sleep):
        """Recover confirmed orphan groups without releasing canonical claims.

        Only a dead/reused supervisor and the exact recorded live child leader
        authorize a kill. A missing/reused leader with surviving descendants,
        an unrecorded spawn or failed probe stays quarantined. Release requires
        a successful empty-group observation AFTER cleanup. No automatic retry
        or queue completion follows; durable launch seals remain untouched.
        """
        if not isinstance(timeout, (int, float)) or not 0 < timeout <= 5:
            raise ValueError("bounded recovery timeout required")
        results = []
        with self.locked() as rows:
            retained = []
            for row in rows:
                self._validate_row(row, at)
                result = dict(token=row.get("token"), job=row.get("job"), phase="quarantined")
                try:
                    if self.probe(row.get("pid")) == row.get("process_identity") and row.get("process_identity"):
                        retained.append(row)
                        continue  # Including overdue supervisors: timer is not exit proof.
                    if not row.get("child_may_exist"):
                        result["phase"] = "dead_supervisor_recovered"
                    else:
                        child_pid = row.get("child_pid")
                        if not child_pid or not row.get("child_identity"):
                            raise ValueError("unrecorded child requires explicit investigation")
                        current = members(child_pid)
                        if current:
                            if (child_pid not in current
                                    or self.child_probe(child_pid) != row["child_identity"]):
                                raise ValueError("child group identity cannot be established")
                            # Recheck supervisor just before signalling; a probe
                            # error or unexpected identity keeps the slot closed.
                            if self.probe(row.get("pid")) == row.get("process_identity"):
                                raise ValueError("supervisor became live during recovery")
                            kill_group(child_pid, signal.SIGKILL)
                            until = monotonic() + timeout
                            while members(child_pid):
                                if monotonic() >= until:
                                    raise ValueError("child group cleanup not confirmed")
                                pause(0.02)
                        result["phase"] = "orphan_recovered"
                except (OSError, subprocess.SubprocessError, RuntimeError, ValueError):
                    # Deliberately omit OS error/command details from reports.
                    retained.append(dict(row, recovery_required=True, process_validated=False))
                results.append(result)
            rows[:] = retained
        return results

    def record(self, reservation, pid, at, cap_seconds, *, exclusive=False):
        if (reservation.get("host") != self.host or reservation.get("phase") != "reserved"
                or not reservation.get("token") or not reservation.get("job")
                or not reservation.get("worker") or not reservation.get("account")
                or type(cap_seconds) is not int or not 1 <= cap_seconds <= 1500):
            raise ValueError("matching reservation and bounded supervisor required")
        start, end = workflow.timestamp(reservation.get("at")), workflow.timestamp(reservation.get("expiresAt"))
        if not start or not end or not start <= at < end:
            raise ValueError("reservation expired before launch")
        identity = self.probe(pid)
        if not identity:
            raise ValueError("supervisor process cannot be validated")
        with self.locked() as rows:
            live = self._live(rows, at)
            same = next((r for r in live if r.get("token") == reservation["token"]), None)
            if same:
                if exclusive:
                    raise ValueError("reservation already has a supervisor")
                if same.get("pid") != pid or same.get("process_identity") != identity:
                    raise ValueError("reservation already launched by another process")
                return dict(same)
            if len(live) >= self.limit or any(r.get("job") == reservation["job"] for r in live):
                raise ValueError("host capacity or job already occupied")
            row = dict(reservation, pid=pid, process_identity=identity, phase="starting",
                       startedAt=at.isoformat(), expiresAt=(at + dt.timedelta(seconds=cap_seconds)).isoformat())
            rows[:] = [*live, row]
            return dict(row)

    def finish(self, token, pid):
        with self.locked() as rows:
            match = next((r for r in rows if r.get("token") == token), None)
            if not match:
                return False
            if match.get("pid") != pid:
                raise ValueError("only the recorded supervisor may finish its lease")
            rows.remove(match)
            return True

    def resolve_quarantine(self, token, *, at, approved_by, approval_ref, reason,
                           members=group_members):
        """Explicit Chief/operator clearance for a quarantined unknown-orphan slot.

        Requires a dead supervisor, verified empty child group (if child_pid was
        recorded), and writes an immutable audit receipt without touching the
        durable launch seal so the old token can still never be replayed.
        """
        import hashlib
        if any(not isinstance(v, str) or not v.strip()
               for v in (token, approved_by, approval_ref, reason)):
            raise ValueError("quarantine resolution requires token, approved_by, approval_ref and reason")
        with self.locked() as rows:
            match = next((r for r in rows if r.get("token") == token), None)
            if not match:
                raise ValueError("no matching execution lease to resolve")
            self._validate_row(match, at)
            if self.probe(match["pid"]) == match["process_identity"]:
                raise ValueError("live supervisor cannot be cleared as a quarantined orphan")
            if not match.get("child_may_exist") and not match.get("recovery_required"):
                raise ValueError("unarmed dead supervisor recovers automatically via observe/reconcile")
            child_pid = match.get("child_pid")
            if child_pid is not None:
                if members(child_pid):
                    raise ValueError("recorded child group still has executing members")
            audit_dir = self.root / (self.host + "-quarantine-resolutions")
            audit_dir.mkdir(exist_ok=True)
            key = hashlib.sha256(token.encode()).hexdigest()
            audit_path = audit_dir / (key + ".json")
            receipt = dict(
                version=1,
                host=self.host,
                job=match["job"],
                token=token,
                worker=match["worker"],
                account=match["account"],
                approved_by=approved_by.strip(),
                approval_ref=approval_ref.strip(),
                reason=reason.strip(),
                at=at.isoformat(),
            )
            with audit_path.open("x") as out:
                json.dump(receipt, out, allow_nan=False)
                out.flush()
                os.fsync(out.fileno())
            rows.remove(match)
            return receipt
