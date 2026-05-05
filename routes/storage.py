import json
from pathlib import Path
from threading import Lock

# Path to the data folder — JSON files act as our tiny "database" so nothing
# external has to be installed for the demo to run.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Lock so two requests writing at the same time don't corrupt the JSON file.
_write_lock = Lock()


# Read a JSON file from data/ and return whatever python type is in it
# (list for collections, dict for the sprint state).
def load(name: str):
    path = DATA_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# Write any python object back as nicely indented JSON. We acquire a lock
# so concurrent writes can't shred the file.
def save(name: str, data) -> None:
    path = DATA_DIR / name
    with _write_lock:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
