from sqlalchemy.orm import DeclarativeBase

from src.database.postgres import DATABASE_URL


class Base(DeclarativeBase):
    pass

__all__ = [
    "Base",
    "DATABASE_URL"
    # "AuthToken",
    # "BlogPost",
    # "BlogCategory"
]