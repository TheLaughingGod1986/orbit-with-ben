"""Read the published local board for dispatch; never write it or persist it in the queue."""
import json
from pathlib import Path

BOARD = Path.home() / "_desk/state/board/board.json"
_CACHE = {}


def load_tracker(path=None):
    target = Path(path or BOARD)
    try:
        st = target.stat()
        key = (str(target), st.st_mtime_ns, st.st_size)
        if key not in _CACHE:
            board = json.loads(target.read_text())
            tracker = board.get("tracker") if isinstance(board, dict) else None
            _CACHE[key] = tracker if isinstance(tracker, dict) and isinstance(tracker.get("videos"), list) else {}
        return _CACHE[key]
    except (OSError, ValueError):
        return {}
