from fastapi import FastAPI, HTTPException, Query, APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
import json
import datetime
import uuid
from schemas.task import TaskCreate, Task, TaskUpdate
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, Task as TaskModel
import models

router = APIRouter()

Base.metadata.create_all(bind=engine)

def generate_id():
    return str(uuid.uuid4())

@router.post("/task")
def Create_task(task: TaskCreate , db: Session = Depends(get_db)):
    
    #Generate unique ID and timestamps for the new task
    task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        id=generate_id(),
        created_at=datetime.datetime.now().isoformat(),
        updated_at=datetime.datetime.now().isoformat()
    )

     #save new task to the database
    db.add(TaskModel(**task.model_dump()))
    db.commit()

    return JSONResponse(content={"message": "Task created successfully"}, status_code=201)

@router.get("/tasks")
def get_all_task(skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10), db: Session = Depends(get_db)):
    
    db_tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    tasks = {task.id: {
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    } for task in db_tasks}

    return JSONResponse(content=tasks, status_code=200)

@router.get("/task/{task_id}")
def get_task_by_ID(task_id:str, db: Session = Depends(get_db)):

    #Search for the task in the database
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')
    return db_task

@router.patch("/task/{task_id}")
def update_task(task_id: str,task_update:TaskUpdate, db: Session = Depends(get_db)):
    
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='No task with this ID found')

    updated_data = task_update.model_dump(exclude_unset=True)
    clean_data = {
        key: value for key, value in updated_data.items() if value is not None
    }

    # Apply update
    for key, value in clean_data.items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.datetime.now().isoformat()

    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/task/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
   
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')
    db.delete(db_task)
    db.commit()
    return JSONResponse(content={"message": "Task Deleted Succesfully"},status_code= 200)
    
@router.get("/tasks/filter")
def status_of_Task(filter: Annotated[str, Query(...,description="Enter Pending or Done")],skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10), db: Session = Depends(get_db)):
    
    db_tasks = db.query(TaskModel).all()
    
    if filter not in ['Pending', 'Done']:
        raise HTTPException(
            status_code=400,
            detail='Invalid filter value. Use "Pending" or "Done".'
        )

    filtered = {
        task.id: task
        for task in db_tasks
        if task.status == filter
        
    }

    paginated = list(filtered.items())[skip: skip + limit]
    result = {k: v for k, v in paginated}
    
    if not result:
        raise HTTPException(status_code=404, detail='No tasks found with the specified filter.')
    return result
     
@router.get("/tasks/search")
def search_tasks(query: str, skip: int = Query(0, ge=0), limit: int = Query(5, ge=5, le=10), db: Session = Depends(get_db)):

    db_tasks = db.query(TaskModel).all()
    filtered = {
        task.id: task
        for task in db_tasks
        if query.lower() in task.title.lower() or (task.description and query.lower() in task.description.lower())
    }

    paginated = list(filtered.items())[skip: skip + limit]
    result = {k: v for k, v in paginated}

    return result

@router.get("/tasks/sort")
def sort_tasks(by: Annotated[str, Query(..., description="Enter 'created_at' or 'updated_at'")], order: str = 'asc', skip: int = Query(0, ge=0), limit: int = Query(5, ge=5, le=10), db: Session = Depends(get_db)):

    db_tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    if by not in ['created_at', 'updated_at']:
        raise HTTPException(status_code=400, detail='Invalid sort field. Use "created_at" or "updated_at".')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid sort order. Use "asc" or "desc".')

    sorted_tasks = sorted(
        db_tasks,
        key=lambda 
        task: getattr(task, by),
        reverse=(order == 'desc')
    )
    
    paginated = sorted_tasks[skip: skip + limit]
    result = {task.id: task for task in paginated}

    return result


