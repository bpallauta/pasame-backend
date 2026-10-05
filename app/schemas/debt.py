from pydantic import BaseModel
from typing import List

class DebtCreate(BaseModel):
    debtor_name: str
    amount: float

class SendChargeRequest(BaseModel):
    debts: List[DebtCreate]

class SendChargeResponse(BaseModel):
    message: str
    debts_created: int
