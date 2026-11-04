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
import subprocess
import tempfile

import workflow_state as workflow


def process_identity(pid):
    """Bind PID to OS start time so PID reuse cannot preserve an old lease."""
    if type(pid) is not int or pid <= 0:
        return None
    try:
        result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart=", "-o", "comm="],
                                capture_output=True, text=True, timeout=3)
        return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None
    except (OSError, subprocess.SubprocessError):
        return None


class Registry:
    def __init__(self, root, host, limit, *, probe=process_identity):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", host) or type(limit) is not int or not 1 <= limit <= 8:
            raise ValueError("registered host and bounded configured limit required")
        self.root = pathlib.Path(root)
        self.host, self.limit, self.probe = host, limit, probe

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
            if not isinstance(row, dict) or row.get("host") != self.host:
                raise ValueError("execution registry host mismatch")
            start, end = workflow.timestamp(row.get("startedAt")), workflow.timestamp(row.get("expiresAt"))
            if (start and end and start <= at and row.get("process_identity")
                    and self.probe(row.get("pid")) == row["process_identity"]):
                # A timer is not process-exit proof. A stuck supervisor keeps its
                # slot occupied until it is confirmed dead, even after its cap.
                live.append(dict(row, overdue=at >= end, process_validated=True))
            elif row.get("child_may_exist") is True:
                # A dead supervisor is not proof its child session is dead.
                # Quarantine this slot until explicit process-group cleanup.
                # Never silently turn an orphaned launch into spare capacity.
                live.append(dict(row, process_validated=False, recovery_required=True))
        return live

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
