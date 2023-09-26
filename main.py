from fastapi import FastAPI

from config.database import Base, engine
from config.routers import router

app = FastAPI()

app.include_router(router)
