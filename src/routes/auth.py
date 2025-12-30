from fastapi import APIRouter, Form, Request
from src.dependencies import UOWdep
from src.schemas.user import UserCreateSchema
from src.schemas.auth import LoginSchema
from src.service.auth import AuthService
from src.config import limiter
from loguru import logger


router = APIRouter()


@router.post("/register")
@limiter.limit('5/minute')
async def register_user(request: Request, user_create: UserCreateSchema, uow: UOWdep):
    logger.info(f"POST /api/auth/register - Registration request for username='{user_create.username}', email='{user_create.email}'")
    try:
        user = await AuthService().create_user(user_create, uow)
        logger.info(f"Registration successful for username='{user_create.username}'")
        return user
    except Exception as e:
        logger.error(f"Registration failed for username='{user_create.username}': {e}")
        raise

@router.get('/activate')
@limiter.limit('10/minute')
async def activate_user(request: Request, activation_token: str, uow: UOWdep):
    logger.info("GET /api/auth/activate - User activation request")
    try:
        result = await AuthService().activate_user(activation_token, uow)
        logger.info("User activation successful")
        return result
    except Exception as e:
        logger.warning(f"User activation failed: {e}")
        raise


@router.post('/login')
@limiter.limit('10/minute')
async def login_user(request: Request, uow: UOWdep, username: str = Form(...), password: str = Form(...)):
    logger.info(f"POST /api/auth/login - Login attempt for username='{username}'")
    try:
        access_token, refresh_token = await AuthService().login(LoginSchema(username=username, password=password), uow=uow)
        logger.info(f"Login successful for username='{username}'")
        return {'access_token': access_token,
                'refresh_token': refresh_token,
                'type': 'bearer'}
    except Exception as e:
        logger.warning(f"Login failed for username='{username}': {e}")
        raise


