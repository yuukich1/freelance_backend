from typing import List, Optional
from loguru import logger
from src.utils.unit_of_work import IUnitOfWork
from src.schemas.executer import ExecuterCreateSchema, ExecuterDBSchema, ExecuterResponseSchema, ExecuterUpdateSchema, ExecuterUserSchema, SkillsSchema
from src.workers.tasks import create_skills_task
from fastapi import HTTPException, Response

class ExecuterService:

    async def add(self, uow: IUnitOfWork, executer_data: ExecuterCreateSchema, user: dict):
        logger.info(f"ExecuterService.add called for user_id={user.get('user_id')}")
        async with uow:
            if not executer_data.user_id:
                executer_data.user_id = user.get('user_id')
            skills_dict = self.__skills_dict(executer_data.skills)
            logger.debug(f"Creating executer with {len(skills_dict)} skills for user_id={executer_data.user_id}")
            executer = ExecuterDBSchema(
                user_id=executer_data.user_id, # type: ignore
                skills=skills_dict
            )
            try:
                executer = await uow.executers.add(executer)
                uow.users.update(executer_data.user_id, role='executer') # type: ignore
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
                
    async def get_executers(self, uow: IUnitOfWork, filters: dict):
        logger.info("ExecuterService.get_executers called")
        async with uow:
            if filters.get('username'):
                user = await uow.users.get(username=filters.get('username'))
                if not user:
                    logger.warning(f"No user found with username={filters.get('username')}")
                    return []
                del filters['username']
                filters['user_id'] = user.id
            if filters.get('email'):
                user = await uow.users.get(email=filters.get('email'))
                if not user:
                    logger.warning(f"No user found with email={filters.get('email')}")
                    return []
                del filters['email']
                filters['user_id'] = user.id
            executers = await uow.executers.list(**filters) if filters.get('skills') is None else await uow.executers.get_by_skills(filters.get('skills'))  # type: ignore
            logger.info(f"Retrieved {len(executers) if executers else 0} executers from database")
            exec_response = []
            for executer in executers:
                user = await uow.users.get(id=executer.user_id) # type: ignore
                logger.debug(f"Fetched user for executer {executer.id}: user_id={user.id if user else None}")  # type: ignore
                exec_response.append(ExecuterResponseSchema(id=executer.id, # type: ignore
                                                             user=ExecuterUserSchema(email=user.email, username=user.username),  # type: ignore
                                                             skills=executer.skills,  # type: ignore
                                                             created_at=executer.created_at)) # type: ignore
            logger.info(f"Prepared response for {len(exec_response)} executers")
            return exec_response
        

    async def get_by_executer_id(self, uow: IUnitOfWork, executer_id: int):
        logger.info(f"ExecuterService.get_by_executer_id called for executer_id={executer_id}")
        async with uow:
            executer = await uow.executers.get(id=executer_id)
            if not executer:
                logger.warning(f"Executer with id={executer_id} not found")
                raise HTTPException(status_code=404, detail="Executer not found")
            user = await uow.users.get(id=executer.user_id)
            logger.debug(f"Fetched user for executer {executer.id}: user_id={user.id if user else None}")  # type: ignore
            exec_response = ExecuterResponseSchema(id=executer.id,
                                                   user=ExecuterUserSchema(email=user.email, username=user.username),  # type: ignore
                                                   skills=executer.skills, 
                                                   created_at=executer.created_at)
            logger.info(f"Prepared response for executer id={executer_id}")
            return exec_response
        
    async def get_by_user(self, uow: IUnitOfWork, user: dict):
        logger.info(f"ExecuterService.get_by_user called for user_id={user.get('user_id')}")
        async with uow:
            executer = await uow.executers.get(user_id=user.get('user_id'))
            if not executer:
                logger.warning(f"Executer for user_id={user.get('user_id')} not found")
                raise HTTPException(status_code=404, detail="Executer not found")
            logger.info(f"Executer for user_id={user.get('user_id')} retrieved successfully")
            return executer
        

    async def delete(self, uow: IUnitOfWork, executer_id: int, user: dict):
        logger.info(f"ExecuterService.delete called for executer_id={executer_id} by user_id={user.get('user_id')}")
        async with uow:
            executer = await uow.executers.get(id=executer_id)
            if not executer:
                logger.warning(f"Executer with id={executer_id} not found")
                raise HTTPException(status_code=404, detail="Executer not found")
            if not (executer.user_id == user.get('user_id') or user.get('is_admin')):
                logger.warning(f"User_id={user.get('user_id')} unauthorized to delete executer id={executer_id}")
                raise HTTPException(status_code=403, detail="Not authorized to delete this executer")
            await uow.executers.remove(executer)
            await uow.commit()
            logger.info(f"Executer with id={executer_id} deleted successfully by user_id={user.get('user_id')}")
            return {"detail": "success"}
        
    async def update(self, uow: IUnitOfWork, executer_data: ExecuterUpdateSchema, user: dict, executer_id: int | None):
        logger.info(f"ExecuterService.update called for executer_id={executer_id} by user_id={user.get('user_id')}")
        if executer_data.skills is None:
            return Response(status_code=304)
        async with uow:
            if (executer_id or user.get('is_admin')) and executer_id is not -1:
                executer = await uow.executers.get(id=executer_id)
            else: 
                executer = await uow.executers.get(user_id=user.get('user_id'))
            if not executer:
                logger.warning(f"Executer with id={executer_id} not found")
                raise HTTPException(status_code=404, detail="Executer not found")
            if not (executer.user_id == user.get('user_id') or user.get('is_admin')):
                logger.warning(f"User_id={user.get('user_id')} unauthorized to update executer id={executer_id}")
                raise HTTPException(status_code=403, detail="Not authorized to update this executer")
            skill_dict = self.__skills_dict(executer_data.skills)   
            execute_db = ExecuterDBSchema(
                user_id=executer.user_id, # type: ignore
                skills=skill_dict
            )
            update_executer = await uow.executers.update(executer.id, **execute_db.dict()) # type: ignore
            await uow.commit()
            logger.info(f"Executer with id={executer_id} updated successfully by user_id={user.get('user_id')}")
            create_skills_task.delay(skill_dict) # type: ignore
            return update_executer

    def __skills_dict(self, skills: List[SkillsSchema]) -> dict:
        return {skill.title: skill.experience for skill in skills}
    
