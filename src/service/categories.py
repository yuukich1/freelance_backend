from src.utils.unit_of_work import IUnitOfWork
from src.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema
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
        
    
    async def get_category(self, category_id: int, uow: IUnitOfWork):
        async with uow: 
            category = await uow.categories.get(id=category_id)
            if not category:
                raise HTTPException(status_code=404)
            return category
        
    
    async def delete_category(self, category_id: int, uow: IUnitOfWork):
        async with uow:
            category = await self.get_category(category_id=category_id, uow=uow)
            try:
                await uow.categories.remove(category)
                await uow.commit()
                return {'status': 'success'}
            except:
                raise HTTPException(status_code=409)
            
    async def update_category(self, category_id: int, new_category_data: CategoryUpdateSchema, uow: IUnitOfWork):
        async with uow:
            update_data = {} 
            for k in new_category_data.dict().keys():
                if new_category_data.dict().get(k):
                    update_data[k] = new_category_data.dict().get(k)
            updated_category = await uow.categories.update(category_id, **update_data)
            await uow.commit()
            if not updated_category:
                raise HTTPException(status_code=404)
            return updated_category
            

    
