from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None


class CategoryCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None


class CategoryUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None