from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ServicesSchema(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    category_id: Optional[int] = None
    buyer_id: int
    delivery_time: Optional[int] = None


