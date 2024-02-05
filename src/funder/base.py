from typing import Callable, Tuple

from fastapi import APIRouter

from funder.database.database import funder_database
from funder.routers.transaction import router as transaction_router
from global_variables import global_variables

router = APIRouter(
    prefix="/funder",
    tags=["funder"]
)


async def router_startup(fastapi_app):
    print("Starting up the funder...")
    global_variables.databases["funder"] = funder_database


async def router_shutdown(fastapi_app):
    print("Shutting down the funder...")

router_lifespan: Tuple[Callable, Callable] = (router_startup, router_shutdown)


router.include_router(transaction_router)
