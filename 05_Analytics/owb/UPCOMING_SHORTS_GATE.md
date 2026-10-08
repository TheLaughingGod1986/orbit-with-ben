# Upcoming Shorts: gate check

Written by `gate_upcoming.py` at 2026-10-08 06:40 London for Shorts scheduled in the next 14 days. Don't edit by hand.

| Airs (London) | Short | In library | Gate |
|---|---|---|---|
| 2026-10-12 11:30 | [Saturn's Rings Are Already Falling](https://youtu.be/Qn56D6TOi0k) `Qn56D6TOi0k` | yes | **FAIL** |
| 2026-10-14 11:30 | [Could a Robot Survive Falling Into Jupiter?](https://youtu.be/buaOI3QGm7U) `buaOI3QGm7U` | yes | **FAIL** |
| 2026-10-16 11:30 | [Why No Black Dwarf Exists Yet](https://youtu.be/1NeQFVnzO2Q) `1NeQFVnzO2Q` | yes | **FAIL** |

## Details

### Qn56D6TOi0k: FAIL

```
Traceback (most recent call last):
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 554, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 465, in main
    results = [check(p.resolve(), air, ns.days, lib, ns.sheet_dir, ns.id, ns.last) for p in ns.files]
               ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 352, in check
    dur = duration_s(path)
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 100, in duration_s
    out = run(
          ~~~^
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ).stdout.decode().strip()
    ^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 96, in run
    return subprocess.run(cmd, check=True, capture_output=True, **kw)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1972, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'
```

### buaOI3QGm7U: FAIL

```
Traceback (most recent call last):
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 554, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 465, in main
    results = [check(p.resolve(), air, ns.days, lib, ns.sheet_dir, ns.id, ns.last) for p in ns.files]
               ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 352, in check
    dur = duration_s(path)
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 100, in duration_s
    out = run(
          ~~~^
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ).stdout.decode().strip()
    ^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 96, in run
    return subprocess.run(cmd, check=True, capture_output=True, **kw)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1972, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'
```

### 1NeQFVnzO2Q: FAIL

```
Traceback (most recent call last):
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 554, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 465, in main
    results = [check(p.resolve(), air, ns.days, lib, ns.sheet_dir, ns.id, ns.last) for p in ns.files]
               ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 352, in check
    dur = duration_s(path)
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 100, in duration_s
    out = run(
          ~~~^
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ).stdout.decode().strip()
    ^
  File "/Users/benjaminoats/_desk/worktrees/analytics/00_Brand/Channel-Setup/tools/gate_shorts_open.py", line 96, in run
    return subprocess.run(cmd, check=True, capture_output=True, **kw)
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/subprocess.py", line 1972, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'
```

