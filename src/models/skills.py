from sqlalchemy.orm import Mapped, mapped_column
from src.utils.models import Base
from datetime import datetime
from sqlalchemy import DateTime
from src.schemas.skills import SkillsSchema

class Skills(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def to_schema(self):
        return SkillsSchema(
            id=self.id,
            title=self.title
        )