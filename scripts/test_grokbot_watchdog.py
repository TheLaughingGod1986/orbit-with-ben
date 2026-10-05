"""Drives scripts/mini/grokbot_watchdog.sh with stub commands (no real app, lsof or osascript)."""
import os, pathlib, subprocess, tempfile, textwrap, unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "mini" / "grokbot_watchdog.sh"
LSOF_UP = "COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\nGrok 1 b 1u IPv4 0 0t0 TCP 192.168.1.5:50000->34.1.2.3:443 (ESTABLISHED)\n"
LSOF_LOCAL = "COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\nGrok 1 b 1u IPv4 0 0t0 TCP 127.0.0.1:50000->127.0.0.1:9000 (ESTABLISHED)\n"


class Watchdog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = pathlib.Path(self.tmp.name)
        self.calls = self.d / "calls.txt"
        self.calls.write_text("")
        (self.d / "locks").mkdir()
        self.now = 1_760_000_000
        self.pids = "965\n977\n"
        self.lsof = ""

    def tearDown(self):
        self.tmp.cleanup()

    def stub(self, name, body):
        p = self.d / name
        p.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        p.chmod(0o755)
        return str(p)

    def run_once(self, mode="enforce", **env):
        (self.d / "pids.txt").write_text(self.pids)
        (self.d / "lsof.txt").write_text(self.lsof)
        rec = f'echo "$(basename $0) $*" >> {self.calls}\n'
        e = dict(os.environ,
                 GROKBOT_MODE=mode,
                 GROKBOT_NOW=str(self.now),
                 GROKBOT_STATE_DIR=str(self.d / "state"),
                 GROKBOT_LOG=str(self.d / "watchdog.log"),
                 GROKBOT_SUPPORT_DIR=str(self.d / "support"),
                 DESK_LOCK_ROOT=str(self.d / "locks"),
                 GROKBOT_PGREP=self.stub("pgrep", f"cat {self.d}/pids.txt\n"),
                 GROKBOT_LSOF=self.stub("lsof", f'[ "$3" = "965" ] && cat {self.d}/lsof.txt\nexit 0\n'),
                 GROKBOT_OSASCRIPT=self.stub("osascript", rec),
                 GROKBOT_OPEN=self.stub("open", rec),
                 GROKBOT_KILL=self.stub("kill", rec),
                 GROKBOT_SLEEP=self.stub("sleep", "exit 0\n"),
                 GROKBOT_NOTIFY=self.stub("notify", rec))
        e.update(env)
        r = subprocess.run(["bash", str(SCRIPT)], env=e, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.now += 300
        return self.calls.read_text()

    def log(self):
        return (self.d / "watchdog.log").read_text()

    def test_connected_does_nothing(self):
        self.lsof = LSOF_UP
        self.assertEqual(self.run_once(), "")
        self.assertIn("tcp=1", self.log())
        self.assertIn("down=0 fails=0", self.log())

    def test_loopback_only_counts_as_down(self):
        self.lsof = LSOF_LOCAL
        self.run_once()
        self.assertIn("tcp=0", self.log())
        self.assertIn("down=1 fails=1", self.log())

    def test_two_down_checks_restart_and_notify(self):
        self.assertEqual(self.run_once(), "")             # 1st disconnected check: wait
        calls = self.run_once()                            # 2nd: restart
        self.assertIn('osascript -e quit app "Grok Bot"', calls)
        self.assertIn("kill -9 965", calls)
        self.assertIn("open -a Grok Bot", calls)
        self.assertIn("notify [Chief] Grok Bot watchdog: restarted", calls)
        self.assertIn("ACTION restarted", self.log())
        self.assertEqual((self.d / "state" / "fails").read_text().strip(), "0")

    def test_recovery_resets_the_count(self):
        self.run_once()
        self.lsof = LSOF_UP
        self.run_once()
        self.lsof = ""
        self.assertEqual(self.run_once(), "")             # back to 1 fail, not 2
        self.assertIn("down=1 fails=1", self.log().splitlines()[-1])

    def test_observe_mode_never_acts(self):
        self.run_once(mode="observe")
        self.assertEqual(self.run_once(mode="observe"), "")
        self.assertIn("WOULD RESTART", self.log())

    def test_tts_lock_holds_until_grace_passes(self):
        (self.d / "locks" / "elevenlabs.lock").mkdir()
        self.run_once()
        self.assertEqual(self.run_once(), "")             # down 5 min, lock held: hold
        self.assertIn("HOLD", self.log())
        for _ in range(3):                                 # down 10, 15 min: still held (grace is "more than 15")
            self.run_once()
        calls = self.run_once()                            # down 20 min: restart despite the lock
        self.assertIn("open -a Grok Bot", calls)

    def test_not_running_relaunches(self):
        self.pids = ""
        calls = self.run_once()
        self.assertIn("open -a Grok Bot", calls)
        self.assertIn("app=not-running", self.log())

    def test_heartbeat_signal(self):
        sessions = self.d / "support" / "dune-reliability" / "sessions"
        sessions.mkdir(parents=True)
        hb = sessions / "s1.running.json"
        hb.write_text("{}")
        os.utime(hb, (self.now - 600, self.now - 600))
        self.lsof = LSOF_UP                                # tcp says up, heartbeat says stale
        self.run_once(GROKBOT_SIGNAL="heartbeat")
        self.assertIn("hb=600", self.log())
        self.assertIn("signal=heartbeat down=1", self.log())

    def test_status_signal_reads_json(self):
        (self.d / "support").mkdir()
        (self.d / "support" / "desktop-status.json").write_text('{"server": {"connected": false}, "v": "0.66.0"}')
        self.lsof = LSOF_UP
        self.run_once(GROKBOT_SIGNAL="status")
        self.assertIn("server.connected=false", self.log())
        self.assertIn("signal=status down=1", self.log())


if __name__ == "__main__":
    unittest.main()
