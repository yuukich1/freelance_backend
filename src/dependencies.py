from typing import Annotated
from fastapi import Depends
from src.utils.unit_of_work import UnitOfWork
from src.service.auth import AuthService

UOWdep = Annotated[UnitOfWork, Depends(UnitOfWork)]
UserDep = Annotated[dict, Depends(AuthService.get_user_by_jwt)]
AdminDep = Annotated[dict, Depends(AuthService.get_admin_by_jwt)]