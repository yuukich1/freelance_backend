from fastapi import FastAPI
from src.routes import *
from src.config import lifespan, limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from loguru import logger

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix='/api/categories', tags=['categories'])
app.include_router(service_router, prefix='/api/services', tags=['services'])
app.include_router(executer_router, prefix='/api/executers', tags=['executers'])
app.include_router(skills_router, prefix='/api/skills', tags=['skills'])

logger.info("FastAPI application initialized")
logger.info("Registered routers: auth, categories, services, executers, skills")