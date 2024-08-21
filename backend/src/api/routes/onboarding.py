import fastapi
from fastapi import HTTPException
from typing import Dict, List, Tuple
from src.api.dependencies.repository import get_repository
from src.models.schemas.onboarding import OnboardingRequest, OnboardingResponse, AnswerItem, OnboardingFeedback
from src.repository.crud.onboarding import OnboardingCRUDRepository

router = fastapi.APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.post(
    path="/submit-answers/", 
    name="onboarding:create-onboarding",
    response_model=OnboardingResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def create_onboarding(
    onboarding_create: OnboardingRequest,
    onboarding_repo: OnboardingCRUDRepository = 
        fastapi.Depends(
            get_repository(
                repo_type=OnboardingCRUDRepository
            )
        ),
  ) -> OnboardingResponse:
    try:
        # Calculate points and percentages
        points = calculate_points(onboarding_create.items)
        percentage, best_score = calculate_percentage(points)
        
        # Update the OnboardingRequest object with calculated values
        onboarding_create.primaryPersonality = best_score
        onboarding_create.specificPersonality = percentage

        # Attempt to create onboarding
        is_success = await onboarding_repo.create_onboarding(onboarding_create=onboarding_create)
        
        if not is_success:
            raise HTTPException(
                status_code=500, 
                detail="Failed to create onboarding record"
            )
        
        # Return successful response
        return OnboardingResponse(
            primaryPersonality=best_score,
            specificPersonality=percentage
        )

    except Exception as e:
        # Handle any unexpected exceptions
        print("Error occurred during onboarding:", str(e))
        raise HTTPException(
            status_code=500, 
            detail="An error occurred during onboarding"
        )

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

@router.post(
    path="/save-feedback/",
    name="onboarding:save-feedback",
    status_code=fastapi.status.HTTP_200_OK,
)
async def save_feedback(
    feedback_create: OnboardingFeedback,
    onboarding_repo: OnboardingCRUDRepository = fastapi.Depends(
        get_repository(
            repo_type=OnboardingCRUDRepository
        )
    ), 
) -> bool:
    try:
        # Save feedback using the repository
        is_saved = await onboarding_repo.save_feedback(feedback_create)
        if not is_saved:
            raise HTTPException(
                status_code=500, 
                detail="Failed to save feedback"
            )
        return True
    except Exception as e:
        print("Error occurred during feedback saving:", str(e))
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while saving feedback"
        )