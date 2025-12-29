from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class SkillsSchema(BaseModel):
    title: str
    experience: int

class ExecuterSchema(BaseModel):
    id: int
    user_id: int
    skills: List[SkillsSchema] = [] 
    created_at: datetime 

class ExecuterCreateSchema(BaseModel):
    user_id: Optional[int] = None
    skills: List[SkillsSchema] = []

class ExecuterDBSchema(BaseModel):
    user_id: int
    skills: dict

class ExecuterUserSchema(BaseModel):
    email: EmailStr
    username: str
    

class ExecuterResponseSchema(BaseModel):
    id: int
    user: ExecuterUserSchema
    skills: List[SkillsSchema]
    created_at: datetime