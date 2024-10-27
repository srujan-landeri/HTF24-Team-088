from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from newspaper import Article
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from ollama import generate
from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()
router = APIRouter()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    question: str
    url: str


# Store databases in a dictionary, mapping URLs to ChromaDB instances
url_to_db = {}

def handle_chat(question: str, url: str, is_groq: bool = False):
    # Download and parse the article
    article = Article(url)
    article.download()
    article.parse()
    text = article.text

    # Split the text into manageable chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_text(text)

    # Get or create the ChromaDB instance for this URL
    if url_to_db.get(url) is None:
        url_to_db[url] = Chroma.from_texts(
            documents, OllamaEmbeddings(model="snowflake-arctic-embed:22m")
        )
    db = url_to_db[url]

    # Perform similarity search
    docs = db.similarity_search(question)
    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found.")

    context = " ".join([doc.page_content for doc in docs])

    # Generate a response using the LLM
    prompt = f"""
    You are a question answering AI.
    You are asked a question: "{question}"
    Given the context: {context}
    Please provide a clear and concise answer based on the context provided.
    """

    try:
        if is_groq:
            # Use Groq API
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
                model="gemma-7b-it",  # You can change the model as needed
                temperature=0.7,
                max_tokens=1000
            )
            response = completion.choices[0].message.content
        else:
            # Use Ollama
            response = generate("gemma2:2b", prompt)["response"]
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.get("/chat")
async def chat(request: ChatRequest):
    """
    Handle chat requests using Ollama
    Example request body:
    {
        "question": "What did anand mahindra say",
        "url": "https://www.ndtv.com/offbeat/video-anand-mahindra-praises-iit-graduates-for-creating-compact-home-gym-6876927"
    }
    """
    return handle_chat(request.question, request.url)

@router.get("/chat_groq")
async def chat_groq(request: ChatRequest):
    """
    Handle chat requests using Groq
    Example request body:
    {
        "question": "What did anand mahindra say",
        "url": "https://www.ndtv.com/offbeat/video-anand-mahindra-praises-iit-graduates-for-creating-compact-home-gym-6876927"
    }
    """
    return handle_chat(request.question, request.url, is_groq=True)