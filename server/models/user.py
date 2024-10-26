from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str
    