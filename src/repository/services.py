from src.utils.repository import SQLAlchemyRepository
from src.models.services import Services


class ServicesRepository(SQLAlchemyRepository):
    
    entity = Services