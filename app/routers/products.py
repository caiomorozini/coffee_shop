from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.product import Product, ProductResponse
from app.database.database import database, products


products_router = APIRouter(prefix="/products")


@products_router.post("/")
async def create_pruduct(
        product: Product = Body(
            ...,
            **Product.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "café com leite",
                        "price": 10.9,
                        "descript": "Com o café passado, acrescentar 100ml de leite",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "café com leite",
                        "price": "dez e noventa",
                        "descript": "Com o café passado, acrescentar 100ml de leite",
                    },
                },
            }
        )) -> ProductResponse:

    # Checando se ingredient já existe
    query = products.select().where(
        (products.c.name == product.name)
    )
    product_exists = await database.fetch_one(query)

    if product_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto já existe",
        )

    # Cria comando SQL para inserir o lote e executa
    query = products.insert().values(
        **product.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return ProductResponse(
        id=last_record_id, **product.model_dump()
    )


@products_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os produtos",
    response_description="A lista de produtos registrados",
    response_model=List[ProductResponse],
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

    query = products.select().limit(limit)
    if recent is True:
        query = products.select().order_by(
            products.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)

@products_router.get(
    "/{product_id}",
    summary="Mostra um único produto pelo ID",
    response_description="Detalhes do produto",
    response_model=ProductResponse,
)
async def mostrar_item(
    product_id: int = Path(..., title="ID da entrada"),
) -> ProductResponse:
    """
    Mostra os detalhes de um ingrediente.
    Returns:
        Detalhes do ingrediente.
    """
    # Consultar o banco de dados para obter o ingrediente com base no ID
    product_exists = await database.fetch_one(
        products.select().where(
        products.c.id == product_id)
    )

    # Se o ingrediente não for encontrado, levanta uma exceção HTTP 404 Not Found
    if not product_exists:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado",
        )

    query = products.select().where(
        products.c.id == product_id)

    return await database.fetch_one(query)

@products_router.put("/{product_id}")
async def update_ingredient(
        product_id: int = Path(..., title="ID do produto"),
        product: Product = Body(
            ...,
            **Product.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "name": "café com leite",
                        "price": 10.9,
                        "descript": "Com o café passado, acrescentar 100ml de leite",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "name": "café com leite",
                        "price": "dez e noventa",
                        "descript": "Com o café passado, acrescentar 100ml de leite",
                    }
                },
            }
        )) -> ProductResponse:
    product_exists = await database.fetch_one(
        products.select().where(products.c.id == product_id)
    )
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product não existe",
        )
    await database.execute(
        products.update().where(products.c.id == product_id).values(
            **product.model_dump(exclude_unset=True))
    )

    return ProductResponse(
        id=product_id, **product.model_dump()
    )

@products_router.delete("/{product_id}")
async def update_product(
        product_id: int = Path(..., title="ID do produto"),
):
    product_exists = await database.fetch_one(
        products.select().where(products.c.id == product_id)
    )
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não existe",
        )
    await database.execute(
        products.delete().where(
            products.c.id == product_id)
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


