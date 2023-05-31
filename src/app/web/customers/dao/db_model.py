from typing import Optional
from sqlmodel import Field, SQLModel, Column, DateTime
from datetime import datetime


class Customers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    first_name: str
    last_name: str
    email: Optional[str]
    mobile_number: str
    pincode: int
    state: str
    district: str

    is_active: bool = Field(default=True) 
    created_on: datetime = Field(default_factory=datetime.utcnow)
    modified_on: Optional[datetime] = Field(
        sa_column=Column(
            "modified_on",
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )

    class Config:
        orm_mode = True

