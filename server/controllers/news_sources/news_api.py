# functions and preprocessing for news API

import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetch_top_highlights_news(api_key, country_code='us', categories=None, num_articles=10,page=1,include_content=True,seen_urls=None):
    if categories is None:
        categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    
    if seen_urls is None:
        seen_urls = set()
    
    articles_data = {}

    for category in categories:
        # Construct the URL for each category
        url = f'https://newsapi.org/v2/top-headlines'
        params = {
            'country': country_code,
            'category': category,
            'pageSize': num_articles,
            'page': page,
            'apiKey': api_key
        }
        
        try:
            response = requests.get(url, params=params)
            res = response.json()
            
            if res.get("status") != "ok":
                print(f"Error fetching news for category '{category}': {res.get('message')}")
                continue

            # Extract data from articles
            articles_data[category] = []
            for article in res['articles']:
                article_url = article.get('url')
                
                # Skip if we've seen this article before
                if article_url in seen_urls:
                    continue
                
                # Add URL to seen set
                if article_url:
                    seen_urls.add(article_url)
                
                article_data = {
                    'source': article.get('source', {}).get('name', 'N/A'),
                    'author': article.get('author', 'N/A'),
                    'title': article.get('title', 'N/A'),
                    'url': article_url,
                    'description': article.get('description', 'N/A'),
                    'publishedAt': article.get('publishedAt', 'N/A')
                }
                
                if include_content:
                    article_data['content'] = article.get('content', 'N/A')
                
                articles_data[category].append(article_data)

        except requests.exceptions.RequestException as e:
            print(f"Request failed for category '{category}': {str(e)}")
            continue

    return articles_data, seen_urls

def save_to_json(data, filename='sample_gnews.json'):
    """Save the news data to a JSON file"""
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'articles': data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"\nData saved to {filename}")

def main():
    api_key = os.getenv("GOOGLE_NEWS_API_KEY")
    seen_urls = set()
    
    # First page of results
    articles, seen_urls = fetch_top_highlights_news(
        api_key=api_key,
        categories=['technology', 'business'],
        num_articles=10,
        seen_urls=seen_urls
    )

    
    # Get next page, automatically skipping duplicates
    more_articles, seen_urls = fetch_top_highlights_news(
        api_key=api_key,
        categories=['technology', 'business'],
        num_articles=5,
        page=2,
        seen_urls=seen_urls
    )

    # Combine both pages of articles
    all_articles = articles.copy()
    for category in more_articles:
        if category in all_articles:
            all_articles[category].extend(more_articles[category])
        else:
            all_articles[category] = more_articles[category]
    
    # Save to JSON file
    save_to_json(all_articles)

if __name__ == "__main__":
    main()