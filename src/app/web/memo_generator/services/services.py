import PIL
import boto3
from PIL import Image
from fastapi.datastructures import UploadFile
import json
import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import HTTPException
from starlette.responses import FileResponse
from fastapi import HTTPException, status 

from ..dto import request_model
from ..dao import db_model
from ..repository import repository

IMAGE_DIRECTORY ="./app/images/"
DEFAULT_IMAGE_DIRECTORY = "./app/default_image_directory/no_image_available.jpeg"


async def upload_images(
    image_model: request_model.CreateImage,
    file: UploadFile,
    session: AsyncSession,
):
    try:        
        im = Image.open(file.file)
        im = im.resize((150, 150))
        im.save(IMAGE_DIRECTORY +file.filename) 
        setattr(image_model, "file", file.filename)
        db_memo = db_model.MemoGenerator.from_orm(image_model)
        session.add(db_memo)
        await session.commit()
        await session.refresh(db_memo)

    except Exception as e:
        print(" e==",e)
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()
        im.close()
        return "Image Uploaded Successfully."


async def download_images(
    session: AsyncSession,
    id: int,
):
    image_details = await repository.get_imagge_details_by_id(
        session=session, id=id
    )
    if image_details is None:
        return FileResponse(DEFAULT_IMAGE_DIRECTORY)
    try:
        return FileResponse(
            IMAGE_DIRECTORY+image_details.file,  
        )
    except Exception as error:
        print("exception===========", error)
        return FileResponse(DEFAULT_IMAGE_DIRECTORY)
    


async def get_images_list(
    session: AsyncSession,
    search_criteria: request_model.SearchCriteria,
):
    offset = (search_criteria.current_page - 1) * search_criteria.page_size
    limit = search_criteria.page_size

    query_statement = generate_query_statement(
        search_criteria=search_criteria,
        offset=offset,
        limit=limit
    )
    
    image_list = await repository.get_images_list(
        search_criteria=search_criteria,
        query_statement=query_statement,
        session=session,
    )
    
    total_image = len(image_list)
    
    last_page = True
    if total_image == limit:
        last_page = False

    final_obj = {"list": image_list, "is_last_page": last_page}

    return final_obj


def generate_query_statement(
    search_criteria: request_model.SearchCriteria,
    offset: int,
    limit: int,
):
    query_statement = select(
        db_model.MemoGenerator
    )
    query_statement = query_statement.offset(offset).limit(limit)
    return query_statement
