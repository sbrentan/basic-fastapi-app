import os

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///funder/database/funder_db.db")
