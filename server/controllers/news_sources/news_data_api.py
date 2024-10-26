import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_latest_news(categories:dict):
    articles={}
    params={
        "apikey": os.getenv("NEWSDATA_API_KEY"),
        "country":"us,in",
        "language":"en",
        "size":10,
        "removeduplicate":1
    }
    url = "https://newsdata.io/api/1/latest"
    for category in categories["categories"]:
        links=[]
        titles=[]
        published_dates=[]
        authors=[]
        articles[category]={}
        params["category"]=category
        response = requests.get(url, params=params)
        response=response.json()
        for article in response["results"]:
            links.append(article["link"])
            titles.append(article["title"])
            published_dates.append(article["pubDate"])
            authors.append(article["creator"])
        articles[category]["links"]=links
        articles[category]["titles"]=titles
        articles[category]["published_dates"]=published_dates
        articles[category]["authors"]=authors
    return articles


def get_news_from_trends(words:dict):
    articles = {}
    params = {
        "apikey": os.getenv("NEWSDATA_API_KEY"),
        "country": "us,in",
        "language": "en",
        "size": 10,
        "removeduplicate": 1,
    }
    url = "https://newsdata.io/api/1/latest"
    for word in words["words"]:
        links = []
        titles = []
        published_dates = []
        authors = []
        articles[word] = {}
        params["q"] = word
        response = requests.get(url, params=params)
        response = response.json()
        for article in response["results"]:
            links.append(article["link"])
            titles.append(article["title"])
            published_dates.append(article["pubDate"])
            authors.append(article["creator"])
        articles[word]["links"] = links
        articles[word]["titles"] = titles
        articles[word]["published_dates"] = published_dates
        articles[word]["authors"] = authors
    return articles


if __name__ == "__main__":
    # print(get_latest_news(categories={"categories":["business","technology"]}))
    print(get_news_from_trends(words={"words":["covid","vaccine"]}))
