from fastapi import APIRouter, Depends, Request
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema
from src.service.categories import CategoriesService
from src.service.auth import AuthService
from src.dependencies import UOWdep, UserDep, AdminDep
from fastapi_cache.decorator import cache
from src.config import limiter


router = APIRouter()

@router.post('/')
@limiter.limit('10/minutes')
async def create_category(request: Request, new_category: CategoryCreateSchema, uow: UOWdep, admin: AdminDep):
    return await CategoriesService().create_category(new_category, uow)

@router.get('/')
@cache(expire=60*60)
@limiter.limit('100/minutes')
async def get_all_categories(request: Request, uow: UOWdep):
    return await CategoriesService().get_all_categories(uow)

@router.get('/{category_id}')
@limiter.limit('100/minutes')
async def get_category_by_id(request: Request, category_id: int, uow: UOWdep):
    return await CategoriesService().get_category(category_id, uow)

@router.put('/{category_id}')
@limiter.limit('10/minutes')
async def update_category(request: Request, category_id: int, update_category: CategoryUpdateSchema, uow: UOWdep, admin: AdminDep):
    return await CategoriesService().update_category(category_id, update_category, uow)

@router.delete('/{category_id}')
@limiter.limit('10/minutes')
async def delete_category(request: Request, category_id: int, uow: UOWdep, admin: AdminDep):
    return await CategoriesService().delete_category(category_id, uow)


