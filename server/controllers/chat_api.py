from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from newspaper import Article
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from ollama import generate

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    url: str


# Store databases in a dictionary, mapping URLs to ChromaDB instances
url_to_db = {}

def handle_chat(question: str, url: str):
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
        db=url_to_db[url]
    else:
        db=url_to_db[url]

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
    """

    return generate("gemma2:2b", prompt)["response"]


@router.get("/chat")
async def chat(request: ChatRequest):
    """
        {
        "question":"What did anand mahindra say",
        "url":"https://www.ndtv.com/offbeat/video-anand-mahindra-praises-iit-graduates-for-creating-compact-home-gym-6876927"
        }
    """
    return handle_chat(request.question, request.url)
