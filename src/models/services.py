from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, DateTime, ForeignKey, Text
from src.utils.models import Base
from src.schemas.services import ServicesSchema

class Services(Base):

    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False,index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    delivery_time: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default='Pending')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def to_schema(self):
        return ServicesSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price,
            category_id=self.category_id,
            buyer_id=self.buyer_id,
            delivery_time=self.delivery_time,
            status=self.status
        )


