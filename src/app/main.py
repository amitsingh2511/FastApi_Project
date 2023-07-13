import asyncio
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from starlette.middleware import Middleware
from fastapi_versioning import VersionedFastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import get_settings
from sqlalchemy.orm import Session
import time
import os
import uvicorn

from app.web.db import disconnect_db
from app.web.customers.controllers import customer_controllers
from app.web.memo_generator.controllers import controllers
from app.web.commons.auth_middleware import AuthMiddleware


origins = [
    "http://localhost:8002",
    "https://localhost:8002",
    "http://localhost:3001",
    "http://localhost",
    "*",
]

middlewares = [
    # Setup CORS
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    # Enable GZip
    Middleware(GZipMiddleware, minimum_size=1000),
    # Setup Trusted Host
    Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
    # Auth
    Middleware(AuthMiddleware)
]

app = FastAPI(title="FastApi-Curd", middleware=middlewares)


app.include_router(
    customer_controllers.router, prefix="/customers", tags=["/customers"]
)

app.include_router(
    controllers.router, prefix="/image", tags=["/image"]
)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/fastapi-project/v{major}",
    middleware=middlewares,
)


@app.on_event("startup")
async def on_startup():
    print("App started.....")
    

@app.on_event("shutdown")
async def shutdown():
    print("App shutdown....")
    
    await disconnect_db()
