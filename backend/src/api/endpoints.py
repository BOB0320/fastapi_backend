import fastapi

from src.api.routes.user import router as user_router
from src.api.routes.onboarding import router as user_onboarding

router = fastapi.APIRouter()

router.include_router(router=user_router)
router.include_router(router=user_onboarding)
