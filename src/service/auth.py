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
        logger.info(f"create_user called for username='{user_create.username}', email='{user_create.email}'")
        async with uow:
            hashed_password = pwd_context.hash(user_create.password)
            logger.debug(f"Password hashed for username='{user_create.username}' (value not logged)")
            try:
                user = await uow.users.add(
                    UserCreateSchema(
                        username=user_create.username,
                        email=user_create.email,
                        password=hashed_password
                    )
                )
                await uow.commit()
                logger.info(f"User created with ID: {user.id} username='{user.username}'")
                # generate activation token (do not log token contents)
                activation_token = await self.generate_activation_jwt(user)
                logger.info(f"Generated activation token for user='{user.username}' (token not logged)")
                logger.info(f"Sending welcome email task to {user_create.email}")
                task = send_welcome_email_task.delay(
                    to_email=user_create.email,
                    username=user_create.username,
                    action_url=f'{SecurityConfig.activation_url}?activation_token={activation_token}'
                )
                logger.debug(f"Celery task queued: {task}")
                return {'status': 'success'}
            except Exception as e:
                logger.exception(f"Error creating user: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email or username already exists."
                )
            
    async def activate_user(self, activation_token: str, uow: IUnitOfWork):
        logger.info("activate_user called (activation token not logged)")
        async with uow: 
            data = await self.__decode_activation_jwt(activation_token)
            username = data.get('username')
            logger.debug(f"Activation token decoded for username='{username}'")
            user = await uow.users.get(username=username)
            if not user:
                logger.warning(f"activate_user: user not found for username='{username}'")
                raise HTTPException(status_code=404)
            user_update = await uow.users.update(user.id, is_active=True)
            if user_update:
                await uow.commit()
                logger.info(f"User activated: username='{username}', id={user.id}")
                return {'status': 'success'}
            logger.error(f"activate_user: failed to update user id={user.id}")
            raise HTTPException(status_code=409)
             

    async def login(self, user_login: LoginSchema, uow: IUnitOfWork):
        logger.info(f"login called for username='{user_login.username}'")
        async with uow:
            user = await uow.users.get(username=user_login.username)
            if not user:
                logger.warning(f"login failed: invalid credentials for username='{user_login.username}'")
                raise HTTPException(status_code=400, detail='invalid credetials')
            # returning access_token, refresh_token
            access = await self.generate_access_jwt(user)
            refresh = await self.generate_refresh_jwt(user)
            logger.info(f"User logged in: username='{user.username}' (tokens generated, not logged)")
            return access, refresh


    def _create_payload(self, user: UserSchema, expires):
        payload = {
            "exp": expires,
            "username": user.username,
            "role": user.role,
        }
        logger.debug(f"_create_payload: username='{user.username}', role='{user.role}', exp={expires}")
        return payload

    def _encode_jwt(self, payload: dict, key):
        logger.debug(f"_encode_jwt: encoding payload for username='{payload.get('username')}'")
        token = PyJWT().encode(payload=payload, key=key, algorithm=SecurityConfig.algorithm)
        logger.debug(f"_encode_jwt: token encoded (value not logged)")
        return token

    def expires_time(self, expires):
        expire_time = datetime.utcnow() + expires
        logger.debug(f"expires_time: computed expire timestamp: {int(expire_time.timestamp())}")
        logger.debug(f"expires_time: current utc timestamp: {int(datetime.utcnow().timestamp())}")
        return expire_time


    async def generate_access_jwt(self, user: UserSchema):
        logger.debug(f"generate_access_jwt called for username='{user.username}'")
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp))
        token = self._encode_jwt(payload, SecurityConfig.secret_key)
        logger.debug(f"generate_access_jwt: access token generated for username='{user.username}' (not logged)")
        return token

    async def generate_refresh_jwt(self, user: UserSchema):
        logger.debug(f"generate_refresh_jwt called for username='{user.username}'")
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp_refresh))
        token = self._encode_jwt(payload, SecurityConfig.secret_key)
        logger.debug(f"generate_refresh_jwt: refresh token generated for username='{user.username}' (not logged)")
        return token

    async def generate_activation_jwt(self, user: UserSchema):
        logger.debug(f"generate_activation_jwt called for username='{user.username}'")
        payload = self._create_payload(user, self.expires_time(SecurityConfig.exp_activation))
        token = self._encode_jwt(payload, SecurityConfig.activation_secret)
        logger.debug(f"generate_activation_jwt: activation token generated for username='{user.username}' (not logged)")
        return token
    
    async def _decode_jwt(self, token: str):
        logger.debug("_decode_jwt called (token not logged)")
        try:
            data = PyJWT().decode(token, key=SecurityConfig.secret_key, algorithms=[SecurityConfig.algorithm])
            if not data:
                logger.warning("_decode_jwt: decoded payload empty")
                raise HTTPException(status_code=401)
            logger.debug(f"_decode_jwt: decoded payload for username='{data.get('username')}'")
            return data
        except Exception as e:
            logger.exception(f"_decode_jwt: failed to decode token: {e}")
            raise HTTPException(status_code=401)
        
    async def __decode_activation_jwt(self, activation_token: str):
        logger.debug("__decode_activation_jwt called (token not logged)")
        try:
            data = PyJWT().decode(activation_token, key=SecurityConfig.activation_secret, algorithms=[SecurityConfig.algorithm])
            if not data:
                logger.warning("__decode_activation_jwt: decoded payload empty")
                raise HTTPException(status_code=401)
            logger.debug(f"__decode_activation_jwt: decoded payload for username='{data.get('username')}'")
            return data
        except Exception as e:
            logger.exception(f"error decode activation token: {e}")
            raise HTTPException(status_code=401)
