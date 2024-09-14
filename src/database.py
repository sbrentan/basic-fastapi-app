import logging

from common.database import SQLDatabase
from common.exceptions import DatabaseException
from sample_app.database.collections.transaction import TransactionCollection
from common.settings import DATABASE_URL


class AppDatabase(SQLDatabase):
    transaction: TransactionCollection

    def __init__(self, database_url: str):
        super().__init__(database_url)


database = AppDatabase(DATABASE_URL)


async def get_db():
    try:
        logging.debug("Starting database")
        database.start()
        yield database
        logging.debug("Committing database")
        try:
            database.commit()
        except Exception as e:
            logging.error(f"Error committing database: {e}")
            raise DatabaseException("There was an error executing the operation on the database", e)
    finally:
        # Close the database connection when the request is done
        logging.debug("Closing database")
        database.close()
