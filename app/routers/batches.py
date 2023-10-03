from fastapi import (
    Query,
    Path, Body, Header, Response, status, Form, File,
    UploadFile, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.batch import Batch, BatchResponse
from app.database.database import database, batches



route = APIRouter()

@route.post("/")
async def create_item(
    batch: Batch = Body(
        ...,
        **Batch.model_config,
        openapi_examples={
            "normal": {
                "summary": "Um exemplo normal",
                "description": "Um exemplo normal",
                "value": {
                    "purchase": "01/01/2021",
                    "expiration": "01/01/2022",
                    "manufacturing": "01/01/2021",
                }
            },
            "invalid": {
                "summary": "Um exemplo inválido",
                "description": "Um exemplo inválido",
                "value": {
                    "purchase": "01/01/2021",
                    "expiration": "01/01/2020",
                    "manufacturing": "01/01/2021",
                },
            },
            "isoformat": {
                "summary": "Um exemplo inválido",
                "description": "Um exemplo inválido",
                "value": {
                    "purchase": "2021-01-01T00:00:00",
                    "expiration": "2020-01-01T00:00:00",
                    "manufacturing": "2021-01-01T00:00:00",
                },
            },
        }
    )) -> BatchResponse:

    # Checando se o lote já existe
    query = batches.select().where(
        (batches.c.purchase == batch.purchase) &
        (batches.c.expiration == batch.expiration) &
        (batches.c.manufacturing == batch.manufacturing)
    )
    batch_exists = await database.fetch_one(query)

    if batch_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lote já existe"
        )

    # Cria comando SQL para inserir o lote e executa
    query = batches.insert().values(**batch.model_dump())
    last_record_id = await database.execute(query)

    return BatchResponse(id=last_record_id, **batch.model_dump())


@route.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os cafés registrados",
    response_description="A lista de cafés registrados",
    response_model=List[BatchResponse],
)
async def mostrar_items(
    query: list = Query(
        default_factory=list,
        title="Query string",
        description="Query string para filtrar os items",
        alias="abc",
        ),
    limit: int = Query(default=10, ge=1, le=50),
    recent: bool = False
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    query = batches.select().limit(limit)
    if recent is True:
        query = batches.select().order_by(batches.c.id.desc()).limit(limit)

    return await database.fetch_all(query)
