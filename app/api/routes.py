from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.models.sentiment_model import get_model
from app.services.sentiment_service import SentimentService
from app.schemas.comment_schema import CommentsRequest, AnalysisResponse
import json

router = APIRouter(prefix="/api", tags=["Sentiment Analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_comments(request: CommentsRequest, model=Depends(get_model)):
    service = SentimentService(model)
    return service.analyze(request.comments)

@router.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_comments_file(
    file: UploadFile = File(...),
    model = Depends(get_model)
):
    service = SentimentService(model)
    
    if file.content_type == "application/json":
        content = await file.read()
        try:
            data = json.loads(content.decode("utf-8"))
            if isinstance(data, list):
                comments = data
            elif isinstance(data, dict) and "comments" in data:
                comments = data["comments"]
            else:
                raise ValueError("Некорректный формат JSON")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ошибка чтения JSON: {e}")
    elif file.content_type in ["text/plain", "application/octet-stream"]:
        text = (await file.read()).decode("utf-8")
        comments = [line.strip() for line in text.splitlines() if line.strip()]
    else:
        raise HTTPException(status_code=415, detail="Поддерживаются только .txt и .json")
    print(comments)
    return service.analyze(comments)