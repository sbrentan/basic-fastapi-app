import os

# Environment
IS_PRODUCTION = os.getenv("IS_PRODUCTION", False)


# Logging
if IS_PRODUCTION:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
else:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


# Database
DB_TYPE = os.getenv("DB_TYPE", "sqlite3")

if IS_PRODUCTION and DB_TYPE == "sqlite3":
    raise RuntimeError("Cannot use SQLite in production")

if DB_TYPE == "sqlite3":
    SQLITE_DB = os.getenv("SQLITE_DB", "db.sqlite3")
    DATABASE_URL = f"sqlite:///{SQLITE_DB}"
    # DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///sample_app/database/sample.db")
elif DB_TYPE == "postgres":
    PG_USER = os.getenv("PG_USER", "postgres")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "password")
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_DATABASE = os.getenv("PG_DATABASE", "spazial_db")
    DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
else:
    raise RuntimeError(f"Unable to load a database of type {DB_TYPE}")


# Middlewares
MIDDLEWARES = []
