# Notes API

A simple REST API for managing notes, built with FastAPI.  
Created as a pet-project for learning backend development, Python, and Git.

## About the project

This is a basic Notes API that supports full CRUD operations.  
Notes are stored in a JSON file so data persists between restarts.

## Features

- Get all notes
- Get a single note by ID
- Create a new note
- Update an existing note
- Delete a note

## Tech stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Project structure

```
notes-api/
├── app/
│   └── main.py
├── data/
│   └── notes.json
├── tests/
│   └── test_main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Yesmakhan/notes-api.git
cd notes-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes |
| GET | `/notes/{id}` | Get a note by ID |
| POST | `/notes` | Create a new note |
| PUT | `/notes/{id}` | Update a note |
| DELETE | `/notes/{id}` | Delete a note |

You can explore and test all endpoints via the interactive docs at:  
`http://127.0.0.1:8000/docs`

## Running tests

```bash
pytest tests/
```

## Author

[Yesmakhan](https://github.com/Yesmakhan)