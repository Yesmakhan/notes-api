from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    done: bool = False

class NoteUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

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
    raise HTTPException(status_code=404, detail="Note not found")

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "done": note.done
    }
    notes.append(new_note)
    return new_note


@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteUpdate):
    for note in notes:
        if note["id"] == note_id:
            if updated_note.title is not None:
                note["title"] = updated_note.title
            if updated_note.done is not None:
                note["done"] = updated_note.done
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            return deleted_note
    raise HTTPException(status_code=404, detail="Note not found")