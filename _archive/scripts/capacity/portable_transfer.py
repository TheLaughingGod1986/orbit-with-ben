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


def _bundle_regular_paths(root):
    base = pathlib.Path(root)
    if base.is_symlink() or not base.is_dir():
        raise ValueError("bundle root must be a local directory")
    paths = []
    for current, dirs, files in os.walk(base, followlinks=False):
        current_path = pathlib.Path(current)
        for d in dirs:
            if (current_path / d).is_symlink():
                raise ValueError("symlink directory in portable bundle")
        for f in files:
            candidate = current_path / f
            if candidate.is_symlink() or not candidate.is_file():
                raise ValueError("nonregular file in portable bundle")
            paths.append(candidate.relative_to(base).as_posix())
    return sorted(paths)


def stage_outbound(job_doc, *, reservation, host, source_root, staging_parent,
                   at, max_bytes, max_files):
    """Stage approved inputs into a unique outbound bundle and emit an input receipt."""
    import dispatch_capacity as capacity
    contract = (job_doc or {}).get("portable") or {}
    probe_host = dict(
        input_receipts={
            row.get("path", ""): dict(
                sha256=row.get("sha256", ""),
                readable=True,
                at=at.isoformat(),
                expiresAt=(at + dt.timedelta(minutes=5)).isoformat(),
            )
            for row in (contract.get("inputs") or [])
            if isinstance(row, dict)
        }
    )
    problem = capacity.portable_problem(job_doc, probe_host, at)
    if problem:
        raise ValueError("invalid portable contract: " + problem)
    bundle = copy_verified(contract["inputs"], source_root, staging_parent,
                           max_bytes=max_bytes, max_files=max_files)
    try:
        receipt = make_receipt(contract, contract["inputs"], bundle,
                               job=job_doc["id"], reservation=reservation,
                               host=host, direction="input", at=at, max_bytes=max_bytes)
        return bundle, receipt
    except BaseException:
        shutil.rmtree(bundle)
        raise


def input_receipts_map(receipt, contract, bundle_root, *, job, reservation, host, at, max_bytes):
    """Verify inbound bundle on the consuming host and produce host['input_receipts']."""
    checked = verify_receipt(receipt, contract, bundle_root, job=job,
                             reservation=reservation, host=host, direction="input",
                             at=at, max_bytes=max_bytes)
    return {
        row["path"]: dict(
            sha256=row["sha256"],
            readable=True,
            at=checked["at"],
            expiresAt=checked["expiresAt"],
        )
        for row in checked["files"]
    }


def preflight_inbound(job_doc, *, reservation, host, bundle_root, receipt, at, max_bytes):
    """Consuming-host preflight immediately before supervised execution."""
    contract = (job_doc or {}).get("portable") or {}
    actual = _bundle_regular_paths(bundle_root)
    expected = sorted(row["path"] for row in manifest(contract.get("inputs") or []))
    if actual != expected:
        raise ValueError("inbound bundle files differ from approved input manifest")
    return verify_receipt(receipt, contract, bundle_root, job=job_doc["id"],
                          reservation=reservation, host=host, direction="input",
                          at=at, max_bytes=max_bytes)


def stage_return(job_doc, *, reservation, host, work_root, return_parent,
                 at, max_bytes, max_files):
    """Hash scoped output paths on the worker host and copy into a clean return bundle."""
    contract = (job_doc or {}).get("portable") or {}
    outputs = contract.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ValueError("explicit portable output paths required")
    manifest([{"path": name, "sha256": "0" * 64} for name in outputs])
    rows = []
    total = 0
    for name in sorted(outputs):
        digest = hashlib.sha256()
        with open_regular(work_root, name) as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("return output byte budget exceeded")
                digest.update(chunk)
        rows.append({"path": name, "sha256": digest.hexdigest()})
    bundle = copy_verified(rows, work_root, return_parent,
                           max_bytes=max_bytes, max_files=max_files)
    try:
        receipt = make_receipt(contract, rows, bundle, job=job_doc["id"],
                               reservation=reservation, host=host, direction="output",
                               at=at, max_bytes=max_bytes)
        return bundle, receipt
    except BaseException:
        shutil.rmtree(bundle)
        raise


def consume_return(job_doc, *, reservation, host, return_bundle, receipt,
                   review_parent, at, max_bytes, max_files):
    """Verify returned outputs on Mini into an isolated review bundle without auto-approval."""
    contract = (job_doc or {}).get("portable") or {}
    outputs = contract.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ValueError("explicit portable output paths required")
    actual = _bundle_regular_paths(return_bundle)
    if actual != sorted(outputs):
        raise ValueError("return bundle contains unexpected or missing files")
    checked = verify_receipt(receipt, contract, return_bundle, job=job_doc["id"],
                             reservation=reservation, host=host, direction="output",
                             at=at, max_bytes=max_bytes)
    staged = copy_verified(checked["files"], return_bundle, review_parent,
                           max_bytes=max_bytes, max_files=max_files)
    return dict(
        job=job_doc["id"],
        reservation=reservation,
        host=host,
        review_bundle=str(staged),
        receipt=checked,
        stage_approved=False,
        keep_approved=False,
        job_completed=False,
    )
