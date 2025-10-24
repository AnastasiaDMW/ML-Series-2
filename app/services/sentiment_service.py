from typing import List
from app.models.sentiment_model import SentimentModel
from app.schemas.comment_schema import CommentResult, AnalysisResponse

class SentimentService:
    
    def __init__(self, model: SentimentModel):
        self.model = model
        
    def analyze(self, comments_input) -> AnalysisResponse:
        
        if isinstance(comments_input, str):
            comments = [comments_input]
        else:
            comments = comments_input
            
        positive, negative = 0, 0
        results: List[CommentResult] = []
        
        for comment in comments:
            result = self.model.predict(comment)
            label = result["label"]
            score = result["score"]
            
            if label == "POSITIVE":
                positive += 1
            else:
                negative += 1
                
            results.append(CommentResult(text=comment, label=label, score=score))
            
        total = positive + negative or 1
        
        return AnalysisResponse(
            positive=positive,
            negative=negative,
            positive_percent=round(positive/total * 100, 2),
            negative_percent=round(negative/total * 100, 2),
            results=results
        )