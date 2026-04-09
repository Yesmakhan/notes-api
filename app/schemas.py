from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    done: bool = False

class NoteUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class NoteResponse(BaseModel):
    id: int
    title: str
    done: bool

class AboutResponse(BaseModel):
    project: str
    storage: str
    version: int
    notes_count: int
    endpoints_count: int