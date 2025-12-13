from fastapi import APIRouter, Depends
from src.schemas.categories import CategoryCreateSchema
from src.service.categories import CategoriesService
from src.service.auth import AuthService
from src.dependencies import UOWdep
from fastapi_cache.decorator import cache

router = APIRouter()

@router.post('/')
async def create_category(new_category: CategoryCreateSchema, uow: UOWdep, user = Depends(AuthService.get_user_by_jwt)):
    return await CategoriesService().create_category(new_category, uow)



@router.get('/')
@cache(expire=60*60*24)
async def get_all_categories(uow: UOWdep):
    return await CategoriesService().get_all_categories(uow)