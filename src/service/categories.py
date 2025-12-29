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
        logger.info("CategoriesService.get_all_categories called")
        async with uow:
            categories = await uow.categories.list()
            logger.info(f"Retrieved {len(categories) if categories else 0} categories from database")
            return categories
        
    
    async def get_category(self, category_id: int, uow: IUnitOfWork):
        logger.info(f"CategoriesService.get_category called for category_id={category_id}")
        async with uow: 
            category = await uow.categories.get(id=category_id)
            if not category:
                logger.warning(f"Category {category_id} not found")
                raise HTTPException(status_code=404)
            logger.debug(f"Category {category_id} retrieved successfully")
            return category
        
    
    async def delete_category(self, category_id: int, uow: IUnitOfWork):
        logger.info(f"CategoriesService.delete_category called for category_id={category_id}")
        async with uow:
            category = await self.get_category(category_id=category_id, uow=uow)
            try:
                await uow.categories.remove(category)
                await uow.commit()
                logger.info(f"Category {category_id} deleted successfully")
                return {'status': 'success'}
            except Exception as e:
                logger.exception(f"Failed to delete category {category_id}: {e}")
                raise HTTPException(status_code=409)
            
    async def update_category(self, category_id: int, new_category_data: CategoryUpdateSchema, uow: IUnitOfWork):
        logger.info(f"CategoriesService.update_category called for category_id={category_id}")
        async with uow:
            update_data = {} 
            for k in new_category_data.dict().keys():
                if new_category_data.dict().get(k):
                    update_data[k] = new_category_data.dict().get(k)
            logger.debug(f"Updating category {category_id} with data: {update_data}")
            updated_category = await uow.categories.update(category_id, **update_data)
            await uow.commit()
            if not updated_category:
                logger.warning(f"Category {category_id} update failed - category not found after update")
                raise HTTPException(status_code=404)
            logger.info(f"Category {category_id} updated successfully")
            return updated_category
            

    
