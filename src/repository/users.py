from src.models import Users
from src.utils.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):

    entity = Users
