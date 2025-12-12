from fastapi import FastAPI
from src.routes import auth_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

