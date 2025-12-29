from typing import List
from src.schemas.executer import SkillsSchema
from src.models import Skills
from src.connect import SyncSession
from loguru import logger
from sqlalchemy.exc import IntegrityError

class SkillsWorker:
    @staticmethod
    def create_skills(skills_data: dict): 
        with SyncSession() as session:
            created_count = 0
            skipped_count = 0
            
            for title, _ in skills_data.items(): 
                logger.info(f"Creating skill: {title}")
                skill_obj = Skills()
                skill_obj.title = title  
                
                try:
                    session.add(skill_obj)
                    session.flush() 
                    created_count += 1
                except IntegrityError as e:
                    session.rollback()
                    logger.warning(f"Skill '{title}' already exists, skipping")
                    skipped_count += 1
                except Exception as e:
                    logger.exception(f"Error adding skill {title}: {e}")
            
            session.commit()
            logger.info(f'Skills created: {created_count}, skipped duplicates: {skipped_count}')