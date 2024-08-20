import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.crud.base import BaseCRUDRepository
from src.securities.hashing.password import pwd_generator
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from src.utilities.exceptions.password import PasswordDoesNotMatch


class AccountCRUDRepository(BaseCRUDRepository):
    async def is_email_taken(self, email: str) -> bool:
        return True
