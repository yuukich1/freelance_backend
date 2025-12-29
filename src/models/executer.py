from sqlalchemy.orm import Mapped, mapped_column
from src.utils.models import Base
from src.schemas.executer import ExecuterSchema, SkillsSchema
from datetime import datetime
from sqlalchemy import DateTime, JSON


class Executer(Base):

    __tablename__ = 'executers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    skills: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def to_schema(self):
        return ExecuterSchema(
            id=self.id,
            user_id=self.user_id,
            skills=[
                SkillsSchema(title=key, experience=value) 
                for key, value in self.skills.items()
            ],
            created_at=self.created_at
        )
    