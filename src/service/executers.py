from loguru import logger
from src.utils.unit_of_work import IUnitOfWork
from src.schemas.executer import ExecuterCreateSchema, ExecuterDBSchema, ExecuterResponseSchema, ExecuterUserSchema
from src.workers.tasks import create_skills_task
from fastapi import HTTPException

class ExecuterService:

    async def add(self, uow: IUnitOfWork, executer_data: ExecuterCreateSchema, user: dict):
        logger.info(f"ExecuterService.add called for user_id={user.get('user_id')}")
        async with uow:
            if not executer_data.user_id:
                executer_data.user_id = user.get('user_id')
            skills_dict = {skill.title: skill.experience for skill in executer_data.skills}
            logger.debug(f"Creating executer with {len(skills_dict)} skills for user_id={executer_data.user_id}")
            executer = ExecuterDBSchema(
                user_id=executer_data.user_id, # type: ignore
                skills=skills_dict
            )
            try:
                executer = await uow.executers.add(executer)
                if executer:
                    await uow.commit()
                    logger.info(f"Executer created successfully with id={executer.id} for user_id={executer_data.user_id}")
                    logger.debug(f"Queuing skills creation task for {len(skills_dict)} skills")
                    create_skills_task.delay(skills_dict)
                    return executer
                else:
                    logger.error("Executer could not be created - add returned None")
                    raise HTTPException(status_code=400, detail="Executer could not be created")
            except Exception as e:
                logger.exception(f"Error creating executer: {e}")
                raise HTTPException(status_code=400, detail="Executer with this user_id already exists.")
                
    async def get_executers(self, uow: IUnitOfWork):
        logger.info("ExecuterService.get_executers called")
        async with uow:
            executers = await uow.executers.list()
            logger.info(f"Retrieved {len(executers) if executers else 0} executers from database")
            exec_response = []
            for executer in executers:
                user = await uow.users.get(id=executer.user_id)
                logger.debug(f"Fetched user for executer {executer.id}: user_id={user.id if user else None}")  # type: ignore
                exec_response.append(ExecuterResponseSchema(id=executer.id,
                                                             user=ExecuterUserSchema(email=user.email, username=user.username),  # type: ignore
                                                             skills=executer.skills, 
                                                             created_at=executer.created_at))
            logger.info(f"Prepared response for {len(exec_response)} executers")
            return exec_response
        