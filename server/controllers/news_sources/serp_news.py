# pip install google-search-results
from serpapi import GoogleSearch
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


#news by keyword
def get_serp_by_query(query: str, limit: int = 10) -> Optional[List[Dict]]:
    """
    Fetch news stories for a specific query using SerpAPI.
    
    Args:
        query (str): Search query for news articles
        limit (int): Maximum number of stories to return (default: 10)
    
    Returns:
        List[Dict]: List of news stories with relevant attributes
        None: If there's an error in the API call
    """
    try:
        search = GoogleSearch({
            "api_key": SERPAPI_KEY,
            "q": query,
            "engine": "bing",
            "tbm": "nws",
            "num": limit
        })
        
        results = search.get_dict()
        
        if "error" in results:
            print(f"API Error: {results['error']}")
            return None
        
        stories = []
        news_results = results.get("news_results", [])
        
        for article in news_results[:limit]:
            story = {
                "title": article.get("title"),
                "link": article.get("link"),
                "source": article.get("source"),
                "date": article.get("date"),
                "snippet": article.get("snippet"),
                "thumbnail": article.get("thumbnail"),
                "position": article.get("position")
            }
            stories.append(story)
            
        return stories
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None