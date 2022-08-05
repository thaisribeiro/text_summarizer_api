from fastapi import APIRouter
from api.schemas.summarization_schema import Summarization
from api.services.summarization_service import get_summarization

router = APIRouter(tags=['Summarizations'], prefix='/summarization')

@router.post('')
async def extract_resume_scraping(summarization: Summarization):
    return await get_summarization(summarization)
    