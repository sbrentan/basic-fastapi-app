from datetime import datetime
from typing import Optional

from enum import Enum
from sqlmodel import SQLModel, Field


class TransactionType(str, Enum):
    PAYCHECK = "paycheck"
    FUND = "fund"
    BILL = "bill"
    HOUSE_BILL = "house_bill"
    OTHER = "other"


class TransferType(str, Enum):
    IN = "in"
    OUT = "out"


class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    amount: float
    datetime: datetime
    transfer_type: TransferType
    transaction_type: TransactionType
    description: Optional[str] = None
