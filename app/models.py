from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=False, unique=True, index=True)

    __table_args__ = (
        UniqueConstraint("phone", name="uq_customers_phone"),
    )
