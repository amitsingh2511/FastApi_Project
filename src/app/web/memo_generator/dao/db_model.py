from typing import Optional
from sqlmodel import Field, SQLModel, Column, DateTime
from datetime import datetime


class MemoGenerator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    file: str

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