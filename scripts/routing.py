#!/usr/bin/env python3
"""Who does what: each kind of job -> the model that does it best, and its backup (Ben, 11 Oct 2026).

Ben, 11 Oct 2026 21:48: "Make sure all the tasks are correctly dedicated to the correct LLM that can do the job. If
GPT-Astra is better at image or graph creation, use GPT-Astra. If Claude Opus 5.5 is better at reasoning and script
writing, use that."

This table is the code copy of AGENTS.md "Who does what"; test_routing.py checks the two agree. Model ids are only the
ones actually configured on the Mac mini on 11 Oct 2026 (Codex models_cache, Claude Code sessions, Cursor cli-config,
the Vertex and ElevenLabs tools). Never add a name that isn't installed.

  python3 scripts/routing.py            # print the table
  python3 scripts/routing.py chart      # one kind: primary, backup, model to pass

Fallback chains (Ben, 11 Oct 2026 23:40 and 23:47): "if Claude Code is out of usage you can use a Claude model in
Cursor" and "remember we also have Gemini and Codex". Each kind has a CHAIN: the primary, then every stand-in in
order. A Claude-owned job goes 1) Claude Code, 2) Cursor CLI on the same Claude model (CURSOR_CLAUDE_MODEL), 3) Gemini
via `agy` for reasoning, scripts, listings and review notes, 4) Codex gpt-6-astra as the last resort. Code and
graphics go to Codex first. When a worker is out of usage or rate-limited, chief_relay.py walks the chain to the next
worker that is up (`jobs.py reroute` for a job already addressed to the worker that ran out), instead of parking the
job; the next job of that kind goes back to the primary once it's up again. Which worker ran each job is logged
(~/_desk/state/chief/runs.jsonl).
A stand-in never makes a protected call (PROTECTED): it parks the job for Chief with
`jobs.py block --reason "parked for Chief: ..."`.
"""
from __future__ import annotations

import os
import sys

# Real, configured model ids (11 Oct 2026).
MODELS = {
    "grok": "Grok Bot app (Chief)",
    "claude-opus-5-5": "Claude Opus 5.5 (Claude cloud sessions; Claude Code 2.1.288 on the Mini)",
    "gpt-6-astra": "GPT-6-Astra (Codex CLI 0.160, `-m gpt-6-astra`; checked on the Mini 11 Oct)",
    "gpt-6.1-sol": "GPT-6.1-Sol (Codex CLI default)",
    "cursor-auto": "Cursor agent CLI, model Auto",
    "cursor-claude-opus-5-5": "Claude Opus 5.5 inside the Cursor agent CLI on the Mini (`agent --model claude-opus-5-5`); "
                              "Claude's first fallback when Claude Code is out of usage",
    "gemini-agy": "Gemini via Antigravity `agy` (its default model)",
    "eleven_v3": "ElevenLabs eleven_v3, voice Ben Orbit Narrator (API only)",
    "scribe_v2": "ElevenLabs Scribe v2 (VO word check)",
    "veo-3.1-fast-generate-001": "Vertex Veo 3.1 Fast",
    "veo-3.1-generate-001": "Vertex Veo 3.1 Quality",
    "gemini-omni-flash-preview": "Vertex Gemini Omni Flash, location global (Orbit only)",
    "gemini-2.5-flash-image": "Vertex Gemini 2.5 Flash Image (stills, no text)",
    "flow-veo-3.1": "Google Flow Veo 3.1 (HOS, Mini browser)",
    "flow-nano-banana-2": "Google Flow Nano Banana 2 (HOS stills)",
}

# The agent (jobs.py --agent) that runs each model. "gemini" = the Antigravity `agy` CLI woken by the relay itself.
RUNS_ON = {"grok": "chief", "claude-opus-5-5": "claude", "gpt-6-astra": "codex", "gpt-6.1-sol": "codex",
           "cursor-auto": "cursor", "cursor-claude-opus-5-5": "cursor", "gemini-agy": "gemini"}

# The Mini workers the relay can wake (chief_relay.cli_spec). Claude and Chief are woken elsewhere.
MINI_WORKERS = ("cursor", "codex", "gemini")

# The model id the Cursor agent CLI is given (`agent --model <id>`) when it stands in for Claude. "claude-opus-5-5" is
# the Opus 5.5 entry in Cursor's own model list on the Mini (availableDefaultModels2: name "claude-opus-5-5",
# supportsAgent true; read 11 Oct 2026). It is the same Opus tier Claude Code runs. Cursor also lists
# claude-fable-5-1 (special data-retention terms), which we don't use. If Cursor renames the id, change it here or set
# CURSOR_CLAUDE_MODEL in the relay's environment; `agent --list-models` on the Mini shows the current names.
CURSOR_CLAUDE_MODEL = os.environ.get("CURSOR_CLAUDE_MODEL", "claude-opus-5-5")

