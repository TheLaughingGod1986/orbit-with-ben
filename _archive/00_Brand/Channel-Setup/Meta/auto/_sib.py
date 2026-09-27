#!/usr/bin/env python3
"""Load sibling Meta auto modules under unique sys.modules keys (avoid TikTok clashes)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

AUTO = Path(__file__).resolve().parent


def load(name: str) -> ModuleType:
    key = f"orbit_meta_auto_{name}"
    if key in sys.modules:
        return sys.modules[key]
    path = AUTO / f"{name}.py"
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod
