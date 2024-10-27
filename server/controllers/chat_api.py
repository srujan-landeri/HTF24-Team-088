from groq import Groq
import os
import validators
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl, validator
from newspaper import Article
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from ollama import generate
from dotenv import load_dotenv
from typing import Optional, Dict, List
from newspaper.article import ArticleException

load_dotenv()
router = APIRouter()

# Validate GROQ API key at startup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize Groq client
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    raise ValueError(f"Failed to initialize Groq client: {str(e)}")

class ChatRequest(BaseModel):
    question: str
    url: str

    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        
        if len(v) > 500:
            raise ValueError("Question is too long (max 500 characters)")
        return v.strip()

    @validator('url')
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Invalid URL format")
        return v

# Store databases in dictionaries, mapping URLs to ChromaDB instances
ollama_dbs: Dict[str, Optional[Chroma]] = {}

def get_embeddings(is_groq: bool = False):
    """Get the appropriate embeddings based on the API being used"""
    return OllamaEmbeddings(model="snowflake-arctic-embed:22m")

async def handle_chat(question: str, url: str, is_groq: bool = False) -> dict:
    try:
        # Download and parse the article
        article = Article(url)
        try:
            article.download()
            article.parse()
        except ArticleException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch or parse article: {str(e)}"
            )

        if not article.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content found in the article"
            )

        # Split the text into manageable chunks
        try:
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            documents = text_splitter.split_text(article.text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error splitting text: {str(e)}"
            )

        # Choose the appropriate database dictionary based on embedding type
        db_dict = ollama_dbs

        # Get or create the ChromaDB instance for this URL
        try:
            if url not in db_dict or db_dict[url] is None:
                embeddings = get_embeddings(is_groq)
                db_dict[url] = Chroma.from_texts(
                    documents,
                    embeddings,
                    persist_directory=f"./chroma_{'st' if is_groq else 'ollama'}_{hash(url)}"
                )
            db = db_dict[url]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error with vector database: {str(e)}"
            )

        # Perform similarity search
        try:
            docs = db.similarity_search(question)
            if not docs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No relevant documents found"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during similarity search: {str(e)}"
            )

        context = " ".join([doc.page_content for doc in docs])

        prompt = f"""
        You are a question answering AI.
        You are asked a question: "{question}"
        Given the context: {context}
        Please provide a clear and concise answer based on the context provided.
        """

        try:
            if is_groq:
                completion = groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful question-answering assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="gemma-7b-it",
                    temperature=0.7,
                    max_tokens=1000
                )
                response = completion.choices[0].message.content
            else:
                response = generate("gemma2:2b", prompt)["response"]

            return {"answer": response, "status": "success"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating response: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
            )

@router.get("/chat")
async def chat(request: ChatRequest):
    """Handle chat requests using Ollama"""
    return await handle_chat(request.question, request.url)

@router.post("/chat_groq")
async def chat_groq(request: ChatRequest):
    """Handle chat requests using Groq"""
    return await handle_chat(request.question, request.url, is_groq=True)