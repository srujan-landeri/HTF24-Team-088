import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

def get_latest_news_api(
        categories: dict,
        lang: str = 'en'
    ):
    articles = {}
    params = {
        "apiKey": os.getenv("GOOGLE_NEWS_API_KEY"),
        "country": "us",
        "pageSize": 10
    }
    url = "https://newsapi.org/v2/top-headlines"
    
    for category in categories["categories"]:
        links = []
        titles = []
        published_dates = []
        authors = []
        article_source = []
        descriptions = []
        articles[category] = {}
        
        params["category"] = category
        response = requests.get(url, params=params)
        response = response.json()
        
        if response.get("status") == "ok":
            for article in response["articles"]:
                links.append(article.get("url", "N/A"))
                titles.append(article.get("title", "N/A"))
                published_dates.append(article.get("publishedAt", "N/A"))
                authors.append(article.get("author", "N/A"))
                descriptions.append(article.get("description", "N/A"))
                
            articles[category]["links"] = links
            articles[category]["titles"] = titles
            articles[category]["published_dates"] = published_dates
            articles[category]["sources"] = authors
            articles[category]["descriptions"] = descriptions
    
    # Create samples directory and save to JSON
    os.makedirs("samples", exist_ok=True)
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "articles": articles
    }
    filepath = os.path.join("samples", "category_news.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {filepath}")
            
    return articles

def search_for_news(
        words: dict,
        lang: str = 'en'
    ):
    articles = {}
    params = {
        "apiKey": os.getenv("GOOGLE_NEWS_API_KEY"),
        "language": lang,
        "pageSize": 10,
        "sortBy": "publishedAt"
    }
    url = "https://newsapi.org/v2/everything"
    
    for word in words["words"]:
        links = []
        titles = []
        published_dates = []
        authors = []
        descriptions = []
        articles[word] = {}
        
        params["q"] = word
        response = requests.get(url, params=params)
        response = response.json()
        
        if response.get("status") == "ok":
            for article in response["articles"]:
                links.append(article.get("url", "N/A"))
                titles.append(article.get("title", "N/A"))
                published_dates.append(article.get("publishedAt", "N/A"))
                authors.append(article.get("author", "N/A"))
                descriptions.append(article.get("description", "N/A"))
                
            articles[word]["links"] = links
            articles[word]["titles"] = titles
            articles[word]["published_dates"] = published_dates
            articles[word]["sources"] = authors
            articles[word]["descriptions"] = descriptions
    
    os.makedirs("samples", exist_ok=True)
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "articles": articles
    }

    filepath = os.path.join("samples", "keyword_news.json")
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {filepath}")
            
    return articles

# if __name__ == "__main__":
#     category_news = get_latest_news(categories={"categories": ["business", "technology"]})
#     keyword_news = search_for_news(words={"words": ["artificial intelligence", "machine learning"]}, lang = 'ta')
