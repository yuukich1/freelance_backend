from fastapi import APIRouter
from src.dependencies import UOWdep, UserDep, AdminDep
from src.schemas.executer import ExecuterCreateSchema
from src.service.executers import ExecuterService

router = APIRouter()

@router.post("/")
async def create_executer(executer_data: ExecuterCreateSchema, uow: UOWdep, user: UserDep):
    return await ExecuterService().add(uow, executer_data, user)

@router.get("/")
async def list_executers(uow: UOWdep):
    return await ExecuterService().get_executers(uow)
