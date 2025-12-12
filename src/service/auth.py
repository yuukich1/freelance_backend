from datetime import datetime
from src.utils.unit_of_work import IUnitOfWork
from src.schemas.user import *
from src.schemas.auth import LoginSchema
from src.config import pwd_context, SecurityConfig
from loguru import logger
from fastapi import HTTPException, status
from src.workers.tasks import send_welcome_email_task
from jwt import PyJWT


class AuthService:

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
                logger.info(f"Sending welcome email task to {user_create.email}")
                task = send_welcome_email_task.delay(to_email=user_create.email, username=user_create.username, action_url=f'{SecurityConfig.activation_url}?activation_token={await self.generate_activation_jwt(user)}')
                logger.info(task)
                return {'status': 'success'}
            except Exception as e:
                logger.exception(f"Error creating user: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email or username already exists."
                )
            
    async def activate_user(self, activation_token: str, uow: IUnitOfWork):
        async with uow: 
            data = await self.__decode_activation_jwt(activation_token)
            user = await uow.users.get(username=data.get('username'))
            if not user: raise HTTPException(status_code=404)
            user_update = await uow.users.update(user.id, is_active=True)
            if user_update:
                await uow.commit()
                return {'status': 'success'}
            raise HTTPException(status_code=409)
             

    async def login(self, user_login: LoginSchema, uow: IUnitOfWork):
        async with uow:
            user = await uow.users.get(username=user_login.username)
            if not user: raise HTTPException(status_code=400, detail='invalid credetials')
            # returning access_token, refresh_token
            return await self.generate_access_jwt(user), await self.generate_refresh_jwt(user)


    def _create_payload(self, user: UserSchema, expires):
        payload = {
            "exp": expires,
            "username": user.username,
            "role": user.role,
        }
        return payload

    def _encode_jwt(self, payload: dict, key):
        return PyJWT().encode(payload=payload, key=key, algorithm=SecurityConfig.algorithm)

    def expires_time(self, expires):
        expire_time = datetime.utcnow() + expires
        logger.debug(f"Expire timestamp: {int(expire_time.timestamp())}")
        logger.debug(f"Current utc timestamp: {int(datetime.utcnow().timestamp())}")
        return expire_time


    async def generate_access_jwt(self, user: UserSchema):
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp))
        return self._encode_jwt(payload, SecurityConfig.secret_key)

    async def generate_refresh_jwt(self, user: UserSchema):
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp_refresh))
        return self._encode_jwt(payload, SecurityConfig.secret_key)

    async def generate_activation_jwt(self, user: UserSchema):
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp_activation))
        return self._encode_jwt(payload, SecurityConfig.activation_secret)
    
    async def _decode_jwt(self, token: str):
        try:
            data = PyJWT().decode(token, key=SecurityConfig.secret_key, algorithms=[SecurityConfig.algorithm])
            if not data: raise HTTPException(status_code=401)
            return data
        except:
            raise HTTPException(status_code=401)
        
    async def __decode_activation_jwt(self, activation_token: str):
        try:
            data = PyJWT().decode(activation_token, key=SecurityConfig.activation_secret, algorithms=[SecurityConfig.algorithm])
            if not data: raise HTTPException(status_code=401)
            return data
        except:
            logger.exception('error decode activation token')
            raise HTTPException(status_code=401)


