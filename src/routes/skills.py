from fastapi import APIRouter, Request
from src.dependencies import UOWdep
from src.service.skills import SkillsService
from src.config import limiter
from loguru import logger

router = APIRouter()

@router.get("/")
@limiter.limit('100/minutes')
async def list_skills(request: Request, uow: UOWdep):
    logger.info("GET /api/skills - List all skills request")
    try:
        result = await SkillsService().get_all_skills(uow)
        logger.info(f"Retrieved {len(result) if result else 0} skills")
        return result
    except Exception as e:
        logger.error(f"Failed to list skills: {e}")
        raise
