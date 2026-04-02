from fastapi import FastAPI

app = FastAPI()

notes = [
    {"id" : 1, "title" : "Learn FastAPI", "done" : False},
    {"id" : 2, "title" : "Learn Git", "done" : False},
]

@app.get("/")
def root():
    return {"message": "My first backend app"}

@app.get("/health")
def health():
    return {"status" : "Healthy"}

@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    return {"error" : "Note not found"}

@app.post("/notes")
def create_note(note: dict):
    new_note = {
        "id" : len(notes) + 1,
        "title" : note["title"],
        "done" : note.get("done", False)
    }
    notes.append(new_note)
    return new_note