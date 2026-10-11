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

Failover (Ben): when the primary hits its limit the backup takes over, and the next job of that kind goes back to the
primary once it's up again. A stand-in never makes a protected call (PROTECTED): it parks the job for Chief with
`jobs.py block --reason "parked for Chief: ..."`.
"""
from __future__ import annotations

import sys

# Real, configured model ids (11 Oct 2026).
MODELS = {
    "grok": "Grok Bot app (Chief)",
    "claude-opus-5-5": "Claude Opus 5.5 (Claude cloud sessions; Claude Code 2.1.288 on the Mini)",
    "gpt-6-astra": "GPT-6-Astra (Codex CLI 0.160, `-m gpt-6-astra`; checked on the Mini 11 Oct)",
    "gpt-6.1-sol": "GPT-6.1-Sol (Codex CLI default)",
    "cursor-auto": "Cursor agent CLI, model Auto",
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

# The agent (jobs.py --agent) that runs each model.
RUNS_ON = {"grok": "chief", "claude-opus-5-5": "claude", "gpt-6-astra": "codex", "gpt-6.1-sol": "codex",
           "cursor-auto": "cursor"}

# Calls only Chief (Grok) makes; real money and the irreversible stay with Ben.
PROTECTED = ("final OK / PASS", "merge", "AGENTS.md and the Never list", "spend past the written rules",
             "anything irreversible")

# kind: (job type, primary (agent, model), backup (agent, model) or None, how the job runs)
KINDS = {
    "script":   ("Script writing and fact research", ("claude", "claude-opus-5-5"), ("codex", "gpt-6-astra"),
                 "Claude writes; Gemini (agy) drafts SOURCES.md and checks every claim (kind facts)"),
    "facts":    ("Sources and claims check", ("cursor", "gemini-agy"), ("claude", "claude-opus-5-5"),
                 "the acting Chief or worker runs `agy` (claims as <driver>/gemini); Claude's quote check backs it"),
    "review":   ("Script review, reasoning, shot lists, music prompts", ("claude", "claude-opus-5-5"),
                 ("codex", "gpt-6-astra"), "Codex's review is advisory; Chief makes the call"),
    "vo":       ("Voice-over", ("cursor", "eleven_v3"), ("codex", "eleven_v3"),
                 "vo_take.py / el_client.py on the Mini, Scribe v2 check; no other voice, ever"),
    "image":    ("Stills, plates and thumbnail art", ("cursor", "gemini-2.5-flash-image"),
                 ("codex", "gemini-2.5-flash-image"),
                 "OWB: master frame or NASA plate first, else a Vertex still; HOS: Flow Nano Banana 2, then Vertex. "
                 "Text always from the builders, never the image model"),
    "chart":    ("Charts, graphs, overlays, people cards, date call-outs, thumbnail builders", ("codex", "gpt-6-astra"),
                 ("cursor", "cursor-auto"), "our own code graphics (Python/ffmpeg), rendered per row"),
    "video":    ("Video generation", ("cursor", "veo-3.1-fast-generate-001"), ("codex", "veo-3.1-fast-generate-001"),
                 "OWB: Vertex Veo (Quality only for a hero), Omni gemini-omni-flash-preview at global for Orbit only; "
                 "HOS: Flow Veo 3.1, fallback Vertex Veo"),
    "assembly": ("Picture assembly, ffmpeg, code and tools", ("cursor", "cursor-auto"), ("codex", "gpt-6.1-sol"),
                 "on the Mini; long renders in detached tmux"),
    "qa":       ("Frame review and QA", ("claude", "claude-opus-5-5"), ("codex", "gpt-6-astra"),
                 "picture_qa / polish_gate / music_gate must PASS first; Chief gives the PASS"),
    "listing":  ("Titles, descriptions, tags, SEO", ("claude", "claude-opus-5-5"), ("codex", "gpt-6-astra"),
                 "Gemini checks any fact in it; Chief OKs; applied by the upload or Studio job"),
    "studio":   ("Studio browser tasks", ("chief", "grok"), ("cursor", "cursor-auto"),
                 "OWB Studio CDP 9223, HOS Flow 9222; never Replace, never delete"),
    "chief":    ("Merges, final OK, PASS, AGENTS.md", ("chief", "grok"), None,
                 "no stand-in: parked for Chief; money and the irreversible go to Ben"),
}


def route(kind: str) -> dict:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {', '.join(KINDS)}")
    what, primary, backup, how = KINDS[kind]
    return {"kind": kind, "what": what, "primary": primary, "backup": backup, "how": how}


def model_for(job: dict, agent: str) -> str:
    """The model `agent` should run for this job: the job's own `model` if it names one this agent runs, else the
    table's model for this agent in the job's kind, else "" (the agent's default)."""
    m = job.get("model") or ""
    if m and RUNS_ON.get(m) == agent:
        return m
    kind = job.get("kind")
    if kind in KINDS:
        for lane in KINDS[kind][1:3]:
            if lane and lane[0] == agent and RUNS_ON.get(lane[1]) == agent:
                return lane[1]
    return ""


def preferred_worker(job: dict) -> str:
    """The Mini worker (cursor or codex) a job should go to first, or "" when either will do."""
    m = job.get("model") or ""
    if RUNS_ON.get(m) in ("cursor", "codex"):
        return RUNS_ON[m]
    kind = job.get("kind")
    if kind in KINDS:
        for lane in KINDS[kind][1:3]:
            if lane and lane[0] in ("cursor", "codex"):
                return lane[0]
    return ""


def table() -> str:
    rows = ["| Job type | kind | Primary | Backup |", "|---|---|---|---|"]
    for k, (what, p, b, _) in KINDS.items():
        rows.append(f"| {what} | `{k}` | {p[0]} · `{p[1]}` | {(b[0] + ' · `' + b[1] + '`') if b else 'none: parked for Chief'} |")
    return "\n".join(rows)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        r = route(sys.argv[1])
        print(f"{r['what']}\n  primary: {r['primary'][0]} ({MODELS[r['primary'][1]]})\n  backup:  "
              + (f"{r['backup'][0]} ({MODELS[r['backup'][1]]})" if r["backup"] else "none (parked for Chief)")
              + f"\n  how:     {r['how']}")
    else:
        print(table())
