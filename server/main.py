from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import aggregated_news
from controllers import aggregated_news, chat_api
from routes import auth, summarize, interactions

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(summarize.router, prefix="/news")
app.include_router(interactions.router)
app.include_router(aggregated_news.router)
app.include_router(chat_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
