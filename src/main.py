from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from common import MIDDLEWARES
from vars import global_variables
from sample_app.base import router as sample_router, router_lifespan as sample_lifespan
from common.base import router as common_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # SINGLE APPLICATIONS STARTUP
    await sample_lifespan[0](fastapi_app)

    # MAIN APPLICATION STARTUP
    global_variables.APP = fastapi_app
    yield

    # SINGLE APPLICATIONS SHUTDOWN
    await sample_lifespan[1](fastapi_app)


app = FastAPI(lifespan=lifespan)


origins = [
    "*",  # replace with your frontend domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # specify allowed HTTP methods
    allow_headers=["*"],  # allow all headers, adjust as needed
    expose_headers=["Content-Disposition"],  # expose specific headers, if required
)

app.include_router(common_router)
app.include_router(sample_router)

for middleware in MIDDLEWARES:
    app.add_middleware(middleware)
