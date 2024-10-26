## Will contain the all the news aggregated from different sources
# Call all the functions from the news_sources and return the aggregated news

from fastapi import APIRouter
from controllers.news_sources import news_data_api
from news_sources.serp_news import get_serp_by_query
from news_sources.news_data_api import get_latest_news, get_news_from_trends
from typing import List
from pydantic import BaseModel

router = APIRouter()

class AggregatedRequest(BaseModel):
    categories: List[str]
    language: str

@router.get("/aggregated_news_normal")
async def aggregated_news_normal(AggregatedRequest: AggregatedRequest):
    pass

@router.get("/aggregated_news_trends")
async def aggregated_news_trends(AggregatedRequest: AggregatedRequest):
    pass