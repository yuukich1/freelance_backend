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
    status: str


class ServiceCreateSchema(BaseModel):
    title: str
    description: str
    price: Decimal
    category_id: Optional[int] = None
    buyer_id: Optional[int] = None
    delivery_time: Optional[int] = None



class ServiceUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[int] = None
    delivery_time: Optional[int] = None
    status: Optional[str] = None