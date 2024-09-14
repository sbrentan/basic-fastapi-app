import logging
from typing import Callable, Tuple

from fastapi import APIRouter

from database import database
from sample_app.routers.transaction import router as transaction_router
from vars import global_variables

router = APIRouter(
    prefix="/sample",
    tags=["sample"]
)


async def router_startup(fastapi_app):
    logging.debug("Starting up the sample app...")
    global_variables.databases["sample"] = database


async def router_shutdown(fastapi_app):
    logging.debug("Shutting down the sample app...")

router_lifespan: Tuple[Callable, Callable] = (router_startup, router_shutdown)


router.include_router(transaction_router)
