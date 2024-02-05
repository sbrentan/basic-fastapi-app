from pydantic import BaseModel

from common.schemas.crud.common import create_crud_model, CRUD
from funder.schemas.models import Transaction


TransactionCreate: BaseModel = create_crud_model(
    Transaction,
    CRUD.CREATE,
    excluded=["id"],
)
