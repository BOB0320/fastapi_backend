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
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        await user_repo.is_email_taken(email=user_create.email)
        new_user = await user_repo.create_user(user_create=user_create)
    except EntityDoesNotExist:
        raise await http_exc_400_credentials_bad_signup_request()
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

@router.get(
    path="/{user_id}",
    name="users:get-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        user = await user_repo.get_user_by_id(id=user_id)
        return UserInResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=user.roles,
            auth_id=user.auth_id,
            is_active=user.is_active,
            is_onboarding=user.is_onboarding,
            is_logged_in=user.is_logged_in,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request()

@router.put(
    path="/{user_id}",
    name="users:update-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_update: UserInCreate,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        updated_user = await user_repo.update_user(id=user_id, user_update=user_update)
        return UserInResponse(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            roles=updated_user.roles,
            auth_id=updated_user.auth_id,
            is_active=updated_user.is_active,
            is_onboarding=updated_user.is_onboarding,
            is_logged_in=updated_user.is_logged_in,
            last_login=updated_user.last_login,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request()

@router.delete(
    path="/{user_id}",
    name="users:delete-user",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    user_repo: UserCRUDRepository = fastapi.Depends(get_repository(repo_type=UserCRUDRepository)),
) -> None:
    try:
        await user_repo.delete_user(id=user_id)
    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request()


