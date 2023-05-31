from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.param_functions import File
from fastapi_versioning import version
from sqlalchemy.ext.asyncio.session import AsyncSession
import json

from app.config.config import get_settings
from app.web.db import get_session
from ..dto import request_model
from ..services import customer_services


router = APIRouter()


@router.post(
    "",
    status_code=201,
)
@version(1)
async def create_customer(
    customer_model: request_model.CreateCustomer,
    session: AsyncSession = Depends(get_session),
):
    customer = await customer_services.create_customer(
        session=session, customer_model=customer_model
    )
    return customer


@router.get("/{id}", status_code=200)
@version(1)
async def get_customer_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):

    customer = await customer_services.get_customer_by_id(
        session=session, id=id
    )
    return customer


@router.get("", status_code=200)
@version(1)
async def get_customer_by_search_criteria(
    search_criteria: request_model.SearchCriteriaCustomer = Depends(),
    session: AsyncSession = Depends(get_session),
):
    
    customer_list = await customer_services.get_customer_by_search_criteria(
        session=session, search_criteria=search_criteria
    )
    return customer_list


@router.put(
    "/{id}",
    status_code=200
)
@version(1)
async def update_customer(
    id: int,
    customer_model: request_model.UpdateCustomer,
    session: AsyncSession = Depends(get_session),
):
    setattr(customer_model, "id", id)

    update_data = await customer_services.update_customer(
        session=session, customer_model=customer_model
    )
    return update_data
