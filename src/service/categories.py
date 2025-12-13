from src.utils.unit_of_work import IUnitOfWork
from schemas.categories import CategoryCreateSchema
from fastapi import HTTPException
from loguru import logger

class CategoriesService:

    async def create_category(self, new_category: CategoryCreateSchema, uow: IUnitOfWork):
        async with uow:
            try:
                category = await uow.categories.add(new_category)
                await uow.commit()
                logger.info(f"Category created successfully: {category}")
                return {
                    'message': 'success',
                    'category': category
                }
            except Exception:
                logger.exception(f"Failed to create category")
                raise HTTPException(status_code=409, detail='Cannot category created')
            
    async def get_all_categories(self, uow: IUnitOfWork):
        async with uow:
            return await uow.categories.list()
    
