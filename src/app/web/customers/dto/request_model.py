from http.client import HTTPException
from typing import Optional
from pydantic import BaseModel, conint
from sqlmodel.main import SQLModel
from fastapi import Query
from pydantic import BaseModel


 

class CreateCustomer(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    pincode: int
    state: str
    district: str

    class Config:
        orm_mode = True


class SearchCriteriaCustomer(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    mobile_number: Optional[str]

    page_size: Optional[int] = Query(
        20, strict=True, ge=20, le=200, multiple_of=10
    )
    current_page: Optional[int] = Query(1, strict=True, ge=1)

    class Config:
        orm_mode = True


class UpdateCustomer(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    mobile_number: Optional[str]
    pincode: Optional[int]
    state: Optional[str]
    district: Optional[str]

    class Config:
        orm_mode = True