from fastapi import APIRouter, HTTPException, Depends
from models.user import UserCreate, UserLogin, UserResponse
from utils.security import hash_password, verify_password, create_access_token
from datetime import timedelta
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# MongoDB client setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["news_aggregator"]
user_collection = db["users"]

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "liked_articles": [],      
        "disliked_articles": [],   
        "saved_articles": []       
    }

    user_collection.insert_one(user_data)
    return UserResponse(username=user.username, email=user.email)


@router.post("/login")
async def login_user(user: UserLogin):
    db_user = user_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "id": str(db_user["_id"])}
