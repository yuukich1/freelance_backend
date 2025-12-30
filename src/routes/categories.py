from fastapi import APIRouter, Depends, Request
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema
from src.service.categories import CategoriesService
from src.service.auth import AuthService
from src.dependencies import UOWdep, UserDep, AdminDep
from fastapi_cache.decorator import cache
from src.config import limiter
from loguru import logger


router = APIRouter()

@router.post('/')
@limiter.limit('10/minute')
async def create_category(request: Request, new_category: CategoryCreateSchema, uow: UOWdep, admin: AdminDep):
    logger.info(f"POST /api/categories - Create category request from admin user_id={admin.get('user_id')}")
    try:
        result = await CategoriesService().create_category(new_category, uow)
        logger.info(f"Category created successfully by admin user_id={admin.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to create category: {e}")
        raise

@router.get('/')
@cache(expire=60*60)
@limiter.limit('60/minute')
async def get_all_categories(request: Request, uow: UOWdep):
    logger.info("GET /api/categories - List all categories request")
    try:
        result = await CategoriesService().get_all_categories(uow)
        logger.info(f"Retrieved {len(result) if result else 0} categories")
        return result
    except Exception as e:
        logger.error(f"Failed to list categories: {e}")
        raise

@router.get('/{category_id}')
@limiter.limit('120/minute')
async def get_category_by_id(request: Request, category_id: int, uow: UOWdep):
    logger.info(f"GET /api/categories/{category_id} - Get category request")
    try:
        result = await CategoriesService().get_category(category_id, uow)
        logger.info(f"Category {category_id} retrieved successfully")
        return result
    except Exception as e:
        logger.warning(f"Category {category_id} not found: {e}")
        raise

@router.put('/{category_id}')
@limiter.limit('30/minute')
async def update_category(request: Request, category_id: int, update_category: CategoryUpdateSchema, uow: UOWdep, admin: AdminDep):
    logger.info(f"PUT /api/categories/{category_id} - Update category request from admin user_id={admin.get('user_id')}")
    try:
        result = await CategoriesService().update_category(category_id, update_category, uow)
        logger.info(f"Category {category_id} updated successfully by admin user_id={admin.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to update category {category_id}: {e}")
        raise

@router.delete('/{category_id}')
@limiter.limit('30/minute')
async def delete_category(request: Request, category_id: int, uow: UOWdep, admin: AdminDep):
    logger.info(f"DELETE /api/categories/{category_id} - Delete category request from admin user_id={admin.get('user_id')}")
    try:
        result = await CategoriesService().delete_category(category_id, uow)
        logger.info(f"Category {category_id} deleted successfully by admin user_id={admin.get('user_id')}")
        return result
    except Exception as e:
        logger.error(f"Failed to delete category {category_id}: {e}")
        raise


