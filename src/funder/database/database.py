import logging

from common.database.sqlite import SqliteDatabase
from funder.database.collections.transaction import TransactionCollection
from funder.settings import SQLITE_DATABASE_URL, POSTGRES_DATABASE_URL
from common.settings import IS_PRODUCTION


class FunderDatabase(SqliteDatabase):
    transaction: TransactionCollection

    def __init__(self, database_url: str):
        super().__init__(database_url)


if IS_PRODUCTION:
    logging.info(f"Running in production mode. Using PostgreSQL database.")
    funder_database = FunderDatabase(POSTGRES_DATABASE_URL)
else:
    logging.info(f"Running in development mode. Using SQLite database.")
    funder_database = FunderDatabase(SQLITE_DATABASE_URL)


async def get_db():
    try:
        funder_database.start()
        yield funder_database
        funder_database.commit()
    finally:
        # Close the database connection when the request is done
        funder_database.close()
