from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import aggregated_news, chat_api
from routes import auth, summarize, interactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a basic route for health check
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Include the routes from different controllers and modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(summarize.router, prefix="/news")
app.include_router(interactions.router)
app.include_router(aggregated_news.router)
app.include_router(chat_api.router)

# Start the server when running this script directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
