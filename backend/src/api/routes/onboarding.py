from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies.repository import get_repository
from src.models.schemas.onboarding import OnboardingRequest, OnboardingResponse, OnboardingFeedback
from src.repository.crud.onboarding import OnboardingCRUDRepository
from src.utilities.onboarding.calculate_points import calculate_points
from src.utilities.onboarding.calculate_percentage import calculate_percentage

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.post(
    path="/submit-answers", 
    name="onboarding:create-onboarding",
    response_model=OnboardingResponse,
    status_code=status.HTTP_200_OK,
)
async def create_or_update_onboarding(
    onboarding_create: OnboardingRequest,
    onboarding_repo: OnboardingCRUDRepository = Depends(
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
        await onboarding_repo.create_or_update_onboarding(onboarding_create=onboarding_create)

        # Return successful response
        return OnboardingResponse(
            primaryPersonality=best_score,
            specificPersonality=percentage
        )

    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except SystemError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.post(
    path="/save-feedback",
    name="onboarding:save-feedback",
)
async def save_feedback(
    feedback_create: OnboardingFeedback,
    onboarding_repo: OnboardingCRUDRepository = Depends(
        get_repository(
            repo_type=OnboardingCRUDRepository
        )
    ), 
) -> JSONResponse:
    try:
        # Save feedback using the repository
        await onboarding_repo.save_feedback(feedback_create)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Feedback saved successfully"}
        )
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except SystemError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
