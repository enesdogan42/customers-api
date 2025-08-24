from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models, schemas
from typing import List, Optional, Tuple


# CREATE
def create_customer(db: Session, data: schemas.CustomerCreate) -> models.Customer:
    customer = models.Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

# READ (by id)
def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.get(models.Customer, customer_id)

def get_customers(
    db: Session,
    phone: Optional[str] = None,
    name: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> Tuple[List[models.Customer], int]:
    """
    Retourneert (items, total) met filters:
      - phone: exact match
      - name: case-insensitive deelmatch
    """
    # 1) basisselectie + filters
    base = select(models.Customer)
    if phone:
        base = base.where(models.Customer.phone == phone)
    if name:
        base = base.where(func.lower(models.Customer.full_name).like(f"%{name.lower()}%"))

    # 2) total veilig tellen via subquery (werkt stabiel in SA 2.x)
    base_subq = base.subquery()
    total = db.scalar(select(func.count()).select_from(base_subq))

    # 3) items ophalen met order + paginatie
    stmt = base.order_by(models.Customer.id.desc()).offset(offset).limit(limit)
    items = db.execute(stmt).scalars().all()

    return items, (total or 0)

# UPDATE
def update_customer(db: Session, customer_id: int, data: schemas.CustomerUpdate) -> Optional[models.Customer]:
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(customer, k, v)
    db.commit()
    db.refresh(customer)
    return customer

# DELETE
def delete_customer(db: Session, customer_id: int) -> bool:
    customer = get_customer(db, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True
