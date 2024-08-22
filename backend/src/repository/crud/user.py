import typing
import loguru
import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import delete

from src.models.db.user import User
from src.models.schemas.user import UserInCreate, UserInUpdate
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
    
    async def update_user(self, user_id: int, user_update: UserInUpdate) -> User:
        stmt = sqlalchemy.select(User).where(User.id == user_id)
        result = await self.async_session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)

        try:
            await self.async_session.commit()
            await self.async_session.refresh(user)
            return user
        except IntegrityError:
            await self.async_session.rollback()
            raise IntegrityError(f"Updated user collides with other users")
        
    async def delete_user(self, user_id: int) -> bool:
        try:
            stmt = delete(User).where(User.id == user_id)
            result = await self.async_session.execute(stmt)
            if result.rowcount == 0:
                raise NoResultFound(f"User with ID {user_id} not found.")
            await self.async_session.commit()
            return True
        except NoResultFound:
            raise NoResultFound(f"User with ID {user_id} not found.")
        except IntegrityError as e:
            await self.async_session.rollback()
            raise ValueError(f"Cannot delete user with ID {user_id} due to integrity constraints.") from e
        except Exception as e:
            await self.async_session.rollback()
            raise SystemError(f"An unexpected error occurred while deleting user with ID {user_id}.") from e
        

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            stmt = sqlalchemy.select(User).where(User.id == user_id)
            result = await self.async_session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise NoResultFound(f"User with ID {user_id} not found.")
            return user
        except NoResultFound:
            raise NoResultFound(f"User with ID {user_id} not found.")
        except Exception as e:
            raise SystemError(f"An unexpected error occurred while fetching user with ID {user_id}.") from e

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