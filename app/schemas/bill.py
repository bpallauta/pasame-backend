from pydantic import BaseModel
from typing import List, Optional

class BillItemSchema(BaseModel):
    name: str
    quantity: int = 1
    price: int

class BillResultSchema(BaseModel):
    restaurant: str
    date: str
    items: List[BillItemSchema]
    subtotal: int
    tax: int = 0
    discount: int = 0
    tip: int = 0
    total: int
