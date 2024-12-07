from typing import Generic, List, TypeVar, Any

from abc import ABC, abstractmethod

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseCollection(ABC, Generic[T]):

    def __init__(self, database: Any):  # Any is used to avoid circular imports
        self.collection = None
        self.database = database
        self.instance_class = None

    @abstractmethod
    async def get(self, item_id: str) -> T:
        raise NotImplementedError

    @abstractmethod
    async def filter(self, **kwargs) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, new_item: T, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, item: T, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item_id) -> bool:
        raise NotImplementedError
