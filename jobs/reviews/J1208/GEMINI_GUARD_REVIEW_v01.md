Gemini Argon via agy, 4 November 2026. Advisory review of initial draft; findings retained verbatim. The revised implementation and Chief disposition are separate.

### Review Verdict

* **Generation Approval:** **NEVER APPROVED.** This review does not authorize any live API call, Vertex/Veo request, or spend.
* **No-Spend Prototype Integration:** `promo_guard.py` contains no network imports, credentials, or generation entry points, so importing and running its unit tests in isolation cannot incur spend. However, **it is NOT safe to rely on its accounting or state-machine logic as written**—even in a prototype harness—until the concrete bugs below are fixed.

---

### 1. Accounting Safety Bugs

#### Bug 1.1: Spend disappears between `credits["at"]` and `usage["pending_since"]` (Double-Omission Window)
* **Location:** `assess()` (`cutoff = stamp(e["usage"]["pending_since"])` vs `e["credits"]["at"]`)
* **Failure mode:** `assess()` checks that `credits["at"]` and `usage["at"]` are each $\le 300\text{s}$ old, and that `cutoff <= usage["at"]`, but **never checks `cutoff <= stamp(e["credits"]["at"])`**.
  * Suppose `credits` is read at `00:00:00` (`remaining_gbp = 2.76`), a spend of `£0.88` occurs and is reconciled at `00:01:00`, and `usage` is read at `00:02:00` with `pending_since = 00:02:00`.
  * At `00:02:00`, both `credits` and `usage` are within the 300s freshness window.
  * Because `rid in reconciled`, the reservation is removed from `pending`. Because `stamp(r["at"]) < cutoff` (`00:01:00 < 00:02:00`), the `spend` row is **also** excluded from `pending`. And because `credits` was read at `00:00:00`, the spend is **not** deducted from `available` either. The `£0.88` spend vanishes from both sides of the equation.
* **Fix:**
  1. Require `cutoff <= stamp(e["credits"]["at"])` (a usage cutoff cannot be newer than the credit balance snapshot it reconciles against).
  2. For J1208 reservations reconciled with `amount=None` (conservative estimate for an unknown failure) or until billing balance demonstrably reflects the deduction, do not drop reconciled J1208 spend solely because `r["at"] < cutoff` unless `cutoff` is strictly after the spend settled in billing **and** `credits["at"] >= cutoff`.

#### Bug 1.2: `reconcile()` accepts `amount = 0` (or `0.00`), releasing reserved budget
* **Location:** `reconcile()` (`value = money(r["amount"] if amount is None else amount)`) and `money()` (`if not d.is_finite() or d < 0:`)
* **Failure mode:** `money(0)` returns `Decimal("0")`. If a caller passes `amount=0` (e.g., on an error or unpriced response), `reconcile()` writes a `spend` row with `amount: 0.0` and `what: "J1208 verified cost"`, marking `reservation_id` as reconciled. In `assess()`, this removes the `£0.88` reservation from `pending` and replaces it with `£0.00`, violating *"A reservation consumes its take even if the process crashes or call fails"*.
* **Fix:** In `reconcile()`, require `value > 0` (or `if amount is not None and money(amount) <= 0: raise Stop("verified spend must be positive; pass None to retain full bound")`).

#### Bug 1.3: Zero-amount / unpriced spend rows without the literal word `"unpriced"` pass as `£0`
* **Location:** `assess()`:
  ```python
  if amount == 0 and "unpriced" in r.get("what", "").lower():
      raise Stop("unpriced pending spend requires upper bound")
  ```
* **Failure mode:** Any `kind == "spend"` row on pool `"vertex"` with `amount == 0` whose `what` field says `"unknown"`, `"pending"`, `"TBD"`, or `""` instead of containing `"unpriced"` is silently treated as `£0.00` spend, violating *"Unknown historic spend blocks rather than becoming zero."*
* **Fix:** Fail closed on **any** zero-amount `spend` row in the `vertex` pool (`if amount <= 0: raise Stop("zero or unpriced spend row requires positive upper bound")`), and check this regardless of whether `stamp(r["at"]) >= cutoff` if `rid` is set.

#### Bug 1.4: Unknown `kind` values and direct J1208 `spend` rows are ignored
* **Location:** `assess()` loop over `rows`
* **Failure mode:**
  1. Any ledger row with `pool == "vertex"` and `kind not in ("reserve", "spend")` (including legacy rows where `kind` is omitted/null) is silently skipped (`continue` / falls through `if/elif`).
  2. `seen_takes` and `committed` are only populated inside `if kind == "reserve":`. A direct `kind == "spend"` row with `job == "J1208"` (and no `reservation_id`) is neither counted toward `seen_takes` nor added to `committed`, allowing the `£4` J1208 scope cap and 2-take cap to be bypassed.
* **Fix:**
  1. Raise `Stop(f"unknown vertex ledger row kind: {kind!r}")` in an `else:` branch.
  2. Reject any `kind == "spend"` row with `job == "J1208"` or `film == "OWB:030"` that lacks a valid `J1208:<take>` `reservation_id`.
  3. In `if kind == "reserve"` for `job == "J1208"`, enforce `rid == f"J1208:{r['take']}"`.

#### Bug 1.5: `reserve()` returns stale pre-reservation budget state
* **Location:** `reserve()` returns `result` computed *before* writing the new reservation rows.
* **Failure mode:** After `reserve()` writes two `£0.88` reservations to `ledger`, its return dict still reports the old `pending_gbp` (e.g. `'0'`), the old `remaining_takes` (`['s5', 's6']`), and the old `ledger_sha256` from before the append.
* **Fix:** Either re-run `assess(evidence_with_new_sha, updated_rows, now)` or explicitly return both `reserved_takes` (the takes just written) and the post-write `pending_gbp` / `ledger_sha256`.

