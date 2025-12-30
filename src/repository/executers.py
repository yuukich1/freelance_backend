from sqlalchemy import func, and_, select
from src.utils.repository import SQLAlchemyRepository
from src.models.executer import Executer

class ExecuterRepository(SQLAlchemyRepository):

    entity = Executer

    async def get_by_skills(self, skills: list):
        conditions = [
            func.json_extract(self.entity.skills, f'$.{skill}').isnot(None) # type: ignore
            for skill in skills
        ]

        stmt = select(self.entity).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return [entity.to_schema() for entity in result.scalars().all()]