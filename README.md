# Notes API

A simple REST API for managing notes, built with FastAPI and PostgreSQL.  
Created as a pet-project for learning backend development, databases, and Docker containerization.

## About the project

This is a basic Notes API that supports full CRUD operations.  
Notes are persistently stored in a PostgreSQL database, and the entire application is containerized using Docker for easy deployment.

## Features

- Get all notes (with search and filtering)
- Get a single note by ID
- Create a new note
- Update an existing note
- Delete a note
- Health and metadata checks

## Tech stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker & Docker Compose
- Pytest

## Project structure

```text
notes-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── tests/
│   └── test_main.py
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting started

The easiest way to run this project is using Docker. 
You don't need to install Python or PostgreSQL on your local machine.

### 1. Clone the repository

```bash
git clone [https://github.com/Yesmakhan/notes-api.git](https://github.com/Yesmakhan/notes-api.git)
cd notes-api
```

### 2. Run with Docker Compose

```bash
docker compose up -d --build
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
| GET | `/about` | Get project metadata |
| GET | `/health` | Health check endpoint |

You can explore and test all endpoints via the interactive docs at:  
`http://127.0.0.1:8000/docs`

## Running tests locally (Without Docker)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
pytest tests/
```

## Author

[Yesmakhan](https://github.com/Yesmakhan)