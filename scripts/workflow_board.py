"""Read the published local board for dispatch; never write it or persist it in the queue."""
import json
from pathlib import Path

BOARD = Path.home() / "_desk/state/board/board.json"


def load_tracker(path=None):
    try:
        board = json.loads((path or BOARD).read_text())
        tracker = board.get("tracker") if isinstance(board, dict) else None
        return tracker if isinstance(tracker, dict) and isinstance(tracker.get("videos"), list) else {}
    except (OSError, ValueError):
        return {}
