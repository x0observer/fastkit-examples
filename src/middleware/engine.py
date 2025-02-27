import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from setup import settings


Base = declarative_base()

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# Constants and Global Variables
POSTGRESQL_ASYNC_DATABASE_URL = settings["db"]["uri"]

# Asynchronous Engine Creation
engine: AsyncEngine = create_async_engine(
    POSTGRESQL_ASYNC_DATABASE_URL, future=True, echo=False
)


async def init_db() -> None:
    """
    Initialize the database by dropping and recreating tables.
    """
    async with engine.begin() as connection:
        # await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

# Asynchronous Session Configuration
async_session_factory = sessionmaker(
    # autocommit=False,
    # autoflush=False, 
    bind=engine, 
    expire_on_commit=False,
    class_=AsyncSession,
)


async_session_local = sessionmaker(
    # autocommit=False,
    # autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    # execution_options={"compiled_cache": None}
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous session for database operations.
    """
    logger.info("Creating a new database session")
    async with async_session_factory() as session:
        yield session
        logger.info("Closing the database session")


async def ping_pong_db() -> str:
    """
    'Ping-pong' method to check the database or server status.
    Returns 'pong' if the connection is successful.
    """
    async with engine.connect() as connection:
        # Simple database operation to check the connection
        result = await connection.execute("SELECT 1")
        return "pong" if result.fetchone() is not None else "fail"
