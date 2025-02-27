from typing import Generic, Type, TypeVar, Any, cast
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.middleware.engine import get_async_session
from src.fastkit.services.base import BaseService

T = TypeVar("T")  # ORM model
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)  # Schema for creation
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)  # Schema for response


class BaseRouter(Generic[T, CreateSchema, ReadSchema]):

    def __init__(self, service_cls: Type[BaseService[T]], prefix: str, create_schema: Type[BaseModel], read_schema: Type[ReadSchema]):
        self.service_cls = service_cls
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.router = APIRouter(prefix=prefix, tags=[prefix.strip("/")])

        @self.router.post("/", response_model=cast(Any, read_schema), status_code=status.HTTP_201_CREATED)
        async def create(
            entity: cast(Any, create_schema) = Body(...), #CreateSchema = Body(...),
            db_session: AsyncSession = Depends(get_async_session),
        ) -> ReadSchema:
            service = self.service_cls(db_session)
            created_entity = await service.create(entity)
            return self.read_schema.model_validate(created_entity, from_attributes=True)

        @self.router.get("/{entity_id}", response_model=cast(Any, read_schema))
        async def get_by_id(
            entity_id: int,
            db_session: AsyncSession = Depends(get_async_session),
        ) -> ReadSchema:
            service = self.service_cls(db_session)
            entity = await service.get_by_id(entity_id)
            if entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with ID {entity_id} not found",
                )
            return self.read_schema.model_validate(entity, from_attributes=True)

        @self.router.get("/", response_model=cast(Any, list[self.read_schema]))
        async def get_all(db_session: AsyncSession = Depends(get_async_session)):
            """Retrieve all entities."""
            service = self.service_cls(db_session)
            entities = await service.get_all()
            # [ReadSchema.model_validate(e, from_attributes=True) for e in entities]
            return [self.read_schema.model_validate(e, from_attributes=True) for e in entities]

        @self.router.put("/{entity_id}", response_model=cast(Any, read_schema))
        async def update(
            entity_id: int,
            entity: cast(Any, create_schema) = Body(...),
            db_session: AsyncSession = Depends(get_async_session),
        ) -> ReadSchema:
            service = self.service_cls(db_session)
            updated_entity = service.update(entity_id, entity.dict())
            if updated_entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with ID {entity_id} not found",
                )
            return self.read_schema.model_validate(updated_entity, from_attributes=True)

        @self.router.delete("/{entity_id}", response_model=cast(Any, read_schema))
        async def delete(
            entity_id: int,
            db_session: AsyncSession = Depends(get_async_session),
        ) -> ReadSchema:
            service = self.service_cls(db_session)
            deleted_entity = await service.delete(entity_id)
            if deleted_entity is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Entity with ID {entity_id} not found",
                )
            return self.read_schema.model_validate(deleted_entity, from_attributes=True)

    def get_router(self) -> APIRouter:
        return self.router
