from typing import TypeVar
import logging
from contextlib import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generic type for Pydantic models
T = TypeVar("T", bound=BaseModel)


class UnitOfWork:
    """
    Implements the Unit of Work pattern to manage database transactions.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for handling database transactions.
        Rolls back the transaction if an error occurs.
        """
        try:
            yield
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error("Transaction rollback", error=str(e))
            raise e
        finally:
            if self.db.is_active:
                # await self.db.expunge_all()
                await self.db.close()
                logger.debug("Session closed")