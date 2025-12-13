from src.utils.repository import SQLAlchemyRepository
from src.models.categories import Categories

class CategoriesRepository(SQLAlchemyRepository):

    entity = Categories