# routing key -> the string the worker's CLI takes. "" = the CLI's own default (Cursor Auto, agy's default Gemini).
CLI_MODEL = {"cursor-auto": "", "cursor-claude-opus-5-5": CURSOR_CLAUDE_MODEL, "gemini-agy": ""}

# Claude's first fallback when Claude Code is out of usage or rate-limited (Ben, 11 Oct 2026 23:40).
CLAUDE_FALLBACK = ("cursor", "cursor-claude-opus-5-5")
GEMINI = ("gemini", "gemini-agy")
ASTRA = ("codex", "gpt-6-astra")

# Calls only Chief (Grok) makes; real money and the irreversible stay with Ben.
PROTECTED = ("final OK / PASS", "merge", "AGENTS.md and the Never list", "spend past the written rules",
             "anything irreversible")

# Reasoning, scripts, listings and review notes: Claude Code -> Cursor on Claude -> Gemini -> Codex (last resort).
_CLAUDE_CHAIN = [("claude", "claude-opus-5-5"), CLAUDE_FALLBACK, GEMINI, ASTRA]

# kind: (job type, chain [(agent, model), ...] primary first, how the job runs). Code and graphics: Codex first.
# Tool jobs (vo, image, video): the same tool, run by whichever worker is up.
CHAINS = {
    "script":   ("Script writing and fact research", _CLAUDE_CHAIN,
                 "Claude writes; Gemini (agy) drafts SOURCES.md and checks every claim (kind facts). A Gemini or Codex "
                 "draft is a draft only; Claude or Chief locks it"),
    "facts":    ("Sources and claims check", [("cursor", "gemini-agy"), GEMINI, ("claude", "claude-opus-5-5"),
                                               CLAUDE_FALLBACK, ASTRA],
                 "the worker runs `agy` (claims as <driver>/gemini), or the relay wakes agy itself; Claude's quote "
                 "check backs it"),
    "review":   ("Script review, reasoning, shot lists, music prompts", _CLAUDE_CHAIN,
                 "a stand-in's review is advisory; Chief makes the call"),
    "vo":       ("Voice-over", [("cursor", "eleven_v3"), ("codex", "eleven_v3"), ("gemini", "eleven_v3")],
                 "vo_take.py / el_client.py on the Mini, Scribe v2 check; no other voice, ever"),
    "image":    ("Stills, plates and thumbnail art", [("cursor", "gemini-2.5-flash-image"),
                                                      ("codex", "gemini-2.5-flash-image"),
                                                      ("gemini", "gemini-2.5-flash-image")],
                 "OWB: master frame or NASA plate first, else a Vertex still; HOS: Flow Nano Banana 2, then Vertex. "
                 "Text always from the builders, never the image model"),
    "chart":    ("Charts, graphs, overlays, people cards, date call-outs, thumbnail builders",
                 [ASTRA, ("cursor", "cursor-auto"), GEMINI],
                 "our own code graphics (Python/ffmpeg), rendered per row"),
    "video":    ("Video generation", [("cursor", "veo-3.1-fast-generate-001"), ("codex", "veo-3.1-fast-generate-001"),
                                      ("gemini", "veo-3.1-fast-generate-001")],
                 "OWB: Vertex Veo (Quality only for a hero), Omni gemini-omni-flash-preview at global for Orbit only; "
                 "HOS: Flow Veo 3.1, fallback Vertex Veo"),
    "assembly": ("Picture assembly, ffmpeg, code and tools", [("cursor", "cursor-auto"), ("codex", "gpt-6.1-sol"), GEMINI],
                 "on the Mini; long renders in detached tmux"),
    "qa":       ("Frame review and QA", _CLAUDE_CHAIN,
                 "picture_qa / polish_gate / music_gate must PASS first; Chief gives the PASS"),
    "listing":  ("Titles, descriptions, tags, SEO", _CLAUDE_CHAIN,
                 "Gemini checks any fact in it; Chief OKs; applied by the upload or Studio job"),
    "studio":   ("Studio browser tasks", [("chief", "grok"), ("cursor", "cursor-auto"), ("codex", "gpt-6.1-sol")],
                 "OWB Studio CDP 9223, HOS Flow 9222; never Replace, never delete"),
    "chief":    ("Merges, final OK, PASS, AGENTS.md", [("chief", "grok")],
                 "no stand-in: parked for Chief; money and the irreversible go to Ben"),
}

