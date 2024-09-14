import os

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Production
IS_PRODUCTION = os.getenv("IS_PRODUCTION", False)
