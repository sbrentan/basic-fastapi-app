import os

# App
APP_NAME = os.getenv("APP_NAME", "funder")

# Database
SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///funder/database/funder.db")
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL", "postgresql://postgres:password@localhost/spazial_db")
