from fastapi import APIRouter, Form, Request
from src.dependencies import UOWdep
from src.schemas.user import UserCreateSchema, UserResponseSchema
from src.schemas.auth import LoginSchema
from src.service.auth import AuthService
from src.config import limiter


router = APIRouter()


@router.post("/register")
@limiter.limit('5/minutes')
async def register_user(request: Request, user_create: UserCreateSchema, uow: UOWdep):
    user = await AuthService().create_user(user_create, uow)
    return user

@router.get('/activate')
async def activate_user(activation_token: str, uow: UOWdep):
    return await AuthService().activate_user(activation_token, uow)


@router.post('/login')
@limiter.limit('5/minutes')
async def login_user(request: Request, uow: UOWdep, username: str = Form(...), password: str = Form(...)):

    access_token, refresh_token = await AuthService().login(LoginSchema(username=username, password=password), uow=uow)
    return {'access_token': access_token,
            'refresh_token': refresh_token,
            'type': 'bearer'}


