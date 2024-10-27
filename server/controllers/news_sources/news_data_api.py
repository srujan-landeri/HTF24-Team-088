import requests
from dotenv import load_dotenv
import os

load_dotenv()

#latest news by category
def get_latest_news_data_api(categories:dict,language="en"):
    articles={}
    params={
        "apikey": os.getenv("NEWSDATA_API_KEY"),
        "country":"us,in",
        "size":10,
        "language":language
    }
    url = "https://newsdata.io/api/1/latest"
    for category in categories["categories"]:
        links=[]
        titles=[]
        published_dates=[]
        authors=[]
        descriptions=[]
        articles[category]={}
        params["category"]=category
        response = requests.get(url, params=params)
        response=response.json()
        print(response)
        for article in response["results"]:
            # print(article)
            links.append(article["link"])
            titles.append(article["title"])
            published_dates.append(article["pubDate"])
            authors.append(article["creator"])
            descriptions.append(article["description"])
        articles[category]["links"]=links
        articles[category]["titles"]=titles
        articles[category]["published_dates"]=published_dates
        articles[category]["sources"]=authors
        articles[category]["descriptions"]=descriptions
        # print(articles)
    return articles

#news by keyword
def get_news_from_trends(words:dict,language="en"):
    articles = {}
    params = {
        "apikey": os.getenv("NEWSDATA_API_KEY"),
        "country": "us,in",
        "language": language,
        "size": 10,
        "removeduplicate": 1,
    }
    url = "https://newsdata.io/api/1/latest"
    for word in words["words"]:
        links = []
        titles = []
        published_dates = []
        authors = []
        descriptions=[]
        articles[word] = {}
        params["q"] = word
        response = requests.get(url, params=params)
        response = response.json()
        for article in response["results"]:
            links.append(article["link"])
            titles.append(article["title"])
            published_dates.append(article["pubDate"])
            authors.append(article["creator"])
            descriptions.append(article["description"])
        articles[word]["links"] = links
        articles[word]["titles"] = titles
        articles[word]["published_dates"] = published_dates
        articles[word]["sources"] = authors
        articles[word]["descriptions"]=descriptions
    return articles


if __name__ == "__main__":
    # print(get_latest_news(categories={"categories":["business","technology"]}))
    print(get_news_from_trends(words={"words":["covid","vaccine"]}))
