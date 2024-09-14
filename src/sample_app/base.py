import logging
from typing import Callable, Tuple

from fastapi import APIRouter

from sample_app.database.database import sample_database
from sample_app.routers.transaction import router as transaction_router
from global_variables import global_variables

router = APIRouter(
    prefix="/sample",
    tags=["sample"]
)


async def router_startup(fastapi_app):
    logging.debug("Starting up the sample app...")
    global_variables.databases["sample"] = sample_database


async def router_shutdown(fastapi_app):
    logging.debug("Shutting down the sample app...")

router_lifespan: Tuple[Callable, Callable] = (router_startup, router_shutdown)


router.include_router(transaction_router)
