from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .db import engine
from .deps import get_db

# Tabellen aanmaken (demo). In productie: migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customers API", version="1.0.0")

# Health
@app.get("/health")
def health():
    return {"status": "ok"}


# LIST + SEARCH (met paginatie + name-zoek)
@app.get("/customers", response_model=schemas.CustomerListResponse)
def list_customers(
    phone: Optional[str] = None,
    name: Optional[str] = None,   # zoeken op deel van naam
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    items, total = crud.get_customers(db, phone=phone, name=name, limit=limit, offset=offset)
    return {
        "items": items,
        "page": {"total": total, "limit": limit, "offset": offset},
    }


# GET BY ID
@app.get("/customers/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

# CREATE
@app.post("/customers", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_customer(db, payload)
    except Exception as e:
        # bijv. unique phone constraint
        raise HTTPException(status_code=400, detail=str(e))

# UPDATE (PATCH)
@app.patch("/customers/{customer_id}", response_model=schemas.CustomerRead)
def patch_customer(customer_id: int, payload: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    customer = crud.update_customer(db, customer_id, payload)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

# DELETE
@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_customer(customer_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_customer(db, customer_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return None