---

### 2. Crash / Restart & Idempotency Bugs

#### Bug 2.1: Upfront batch reservation of `s5` and `s6` + silent no-op on re-call breaks crash/restart semantics
* **Location:** `reserve()` and `assess()` (`remaining_takes`)
* **Failure mode:** `reserve()` writes `kind: "reserve"` rows for **both** `s5` and `s6` in one call. Because `assess()` populates `seen_takes` from `kind == "reserve"` rows:
  1. **Silent no-op on duplicate `reserve()`:** When `seen_takes == {"s5", "s6"}`, calling `reserve()` again does **not** raise `Stop`; it succeeds with `remaining == 0` and writes 0 rows (`test_promo_guard.py` line 75 explicitly tests this behavior). Any caller that treats a non-raising `reserve()` call as "lock and reservation acquired, proceed" will **re-run takes after a crash and double-spend**.
  2. **Cannot resume `s6` after a crash during/after `s5`:** Because `J1208:s6` is already written as `kind: "reserve"` before `s5` even starts, a process that finishes `s5` and crashes before `s6` restarts to find `seen_takes == {"s5", "s6"}` and `remaining_takes == []`. There is no ledger state distinguishing *"budget reserved for `s6`, take not yet attempted"* from *"take `s6` started and crashed mid-flight"*.
* **Fix:**
  * Separate **scope budget reservation** from **per-take consumption** (or reserve one take at a time while `assess()` still enforces that `available - pending` covers the full remaining 2-take scope), **and**
  * Make `reserve()` raise `Stop("nothing left to reserve")` whenever `result["remaining_takes"]` is empty instead of returning silently.

#### Bug 2.2: Partial/truncated trailing line on crash corrupts subsequent appends
* **Location:** `reserve()` and `reconcile()` (`with ledger.open("a+") as f:`)
* **Failure mode:**
  1. If a previous crash or disk-full error left a non-newline-terminated or truncated line at EOF, `[json.loads(x) for x in f if x.strip()]` raises an uncaught `json.JSONDecodeError` (not `Stop`).
  2. If the last line of `ledger.jsonl` is valid JSON but lacks a trailing `\n`, `f.write(json.dumps(row) + "\n")` in `"a+"` mode appends on the same line, corrupting both records.
  3. Write both reserve lines in a single `f.write("".join(...))` call rather than a loop of `f.write()` calls, and verify the file ends with `\n` (when non-empty) before appending.

---

### 3. Concurrency & Locking Bugs

#### Bug 3.1: `DESK_LOCK_HELD_DIR` check is spoofable and does not verify lock ownership or liveliness
* **Location:** `reserve()`:
  ```python
  held = Path(os.environ.get("DESK_LOCK_HELD_DIR", "/nonexistent"))
  if held.name != "vertex.lock" or not (held / "owner.txt").is_file():
      raise Stop("existing vertex desk-lock required")
  ```
* **Failure mode:**
  1. Any directory named `vertex.lock` containing an empty `owner.txt` (e.g. `/tmp/vertex.lock/owner.txt`, as in `test_missing_lock_and_changed_ledger`) satisfies the check.
  2. It never reads `owner.txt` to verify that the current process (or parent PID) actually owns the lock, nor whether the recorded PID is alive. If a stale `vertex.lock` is left on disk or held by *another* process while `DESK_LOCK_HELD_DIR` is set in the environment, `reserve()` proceeds concurrently.
* **Fix:** Validate `held.resolve()` against the canonical studio lock directory (or pass the expected lock root explicitly), parse `pid=<int>` from `owner.txt`, and verify it matches `os.getpid()` or `os.getppid()`.

#### Bug 3.2: `digest(rows)` hashes re-serialized JSON objects, not file bytes, and `amount` uses `float()`
* **Location:** `digest()`, `reserve()`, `reconcile()`
* **Failure mode:**
  1. `reserve()` and `reconcile()` convert `Decimal` back to `float(...)` (`"amount": float(result["per_take_gbp"])`), reintroducing binary floating-point representation in JSON.
  2. `digest(rows)` computes `sha256(json.dumps(rows, sort_keys=True))`. If an external audit tool computes standard `sha256` over `ledger.jsonl` bytes, it will never match `ledger_sha256`.
  3. `ledger.open("a+")` silently creates a new file if `ledger` does not exist; if `evidence["ledger_sha256"] == digest([])`, `reserve()` will create a new file at a typo path instead of raising `Stop("ledger file missing")`.
* **Fix:** Store `amount` via `Decimal` or exact string/number formatting, check `if not ledger.is_file(): raise Stop("ledger missing")` before opening, and document or align `digest()` with canonical byte hashing.

---

### 4. Input Validation & Test Suite Gaps

* **Uncaught `KeyError` / `TypeError` on malformed evidence or ledger rows:** `assess()` directly indexes `e[key]["at"]`, `e["credits"]["rows"]`, `e["duration"][subject]`, `r["reservation_id"]`, `r["amount"]`, and `r["at"]`. Missing keys or `None` sections raise raw `KeyError`/`TypeError` instead of `Stop`. Wrap schema lookups or catch `(KeyError, TypeError)` and raise `Stop`.
* **Missing tests in `test_promo_guard.py`:**
  1. Test `credits["at"] < spend["at"] < usage["pending_since"]` (currently passes and loses the spend).
  2. Test `reconcile(ledger, "J1208:s5", 0, NOW)` (currently passes and erases the reservation).
  3. Test `spend` row with `amount: 0` and `what: "unknown"` (currently passes as `£0` spend).
  4. Test crash recovery between `s5` and `s6` (currently leaves `remaining_takes == []`).
  5. Test `owner.txt` PID ownership mismatch.
