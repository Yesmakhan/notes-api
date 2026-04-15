from fastapi.testclient import TestClient
from app.main import app
from app.services import get_all_notes
from app.storage import save_notes

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

def test_update_existing_note():
    original_note = {
        "title": "Original text"
    }

    new_note = {
        "title": "Updated test note",
        "done": True
    }

    post_response = client.post("/notes", json=original_note)
    assert post_response.status_code == 201

    post_data = post_response.json()
    
    by_id_response = client.put(f"/notes/{post_data['id']}", json=new_note)
    assert by_id_response.status_code == 200

    data = by_id_response.json()

    assert data["title"] == new_note["title"]
    assert data["done"] == new_note["done"]
    assert data["id"] == post_data["id"]

def test_delete_note():
    new_note = {
        "title": "Deleted test note",
        "done": True
    }

    post_response = client.post("/notes", json=new_note)
    assert post_response.status_code == 201

    post_data = post_response.json()
    
    by_id_response = client.delete(f"/notes/{post_data['id']}")
    assert by_id_response.status_code == 200

    data = by_id_response.json()

    assert data["title"] == new_note["title"]
    assert data["done"] == new_note["done"]
    assert data["id"] == post_data["id"]

    get_response = client.get(f"/notes/{post_data['id']}")
    assert get_response.status_code == 404

def test_get_notes_with_search():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Fast search example", "done": False})
    client.post("/notes", json={"title": "Docker basics", "done": False})


    search_check_response = client.get("/notes?search=fast")
    assert search_check_response.status_code == 200

    data = search_check_response.json()
    assert isinstance(data, list)
    
    for note in data:
        assert "fast" in note["title"].lower()

def test_get_notes_done_true():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Fast search example", "done": False})
    client.post("/notes", json={"title": "Docker basics", "done": False})


    done_check_response = client.get("/notes?done=true")
    assert done_check_response.status_code == 200
    
    data = done_check_response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for note in data:
        assert note["done"] is True

def test_get_notes_with_done_true_and_search():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Fast search example", "done": False})
    client.post("/notes", json={"title": "Docker basics", "done": False})


    mixed_check_response = client.get("/notes?done=true&search=fast")
    assert mixed_check_response.status_code == 200

    data = mixed_check_response.json()
    assert isinstance(data, list)
    
    for note in data:
        assert note["done"] is True
        assert "fast" in note["title"].lower()

def test_get_notes_with_done_false_and_search():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Fast search example", "done": False})
    client.post("/notes", json={"title": "Docker basics", "done": False})


    mixed_check_response = client.get("/notes?done=false&search=fast")
    assert mixed_check_response.status_code == 200

    data = mixed_check_response.json()
    assert isinstance(data, list)

    for note in data:
        assert note["done"] is False
        assert "fast" in note["title"].lower()
