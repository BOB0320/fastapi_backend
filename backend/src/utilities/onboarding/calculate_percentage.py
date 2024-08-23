from typing import Dict, List, Tuple

# Function to calculate the percent to choose the main profile of user
def calculate_percentage(points: Dict[str, int]) -> Tuple[Dict[str, float], str]:
    total_points = sum(points.values())
    percentage = {
        key: round((value / total_points) * 100, 1) 
        if total_points > 0 else 0 
        for key, value in points.items()
    }
    
    # Find the answer with the highest score
    best_score = max(points, key=points.get) if points else None
    return percentage, best_score