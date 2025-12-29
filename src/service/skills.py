
from typing import List
from src.utils.unit_of_work import IUnitOfWork
from src.schemas.skills import SkillsSchema


class SkillsService:
    

    async def get_all_skills(self, uow: IUnitOfWork) -> List[SkillsSchema]:
        async with uow:
            skills = await uow.skills.list()
            return skills
        