from bson import ObjectId
from fastapi import HTTPException
import hashlib

def url_to_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()

def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    