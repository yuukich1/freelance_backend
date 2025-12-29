from src.utils.repository import SQLAlchemyRepository
from src.models.skills import Skills   

class SkillsRepository(SQLAlchemyRepository):

    entity = Skills