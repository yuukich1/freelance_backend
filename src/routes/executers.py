from fastapi import APIRouter, Path, Query, Request
from fastapi_cache.decorator import cache
from src.dependencies import UOWdep, UserDep
from src.schemas.executer import ExecuterCreateSchema, ExecuterUpdateSchema, ExecuterFilters
from src.service.executers import ExecuterService
from src.config import limiter
from loguru import logger

router = APIRouter()

@router.post("/")
@limiter.limit('10/minute')
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
@limiter.limit('60/minute')
async def list_executers(request: Request, uow: UOWdep, filters: ExecuterFilters = Query(...)):
    logger.info("GET /api/executers - List all executers request")
    try:
        result = await ExecuterService().get_executers(uow, filters.dict(exclude_none=True))
        logger.info(f"Retrieved {len(result) if result else 0} executers")
        return result
    except Exception as e:
        logger.error(f"Failed to list executers: {e}")
        raise


@router.get('/me')
async def get_my_executer(request: Request, uow: UOWdep, user: UserDep):
    logger.info(f"GET /api/executers/me - Get my executer request from user_id={user.get('user_id')}")
    try:
        result = await ExecuterService().get_by_user(uow, user)
        logger.info(f"Retrieved my executer for user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to get my executer for user_id={user.get('user_id')}: {e}")
        raise


@router.get("/{executer_id}")
@cache(expire=30)
@limiter.limit('120/minute')
async def get_executer(request: Request, executer_id: int, uow: UOWdep):
    logger.info(f"GET /api/executers/{executer_id} - Get executer by ID request")
    try:
        result = await ExecuterService().get_by_executer_id(uow, executer_id)
        logger.info(f"Retrieved executer with id={executer_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to get executer with id={executer_id}: {e}")
        raise


@router.delete("/{executer_id}")
@limiter.limit('30/minute')
async def delete_executer(request: Request, executer_id: int, uow: UOWdep, user: UserDep):
    logger.info(f"DELETE /api/executers/{executer_id} - Delete executer request from user_id={user.get('user_id')}")
    try:
        result = await ExecuterService().delete(uow, executer_id, user)
        logger.info(f"Executer with id={executer_id} deleted successfully by user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to delete executer with id={executer_id} by user_id={user.get('user_id')}: {e}")
        raise

@router.put("/{executer_id}")
@limiter.limit('30/minute')
async def update_executer(request: Request, executer_data: ExecuterUpdateSchema, uow: UOWdep, user: UserDep, executer_id: int = Path(description='-1 if the user updates their profile')):
    logger.info(f"PUT /api/executers/{executer_id} - Update executer request from user_id={user.get('user_id')}")
    try:
        result = await ExecuterService().update(uow, executer_data, user, executer_id)
        logger.info(f"Executer with id={executer_id} updated successfully by user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to update executer with id={executer_id} by user_id={user.get('user_id')}: {e}")
        raise