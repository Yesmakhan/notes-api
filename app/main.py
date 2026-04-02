from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    done: bool = False


notes = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Learn Git", "done": False},
]


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes")
def get_notes():
    return notes


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    return {"error": "Note not found"}


@app.post("/notes")
def create_note(note: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "done": note.done
    }
    notes.append(new_note)
    return new_note


@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteCreate):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["done"] = updated_note.done
            return note
    return {"error": "Note not found"}


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            return deleted_note
    return {"error": "Note not found"}