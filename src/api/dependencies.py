from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres import get_db_session

async_session_dep = Annotated[AsyncSession, Depends(get_db_session)]