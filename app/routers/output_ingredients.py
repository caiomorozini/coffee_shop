from fastapi import (
    Query, Path, Body, Header, Response, status, HTTPException,
    APIRouter
)
from typing import Union, List, Annotated
from app.schemas.output_ingredient import OutputIngredient, OutputIngredientResponse
from app.database.database import database, output_table


output_ingredients_router = \
    APIRouter(prefix="/output-ingredients")


@output_ingredients_router.post("/")
async def create_ingredient(
        ingredient: OutputIngredient = Body(
            ...,
            **OutputIngredient.model_config,
            openapi_examples={
                "normal": {
                    "summary": "Um exemplo normal",
                    "description": "Um exemplo normal",
                    "value": {
                        "id_ingredient": 1,
                        "quantity": 4,
                        "date": 15/12/2023,
                    }
                },
                "invalid": {
                    "summary": "Um exemplo inválido",
                    "description": "Um exemplo inválido",
                    "value": {
                        "id_ingredient": 1,
                        "quantity": "quatro",
                        "date": 15/12/2023,
                    },
                },
            }
        )) -> OutputIngredientResponse:

    # Cria comando SQL para inserir o lote e executa
    query = output_table.insert().values(
        **ingredient.model_dump(exclude_unset=True))
    last_record_id = await database.execute(query)

    return OutputIngredientResponse(
        id=last_record_id, **ingredient.model_dump()
    )

@output_ingredients_router.get(
    "/",
    # tags=[Tags.items, Tags.users],
    summary="Mostra os ingredientes",
    response_description="A lista de ingredientes registrados",
    response_model=List[OutputIngredientResponse],
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

    query = output_table.select().limit(limit)
    if recent is True:
        query = output_table.select().order_by(
            output_table.c.created_at.desc()).limit(limit)

    return await database.fetch_all(query)

@output_ingredients_router.get(
    "/{ingredient_id}",
    summary="Mostra um único ingrediente pelo ID",
    response_description="Detalhes do ingrediente",
    response_model=OutputIngredientResponse,
)
async def mostrar_item(
    ingredient_id: int = Path(..., title="ID da entrada"),
) -> OutputIngredientResponse:
    """
    Mostra os detalhes de um ingrediente.
    Returns:
        Detalhes do ingrediente.
    """
    # Consultar o banco de dados para obter o ingrediente com base no ID
    ingredient_exists = await database.fetch_one(
        output_table.select().where(
        output_table.c.id == ingredient_id)
    )

    # Se o ingrediente não for encontrado, levanta uma exceção HTTP 404 Not Found
    if not ingredient_exists:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente não encontrado",
        )

    query = output_table.select().where(
        output_table.c.id == ingredient_id)

    return await database.fetch_one(query)

@output_ingredients_router.put("/{output_id}")
async def update_output(
        output_id: int = Path(..., title="ID da entrada"),
        ingredient: OutputIngredient = Body(
            ...,
            **OutputIngredient.model_config
        )) -> OutputIngredientResponse:

    ingredient_exists = await database.fetch_one(
        output_table.select().where(output_table.c.id == output_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )
    await database.execute(
        output_table.update().where(output_table.c.id == output_id).values(
            **ingredient.model_dump(exclude_unset=True))
    )

    return OutputIngredientResponse(
        id=output_id, **ingredient.model_dump()
    )

@output_ingredients_router.delete(
    "/{output_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    )
async def delete_output(
        output_id: int = Path(..., title="ID do ingrediente"),
        ):

    ingredient_exists = await database.fetch_one(
        output_table.select().where(
            output_table.c.id == output_id)
    )
    if not ingredient_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingrediente não existe",
        )

    await database.execute(
        output_table.delete().where(
            output_table.c.id == output_id)
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
