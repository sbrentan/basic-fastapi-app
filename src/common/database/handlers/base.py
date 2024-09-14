from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Type

from pydantic import BaseModel
from typing import TypeVar

from common.database.collections.base import BaseCollection

T = TypeVar('T', bound=BaseModel)


class Database(ABC):

    def __init__(self, collections: dict[str, Type[BaseCollection]]):
        self.database = None
        self._instantiate_collections(collections)

    def _instantiate_collections(self, collections: dict[str, Type[BaseCollection]] = None):
        if collections:
            self.collections = collections
        elif not hasattr(self, "collections"):
            self.collections = {}
            for annotation, value in self.__annotations__.items():
                if issubclass(value, BaseCollection):
                    self.collections[annotation] = value

        self.collections = {
            collection_name: collection.__call__(self) for collection_name, collection in self.collections.items()
        }

        for collection_name, collection in self.collections.items():
            setattr(self, collection_name, self.collections[collection_name])

    def get_collection(self, collection_name):
        return self.collections[collection_name]

    def __getitem__(self, item):
        return self.get_collection(item)

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
