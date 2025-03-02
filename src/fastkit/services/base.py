from typing import Generic, List, Optional, Dict, Any, TypeVar, Type
from pydantic import BaseModel
from src.fastkit.repositories.base import BaseRepository
from src.fastkit.filters.base import FilterBase
from src.fastkit.utils.base import T


CreateSchema = TypeVar("CreateSchema", bound=BaseModel)  # Pydantic-схема создания


class BaseService(Generic[T]):
    """
    Base service class for handling business logic.
    Provides common CRUD operations.
    """

    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository
        
    def _convert_to_orm(self, schema: CreateSchema) -> T:
        """Конвертирует Pydantic-схему в ORM-модель."""
        return self._get_model()(**schema.model_dump())

    def _get_model(self) -> Type[T]:
        """..."""
        return self.repository.model


    async def get_all(self, filters: Optional[FilterBase] = None) -> List[T]:
        """Retrieve all entities, optionally applying filters."""
        return await self.repository.get_all(filters)

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        return await self.repository.get_by_id(entity_id)

    async def create(self, entity: CreateSchema) -> T:
        """..."""
        db_obj = self._convert_to_orm(entity)
        return await self.repository.create(db_obj)

    async def update(self, entity_id: int, updates: Dict[str, Any]) -> Optional[T]:
        """Update an existing entity by its ID."""
        return await self.repository.update(entity_id, updates)

    async def delete(self, entity_id: int) -> Optional[T]:
        """Delete an entity by its ID."""
        return await self.repository.delete(entity_id)

    async def filter(self, filters: FilterBase) -> List[T]:
        """Apply filters and return the filtered result set."""
        return await self.repository.filter(filters)

