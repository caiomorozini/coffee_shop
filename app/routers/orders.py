from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.order import Order, OrderResponse
from app.database.database import database, orders, products


orders_router = APIRouter(prefix="/orders")


@orders_router.post("/")
async def create_order(
        order: Order = Body(
            ...,
            **Order.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "products": [1],
                        "observations": "Não colocar canela no capuccino",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "products": 1,
                        "observations": "Não colocar canela no capuccino",
                    }
                },
            }
        )) -> OrderResponse:
    for id_product in order.products:
        product_exists = await database.fetch_one(
            products.select().where(products.c.id == id_product)
        )
        if not product_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {id_product} não existe",
            )
        continue

    # Cria comando SQL para inserir o lote e executa
    query = orders.insert().values(
        **order.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return OrderResponse(
        id=last_record_id, **order.model_dump()
    )

@orders_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os pedidos",
    response_description="A lista de pedidos registrados",
    response_model=List[OrderResponse],
)
async def mostrar_pedidos(
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

    - **products**: list with product ids
    - **price**: required
    - **description**: a long description
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

    query = orders.select().limit(limit)
    if recent is True:
        query = orders.select().order_by(
            orders.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)

@orders_router.get(
    "/{order_id}",
    summary="Mostra um único pedido pelo ID",
    response_description="Detalhes do pedido",
    response_model=OrderResponse,
)
async def mostrar_pedido(
    order_id: int = Path(..., title="ID da entrada"),
) -> OrderResponse:
    """
    Mostra os detalhes de um ingrediente.
    Returns:
        Detalhes do ingrediente.
    """
    # Consultar o banco de dados para obter o ingrediente com base no ID
    order_exists = await database.fetch_one(
        orders.select().where(
        orders.c.id == order_id)
    )

    # Se o ingrediente não for encontrado, levanta uma exceção HTTP 404 Not Found
    if not order_exists:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente não encontrado",
        )
    query = orders.select().where(
        orders.c.id == order_id)

    return await database.fetch_one(query)

@orders_router.put("/{order_id}")
async def update_order(
        order_id: int = Path(..., title="ID do pedido"),
        order: Order = Body(
            ...,
            **Order.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "products": [1],
                        "observations": "Não colocar canela no capuccino",
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "products": 1,
                        "observations": "Não colocar canela no capuccino",
                    }
                },
            }
        )) -> OrderResponse:
    order_exists = await database.fetch_one(
        orders.select().where(orders.c.id == order_id)
    )
    if not order_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não existe",
        )
    await database.execute(
        orders.update().where(orders.c.id == order_id).values(
            **order.model_dump(exclude_unset=True))
    )

    return OrderResponse(
        id=order_id, **order.model_dump()
    )

@orders_router.delete("/{order_id}")
async def delete_order(
        order_id: int = Path(..., title="ID do ingrediente"),
):
    order_exists = await database.fetch_one(
        orders.select().where(orders.c.id == order_id)
    )
    if not order_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não existe",
        )
    await database.execute(
        orders.delete().where(
            orders.c.id == order_id)
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

