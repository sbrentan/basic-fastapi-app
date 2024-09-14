from common.database.sqlite import BaseSqliteCollection, SqliteDatabase
from sample_app.schemas.models import Transaction


class TransactionCollection(BaseSqliteCollection[Transaction]):

    def __init__(self, database: SqliteDatabase):
        super().__init__(database)
        self.instance_class = Transaction
        self.sqlmodel_class = Transaction
