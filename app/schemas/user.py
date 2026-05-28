from pydantic import BaseModel, EmailStr, Field
from typing import Union, Annotated,Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)

class Userout(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr

class Userupdate(BaseModel):
    id: str
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Optional[str] = Field(default=None, min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserToken(BaseModel):
    token: str  