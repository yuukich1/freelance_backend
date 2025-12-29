from fastapi import APIRouter, Request
from src.schemas.services import ServiceCreateSchema, ServiceUpdateSchema, ServiceUpdateSchema
from src.dependencies import UOWdep, UserDep, AdminDep
from src.service.services import ServicesService
from src.config import limiter
from loguru import logger


router = APIRouter()

@router.post("/")
@limiter.limit('10/minutes')
async def create_service(request: Request, service_data: ServiceCreateSchema, uow: UOWdep, user: UserDep):
    logger.info(f"POST /api/services - Create service request from user_id={user.get('user_id')}")
    try:
        result = await ServicesService().add(uow, service_data, user)
        logger.info(f"Service created successfully by user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to create service for user_id={user.get('user_id')}: {e}")
        raise

@router.get("/")
@limiter.limit('100/minutes')
async def list_services(request: Request, uow: UOWdep):
    logger.info("GET /api/services - List all services request")
    try:
        result = await ServicesService().get_all_service(uow)
        logger.info(f"Retrieved {len(result) if result else 0} services")
        return result
    except Exception as e:
        logger.error(f"Failed to list services: {e}")
        raise

@router.get("/{service_id}")
@limiter.limit('100/minutes')
async def get_service(request: Request, service_id: int, uow: UOWdep):
    logger.info(f"GET /api/services/{service_id} - Get service request")
    try:
        result = await ServicesService().get_service(service_id, uow)
        logger.info(f"Service {service_id} retrieved successfully")
        return result
    except Exception as e:
        logger.warning(f"Service {service_id} not found: {e}")
        raise

@router.delete("/{service_id}")
@limiter.limit('10/minutes')
async def delete_service(request: Request, service_id: int, uow: UOWdep, user: UserDep):
    logger.info(f"DELETE /api/services/{service_id} - Delete service request from user_id={user.get('user_id')}")
    try:
        result = await ServicesService().delete_service(service_id, uow, user)
        logger.info(f"Service {service_id} deleted successfully by user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to delete service {service_id}: {e}")
        raise

@router.put("/{service_id}")
@limiter.limit('20/minutes')
async def update_service(request: Request, service_id: int, new_service_data: ServiceUpdateSchema, uow: UOWdep, user: UserDep):
    logger.info(f"PUT /api/services/{service_id} - Update service request from user_id={user.get('user_id')}")
    try:
        result = await ServicesService().update_service(service_id, new_service_data, uow, user)
        logger.info(f"Service {service_id} updated successfully by user_id={user.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to update service {service_id}: {e}")
        raise
