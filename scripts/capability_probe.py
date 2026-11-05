#!/usr/bin/env python3
"""Probe a worker's media input with clips whose content only we know, and grade its answer.

Capability reports must come from a real probe, never a model name (chief_relay.record_capabilities). Workers self-report
at session start and, unable to test, report "none", so jobs needing audio or video wait forever. Here the relay makes
a fresh clip each probe (random words, random motion), asks the worker to open it with its own file tool, and grades
the structured reply. Any shell tool use fails the probe: an ffmpeg frame grab or a local ASR is not the model hearing
or watching.

Claude, 5 Nov 2026 (probe by hand): Gemini (`agy` 1.5.1) transcribed a `say` clip and 15 s of the 033 VO word for word,
but described a 6 s moving-square clip wrongly twice. So audio_input is real for Gemini and moving_video_input isn't.

    python3 scripts/capability_probe.py gemini            # print the result
    python3 scripts/capability_probe.py gemini --record   # also record it for the relay
"""
import argparse
import difflib
import json
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile

ADJ = "violet amber silver crooked hollow quiet frozen woollen copper gentle".split()
NOUN = "kettle lantern harbour pebble orchard ladder button compass meadow teapot".split()
VERB = "counted painted carried folded followed borrowed polished buried".split()
PLACE = "lighthouse bakery glacier windmill library canal".split()
COUNT = "three seven eleven twelve nineteen forty".split()
COLOURS = {"red": "red", "green": "lime", "blue": "blue", "yellow": "yellow"}
DIRECTIONS = ("left_to_right", "right_to_left")
# The worker's own file viewers (and agy's end-of-turn `finish`); anything else (run_command, a subagent, the web)
# fails the probe.
FILE_TOOLS = {"read_file", "view_file", "list_dir", "finish"}
AUDIO_PASS = 0.85


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def audio_score(expected, heard):
    """Character match of the words: a random sentence can't be guessed, so near-misses ("woolen", "wheel" for
    "windmill", 5 Nov 2026 live probe: 0.80 by whole words) still prove hearing."""
    return difflib.SequenceMatcher(None, " ".join(words(expected)), " ".join(words(heard))).ratio()


def make_audio(dirpath, rng):
    phrase = (f"The {rng.choice(ADJ)} {rng.choice(NOUN)} {rng.choice(VERB)} {rng.choice(COUNT)} "
              f"{rng.choice(NOUN)}s beside the {rng.choice(ADJ)} {rng.choice(PLACE)}.")
    path = pathlib.Path(dirpath) / "clip_a.wav"
    subprocess.run(["say", "-o", str(path), "--data-format=LEI16@16000", phrase], check=True, capture_output=True)
    return path, phrase


def make_video(dirpath, rng):
    """6 s: one square crosses the frame and changes colour every 2 s. No single frame shows the direction or order."""
    direction = rng.choice(DIRECTIONS)
    order = rng.sample(list(COLOURS), 3)
    x = "20+t*90" if direction == "left_to_right" else "540-t*90"
    spans = ("lt(t,2)", "between(t,2,4)", "gt(t,4)")
    boxes = ",".join(f"drawbox=x='{x}':y=140:w=80:h=80:color={COLOURS[c]}:t=fill:enable='{s}'" for c, s in zip(order, spans))
    path = pathlib.Path(dirpath) / "clip_v.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=black:s=640x360:d=6:r=24",
                    "-vf", boxes, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
    return path, direction, order


AUDIO_SCHEMA = {"type": "object", "required": ["heard", "transcript"],
                "properties": {"heard": {"type": "boolean"}, "transcript": {"type": "string"}}}
VIDEO_SCHEMA = {"type": "object", "required": ["watched", "direction", "colours_in_order"],
                "properties": {"watched": {"type": "boolean"},
                               "direction": {"type": "string", "enum": list(DIRECTIONS) + ["other", "none"]},
                               "colours_in_order": {"type": "array", "items": {"type": "string",
                                                    "enum": list(COLOURS) + ["other"]}}}}
RULES = ("Use only your own file viewer (read_file/view_file). Never run commands, ffmpeg, ASR or scripts. "
         "If the viewer does not give you the actual sound or moving picture, answer heard/watched false.")


def agy_runner(prompt, schema, cwd, timeout=180):
    """Run `agy -p` in the clip folder; return (structured answer or None, tools it used)."""
    agy = shutil.which("agy") or str(pathlib.Path.home() / ".local/bin/agy")
    out = subprocess.run([agy, "-p", prompt, "--sandbox", "--output-format", "stream-json",
                          "--print-timeout", f"{timeout}s", "--json-schema", json.dumps(schema)],
                         cwd=cwd, capture_output=True, text=True, timeout=timeout + 30)
    answer, tools = None, set()
    for line in out.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        step = e.get("step_update") or {}
        if step.get("step_type") == "tool" and step.get("tool_name"):
            tools.add(step["tool_name"])
        if e.get("event") == "result":
            answer = (e.get("result") or {}).get("structured_output")
    return answer, tools


RUNNERS = {"gemini": agy_runner}


def probe(agent, runner=None, rng=None):
    """Return (available capability ids, one-line evidence)."""
    runner = runner or RUNNERS[agent]
    rng = rng or random.Random()
    available, notes = [], []
    with tempfile.TemporaryDirectory(prefix="owb-probe-") as tmp:
        clip, phrase = make_audio(tmp, rng)
        ans, tools = runner(f"Open {clip.name} and transcribe the speech exactly. {RULES}", AUDIO_SCHEMA, tmp)
        extra = sorted(tools - FILE_TOOLS)
        score = audio_score(phrase, (ans or {}).get("transcript", "")) if ans and ans.get("heard") else 0.0
        if score >= AUDIO_PASS and not extra:
            available.append("audio_input")
        notes.append(f"audio {'PASS' if 'audio_input' in available else 'FAIL'} (said {phrase!r}; heard "
                     f"{(ans or {}).get('transcript', '')!r}; match {score:.2f}" + (f"; used {extra}" if extra else "") + ")")

        clip, direction, order = make_video(tmp, rng)
        ans, tools = runner(f"Open {clip.name}. Say which way the square moves and list its colours in the order they "
                            f"appear. {RULES}", VIDEO_SCHEMA, tmp)
        extra = sorted(tools - FILE_TOOLS)
        ok = bool(ans and ans.get("watched") and ans.get("direction") == direction
                  and ans.get("colours_in_order") == order and not extra)
        if ok:
            available.append("moving_video_input")
        notes.append(f"video {'PASS' if ok else 'FAIL'} (truth {direction} {'>'.join(order)}; answer "
                     f"{(ans or {}).get('direction')} {'>'.join((ans or {}).get('colours_in_order') or [])}"
                     + (f"; used {extra}" if extra else "") + ")")
    return available, f"relay probe of {agent}, fresh clips, file tools only: " + "; ".join(notes)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("agent", choices=sorted(RUNNERS))
    ap.add_argument("--record", action="store_true", help="record the result for the relay (60 min)")
    a = ap.parse_args(argv)
    available, evidence = probe(a.agent)
    print(json.dumps({"agent": a.agent, "available": available, "evidence": evidence}, indent=1))
    if a.record:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import chief_relay
        chief_relay.record_capabilities(a.agent, ",".join(available), evidence, 60, chief_relay.now(), source="probe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
