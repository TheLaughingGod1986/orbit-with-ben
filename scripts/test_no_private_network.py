#!/usr/bin/env python3
"""No private-network address in a tracked file. Both repos are public (security pass, 9 Nov 2026).

On 11 Nov 2026 the NAS's home-network address sat in 16 tracked files and in the job queue, the rule book among
them, with the two machines' network names, the phone's and a private-mesh address beside it. All were replaced with
"the NAS", "the Mini", "the MacBook" or a placeholder. This test keeps the addresses out: there is no list of
exceptions, because nothing in the studio needs one written down. The address is on the machines (`mount`,
`tailscale status`) for whoever needs it.

What counts: the three ranges a home or office network uses, and the range a private mesh hands out.
What does not: this machine's own loopback address, public addresses, version numbers with fewer than four parts.

    python3 scripts/test_no_private_network.py            # the test
    python3 scripts/test_no_private_network.py --report   # the files that hold one today (paths only, never the address)

Device names cannot be found by a pattern. AGENTS.md "Never" carries the rule for those.
"""
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PART = "[0-9]{1,3}"
# One pattern for git grep (extended regex) and for Python. The dots are escaped, so this file does not match itself.
RANGES = rf"(192\.168|10\.{PART}|172\.(1[6-9]|2[0-9]|3[01])|100\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7]))"
PATTERN = rf"(^|[^0-9.]){RANGES}\.{PART}\.{PART}([^0-9.]|$)"
ADDRESS = re.compile(PATTERN, re.M)


def files_with_an_address(root: pathlib.Path = ROOT) -> list[str]:
    """Tracked text files under `root` that hold a private-network address. Paths only."""
    done = subprocess.run(["git", "-C", str(root), "grep", "-lIE", PATTERN], capture_output=True, text=True)
    if done.returncode not in (0, 1):  # 1 means no match
        raise RuntimeError(f"git grep failed: {done.stderr.strip()}")
    return sorted(line for line in done.stdout.splitlines() if line)


def address(*parts) -> str:
    """Test addresses are put together here, so none sits in this file."""
    return ".".join(str(p) for p in parts)


class WhatCounts(unittest.TestCase):
    def test_each_private_range_counts(self):
        for parts in ((192, 168, 1, 20), (10, 0, 0, 5), (172, 16, 4, 1), (172, 31, 255, 9), (100, 64, 0, 1), (100, 127, 3, 3)):
            a = address(*parts)
            for text in (a, f"NFS `{a}:/volume1/data` at", f"ssh someone@{a}", f"({a})", f"smb://{a}/shared"):
                self.assertTrue(ADDRESS.search(text), text.replace(a, "<address>"))

    def test_loopback_public_addresses_and_version_numbers_do_not(self):
        for parts in ((127, 0, 0, 1), (0, 0, 0, 0), (8, 8, 8, 8), (172, 15, 0, 1), (172, 32, 0, 1), (100, 63, 0, 1),
                      (100, 128, 0, 1), (192, 169, 1, 1), (1, 192, 168, 1, 1)):
            self.assertFalse(ADDRESS.search("at " + address(*parts) + " now"), parts)
        for text in ("Python 3.10.12", "macOS 10.15", "ffmpeg 7.1", "v10.2.3", "100.5% of the limit", "192.168 is a range"):
            self.assertFalse(ADDRESS.search(text), text)

    def test_only_tracked_files_are_searched(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            git = ["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@example.com"]
            subprocess.run(git + ["init", "-q"], check=True)
            (root / "report.md").write_text("mounted from " + address(192, 168, 1, 20) + ":/volume1/data\n")
            (root / "clean.md").write_text("mounted from the NAS; the browser answers on " + address(127, 0, 0, 1) + "\n")
            (root / "untracked.txt").write_text(address(10, 0, 0, 5) + "\n")
            subprocess.run(git + ["add", "report.md", "clean.md"], check=True)
            self.assertEqual(files_with_an_address(root), ["report.md"])


class TheRepo(unittest.TestCase):
    def test_no_tracked_file_holds_a_private_network_address(self):
        found = files_with_an_address()
        self.assertEqual(found, [], "these tracked files hold a private-network address. Write \"the NAS\", \"the Mini\" "
                         "or \"the MacBook\" instead (AGENTS.md \"Never\"): " + ", ".join(found))

    def test_the_rule_is_in_the_never_list(self):
        never = (ROOT / "AGENTS.md").read_text().split("\n## Never\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("private-network address", never)
        self.assertIn("scripts/test_no_private_network.py", never)


if __name__ == "__main__":
    if "--report" in sys.argv[1:]:
        for path in files_with_an_address():
            print(path)
        sys.exit(0)
    unittest.main()
