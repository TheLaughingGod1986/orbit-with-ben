# J2209 — Shared folder test: MacBook worker side (under launchd)

- **Status:** PASS (`KEEP`)
- **Agent:** `macbook` (run by launchd)
- **Date:** 2026-11-05T10:31Z

## 1. SMB Mount & Directory Listing
```text
mount: /Volumes/shared
//com.apple.idms.appleid.prd.001177-10-2515c37c-d88f-4716-8e99-b49cf6713116@ben-mac-mini/shared on /Volumes/shared (smbfs, nodev, nosuid, mounted by ben)
total 1048592
-rw-r--r--  1 ben  staff  268435456 Nov  5 09:35 from_macbook_20261105T0935Z.bin
-rw-r--r--  1 ben  staff         65 Nov  5 09:35 from_macbook_20261105T0935Z.bin.sha256
-rw-r--r--@ 1 ben  staff  268435456 Nov  5 09:53 from_mini_20261105T0953Z.bin
-rw-r--r--@ 1 ben  staff         65 Nov  5 09:53 from_mini_20261105T0953Z.bin.sha256
```

## 2. Read & SHA-256 Verification of Mini File
- **File:** `/Volumes/shared/_share_test/from_mini_20261105T0953Z.bin` (268,435,456 bytes)
- **Expected SHA-256:** `19e3e573873d6df9e9d42a011015dc9f15999226de203c90a1e7877c13cba8f4`
- **Computed SHA-256:** `19e3e573873d6df9e9d42a011015dc9f15999226de203c90a1e7877c13cba8f4`
- **Result:** `OK /Volumes/shared/_share_test/from_mini_20261105T0953Z.bin read in 23s`

## 3. MacBook Worker Write Test (64 MB)
- **File:** `/Volumes/shared/_share_test/from_macbook_worker_20261105T1030Z.bin` (67,108,864 bytes)
- **SHA-256 file:** `/Volumes/shared/_share_test/from_macbook_worker_20261105T1030Z.bin.sha256`
- **SHA-256:** `98c9958da9154eca0119af17c9f4c9ead56fb231e750c383be24561aa9d41fa0`
- **Write + hash time:** 6s
- **Directory listing after write:**
```text
total 1179672
-rw-r--r--  1 ben  staff  268435456 Nov  5 09:35 from_macbook_20261105T0935Z.bin
-rw-r--r--  1 ben  staff         65 Nov  5 09:35 from_macbook_20261105T0935Z.bin.sha256
-rw-r--r--@ 1 ben  staff   67108864 Nov  5 10:31 from_macbook_worker_20261105T1030Z.bin
-rw-r--r--@ 1 ben  staff         65 Nov  5 10:31 from_macbook_worker_20261105T1030Z.bin.sha256
-rw-r--r--@ 1 ben  staff  268435456 Nov  5 09:53 from_mini_20261105T0953Z.bin
-rw-r--r--@ 1 ben  staff         65 Nov  5 09:53 from_mini_20261105T0953Z.bin.sha256
```
