from fastapi import APIRouter, HTTPException
from models.user import UserResponse, UserCreate
from models.article import ArticleInteraction
from utils.database import to_object_id, url_to_id
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["news_aggregator"]

router = APIRouter()

# Like an article
@router.post("/articles/like")
def like_article(interaction: ArticleInteraction):
    user_id = to_object_id(interaction.user_id)
    article_id = url_to_id(interaction.article_url)

    # Ensure article is saved if it does not exist
    article = db.articles.find_one({"_id": article_id})
    if not article:
        article_data = {
            "_id": article_id,
            "title": interaction.title,
            "url": interaction.article_url,
            "source": interaction.source,
            "published_at": interaction.published_at,
            "description": interaction.description,
            "author": interaction.author,
            "likes": 0,
            "dislikes": 0
        }
        db.articles.insert_one(article_data)

    # Check if the article is already liked or disliked by the user
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if article_id in user.get("liked_articles", []):
        db.articles.update_one({"_id": article_id}, {"$inc": {"likes": -1}})
        db.users.update_one({"_id": user_id}, {"$pull": {"liked_articles": article_id}})
        return {"message": "Article unliked successfully"}

    if article_id in user.get("disliked_articles", []):
        # Remove dislike and decrement dislike count
        db.users.update_one({"_id": user_id}, {"$pull": {"disliked_articles": article_id}})
        db.articles.update_one({"_id": article_id}, {"$inc": {"dislikes": -1}})

    # Add article to liked articles and increment like count
    db.users.update_one({"_id": user_id}, {"$addToSet": {"liked_articles": article_id}})
    db.articles.update_one({"_id": article_id}, {"$inc": {"likes": 1}})

    return {"message": "Article liked successfully"}

# Dislike an article
@router.post("/articles/dislike")
def dislike_article(interaction: ArticleInteraction):
    user_id = to_object_id(interaction.user_id)
    article_id = url_to_id(interaction.article_url)

    # Ensure article is saved if it does not exist
    article = db.articles.find_one({"_id": article_id})
    if not article:
        article_data = {
            "_id": article_id,
            "title": interaction.title,
            "url": interaction.article_url,
            "source": interaction.source,
            "published_at": interaction.published_at,
            "description": interaction.description,
            "author": interaction.author,
            "likes": 0,
            "dislikes": 0
        }
        db.articles.insert_one(article_data)

    # Check if the article is already liked or disliked by the user
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if article_id in user.get("disliked_articles", []):
        db.articles.update_one({"_id": article_id}, {"$inc": {"dislikes": -1}})
        db.users.update_one({"_id": user_id}, {"$pull": {"disliked_articles": article_id}})
        return {"message": "undisliked article"}
    
    if article_id in user.get("liked_articles", []):
        # Remove like and decrement like count
        db.users.update_one({"_id": user_id}, {"$pull": {"liked_articles": article_id}})
        db.articles.update_one({"_id": article_id}, {"$inc": {"likes": -1}})

    # Add article to disliked articles and increment dislike count
    db.users.update_one({"_id": user_id}, {"$addToSet": {"disliked_articles": article_id}})
    db.articles.update_one({"_id": article_id}, {"$inc": {"dislikes": 1}})

    return {"message": "Article disliked successfully"}

# Save or unsave an article
@router.post("/articles/save")
def save_article(interaction: ArticleInteraction):
    user_id = to_object_id(interaction.user_id)
    article_id = url_to_id(interaction.article_url)

    # Check if the article already exists in the database
    article = db.articles.find_one({"_id": article_id})
    if not article:
        article_data = {
            "_id": article_id,
            "title": interaction.title,
            "url": interaction.article_url,
            "source": interaction.source,
            "published_at": interaction.published_at,
            "description": interaction.description,
            "author": interaction.author,
            "likes": 0,
            "dislikes": 0
        }
        db.articles.insert_one(article_data)

    # Check if the article is already saved by the user
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if article_id in user.get("saved_articles", []):
        # Article is already saved, unsave it
        db.users.update_one({"_id": user_id}, {"$pull": {"saved_articles": article_id}})
        return {"message": "Article unsaved successfully"}
    else:
        # Article is not saved, save it
        db.users.update_one({"_id": user_id}, {"$addToSet": {"saved_articles": article_id}})
        return {"message": "Article saved successfully"}

from pydantic import BaseModel

class ArticleURL(BaseModel):
    url: str

@router.post("/articles/details")
def get_article_details(article_url: ArticleURL):
    article_id = url_to_id(article_url.url)
    article = db.articles.find_one({"_id": article_id})

    print(article_id)  # Debugging output
    if not article:
        return {"error": "Article not found"}
    
    return {
        "title": article["title"],
        "url": article["url"],
        "source": article["source"],
        "published_at": article["published_at"],
        "description": article.get("description"),
        "author": article.get("author"),
        "likes_count": article.get("likes", 0),
        "dislikes_count": article.get("dislikes", 0),
    }

@router.get("/articles/details/{id}")
def get_article_details(id: str):
    try:
        # Convert to ObjectId only if the length matches MongoDB's ObjectId format
        if len(id) == 24:
            article_id = to_object_id(id)
        else:
            article_id = id  # Use as-is if it's not an ObjectId format
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid article ID format")

    article = db.articles.find_one({"_id": article_id})
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {
        "title": article["title"],
        "url": article["url"],
        "source": article["source"],
        "published_at": article["published_at"],
        "description": article.get("description"),
        "author": article.get("author"),
        "likes_count": article.get("likes", 0),
        "dislikes_count": article.get("dislikes", 0),
    }

@router.get("/likes/{user_id}")
def get_user_likes(user_id: str):
    user = db.users.find_one({"_id": to_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    liked_articles = user.get("liked_articles", [])
    return {"liked_articles": liked_articles}

@router.get("/dislikes/{user_id}")
def get_user_dislikes(user_id: str):
    user = db.users.find_one({"_id": to_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    disliked_articles = user.get("disliked_articles", [])
    return {"disliked_articles": disliked_articles}

@router.get("/saved/{user_id}")
def get_user_saved_articles(user_id: str):
    user = db.users.find_one({"_id": to_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    saved_articles = user.get("saved_articles", [])
    return {"saved_articles": saved_articles}


def serialize_user(user):
    if user:
        user['id'] = str(user['_id'])  # Convert ObjectId to string
        del user['_id']  # Optionally remove the ObjectId if not needed
    return user

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.users.find_one({"_id": to_object_id(user_id)})
    user.pop("password", None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)


class UrlRequest(BaseModel):
    url: str

@router.post("/hash")
def get_hash(url_request: UrlRequest):
    article_id = url_to_id(url_request.url)  # Access url through url_request
    return {"article_id": article_id}