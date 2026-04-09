from fastapi import FastAPI

from app.schemas import NoteCreate, NoteUpdate, NoteResponse, AboutResponse
from app.services import (
    get_all_notes,
    get_note_by_id,
    create_new_note,
    update_existing_note,
    delete_existing_note,
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/about", response_model=AboutResponse)
def about():
    return {
        "project": "Notes API",
        "storage": "file",
        "version": 1,
        "notes_count": len(get_all_notes())
    }


@app.get("/notes", response_model=list[NoteResponse])
def get_notes():
    return get_all_notes()


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    return get_note_by_id(note_id)


@app.post("/notes", status_code=201, response_model=NoteResponse)
def create_note(note: NoteCreate):
    return create_new_note(note)


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated_note: NoteUpdate):
    return update_existing_note(note_id, updated_note)


@app.delete("/notes/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int):
    return delete_existing_note(note_id)