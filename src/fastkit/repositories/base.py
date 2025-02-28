from typing import Type, Generic, List, Dict, Optional, Any
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.fastkit.utils.base import T, UnitOfWork
from src.fastkit.filters.base import FilterBase

class BaseRepository(Generic[T]):
    """
    Generic repository providing common database operations with Unit of Work.
    """


    def __init__(self, model: Type[T], db_session: AsyncSession):
        print(f"🔍 BaseRepository -> db_session type: {type(db_session)}")
        self.model = model
        self.uow = UnitOfWork(db_session)

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        query = select(self.model).where(self.model.id == entity_id)
        result = await self.uow.db.execute(query)
        return result.scalars().first()

    async def get_all(self, filters: Optional[FilterBase] = None) -> List[T]:
        """Retrieve all entities, optionally applying filters."""
        query = select(self.model)
        if filters:
            query = filters.apply_filters(query)
        result = await self.uow.db.execute(query)
        return result.scalars().all()

    async def filter(self, filters: FilterBase) -> List[T]:
        """Apply filters and return the filtered result set."""
        query = select(self.model)
        query = filters.apply_filters(query)
        result = await self.uow.db.execute(query)
        return result.scalars().all()

    async def create(self, entity: T) -> T:
        """Create a new entity in the database within a transaction."""
        async with self.uow.transaction():
            self.uow.db.add(entity)
            await self.uow.db.flush()  # ...
            if self.uow.db.is_active:
                await self.uow.db.refresh(entity)
                print("🔍 Entity refreshed")
            else:
                print("🔍 Session is not active")
        return entity

    async def update(self, entity_id: int, updates: Dict[str, Any]) -> Optional[T]:
        """Update an existing entity within a transaction."""
        async with self.uow.transaction():
            entity = await self.get_by_id(entity_id)
            if not entity:
                return None

            for key, value in updates.items():
                setattr(entity, key, value)

            await self.uow.db.flush()
            if self.uow.db.is_active:
                await self.uow.db.refresh(entity)
            return entity

    async def delete(self, entity_id: int) -> Optional[T]:
        """Delete an entity by its ID within a transaction."""
        async with self.uow.transaction():
            entity = await self.get_by_id(entity_id)
            if not entity:
                raise HTTPException(status_code=404, detail="Entity not found")

            await self.uow.db.delete(entity)
            return entity
        
    async def create_many(self, entities: list[T]):
        """Создаёт несколько записей в БД за один раз с использованием UnitOfWork."""
        async with self.uow.transaction():
            self.uow.db.add_all(entities)
            await self.uow.db.flush()