# To-Do API

A simple REST API built using FastAPI for managing tasks.
This project demonstrates CRUD operations, filtering, searching, sorting, pagination, and data validation using Pydantic.

---

## Features

* Create, update, delete tasks
* Get all tasks or a single task by ID
* Filter tasks by status
* Search tasks by title or description
* Sort tasks by creation/update time
* Pagination support
* UUID-based task IDs
* JSON file storage

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

---

## Installation

```bash id="tczm3f"
git clone <repository-url>
cd <project-folder>

pip install -r requirements.txt
```

---

## Run the Server

```bash id="4fv50t"
uvicorn main:app --reload
```

Server runs at:

```bash id="x2k4wt"
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```bash id="9j0j4s"
http://127.0.0.1:8000/docs
```

ReDoc:

```bash id="cbyhbb"
http://127.0.0.1:8000/redoc
```

---

## Main Endpoints

| Method | Endpoint          | Description      |
| ------ | ----------------- | ---------------- |
| GET    | `/`               | Check API status |
| POST   | `/task`           | Create task      |
| GET    | `/tasks`          | Get all tasks    |
| GET    | `/task/{task_id}` | Get task by ID   |
| PATCH  | `/task/{task_id}` | Update task      |
| DELETE | `/task/{task_id}` | Delete task      |
| GET    | `/tasks/filter`   | Filter tasks     |
| GET    | `/tasks/search`   | Search tasks     |
| GET    | `/tasks/sort`     | Sort tasks       |

---

## Example Task Object

```json id="v8oqrq"
{
  "id": "uuid-string",
  "title": "Learn FastAPI",
  "description": "Build CRUD API",
  "completion": "Pending",
  "created_at": "2026-05-21T10:30:00",
  "updated_at": "2026-05-21T10:30:00"
}
```

---

## Requirements

```txt id="jlwmn2"
fastapi
uvicorn
pydantic
```
## author 
   BALMUKUND PANDEY