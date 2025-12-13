from pydantic import BaseModel
from fastapi import Form

class LoginSchema(BaseModel):
    username: str
    password: str