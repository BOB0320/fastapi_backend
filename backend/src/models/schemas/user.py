import datetime
from typing import Optional

import pydantic

from src.models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    email: pydantic.EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    roles: int


class UserInUpdate(BaseSchemaModel):
    username: Optional[str] = None
    email: Optional[pydantic.EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: Optional[int] = None
    is_onboarding: Optional[bool] = None
    is_active: Optional[bool] = None

class UserInLogin(BaseSchemaModel):
    username: str
    email: pydantic.EmailStr
    password: str


class UserInResponse(BaseSchemaModel):
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    auth_id: Optional[str]
    is_onboarding: bool
    is_active: bool
    is_logged_in: bool
    last_login: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]