from pydantic import BaseModel, Field
from typing import List, Union

class CommentsRequest(BaseModel):
    comments: Union[str, List[str]] = Field(
        ...,
        example=[
            "Мне понравилось видео!",
            "Это было ужасно, не делай так больше."
        ]
    )
    
class CommentResult(BaseModel):
    text: str
    label: str
    score: float
    
class AnalysisResponse(BaseModel):
    positive: int
    negative: int
    positive_percent: float
    negative_percent: float
    results: List[CommentResult]