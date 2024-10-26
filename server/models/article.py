from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ArticleInteraction(BaseModel):
    user_id: str
    article_url: str
    title: str
    source: Optional[str] = None
    published_at: Optional[datetime]
    description: Optional[str] = None
    author: Optional[str] = None