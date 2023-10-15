from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.input_ingredients import InputIngredient, InputIngredientResponse
from app.database.database import database, input_table

input_ingredients_router = APIRouter(prefix="/input-ingredients")

@input_ingredients_router.post("/")
async def create(
        ingredient: InputIngredient = Body(
            ...,
            **InputIngredient.model_config,
        )) -> InputIngredientResponse:

    # Cria comando SQL para inserir o lote e executa
    query = input_table.insert().values(
        **ingredient.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return InputIngredientResponse(
        id=last_record_id, **ingredient.model_dump()
    )

@input_ingredients_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os ingredientes",
    response_description="A lista de ingredientes registrados",
    response_model=List[InputIngredientResponse],
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
    Returns:
        Retorna ingredientes comprados
    """

    query = input_table.select().limit(limit)
    if recent is True:
        query = input_table.select().order_by(
            input_table.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)

@input_ingredients_router.get(
    "/{ingredient_id}",
    summary="Mostra um único ingrediente pelo ID",
    response_description="Detalhes do ingrediente",
    response_model=InputIngredientResponse,
)
async def mostrar_item(
    ingredient_id: int = Path(..., title="ID da entrada"),
) -> InputIngredientResponse:
    """
    Mostra os detalhes de um ingrediente.
    Returns:
        Detalhes do ingrediente.
    """
    # Consultar o banco de dados para obter o ingrediente com base no ID
    ingredient_exists = await database.fetch_one(
        input_table.select().where(
        input_table.c.id == ingredient_id)
    )

# Se o ingrediente não for encontrado, levanta uma exceção HTTP 404 Not Found
    if not ingredient_exists:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente não encontrado",
        )

    query = input_table.select().where(
            input_table.c.id == ingredient_id)

    return await database.fetch_one(query)

@input_ingredients_router.put("/{input_id}")
async def update_input(
        input_id: int = Path(..., title="ID da entrada"),
        ingredient: InputIngredient = Body(
            ...,
            **InputIngredient.model_config
        )) -> InputIngredientResponse:
    ingredient_exists = await database.fetch_one(
        input_table.select().where(input_table.c.id == input_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    await database.execute(
        input_table.update().where(input_table.c.id == input_id).values(
            **ingredient.model_dump(exclude_unset=True))
    )

    return InputIngredientResponse(
        id=input_id, **ingredient.model_dump()
    )

@input_ingredients_router.delete(
    "/{input_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    )
async def delete_input(
        input_id: int = Path(..., title="ID do ingrediente"),
):
    ingredient_exists = await database.fetch_one(
        input_table.select().where(
            input_table.c.id == input_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )

    await database.execute(
        input_table.delete().where(
            input_table.c.id == input_id)
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
