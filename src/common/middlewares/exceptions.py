import traceback

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from common.exceptions import RequestException, DatabaseException
from common.settings import MIDDLEWARES
from vars import global_variables


class ExceptionResponse(BaseModel):
    detail: str


class ExceptionMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except (RequestException, DatabaseException) as e:
            traceback.print_exc()
            exception_response = ExceptionResponse(detail=str(e))
            status_code = 400
            if isinstance(e, RequestException):
                status_code = e.status_code
            return JSONResponse(content=jsonable_encoder(exception_response), status_code=status_code)

        return response


MIDDLEWARES.append(ExceptionMiddleware)
