
from typing import List
from src.utils.unit_of_work import IUnitOfWork
from src.schemas.skills import SkillsSchema
from loguru import logger


class SkillsService:
    

    async def get_all_skills(self, uow: IUnitOfWork) -> List[SkillsSchema]:
        logger.info("SkillsService.get_all_skills called")
        async with uow:
            skills = await uow.skills.list()
            logger.info(f"Retrieved {len(skills) if skills else 0} skills from database")
            return skills
        