from fastapi import FastAPI
from app.routes.player import router

app = FastAPI()
app.include_router(router)
