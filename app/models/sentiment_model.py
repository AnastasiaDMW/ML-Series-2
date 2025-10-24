from transformers import pipeline
from functools import lru_cache

from app.constants import *

class SentimentModel:
    
    def __init__(self, model_name: str = MODEL_NAME):
        self._classifier = pipeline(task=TASK_TYPE, model=model_name, tokenizer=model_name)
        
    def predict(self, text: str) -> dict:
        result = self._classifier(text)[0]
        return { "label": result["label"], "score": round(result["score"], 4) }

@lru_cache
def get_model() -> SentimentModel:
    return SentimentModel()