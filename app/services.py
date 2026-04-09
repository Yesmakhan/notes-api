from fastapi import HTTPException

from app.storage import notes, save_notes


def get_all_notes():
    return notes


def get_note_by_id(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


def create_new_note(note):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "done": note.done
    }
    notes.append(new_note)
    save_notes(notes)
    return new_note


def update_existing_note(note_id: int, updated_note):
    for note in notes:
        if note["id"] == note_id:
            if updated_note.title is not None:
                note["title"] = updated_note.title
            if updated_note.done is not None:
                note["done"] = updated_note.done
            save_notes(notes)
            return note
    raise HTTPException(status_code=404, detail="Note not found")


def delete_existing_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            deleted_note = notes.pop(index)
            save_notes(notes)
            return deleted_note
    raise HTTPException(status_code=404, detail="Note not found")