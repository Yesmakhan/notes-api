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