# J2011 — native Gemini audio transport investigation

4 November 2026. Codex, specialist worker. Engineering investigation complete; no supported headless repair established. Park for Chief review, with J1810 still at 2/3 and J1752/J1753 still at 1/3. No acoustic perception or VO approval is claimed.

## Directly observed evidence

- Installed executable: `~/.local/bin/agy`, version **1.5.0**. `agy --help` exposes text/stream-json print input, ACP, and mic-serve; no file-attachment CLI flag.
- Started the installed `agy acp --disable-telemetry` from `/private/tmp` and sent only an ACP `initialize` request. Exit 0. The actual server identifies itself as Antigravity ACP Server 1.5.0 and advertises `promptCapabilities: {image: true, audio: false, embeddedContext: true}`. See [ACP_CAPABILITIES.json](ACP_CAPABILITIES.json) for the exact request and selected non-sensitive response fields. No session/new, prompt, model turn, authentication request or media delivery was attempted. This is a transport-capability observation, not a listening test.
- Inspected only top-level local settings keys, without reading credential files or printing settings values. `~/.gemini/settings.json` has `security`; `~/.gemini/antigravity-cli/settings.json` has `permissions` and `trustedWorkspaces`. Neither contains a top-level custom model/modelFeatures override. This narrow inspection does not establish effective backend media support or rule out every possible nested setting.
- Read the existing J1810 report and PROBE_2 evidence. Its read_file call accepted audio/mpeg, but the first answer contradicted independently measured signal content and the second explicitly declined reliable hearing. File-read permissions and MIME acceptance were already achieved; granting them again would not fix the demonstrated failure.

## Supported routes assessed

| Route | Evidence and conclusion |
|---|---|
| ACP direct audio | Actual installed initialize schema says `audio: false`. Do not force audio blocks into a transport that explicitly declines them, or mislabel audio as image/context. Embedded-context support is not an audio promise. |
| Headless stream-json direct blocks | Official [headless documentation](https://antigravity.google/docs/cli/headless/) specifies text blocks only. No supported direct binary audio injection route is documented. |
| @file in prompt | Official [mention documentation](https://antigravity.google/docs/at-mentions/) describes path context, rather than inlining file contents. This offers no demonstrated bypass of the failed read_file route. |
| Interactive paste | Official [prompting documentation](https://antigravity.google/docs/cli/prompting) lists image/video paste. The installed changelog also mentions audio attachment MIME fixes, so audio support cannot be declared universally absent. Those notes do not supply a verified unattended acoustic-input transport. Interactive audio paste was not tested here. |
| mic-serve / voice | `agy help mic-serve` describes microphone capture, not a file attachment endpoint. Official [voice documentation](https://antigravity.google/docs/voice-mode/) describes a Gemini Live route. Recording, live-model switching, virtual microphone routing and ASR are outside this repair's fixture/file transport scope and were not activated. |

The official [ACP guide](https://antigravity.google/docs/ide/extensions/acp) supports the stdio initialize route used above. No closed-source binary was patched, provider/account/billing changed, or unsupported payload invented. Local release notes were inspected with `agy changelog`; MIME fixes alone are not a finding that acoustic content reaches the reasoning session.

## Why no new fixture pair

The job permits at most one justified pair; it does not require a pair after discovering that candidate transports lack supported audio input. No new supported route survived inspection. Therefore **zero** new fixtures and **zero** acoustic model calls were made. Repeating the old native read_file prompts would spend the bounded investigation on the same failed mechanism. No raw logs, private input, production media, recordings or credentials accompany this report. No model/API/picture/VO credits were spent by this investigation.

The precise established limitation is ACP 1.5.0's explicit lack of direct audio-prompt support, alongside a documented text-only headless stream format. The root cause of the separate native read_file perception failure is **not established**. This is not a claim that every Gemini product or every interactive session lacks hearing.

## Concrete next decision for Chief

Review this engineering evidence, preserving the original capability holds and progress. No timed retry of the unchanged CLI is proposed.

Smallest separate experiment: Chief can scope a local **interactive attachment-only** investigation in the existing subscribed Antigravity CLI, with a bounded operator/session, no microphone or provider/model switch, no production input, and at most one neutral-filename synthetic fixture pair. First establish a real audio attachment control and its declared payload type; if the UI offers only image/video or merely a path/read_file fallback, stop before a model call. If actual audio attachment is available, require blind signal-content discrimination against separately retained waveform truth before registering audio_input. This route is a candidate, not verified support or promised success. Chief must authorize that scope and any specialist-listening delegation; this worker has not activated it.

If interactive attachment cannot provide audio either, Chief needs to approve a separately scoped existing capable reviewer/product route or obtain a vendor-supported transport fix. Any new provider, paid API, account/billing change or production-source egress needs its own explicit authorization; none is implicitly authorized by J2011. A vendor report can use only the initialize request, selected capability response and version above, without uploading private logs or production audio. No external message was sent.

Only the currently elected Chief may recheck/reopen J1810 or activate the undispatched exact-take listening briefs. Actual VO jobs remain audio_input gated. No studio stage, film approval, script, VO, YouTube or Buffer state changed. No work on another queue job or desk task was undertaken.
