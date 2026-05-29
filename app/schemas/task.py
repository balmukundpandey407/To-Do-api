from pydantic import BaseModel, Field
from typing import Literal,Optional, Annotated
from datetime import datetime

class Task(BaseModel):
    id: str 
    title: Annotated[str, Field(..., max_length=100, title="Title of the task")]
    description: Annotated[Optional[str], Field(default=None, max_length=200, title="Description of the task")]
    status: Annotated[Literal['Done','Pending'], Field(title="Completion status of the task",default='Pending')]
    created_at: datetime
    updated_at: datetime
    owner_id: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Literal['Done','Pending'] = 'Pending'

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal['Done','Pending']] = None