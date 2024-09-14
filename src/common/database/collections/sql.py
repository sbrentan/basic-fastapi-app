from __future__ import annotations

import logging
from functools import wraps
from typing import TypeVar, List, Optional, Any

from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import select, SQLModel

from common.database.collections.base import BaseCollection
from common.exceptions import DatabaseException

T = TypeVar('T', bound=BaseModel)


def validate_operation(collection_function):
    @wraps(collection_function)
    def wrapper(self, *args, **kwargs):
        if self.session is None:
            raise ValueError("Session not set")
        if self.instance_class is None:
            raise ValueError("Instance class not set")
        if self.sqlmodel_class is None:
            raise ValueError("SQLModel class not set")

        return collection_function(self, *args, **kwargs)

    return wrapper


class BaseSQLCollection(BaseCollection[T]):

    def __init__(self, database: Any):  # Any is used to avoid circular imports
        super().__init__(database)
        self.database = database
        self.instance_class: Optional[T] = None
        self.sqlmodel_class: Optional[SQLModel] = None

    @property
    def session(self):
        return self.database.session

    def _to_instance(self, sqlmodel_instance):
        if sqlmodel_instance is None:
            return None
        if self.sqlmodel_class == self.instance_class:
            return sqlmodel_instance
        try:
            return self.instance_class.model_validate(sqlmodel_instance.model_dump())
        except Exception as e:
            logging.error(f"Error converting SQLModel [{sqlmodel_instance}] to instance [{self.instance_class}]:\n{e}")
            raise e

    def _to_sqlmodel(self, instance):
        if instance is None:
            return None
        if self.sqlmodel_class == self.instance_class:
            return instance
        try:
            return self.sqlmodel_class.model_validate(instance.model_dump())
        except Exception as e:
            logging.error(f"Error converting instance [{instance}] to SQLModel [{self.sqlmodel_class}]:\n{e}")
            raise e

    def _commit_operation(self):
        try:
            logging.debug(f"Committing [{self.sqlmodel_class.__name__}] operation to database")
            self.database.commit()
        except exc.SQLAlchemyError as e:
            logging.error(f"Error in committing [{self.sqlmodel_class.__name__}] operation:\n{e}")
            raise DatabaseException(f"There was an error in the database operation", e)

    @validate_operation
    async def get(self, item_id: int) -> T:
        logging.debug(f"Getting item [{item_id}] from [{self.sqlmodel_class.__name__}]")
        statement = select(self.sqlmodel_class).where(self.sqlmodel_class.id == item_id)
        result = self.session.exec(statement).first()
        return self._to_instance(result)

    @validate_operation
    async def filter(self, **kwargs) -> List[T]:
        logging.debug(f"Filtering items from [{self.sqlmodel_class.__name__}] with kwargs [{kwargs}]")
        conditions = [getattr(self.sqlmodel_class, key) == value for key, value in kwargs.items()]
        statement = select(self.sqlmodel_class).where(*conditions)
        result = self.session.exec(statement).all()
        return [self._to_instance(item) for item in result]

    @validate_operation
    async def create(self, new_item: T, **kwargs) -> T:
        logging.debug(f"Creating item [{self.sqlmodel_class.__name__}] with values: \n\t[{new_item.model_dump()}]")
        sqlmodel_instance = self._to_sqlmodel(new_item)
        self.session.add(sqlmodel_instance)
        self._commit_operation()
        self.session.refresh(sqlmodel_instance)
        return self._to_instance(sqlmodel_instance)

    @validate_operation
    async def update(self, item: T, **kwargs) -> T:
        sql_item = item
        if sql_item.__class__ != self.sqlmodel_class:
            raise Exception(f"Trying to update item [{sql_item.__class__.__name__}] with collection of "
                            f"[{self.sqlmodel_class.__name__}]")
        else:
            sql_item = self.session.get(self.sqlmodel_class, item.id)
            logging.debug(f"Updating item [{self.sqlmodel_class.__name__}]\n\tfrom values:"
                          f"\n\t\t[{sql_item.model_dump()}]\n\tto values: \n\t\t[{item.model_dump()}]")
            for key, value in item.model_dump().items():
                setattr(sql_item, key, value)

        self.session.add(sql_item)
        if kwargs.pop("commit", True):
            self._commit_operation()
            self.session.refresh(sql_item)
        return sql_item

    @validate_operation
    async def delete(self, item_id, **kwargs) -> bool:
        logging.debug(f"Deleting item [{item_id}] from [{self.sqlmodel_class.__name__}]")
        statement = select(self.sqlmodel_class).where(self.sqlmodel_class.id == item_id)
        result = self.session.exec(statement).first()
        if result is None:
            return False
        self.session.delete(result)
        if kwargs.pop("commit", True):
            self._commit_operation()
        return True
