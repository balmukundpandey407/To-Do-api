
# To-Do API

A simple and structured REST API built using FastAPI for managing tasks.  
This project demonstrates CRUD operations, filtering, searching, sorting, pagination, and PostgreSQL database integration using SQLAlchemy.

---

## Live Demo

API Documentation:

https://to-do-api-687z.onrender.com/docs#/

---

## Features

- User Registration & Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected Routes
- Task CRUD Operations
- Search, Filter & Sort
- Pagination
- UUID-based IDs
- PostgreSQL Integration
- User-specific Task Ownership

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- bcrypt
- Render

## API Endpoints

### Auth
- POST `/register`
- POST `/login`

### Tasks
- POST `/task`
- GET `/tasks`
- GET `/task/{task_id}`
- PATCH `/task/{task_id}`
- DELETE `/task/{task_id}`
- GET `/tasks/filter`
- GET `/tasks/search`
- GET `/tasks/sort`

## Concepts Practiced

- REST APIs
- CRUD Operations
- Authentication & Authorization
- SQLAlchemy ORM
- Database Relationships
- Pagination
- Filtering & Searching
- Dependency Injection

## Future Improvements

- Refresh Tokens
- Alembic Migrations
- Docker
- Unit Testing

## Author

BALMUKUND PANDEY