import json
from pathlib import Path

DATA_FILE = Path("data/notes.json")

def load_notes():
    if not DATA_FILE.exists():
        return []
    
    content = DATA_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []
    
    return json.loads(content)

def save_notes(notes):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(notes, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


notes = load_notes()