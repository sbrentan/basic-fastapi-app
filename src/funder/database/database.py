from common.database.sqlite import SqliteDatabase
from funder.database.collections.transaction import TransactionCollection
from funder.settings import DATABASE_URL


class FunderDatabase(SqliteDatabase):
    transaction: TransactionCollection
    database_url = DATABASE_URL


funder_database = FunderDatabase()


async def get_db():
    try:
        funder_database.start()
        yield funder_database
        funder_database.commit()
    finally:
        # Close the database connection when the request is done
        funder_database.close()
