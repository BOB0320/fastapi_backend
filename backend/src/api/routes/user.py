import fastapi
import pydantic

from src.api.dependencies.repository import get_repository
from src.models.schemas.user import UserInResponse, UserInCreate
from src.models.db.user import User
from src.repository.crud.user import UserCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_email_not_found_request,
    http_404_exc_id_not_found_request,
    http_404_exc_username_not_found_request,
)
from src.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/accounts", tags=["users"])

@router.post(
    path="",
    name="users:create-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def create_user(
    user_create: UserInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    print("-------------------")
    
    # try:
    #     await user_repo.is_email_taken(email=user_create.email)
    # except EntityDoesNotExist:
    #     raise await http_exc_400_credentials_bad_signup_request()
    print("====================")
    new_user = await user_repo.create_user(user_create=user_create)
    print("ddddddddddddddddd",new_user)
    return UserInResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        roles=new_user.roles,
        auth_id=new_user.auth_id,
        is_active=new_user.is_active,
        is_onboarding=new_user.is_onboarding,
        is_logged_in=new_user.is_logged_in,
        last_login=new_user.last_login,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )


