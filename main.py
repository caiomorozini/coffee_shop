from fastapi import FastAPI
from endpoints import route
from schemas import Tags
from database import database

app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

app.include_router(route, prefix="/api/v1/items", tags=[Tags.items])

@app.on_event("startup")
async def startup_event():
   await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()