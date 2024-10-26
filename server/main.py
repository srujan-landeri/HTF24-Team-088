from fastapi import FastAPI
from controllers import aggregated_news

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(aggregated_news.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
