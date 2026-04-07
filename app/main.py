from fastapi import FastAPI, HTTPException

from app.schemas import NoteCreate, NoteUpdate, NoteResponse
from app.storage import notes

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/notes", response_model=list[NoteResponse])
def get_notes():
    return notes


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.post("/notes", status_code=201, response_model=NoteResponse)
def create_note(note: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "done": note.done
    }
    notes.append(new_note)
    return new_note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated_note: NoteUpdate):
    for note in notes:
        if note["id"] == note_id:
            if updated_note.title is not None:
                note["title"] = updated_note.title
            if updated_note.done is not None:
                note["done"] = updated_note.done
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            return deleted_note
    raise HTTPException(status_code=404, detail="Note not found")