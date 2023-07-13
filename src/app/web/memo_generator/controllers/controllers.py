from app.web.db import get_session
from ..dto import request_model
from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.ext.asyncio.session import AsyncSession
import json
from app.config.config import get_settings
from typing import Optional
from fastapi import UploadFile 
from fastapi.param_functions import File
from ..services import services

router = APIRouter()


@router.post(
    "", status_code=200
)
@version(1)
async def upload_images(
    image_model: request_model.CreateImage = Depends(request_model.CreateImage.as_form),
    file: Optional[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
):
    
    response = await services.upload_images(
        image_model=image_model, 
        file=file,
        session=session,
    )
    
    return response



@router.get(
    "/{id}", status_code=200
)
@version(1)
async def download_images(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    response = await services.download_images(
        session=session, id=id
    )
    return response


@router.get("", status_code=200)
@version(1)
async def get_images_list(
    search_criteria: request_model.SearchCriteria = Depends(),
    session: AsyncSession = Depends(get_session),
):
    
    customer_list = await services.get_images_list(
        session=session, search_criteria=search_criteria
    )
    return customer_list
