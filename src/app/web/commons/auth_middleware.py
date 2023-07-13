import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import BackgroundTasks, HTTPException
from starlette.responses import JSONResponse
import requests
import json
from app.web.db import get_session, async_session
import base64
from starlette.datastructures import URL
from app.web.customers.repository import customer_repository
 

from app.config.config import get_settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        email = request.headers.get("email", None)

        swagger_documentation_urls = ["/docs", "openapi.json", "/redoc"]
        if any(ext in str(request.url) for ext in swagger_documentation_urls):
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
        if email is None:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        async with async_session() as session:
            validate_email = await customer_repository.get_customer_by_email(
                session=session,email=email
            )
            if validate_email is None:
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
        response = await call_next(request)
        return response
        
