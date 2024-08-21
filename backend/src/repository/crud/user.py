import typing
import loguru
import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.user import User
from src.models.schemas.user import UserInCreate
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EmailAlreadyExists, UsernameAlreadyExists
from src.utilities.exceptions.password import PasswordDoesNotMatch


class UserCRUDRepository(BaseCRUDRepository):
    async def create_user(self, user_create: UserInCreate) -> User:
        new_user = User(**user_create.dict())
        self.async_session.add(instance=new_user)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_user)

        return new_user
    async def is_email_taken(self, email: str) -> bool:
        email_stmt = sqlalchemy.select(User.email).select_from(User).where(User.email == email)
        email_query = await self.async_session.execute(email_stmt)
        db_email = email_query.scalar()

        if db_email:
            raise EmailAlreadyExists(f"The email `{email}` is already registered!")
        
    async def is_username_taken(self, username: str) -> bool:
        username_stmt = sqlalchemy.select(User.username).select_from(User).where(User.username == username)
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if db_username:
            raise UsernameAlreadyExists(f"The username `{username}` is already taken!")  # type: ignore