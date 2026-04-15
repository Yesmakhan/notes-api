import json
from pathlib import Path

DATA_FILE = Path("data/notes.json")

def load_notes(new_path: str | None = None):
    path_to_notes = DATA_FILE
    if new_path is not None:
        path_to_notes = Path(new_path)

    if not path_to_notes.exists():
        return []
    
    content = path_to_notes.read_text(encoding="utf-8").strip()
    if not content:
        return []
    
    return json.loads(content)

def save_notes(notes, new_path: str | None = None):
    path_to_notes = DATA_FILE
    if new_path is not None:
        path_to_notes = Path(new_path)

    path_to_notes.parent.mkdir(parents=True, exist_ok=True)
    path_to_notes.write_text(
        json.dumps(notes, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )    