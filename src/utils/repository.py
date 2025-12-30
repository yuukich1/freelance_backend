from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert
from typing import List, Any, Optional, Type
from src.utils.models import Base

class AbstractRepository(ABC):

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    async def get(self, entity_id):
        pass

    @abstractmethod
    async def list(self):
        pass

    @abstractmethod
    async def remove(self, entity):
        pass

    @abstractmethod
    async def update(self, entity_id, **kwargs):
        pass


class SQLAlchemyRepository(AbstractRepository):

    entity: Type[Base]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: Any):
        stmt = insert(self.entity).values(**entity.__dict__).returning(self.entity)
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity.to_schema()
    
    async def get(self, **kwargs) -> Optional[Any]:
        stmt = select(self.entity).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity.to_schema() if entity else None

    async def list(self, **kwargs) -> List[Any]:
        stmt = select(self.entity).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return [entity.to_schema() for entity in result.scalars().all()]
    
    async def remove(self, entity):
        stmt = delete(self.entity).filter_by(id=entity.id)
        await self.session.execute(stmt)

    async def update(self, entity_id, **kwargs):
        stmt = update(self.entity).filter_by(id=entity_id).values(**kwargs).returning(self.entity)
        result = await self.session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity.to_schema() if entity else None