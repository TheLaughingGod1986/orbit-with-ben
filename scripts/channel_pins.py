#!/usr/bin/env python3
"""For tests: say how a channel keeps its films while a test runs (J2622).

A test that hands the board a channel's films in one shape is about that shape, not about what the real channel does
this week. Until 11 Nov 2026 about fifty tests fed History of Science's films as one pipeline document and leaned on
the real channel keeping them that way. The day that channel moves to one status file per film they would all fail,
in the studio's checks and in the dry run of the move, with nothing wrong in the code.

A test file whose films are in the one-file shape says so:

    PIN = channel_pins.one_file("hos")

    def setUpModule():
        PIN.start()

    def tearDownModule():
        PIN.stop()

or, round one test, `with channel_pins.one_file("hos"): ...`.

While it is on, the loader answers for that channel: it keeps every film in one pipeline file and takes its stages
from that file. Everything else about the channel is what its settings say. A test that plugs in a made-up channel
inside it (by patching `channels._load` with what `channels._load()` returns, plus its own) keeps the pin.
"""
from __future__ import annotations

from unittest import mock

import channels

ONE_FILE = "00_Brand/Channel-Setup/PIPELINE.json"


class one_file:
    """The channel `slug` keeps every film in one pipeline file, at `path` inside its checkout."""

    def __init__(self, slug: str, path: str = ONE_FILE):
        self.slug, self.path, self._on = slug, path, []

    def _pinned(self, settings: dict) -> dict:
        return dict(settings, stages="from pipeline", pipeline={"kind": "pipeline_json", "path": self.path})

    def start(self) -> "one_file":
        loaded = tuple(self._pinned(c) if c["slug"] == self.slug else c for c in channels._load())
        cached = channels._cached

        def load(directory=None):
            return loaded
        load.cache_clear = lambda: None       # the real loader is cached, and some callers clear it

        def cached_copy(slug: str) -> dict:   # the studio's own copy of the settings must say the same
            return self._pinned(cached(slug)) if slug == self.slug else cached(slug)

        self._on = [mock.patch.object(channels, "_load", load), mock.patch.object(channels, "_cached", cached_copy)]
        for patch in self._on:
            patch.start()
        return self

    def stop(self) -> None:
        for patch in reversed(self._on):
            patch.stop()
        self._on = []

    def __enter__(self) -> "one_file":
        return self.start()

    def __exit__(self, *exc) -> None:
        self.stop()
