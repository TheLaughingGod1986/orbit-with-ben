# J2215 — Shared folder re-check after lock-down: MacBook worker reads/writes /Volumes/shared

- **Status:** BLOCKED (`smbfs` share `/Volumes/shared` is not mounted on the MacBook)
- **Agent:** `macbook` (run by launchd)
- **Date:** 2026-11-05T12:45Z

## 1. Command Output
Running the exact command from the J2215 brief:
```sh
M=$(mount | awk '/smbfs/ && /ben-mac-mini/ {for(i=1;i<=NF;i++) if($i=="on"){print $(i+1); exit}}'); echo $M; f="$M/.rw_check_$(date +%s)"; echo ok > "$f" && cat "$f" && rm "$f" && echo PASS
```
Output (exit code `1`):
```text
M=
f=/.rw_check_1793882706
zsh:1: read-only file system: /.rw_check_1793882706
```

## 2. Mount & Network Diagnostics
- `mount` shows **no `smbfs` mounts** on the MacBook (only APFS system volumes, `192.168.1.119:/volume1/data on /Volumes/data (nfs)`, and `OrbStack`).
- `ls -la /Volumes` (`Nov 5 10:47`):
  ```text
  total 1
  drwxr-xr-x   5 root  wheel        160 Nov  5 10:47 .
  drwxr-xr-x  23 root  wheel        736 Sep 24 08:10 ..
  lrwxr-xr-x   1 root  wheel          1 Oct  6 00:40 Macintosh HD -> /
  drwxr-xr-x@  4 root  wheel        128 Nov  3 00:40 Recovery
  drwxrwxr-x   1 1027  _lpoperator  182 Oct 14 16:27 data
  ```
- `ben-mac-mini` (`100.96.7.11`) is reachable (`0.0% packet loss`, `smbutil status ben-mac-mini` -> `Server: MAC-7993A6`), so turning off guest access / reconfiguring File Sharing on the Mini at ~10:47 UTC dropped the MacBook's active SMB mount (`/Volumes/shared`).
- Per MacBook worker rules (*"never sign in to anything"*), the unattended worker did not attempt to mount or authenticate `smb://ben-mac-mini/shared`. Remount `smb://ben-mac-mini/shared` in Finder on the MacBook, then re-run `J2215`.
