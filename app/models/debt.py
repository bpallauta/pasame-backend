from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, index=True) # Usually ForeignKey("bills.id")
    debtor_id = Column(Integer, index=True) # Usually ForeignKey("users.id")
    creditor_id = Column(Integer, index=True) 
    amount = Column(Float, nullable=False)
    status = Column(String, default="PENDING") # PENDING, PAID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
