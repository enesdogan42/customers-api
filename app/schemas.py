from pydantic import BaseModel, Field
from typing import Optional

class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    address: Optional[str] = None
    phone: str = Field(..., min_length=6, max_length=20)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=6, max_length=20)

class CustomerRead(CustomerBase):
    id: int

    class Config:
        from_attributes = True


from typing import List

class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int

class CustomerListResponse(BaseModel):
    items: List[CustomerRead]
    page: PaginationMeta

