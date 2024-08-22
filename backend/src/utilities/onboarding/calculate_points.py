from typing import Dict, List, Tuple

from src.models.schemas.onboarding import AnswerItem

# Function to calculate points
def calculate_points(answers: List[AnswerItem]) -> Dict[str, int]:
    points = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    
    for item in answers:
        if item.answerType == 0:
            for ans in item.answer:
                points[ans] += 6
        elif item.answerType == 1:
            for ans in item.answer:
                points[ans] += 3
        elif item.answerType == 2:
            points[item.answer[0]] += 4
            points[item.answer[1]] += 2
    
    return points