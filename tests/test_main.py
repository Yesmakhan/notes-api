from fastapi.testclient import TestClient
from app.main import app
from app.services import get_all_notes
from app.storage import notes, save_notes

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_about():
    response = client.get("/about")
    assert response.status_code == 200
    
    data = response.json()

    assert data["project"] == "Notes API"
    assert data["storage"] == "file"
    assert data["version"] == 1
    assert data["notes_count"] == len(get_all_notes())
    assert data["endpoints_count"] == 8

def test_get_notes():
    response = client.get("/notes")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for note in data:
        assert isinstance(note["id"], int)
        assert isinstance(note["title"], str)
        assert isinstance(note["done"], bool)

def test_create_note():
    new_note = {
        "title": "Test note"
    }
    response = client.post("/notes", json=new_note)
    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "done" in data
    assert data["title"] == "Test note"
    assert data["done"] == False

def test_get_note_by_id():
    new_note = {
        "title": "Another test note"
    }
    post_response = client.post("/notes", json=new_note)
    assert post_response.status_code == 201

    post_data = post_response.json()

    by_id_response = client.get(f"/notes/{post_data['id']}")
    assert by_id_response.status_code == 200

    data = by_id_response.json()

    assert data["title"] == "Another test note"
    assert data == post_data