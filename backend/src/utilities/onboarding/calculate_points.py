from typing import Dict, List
from enum import Enum

from src.models.schemas.onboarding import AnswerItem

# Define an Enum for answer types
class AnswerType(Enum):
    single = 0
    tie = 1
    rank = 2

# Function to calculate points
def calculate_points(answers: List[AnswerItem]) -> Dict[str, int]:
    points = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    
    for item in answers:
        if item.answerType == AnswerType.single:
            for ans in item.answer:
                points[ans] += 6
        elif item.answerType == AnswerType.tie:
            for ans in item.answer:
                points[ans] += 3
        elif item.answerType == AnswerType.rank:
            points[item.answer[0]] += 4
            points[item.answer[1]] += 2
    
    return points