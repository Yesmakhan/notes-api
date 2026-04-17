import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield  # Здесь выполняется сам тест
    Base.metadata.drop_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_about():
    client.post("/notes", json={"title": "Test info", "done": False})
    
    response = client.get("/about")
    assert response.status_code == 200
    
    data = response.json()
    assert data["project"] == "Notes API"
    assert data["storage"] == "postgres"
    assert data["version"] == 1
    assert data["notes_count"] == 1
    assert data["endpoints_count"] == 8

def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_note():
    new_note = {"title": "Test note"}
    response = client.post("/notes", json=new_note)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == "Test note"
    assert data["done"] is False

def test_get_note_by_id():
    post_response = client.post("/notes", json={"title": "Another test note"})
    post_data = post_response.json()

    by_id_response = client.get(f"/notes/{post_data['id']}")
    assert by_id_response.status_code == 200
    assert by_id_response.json()["title"] == "Another test note"

def test_update_existing_note():
    post_response = client.post("/notes", json={"title": "Original text"})
    post_data = post_response.json()
    
    new_note = {"title": "Updated test note", "done": True}
    
    put_response = client.put(f"/notes/{post_data['id']}", json=new_note)
    assert put_response.status_code == 200

    data = put_response.json()
    assert data["title"] == "Updated test note"
    assert data["done"] is True

def test_delete_note():
    post_response = client.post("/notes", json={"title": "To be deleted"})
    post_data = post_response.json()
    
    delete_response = client.delete(f"/notes/{post_data['id']}")
    assert delete_response.status_code == 200
    
    get_response = client.get(f"/notes/{post_data['id']}")
    assert get_response.status_code == 404

def test_get_notes_with_search():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Fast search example", "done": False})
    
    response = client.get("/notes?search=fast")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    for note in data:
        assert "fast" in note["title"].lower()

def test_get_notes_done_true():
    client.post("/notes", json={"title": "Learn FastAPI", "done": True})
    client.post("/notes", json={"title": "Docker basics", "done": False})
    
    response = client.get("/notes?done=true")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["done"] is True