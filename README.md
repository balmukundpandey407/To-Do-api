
# To-Do API

A simple and structured REST API built using FastAPI for managing tasks.  
This project demonstrates CRUD operations, filtering, searching, sorting, pagination, and PostgreSQL database integration using SQLAlchemy.

---

## Features

- Create, update, and delete tasks
- Retrieve single or multiple tasks
- Filter tasks by status
- Search tasks by title or description
- Sort tasks by created or updated time
- Pagination support
- UUID-based task IDs
- PostgreSQL database integration
- Clean project architecture

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

---

## Installation

```bash
git clone <repository-url>
cd <project-folder>

pip install -r requirements.txt
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

Server will run at:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/task` | Create a task |
| GET | `/tasks` | Get all tasks |
| GET | `/task/{task_id}` | Get task by ID |
| PATCH | `/task/{task_id}` | Update task |
| DELETE | `/task/{task_id}` | Delete task |

---

## Requirements

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
```

---

## Author

Developed by BALMUKUND PANDEY
````
