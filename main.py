from fastapi import FastAPI

from config.routers import router

app = FastAPI()

app.include_router(router)
