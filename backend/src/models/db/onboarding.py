import datetime
from typing import Optional, Dict, Union, List

import sqlalchemy
from sqlalchemy import Column, JSON, Integer, String, ForeignKey, Text
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column, relationship

from src.repository.table import Base

class Onboarding(Base):
    __tablename__ = "onboarding"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(Integer, primary_key=True, index=True)
    user_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    primary_personality: SQLAlchemyMapped[Optional[str]] = sqlalchemy_mapped_column(String, nullable=True)
    specific_personality: SQLAlchemyMapped[Optional[Dict[str, float]]] = sqlalchemy_mapped_column(JSON, nullable=True)
    detailed_qa: SQLAlchemyMapped[Optional[List[Dict[str, Union[int, List[str]]]]]] = sqlalchemy_mapped_column(JSON, nullable=True)
    feedback: SQLAlchemyMapped[Optional[str]] = sqlalchemy_mapped_column(Text, nullable=True)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

     # Relationship back to User
    user = relationship("User", back_populates="onboarding")
    