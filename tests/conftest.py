import json
import pytest

import app.storage as storage

@pytest.fixture(autouse=True)
def temp_notes_file(tmp_path, monkeypatch):
    test_file = tmp_path / "notes.json"
    test_file.write_text(json.dumps([]), encoding="utf-8")
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    return test_file