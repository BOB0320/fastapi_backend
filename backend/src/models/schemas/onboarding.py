from typing import List, Dict, Optional, Union

from src.models.schemas.base import BaseSchemaModel

class AnswerItem(BaseSchemaModel):
    questionNumber: int
    answer: List[str]
    answerType: int
    
    def to_dict(self) -> dict:
        return {
            "questionNumber": self.questionNumber,
            "answer": self.answer,
            "answerType": self.answerType
        }
    
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