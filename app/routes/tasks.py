from fastapi import FastAPI, HTTPException, Query, APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
import json
import datetime
import uuid
from app.schemas.task import TaskCreate, Task, TaskUpdate
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.task import Base, Task as TaskModel
from app.routes.auth import get_current_user

task_router = APIRouter()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def generate_id():
    return str(uuid.uuid4())

@task_router.post("/task")
def create_task(task: TaskCreate , db: Session = Depends(get_db),current_user= Depends(get_current_user)):

    #Generate unique ID and timestamps for the new task
    task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        id=generate_id(),
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        owner_id = current_user.id
    )

     #save new task to the database
    db.add(TaskModel(**task.model_dump()))
    db.commit()

    return JSONResponse(content={"message": "Task created successfully"}, status_code=201)

@task_router.get("/tasks", response_model=list[TaskCreate])
def get_all_task(skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10), db: Session = Depends(get_db),current_user= Depends(get_current_user)):
     
    db_tasks = db.query(TaskModel).filter(TaskModel.owner_id == current_user.id).offset(skip).limit(limit).all()
    return db_tasks

@task_router.get("/task/{task_id}", response_model=TaskCreate)
def get_task_by_ID(task_id:str, db: Session = Depends(get_db),current_user= Depends(get_current_user)):
     
    #Search for the task in the database
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).filter(TaskModel.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')   
    return db_task

@task_router.patch("/task/{task_id}", response_model=TaskCreate)
def update_task(task_id: str,task_update:TaskUpdate, db: Session = Depends(get_db),current_user= Depends(get_current_user)):
    
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).filter(TaskModel.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='No task with this ID found')

    updated_data = task_update.model_dump(exclude_unset=True)

    clean_data = {
        key: value for key, value in updated_data.items() if value is not None
    }

    # Apply update
    for key, value in clean_data.items():
        setattr(db_task, key, value)
    db_task.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.delete("/task/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db),current_user= Depends(get_current_user)):
   
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).filter(TaskModel.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')
    db.delete(db_task)
    db.commit()
    return JSONResponse(content={"message": "Task Deleted Succesfully"},status_code= 200)
    
@task_router.get("/tasks/filter", response_model=list[TaskCreate])
def status_of_Task(filter: Annotated[str, Query(...,description="Enter Pending or Done")],skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10), db: Session = Depends(get_db),current_user= Depends(get_current_user)):
    

    if filter not in ['Pending', 'Done']:
        raise HTTPException(
            status_code=400,
            detail='Invalid filter value. Use "Pending" or "Done".'
        )
    
    db_tasks = db.query(TaskModel).filter(TaskModel.status == filter).filter(TaskModel.owner_id == current_user.id).all()

    paginated = list(db_tasks)[skip: skip + limit]
    
    if not paginated:
        raise HTTPException(status_code=404, detail='No tasks found with the specified filter.')
    return paginated
     
@task_router.get("/tasks/search", response_model=list[TaskCreate])
def search_tasks(query: str, skip: int = Query(0, ge=0), limit: int = Query(5, ge=5, le=10), db: Session = Depends(get_db),current_user= Depends(get_current_user)):
    
    db_tasks = db.query(TaskModel).filter(
        TaskModel.title.ilike(f'%{query}%') | TaskModel.description.ilike(f'%{query}%')
    ).filter(TaskModel.owner_id == current_user.id).all()
    
    paginated = list(db_tasks)[skip: skip + limit]
    if not paginated:
        raise HTTPException(status_code=404, detail='No tasks found with the specified query.')
    return paginated

@task_router.get("/tasks/sort", response_model=list[TaskCreate])
def sort_tasks(by: Annotated[str, Query(..., description="Enter 'created_at' or 'updated_at'")], order: str = 'asc', skip: int = Query(0, ge=0), limit: int = Query(5, ge=5, le=10), db: Session = Depends(get_db),current_user= Depends(get_current_user)):

    if by not in ['created_at', 'updated_at']:
        raise HTTPException(status_code=400, detail='Invalid sort field. Use "created_at" or "updated_at".')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid sort order. Use "asc" or "desc".')

    db_tasks = db.query(TaskModel).filter(TaskModel.owner_id == current_user.id).order_by(getattr(TaskModel, by).asc() if order == 'asc' else getattr(TaskModel, by).desc()).all()
    
    paginated = list(db_tasks)[skip: skip + limit]
    if not paginated:
        raise HTTPException(status_code=404, detail='No tasks found to sort.')
    return paginated


