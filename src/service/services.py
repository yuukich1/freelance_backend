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
        logger.info("ServicesService.get_all_service called")
        async with uow:
            services = await uow.services.list()
            logger.info(f"Retrieved {len(services) if services else 0} services from database")
            return services
        
    async def get_service(self, service_id: int, uow: IUnitOfWork):
        logger.info(f"ServicesService.get_service called for service_id={service_id}")
        async with uow: 
            service = await uow.services.get(id=service_id)
            if not service:
                logger.warning(f"Service {service_id} not found")
                raise HTTPException(status_code=404)
            logger.debug(f"Service {service_id} retrieved successfully")
            return service
    
    async def delete_service(self, service_id: int, uow: IUnitOfWork, user: dict):
        logger.info(f"ServicesService.delete_service called for service_id={service_id} by user_id={user.get('user_id')}")
        async with uow:
            service = await self.get_service(service_id=service_id, uow=uow)
            if not (service.buyer_id == user.get('user_id') or user.get('role') == 'admin'):
                logger.warning(f"Access denied: user_id={user.get('user_id')} attempted to delete service_id={service_id}")
                raise HTTPException(status_code=403)
            try:
                await uow.services.remove(service)
                await uow.commit()
                logger.info(f"Service {service_id} deleted successfully by user_id={user.get('user_id')}")
                return {'status': 'success'}
            except Exception as e:
                logger.exception(f"Failed to delete service {service_id}: {e}")
                raise HTTPException(status_code=409)
            
    async def update_service(self, service_id: int, new_service_data: ServiceUpdateSchema, uow: IUnitOfWork, user: dict):
        logger.info(f"ServicesService.update_service called for service_id={service_id} by user_id={user.get('user_id')}")
        async with uow:
            service = await self.get_service(service_id=service_id, uow=uow)
            if not (service.buyer_id == user.get('user_id') or user.get('role') == 'admin'):
                logger.warning(f"Access denied: user_id={user.get('user_id')} attempted to update service_id={service_id}")
                raise HTTPException(status_code=403)
            update_data = {} 
            for k in new_service_data.dict().keys():
                if new_service_data.dict().get(k):
                    update_data[k] = new_service_data.dict().get(k)
            logger.debug(f"Updating service {service_id} with data: {update_data}")
            updated_service = await uow.services.update(service_id, **update_data)
            await uow.commit()
            if not updated_service:
                logger.warning(f"Service {service_id} update failed - service not found after update")
                raise HTTPException(status_code=404)
            logger.info(f"Service {service_id} updated successfully by user_id={user.get('user_id')}")
            return updated_service
    
