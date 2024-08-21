import typing
import loguru
import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.user import User
from src.models.schemas.user import UserInCreate
from src.repository.crud.base import BaseCRUDRepository
from src.securities.hashing.password import pwd_generator
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.utilities.exceptions.password import PasswordDoesNotMatch


class UserCRUDRepository(BaseCRUDRepository):
    async def create_user(self, user_create: UserInCreate) -> User:
        try:
            new_user = User(
                email=user_create.email, 
                username=user_create.username, 
                first_name=user_create.first_name, 
                last_name=user_create.last_name, 
                roles=0,
                is_onboarding=True,
                is_active=False,
                is_logged_in=False
            )
            loguru.logger.info(new_user)
            print(self.async_session,"asdfasdffsadf", new_user)
            # self.async_session.add(instance=new_user)
            # await self.async_session.commit()
            # await self.async_session.refresh(instance=new_user)

            return new_user
        except Exception as e:
            print("****************8",e)
    async def is_email_taken(self, email: str) -> bool:
        email_stmt = sqlalchemy.select(User.email).select_from(User).where(User.email == email)
        email_query = await self.async_session.execute(email_stmt)
        db_email = email_query.scalar()

        if not credential_verifier.is_email_available(email=db_email):
            raise EntityAlreadyExists(f"The email `{email}` is already registered!")  # type: ignore

        return True