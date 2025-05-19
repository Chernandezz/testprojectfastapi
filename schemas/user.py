from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
  name:str
  email: EmailStr
  password: str

class UserUpdate(BaseModel):
  name: Optional[str] = None
  email: Optional[str] = None
  password: Optional[str] = None

class User(BaseModel):
  id: str
  name: str
  email: EmailStr