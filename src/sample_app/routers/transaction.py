import logging

from fastapi import APIRouter, Depends

from common import RequestException
from common.schemas.models.message import SuccessMessage
from database import get_db, AppDatabase
from sample_app.schemas.crud.transaction import TransactionCreate
from sample_app.schemas.models import Transaction

router = APIRouter(
    prefix="/transactions",
    tags=["transaction"]
)


@router.post("", response_model=Transaction, status_code=201, summary="Create a new transaction",
             description="Create a new transaction", response_description="The created transaction")
async def create_transaction(new_transaction: TransactionCreate, db: AppDatabase = Depends(get_db)):
    transaction = Transaction(**new_transaction.model_dump())
    result = await db.transaction.create(transaction)
    return result


@router.get("", response_model=list[Transaction], summary="Read all transactions",
            description="Read all transactions", response_description="List of all transactions")
async def read_transactions(db: AppDatabase = Depends(get_db)):
    result = await db.transaction.filter()
    return result


@router.get("/{transaction_id}", response_model=Transaction, summary="Read a transaction",
            description="Read a transaction", response_description="The requested transaction")
async def read_transaction(transaction_id: int, db: AppDatabase = Depends(get_db)):
    result = await db.transaction.get(transaction_id)
    return result


@router.put("/{transaction_id}", response_model=Transaction, summary="Update a transaction",
            description="Update a transaction", response_description="The updated transaction")
async def update_transaction(transaction_id: int, new_transaction: TransactionCreate,
                             db: AppDatabase = Depends(get_db)):
    old_transaction = await db.transaction.get(transaction_id)
    if old_transaction is None:
        raise RequestException(f"Transaction with id {transaction_id} not found", 404)
    updatable_fields = TransactionCreate.model_fields
    for field_name, field in updatable_fields.items():
        try:
            setattr(old_transaction, field_name, getattr(new_transaction, field_name))
        except AttributeError:
            pass
    result = await db.transaction.update(old_transaction)
    return result


@router.delete("/{transaction_id}", response_model=SuccessMessage, summary="Delete a transaction",
               description="Delete a transaction", response_description="True if the transaction was deleted")
async def delete_transaction(transaction_id: int, db: AppDatabase = Depends(get_db)):
    result = await db.transaction.delete(transaction_id)
    return SuccessMessage(success=result, message="Transaction deleted", data={"transaction_id": transaction_id})
