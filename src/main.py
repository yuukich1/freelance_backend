from fastapi import FastAPI
from src.routes import *
from src.config import lifespan, limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix='/api/categories', tags=['categories'])

