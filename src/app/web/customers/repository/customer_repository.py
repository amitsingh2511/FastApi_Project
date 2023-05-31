from typing import List
from urllib import response
from fastapi import HTTPException
from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import and_
from sqlalchemy import between, or_, true
from sqlalchemy.orm import aliased
from sqlalchemy import select, func, update
import sqlalchemy as db
import inspect

from ..dto import request_model
from ..dao import db_model


async def create_customer(
    session: AsyncSession,
    customer_model: request_model.CreateCustomer,
):
    db_customer = db_model.Customers.from_orm(customer_model)
    session.add(db_customer)
    await session.commit()
    await session.refresh(db_customer)
    return db_customer

    
async def get_customer_by_id(session: AsyncSession, id: int):
    
    query_statement = select(db_model.Customers).where(
        db_model.Customers.id == id
    )
    result = await session.execute(query_statement)
    response = result.scalars().first()
    return response

async def get_customer_by_search_criteria(
    session: AsyncSession,
    query_statement: BaseModel,
    search_criteria: request_model.SearchCriteriaCustomer,
):
    result = await session.execute(query_statement)
    customer = result.scalars().all()
    return customer


async def update_customer(
    session: AsyncSession,
    dbo: db_model.Customers,
    customer_model: request_model.UpdateCustomer,
):
         
    for key, value in customer_model.__dict__.items():
        if value is not None:
            setattr(dbo, key, value)
    session.add(dbo)
    await session.commit()
    await session.refresh(dbo)
    return dbo
