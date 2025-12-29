from pydantic import BaseModel


class SkillsSchema(BaseModel):
    id: int
    title: str

class SkillCreateSchema(BaseModel):
    title: str
    