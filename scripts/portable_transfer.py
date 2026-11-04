"""Bounded local transport adapter for approved portable jobs.

No network, launch, queue mutation or approval is performed here. The caller
provides already mounted/readable roots; unsupported remote paths fail closed.
Bundles are new directories: existing approved or uploaded bytes are never
overwritten. Dispatch remains disconnected until canonical reservations exist.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import tempfile

import workflow_state as workflow


def manifest(items):
    if not isinstance(items, list):
        raise ValueError("explicit file manifest required")
    seen = set()
    result = []
    for row in items:
        if not isinstance(row, dict):
            raise ValueError("malformed file manifest")
        name = row.get("path")
        path = pathlib.PurePosixPath(name) if isinstance(name, str) else None
        if (not name or not path or path.is_absolute() or ".." in path.parts
                or "\\" in name or str(path) != name or name in {".", ""}
                or name in seen or not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", ""))):
            raise ValueError("invalid or duplicate manifest path/hash")
        seen.add(name)
        result.append({"path": name, "sha256": row["sha256"]})
    # A file cannot also be a directory containing another approved file.
    for name in seen:
        if any(str(parent) in seen for parent in pathlib.PurePosixPath(name).parents):
            raise ValueError("manifest file/directory collision")
    return sorted(result, key=lambda row: row["path"])


def contract_digest(contract):
    return hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def open_regular(root, name):
    """Open each component without following symlinks, including the root."""
    flags = os.O_RDONLY | os.O_NOFOLLOW
    directory = os.open(root, flags | os.O_DIRECTORY)
    try:
        parts = pathlib.PurePosixPath(name).parts
        for part in parts[:-1]:
            child = os.open(part, flags | os.O_DIRECTORY, dir_fd=directory)
            os.close(directory)
            directory = child
        fd = os.open(parts[-1], flags | os.O_NONBLOCK, dir_fd=directory)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            raise ValueError("manifest input is not a regular file")
        return os.fdopen(fd, "rb")
    finally:
        os.close(directory)


def copy_verified(items, source_root, destination_parent, *, max_bytes, max_files):
    """Copy into a unique bundle; rehash destination and clean only our bundle.

    File/byte budgets are mandatory, shared across the whole copy. The result
    is a local path, not proof that another host can read it. Each consumer
    verifies its own bytes with verify_receipt before execution or review.
    """
    rows = manifest(items)
    if (type(max_bytes) is not int or max_bytes < 0 or type(max_files) is not int
            or max_files < 0 or len(rows) > max_files):
        raise ValueError("invalid or exceeded transfer budget")
    parent = pathlib.Path(destination_parent)
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError("destination must be an existing local directory")
    bundle = pathlib.Path(tempfile.mkdtemp(prefix="portable-", dir=parent))
    total = 0
    try:
        for row in rows:
            target = bundle / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256()
            with open_regular(source_root, row["path"]) as source, target.open("xb") as output:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    total += len(chunk)
                    if total > max_bytes:
                        raise ValueError("transfer byte budget exceeded")
                    digest.update(chunk)
                    output.write(chunk)
            if digest.hexdigest() != row["sha256"]:
                raise ValueError("source hash mismatch: " + row["path"])
        verify_files(rows, bundle, max_bytes=max_bytes)
        return bundle
    except BaseException:
        shutil.rmtree(bundle)  # only the unique directory created by this call
        raise


def verify_files(items, root, *, max_bytes):
    if type(max_bytes) is not int or max_bytes < 0:
        raise ValueError("byte budget required")
    total = 0
    for row in manifest(items):
        digest = hashlib.sha256()
        with open_regular(root, row["path"]) as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("verification byte budget exceeded")
                digest.update(chunk)
        if digest.hexdigest() != row["sha256"]:
            raise ValueError("local hash mismatch: " + row["path"])
    return total


def make_receipt(contract, items, root, *, job, reservation, host, direction, at, max_bytes):
    if direction not in {"input", "output"} or not all((job, reservation, host)):
        raise ValueError("receipt needs job, reservation, host and direction")
    rows = manifest(items)
    if direction == "input" and rows != manifest(contract.get("inputs")):
        raise ValueError("input receipt differs from approved contract")
    if direction == "output":
        expected = contract.get("outputs")
        if (not isinstance(expected, list) or len(expected) != len(set(expected))
                or sorted(expected) != [row["path"] for row in rows]):
            raise ValueError("output receipt differs from scoped output paths")
    count = verify_files(rows, root, max_bytes=max_bytes)
    return dict(version=1, job=job, reservation=reservation, host=host, direction=direction,
                contract_sha256=contract_digest(contract), files=rows, bytes=count,
                at=at.isoformat(), expiresAt=(at + dt.timedelta(minutes=5)).isoformat())


def verify_receipt(receipt, contract, root, *, job, reservation, host, direction, at, max_bytes):
    """Rehash on the receiving host; a receipt alone never approves any stage."""
    stamp = workflow.timestamp(receipt.get("at"))
    end = workflow.timestamp(receipt.get("expiresAt"))
    if (receipt.get("version") != 1 or not stamp or not end or not stamp <= at < end
            or (at - stamp).total_seconds() > 300
            or any(receipt.get(k) != v for k, v in dict(job=job, reservation=reservation,
                       host=host, direction=direction, contract_sha256=contract_digest(contract)).items())):
        raise ValueError("receipt stale or identity/contract mismatch")
    checked = make_receipt(contract, receipt.get("files"), root, job=job, reservation=reservation,
                           host=host, direction=direction, at=at, max_bytes=max_bytes)
    if checked["bytes"] != receipt.get("bytes"):
        raise ValueError("receipt byte count mismatch")
    return checked
