from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Expense(BaseModel):
    id: int
    description: str
    amount: float
    category: str

# Stored proc to get expenses
class ExpensesSP(Expense):
    transaction_date: datetime
    post_date: datetime
    card_number: int
    type: str
    created: datetime
    memo: Optional[str] = None
    report_id: Optional[int] = None
    receipt_url: Optional[str] = None

    class Config:
        from_attributes = True
