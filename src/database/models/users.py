import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String(255), nullable=False)