from src.utils.repository import SQLAlchemyRepository
from src.models.executer import Executer

class ExecuterRepository(SQLAlchemyRepository):

    entity = Executer
