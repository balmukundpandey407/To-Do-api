from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal,Optional, Annotated
import json
import random
import datetime
import uuid

app = FastAPI()

class Task(BaseModel):
    id: str 
    title: Annotated[str, Field(..., max_length=100, title="Title of the task")]
    description: Annotated[Optional[str], Field(default=None, max_length=200, title="Description of the task")]
    completion: Annotated[Literal['Done','Pending'], Field(title="Completion status of the task",default='Pending')]
    created_at: str
    updated_at: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completion: Literal['Done','Pending'] = 'Pending'

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completion: Optional[Literal['Done','Pending']] = None

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data,f , indent=4)

def generate_id():
    return str(uuid.uuid4())

@app.get("/")
def home():
    return JSONResponse(content={"message": "TO DO API IS WORKING PROPERLY"}, status_code=200)

@app.post("/task")
def Create_task(task: TaskCreate):
    #Load existing data
    data = load_data()
    #Generate unique ID and timestamps for the new task
    task = Task(
        title=task.title,
        description=task.description,
        completion=task.completion,
        id=generate_id(),
        created_at=datetime.datetime.now().isoformat(),
        updated_at=datetime.datetime.now().isoformat()
    )
    #Add new task to the data
    data[task.id]=task.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(content={"message": "Task created successfully"}, status_code=201)

@app.get("/tasks")
def get_all_task(skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10)):
    #Load existing data
    data = load_data()
    #Apply pagination
    paginated_data = list(data.items())[skip:skip+limit]
    return JSONResponse(content=dict(paginated_data), status_code=200)

@app.get("/task/{task_id}")
def get_task_by_ID(task_id:str):
    #Load existing data
    data = load_data()

    if task_id not in data:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')
    return JSONResponse(content= data[task_id], status_code= 200)

@app.patch("/task/{task_id}")
def update_task(task_id: str,task_update:TaskUpdate):
    #Load existing data
    data = load_data()
    
    if task_id not in data:
      raise HTTPException(status_code=404, detail='No task with this ID found')

    update_data = task_update.model_dump(exclude_unset=True)
    existing = data[task_id]
    clean_data = {
    k: v for k, v in update_data.items()
    if v is not None and v != "string"
    }

    # apply update
    existing.update(clean_data)
    existing["updated_at"] = datetime.datetime.now().isoformat()

    data[task_id] = existing
    save_data(data)

    return JSONResponse(content=existing, status_code=200)

@app.delete("/task/{task_id}")
def delete_task(task_id: str):
     #Load existing data
    data = load_data()

    if task_id not in data:
        raise HTTPException(status_code=404, detail ='No task with task ID Found')
    del data[task_id]
    save_data(data)
    return JSONResponse(content={"message": "Task Deleted Succesfully"},status_code= 200)
    
@app.get("/tasks/filter")
def completed_Task(filter: str,skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10)):
    #Load Data
    data = load_data()
    
    if filter not in ['Pending', 'Done']:
        raise HTTPException(
            status_code=400,
            detail='Invalid filter value. Use "Pending" or "Done".'
        )

    filtered = {
        task_id: task
        for task_id, task in data.items()
        if task['completion'] == filter
        
    }

    paginated = list(filtered.items())[skip: skip + limit]
    result = {k: v for k, v in paginated}

    return JSONResponse(content=result, status_code=200)
     
@app.get("/tasks/search")
def search_tasks(query: str,skip:int= Query(0, ge=0),limit:int= Query(5, ge=5, le=10)):
    #Load Data
    data = load_data()

    filtered = {
        task_id: task
        for task_id, task in data.items()
        if query.lower() in task['title'].lower() or (task['description'] and query.lower() in task['description'].lower())
    }
    
    paginated = list(filtered.items())[skip: skip + limit]
    result = {k: v for k, v in paginated}

    return JSONResponse(content=result, status_code=200)

@app.get("/tasks/sort")
def sort_tasks(by: str, order: str = 'asc', skip: int = Query(0, ge=0), limit: int = Query(5, ge=5, le=10)):
    #Load Data
    data = load_data()

    if by not in ['created_at', 'updated_at']:
        raise HTTPException(status_code=400, detail='Invalid sort field. Use "created_at" or "updated_at".')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid sort order. Use "asc" or "desc".')

    sorted_tasks = sorted(
        data.items(),
        key=lambda item: item[1][by],
        reverse=(order == 'desc')
    )

    paginated = sorted_tasks[skip: skip + limit]
    result = {k: v for k, v in paginated}

    return JSONResponse(content=result, status_code=200)

