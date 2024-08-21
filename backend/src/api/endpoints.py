import fastapi

from src.api.routes.user import router as user_router
from src.api.routes.authentication import router as authentication_rouer

router = fastapi.APIRouter()

router.include_router(router=user_router)
router.include_router(router=authentication_rouer)
