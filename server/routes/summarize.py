from fastapi import APIRouter, HTTPException
from utils.summary import summarize
from models.scraper import ScrapeRequest
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.post("/summarize")
async def scrape_and_summarize(request: ScrapeRequest):
    summary = summarize(request.url)
    return {"summary": summary}

class UrlRequest(BaseModel):
    url: str

# @router.post("/embed")
# def embed_article(url_request: UrlRequest):
#     print(url_request.url)
#     response = requests.get(url_request.url)
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Unable to fetch the article")

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Try to extract title, description, and image
#     title = soup.find("meta", property="og:title") or soup.find("title")
#     description = soup.find("meta", property="og:description")
#     image = soup.find("meta", property="og:image")

#     return {
#         "title": title["content"] if title else "No title found",
#         "description": description["content"] if description else "No description found",
#         "image": image["content"] if image else "No image found",
#         "url": url_request.url,
#     }