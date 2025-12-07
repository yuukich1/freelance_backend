from abc import ABC, abstractmethod
from typing import Type
from src.repository import *
from src.connect import async_session_maker 

class IUnitOfWork(ABC):

    users: UserRepository

    @abstractmethod
    async def __aenter__(self):
        return NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return NotImplementedError
    
    @abstractmethod
    async def commit(self):
        return NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        return NotImplementedError
    

class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()