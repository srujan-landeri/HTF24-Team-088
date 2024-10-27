from fastapi import FastAPI
from controllers import aggregated_news, chat_api
from routes import auth, summarize, interactions


app = FastAPI()

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