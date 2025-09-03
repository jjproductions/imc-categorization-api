from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    post_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    card_id = Column(Integer, nullable=True)
    category_id = Column(Integer, nullable=False)
    type_id = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    memo = Column(String, nullable=True)
    report_id = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=False, default=0)
