import logging

from common.database.sqlite import SqliteDatabase
from sample_app.database.collections.transaction import TransactionCollection
from sample_app.settings import SQLITE_DATABASE_URL, POSTGRES_DATABASE_URL
from common.settings import IS_PRODUCTION


class SampleDatabase(SqliteDatabase):
    transaction: TransactionCollection

    def __init__(self, database_url: str):
        super().__init__(database_url)


if IS_PRODUCTION:
    logging.info(f"Running in production mode. Using PostgreSQL database.")
    sample_database = SampleDatabase(POSTGRES_DATABASE_URL)
else:
    logging.info(f"Running in development mode. Using SQLite database.")
    sample_database = SampleDatabase(SQLITE_DATABASE_URL)


async def get_db():
    try:
        sample_database.start()
        yield sample_database
        sample_database.commit()
    finally:
        # Close the database connection when the request is done
        sample_database.close()
