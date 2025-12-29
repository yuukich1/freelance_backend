from fastapi import APIRouter, Request
from src.dependencies import UOWdep, UserDep, AdminDep
from src.schemas.executer import ExecuterCreateSchema
from src.service.executers import ExecuterService
from src.config import limiter
from loguru import logger

router = APIRouter()

@router.post("/")
@limiter.limit('5/minutes')
async def create_executer(request: Request, executer_data: ExecuterCreateSchema, uow: UOWdep, user: UserDep):
    logger.info(f"POST /api/executers - Create executer request from user_id={user.get('user_id')}")
    try:
        result = await ExecuterService().add(uow, executer_data, user)
        logger.info(f"Executer created successfully for user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to create executer for user_id={user.get('user_id')}: {e}")
        raise

@router.get("/")
@limiter.limit('100/minutes')
async def list_executers(request: Request, uow: UOWdep):
    logger.info("GET /api/executers - List all executers request")
    try:
        result = await ExecuterService().get_executers(uow)
        logger.info(f"Retrieved {len(result) if result else 0} executers")
        return result
    except Exception as e:
        logger.error(f"Failed to list executers: {e}")
        raise
