from fastapi import APIRouter
from src.schemas.services import ServiceCreateSchema, ServiceUpdateSchema, ServiceUpdateSchema
from src.dependencies import UOWdep, UserDep, AdminDep
from src.service.services import ServicesService


router = APIRouter()

@router.post("/")
async def create_service(service_data: ServiceCreateSchema, uow: UOWdep, user: UserDep):
    return await ServicesService().add(uow, service_data, user)

@router.get("/")
async def list_services(uow: UOWdep):
    return await ServicesService().get_all_service(uow)

@router.get("/{service_id}")
async def get_service(service_id: int, uow: UOWdep):
    return await ServicesService().get_service(service_id, uow)

@router.delete("/{service_id}")
async def delete_service(service_id: int, uow: UOWdep, user: UserDep):
    return await ServicesService().delete_service(service_id, uow, user)

@router.put("/{service_id}")
async def update_service(service_id: int, new_service_data: ServiceUpdateSchema, uow: UOWdep, user: UserDep):
    return await ServicesService().update_service(service_id, new_service_data, uow, user)
