from sqlalchemy.orm import Mapped, mapped_column
from src.utils.models import Base
from src.schemas.categories import CategorySchema

class Categories(Base):

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    description: Mapped[str]

    def to_schema(self):
        return CategorySchema(
            id=self.id,
            title=self.title,
            description=self.description
        )