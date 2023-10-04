﻿from fastapi import FastAPI
from app.routers.batches import route
from app.schemas.core import Tags
from app.database.database import database
from app.routers.ingredients import ingredients_router

app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

app.include_router(ingredients_router, prefix="/api/v1", tags=[Tags.items])
app.include_router(route, prefix="/api/v1", tags=[Tags.items])


@app.on_event("startup")
async def startup_event():
   await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()