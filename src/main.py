import uvicorn
from fastapi import FastAPI
from src.api.routers import api_router

app = FastAPI(title='Sumarizador')

app.include_router(api_router)
