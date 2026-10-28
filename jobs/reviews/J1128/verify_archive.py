"""Verify every source byte; tolerate only NAS-created AppleDouble sidecars."""
import pathlib

def verified(source, destination, before, after):
    if any(after.get(k) != v for k, v in before.items()):
        return False
    for key in set(after) - set(before):
        rel = pathlib.Path(key)
        if not rel.name.startswith("._"):
            return False
        original = source / rel.with_name(rel.name[2:])
        if not original.exists():
            return False
        with (destination / rel).open("rb") as f:
            if f.read(8) != bytes.fromhex("0005160700020000"):
                return False
    return True
