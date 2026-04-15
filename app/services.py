from fastapi import HTTPException
from pathlib import Path
from app.storage import save_notes, load_notes


def get_all_notes(done: bool | None = None, search: str | None = None, data_file: Path | None = None):
    new_notes = []
    notes = load_notes(data_file)
    if done is None:
        if search is None:
            return notes
        else:
            for note in notes:
                if search.lower() in note["title"].lower():
                    new_notes.append(note)
            return new_notes
    else:
        if search is None:
            for note in notes:
                if note["done"] is done:
                    new_notes.append(note)
            return new_notes
        else:
            for note in notes:
                if note["done"] is done and search.lower() in note["title"].lower():
                    new_notes.append(note)
            return new_notes


def get_note_by_id(note_id: int, data_file: Path | None = None):
    notes = load_notes(data_file)
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


def create_new_note(note, data_file: Path | None = None):
    notes = load_notes(data_file)
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "done": note.done
    }
    notes.append(new_note)
    save_notes(notes, data_file)
    return new_note


def update_existing_note(note_id: int, updated_note, data_file: Path | None = None):
    notes = load_notes(data_file)
    for note in notes:
        if note["id"] == note_id:
            if updated_note.title is not None:
                note["title"] = updated_note.title
            if updated_note.done is not None:
                note["done"] = updated_note.done
            save_notes(notes, data_file)
            return note
    raise HTTPException(status_code=404, detail="Note not found")


def delete_existing_note(note_id: int, data_file: Path | None = None):
    notes = load_notes(data_file)
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            save_notes(notes, data_file)
            return deleted_note
    raise HTTPException(status_code=404, detail="Note not found")