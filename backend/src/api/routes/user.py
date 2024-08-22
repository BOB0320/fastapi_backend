import fastapi
import pydantic
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.api.dependencies.repository import get_repository
from src.models.schemas.user import UserInResponse, UserInCreate, UserInUpdate
from src.models.db.user import User
from src.repository.crud.user import UserCRUDRepository
from src.utilities.exceptions.database import EmailAlreadyExists, UsernameAlreadyExists
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request
)
from src.utilities.exceptions.http.exc_400 import (
    http_400_exc_bad_email_request,
    http_400_exc_bad_username_request
)
from src.utilities.exceptions.http.exc_409 import  (
    http_409_exc_bad_user_collision_request
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    path="",
    name="users:create-user",
    response_model=UserInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserInCreate,
    user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        await user_repo.is_email_taken(email=user_create.email)
        await user_repo.is_username_taken(username=user_create.username)
        new_user = await user_repo.create_user(user_create=user_create)
    except EmailAlreadyExists:
        raise await http_400_exc_bad_email_request(email=user_create.email)
    except UsernameAlreadyExists:
        raise await http_400_exc_bad_username_request(username=user_create.username)
    
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

@router.put(
    path="/{user_id}",
    name="users:update-user",
    response_model=UserInResponse,
)
async def update_user(
    user_id: int,
    user_update: UserInUpdate,
    user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    try:
        if user_update.email:
            await user_repo.is_email_taken(email=user_update.email)
        if user_update.username:
            await user_repo.is_username_taken(username=user_update.username)
        updated_user = await user_repo.update_user(user_id=user_id, user_update=user_update)
    except EmailAlreadyExists:
        raise await http_400_exc_bad_email_request(email=user_update.email)
    except UsernameAlreadyExists:
        raise await http_400_exc_bad_username_request(username=user_update.username)
    except IntegrityError:
        raise await http_409_exc_bad_user_collision_request(id=user_id)
    
    if not updated_user:
        raise await http_404_exc_id_not_found_request(user_id=user_id)
    return UserInResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        auth_id=updated_user.auth_id,
        is_onboarding=updated_user.is_onboarding,
        is_active=updated_user.is_active,
        is_logged_in=updated_user.is_logged_in,
        last_login=updated_user.last_login,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

@router.delete(
    path="/{user_id}",
    name="users:delete-user",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
) -> None:
    try:
        await user_repo.delete_user(user_id=user_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except SystemError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    path="/{user_id}",
    name="users:get-user",
    response_model=UserInResponse,
)
async def get_user(
    user_id: int,
    user_repo: UserCRUDRepository = Depends(get_repository(repo_type=UserCRUDRepository)),
) -> UserInResponse:
    user = await user_repo.get_user_by_id(user_id=user_id)
    if not user:
        raise await http_404_exc_id_not_found_request(user_id=user_id)
    
    return UserInResponse(**user.dict())
