"""Read the published local board for dispatch; never write it or persist it in the queue."""
import copy
import json
from pathlib import Path

BOARD = Path.home() / "_desk/state/board/board.json"
_CACHE = {}


def load_tracker(path=None):
    """The board's tracker, or {}. The file is parsed once per version (path, mtime, size); every caller gets its
    own copy, so one caller changing what it was handed can never change what the next caller reads."""
    target = Path(path or BOARD)
    try:
        st = target.stat()
        key = (str(target), st.st_mtime_ns, st.st_size)
        if key not in _CACHE:
            board = json.loads(target.read_text())
            tracker = board.get("tracker") if isinstance(board, dict) else None
            _CACHE.clear()
            _CACHE[key] = tracker if isinstance(tracker, dict) and isinstance(tracker.get("videos"), list) else {}
        return copy.deepcopy(_CACHE[key])
    except (OSError, ValueError):
        return {}
