from sqlalchemy.orm import Session
from app import models, schemas

def get_all_notes(db: Session, done: bool | None = None, search: str | None = None):
    query = db.query(models.Note)
    
    if done is not None:
        query = query.filter(models.Note.done == done)
    if search:
        query = query.filter(models.Note.title.ilike(f"%{search}%"))
        
    return query.all()

def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def create_new_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, done=note.done)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_existing_note(db: Session, note_id: int, updated_note: schemas.NoteUpdate):
    db_note = get_note_by_id(db, note_id)
    if db_note:
        if updated_note.title is not None:
            db_note.title = updated_note.title
        if updated_note.done is not None:
            db_note.done = updated_note.done
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_existing_note(db: Session, note_id: int):
    db_note = get_note_by_id(db, note_id)
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note