from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import aggregated_news, chat_api
from routes import auth, summarize, interactions

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows requests from any origin. Change this to specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
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
