from fastapi import APIRouter
from utils.summary import summarize
from models.scraper import ScrapeRequest

router = APIRouter()

@router.post("/summarize")
async def scrape_and_summarize(request: ScrapeRequest):
    summary = summarize(request.url)
    return {"summary": summary}