from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, Type, TypeVar, List, Dict, Any, Callable
from pydantic import BaseModel
from src.middleware.engine import get_async_session
from src.fastkit.services.base import BaseService

T = TypeVar("T")  # ORM model type
# Pydantic schema for creation
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
# Pydantic schema for response
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


class BaseRouter(Generic[T]):
    """
    Generic router to standardize CRUD endpoints for any entity.
    """

    def __init__(self, service_cls: Type[BaseService[T]], schema: Type[BaseModel], prefix: str):
        """
        :param service_cls: ...
        :param schema: ...
        :param prefix: ...
        """
        print(f"🛠 BaseRouter -> service_cls: {service_cls}")

        self.service_cls = service_cls  # ...
        self.schema = schema
        self.router = APIRouter(prefix=prefix, tags=[prefix.strip("/")])

        @self.router.post("/", response_model=schema)
        async def create(
            entity: schema,
            db_session: AsyncSession = Depends(get_async_session),  # ...
        ):
            """Create a new entity."""
            service = self.service_cls(db_session)  # ...
            # return await service.create(entity)
            created_entity = await service.create(entity)  # ...

            # return schema.model_validate(created_entity, from_attributes=True)
            return created_entity

        @self.router.get("/{entity_id}", response_model=schema)
        async def get_by_id(
            entity_id: int,
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """Retrieve an entity by ID."""
            service = self.service_cls(db_session)
            entity = await service.get_by_id(entity_id)

            if entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with ID {entity_id} not found",
                )

            return entity

        @self.router.get("/", response_model=List[schema])
        async def get_all(
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """Retrieve all entities."""
            service = self.service_cls(db_session)
            return await service.get_all()

        @self.router.put("/{entity_id}", response_model=schema)
        async def update(
            entity_id: int,
            entity: schema,
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """Update an existing entity."""
            service = self.service_cls(db_session)
            return await service.update(entity_id, entity.dict())

        @self.router.delete("/{entity_id}", response_model=schema)
        async def delete(
            entity_id: int,
            db_session: AsyncSession = Depends(get_async_session),
        ):
            """Delete an entity."""
            service = self.service_cls(db_session)
            return await service.delete(entity_id)

    def get_router(self):
        """Return the router instance."""
        return self.router
