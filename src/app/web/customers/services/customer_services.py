import inspect
import json
import traceback
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 
from starlette.status import (
    HTTP_400_BAD_REQUEST,
)
from sqlalchemy.future import select

from ..dto import request_model
from ..dao import db_model
from ..repository import customer_repository



async def create_customer(
    session: AsyncSession,
    customer_model: request_model.CreateCustomer,
):

    customer = await customer_repository.create_customer(
        session=session, customer_model=customer_model
    )
    return customer


async def get_customer_by_id(session: AsyncSession, id: int):
    
    customer_details = await customer_repository.get_customer_by_id(
        id=id, session=session
    )
    if customer_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer does not exist for this ID: {id}",
        )
    
    return customer_details


async def get_customer_by_search_criteria(
    session: AsyncSession,
    search_criteria: request_model.SearchCriteriaCustomer,
):
    offset = (search_criteria.current_page - 1) * search_criteria.page_size
    limit = search_criteria.page_size

    query_statement = generate_customer_query_statement(
        search_criteria=search_criteria,
        offset=offset,
        limit=limit
    )
    
    customer_list = await customer_repository.get_customer_by_search_criteria(
        search_criteria=search_criteria,
        query_statement=query_statement,
        session=session,
    )
    
    total_customer = len(customer_list)
    
    last_page = True
    if total_customer == limit:
        last_page = False

    final_obj = {"customer_list": customer_list, "is_last_page": last_page}

    return final_obj


def generate_customer_query_statement(
    search_criteria: request_model.SearchCriteriaCustomer,
    offset: int,
    limit: int,
):

    query_statement = select(
        db_model.Customers
    )

    if search_criteria.email != None:
        query_statement = query_statement.where(
            db_model.Customers.email == search_criteria.email)
    
    query_statement = query_statement.offset(offset).limit(limit)
    
    return query_statement


async def update_customer(
    session: AsyncSession,
    customer_model: request_model.UpdateCustomer,
):
    customer_details = await customer_repository.get_customer_by_id(
        id=customer_model.id, session=session
    )
    if customer_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer does not exist for this ID: {customer_model.id}",
        )
    
    update_data = await customer_repository.update_customer(
        session=session,
        customer_model=customer_model, 
        dbo=customer_details
    )

    return update_data
