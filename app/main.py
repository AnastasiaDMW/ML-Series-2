from fastapi import FastAPI
from app.api.routes import router as sentiment_router
import uvicorn

app = FastAPI(
    title="Sentiment Analysis API",
    description="API для анализа тональности комментариев на русском языке",
    version="1.1.0",
)

app.include_router(sentiment_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)