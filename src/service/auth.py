from src.utils.unit_of_work import IUnitOfWork
from src.schemas.user import *
from src.config import pwd_context
from loguru import logger
from fastapi import HTTPException, status


class AuthService():

    async def create_user(self, user_create: UserCreateSchema, uow: IUnitOfWork) -> dict:
        async with uow:
            hashed_password = pwd_context.hash(user_create.password)
            try:
                user = await uow.users.add(
                    UserCreateSchema(
                        username=user_create.username,
                        email=user_create.email,
                        password=hashed_password
                    )
                )
                await uow.commit()
                logger.info(f"User created with ID: {user.id}")
                return {'status': 'success'}
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email or username already exists."
                )

    
            
    