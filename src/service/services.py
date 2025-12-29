from src.utils.unit_of_work import IUnitOfWork
from src.schemas.services import ServiceCreateSchema, ServiceUpdateSchema
from fastapi import HTTPException
from loguru import logger


class ServicesService:

    async def add(self, uow: IUnitOfWork, service_data: ServiceCreateSchema, user: dict):
        logger.info("ServicesService.add called")
        async with uow:
            if service_data.buyer_id is None:
                service_data.buyer_id = user.get('user_id')
            logger.debug("Attempting to add service with data: {}", service_data)
            service = await uow.services.add(service_data)
            if service:
                await uow.commit()
                svc_id = getattr(service, 'id', None)
                logger.info("Service created successfully, id={}", svc_id)
                return service
            else:
                logger.exception("Service could not be created for data: {}", service_data)
                raise HTTPException(status_code=400, detail="Service could not be created")

    async def get_all_service(self, uow: IUnitOfWork):
        async with uow:
            return await uow.services.list()
        
    async def get_service(self, service_id: int, uow: IUnitOfWork):
        async with uow: 
            service = await uow.services.get(id=service_id)
            if not service:
                raise HTTPException(status_code=404)
            return service
    
    async def delete_service(self, service_id: int, uow: IUnitOfWork, user: dict):
        async with uow:
            service = await self.get_service(service_id=service_id, uow=uow)
            if not (service.buyer_id == user.get('user_id') or user.get('role') == 'admin'):
                raise HTTPException(status_code=403)
            try:
                await uow.services.remove(service)
                await uow.commit()
                return {'status': 'success'}
            except:
                raise HTTPException(status_code=409)
            
    async def update_service(self, service_id: int, new_service_data: ServiceUpdateSchema, uow: IUnitOfWork, user: dict):
        async with uow:
            service = await self.get_service(service_id=service_id, uow=uow)
            if not (service.buyer_id == user.get('user_id') or user.get('role') == 'admin'):
                raise HTTPException(status_code=403)
            update_data = {} 
            for k in new_service_data.dict().keys():
                if new_service_data.dict().get(k):
                    update_data[k] = new_service_data.dict().get(k)
            updated_service = await uow.services.update(service_id, **update_data)
            await uow.commit()
            if not updated_service:
                raise HTTPException(status_code=404)
            return updated_service
    
