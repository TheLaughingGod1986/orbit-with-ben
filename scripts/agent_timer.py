#!/usr/bin/env python3
"""One agent's heartbeat (J3265). Launchd runs `tick` every 10–15 minutes.

AGENT_SELF_DISPATCH=0 makes tick record a wake and exit, so the relay is the only dispatcher.
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import agent_autonomy  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    tick = sub.add_parser("tick")
    tick.add_argument("--agent", required=True, choices=[agent for agent, _, _ in agent_autonomy.TIMERS])
    write = sub.add_parser("write-plists")
    write.add_argument("--dir", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "write-plists":
        for path in agent_autonomy.write_plists(pathlib.Path(args.dir)):
            print(path)
        return 0
    return agent_autonomy.live_tick(args.agent)


if __name__ == "__main__":
    sys.exit(main())
