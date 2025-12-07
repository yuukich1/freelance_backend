from fastapi import APIRouter
from src.dependencies import UOWdep
from src.schemas.user import UserCreateSchema, UserResponseSchema
from src.service.auth import AuthService

router = APIRouter()

@router.post("/register")
async def register_user(user_create: UserCreateSchema, uow: UOWdep):
    user = await AuthService().create_user(user_create, uow)
    return user