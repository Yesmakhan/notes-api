from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import NoteCreate, NoteUpdate, NoteResponse, AboutResponse
from app.services import (
    get_all_notes,
    get_note_by_id,
    create_new_note,
    update_existing_note,
    delete_existing_note,
)
from app.database import engine, get_db
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/about", response_model=AboutResponse)
def about(db: Session = Depends(get_db)):
    return {
        "project": "Notes API",
        "storage": "postgres",
        "version": 1,
        "notes_count": len(get_all_notes(db)),
        "endpoints_count": 8
    }

@app.get("/notes", response_model=list[NoteResponse])
def get_notes(done: bool | None = None, search: str | None = None, db: Session = Depends(get_db)):
    return get_all_notes(db, done=done, search=search)

@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes", status_code=201, response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return create_new_note(db, note)

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated_note: NoteUpdate, db: Session = Depends(get_db)):
    note = update_existing_note(db, note_id, updated_note)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = delete_existing_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note