# Older view kept for callers: kind -> (job type, primary, first fallback or None, how).
KINDS = {k: (what, ch[0], ch[1] if len(ch) > 1 else None, how) for k, (what, ch, how) in CHAINS.items()}


def chain(kind: str) -> list:
    """Primary, then every fallback in order."""
    return list(CHAINS[kind][1])


def fallbacks(kind: str) -> list:
    """The kind's stand-ins in order (the chain without its primary)."""
    return chain(kind)[1:]


lanes = chain  # older name


def job_chain(job: dict) -> list:
    """The chain for one job: its kind's chain; a job naming only a model gets the chain of the first kind whose
    primary runs that model (claude-opus-5-5 -> the Claude chain), else just that model."""
    kind = job.get("kind")
    if kind in CHAINS:
        return chain(kind)
    m = job.get("model") or ""
    for k, (_, ch, _) in CHAINS.items():
        if ch[0][1] == m:
            return list(ch)
    return [(RUNS_ON[m], m)] if m in RUNS_ON else []


def next_lane(job: dict, after_agent: str = "", up=None, after_model: str = ""):
    """The first lane in the job's chain after the lane (after_agent, after_model) whose worker is a Mini worker in
    `up`. With no `after_agent`, the first such lane from the top. None when the chain runs out."""
    ch = job_chain(job)
    start = 0
    if after_agent:
        idx = [i for i, (a, m) in enumerate(ch) if a == after_agent and (not after_model or m == after_model)]
        start = idx[0] + 1 if idx else 0
    for a, m in ch[start:]:
        if a in MINI_WORKERS and (up is None or a in up):
            return (a, m)
    return None


def claude_owned(job: dict) -> bool:
    """Claude does this job first: its model is claude-opus-5-5, or (no model named) its kind's primary is Claude."""
    m = job.get("model") or ""
    if m:
        return RUNS_ON.get(m) == "claude"
    kind = job.get("kind")
    return kind in CHAINS and CHAINS[kind][1][0][0] == "claude"


def cli_model(key: str) -> str:
    """The id the worker's CLI is given for a routing key: Codex takes the key itself (gpt-...), Cursor takes
    CLI_MODEL's string ("" = its Auto default)."""
    if key in CLI_MODEL:
        return CLI_MODEL[key]
    return key


def route(kind: str) -> dict:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {', '.join(KINDS)}")
    what, primary, backup, how = KINDS[kind]
    fb = fallbacks(kind)
    return {"kind": kind, "what": what, "primary": primary, "backup": fb[0] if fb else None, "fallbacks": fb,
            "how": how}


def model_for(job: dict, agent: str) -> str:
    """The model `agent` should run for this job: the job's own `model` if it names one this agent runs, else the
    table's model for this agent in the job's kind (primary, then fallbacks in order), else "" (the agent's default).
    A Claude job handed to Cursor gets cursor-claude-opus-5-5, so Cursor runs it on the Claude model, not Auto."""
    m = job.get("model") or ""
    if m and RUNS_ON.get(m) == agent:
        return m
    for a, lm in job_chain(job):
        if a == agent:  # this agent's first lane in the chain decides (facts: Cursor drives agy, not Claude)
            return lm if RUNS_ON.get(lm) == agent else ""
    return ""


def preferred_worker(job: dict, up=None) -> str:
    """The Mini worker a job should go to: its own model's worker, else the first Mini worker in its chain that is in
    `up` (all of them when up is None); "" when the chain names none (any worker will do)."""
    m = job.get("model") or ""
    if RUNS_ON.get(m) in MINI_WORKERS and (up is None or RUNS_ON[m] in up):
        return RUNS_ON[m]
    lane = next_lane(job, up=up)
    return lane[0] if lane else ""


def table() -> str:
    rows = ["| Job type | kind | Primary | Fallbacks, in order |", "|---|---|---|---|"]
    for k, (what, p, _, _) in KINDS.items():  # noqa: B007
        fb = fallbacks(k)
        rows.append(f"| {what} | `{k}` | {p[0]} · `{p[1]}` | "
                    + (" → ".join(f"{a} · `{m}`" for a, m in fb) if fb else "none: parked for Chief") + " |")
    return "\n".join(rows)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        r = route(sys.argv[1])
        print(f"{r['what']}\n  primary: {r['primary'][0]} ({MODELS[r['primary'][1]]})\n"
              + ("".join(f"  fallback {i}: {a} ({MODELS[m]})\n" for i, (a, m) in enumerate(r["fallbacks"], 1))
                 or "  fallback: none (parked for Chief)\n")
              + f"  how:     {r['how']}")
    else:
        print(table())
