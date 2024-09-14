from common.database.handlers.sql import SQLDatabase
from common.database.collections.sql import BaseSQLCollection
from sample_app.schemas.models import Transaction


class TransactionCollection(BaseSQLCollection[Transaction]):

    def __init__(self, database: SQLDatabase):
        super().__init__(database)
        self.instance_class = Transaction
        self.sqlmodel_class = Transaction
