## Will contain the all the news aggregated from different sources
# Call all the functions from the news_sources and return the aggregated news

from fastapi import APIRouter
from controllers.news_sources.news_data_api import get_latest_news_data_api, get_news_from_trends
from controllers.news_sources.news_api import get_latest_news_api,search_for_news
from typing import List,Optional,Dict
from pydantic import BaseModel
from utils.summary import summarize

router = APIRouter()


class AggregatedRequest(BaseModel):
    categories: List[str]
    language: Optional[str]


def news_latest(categories:dict,language="en"):
    response={}
    response1=get_latest_news_data_api(categories,language)
    response2=get_latest_news_api(categories,language)
    for key in response1.keys():
        response[key]={}

    for key in response2.keys():
        for key1 in response2[key].keys():
            response[key][key1]=response2[key][key1]+response1[key][key1]

    return response


def news_trends(words:dict,language="en"):
    response={}
    response1=get_news_from_trends(words,language)
    response2=search_for_news(words,language)
    for key in response1.keys():
        response[key]={}

    for key in response2.keys():
        for key1 in response2[key].keys():
            response[key][key1]=response2[key][key1]+response1[key][key1]

    return response

@router.post("/aggregated_news_normal")
async def aggregated_news_normal(AggregatedRequest: AggregatedRequest):
    """
        {
            "categories":["business","sports"],
            "language":"en"
        }
    """
    a=news_latest({"categories":AggregatedRequest.categories},AggregatedRequest.language)
    return a

@router.post("/aggregated_news_trends")
async def aggregated_news_trends(AggregatedRequest: AggregatedRequest):
    """
        {
            "categories":["business","sports"],
            "language":"en"
        }
    """
    return news_trends({"words":AggregatedRequest.categories},AggregatedRequest.language)
