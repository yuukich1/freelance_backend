from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str
    is_active: bool
    role: str


class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool

