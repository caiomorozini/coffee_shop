from fastapi import FastAPI
from app.routers.batches import route
from app.schemas.core import Tags
from app.database.database import database
from app.routers.ingredients import ingredients_router
from app.routers.input_ingredients import input_ingredients_router
from app.routers.output_ingredients import output_ingredients_router
from app.routers.products import products_router
from app.routers.orders import orders_router

app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

app.include_router(orders_router, prefix="/api/v1", tags=["orders"])
app.include_router(products_router, prefix="/api/v1", tags=["products"])
app.include_router(output_ingredients_router, prefix="/api/v1", tags=["output_ingredients"])
app.include_router(input_ingredients_router, prefix="/api/v1", tags=["input_ingredients"])
app.include_router(ingredients_router, prefix="/api/v1", tags=["ingredients"])
app.include_router(route, prefix="/api/v1", tags=["batches"])


@app.on_event("startup")
async def startup_event():
   await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()