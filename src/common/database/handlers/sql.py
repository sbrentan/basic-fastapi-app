from __future__ import annotations
from typing import TypeVar, Type

from pydantic import BaseModel
from sqlmodel import create_engine, Session, SQLModel

from common.database import BaseSQLCollection
from common.database.handlers.base import Database

T = TypeVar('T', bound=BaseModel)


class SQLDatabase(Database):

    session = None
    engine = None

    def __init__(self, database_url: str = None, collections: dict[str, Type[BaseSQLCollection[T]]] = None):
        super().__init__(collections)
        if database_url:
            self.database_url = database_url
        if not hasattr(self, "database_url") or not self.database_url:
            raise ValueError("Database URL not provided")
        self.engine = create_engine(self.database_url)
        SQLModel.metadata.create_all(self.engine)

    def start(self):
        with Session(self.engine) as session:
            self.session = session

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close_all()
