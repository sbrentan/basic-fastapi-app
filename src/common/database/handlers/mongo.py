from typing import Type

from motor import motor_asyncio

from common.database.handlers.base import Database
from common.database.collections.base import BaseCollection


class MongoDatabase(Database):

    database = None
    client = None

    def __init__(self, database_url: str, collections: dict[str, Type[BaseCollection]]):
        super().__init__(collections)
        self.database_url = database_url
        self.collections = collections

    def start(self):
        self.client = motor_asyncio.AsyncIOMotorClient(self.database_url)
        self.database = self.client.melius

    def close(self):
        self.database.client.close()
