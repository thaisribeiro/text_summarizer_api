from fastapi import APIRouter
from src.api.routers import summarization

api_router = APIRouter()
api_router.include_router(summarization.router)
