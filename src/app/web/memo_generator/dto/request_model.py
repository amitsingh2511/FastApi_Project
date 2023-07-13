from http.client import HTTPException
from typing import Optional
from pydantic import BaseModel, conint
from sqlmodel.main import SQLModel
from fastapi.param_functions import Query, Form
from pydantic import BaseModel


class CreateImage(BaseModel):
    name: str
    file: Optional[str]

    @classmethod
    def as_form(
        cls,
        name = Form(None),
    ):
        return cls(
            name = name,
        )
    
    class Config:
        orm_mode = True


class SearchCriteria(BaseModel):
    page_size: Optional[int] = Query(
        20, strict=True, ge=20, le=200, multiple_of=10
    )
    current_page: Optional[int] = Query(1, strict=True, ge=1)

    class Config:
        orm_mode = True
