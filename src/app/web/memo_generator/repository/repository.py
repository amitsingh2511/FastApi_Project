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

async def get_imagge_details_by_id(
    session: AsyncSession,
    id: int
):
    query_statement = select(db_model.MemoGenerator).where(
        db_model.MemoGenerator.id == id
    )
    result = await session.execute(query_statement)
    response = result.scalars().first()
    return response


async def get_images_list(
    session: AsyncSession,
    query_statement: BaseModel,
    search_criteria: request_model.SearchCriteria,
):
    result = await session.execute(query_statement)
    customer = result.scalars().all()
    return customer
