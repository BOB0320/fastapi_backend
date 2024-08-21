from src.models.schemas.base import BaseSchemaModel
from typing import List, Dict, Optional

class AnswerItem(BaseSchemaModel):
    answer: List[str]
    answerType: int
    
class OnboardingRequest(BaseSchemaModel):
    items: List[AnswerItem]
    userId: int
    primaryPersonality: Optional[str] = None
    specificPersonality: Optional[Dict[str, str]] = None
    
class OnboardingFeedback(BaseSchemaModel):
    feedback: Optional[str] = None
    userId: int

class OnboardingResponse(BaseSchemaModel):
    primaryPersonality: Optional[str]
    specificPersonality: Optional[Dict[str, float]]