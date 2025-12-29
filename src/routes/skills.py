from fastapi import APIRouter
from src.dependencies import UOWdep
from src.service.skills import SkillsService

router = APIRouter()

@router.get("/")
async def list_skills(uow: UOWdep):
    return await SkillsService().get_all_skills(uow)
